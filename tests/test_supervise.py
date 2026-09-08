"""AUTONOMY_DESIGN v2 §7 — the unattended supervisor: the terminal-state oracle, its exit codes
(the queue gate), the external-chooser drive loop, and resumability.

The point of every case here is that the state is derived from the journal, so a fresh process
gives the same answer a crashed one would have — that is what makes a long run resumable rather
than merely long.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from ancient_games.ctx import Ctx
from ancient_games.hybrid import autonomy, cli, loop, supervise
from ancient_games.hybrid.registry import load_tools
from ancient_games.journal import Journal, read_events

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "ablation" / "runs" / "attempt4"
TOOLS = load_tools()


def tool_call(tool, ok=True, exit_type=None, refused_by=None):
    return {"event": "tool_call", "tool": tool, "action_id": None, "args": {}, "args_hash": "h",
            "result_summary": ("ok: x" if ok else "declined: x"), "exit_type": exit_type,
            "invariants_checked": [], "refused_by": refused_by,
            "reason": (None if ok and refused_by is None else "r"), "run_id": "R", "ts": "t"}


def deferral():
    return {"event": "deferred_decision", "kind": "kind-override", "payload": "C1", "boundary": "b",
            "reason": "committed under grant:1", "run_id": "R", "ts": "t"}


# --- the oracle ------------------------------------------------------------------------------
def test_terminal_state_reports_each_terminus_from_the_journal_alone():
    assert supervise.terminal_state([], [], 10)["state"] == "RUNNING"
    assert supervise.terminal_state([tool_call("gate")], [], 1)["state"] == "CEILING_REACHED"
    assert supervise.terminal_state([tool_call("done")], [], 10)["state"] == "DONE"
    # a DECLINED done is not a terminus (event_ok is false for it)
    assert supervise.terminal_state([tool_call("done", ok=False)], [], 10)["state"] == "RUNNING"


def test_a_pause_is_a_terminus_but_a_finished_run_outranks_it():
    rules = [{"name": "step", "tool": "*"}]
    assert supervise.terminal_state([tool_call("gate")], rules, 10)["state"] == "PAUSED"
    # a boundary tripped by `done` itself has nothing left to gate
    assert supervise.terminal_state([tool_call("done")], rules, 10)["state"] == "DONE"


def test_deferrals_outrank_done_so_an_unattended_run_cannot_end_silently():
    st = supervise.terminal_state([tool_call("done"), deferral()], [], 10)
    assert st["state"] == "DONE_WITH_DEFERRALS" and st["deferred"] == 1


def test_only_a_clean_finish_exits_zero():
    """The queue gate. §6 keeps the queue out of the invariant floor on purpose, so this exit
    code is the only teeth it has."""
    assert supervise.STATE_EXIT["DONE"] == 0
    assert all(code != 0 for state, code in supervise.STATE_EXIT.items() if state != "DONE")


# --- plan reconstruction (§7) -----------------------------------------------------------------
def test_default_plan_from_matches_what_the_live_loop_held_in_memory(tmp_path):
    """Differential: `loop.run` keeps `default_plan` in memory and offers it as `suggested_next`.
    A resumed run has to rebuild it from the journal. The chooser records what the live loop
    offered at every step; the rebuilt plan must equal it at the matching prefix."""
    j = Journal(str(tmp_path / "j.jsonl"), "R")
    seen: list[list[str]] = []
    rebuilt: list[list[str]] = []
    script = loop.scripted([{"tool": "read_journal"}, {"tool": "gate"}, {"tool": "read_journal"}])

    def choose(obs, tools):
        seen.append(list(obs["suggested_next"]))
        rebuilt.append(supervise.default_plan_from(obs["events"]))
        return script(obs, tools)

    loop.run(TOOLS, choose, j, 5, Ctx())
    # 4 observations: three scripted calls plus the one where the queue is found empty
    assert seen == rebuilt and len(seen) == 4
    assert seen[0] == list(loop.DEFAULT_PLAN) and seen[-1] != list(loop.DEFAULT_PLAN)  # it really moved


def test_default_plan_from_resets_on_a_prove_that_returned_to_the_planner():
    """The plan must be walked all the way to `prove` before this can discriminate: with only
    `gate, guard` popped the remaining plan is ALREADY equal to REPLAN, so a version that ignores
    RETURN_TO_PLANNER entirely still looks correct. (Found by sabotage — the first form of this
    test passed with the reset deleted.)"""
    walked = [tool_call(t) for t in ("gate", "guard", "corroborate", "filter_candidates")]
    assert supervise.default_plan_from(walked) == ["prove"]

    returned = walked + [tool_call("prove", exit_type="RETURN_TO_PLANNER")]
    assert supervise.default_plan_from(returned) == list(loop.REPLAN)  # reset, not popped to []
    passed = walked + [tool_call("prove", exit_type="PASS")]
    assert supervise.default_plan_from(passed) == []                   # popped, not reset

    # and a REFUSED call never pops the head
    assert supervise.default_plan_from([tool_call("gate", refused_by="I4")])[0] == "gate"


def test_default_plan_from_runs_on_the_real_attempt4_journals():
    for name in ("UC3", "UC2J"):
        plan = supervise.default_plan_from(read_events(str(RUNS / f"{name}.journal.jsonl")))
        assert isinstance(plan, list) and set(plan) <= set(loop.DEFAULT_PLAN)


# --- the drive loop ---------------------------------------------------------------------------
def test_drive_runs_to_a_pause_and_a_later_drive_resumes_the_same_run(tmp_path):
    j = Journal(str(tmp_path / "j.jsonl"), "R")
    j.append({"event": "run_config", "autonomy": "step", "pause_after": autonomy.STEP_RULES, "ceiling": 10})
    calls = [{"tool": "read_journal"}, {"tool": "read_journal"}]

    st = supervise.drive(TOOLS, loop.scripted(calls), j, 10, Ctx(), cwd=str(tmp_path))
    assert st["state"] == "PAUSED" and st["paused_at"] == "pause:step@1"
    assert supervise.spent(j.read()) == 1

    j.append({"event": "approval_recorded", "action_id": "pause:step@1", "gate": "resume",
              "approver": "ej", "note": ""})
    st = supervise.drive(TOOLS, loop.scripted(calls), j, 10, Ctx(), cwd=str(tmp_path))
    # a NEW invocation, a fresh chooser: the run continued rather than restarting
    assert st["state"] == "PAUSED" and st["paused_at"] == "pause:step@2"
    assert supervise.spent(j.read()) == 2


def test_max_calls_bounds_the_invocation_but_is_not_a_terminus(tmp_path):
    j = Journal(str(tmp_path / "j.jsonl"), "R")
    st = supervise.drive(TOOLS, loop.scripted([{"tool": "read_journal"}] * 5), j, 10, Ctx(),
                         cwd=str(tmp_path), max_calls=2)
    assert st["state"] == "RUNNING" and "stopped after 2 call(s)" in st["detail"]
    assert supervise.spent(j.read()) == 2
    st = supervise.drive(TOOLS, loop.scripted([{"tool": "read_journal"}] * 5), j, 10, Ctx(),
                         cwd=str(tmp_path), max_calls=2)
    assert supervise.spent(j.read()) == 4  # continued, did not restart


def test_a_chooser_with_no_call_ends_the_run_rather_than_guessing(tmp_path):
    j = Journal(str(tmp_path / "j.jsonl"), "R")
    st = supervise.drive(TOOLS, lambda obs, tools: None, j, 10, Ctx(), cwd=str(tmp_path))
    assert st["state"] == "NO_CHOICE" and supervise.STATE_EXIT[st["state"]] != 0


def test_drive_fails_loudly_if_a_step_journals_nothing(tmp_path, monkeypatch):
    """Without this the run spins: the terminal state is derived from the journal, so a step that
    records nothing can never reach a terminus."""
    j = Journal(str(tmp_path / "j.jsonl"), "R")
    monkeypatch.setattr(loop, "step", lambda *a, **k: None)  # journals nothing
    with pytest.raises(RuntimeError, match="made no progress"):
        supervise.drive(TOOLS, loop.scripted([{"tool": "read_journal"}] * 3), j, 10, Ctx(), cwd=str(tmp_path))


# --- the external chooser contract -------------------------------------------------------------
def write_chooser(tmp_path, body: str) -> str:
    path = str(tmp_path / "chooser.py")
    with open(path, "w") as fh:
        fh.write(body)
    return f"{sys.executable} {path}"


def test_command_chooser_reads_the_observation_and_returns_one_call(tmp_path):
    cmd = write_chooser(tmp_path, "import json,sys\n"
                                  "obs = json.load(sys.stdin)\n"
                                  "assert 'events' in obs and 'suggested_next' in obs\n"
                                  "print(json.dumps({'tool': 'read_journal', 'args': {}}))\n")
    call = supervise.command_chooser(cmd)({"events": [], "suggested_next": [], "ctx": {}, "last_results": {}}, TOOLS)
    assert call.tool == "read_journal"


def test_an_empty_or_null_chooser_answer_means_no_choice(tmp_path):
    for body in ("", "print('null')", "print('{}')"):
        cmd = write_chooser(tmp_path, "import sys\n" + body + "\n")
        assert supervise.command_chooser(cmd)({"events": []}, TOOLS) is None


def test_a_failing_chooser_raises_rather_than_being_read_as_no_choice(tmp_path):
    cmd = write_chooser(tmp_path, "import sys\nsys.stderr.write('boom')\nsys.exit(2)\n")
    with pytest.raises(RuntimeError, match="chooser exited 2"):
        supervise.command_chooser(cmd)({"events": []}, TOOLS)


# --- end to end through the CLI ------------------------------------------------------------------
def test_cli_drive_then_status_exit_codes(tmp_path):
    repo = str(tmp_path / "repo")
    os.makedirs(repo)
    for argv in (("init", "-q"), ("config", "user.email", "t@t"), ("config", "user.name", "t")):
        subprocess.run(["git", *argv], cwd=repo, check=True, capture_output=True)
    jp = str(tmp_path / "j.jsonl")
    manifest = cli.write_manifest("R", jp, repo, [], 6, autonomy_mode="step")
    chooser = write_chooser(tmp_path, "import json,sys\njson.load(sys.stdin)\n"
                                      "print(json.dumps({'tool': 'read_journal'}))\n")

    assert cli.main(["--manifest", manifest, "drive", "--chooser", chooser]) == supervise.EXIT_PAUSED
    assert cli.main(["--manifest", manifest, "status"]) == supervise.EXIT_PAUSED

    Journal(jp, "R").append({"event": "deferred_decision", "kind": "kind-override", "payload": "C1",
                             "boundary": "b", "reason": "under grant:1"})
    Journal(jp, "R").append(tool_call("done") | {"run_id": "R"})
    assert cli.main(["--manifest", manifest, "status"]) == supervise.EXIT_DEFERRED  # the queue gate
    assert cli.main(["--manifest", manifest, "queue"]) != 0
