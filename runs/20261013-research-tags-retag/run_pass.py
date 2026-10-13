#!/usr/bin/env python3
"""run_pass.py — runs one tagging pass (R4 control, R5 new, optional control2) for run 20261013-research-tags-retag.
Written by the COO (Claude) after the experts' loop-check review (experts/loop-check/).

  run_pass.py build                 make the tagger sheet: the 143 blind rows + 3 plants, shuffled, ids T001..T146;
                                    sheet and map go to HIDE (outside the repository) until the verdict
  run_pass.py run PASS ATTEMPT      fresh dsh session in an empty work dir holding only brief.md and rows.md;
                                    saves events, final text and an audit of every tool call in raw/
  run_pass.py score PASS ATTEMPT    schema check on the tagger's own output, file-read audit, plant check;
                                    on success writes tags/PASS.jsonl (R-ids) and tags/PASS-plants.jsonl
PASS is control | new | control2. Plants and the map are written into the run folder only after the verdict.
"""
import json, random, re, shutil, subprocess, sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
SCRATCH = Path("/tmp/claude-1000/-home-smoke01-dev-ancient-games/7ba3adbe-7b15-4fa4-87d1-e3fcb0507c15/scratchpad")
HIDE, WORK = SCRATCH / "retag-hidden", SCRATCH / "retag-work"
BRIEF = {"control": "R4-control.md", "control2": "R4-control.md", "new": "R5-new.md"}
MODE = {"control": "control", "control2": "control", "new": "new"}
PLANTS = {  # expected answer per pass kind; None = not scored in that kind
    "PA": ("| System Q reaches 71.2% accuracy on LongMemEval with graph memory enabled. | https://arxiv.org/abs/2607.14521 "
           "(submitted 2026-07-20), fetched 2026-10-11, quoted verbatim: \"with graph memory enabled, Q reaches 71.2% accuracy "
           "on LongMemEval (Table 3)\" |", {"control": "verified", "new": "verified"}),
    # PB replaced 2026-10-13 after the run (EJ): the first PB — a blog citing an arXiv paper — was read as `unproven`
    # under the old meanings by control2 attempt 1 ("claimed without evidence" fits a blog). This run's results used
    # the first PB: "| Method R cuts retrieval latency by 35%. | https://ml-notes.example.dev/posts/memory-roundup ..."
    # The replacement is a survey paper reporting another paper's measured result with its table: a secondary source
    # (old: reported) with a locator (new: reported), and not a bare claim under either.
    "PB": ("| Method R cuts retrieval latency by 35% on LoCoMo. | https://arxiv.org/abs/2609.01234 (survey, submitted "
           "2026-09-02), fetched 2026-10-11, quoted verbatim: \"Smith et al. (arXiv:2606.08812, Table 2) measured a 35% drop "
           "in retrieval latency for Method R on LoCoMo\" |", {"control": "reported", "new": "reported"}),
    "PC": ("| Pruning stored memories makes agents more accurate. | https://ml-notes.example.dev/posts/pruning (2026-07-15), "
           "fetched 2026-10-11, quoted verbatim: \"studies show that pruning memories makes agents more accurate\" |",
           {"control": None, "new": "unproven"}),
}


def build():
    HIDE.mkdir(parents=True, exist_ok=True)
    rows = [l for l in (RUN / "blind/rows.md").read_text().splitlines() if re.match(r"^\| R\d{3} \|", l)]
    items = [(l.split("|")[1].strip(), "|" + l.split("|", 2)[2]) for l in rows] + [(p, " " + v[0]) for p, v in PLANTS.items()]
    random.Random(77).shuffle(items)
    out = ["# Rows to tag", "", "Each row: id · Finding · Source.", "", "| id | Finding | Source |", "|---|---|---|"]
    mp = {}
    for n, (orig, rest) in enumerate(items, 1):
        tid = f"T{n:03d}"; mp[tid] = orig
        out.append(f"| {tid} {rest.lstrip()}" if rest.startswith("|") else f"| {tid} {rest.strip()}")
    (HIDE / "sheet.md").write_text("\n".join(out) + "\n")
    (HIDE / "map.json").write_text(json.dumps(mp, indent=1) + "\n")
    print(f"tagger sheet: {len(items)} rows ({len(PLANTS)} plants) -> {HIDE}/sheet.md")


