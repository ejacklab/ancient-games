"""workload.py — the design-time engine split (EJ, 2026-10-04: 60% opencode, 40% codex)."""
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / ".claude/skills/workflow-design/scripts"
sys.path.insert(0, str(SCRIPTS))
import workload  # noqa: E402


def modules(names):
    """Paired modules: each has a code node and a test node."""
    out = []
    for m in names:
        out += [{"id": f"{m}-dev", "role": "coder"}, {"id": f"{m}-test", "role": "tester"}]
    return out


def names(n):
    return [f"m{i:02d}" for i in range(n)]


@pytest.mark.parametrize("count", [5, 10, 20, 50])
def test_share_is_exactly_sixty_forty(count):
    nodes = modules(names(count))
    engines = workload.assign(nodes)
    primary = sum(1 for e in engines.values() if e == "opencode")
    assert len(engines) == 2 * count
    assert primary == round(0.6 * 2 * count)


@pytest.mark.parametrize("count", [5, 10, 20, 50])
def test_self_tested_fraction_is_two_s_minus_one(count):
    """At s=0.6 exactly one module in five grades its own tests — the price of the share, not an accident.

    Crossing every pair would give 50/50 and full independence; a 60/40 share is only reachable by letting
    2s-1 = 20% of modules test themselves. So this pins the *optimum*, not a chosen compromise.
    """
    nodes = modules(names(count))
    engines = workload.assign(nodes)
    by_module = {}
    for n in nodes:
        by_module.setdefault(workload.module_of(n), set()).add(engines[n["id"]])
    self_tested = sum(1 for engines_used in by_module.values() if len(engines_used) == 1)
    assert self_tested == round(0.2 * count)


def test_the_periodic_pattern_for_five_modules():
    """The worked example from the docstring, so the documented table cannot drift from the code."""
    nodes = modules(["ingest", "parse", "store", "report", "notify"])
    engines = workload.assign(nodes)
    got = {m: (engines[f"{m}-dev"], engines[f"{m}-test"]) for m in
           ("ingest", "notify", "parse", "report", "store")}
    assert got["ingest"] == ("opencode", "codex")
    assert got["notify"] == ("opencode", "codex")
    assert got["parse"] == ("opencode", "opencode")      # the one self-tested module
    assert got["report"] == ("codex", "opencode")
    assert got["store"] == ("codex", "opencode")


def test_assignment_is_independent_of_input_order():
    """A resumed or re-serialized plan must not silently move a node to another engine."""
    nodes = modules(names(20))
    assert workload.assign(nodes) == workload.assign(list(reversed(nodes)))


def test_check_is_clean_on_a_correct_plan():
    for count in (5, 20, 50):
        nodes = modules(names(count))
        assert workload.check(nodes, workload.assign(nodes)) == []


def test_check_catches_a_plan_that_self_tests_everything():
    nodes = modules(["a", "b", "c", "d", "e"])
    engines = {n["id"]: "opencode" for n in nodes}
    findings = workload.check(nodes, engines)
    assert any("grade their own tests" in f for f in findings)
    assert any("share is 100%" in f for f in findings)


def test_check_catches_a_rule_5_breach():
    nodes = [{"id": "a-dev", "role": "coder"}, {"id": "a-test", "role": "tester"},
             {"id": "v1", "role": "verifier", "verified_by": "a-dev"}]
    engines = {"a-dev": "opencode", "a-test": "codex", "v1": "opencode"}
    assert any("rule 5" in f for f in workload.check(nodes, engines))


def test_at_fifty_fifty_nothing_need_self_test():
    """The other end of the same trade: full independence is available at 50/50 and at no other share."""
    nodes = modules(names(10))
    engines = workload.assign(nodes, share=0.5)
    by_module = {}
    for n in nodes:
        by_module.setdefault(workload.module_of(n), set()).add(engines[n["id"]])
    assert all(len(v) == 2 for v in by_module.values())
    assert workload.check(nodes, engines, share=0.5) == []


def test_module_and_kind_can_be_declared_explicitly():
    nodes = [{"id": "n1", "role": "builder", "module": "auth", "kind": "code"},
             {"id": "n2", "role": "builder", "module": "auth", "kind": "test"}]
    engines = workload.assign(nodes)
    assert set(engines) == {"n1", "n2"}
    assert engines["n1"] != engines["n2"], "a declared pair must still be crossed"
