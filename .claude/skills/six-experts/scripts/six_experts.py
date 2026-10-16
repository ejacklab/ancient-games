#!/usr/bin/env python3
"""six_experts.py — ask six experts one question, each on its own engine: four researched personas, Dave (rules and
the project's insights) and Dario (the plain control).

    run   "<question>" [--question-file F] [--out DIR] [--needs-web] [--needs-shell] [--timeout S] [--only IDS]
          [--claude-by-caller]   inside Claude Code: do not start `claude -p`; list Dave (and any 范蠡 fallback)
                                 for the caller's subagents
    check DIR [--sabotage]

Experts and engines (EJ, 2026-10-13):
    Linus Torvalds  codex  gpt-6.1-sol (read-only) — runs on opencode instead when Codex has 20% or less left in
                           its 5-hour or weekly window (EJ, 2026-10-16; read from Codex's own session log), or when
                           Codex stops on its usage limit
    范蠡            agy    gemini-3.8-flash-medium — falls back to Claude Opus 5.5 when the task needs web or shell
                           (agy headless cannot), or when agy returns nothing, an error, a timeout, or an answer
                           without the required sections (e.g. a plan instead of the answer)
    孫子            dsh    deepseek-flash (dsh headless)
    老子            opencode  minimax-coding-plan/MiniMax-M3.1-Flash-Preview (plan mode)
    Dave            claude Sonnet 5.5 — EJ's ten rules (assets/seats/; experiments, data, nature-inspired), and since
                    2026-10-16 the project's insights: the guard's insight index and the named categories' sections
    Dario           claude Sonnet 5.5 — the plain control (EJ, 2026-10-16): no rules, no identity, no insights; the
                    same model and tools as Dave, so Dave against Dario measures what the rules and insights add

Each persona gets its own list from the four-seats run (copied into DIR/seats/, because opencode cannot read files
outside the project) and a brief that makes it decide through its numbered rules; Dario gets only the question and the
answer's shape. Prompts go in files; every engine
call reads stdin from /dev/null. `check` verifies each persona cited only item numbers its list has and quoted Chinese
only as its list writes it, Dave cited real insight ids (or said none applies), and Dario wrote the five sections; `--sabotage` proves the check fails on an invented quote and a non-existent item.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
REPO = HERE.parent.parent.parent  # the skill lives in <repo>/.claude/skills/six-experts
SEATS_ROOT = Path(os.environ.get("SIX_EXPERTS_SEATS") or os.environ.get("FOUR_EXPERTS_SEATS")
                  or REPO / "runs" / "20261013-four-seats").expanduser()
EXPERTS = [  # id, name, engine
    ("linus", "Linus Torvalds", "codex"),
    ("fan-li", "范蠡 (Fan Li)", "agy"),
    ("sun-tzu", "孫子 (Sun Tzu)", "dsh"),
    ("lao-tzu", "老子 (Laozi)", "opencode"),
    ("dave", "Dave", "claude"),  # EJ 2026-10-13: experiments, data, nature-inspired; rules in assets/seats; loads insights
    ("dario", "Dario", "claude"),  # the plain control, EJ 2026-10-16: no rules, no identity, no insights; same engine as Dave
]
PLAIN = {"dario"}
# Dave and Dario on the same model, so their comparison isolates the rules and insights (run 20261016-six-experts, D2).
SEAT_MODEL = {"dave": "claude-sonnet-5-5", "dario": "claude-sonnet-5-5"}
INSIGHT_SEAT = "dave"  # loads the insights before answering
GUARD_CLI = HERE.parent / "workflow-design" / "guard" / "src" / "cli.ts"
INSIGHT_ID = re.compile(r"\bF-[0-9a-f]{8}\b")  # seats with no list: their brief is the question alone, and check reads their sections only
MODELS = {"codex": "gpt-6.1-sol", "agy": "gemini-3.8-flash-medium", "dsh": "deepseek-flash (dsh headless profile)",
          "opencode": "minimax-coding-plan/MiniMax-M3.1-Flash-Preview", "claude": "claude-opus-5-5"}
SECTIONS = ["## Answer", "## How I decided", "## What I need to know", "## Costs and risks",
            "## How we would know I was right"]
ITEM_START = re.compile(r"^(?:### (\d{1,2})\. |(\d{1,2})\. \*\*)", re.M)
CJK_RUN = re.compile(r"[㐀-鿿]{4,}")
ITEM_CITE = re.compile(r"(?<![\w#])#(\d{1,3})\b")
CODEX_MIN_LEFT = 20  # percent; at or below it Linus runs on opencode (EJ, 2026-10-16)
CODEX_LIMIT_ERROR = "usage limit"  # Codex: "You've hit your usage limit ... try again at <time>"


def final_list(text: str) -> str:
    m = re.search(r"^## Final list\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


def n_items(list_file: Path) -> int:
    nums = [int(a or b) for a, b in ITEM_START.findall(final_list(list_file.read_text(encoding="utf-8")))]
    return max(nums) if nums else 0


def seat_files(sid: str) -> tuple[Path, Path]:
    if sid == "dave":
        return HERE / "assets" / "seats" / "dave-list.md", HERE / "assets" / "seats" / "dave-identity.md"
    return SEATS_ROOT / "final-opus" / f"{sid}.md", SEATS_ROOT / "identity" / f"{sid}.md"


def slug(q: str) -> str:
    words = re.findall(r"[a-z0-9]+", q.lower())[:5]
    return "-".join(words) or "question"


def codex_left(home: Path | None = None, now: float | None = None) -> float | None:
    """Percent Codex has left: the lower of its windows, from the newest rate-limit snapshot in its session logs.

    A window whose reset time has passed counts as full. None when no log holds a snapshot with a window."""
    home = home or Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    now = time.time() if now is None else now
    logs = sorted((home / "sessions").glob("*/*/*/*.jsonl"), key=lambda f: f.stat().st_mtime, reverse=True)
    for log in logs[:20]:
        snapshot = None
        for line in log.read_text(encoding="utf-8", errors="ignore").splitlines():
            if '"rate_limits"' not in line:
                continue
            try:
                limits = json.loads(line).get("payload", {}).get("rate_limits") or {}
            except (json.JSONDecodeError, AttributeError):
                continue
            windows = [w for w in (limits.get("primary"), limits.get("secondary")) if isinstance(w, dict)]
            if windows:
                snapshot = windows
        if snapshot:
            return min(100.0 if w.get("resets_at", 0) <= now else 100.0 - float(w.get("used_percent", 0))
                       for w in snapshot)
    return None


def command(engine: str, prompt: str, out_file: Path, timeout: int, web: bool, shell: bool,
            model: str | None = None) -> list[str]:
    if engine == "codex":
        return ["codex", "-m", MODELS["codex"], *(["--search"] if web else []), "exec", "-s", "read-only",
                "--skip-git-repo-check", "-o", str(out_file), prompt]
    if engine == "agy":
        return ["agy", "-p", prompt, "--mode", "plan", "--model", MODELS["agy"], "--print-timeout",
                f"{timeout - 60}s", "--output-format", "text"]
    if engine == "dsh":
        return ["dsh", "headless", prompt]
    if engine == "opencode":
        return ["opencode", "run", "-m", MODELS["opencode"], "--agent", "plan", prompt]
    if engine == "claude":
        tools = ["Read", "Grep", "Glob"] + (["WebSearch", "WebFetch"] if web else []) + (["Bash"] if shell else [])
        # `--allowedTools` takes several values, so the bare form swallows the prompt that follows it (run
        # 20261016-time-monitor: Dave got "Input must be provided"); `=` keeps the prompt an argument.
        return ["claude", "-p", "--model", model or MODELS["claude"], "--output-format", "text",
                f"--allowedTools={','.join(tools)}", prompt]
    raise ValueError(engine)


def start(engine: str, prompt: str, ans: Path, log: Path, timeout: int, web: bool, shell: bool, cwd: Path,
          model: str | None = None):
    env = dict(os.environ)
    if engine == "claude":
        env.pop("ANTHROPIC_API_KEY", None)  # use the subscription login, not an API key
    cmd = ["timeout", str(timeout), *command(engine, prompt, ans, timeout, web, shell, model)]
    out = open(log if engine == "codex" else ans, "w")
    err = open(log, "a" if engine == "codex" else "w")
    p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=out, stderr=err, cwd=cwd, env=env)
    return p, time.time()


def answer_ok(ans: Path) -> tuple[bool, str]:
    text = ans.read_text(encoding="utf-8", errors="ignore") if ans.exists() else ""
    if not text.strip():
        return False, "empty answer"
    missing = [s for s in SECTIONS if s not in text]
    return (False, f"missing sections {missing}") if missing else (True, "")


def guard_text(args: list[str], cwd: Path) -> str:
    """The guard's insight index or chosen sections, as text; "" when the guard cannot answer."""
    try:
        p = subprocess.run(["bun", str(GUARD_CLI), "insight", *args], cwd=cwd, capture_output=True, text=True,
                           timeout=60, stdin=subprocess.DEVNULL, env={**os.environ, "BUN_RUNTIME_TRANSPILER_CACHE_PATH": "0"})
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return p.stdout if p.returncode == 0 else ""


