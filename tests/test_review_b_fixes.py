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
from ancient_games.registry import REGISTRY
from ancient_games.stages import Plan

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


# F3 — the `escalated:` GLOB is not equivalent to lints.DISPOSITION_RE --------------------------
DISPOSITIONS = ["escalated:x", "escalated:ab cd"]  # MAIN's two: python True/False, sql False/True


def _follow_on_journal(tmp_path, name, dispositions):
    j = Journal(str(tmp_path / f"{name}.jsonl"), name)
    j.append({"event": "return", "agent_id": "a",
              "fields": {"CLAIMS": [{"claim_id": "c", "evidence_type": "(opinion)"}],
                         "FOLLOW_ON": [{"finding": f"f{i}", "disposition": d} for i, d in enumerate(dispositions)]}})
    return j


@pytest.mark.parametrize("disposition", DISPOSITIONS)
def test_f3_escalated_glob_agrees_with_the_python_oracle(tmp_path, disposition):
    """Both backends on the same event; `differential` raises LintBackendDivergence when they part."""
    from ancient_games import index, lints
    from ancient_games.stages import Plan

    j = _follow_on_journal(tmp_path, "esc", [disposition])
    events, plan = j.read(), Plan([])
    py = lints.run_all_on_plan(plan, events, backend="python", run_id="esc")
    sql = lints.run_all_on_plan(plan, events, backend="sql", run_id="esc")
    diff = lints.run_all_on_plan(plan, events, backend="differential", run_id="esc")
    assert py == sql == diff
    con = index.memory_index(events)
    try:
        assert index.follow_on_without_disposition(con, "esc") == \
            lints.lint_follow_on_without_disposition([{"finding": "f0", "disposition": disposition}])
    finally:
        con.close()


def test_f3_escalated_x_is_valid_and_escalated_with_a_space_is_not(tmp_path):
    """The two values pinned, so a future rewrite of _DISP_OK cannot flip either silently."""
    from ancient_games import lints

    j = _follow_on_journal(tmp_path, "esc2", DISPOSITIONS)
    got = lints.run_all_on_plan(Plan([]), j.read(), backend="differential", run_id="esc2")
    assert [(f.lint, f.subject) for f in got] == [("follow-on-without-disposition", "f1")]


# F4 — guard()'s stakes=1 early return left the previous action's D·4/D·5 writes in ctx ---------
LEDGER = {"name": "append-ledger", "refs": [{"path": "eval/ledger.jsonl", "mode": "mutate"}],
          "tripwires": {"eval/ledger.jsonl": "wc -l eval/ledger.jsonl"}}
SCRATCH = {"name": "write-notes", "refs": [{"path": "research/notes.md", "mode": "mutate"}]}


def test_f4_a_stakes_1_action_does_not_inherit_the_previous_actions_gate(tmp_path):
    """A stakes-2 action gates and names a tripwire; the stakes-1 action after it has neither,
    so nothing of the first may survive into the second's ctx."""
    from ancient_games.stages import guard as guard_stage
    from ancient_games.hybrid.tools._shared import guard_action

    j = Journal(str(tmp_path / "g.jsonl"), "g")
    ctx = Ctx()
    gated = guard_stage(ctx, guard_action({"action": LEDGER}), j)
    assert gated.exit_type == "GATED" and ctx.tripwire == {"eval/ledger.jsonl": "wc -l eval/ledger.jsonl"}
    assert [(g.who, g.reason) for g in ctx.gate_reason] == [("human(checkpoint)", "stakes-2-checkpoint")]
    plain = guard_stage(ctx, guard_action({"action": SCRATCH}), j)
    assert plain.exit_type == "NO_GATE" and plain.stakes == 1
    assert ctx.tripwire == {} and ctx.gate_reason == []
    assert "tripwire" not in ctx.keys_set() and "gate_reason" not in ctx.keys_set()


def test_f4_a_stale_owner_gate_does_not_name_the_owner_of_a_later_capped_claim(tmp_path):
    """`_owner_for` reads ctx.gate_reason, so the stale stakes-3 entry made a later capped claim
    cite the owner of an action that had already been superseded by a stakes-1 one."""
    from ancient_games.stages import _owner_for, guard as guard_stage
    from ancient_games.hybrid.tools._shared import guard_action

    j = Journal(str(tmp_path / "g2.jsonl"), "g2")
    ctx = Ctx()
    owner_action = {"name": "unseal", "refs": [{"path": "eval.partitions.load_holdout", "mode": "invoke"}],
                    "tripwires": {"eval.partitions.load_holdout": "sha256sum eval/protocol.json"}}
    assert guard_stage(ctx, guard_action({"action": owner_action}), j).gate == "owner"
    assert _owner_for(ctx, REGISTRY) == "ej"
    guard_stage(ctx, guard_action({"action": SCRATCH}), j)
    assert [g.who for g in ctx.gate_reason] == []
    assert _owner_for(ctx, REGISTRY) == "ej"  # falls back to the default, not to the superseded action's row


