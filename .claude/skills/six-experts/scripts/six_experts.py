#!/usr/bin/env python3
"""six_experts.py — ask six experts one question, each on its own engine: four researched personas, Dave (rules and
the project's insights) and Dario (the plain control).

    run   "<question>" [--question-file F] [--out DIR] [--needs-web] [--needs-shell] [--timeout S] [--only IDS]
          [--claude-by-caller]   inside Claude Code: do not start `claude -p`; list Dave (and any 范蠡 fallback)
                                 for the caller's subagents
    check DIR [--sabotage]

Experts and engines (EJ, 2026-10-13):
    Linus Torvalds  codex  gpt-6.1-sol (read-only) — runs on mcode instead when Codex has 20% or less left in
                           its 5-hour or weekly window (EJ, 2026-10-16; read from Codex's own session log), or when
                           Codex stops on its usage limit. mcode, not opencode: 老子 is on opencode, and opencode
                           cannot run twice at once (EJ, 2026-10-16). mcode runs lightweight (no tools, so it cannot
                           write), with the brief and its two files pasted in on stdin
    范蠡            agy    gemini-3.8-flash-medium — falls back to Claude Opus 5.5 when the task needs web or shell
                           (agy headless cannot), or when agy returns nothing, an error, a timeout, or an answer
                           without the required sections (e.g. a plan instead of the answer)
    孫子            dsh    deepseek-flash (dsh headless)
    老子            opencode  minimax-coding-plan/MiniMax-M3.1-Flash-Preview (plan mode)
    Dave            claude Opus 5.5 — EJ's ten rules (assets/seats/; experiments, data, nature-inspired), and since
                    2026-10-16 the project's insights: the guard's insight index and the named categories' sections
    Dario           claude Sonnet 5.5 — the plain control (EJ, 2026-10-16): no rules, no identity, no insights, the
                    same tools as Dave; since Dave moved to Opus, Dave against Dario also differs in model

Each persona gets its own list from the four-seats run (copied into DIR/seats/, because opencode cannot read files
outside the project) and a brief that makes it decide through its numbered rules; Dario gets only the question and the
answer's shape. Prompts go in files; every engine
call reads stdin from /dev/null, except mcode, which reads its prompt file on stdin. `check` verifies each persona cited only item numbers its list has and quoted Chinese
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
# Dave on Opus 5.5 (EJ, 2026-10-16, replacing the experts' advice in run 20261016-six-experts, D2), Dario on Sonnet 5.5;
# Dave against Dario therefore differs in model as well as in rules and insights.
SEAT_MODEL = {"dave": "claude-opus-5-5", "dario": "claude-sonnet-5-5"}
INSIGHT_SEAT = "dave"  # loads the insights before answering
GUARD_CLI = HERE.parent / "workflow-design" / "guard" / "src" / "cli.ts"
INSIGHT_ID = re.compile(r"\bF-[0-9a-f]{8}\b")  # seats with no list: their brief is the question alone, and check reads their sections only
MODELS = {"codex": "gpt-6.1-sol", "agy": "gemini-3.8-flash-medium", "dsh": "deepseek-flash (dsh headless profile)",
          "opencode": "minimax-coding-plan/MiniMax-M3.1-Flash-Preview", "claude": "claude-opus-5-5",
          "mcode": "minimax/MiniMax-M3.1-Flash-Preview"}
MCODE = os.environ.get("MCODE", str(Path.home() / ".minimax-code" / "bin" / "mcode"))  # not on a non-interactive PATH
SECTIONS = ["## Answer", "## How I decided", "## What I need to know", "## Costs and risks",
            "## How we would know I was right"]
VOTE_SECTIONS = ["## Answer", "## Why", "## What I need to know"]  # --vote (run 20261017-experts-speed-trial)
ITEM_START = re.compile(r"^(?:### (\d{1,2})\. |(\d{1,2})\. \*\*)", re.M)
CJK_RUN = re.compile(r"[㐀-鿿]{4,}")
ITEM_CITE = re.compile(r"(?<![\w#])#(\d{1,3})\b")
CODEX_MIN_LEFT = 20  # percent; at or below it Linus runs on mcode (EJ, 2026-10-16)
CODEX_LIMIT_ERROR = "usage limit"  # Codex: "You've hit your usage limit ... try again at <time>"


def final_list(text: str) -> str:
    m = re.search(r"^## Final list\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


def n_items(list_file: Path) -> int:
    nums = [int(a or b) for a, b in ITEM_START.findall(final_list(list_file.read_text(encoding="utf-8")))]
    return max(nums) if nums else 0


def rule_card(list_file: Path, identity_file: Path) -> str:
    """--card: who they are and one line per rule (its heading and its Rule's first sentence), without the quotes and
    sources; the full files stay in seats/ for `check` (run 20261017-experts-speed-trial, fix 1)."""
    body = final_list(list_file.read_text(encoding="utf-8"))
    starts = list(ITEM_START.finditer(body))
    lines = []
    for m, nxt in zip(starts, starts[1:] + [None]):
        chunk = body[m.start():nxt.start() if nxt else len(body)]
        head = chunk.splitlines()[0][m.end() - m.start():].strip().strip("*").strip()
        rule = re.search(r"\*\*Rule:\*\*\s*(.*?)(?=\n\s*- \*\*|\Z)", chunk, re.S)
        first = re.match(r".+?[.!?](?=\s|$)", " ".join(rule.group(1).split())) if rule else None
        lines.append(f"- #{m.group(1) or m.group(2)} **{head}**" + (f" — {first.group(0)}" if first else ""))
    who = re.search(r"^## Who they are\s*$(.*?)(?=^## |\Z)", identity_file.read_text(encoding="utf-8"), re.M | re.S)
    return f"### Who you are\n\n{who.group(1).strip() if who else ''}\n\n### Your rules\n\n" + "\n".join(lines) + "\n"


CARD_SECTION = """## Your rules — read nothing else

Your rules are below, one line each: the heading and the rule, without the quotes and sources (the main agent keeps
the full list for checking). Read nothing else: do not open your list or identity file, and open only the files the
question names, if any. Run no shell commands — no git, no ls, no search. Everything you need is here or in those
files.

{card}
"""


def swap(text: str, pattern: str, new: str) -> str:
    """Replace the one match of `pattern`; a brief template that no longer has it is an error, not a silent skip."""
    found = re.findall(pattern, text, re.M | re.S)
    if len(found) != 1:
        raise ValueError(f"brief template: expected one match of {pattern!r}, found {len(found)}")
    return re.sub(pattern, lambda _m: new, text, flags=re.M | re.S)


def card_brief(text: str, card: str) -> str:
    """--card: the rules in the brief instead of the two files, and no reading or shell beyond the question's files
    (fixes 1 and 5)."""
    text = swap(text, r"^## Read first\n.*?(?=^## )", CARD_SECTION.format(card=card) + "\n")
    text = swap(text, r"^3\. \*\*Quote only from your list,\*\*.*?(?=^4\. )",
                "3. **Quote nothing.** Your rules above hold no original words; cite them by number.\n")
    return swap(text, r"Re-read your list while you work", "Re-read your rules above while you work")


def vote_brief(text: str, name: str, why: str) -> str:
    """--vote: APPROVE or CHANGE with a short cited why, in place of the five sections (fix 2)."""
    form = (HERE / "assets" / "answer-vote.md").read_text(encoding="utf-8").format(name=name, why=why)
    return swap(text, r"^## Write exactly this.*\Z", form)


def sections_of(out: Path) -> list[str]:
    """The sections an answer in this run must have: the vote form's when the run was made with --vote."""
    form = out / "form.txt"
    return VOTE_SECTIONS if form.exists() and form.read_text(encoding="utf-8").strip() == "vote" else SECTIONS


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


def pasted_brief(brief: Path, list_path: Path, identity_path: Path) -> Path:
    """The brief with the two files it names pasted in whole, for an engine that cannot open files (mcode lightweight)."""
    text = brief.read_text(encoding="utf-8").rstrip() + (
        "\n\n---\n\nYou cannot open files here, so the two files this brief names are pasted below, whole.\n")
    for f in (list_path, identity_path):
        text += f"\n## File: {f}\n\n{f.read_text(encoding='utf-8').rstrip()}\n"
    out = brief.with_suffix(".pasted.md")
    out.write_text(text, encoding="utf-8")
    return out


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
    if engine == "mcode":  # lightweight has no tools, so it cannot write; the prompt (a file) is read on stdin
        return [MCODE, "exec", "--mode", "lightweight", "--model", MODELS["mcode"], "--timeout", f"{timeout - 60}s",
                "--input", "-", "-o", str(out_file)]
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
    writes_answer = engine in ("codex", "mcode")  # both write the final message to the answer file themselves
    out = open(log if writes_answer else ans, "w")
    err = open(log, "a" if writes_answer else "w")
    stdin = open(prompt, encoding="utf-8") if engine == "mcode" else subprocess.DEVNULL
    p = subprocess.Popen(cmd, stdin=stdin, stdout=out, stderr=err, cwd=cwd, env=env)
    return p, time.time()


def answer_ok(ans: Path, sections: list[str] = SECTIONS) -> tuple[bool, str]:
    text = ans.read_text(encoding="utf-8", errors="ignore") if ans.exists() else ""
    if not text.strip():
        return False, "empty answer"
    missing = [s for s in sections if s not in text]
    return (False, f"missing sections {missing}") if missing else (True, "")


def guard_text(args: list[str], cwd: Path) -> str:
    """The guard's insight index or chosen sections, as text; "" when the guard cannot answer."""
    try:
        p = subprocess.run(["bun", str(GUARD_CLI), "insight", *args], cwd=cwd, capture_output=True, text=True,
                           timeout=60, stdin=subprocess.DEVNULL, env={**os.environ, "BUN_RUNTIME_TRANSPILER_CACHE_PATH": "0"})
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return p.stdout if p.returncode == 0 else ""


LESSON_AGENT = {"claude": "claude-main"}  # a Claude seat takes the Claude lessons; the other engines are their own type


def lessons_text(engine: str, cwd: Path) -> str:
    """The brief's Lessons section: `lessons for --agent <engine> --kinds brief`, as text; "" when none match or the
    guard cannot answer (guard SPEC Round 18, L4)."""
    try:
        p = subprocess.run(["bun", str(GUARD_CLI), "lessons", "for", "--agent", LESSON_AGENT.get(engine, engine),
                            "--kinds", "brief"], cwd=cwd, capture_output=True, text=True, timeout=60,
                           stdin=subprocess.DEVNULL, env={**os.environ, "BUN_RUNTIME_TRANSPILER_CACHE_PATH": "0"})
    except (OSError, subprocess.TimeoutExpired):
        return ""
    if p.returncode != 0 or not p.stdout.strip():
        return ""
    return "\n\n## Lessons (from earlier agents' failures; apply each that fits)\n\n" + p.stdout.strip() + "\n"


def insight_load(out: Path, categories: str | None, cwd: Path, scheme: str | None = None) -> str:
    """Dave's insights (run 20261016-six-experts, D1): the index, then the named categories' sections, copied into the
    run folder so every engine can read them; the brief section that tells him to load and cite them."""
    extra = ["--categories", scheme] if scheme else []  # another category scheme, for a comparison
    index = guard_text(["index", *extra], cwd)
    (out / "seats" / "dave-insight-index.md").write_text(index or "(the guard gave no index)\n", encoding="utf-8")
    cats = [c.strip() for c in (categories or "").split(",") if c.strip()]
    sections = guard_text(["show", *extra, *[x for c in cats for x in ("--category", c)]], cwd) if cats else ""
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
    card, vote = getattr(a, "card", False), getattr(a, "vote", False)
    if vote:
        (out / "form.txt").write_text("vote\n", encoding="utf-8")
    sections = sections_of(out)
    jobs = {}
    for sid, name, engine in EXPERTS:
        lst, ident = out / "seats" / f"{sid}-list.md", out / "seats" / f"{sid}-identity.md"
        if only and sid not in only:
            continue
        brief = out / "briefs" / f"{sid}.md"
        if sid in PLAIN:  # the control gets the question and the answer's shape, nothing else
            text = plain_t.format(question=question.strip())
            if vote:
                text = vote_brief(text, "Answer", "one reason per line")
            brief.write_text(text, encoding="utf-8")
            jobs[sid] = {"expert": name, "engine": engine, "brief": brief}
            continue
        src_list, src_ident = seat_files(sid)
        shutil.copyfile(src_list, lst)
        shutil.copyfile(src_ident, ident)
        text = brief_t.format(name=name, list_path=lst, identity_path=ident, n_items=n_items(lst),
                              question=question.strip())
        if card:
            text = card_brief(text, rule_card(lst, ident))
        if vote:
            text = vote_brief(text, name, 'each line cites "my #n" or says "my reading"')
        if sid == INSIGHT_SEAT:
            text += insight_load(out, a.insights, cwd, getattr(a, "insight_scheme", None))
        brief.write_text(text, encoding="utf-8")
        jobs[sid] = {"expert": name, "engine": engine, "brief": brief, "list": lst, "identity": ident}
    if (a.needs_web or a.needs_shell) and "fan-li" in jobs:
        jobs["fan-li"].update(engine="claude", fallback_from="agy",
                              fallback_reason="task needs " + " and ".join(
                                  x for x, f in (("web", a.needs_web), ("shell", a.needs_shell)) if f))
    if "linus" in jobs:
        left = codex_left()
        if left is not None and left <= CODEX_MIN_LEFT:
            jobs["linus"].update(engine="mcode", fallback_from="codex",
                                 fallback_reason=f"codex has {left:g}% left ({CODEX_MIN_LEFT}% or less)")
    for sid, j in jobs.items():  # after the fallbacks, so the lessons are the engine's that will run (guard Round 18)
        if sid not in PLAIN:
            lessons = lessons_text(j["engine"], cwd)
            if lessons:
                j["brief"].write_text(j["brief"].read_text(encoding="utf-8") + lessons, encoding="utf-8")
    old = out / "status.json"
    status = json.loads(old.read_text(encoding="utf-8")) if only and old.exists() else {}

    def prompt_for(sid, engine):
        if engine == "mcode" and card:  # the card brief already holds the rules; nothing to paste
            return str(jobs[sid]["brief"])
        if engine == "mcode":
            return str(pasted_brief(jobs[sid]["brief"], jobs[sid]["list"], jobs[sid]["identity"]))
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

    for sid, j in jobs.items():
        if j["engine"] == "claude" and a.claude_by_caller:
            hand_to_caller(sid)
            continue
        launch(sid)
    while procs:
        for sid, (p, t0, ans, log) in list(procs.items()):
            if p.poll() is None:
                continue
            del procs[sid]
            j = jobs[sid]
            ok, why = answer_ok(ans, sections)
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
                j.update(engine="mcode", fallback_from="codex", fallback_reason="codex stopped on its usage limit")
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
    bad = [f"{sid}: missing section {s}" for s in sections_of(out) if s not in text]
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
    r.add_argument("--insights", help="the insight categories Dave loads, comma-separated (e.g. instruction,check); "
                                      "with none named he chooses from the index")
    r.add_argument("--insight-scheme", help="a categories file other than guard/data/insight-categories.yaml, for a "
                                           "comparison of category schemes")
    r.add_argument("--progress", help="append a timestamped line per expert start and end to this file "
                                      "(e.g. runs/<run>/nodes/experts.progress.md)")
    r.add_argument("--only", help="comma-separated ids to run (e.g. dave or linus,dave); with --out, adds them to an "
                   "existing run and keeps its other answers")
    r.add_argument("--claude-by-caller", action="store_true",
                   help="inside Claude Code: leave Dave and any 范蠡 fallback to the caller's subagents")
    r.add_argument("--card", action="store_true", help="put each expert's rules in its brief as a short card (one line "
                   "per rule) and tell it to read nothing else and run no shell")
    r.add_argument("--vote", action="store_true", help="answer form for an approve-or-change question: APPROVE or "
                   "CHANGE, a short cited why, and what I need to know; check judges these sections")
    c = sub.add_parser("check")
    c.add_argument("dir")
    c.add_argument("--sabotage", action="store_true")
    a = ap.parse_args()
    return run(a) if a.cmd == "run" else check(a)


if __name__ == "__main__":
    sys.exit(main())