def insight_load(out: Path, categories: str | None, cwd: Path) -> str:
    """Dave's insights (run 20261016-six-experts, D1): the index, then the named categories' sections, copied into the
    run folder so every engine can read them; the brief section that tells him to load and cite them."""
    index = guard_text(["index"], cwd)
    (out / "seats" / "dave-insight-index.md").write_text(index or "(the guard gave no index)\n", encoding="utf-8")
    cats = [c.strip() for c in (categories or "").split(",") if c.strip()]
    sections = guard_text(["show", *[x for c in cats for x in ("--category", c)]], cwd) if cats else ""
    (out / "seats" / "dave-insights.md").write_text(sections or "(no category named: choose from the index)\n",
                                                   encoding="utf-8")
    named = ", ".join(cats) if cats else "none — choose from the index"
    return f"""
## Load first: what was learned

Before you answer, read the insights — six whys, root causes and fix options from past failures in this project.

- The index, one line per insight: `{out / 'seats' / 'dave-insight-index.md'}` (file, ids, check, source, category).
- The sections of the categories the main agent named ({named}): `{out / 'seats' / 'dave-insights.md'}`. You may add
  any other section from the index; read it in its file.
- In "How I decided", cite each insight you used as `<file>#<id>` and what it changed in your answer; if none applies,
  write `No insight applies: <why>`. If a named category was the wrong one, say so in one line.
"""