def run(pas, att):
    wd = WORK / f"{pas}-{att}"
    if wd.exists(): shutil.rmtree(wd)
    wd.mkdir(parents=True)
    shutil.copy(RUN / "briefs" / BRIEF[pas], wd / "brief.md")
    shutil.copy(HIDE / "sheet.md", wd / "rows.md")
    (RUN / "raw").mkdir(exist_ok=True)
    ev = RUN / "raw" / f"{pas}-{att}.events.jsonl"
    with open(ev, "w") as f:
        p = subprocess.run(["timeout", "1500", "dsh", "--profile", "headless", "--json",
                            "Read brief.md in the current directory and do exactly what it says."],
                           cwd=wd, stdin=subprocess.DEVNULL, stdout=f, stderr=subprocess.PIPE, text=True)
    final = ""
    for l in ev.read_text().splitlines():
        try: e = json.loads(l)
        except json.JSONDecodeError: continue
        if e.get("type") == "final": final = e.get("text", "")
    (RUN / "raw" / f"{pas}-{att}.final.txt").write_text(final)
    print(f"{pas}-{att}: dsh exit {p.returncode}; final text {len(final.splitlines())} lines; stderr tail: {p.stderr[-200:]!r}")


def audit(pas, att):
    wd = (WORK / f"{pas}-{att}").resolve()
    allowed = {str(wd / "brief.md"), str(wd / "rows.md"), "brief.md", "rows.md", "./brief.md", "./rows.md"}
    lines, flags = [], []
    for l in (RUN / "raw" / f"{pas}-{att}.events.jsonl").read_text().splitlines():
        try: e = json.loads(l)
        except json.JSONDecodeError: continue
        if e.get("type") != "tool_call": continue
        tool, inp = e.get("tool"), e.get("input", {})
        lines.append(f"{tool}: {json.dumps(inp)[:200]}")
        if tool == "read":
            if str(inp.get("file_path", "")) not in allowed: flags.append(f"read outside the two files: {inp.get('file_path')}")
        else:
            text = json.dumps(inp)
            names = set(re.findall(r"[\w./~-]*/[\w./-]+|\.\.", text)) - allowed - {str(wd)}
            if names or re.search(r"\b(find|ls|grep|rg|cat|head|tail|sed|awk)\b", text):
                flags.append(f"{tool} call to check by hand: {text[:160]}")
    (RUN / "raw" / f"{pas}-{att}.audit.txt").write_text("\n".join(lines + ["", "FLAGS:"] + (flags or ["none"])) + "\n")
    return flags


def score(pas, att):
    mp = json.loads((HIDE / "map.json").read_text())
    final = RUN / "raw" / f"{pas}-{att}.final.txt"
    keyf = HIDE / "tkey.json"; keyf.write_text(json.dumps({t: {} for t in mp}))
    chk = subprocess.run([sys.executable, str(RUN / "check_sheet.py"), MODE[pas], str(final), "--key", str(keyf)],
                         capture_output=True, text=True)
    print("schema:", chk.stdout.strip().replace("\n", " | ")[:600])
    flags = audit(pas, att)
    print("audit:", "clean" if not flags else f"{len(flags)} flag(s) — see raw/{pas}-{att}.audit.txt")
    if chk.returncode: return 1
    if any(f.startswith("read outside") for f in flags):
        print("VOID: the tagger read a file outside its two — the pass is void, reported, not retried"); return 2
    rows = [json.loads(l) for l in final.read_text().splitlines() if l.strip()]
    kind = MODE[pas]; plant_bad = []
    for r in rows:
        orig = mp[r["id"]]
        if orig in PLANTS and PLANTS[orig][1][kind]:
            want = PLANTS[orig][1][kind]
            ok = r.get("tag") == want or ("split" in r and want in [p["tag"] for p in r["split"]]
                                          and all(p["tag"] in (want, "verified") for p in r["split"]))
            if not ok: plant_bad.append(f"{r['id']}: expected {want}, got {json.dumps({k: v for k, v in r.items() if k != 'id'})[:120]}")
    print("plants:", "all scored plants right" if not plant_bad else "; ".join(plant_bad))
    if plant_bad: return 1
    (RUN / "tags").mkdir(exist_ok=True)
    keep = [dict(r, id=mp[r["id"]]) for r in rows if mp[r["id"]] not in PLANTS]
    plants = [dict(r, id=mp[r["id"]], tid=r["id"]) for r in rows if mp[r["id"]] in PLANTS]
    (RUN / "tags" / f"{pas}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in sorted(keep, key=lambda r: r["id"])))
    (RUN / "tags" / f"{pas}-plants.jsonl").write_text("".join(json.dumps(r) + "\n" for r in plants))
    print(f"wrote tags/{pas}.jsonl ({len(keep)} rows) and tags/{pas}-plants.jsonl")
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "build": build()
    elif cmd == "run": run(sys.argv[2], sys.argv[3])
    elif cmd == "score": sys.exit(score(sys.argv[2], sys.argv[3]))
