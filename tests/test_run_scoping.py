"""A Journal bound to a run hands out only that run's events (journal.Journal.read).

The guarantee at stake: corroboration counts sources *this run* produced. On a shared
journal file the unscoped read let a run with zero claims of its own clear a 2-source
bar on another run's evidence. Every figure below is a real return value of the real
stage/tool on a real (merged) journal — never a re-derivation.
"""
from __future__ import annotations

import copy
from pathlib import Path

import pytest

import test_index as ti
from ancient_games import stages
from ancient_games.ctx import Ctx
from ancient_games.hybrid.tools import _plan, prove as prove_tool, render_trace as render_trace_tool, run_lint as run_lint_tool
from ancient_games.hybrid.types import ToolEnv
from ancient_games.journal import Journal, read_events
from ancient_games.trace import render_trace


def _two_foreign_sources(path: str) -> Journal:
    ja = Journal(path, "runA")
    for fr in ("f1", "f2"):
        ja.claim_recorded(claim_id="C1", author=f"agent-{fr}", actor="agent-x", kind="judgment",
                          text="X is dead", evidence_type="command", evidence_ref="cmd", framing=fr)
    return ja


def _ctx() -> Ctx:
    ctx = Ctx()
    ctx.stakes = 2
    ctx.actor = {"act": "MAIN"}
    return ctx


def test_corroborate_does_not_count_another_runs_sources(tmp_path):
    """The reviewer's F1 repro: run B records nothing, run A recorded two differently
    framed sources on C1 in the same file. B must count 0, not A's 2."""
    path = str(tmp_path / "shared.jsonl")
    _two_foreign_sources(path)
    jb = Journal(path, "runB")
    ctx = _ctx()
    ex = stages.corroborate(ctx, [stages.Claim("C1", "judgment")], jb, "act")
    r = ex.result("C1")
    assert (r.exit_type, r.n_available, r.n_required, r.remedy) == ("CAPPED", 0, 2, "gate-checkpoint")
    assert ctx.n_sources == {"C1": 0}
    assert ex.exit_line == ("Corroborate: C1: n=0/2, capped, remedy=gate-checkpoint; "
                            "reconciled=agree, corroboration-capped=true.")
    assert [g.reason for g in ctx.gate_reason] == ["corroboration-capped"]


def test_corroborate_still_counts_the_runs_own_sources(tmp_path):
    """The same two events, read by the run that wrote them: unchanged SOURCES n=2/2."""
    path = str(tmp_path / "own.jsonl")
    ja = _two_foreign_sources(path)
    ctx = _ctx()
    ex = stages.corroborate(ctx, [stages.Claim("C1", "judgment")], ja, "act")
    assert (ex.result("C1").exit_type, ctx.n_sources) == ("SOURCES", {"C1": 2})
    assert ex.exit_line == "Corroborate: C1: n=2/2; reconciled=agree."


def test_read_all_still_returns_every_run(tmp_path):
    path = str(tmp_path / "shared.jsonl")
    _two_foreign_sources(path)
    jb = Journal(path, "runB")
    assert jb.read() == []
    assert [e["run_id"] for e in jb.read_all()] == ["runA", "runA"] == [e["run_id"] for e in read_events(path)]


# --- merged real journals ------------------------------------------------------------------------
@pytest.fixture
def merged(tmp_path):
    """(merged journal path, the run_id of COLLIDING[0], that run's own journal path).

    Function-scoped: `prove` appends its A exit to the journal it reads."""
    lines: list[str] = []
    for p in ti.COLLIDING:
        lines += [ln for ln in Path(p).read_text().splitlines() if ln.strip()]
    path = str(tmp_path / "merged.jsonl")
    Path(path).write_text("\n".join(lines) + "\n")
    run_id = ti._run_id(read_events(ti.COLLIDING[0]))
    assert len({e["run_id"] for e in read_events(path)}) == 3
    return path, run_id, ti.COLLIDING[0]


def test_prove_and_run_lint_build_the_same_plan_from_a_merged_journal(merged, monkeypatch, tmp_path):
    path, run_id, own = merged
    built: dict[str, object] = {}

    def spy(name, real):
        def wrapper(*a, **kw):
            plan = real(*a, **kw)
            built[name] = copy.deepcopy(plan)  # `prove` stamps exit_line onto the plan afterwards
            return plan
        return wrapper

    monkeypatch.setattr(prove_tool, "plan_from_journal", spy("prove", _plan.plan_from_journal))
    monkeypatch.setattr(run_lint_tool, "plan_from_journal", spy("run_lint", _plan.plan_from_journal))
    env = ToolEnv(run_id, path, Ctx(), cwd=str(tmp_path), tools={})
    assert prove_tool.run(env, {"gate": "checkpoint"}).ok
    assert run_lint_tool.run(env, {"gate": "checkpoint"}).ok
    assert built["prove"] == built["run_lint"]
    assert built["prove"].entries, "the merged journal produced an empty plan: nothing is being compared"
    # and that shared plan is the one this run's own journal produces, not the merged file's
    merged_plan = built["prove"]
    own_env = ToolEnv(run_id, own, Ctx(), cwd=str(tmp_path), tools={})
    assert run_lint_tool.run(own_env, {"gate": "checkpoint"}).ok
    assert built["run_lint"] == merged_plan


def test_render_trace_on_a_merged_journal_renders_only_the_titled_run(merged, tmp_path):
    path, run_id, own = merged
    env = ToolEnv(run_id, path, Ctx(), cwd=str(tmp_path), tools={})
    got = render_trace_tool.run(env, {"title": "T"})
    assert got.ok
    assert got.value == render_trace(read_events(own), "T")
    assert got.value.splitlines()[0] == f"# T — {run_id}"
    # the merged file really does carry the other runs: each renders its own, different trace
    for other in ti.COLLIDING[1:]:
        other_run = ti._run_id(read_events(other))
        assert other_run != run_id
        rendered = render_trace(read_events(path), "T", run_id=other_run)
        assert rendered == render_trace(read_events(other), "T")
        assert rendered != got.value
