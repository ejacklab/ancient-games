"""six-experts runner: the Claude command line, Dave and Dario on one model, their two briefs, what `check`
accepts from them, and Linus on mcode, not a second opencode, when Codex is low (SKILL.md §1–2, run
20261016-six-experts D1/D2).

Every engine is mocked: `start` and `guard_text` are replaced, so no claude, codex, agy, dsh, opencode, mcode or bun
process is ever started."""
import argparse
import importlib.util
import json
import subprocess
from pathlib import Path

import pytest
from types import SimpleNamespace

SCRIPT = Path(__file__).resolve().parent.parent / ".claude" / "skills" / "six-experts" / "scripts" / "six_experts.py"
spec = importlib.util.spec_from_file_location("six_experts", SCRIPT)
fe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fe)

QUESTION = "Should we keep Cloudflare analytics on the page?"
ANSWER = "\n\n".join(s + "\n\nx" for s in fe.SECTIONS) + "\n"
INSIGHT_ID = "F-1a2b3c4d"
OTHER_ID = "F-9f9f9f9f"
INDEX_TEXT = f"| file.md#{INSIGHT_ID} | insight index |\n| other.md#{OTHER_ID} | insight index |\n"
SECTIONS_TEXT = f"## F-1a2b3c4d — what a passed check costs\n\nrun 20261013 · spec\n"


class FakeProc:
    """A fake engine process: alive until `end_after` poll passes have gone by, then exits with `rc`."""

    def __init__(self, rc, alive, on_exit):
        self.rc, self.alive, self.on_exit = rc, alive, on_exit
        self.polls, self.returncode, self.exited = 0, None, False

    def poll(self):
        self.polls += 1
        if self.polls <= self.alive:
            return None
        if not self.exited:
            self.returncode, self.exited = self.rc, True
            self.on_exit()
        return self.returncode


class Ticks:
    """The fake clock `run` sleeps on; one tick is one pass of its wait loop."""

    def __init__(self):
        self.n = 0

    def __call__(self):
        return self.n

    def sleep(self, _seconds):
        self.n += 1


def run_seats(tmp_path, monkeypatch, only, insights=None, guard=None, alive=1, rc=0, answer=ANSWER,
              codex_left=None, lessons=None):
    """Run `only` with fake engines; returns (out, calls, rc).

    calls is one dict per start and one per exit: sid, engine, model, prompt, and `running` — the experts still
    running when this one started, which is what says whether two engines overlapped."""
    clock, calls, live = Ticks(), [], {}

    def fake_start(engine, prompt, ans, log, timeout, web, shell, cwd, model=None):
        sid = ans.stem
        running = [s for s, p in live.items() if not p.exited and p.poll() is None]
        calls.append({"event": "start", "sid": sid, "engine": engine, "model": model, "prompt": prompt,
                      "running": running})
        ans.write_text(answer, encoding="utf-8")
        log.write_text("", encoding="utf-8")
        proc = FakeProc(rc, alive, lambda: calls.append(
            {"event": "end", "sid": sid, "engine": engine, "model": model, "prompt": prompt, "running": []}))
        live[sid] = proc
        return proc, 0.0

    if guard is not None:
        monkeypatch.setattr(fe, "guard_text", guard)
    monkeypatch.setattr(fe, "lessons_text", lessons or (lambda engine, cwd: ""))
    monkeypatch.setattr(fe, "start", fake_start)
    monkeypatch.setattr(fe, "codex_left", lambda *a, **k: codex_left)
    monkeypatch.setattr(fe.time, "sleep", clock.sleep)
    monkeypatch.chdir(tmp_path)
    out = tmp_path / "run"
    args = argparse.Namespace(question=QUESTION, question_file=None, out=str(out), needs_web=False,
                              needs_shell=False, timeout=60, progress=None, only=only, insights=insights,
                              claude_by_caller=False)
    rc = fe.run(args)
    return out, calls, rc


def started(calls):
    return [c for c in calls if c["event"] == "start"]


# --- P1: the Claude command line (SKILL.md: "the tools as one --allowedTools= argument", run 20261016-time-monitor)


def test_claude_keeps_the_prompt_as_its_last_argument():
    out_file = Path("/tmp/answers/dave.md")
    cmd = fe.command("claude", "Read the brief and do what it says.", out_file, 60, False, False,
                     "claude-sonnet-5-5")
    assert cmd[-1] == "Read the brief and do what it says."
    assert "-p" in cmd and cmd.index("-p") < cmd.index("--model")


