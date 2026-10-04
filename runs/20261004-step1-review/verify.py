"""Join the four step-1 reviews mechanically.

The point is to make the engines' claims checkable rather than persuasive:

* every finding must name one of the five artifacts, and its QUOTE must actually appear in that file — a quote that
  is not there is discarded unread, however plausible the finding sounds;
* findings that land on the same place in the same file are clustered, so corroboration is counted rather than
  asserted: "three of four engines independently said this" is evidence, one engine saying it is a lead.

Run: python3 verify.py
"""
import pathlib
import re
import sys
from collections import defaultdict

HERE = pathlib.Path(__file__).parent
ROOT = pathlib.Path("/home/smoke01/dev/ancient-games")

# The step-1 artifacts, and the line window that counts as "step 1" for each.
ARTIFACTS = {
    ".claude/skills/workflow-design/SKILL.md": (43, 75),
    "docs/WORKFLOW_DESIGN_METHOD.md": (72, 167),
    ".claude/skills/workflow-design/scripts/readiness.py": (1, 10_000),
    "docs/WORKFLOW_DESIGN_DIAGRAM.md": (54, 99),
    "docs/workflow-templates/readiness.md": (1, 10_000),
}
ENGINES = ["codex", "claude", "agy", "opencode"]
TOLERANCE = 4                       # a quote this many lines from the stated line still counts as located

FINDING = re.compile(
    r"FINDING\s*(\d+)\s*:\s*(?P<file>[^\s|]+?)\s*:\s*(?P<line>\d+)\s*\|\s*(?P<sev>high|med|low)\s*\|\s*"
    r"(?P<what>.+?)\s*\|\s*QUOTE:\s*(?P<quote>.+)", re.I)


def text_of(engine: str) -> str:
    for name in (f"{engine}.md", f"{engine}.out"):
        p = HERE / name
        if p.exists():
            return p.read_text(errors="replace")
    return ""


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().strip("`*_ ")).lower()


def locate(path: pathlib.Path, quote: str, claimed: int) -> tuple[str, int]:
    """('exact'|'near'|'elsewhere'|'missing', found_line)"""
    lines = path.read_text(errors="replace").splitlines()
    q = norm(quote)
    if not q:
        return "missing", 0
    # a quote may be trimmed by the engine, so accept a prefix match of decent length
    hits = [i + 1 for i, l in enumerate(lines) if q in norm(l) or (len(q) > 24 and norm(l).startswith(q[:40]))]
    if not hits:
        return "missing", 0
    nearest = min(hits, key=lambda h: abs(h - claimed))
    if claimed in hits:
        return "exact", claimed
    if abs(nearest - claimed) <= TOLERANCE:
        return "near", nearest
    return "elsewhere", nearest


def main() -> int:
    findings = []
    for engine in ENGINES:
        raw = text_of(engine)
        got = 0
        for m in FINDING.finditer(raw):
            f = m.group("file").strip().lstrip("./")
            cand = [k for k in ARTIFACTS if k.endswith(f) or f.endswith(pathlib.Path(k).name)]
            if not cand:
                findings.append({"engine": engine, "verdict": "off-artifact", "file": f,
                                 "line": int(m.group("line")), "sev": m.group("sev").lower(),
                                 "what": m.group("what").strip(), "quote": m.group("quote").strip(),
                                 "at": 0})
                continue
            key = cand[0]
            path = ROOT / key
            claimed = int(m.group("line"))
            verdict, at = locate(path, m.group("quote"), claimed) if path.exists() else ("missing", 0)
            lo, hi = ARTIFACTS[key]
            if verdict in ("exact", "near") and not (lo <= at <= hi):
                verdict = "outside-step1"
            findings.append({"engine": engine, "verdict": verdict, "file": key, "line": claimed,
                             "sev": m.group("sev").lower(), "what": m.group("what").strip(),
                             "quote": m.group("quote").strip(), "at": at})
            got += 1
        print(f"  {engine:9} findings parsed: {got}")

    kept = [f for f in findings if f["verdict"] in ("exact", "near")]
    dropped = [f for f in findings if f["verdict"] not in ("exact", "near")]

    # cluster: same file, located lines within 6 of each other
    clusters: list[dict] = []
    for f in sorted(kept, key=lambda x: (x["file"], x["at"])):
        hit = next((c for c in clusters if c["file"] == f["file"] and abs(c["at"] - f["at"]) <= 6), None)
        if hit:
            hit["engines"].add(f["engine"])
            hit["members"].append(f)
            hit["at"] = min(hit["at"], f["at"])
        else:
            clusters.append({"file": f["file"], "at": f["at"], "engines": {f["engine"]}, "members": [f]})
    clusters.sort(key=lambda c: (-len(c["engines"]), c["file"], c["at"]))

    print(f"\n=== {len(kept)} located findings in {len(clusters)} places "
          f"({len(dropped)} discarded) ===")
    for c in clusters:
        n = len(c["engines"])
        mark = "CORROBORATED" if n >= 2 else "single"
        print(f"\n[{mark} {n}/4] {c['file']}:{c['at']}  ({', '.join(sorted(c['engines']))})")
        for m in c["members"][:1]:
            print(f"    {m['sev']}: {m['what'][:150]}")
            print(f"    quote: {m['quote'][:110]}")
        if n >= 2:
            for m in c["members"][1:]:
                print(f"    also {m['engine']}: {m['what'][:120]}")

    if dropped:
        print("\n=== discarded (quote not found where claimed) ===")
        for f in dropped:
            print(f"  {f['engine']:9} {f['verdict']:14} {f['file']}:{f['line']}  {f['what'][:70]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
