"""workload.py — the design-time engine split. EJ, 2026-10-04: give opencode priority.

The default is the *smallest lead that counts as priority*, because that is also the most independence available.
A forced share is supported and is bought with more self-testing, at 2s-1 of the modules.
"""
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


def numbered(n):
    return modules([f"m{i:02d}" for i in range(n)])


def self_tested(nodes, engines):
    by_module = {}
    for n in nodes:
        by_module.setdefault(workload.module_of(n), set()).add(engines[n["id"]])
    return sum(1 for e in by_module.values() if len(e) == 1)


@pytest.mark.parametrize("count", [3, 5, 10, 20, 50])
def test_default_gives_priority_at_the_lowest_cost(count):
    """Opencode leads, and exactly one module self-tests — the least possible while still leading.

    Each self-tested module moves two nodes to the primary engine, so the minimum lead is (N+1)/2N and costs a
    single module its independent tests, whatever the plan size.
    """
    nodes = numbered(count)
    engines = workload.assign(nodes)
    primary = sum(1 for e in engines.values() if e == "opencode")
    assert primary > len(engines) / 2, "opencode must have priority"
    assert primary == count + 1
    assert self_tested(nodes, engines) == 1
    assert workload.check(nodes, engines) == []


def test_five_modules_is_exactly_sixty_forty():
    """EJ's target is not hard to hit — at five modules it is the *minimum* lead, so it comes out for free."""
    nodes = numbered(5)
    engines = workload.assign(nodes)
    assert sum(1 for e in engines.values() if e == "opencode") == 6
    assert sum(1 for e in engines.values() if e == "codex") == 4


def test_the_documented_five_module_pattern():
    """The worked example in the docstring, so the documented table cannot drift from the code."""
    nodes = modules(["ingest", "parse", "store", "report", "notify"])
    engines = workload.assign(nodes)
    got = {m: (engines[f"{m}-dev"], engines[f"{m}-test"]) for m in
           ("ingest", "notify", "parse", "report", "store")}
    assert got["ingest"] == ("opencode", "codex")
    assert got["notify"] == ("opencode", "codex")
    assert got["parse"] == ("opencode", "opencode")      # the one module that self-tests
    assert got["report"] == ("codex", "opencode")
    assert got["store"] == ("codex", "opencode")


def test_forcing_a_bigger_lead_costs_self_testing():
    """A 60% share across 20 modules self-tests 4 of them; the minimum lead self-tests 1."""
    nodes = numbered(20)
    forced = workload.assign(nodes, share=0.6)
    assert sum(1 for e in forced.values() if e == "opencode") == 24
    assert self_tested(nodes, forced) == 4
    assert self_tested(nodes, workload.assign(nodes)) == 1
    assert workload.check(nodes, forced) == []


def test_fifty_fifty_is_fully_independent_but_has_no_priority():
    """The whole trade in one test: full independence is available, and it costs the priority EJ asked for.

    This is why the default takes the minimum lead instead of splitting evenly.
    """
    nodes = numbered(10)
    engines = workload.assign(nodes, share=0.5)
    assert self_tested(nodes, engines) == 0, "an even split crosses every pair"
    assert any("no priority" in f for f in workload.check(nodes, engines))


def test_assignment_is_independent_of_input_order():
    """A resumed or re-serialized plan must not silently move a node to another engine."""
    nodes = numbered(20)
    assert workload.assign(nodes) == workload.assign(list(reversed(nodes)))


def test_check_flags_a_plan_with_no_priority():
    nodes = numbered(10)
    engines = workload.assign(nodes, share=0.5)
    assert any("no priority" in f for f in workload.check(nodes, engines))


def test_check_flags_self_testing_beyond_what_the_lead_costs():
    """Half the modules wholly opencode and half wholly codex: an even split that self-tests everything."""
    nodes = numbered(10)
    engines = {}
    for n in nodes:
        engines[n["id"]] = "opencode" if workload.module_of(n).endswith(("0", "2", "4", "6", "8")) else "codex"
    findings = workload.check(nodes, engines)
    assert any("grade their own tests" in f for f in findings)


def test_check_catches_a_rule_5_breach():
    nodes = [{"id": "a-dev", "role": "coder"}, {"id": "a-test", "role": "tester"},
             {"id": "v1", "role": "verifier", "verified_by": "a-dev"}]
    engines = {"a-dev": "opencode", "a-test": "codex", "v1": "opencode"}
    assert any("rule 5" in f for f in workload.check(nodes, engines))


def test_module_and_kind_can_be_declared_explicitly():
    """Explicit `module` and `kind` beat the id/role heuristics."""
    two = [{"id": "n1", "role": "builder", "module": "auth", "kind": "code"},
           {"id": "n2", "role": "builder", "module": "auth", "kind": "test"},
           {"id": "n3", "role": "builder", "module": "billing", "kind": "code"},
           {"id": "n4", "role": "builder", "module": "billing", "kind": "test"}]
    engines = workload.assign(two)
    assert set(engines) == {"n1", "n2", "n3", "n4"}
    assert engines["n1"] != engines["n2"], "a declared pair must still be crossed"


def test_a_single_module_takes_priority_over_independence():
    """With one pair, priority and crossing are mutually exclusive and priority wins (EJ's instruction).

    Two nodes can go 2-0 to the primary engine, or 1-1 and leave it with no lead at all. So a one-module plan
    self-tests, which is correct rather than a bug — and the check agrees, because a 100% share costs exactly the
    one module of self-testing it gets.
    """
    nodes = [{"id": "only-dev", "role": "coder"}, {"id": "only-test", "role": "tester"}]
    engines = workload.assign(nodes)
    assert set(engines.values()) == {"opencode"}
    assert workload.check(nodes, engines) == []
