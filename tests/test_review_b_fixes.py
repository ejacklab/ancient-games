"""REVIEW_B — the xhigh review's findings, each reproduced on the real return values.

Every test here fails on the commit before its fix: the scenario is the reviewer's, and the
assertion is on what the real function/tool returns, never on a re-derivation of it.
"""
from __future__ import annotations

import os
import subprocess

import pytest

from ancient_games.ctx import Ctx
from ancient_games.hybrid import invariants as inv
from ancient_games.hybrid.loop import step as loop_step
from ancient_games.hybrid.registry import load_tools
from ancient_games.hybrid.tools import _shared as shared
from ancient_games.hybrid.tools import done as done_tool
from ancient_games.hybrid.types import Call, ToolEnv, ToolResult
from ancient_games.journal import Journal

TOOLS = load_tools()
UNRELATED_AID = "invoke:['eval.partitions.load_holdout']"  # a real owner-gated action of another decision
GOV_PASS = "Prove: PASS, plan cleared to terminal gate=owner(ej) [governance-gated]."
PLAIN_PASS = "Prove: PASS, plan cleared to owner(ej) gate (at commit)."


@pytest.fixture
def repo(tmp_path):
    root = str(tmp_path / "repo")
    os.makedirs(root)
    for argv in (("init", "-q"), ("config", "user.email", "t@t"), ("config", "user.name", "t"),
                 ("config", "commit.gpgsign", "false")):
        subprocess.run(["git", *argv], cwd=root, check=True, capture_output=True)
    with open(os.path.join(root, "a.py"), "w") as fh:
        fh.write("x = 1\n")
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=root, check=True, capture_output=True)
    return root


@pytest.fixture
def journal(tmp_path):
    return Journal(str(tmp_path / "j.jsonl"), "rev-b")


def ok(journal, call, value=None, exit_type=None):
    class V:
        pass
    v = V()
    if exit_type:
        v.exit_type = exit_type
    return journal.append(shared.tool_call_event(call, [], ToolResult(True, v if exit_type else value)))


def approve(journal, aid, gate="owner"):
    return journal.append({"event": "approval_recorded", "action_id": aid, "gate": gate, "approver": "ej", "note": "t"})


def env_for(journal, repo):
    return ToolEnv(journal.run_id, journal.path, Ctx(), cwd=repo, tools=TOOLS)


def a_exit(journal, line):
    return journal.append({"event": "exit", "algorithm": "A", "steps_fired": ["A·1"], "exit_type": "PASS",
                           "exit_line": line, "ctx_keys_set": []})


def governance_run(journal, row="R1"):
    """A run whose C·2 declared `row` governance-gated and whose prove PASS cleared to its owner gate."""
    ok(journal, Call("gate", {"task": {"name": "decide", "stop_criterion": "s", "difficulty": "HIGH",
                                       "governance_gated": row}}), "PLAN_NEEDED")
    a_exit(journal, GOV_PASS)
    ok(journal, Call("prove", {}), exit_type="PASS")


# F1 — the terminal owner gate must match the approval to its own decision --------------------
def test_f1_unrelated_owner_approval_does_not_clear_the_governance_gate(journal, repo):
    """The reviewer's scenario: an owner approval recorded for a different action must not
    complete a run whose terminal gate protects the R1 decision."""
    governance_run(journal)
    approve(journal, UNRELATED_AID)
    assert done_tool.run(env_for(journal, repo), {}) == \
        ToolResult(False, None, "owner-gate-pending: ej (approve action_id=R1)")


def test_f1_the_gates_own_decision_clears_it(journal, repo):
    governance_run(journal)
    approve(journal, "R1")
    assert done_tool.run(env_for(journal, repo), {}) == ToolResult(True, "DONE", None)


def test_f1_the_action_id_is_the_row_the_gate_call_declared(journal, repo):
    """Two governance-gated decisions exist; the subject is the one this run's C·2 named."""
    governance_run(journal, row="R2")
    approve(journal, "R1")
    assert done_tool.run(env_for(journal, repo), {}).reason == "owner-gate-pending: ej (approve action_id=R2)"
    approve(journal, "R2")
    assert done_tool.run(env_for(journal, repo), {}).ok


def test_f1_governance_gated_plan_with_no_readable_row_fails_closed(journal, repo):
    """No executed `gate` call names a row, so the subject is unknown — no approval matches."""
    a_exit(journal, GOV_PASS)
    ok(journal, Call("prove", {}), exit_type="PASS")
    approve(journal, UNRELATED_AID)
    approve(journal, "R1")
    assert done_tool.run(env_for(journal, repo), {}).reason == \
        f"owner-gate-pending: ej (approve action_id={done_tool.UNKNOWN_ROW})"


def test_f1_a_plain_owner_gate_arg_gets_its_own_action_id(journal, repo):
    """Not governance-gated: the prove call's own gate=owner(...) clears this run's plan, and the
    terminal gate now carries an id (`plan:<run_id>`) instead of accepting any owner approval."""
    a_exit(journal, PLAIN_PASS)
    ok(journal, Call("prove", {"gate": "owner(ej)", "gate_at": "commit"}), exit_type="PASS")
    approve(journal, UNRELATED_AID)
    assert done_tool.run(env_for(journal, repo), {}).reason == "owner-gate-pending: ej (approve action_id=plan:rev-b)"
    approve(journal, "plan:rev-b")
    assert done_tool.run(env_for(journal, repo), {}).ok


# F2 — invariants_checked names only checks that ran -------------------------------------------
def test_f2_ingest_return_no_longer_declares_an_invariant_it_never_runs(journal, repo):
    """5 live dispatches: `dispatch` is refused by I5 and `ingest_return` is not checked at all,
    so its journaled `invariants_checked` must be empty rather than naming I5."""
    for f in "abcde":
        ok(journal, Call("dispatch", {"role": "x", "framing": f}), f.upper())
    assert shared.live_dispatches(journal.read()) == 5
    d = Call("dispatch", {"role": "x", "framing": "f"})
    ing = Call("ingest_return", {"agent_id": "A"})
    assert inv.check_invariants(d, Ctx(), journal.read(), TOOLS, cwd=repo) == \
        [inv.Refusal("I5", "live_dispatches=5, CAP=3, no slot")]
    assert inv.check_invariants(ing, Ctx(), journal.read(), TOOLS, cwd=repo) == []
    assert inv.invariants_for(ing) == []
    st = loop_step(TOOLS, ing, journal, Ctx(), cwd=repo)
    assert st.refused_by is None
    assert journal.read()[-1]["invariants_checked"] == []


def test_f2_invariants_checked_names_only_checks_that_ran(journal, repo):
    """For every registered tool: the ids `invariants_for` journals are exactly the ids the loop
    evaluation reports back plus the ones ELSEWHERE_CHECKED records as running outside it."""
    for name in TOOLS:
        call = Call(name, {})
        evaluated, _ = inv.evaluate_loop_invariants(call, Ctx(), journal.read(), TOOLS, cwd=repo)
        assert evaluated == list(inv.LOOP_CHECKED.get(name, ())), name
        assert inv.invariants_for(call) == evaluated + list(inv.ELSEWHERE_CHECKED.get(name, ())), name
    assert set(inv.ELSEWHERE_CHECKED) == {"done", "prove"}  # the two the module docstring justifies
    assert "ingest_return" not in inv.LOOP_CHECKED and "ingest_return" not in inv.ELSEWHERE_CHECKED