def test_claude_passes_the_tools_as_one_allowed_tools_argument():
    cmd = fe.command("claude", "p", Path("a.md"), 60, True, True, "claude-sonnet-5-5")
    tools = [a for a in cmd if a.startswith("--allowedTools")]
    assert len(tools) == 1, "the bare --allowedTools swallows the prompt that follows it"
    assert set(tools[0].removeprefix("--allowedTools=").split(",")) == {
        "Read", "Grep", "Glob", "WebSearch", "WebFetch", "Bash"}
    assert cmd[-1] == "p"


def test_claude_without_web_or_shell_asks_for_no_web_and_no_shell():
    cmd = fe.command("claude", "p", Path("a.md"), 60, False, False, "claude-sonnet-5-5")
    tools = next(a for a in cmd if a.startswith("--allowedTools")).removeprefix("--allowedTools=")
    assert set(tools.split(",")) == {"Read", "Grep", "Glob"}


def test_claude_without_a_model_falls_back_to_the_default():
    cmd = fe.command("claude", "p", Path("a.md"), 60, False, False, None)
    assert cmd[cmd.index("--model") + 1] == fe.MODELS["claude"]


# --- P2: Dave on Opus, Dario on Sonnet (SKILL.md table; EJ 2026-10-16, replacing decision D2)


def test_dave_is_on_opus_and_dario_on_sonnet():
    assert fe.SEAT_MODEL == {"dave": "claude-opus-5-5", "dario": "claude-sonnet-5-5"}


def test_dave_and_dario_run_on_their_pinned_models(tmp_path, monkeypatch):
    out, calls, rc = run_seats(tmp_path, monkeypatch, "dave,dario")
    assert rc == 0
    models = {c["sid"]: c["model"] for c in started(calls)}
    assert models == {"dave": "claude-opus-5-5", "dario": "claude-sonnet-5-5"}
    status = json.loads((out / "status.json").read_text(encoding="utf-8"))
    assert [status[s]["model"] for s in ("dave", "dario")] == ["claude-opus-5-5", "claude-sonnet-5-5"]
    assert [status[s]["engine"] for s in ("dave", "dario")] == ["claude"] * 2


# --- P3: Dario's brief (plan round 3: no list, no identity, no insights)


def test_darios_brief_holds_the_question_and_the_five_sections(tmp_path, monkeypatch):
    out, _calls, _rc = run_seats(tmp_path, monkeypatch, "dario")
    brief = (out / "briefs" / "dario.md").read_text(encoding="utf-8")
    assert QUESTION in brief
    for s in fe.SECTIONS:
        assert s in brief


def test_darios_brief_has_no_rules_identity_or_insights(tmp_path, monkeypatch):
    out, _calls, _rc = run_seats(tmp_path, monkeypatch, "dario")
    brief = (out / "briefs" / "dario.md").read_text(encoding="utf-8")
    for absent in ("Load first", "insight", "Final list", "Read first", "my #", "Who they are", "rules"):
        assert absent not in brief
    assert not (out / "seats" / "dario-list.md").exists()
    assert not (out / "seats" / "dario-identity.md").exists()
    assert not (out / "seats" / "dario-insight-index.md").exists()


def test_darios_prompt_names_only_his_own_brief(tmp_path, monkeypatch):
    out, calls, _rc = run_seats(tmp_path, monkeypatch, "dario")
    assert [c["prompt"] for c in started(calls)] == [f"Read {out / 'briefs' / 'dario.md'} and do what it says."]


# --- P4: Dave's brief and the insights he loads (SKILL.md §1 --insights, decision D1)


def test_daves_brief_says_load_first_and_names_the_index_and_categories(tmp_path, monkeypatch):
    seen = []

    def fake_guard(args, cwd):
        seen.append(args)
        return INDEX_TEXT if args == ["index"] else SECTIONS_TEXT

    out, _calls, _rc = run_seats(tmp_path, monkeypatch, "dave", insights="spec,tool", guard=fake_guard)
    brief = (out / "briefs" / "dave.md").read_text(encoding="utf-8")
    assert "## Load first: what was learned" in brief
    assert str(out / "seats" / "dave-insight-index.md") in brief
    assert str(out / "seats" / "dave-insights.md") in brief
    assert "(spec, tool)" in brief
    assert "No insight applies" in brief


