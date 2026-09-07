"""The Python journal lints are run_id-scoped, like the SQL queries (docs/STORE_DESIGN_DECISION.md §Tests:
the oracle must be right on a merged journal). Every figure here is a real lint's real return value on a
merged journal built from real ablation journals whose claim ids collide — never a re-derivation."""
from __future__ import annotations

from pathlib import Path

import pytest

import test_index as ti
from ancient_games import lints
from ancient_games.journal import read_events


@pytest.fixture(scope="module")
def merged():
    """{run_id: (plan, per-run events)} and the merged event list of ti.COLLIDING (3 real journals, C1 in each)."""
    per_run, lines = {}, []
    for p in ti.COLLIDING:
        events = read_events(p)
        run_id = ti._run_id(events)
        per_run[run_id] = (ti._plan_for_real(events, run_id), events)
        lines += [ln for ln in Path(p).read_text().splitlines() if ln.strip()]
    assert len(per_run) == 3
    import tempfile, os
    d = tempfile.mkdtemp()
    path = os.path.join(d, "merged.jsonl")
    Path(path).write_text("\n".join(lines) + "\n")
    events = read_events(path)
    assert len(events) == sum(len(e) for _, e in per_run.values())
    return per_run, events


THREE = (lints.lint_corroboration_capped, lints.lint_hub_touched_without_tripwire,
         lints.lint_downstream_consumer_check_unrecorded)


# (a) scoped == per-run truth; unscoped differs ------------------------------------------------------------
def test_scoped_python_lints_equal_per_run_results_on_the_merged_journal(merged):
    per_run, events = merged
    for run_id, (plan, own) in per_run.items():
        for lint in THREE:
            assert lint(plan, events, run_id) == lint(plan, own), (lint.__name__, run_id)
        # and run_all_on_plan's python backend, scoped, equals the same backend on the run's own events
        assert (lints.run_all_on_plan(plan, events, backend="python", run_id=run_id)
                == lints.run_all_on_plan(plan, own, backend="python")), run_id


def test_unscoped_python_lints_differ_from_per_run_results_on_the_merged_journal(merged):
    per_run, events = merged
    differing = {}
    for run_id, (plan, own) in per_run.items():
        for lint in THREE:
            scoped, unscoped = lint(plan, events, run_id), lint(plan, events)  # run_id=None: today's behaviour
            if scoped != unscoped:
                differing[(lint.__name__, run_id)] = (scoped, unscoped)
    assert differing, "unscoped == scoped for every lint on every run: the merge does not exercise scoping"
    # concretely: attempt2/UC3 (run ablation-UC3-2): its 8 corroboration-capped findings collapse to 2 when other runs' checks count
    key = ("lint_corroboration_capped", "ablation-UC3-2")
    assert key in differing, sorted(differing)
    scoped, unscoped = differing[key]
    assert (len(scoped), len(unscoped)) == (8, 2), \
        f"ablation-UC3-2 corroboration-capped: scoped={len(scoped)} findings vs unscoped={len(unscoped)}: " \
        f"scoped-only={[f.subject for f in scoped if f not in unscoped]}"
    for (name, run_id), (s, u) in differing.items():
        assert s != u, f"{name} on {run_id}: scoped={s!r} unscoped={u!r}"


def test_run_id_none_keeps_unscoped_behaviour(merged):
    """`run_id=None` reads every event: identical to the pre-change call with no run_id at all."""
    per_run, events = merged
    for run_id, (plan, own) in per_run.items():
        for lint in THREE:
            assert lint(plan, events) == lint(plan, events, None)
            assert lint(plan, own) == lint(plan, own, run_id)  # single-run: scoping is the identity
        assert (lints.run_all_on_plan(plan, own, backend="python")
                == lints.run_all_on_plan(plan, own, backend="python", run_id=run_id))


# (b) differential PASSES on the merged journal (it raised LintBackendDivergence before the scoping) --------
def test_differential_passes_on_the_merged_journal(merged):
    per_run, events = merged
    for run_id, (plan, own) in per_run.items():
        got = lints.run_all_on_plan(plan, events, backend="differential", run_id=run_id)  # raises on divergence
        assert got == lints.run_all_on_plan(plan, own, backend="python"), run_id
        assert got == lints.run_all_on_plan(plan, events, backend="sql", run_id=run_id), run_id
    # the findings compared are real ones, not an empty agreement
    assert sum(len(lints.run_all_on_plan(p, events, backend="differential", run_id=r))
               for r, (p, _) in per_run.items()) >= 9  # UC1-2: 1 hub, UC3-2: 8 capped, UC3-4: 1 (test_real_inputs_carry_findings)
