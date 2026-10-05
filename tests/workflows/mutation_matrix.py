"""The mutation matrix — does the gate actually reject a design that breaks a rule?

Recommendation that both domain experts converged on, and the one change the register calls cheapest and most
decisive: take a design the gate **passes**, inject one known-bad change at a time, and observe whether the rule
that should fire does. A rule that never fires on a design built to break it is not a rule.

Four outcomes, and they mean different things:

  CAUGHT      the expected rule fired — the gate has this rule and it works
  MISSED      the expected rule did not fire — a **gate bug**; the rule is dead code
  HOLE        the algorithm requires something the gate has no rule for, and nothing fired. Not a bug in the
              gate's code but in its coverage — this is the number that says how much of the gate is real
  ALARM       nothing should have fired and something did — my understanding of the gate was wrong

Mutations are injected into one design the gate passes (`runs/20261004-corpus-fulltest/designs/p050.json`), one at a
time, on a deep copy. No model calls.

Run: python3 mutation_matrix.py            exit 1 if any MISSED or ALARM
"""
from __future__ import annotations

import copy
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude/skills/workflow-design/scripts"))
import design_gate as dg  # noqa: E402

TYPES = dg.parse_types(ROOT / "docs" / "TASK_TYPES.md")
GOOD = json.loads((ROOT / "runs/20261004-corpus-fulltest/designs/p050.json").read_text())


def review_node(d: dict) -> dict | None:
    return next((n for n in d["nodes"] if n.get("category") == "code review"), None)


# ---- mutations that SHOULD trip a named rule ------------------------------------------------
def m_unknown_category(d):
    d["categories"] = ["frobnicate"]
    d["nodes"][0]["category"] = "frobnicate"


def m_builds_without_product_touch(d):
    d["touched_paths"] = []


def m_node_without_check(d):
    del d["nodes"][0]["check"]


def m_node_missing_a_five_thing(d):
    """G3: the contents, not the names — drop one and the node has no contract."""
    d["nodes"][0].pop("intent", None)


def m_loop_missing(d):
    del d["nodes"][0]["loop"]


def m_loop_without_limit(d):
    del d["nodes"][0]["loop"]["limit"]


def m_loop_without_exit(d):
    del d["nodes"][0]["loop"]["exit"]


def m_loop_without_feedback(d):
    del d["nodes"][0]["loop"]["feedback"]


def m_needs_unknown_node(d):
    d["nodes"][0]["needs"] = ["does-not-exist"]


def m_dependency_cycle(d):
    r = review_node(d)
    d["nodes"][0]["needs"] = [r["id"]]


def m_unknown_pipeline(d):
    d["pipeline"] = "no such pipeline"


def m_challenger_below_twenty_percent(d):
    d["design_source"] = {"type": "challenger", "claim": 0.10, "basis": "x"}


def m_challenger_without_basis(d):
    d["design_source"] = {"type": "challenger", "claim": 0.30}


def m_drop_the_reviewer(d):
    d["nodes"] = [n for n in d["nodes"] if n.get("category") != "code review"]


def m_reviewer_is_the_same_kind(d):
    r = review_node(d)
    r["engine"] = d["nodes"][0]["engine"].split("+")[0].strip()      # same leading engine as the builder


def m_node_category_not_claimed(d):
    d["nodes"].append({"id": "x1", "category": "web search", "engine": "agy", "check": "c",
                       "brief_given": "b", "intent": "i",
                       "stop": {"criteria": "c", "baseline": "b", "must_not_change": "m"},
                       "returns": "r", "state_reads": "s", "tools": ["x"], "evidence": ["e"],
                       "needs": []})


def m_claimed_category_without_a_node(d):
    d["categories"] = sorted(set(d["categories"]) | {"web search"})


# ---- what the ALGORITHM requires and the gate has no rule for ---------------------------------
def m_split_reviewer_is_one_of_the_builders(d):
    """Register 8.1: under the engine split a codex reviewer is a different kind from the opencode half but not
    from the codex half. G6 checks the reviewer against what it reviews, so it must fire."""
    for n in d["nodes"]:
        if n["category"] == "code review":
            n["engine"] = "opencode MiniMax-M3.1-Flash-Preview"
            break


def m_loop_limit_is_a_boolean(d):
    """Found 2026-10-05 by checklist question 4 ("name one failing input"): `isinstance(True, int)` is True."""
    for n in d["nodes"]:
        if n.get("loop"):
            n["loop"]["limit"] = True
            return


def m_others_builds_in_one_node(d):
    """G13: `others` is exempt from the category checks, so one node could scope the unknown and build on it."""
    d["categories"] = ["others"]
    d["nodes"] = [dict(d["nodes"][0], category="others", needs=[])]


def m_baseline_command_is_a_placeholder(d):
    """Found by Claude Code on its own design, 2026-10-05: `UNRESOLVED` is not a test command."""
    d["baseline"]["command"] = "UNRESOLVED: the repo's own test command, found by n1"


def m_touched_paths_is_a_placeholder(d):
    """The same hole on the other field: a promise to name the paths later is not naming them."""
    d["touched_paths"] = ["TBD"]


def m_engine_is_the_tables_placeholder(d):
    """Register 5.6, found 2026-10-05: `others` has no engine, and the placeholder `—` passed the gate."""
    d["nodes"][0]["engine"] = "—"


def m_no_baseline(d):
    """G10 (closed 2026-10-05): a design that builds must name the baseline command and its owner."""
    d.pop("baseline", None)