def test_daves_insight_files_are_written_into_the_runs_seats_folder(tmp_path, monkeypatch):
    seen = []

    def fake_guard(args, cwd):
        seen.append(args)
        return INDEX_TEXT if args == ["index"] else SECTIONS_TEXT

    out, _calls, _rc = run_seats(tmp_path, monkeypatch, "dave", insights="instruction,check", guard=fake_guard)
    assert seen[0] == ["index"]
    assert seen[1] == ["show", "--category", "instruction", "--category", "check"]
    assert (out / "seats" / "dave-insight-index.md").read_text(encoding="utf-8") == INDEX_TEXT
    assert (out / "seats" / "dave-insights.md").read_text(encoding="utf-8") == SECTIONS_TEXT


def test_with_no_category_named_dave_is_told_to_choose_from_the_index(tmp_path, monkeypatch):
    seen = []

    def fake_guard(args, cwd):
        seen.append(args)
        return INDEX_TEXT if args == ["index"] else ""

    out, _calls, _rc = run_seats(tmp_path, monkeypatch, "dave", insights=None, guard=fake_guard)
    assert seen == [["index"]]  # no `show` without a named category
    assert "choose from the index" in (out / "briefs" / "dave.md").read_text(encoding="utf-8")
    assert "no category named" in (out / "seats" / "dave-insights.md").read_text(encoding="utf-8")
    assert INDEX_TEXT in (out / "seats" / "dave-insight-index.md").read_text(encoding="utf-8")


def test_an_empty_index_from_the_guard_is_recorded_not_left_out(tmp_path, monkeypatch):
    out, _calls, _rc = run_seats(tmp_path, monkeypatch, "dave", insights="instruction",
                                         guard=lambda args, cwd: "")
    assert "no index" in (out / "seats" / "dave-insight-index.md").read_text(encoding="utf-8")
    assert str(out / "seats" / "dave-insight-index.md") in (out / "briefs" / "dave.md").read_text(encoding="utf-8")


# --- P5: what `check` accepts from Dave and Dario (SKILL.md §1 last bullet)


def make_run(tmp_path, answers, index=INDEX_TEXT):
    """A run folder with `answers` (sid -> text) and a one-item list and identity per expert."""
    out = tmp_path / "checkdir"
    for d in ("answers", "seats"):
        (out / d).mkdir(parents=True, exist_ok=True)
    (out / "seats" / "dave-insight-index.md").write_text(index, encoding="utf-8")
    for sid, _name, _engine in fe.EXPERTS:
        (out / "seats" / f"{sid}-list.md").write_text(
            f"# {sid}\n\n## Final list\n\n### 1. A rule\n- **Kind:** decision rule\n", encoding="utf-8")
        (out / "seats" / f"{sid}-identity.md").write_text("# who\n", encoding="utf-8")
    for sid, text in answers.items():
        (out / "answers" / f"{sid}.md").write_text(text, encoding="utf-8")
    return out


def dave_answer(citation):
    return ANSWER + f"\n{citation}\n"


def test_dario_passes_on_the_five_sections_alone(tmp_path):
    out = make_run(tmp_path, {"dario": ANSWER})
    assert fe.check_one("dario", ANSWER, out) == []


def test_daves_own_insight_id_passes(tmp_path):
    out = make_run(tmp_path, {})
    text = dave_answer(f"my #1, because {INSIGHT_ID} says so")
    assert fe.check_one("dave", text, out) == []


def test_dave_fails_when_he_cites_an_id_not_in_his_index(tmp_path):
    out = make_run(tmp_path, {}, index=f"| file.md#{INSIGHT_ID} | insight index |\n")
    text = dave_answer("my #1, because F-0badc0de says so")
    bad = fe.check_one("dave", text, out)
    assert [b for b in bad if "not in the index" in b and "F-0badc0de" in b]


def test_dave_fails_when_he_cites_none_and_does_not_say_none_applies(tmp_path):
    out = make_run(tmp_path, {})
    bad = fe.check_one("dave", dave_answer("my #1 is my own reading"), out)
    assert [b for b in bad if "cites none" in b]


def test_dave_passes_with_no_citation_when_he_says_no_insight_applies(tmp_path):
    out = make_run(tmp_path, {})
    assert fe.check_one("dave", dave_answer("my #1; No insight applies: nothing in the index is about this"), out) == []


def test_darios_plain_answer_is_not_judged_on_citations_or_chinese(tmp_path):
    out = make_run(tmp_path, {})
    # Review #8: a 4+ character run that a persona's list does not hold, so the Chinese check would fire if Dario
    # were checked like a persona (shown by checking the same text as Linus).
    text = ANSWER + "\nNo items, and 完全不在列表 here.\n"
    assert fe.check_one("dario", text, out) == []
    assert fe.check_one("linus", text, out) != []


