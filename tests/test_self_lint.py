"""§12 item 10 — the nine lints run against the spec's own tables
(tests/fixtures/V3_3_SPEC.md) and this package's data rows, asserting the
PASS §12 claims where §10/§6 content actually supports it.

Two of §12's claims are not supported by V3_3_SPEC.md's own content
(v3_3_review.md §E: Y4, Y5); those are exercised in test_traces.py (Y4,
xfail) and test_lints.py (Y5, a real FAIL input), not asserted PASS here.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

import cases
from ancient_games import lints
from ancient_games.journal import Journal
from ancient_games.schema import FIELDS, RETURN_CONTRACT
from ancient_games.stages import Plan, PlanEntry

SPEC = (Path(__file__).parent / "fixtures" / "V3_3_SPEC.md").read_text()


def _section(title_re: str) -> str:
    m = re.search(rf"^## {title_re}.*?$(.*?)(?=^## |\Z)", SPEC, re.S | re.M)
    assert m, title_re
    return m.group(1)


def _table_rows(text: str, first_col: str) -> list[dict[str, str]]:
    lines = [ln for ln in text.splitlines() if ln.startswith("|")]
    header = None
    rows = []
    for ln in lines:
        cells = [c.strip() for c in ln.strip().strip("|").split(" | ")]
        if header is None:
            if cells[0].strip("`") == first_col:
                header = [c.strip("`") for c in cells]
            continue
        if set(ln.replace("|", "").strip()) <= {"-", " "}:
            continue
        rows.append(dict(zip(header, [c.replace("`", "") for c in cells])))
    return rows


def test_return_field_without_escape_value_passes_on_spec_section_6():
    rows = _table_rows(_section(r"6\. Return contract"), "field")
    assert len(rows) == 12  # §12 item 9: 12 rows, 12 filled cells
    assert lints.lint_return_field_without_escape_value(rows) == []
    assert [r["field"] for r in rows] == [r.field for r in RETURN_CONTRACT]
    assert [r["escape_value"] for r in rows] == [r.escape_value for r in RETURN_CONTRACT]


def test_schema_field_without_escape_value_passes_on_section_5_rows():
    # V3_3 §5 is unchanged-by-reference; the data rows are the table.
    assert lints.lint_schema_field_without_escape_value(FIELDS) == []


def test_claims_without_evidence_vacuous():
    # No live CLAIMS-return instance exists inside the spec; every §10 claim cites inline.
    assert "CLAIMS:" not in _section(r"10\. Trace test cases")
    assert lints.lint_claims_without_evidence([]) == []


def test_follow_on_dispositions_named_in_the_spec_pass():
    # V3_3_SPEC.md names dispositions in §12 item 10 only; each tag it lists that is
    # in the lint's enum passes. ("EJ decision" from T1_trace.md is Y5 — see test_lints.)
    tags = re.findall(r"`(new-task|fixed|dismissed:[^`]+)`", SPEC)
    assert tags
    assert lints.lint_follow_on_without_disposition([(t, t) for t in tags]) == []


def test_scope_delta_present_in_the_run_traces():
    for name in ("T1_trace.md", "T2_trace.md"):
        text = (Path(__file__).parent / "fixtures" / name).read_text()
        m = re.search(r"`SCOPE_DELTA`: (.+)", text)
        assert m
        assert lints.lint_scope_delta_missing({"SCOPE_DELTA": m.group(1)}, {"SCOPE": True}) == []


def test_evidence_after_verdict_vacuous():
    assert not re.search(r"^## Verdict", SPEC, re.M)
    assert lints.lint_evidence_after_verdict("") == []


@pytest.fixture
def journal(tmp_path):
    return Journal(str(tmp_path / "j.jsonl"))


def test_corroboration_capped_on_section_10_cases(journal):
    # Case 3 second pass PASS; Case (ii) disclosed PASS; the undisclosed hypothetical FAILs (test_lints covers Case 1 forms)
    run3 = cases.run_case3(Journal(journal.path, "c3"), second_pass=True)
    assert lints.lint_corroboration_capped(run3.plan, run3.events) == []
    run_ii = cases.run_case_ii(Journal(journal.path + ".ii", "cii"))
    assert lints.lint_corroboration_capped(run_ii.plan, run_ii.events) == []
    run_ii.plan.exit_line = "Prove: PASS, plan cleared to owner(ej) gate."
    assert lints.lint_corroboration_capped(run_ii.plan, run_ii.events)


def test_hub_touched_without_tripwire_on_section_10_entries(journal):
    # every hub≠[] entry in §10 (T1, Case 1, (i), Case (ii)) names its tripwire
    for i, build in enumerate((cases.run_t1, cases.run_case1, cases.run_case_i, cases.run_case_ii)):
        run = build(Journal(f"{journal.path}.{i}", str(i)))
        assert any(e.hub for e in run.plan.entries)
        assert lints.lint_hub_touched_without_tripwire(run.plan) == []


def test_downstream_consumer_check_recorded_for_t2(journal):
    run = cases.run_t2(journal)
    entry = next(e for e in run.plan.entries if e.stakes == 1)
    assert entry.hub == []
    assert lints.lint_downstream_consumer_check_unrecorded(Plan([entry]), run.events) == []
    assert lints.lint_downstream_consumer_check_unrecorded(Plan([PlanEntry("t3-produce", "research/holdout_recommendation.md", 1, [])]),
                                                           run.events)  # a different run's record does not cover it
