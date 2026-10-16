#!/usr/bin/env python3
"""four_experts.py — ask four experts and Dave (the control) one question, each on its own engine.

    run   "<question>" [--question-file F] [--out DIR] [--needs-web] [--needs-shell] [--timeout S] [--only IDS]
          [--claude-by-caller]   inside Claude Code: do not start `claude -p`; list Dave (and any 范蠡 fallback)
                                 for the caller's subagents
    check DIR [--sabotage]

Experts and engines (EJ, 2026-10-13):
    Linus Torvalds  codex  gpt-6.1-sol (read-only)
    范蠡            agy    gemini-3.8-flash-medium — falls back to Claude Opus 5.5 when the task needs web or shell
                           (agy headless cannot), or when agy returns nothing, an error, a timeout, or an answer
                           without the required sections (e.g. a plan instead of the answer)
    孫子            dsh    deepseek-flash (dsh headless)
    老子            opencode  minimax-coding-plan/MiniMax-M3.1-Flash-Preview (plan mode)
    Dave            claude Opus 5.5 — the control (EJ, 2026-10-13): experiments, data, nature-inspired solutions;
                    his rules are EJ's, in assets/seats/. EJ chose a persona control over a plain no-persona answer.

Each expert gets its own list from the four-seats run (copied into DIR/seats/, because opencode cannot read files
outside the project) and a brief that makes it decide through its numbered rules. Prompts go in files; every engine
call reads stdin from /dev/null. `check` verifies each expert cited only item numbers its list has and quoted Chinese
only as its list writes it; `--sabotage` proves the check fails on an invented quote and a non-existent item.
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
REPO = HERE.parent.parent.parent  # the skill lives in <repo>/.claude/skills/four-experts
SEATS_ROOT = Path(os.environ.get("FOUR_EXPERTS_SEATS", REPO / "runs" / "20261013-four-seats")).expanduser()
EXPERTS = [  # id, name, engine
    ("linus", "Linus Torvalds", "codex"),
    ("fan-li", "范蠡 (Fan Li)", "agy"),
    ("sun-tzu", "孫子 (Sun Tzu)", "dsh"),
    ("lao-tzu", "老子 (Laozi)", "opencode"),
    ("dave", "Dave", "claude"),  # the control seat, EJ 2026-10-13: experiments, data, nature-inspired; rules in assets/seats
]
MODELS = {"codex": "gpt-6.1-sol", "agy": "gemini-3.8-flash-medium", "dsh": "deepseek-flash (dsh headless profile)",
          "opencode": "minimax-coding-plan/MiniMax-M3.1-Flash-Preview", "claude": "claude-opus-5-5"}
SECTIONS = ["## Answer", "## How I decided", "## What I need to know", "## Costs and risks",
            "## How we would know I was right"]
ITEM_START = re.compile(r"^(?:### (\d{1,2})\. |(\d{1,2})\. \*\*)", re.M)
CJK_RUN = re.compile(r"[㐀-鿿]{4,}")
ITEM_CITE = re.compile(r"(?<![\w#])#(\d{1,3})\b")


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


def command(engine: str, prompt: str, out_file: Path, timeout: int, web: bool, shell: bool) -> list[str]:
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
        return ["claude", "-p", "--model", MODELS["claude"], "--output-format", "text",
                f"--allowedTools={','.join(tools)}", prompt]
    raise ValueError(engine)


def start(engine: str, prompt: str, ans: Path, log: Path, timeout: int, web: bool, shell: bool, cwd: Path):
    env = dict(os.environ)
    if engine == "claude":
        env.pop("ANTHROPIC_API_KEY", None)  # use the subscription login, not an API key
    cmd = ["timeout", str(timeout), *command(engine, prompt, ans, timeout, web, shell)]
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


def progress(a, piece: str, state: str, note: str) -> None:
    """One timestamped line per expert start and end (workflow-design method 3.8 item 14; guard Round 10 T4)."""
    if not a.progress:
        return
    line = f"- {dt.datetime.now().astimezone().isoformat(timespec='seconds')} · {piece} · {state} · {note}\n"
    with open(a.progress, "a", encoding="utf-8") as f:
        f.write(line)


def run(a) -> int:
    question = Path(a.question_file).read_text(encoding="utf-8") if a.question_file else a.question
    if not question or not question.strip():
        sys.exit("no question given")
    cwd = Path.cwd()
    out = Path(a.out) if a.out else (cwd / ("runs" if (cwd / "runs").is_dir() else "four-experts")
                                     / f"{dt.date.today():%Y%m%d}-four-experts-{slug(question)}")
    out = out.resolve()
    if not str(out).startswith(str(cwd.resolve())):
        print(f"warning: {out} is outside {cwd}; opencode cannot read it", file=sys.stderr)
    for d in ("seats", "briefs", "answers", "logs"):
        (out / d).mkdir(parents=True, exist_ok=True)
    (out / "question.md").write_text(question.strip() + "\n", encoding="utf-8")
    brief_t = (HERE / "assets" / "brief.md").read_text(encoding="utf-8")
    only = set(a.only.split(",")) if a.only else None
    jobs = {}
    for sid, name, engine in EXPERTS:
        lst, ident = out / "seats" / f"{sid}-list.md", out / "seats" / f"{sid}-identity.md"
        if only and sid not in only:
            continue
        src_list, src_ident = seat_files(sid)
        shutil.copyfile(src_list, lst)
        shutil.copyfile(src_ident, ident)
        brief = out / "briefs" / f"{sid}.md"
        brief.write_text(brief_t.format(name=name, list_path=lst, identity_path=ident, n_items=n_items(lst),
                                        question=question.strip()), encoding="utf-8")
        jobs[sid] = {"expert": name, "engine": engine, "brief": brief}
    if (a.needs_web or a.needs_shell) and "fan-li" in jobs:
        jobs["fan-li"].update(engine="claude", fallback_from="agy",
                              fallback_reason="task needs " + " and ".join(
                                  x for x, f in (("web", a.needs_web), ("shell", a.needs_shell)) if f))
    old = out / "status.json"
    status = json.loads(old.read_text(encoding="utf-8")) if only and old.exists() else {}

    def prompt_for(sid, engine):
        p = f"Read {jobs[sid]['brief']} and do what it says."
        if engine == "agy":
            p += " Do not run shell commands and do not fetch URLs. Write the answer itself as your final message, not a plan."
        return p

    def hand_to_caller(sid):
        status[sid] = {"expert": jobs[sid]["expert"], "engine": "claude-subagent (caller)", "model": "caller's choice",
                       "ok": None, "problem": "to run by the caller",
                       "brief": str(jobs[sid]["brief"]), "answer": str(out / "answers" / f"{sid}.md"),
                       **({k: jobs[sid][k] for k in ("fallback_from", "fallback_reason") if k in jobs[sid]})}
        print(f"CALLER  {sid:8} run a Claude subagent: 'Read {jobs[sid]['brief']} and do what it says.' "
              f"and save its final message to {out / 'answers' / (sid + '.md')}", flush=True)

    procs = {}
    for sid, j in jobs.items():
        if j["engine"] == "claude" and a.claude_by_caller:
            hand_to_caller(sid)
            continue
        ans, log = out / "answers" / f"{sid}.md", out / "logs" / f"{sid}.log"
        procs[sid] = (*start(j["engine"], prompt_for(sid, j["engine"]), ans, log, a.timeout, a.needs_web,
                             a.needs_shell, cwd), ans, log)
        j["started"] = dt.datetime.now().astimezone().isoformat(timespec="seconds")
        progress(a, sid, "start", j["engine"])
        print(f"started {sid:8} on {j['engine']}", flush=True)
    while procs:
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
            status[sid] = {"expert": j["expert"], "engine": j["engine"], "model": MODELS[j["engine"]],
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
        time.sleep(2)
    (out / "status.json").write_text(json.dumps(status, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{out}\nnext: python3 {Path(__file__)} check {out}")
    return 0 if all(s["ok"] is not False for k, s in status.items() if k != "fan-li-agy") else 1
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
        sid = next(s for s in answers if s in {x for x, _, _ in EXPERTS} and CJK_RUN.search(answers[s]))
        t = answers[sid]
        m = CJK_RUN.search(t)
        t = t[:m.start() + 1] + "鑫" + t[m.start() + 2:] + "\nAs my #99 says."
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