def m_baseline_owner_runs_too_late(d):
    """G10: the owner must run before the first building node, not after it."""
    d["baseline"]["captured_by"] = d["nodes"][-1]["id"]


def m_no_three_part_stop(d):
    """G3 (closed 2026-10-05): the stop carries method 3.6's three parts, or the node has no contract."""
    for n in d["nodes"]:
        n["stop"] = {"criteria": "the check passes"}


def m_no_contents(d):
    """G3 (closed 2026-10-05): the five things are contents, not a list of their names."""
    for n in d["nodes"]:
        n.pop("brief_given", None)
        n.pop("stop", None)
        n.pop("returns", None)
        n.pop("tools", None)
        n.pop("evidence", None)


def m_placeholder_check_rather_than_the_rows_check(d):
    """The row's check is "tests/build pass (script)"; the design may say anything non-empty."""
    d["nodes"][0]["check"] = "see TASK_TYPES.md"


def m_no_sabotage_proof(d):
    """G9: a building node must carry the proof its check can fail. The matrix's base design carries one."""
    for n in d["nodes"]:
        n.pop("sabotage", None)


MATRIX = [
    # (name, mutation, rule that must fire, note)
    ("unknown category", m_unknown_category, "G1", ""),
    ("builds, no product path", m_builds_without_product_touch, "G2", ""),
    ("node without a check", m_node_without_check, "G3", ""),
    ("a node missing one of the five contents", m_node_missing_a_five_thing, "G3", ""),
    ("loop object missing", m_loop_missing, "G3", ""),
    ("loop without a limit", m_loop_without_limit, "G3", ""),
    ("loop without an exit", m_loop_without_exit, "G3", ""),
    ("loop without feedback", m_loop_without_feedback, "G3", ""),
    ("needs an unknown node", m_needs_unknown_node, "G4", ""),
    ("dependency cycle", m_dependency_cycle, "G4", ""),
    ("unknown pipeline", m_unknown_pipeline, "G4", ""),
    ("challenger claim 10%", m_challenger_below_twenty_percent, "G5", ""),
    ("challenger without basis", m_challenger_without_basis, "G5", ""),
    ("drop the reviewer", m_drop_the_reviewer, "G6", ""),
    ("reviewer of the same kind", m_reviewer_is_the_same_kind, "G6", ""),
    ("under the split, the reviewer is one of the builder kinds",
     m_split_reviewer_is_one_of_the_builders, "G6", ""),
    ("node category not claimed", m_node_category_not_claimed, "G8", ""),
    ("claimed category, no node", m_claimed_category_without_a_node, "G8", ""),
    ("check points at the table", m_placeholder_check_rather_than_the_rows_check, "G3", ""),
    ("no sabotage proof", m_no_sabotage_proof, "G9", ""),
    # closed 2026-10-05 by the format change: the design now carries a `baseline` and the five things as
    # contents, so the three mutations that used to be holes are rules with a mutation each.
    ("the loop limit is a boolean", m_loop_limit_is_a_boolean, "G3", ""),
    ("one `others` node that builds", m_others_builds_in_one_node, "G13", ""),
    ("`baseline.command` is a placeholder", m_baseline_command_is_a_placeholder, "G12", ""),
    ("`touched_paths` is a placeholder", m_touched_paths_is_a_placeholder, "G12", ""),
    ("the engine is the table's `—` placeholder", m_engine_is_the_tables_placeholder, "G11", ""),
    ("no baseline", m_no_baseline, "G10", ""),
    ("the baseline's owner runs too late", m_baseline_owner_runs_too_late, "G10", ""),
    ("no three-part stop", m_no_three_part_stop, "G3", ""),
    ("no contents behind the five names", m_no_contents, "G3", ""),
]


def main(self_check: bool = False) -> int:
    """`self_check` neuters every mutation, so no rule can fire. If the matrix cannot then report MISSED for the
    rules it claims to test, it is not a check and its green run means nothing."""
    rows, missed, alarms = [], 0, 0
    for name, mutate, expect, note in MATRIX:
        d = copy.deepcopy(GOOD)
        if not self_check:
            mutate(d)
        findings = dg.validate_design(d, TYPES)
        fired = sorted({f.split(":")[0] for f in findings})
        if expect is None:
            outcome = "HOLE" if not fired else "ALARM"
            alarms += fired != []
        else:
            outcome = "CAUGHT" if expect in fired else "MISSED"
            missed += outcome == "MISSED"
        rows.append((outcome, name, expect or "—", ",".join(fired) or "—", note))

    width = max(len(r[1]) for r in rows)
    for outcome, name, expect, fired, note in rows:
        flag = {"CAUGHT": "  ", "MISSED": "!!", "HOLE": "  ", "ALARM": "!!"}[outcome]
        print(f"  {flag} {outcome:6} {name:{width}}  want {expect:4} got {fired:10} {note}")

    caught = sum(1 for r in rows if r[0] == "CAUGHT")
    total_should = sum(1 for r in rows if r[2] != "—")
    holes = sum(1 for r in rows if r[0] == "HOLE")
    print(f"\n  gate catches {caught}/{total_should} mutations aimed at its rules")
    print(f"  and cannot see {holes} mutations that break what the algorithm requires")
    print(f"  missed rules: {missed}   false alarms: {alarms}")
    if self_check:
        able = missed > 0
        print(f"\n  MUTATION MATRIX CAN FAIL: {able}  (with every mutation neutered, {missed} rules went unfired)")
        return 0 if able else 1
    return 1 if (missed or alarms) else 0


if __name__ == "__main__":
    sys.exit(main("--self-check" in sys.argv[1:]))