def test_check_reports_dave_and_dario_together(tmp_path):
    good = {sid: ANSWER + "\nmy #1\n" for sid, _n, _e in fe.EXPERTS if sid not in ("dario", "dave")}
    good["dario"] = ANSWER
    good["dave"] = dave_answer(f"my #1, because {INSIGHT_ID} says so")
    out = make_run(tmp_path, good)
    assert fe.check(argparse.Namespace(dir=str(out), sabotage=False)) == 0
    assert "0 failure(s)" in (out / "check.txt").read_text(encoding="utf-8")


# --- P6: opencode runs once (老子); Linus off Codex goes to mcode (EJ, 2026-10-16; SKILL.md §1)


def test_linus_off_codex_runs_on_mcode_beside_lao_tzu_on_opencode(tmp_path, monkeypatch):
    # codex_left 20.0 moves Linus off Codex: to mcode, so opencode still runs only 老子
    _out, calls, rc = run_seats(tmp_path, monkeypatch, "linus,lao-tzu", alive=2, codex_left=20.0)
    assert rc == 0
    seats = started(calls)
    assert [c["engine"] for c in seats] == ["mcode", "opencode"]
    assert seats[1]["running"] == ["linus"]  # different engines overlap; nothing waits


# COO, after the dsh review (runs/20261016-six-experts/nodes/review.result.md).
def test_sabotage_without_chinese_still_fails_the_check(tmp_path, capsys):
    out = make_run(tmp_path, {"linus": ANSWER + "\nmy #1\n"})
    assert fe.check(SimpleNamespace(dir=str(out), sabotage=True)) == 0
    import re as _re
    found = _re.search(r"→ (\d+) failure\(s\)", capsys.readouterr().out)
    assert found and int(found.group(1)) >= 2


def test_caller_mode_names_dave_and_darios_model(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(fe, "guard_text", lambda args, cwd: "")
    q = tmp_path / "q.md"
    q.write_text("A question?\n", encoding="utf-8")
    out = tmp_path / "run"
    fe.run(SimpleNamespace(question=None, question_file=str(q), out=str(out), needs_web=False, needs_shell=False,
                           timeout=60, only="dave,dario", claude_by_caller=True, insights=None, progress=None))
    printed = capsys.readouterr().out
    assert printed.count("on claude-opus-5-5") == 1 and printed.count("on claude-sonnet-5-5") == 1
    status = __import__("json").loads((out / "status.json").read_text(encoding="utf-8"))
    assert (status["dave"]["model"], status["dario"]["model"]) == ("claude-opus-5-5", "claude-sonnet-5-5")


# --- guard Round 18: each expert's brief ends with the lessons for the engine that will run it (run 20261017-agent-lessons)


def test_each_seat_gets_the_lessons_of_its_engine_and_dario_none(tmp_path, monkeypatch):
    asked = []

    def lessons(engine, cwd):
        asked.append(engine)
        return f"\n\n## Lessons\n\n- lesson for {engine}\n"

    out, _calls, _rc = run_seats(tmp_path, monkeypatch, "linus,sun-tzu,dario", lessons=lessons, codex_left=10.0)
    assert "- lesson for mcode" in (out / "briefs" / "linus.md").read_text(encoding="utf-8")  # after the fallback
    assert "- lesson for dsh" in (out / "briefs" / "sun-tzu.md").read_text(encoding="utf-8")
    assert "Lessons" not in (out / "briefs" / "dario.md").read_text(encoding="utf-8")
    assert sorted(asked) == ["dsh", "mcode"]


def test_no_lessons_leaves_the_brief_as_it_was(tmp_path, monkeypatch):
    out, _calls, _rc = run_seats(tmp_path, monkeypatch, "sun-tzu")
    assert "## Lessons" not in (out / "briefs" / "sun-tzu.md").read_text(encoding="utf-8")


def test_lessons_text_asks_the_guard_for_brief_lessons_of_the_engine(monkeypatch, tmp_path):
    seen = {}

    def fake_run(cmd, **kwargs):
        seen["cmd"] = cmd
        return subprocess.CompletedProcess(cmd, 0, stdout="- a lesson (slug)\n", stderr="")

    monkeypatch.setattr(fe.subprocess, "run", fake_run)
    text = fe.lessons_text("claude", tmp_path)
    assert seen["cmd"][-6:] == ["lessons", "for", "--agent", "claude-main", "--kinds", "brief"]
    assert text.startswith("\n\n## Lessons") and "- a lesson (slug)" in text
    monkeypatch.setattr(fe.subprocess, "run", lambda cmd, **kw: subprocess.CompletedProcess(cmd, 2, stdout="x", stderr=""))
    assert fe.lessons_text("opencode", tmp_path) == ""