# F5 — the C·4 split path never accumulated, so CAP was unenforced on split plans ---------------
def _split_task():
    from ancient_games.stages import TaskInput
    return TaskInput(name="four-angles", stop_criterion="all four answered", difficulty="HIGH",
                     capability=["a", "b", "c", "d"], actors={"four-angles": "MAIN"})


def test_f5_split_plan_accumulates_into_the_parent_ctx(tmp_path):
    from ancient_games.stages import gate as gate_stage

    j = Journal(str(tmp_path / "s.jsonl"), "s")
    ctx = Ctx()
    out = gate_stage(ctx, _split_task(), j)
    assert out.exit_type == "PLAN_NEEDED[]" and [g.count for g in out.groups] == [2, 2]
    assert ctx.dispatch_count == 4  # the split plan really dispatches four agents
    assert ctx.count == 2 and ctx.execution_status == "dispatched"
    assert ctx.stop_criterion == "all four answered" and ctx.time_box == "one drafting pass"
    assert out.steps_fired == ["C·1", "C·2", "C·3", "C·4", "C·5"]
    assert out.count == 4 and out.stop_criterion == "all four answered"
    ctx.validate()  # count stays inside 0..3; the plan-wide total lives in dispatch_count


def test_f5_cap_is_enforced_on_a_split_plan(tmp_path):
    """B·1's cap_state reads ctx.dispatch_count: at 4 no slot remains, so a capped judgment claim
    is routed to a gate instead of being told to add another differently-framed source."""
    from ancient_games.stages import Claim, corroborate, gate as gate_stage

    j = Journal(str(tmp_path / "s2.jsonl"), "s2")
    ctx = Ctx()
    gate_stage(ctx, _split_task(), j)
    ctx.stakes = 3
    out = corroborate(ctx, [Claim("J1", "judgment")], j, "four-angles", framings={"J1": ["unused-framing"]})
    r = out.result("J1")
    assert r.exit_type == "CAPPED" and r.remedy == "gate-owner"
    assert [(g.who, g.reason, g.claim_id) for g in ctx.gate_reason] == [("owner(ej)", "corroboration-capped", "J1")]


def test_f5_a_split_plans_dispatch_total_is_a_return_to_planner_finding(tmp_path):
    """The plan A proves carries dispatched_total from ctx.dispatch_count; at 0 the >CAP lint
    could never fire however many agents the groups dispatched."""
    from ancient_games import lints
    from ancient_games.stages import PlanEntry, gate as gate_stage

    j = Journal(str(tmp_path / "s3.jsonl"), "s3")
    ctx = Ctx()
    gate_stage(ctx, _split_task(), j)
    plan = Plan([PlanEntry("four-angles", dispatched_total=ctx.dispatch_count)])
    assert [f.message for f in lints.lint_corroboration_capped(plan, [])] == \
        ["RETURN_TO_PLANNER: four-angles dispatched 4 category-(a) agents > CAP=3"]


# F6 — corroborate: duplicate gate reasons, and ctx written for a dropped claim -----------------
def _capped_ctx():
    ctx = Ctx()
    ctx.actor["act"] = "MAIN"
    ctx.stakes = 2
    ctx.dispatch_count = 3  # no slot remains, so a capped judgment claim routes to the gate
    return ctx


def test_f6_re_running_corroborate_does_not_duplicate_the_gate_reason(tmp_path):
    """loop.REPLAN re-runs corroborate; the HUMAN_GATE line must not carry the same claim twice."""
    from ancient_games.stages import Claim, corroborate

    j = Journal(str(tmp_path / "b.jsonl"), "b")
    ctx = _capped_ctx()
    for _ in range(2):
        out = corroborate(ctx, [Claim("J1", "judgment")], j, "act")
        assert out.result("J1").remedy == "gate-checkpoint"
    assert [(g.who, g.reason, g.claim_id) for g in ctx.gate_reason] == \
        [("human(checkpoint)", "corroboration-capped", "J1")]
    assert [c.claim_id for c in ctx.corroboration_capped] == ["J1"]


def test_f6_an_unverified_claim_writes_nothing_to_ctx(tmp_path):
    """B·4 drops a claim with no cited command; it must not first fire FRAMING/TEMPLATE
    (ctx.n_sources) or a HUMAN_GATE (ctx.corroboration_capped + gate_reason)."""
    from ancient_games.stages import Claim, corroborate

    j = Journal(str(tmp_path / "b2.jsonl"), "b2")
    ctx = _capped_ctx()
    out = corroborate(ctx, [Claim("J1", "judgment", has_command=False)], j, "act")
    assert out.exit_type == "UNVERIFIED" and out.result("J1").exit_type == "UNVERIFIED"
    assert ctx.n_sources == {} and ctx.corroboration_capped == [] and ctx.gate_reason == []
    assert out.exit_line == "Corroborate: ."