def progress(a, piece: str, state: str, note: str) -> None:
    """One timestamped line per expert start and end (workflow-design method 3.8 item 14; guard Round 10 T4)."""
    if not a.progress:
        return
    line = f"- {dt.datetime.now().astimezone().isoformat(timespec='seconds')} · {piece} · {state} · {note}\n"
    try:
        with open(a.progress, "a", encoding="utf-8") as f:
            f.write(line)
    except OSError as e:  # a progress line is a report, never a reason to drop the experts it reports on
        print(f"warning: progress line not written ({type(e).__name__})", file=sys.stderr)


def run(a) -> int:
    question = Path(a.question_file).read_text(encoding="utf-8") if a.question_file else a.question
    if not question or not question.strip():
        sys.exit("no question given")
    cwd = Path.cwd()
    out = Path(a.out) if a.out else (cwd / ("runs" if (cwd / "runs").is_dir() else "six-experts")
                                     / f"{dt.date.today():%Y%m%d}-six-experts-{slug(question)}")
    out = out.resolve()
    if not str(out).startswith(str(cwd.resolve())):
        print(f"warning: {out} is outside {cwd}; opencode cannot read it", file=sys.stderr)
    for d in ("seats", "briefs", "answers", "logs"):
        (out / d).mkdir(parents=True, exist_ok=True)
    if a.progress:  # made before any expert starts (review finding 1)
        Path(a.progress).parent.mkdir(parents=True, exist_ok=True)
    (out / "question.md").write_text(question.strip() + "\n", encoding="utf-8")
    brief_t = (HERE / "assets" / "brief.md").read_text(encoding="utf-8")
    plain_t = (HERE / "assets" / "brief-plain.md").read_text(encoding="utf-8")
    only = set(a.only.split(",")) if a.only else None
    jobs = {}
    for sid, name, engine in EXPERTS:
        lst, ident = out / "seats" / f"{sid}-list.md", out / "seats" / f"{sid}-identity.md"
        if only and sid not in only:
            continue
        brief = out / "briefs" / f"{sid}.md"
        if sid in PLAIN:  # the control gets the question and the answer's shape, nothing else
            brief.write_text(plain_t.format(question=question.strip()), encoding="utf-8")
            jobs[sid] = {"expert": name, "engine": engine, "brief": brief}
            continue
        src_list, src_ident = seat_files(sid)
        shutil.copyfile(src_list, lst)
        shutil.copyfile(src_ident, ident)
        text = brief_t.format(name=name, list_path=lst, identity_path=ident, n_items=n_items(lst),
                              question=question.strip())
        if sid == INSIGHT_SEAT:
            text += insight_load(out, a.insights, cwd)
        brief.write_text(text, encoding="utf-8")
        jobs[sid] = {"expert": name, "engine": engine, "brief": brief}
    if (a.needs_web or a.needs_shell) and "fan-li" in jobs:
        jobs["fan-li"].update(engine="claude", fallback_from="agy",
                              fallback_reason="task needs " + " and ".join(
                                  x for x, f in (("web", a.needs_web), ("shell", a.needs_shell)) if f))
    if "linus" in jobs:
        left = codex_left()
        if left is not None and left <= CODEX_MIN_LEFT:
            jobs["linus"].update(engine="opencode", fallback_from="codex",
                                 fallback_reason=f"codex has {left:g}% left ({CODEX_MIN_LEFT}% or less)")
    old = out / "status.json"
    status = json.loads(old.read_text(encoding="utf-8")) if only and old.exists() else {}

    def prompt_for(sid, engine):
        p = f"Read {jobs[sid]['brief']} and do what it says."
        if engine == "agy":
            p += " Do not run shell commands and do not fetch URLs. Write the answer itself as your final message, not a plan."
        return p

    def hand_to_caller(sid):
        model = SEAT_MODEL.get(sid)  # Dave and Dario keep their model under the caller too (review #4)
        status[sid] = {"expert": jobs[sid]["expert"], "engine": "claude-subagent (caller)", "model": model or "caller's choice",
                       "ok": None, "problem": "to run by the caller",
                       "brief": str(jobs[sid]["brief"]), "answer": str(out / "answers" / f"{sid}.md"),
                       **({k: jobs[sid][k] for k in ("fallback_from", "fallback_reason") if k in jobs[sid]})}
        print(f"CALLER  {sid:8} run a Claude subagent{' on ' + model if model else ''}: 'Read {jobs[sid]['brief']} and do what it says.' "
              f"and save its final message to {out / 'answers' / (sid + '.md')}", flush=True)
        progress(a, sid, "start", "handed to the caller")
        if a.progress:  # the caller writes the end line, since this script never sees the subagent finish
            print(f"        when it ends, append: - <date -Iseconds> · {sid} · done|fail · caller  to {a.progress}",
                  flush=True)

    procs = {}
    waiting = []  # opencode runs wait for each other: parallel starts can fail with "database is locked"

    def launch(sid):
        j = jobs[sid]
        ans, log = out / "answers" / f"{sid}.md", out / "logs" / f"{sid}.log"
        procs[sid] = (*start(j["engine"], prompt_for(sid, j["engine"]), ans, log, a.timeout, a.needs_web,
                             a.needs_shell, cwd, **seat_model(sid, j["engine"])), ans, log)
        j["started"] = dt.datetime.now().astimezone().isoformat(timespec="seconds")
        progress(a, sid, "start", j["engine"])
        print(f"started {sid:8} on {j['engine']}", flush=True)

    def seat_model(sid, engine):  # only a Claude seat with its own model passes one; other calls keep their shape
        model = SEAT_MODEL.get(sid) if engine == "claude" else None
        return {"model": model} if model else {}

    def opencode_busy():
        return any(jobs[sid]["engine"] == "opencode" for sid in procs)

    for sid, j in jobs.items():
        if j["engine"] == "claude" and a.claude_by_caller:
            hand_to_caller(sid)
            continue
        if j["engine"] == "opencode" and opencode_busy():
            waiting.append(sid)
            print(f"waiting {sid:8} for the running opencode expert", flush=True)
            continue
        launch(sid)
    while procs or waiting:
        if waiting and not opencode_busy():
            launch(waiting.pop(0))
        for sid, (p, t0, ans, log) in list(procs.items()):
            if p.poll() is None:
                continue
            del procs[sid]
            j = jobs[sid]
            ok, why = answer_ok(ans)
            if p.returncode == 124:
                ok, why = False, f"timeout after {a.timeout} s"
            elif p.returncode != 0 and ok:
                ok, why = False, f"exit {p.returncode}"
            progress(a, sid, "done" if ok else "fail", f"{j['engine']} exit {p.returncode}")
            status[sid] = {"expert": j["expert"], "engine": j["engine"], "model": (SEAT_MODEL.get(sid) if j["engine"] == "claude" else None) or MODELS[j["engine"]],
                           "started": j.get("started"),
                           "finished": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
                           "exit": p.returncode, "seconds": round(time.time() - t0, 1), "ok": ok, "problem": why,
                           **({"fallback_from": j["fallback_from"], "fallback_reason": j["fallback_reason"]}
                              if "fallback_from" in j else {})}
            print(f"done    {sid:8} on {j['engine']:8} exit {p.returncode} {'ok' if ok else 'FAILED: ' + why}",
                  flush=True)
            if sid == "fan-li" and j["engine"] == "agy" and not ok:
                shutil.move(ans, ans.with_suffix(".agy-failed.md")) if ans.exists() else None
                shutil.move(log, log.with_suffix(".agy-failed.log")) if log.exists() else None
                status["fan-li-agy"] = status.pop("fan-li")
                j.update(engine="claude", fallback_from="agy", fallback_reason=f"agy failed: {why}")
                if a.claude_by_caller:
                    hand_to_caller(sid)
                    continue
                procs[sid] = (*start("claude", prompt_for(sid, "claude"), ans, log, a.timeout, a.needs_web,
                                     a.needs_shell, cwd), ans, log)
                j["started"] = dt.datetime.now().astimezone().isoformat(timespec="seconds")
                progress(a, sid, "start", "claude (fallback)")
                print("started fan-li   on claude (fallback)", flush=True)
            if (sid == "linus" and j["engine"] == "codex" and not ok and log.exists()
                    and CODEX_LIMIT_ERROR in log.read_text(encoding="utf-8", errors="ignore")):
                shutil.move(ans, ans.with_suffix(".codex-failed.md")) if ans.exists() else None
                shutil.move(log, log.with_suffix(".codex-failed.log"))
                status["linus-codex"] = status.pop("linus")
                j.update(engine="opencode", fallback_from="codex", fallback_reason="codex stopped on its usage limit")
                if opencode_busy():  # one opencode at a time (database is locked)
                    waiting.append(sid)
                    print("waiting linus    for the running opencode expert (fallback)", flush=True)
                else:
                    launch(sid)
        time.sleep(2)
    (out / "status.json").write_text(json.dumps(status, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{out}\nnext: python3 {Path(__file__)} check {out}")
    return 0 if all(s["ok"] is not False for k, s in status.items() if k not in ("fan-li-agy", "linus-codex")) else 1
    # with --only, earlier entries in status.json are kept and the new ones added


def nearest(run_: str, allowed: str) -> str:
    """The closest same-length passage in the list, so a script change (趙/赵) reads differently from an invention."""
    best, at = len(run_) + 1, -1
    for i in range(len(allowed) - len(run_) + 1):
        d = sum(a != b for a, b in zip(run_, allowed[i:i + len(run_)]))
        if d < best:
            best, at = d, i
    if at < 0 or best > len(run_) // 3:
        return " (no close passage in the list)"
    return f" (nearest in the list: {allowed[at:at + len(run_)]}, {best} character(s) differ)"


def check_one(sid: str, text: str, out: Path) -> list[str]:
    bad = [f"{sid}: missing section {s}" for s in SECTIONS if s not in text]
    if sid in PLAIN:  # no list to cite from: the sections are the whole check
        return bad
    index = out / "seats" / "dave-insight-index.md"
    if sid == INSIGHT_SEAT and index.exists():  # Dave loaded insights: he cites real ones, or says none applies
        known = set(INSIGHT_ID.findall(index.read_text(encoding="utf-8")))
        cited = set(INSIGHT_ID.findall(text))
        if cited - known:
            bad.append(f"{sid}: cites insight ids not in the index: {', '.join(sorted(cited - known))}")
        if not cited and "No insight applies" not in text:
            bad.append(f"{sid}: loaded insights but cites none and does not say why none applies")
    lst = out / "seats" / f"{sid}-list.md"
    n = n_items(lst)
    allowed = re.sub(r"\s+", "", lst.read_text(encoding="utf-8") +
                     (out / "seats" / f"{sid}-identity.md").read_text(encoding="utf-8"))
    for c in sorted({int(x) for x in ITEM_CITE.findall(text)}):
        if not 1 <= c <= n:
            bad.append(f"{sid}: cites #{c}, but its list has items 1–{n}")
    for run_ in CJK_RUN.findall(text):
        if run_ not in allowed:
            bad.append(f"{sid}: Chinese not found in its list: {run_[:30]}{nearest(run_, allowed)}")
    if not ITEM_CITE.search(text):
        bad.append(f"{sid}: cites no item at all")
    return bad


def check(a) -> int:
    out = Path(a.dir).resolve()
    answers = {p.stem: p.read_text(encoding="utf-8", errors="ignore") for p in (out / "answers").glob("*.md")
               if "." not in p.stem}
    if a.sabotage:
        listed = [s for s in answers if s in {x for x, _, _ in EXPERTS} and s not in PLAIN]
        sid = next((s for s in listed if CJK_RUN.search(answers[s])), listed[0] if listed else None)
        if sid is None:
            print("sabotage: no persona answer to alter")
            return 1
        t = answers[sid]
        m = CJK_RUN.search(t)
        if m:  # alter one quoted character and cite a missing item
            t = t[:m.start() + 1] + "鑫" + t[m.start() + 2:] + "\nAs my #99 says."
        else:  # no Chinese to alter (review #3): cite a missing item and drop a required section instead
            t = t.replace("## Answer", "## Answr", 1) + "\nAs my #99 says."
        found = check_one(sid, t, out)
        print(f"sabotage on {sid}: altered one quoted character and cited #99 → {len(found)} failure(s)")
        for f in found:
            print("  ", f)
        return 0 if len(found) >= 2 else 1
    bad = []
    for sid, _, _ in EXPERTS:
        if sid not in answers:
            bad.append(f"{sid}: no answer file")
    ids = {sid for sid, _, _ in EXPERTS}
    for sid, text in sorted(answers.items()):
        if sid not in ids:
            print(f"skip {sid}: not one of the current experts (kept as evidence, not checked)")
            continue
        bad += check_one(sid, text, out)
    for b in bad:
        print("FAIL", b)
    summary = f"{'PASS' if not bad else 'FAIL'}: {len(answers)} answers, {len(bad)} failure(s)"
    print(summary)
    (out / "check.txt").write_text("\n".join(["FAIL " + b for b in bad] + [summary]) + "\n", encoding="utf-8")
    return 0 if not bad else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("question", nargs="?")
    r.add_argument("--question-file")
    r.add_argument("--out")
    r.add_argument("--needs-web", action="store_true", help="the task needs web search: 范蠡 goes to Claude")
    r.add_argument("--needs-shell", action="store_true", help="the task needs a shell: 范蠡 goes to Claude")
    r.add_argument("--timeout", type=int, default=1800, help="seconds per engine call")
    r.add_argument("--insights", help="the insight categories Dave loads, comma-separated (e.g. spec,own-work); "
                                      "with none named he chooses from the index")
    r.add_argument("--progress", help="append a timestamped line per expert start and end to this file "
                                      "(e.g. runs/<run>/nodes/experts.progress.md)")
    r.add_argument("--only", help="comma-separated ids to run (e.g. dave or linus,dave); with --out, adds them to an "
                   "existing run and keeps its other answers")
    r.add_argument("--claude-by-caller", action="store_true",
                   help="inside Claude Code: leave Dave and any 范蠡 fallback to the caller's subagents")
    c = sub.add_parser("check")
    c.add_argument("dir")
    c.add_argument("--sabotage", action="store_true")
    a = ap.parse_args()
    return run(a) if a.cmd == "run" else check(a)


if __name__ == "__main__":
    sys.exit(main())
