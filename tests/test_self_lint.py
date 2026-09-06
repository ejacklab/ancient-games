"""§12's self-lint scorecard — the nine lints run against the spec's own
content: V3_6_SPEC.md's §10 (copied to tests/fixtures/) for the trace-borne
lints, V3_3_SPEC.md's §6 table (V3.5 carries it by reference, unchanged)
for the return-contract lint, and this package's data rows for §5.
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

SPEC = (Path(__file__).parent / "fixtures" / "V3_6_SPEC.md").read_text()
SPEC_V33 = (Path(__file__).parent / "fixtures" / "V3_3_SPEC.md").read_text()  # carries the §6 table V3.5 references


def _section(title_re: str, text: str = SPEC) -> str:
    m = re.search(rf"^## {title_re}.*?$(.*?)(?=^## |\Z)", text, re.S | re.M)
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
    assert "Unchanged from `V3_5_SPEC.md` §6" in _section(r"6\. Return contract")
    rows = _table_rows(_section(r"6\. Return contract", SPEC_V33), "field")
    assert len(rows) == 12  # 12 rows, 12 filled cells
    assert lints.lint_return_field_without_escape_value(rows) == []
    assert [r["field"] for r in rows] == [r.field for r in RETURN_CONTRACT]
    # the package's FOLLOW_ON shape carries V3.5's fourth disposition value; every other cell matches verbatim
    assert [r["escape_value"] for r in rows] == [r.escape_value for r in RETURN_CONTRACT]
    assert "escalated" in next(r for r in RETURN_CONTRACT if r.field == "FOLLOW_ON").shape


def test_schema_field_without_escape_value_passes_on_section_5_rows():
    # V3_3 §5 is unchanged-by-reference; the data rows are the table.
    assert lints.lint_schema_field_without_escape_value(FIELDS) == []


def test_claims_without_evidence_vacuous():
    # No live CLAIMS-return instance exists inside the spec; every §10 claim cites inline.
    assert "CLAIMS:" not in _section(r"10\. Trace test cases")
    assert lints.lint_claims_without_evidence([]) == []


def test_follow_on_dispositions_in_section_10_pass():
    """Every FOLLOW_ON disposition §10 states (T1's escalated:ej ×2 and dismissed:out-of-scope,
    T2's new-task / dismissed:out-of-scope, the new-task entries) passes the four-value lint."""
    sec10 = _section(r"10\. Trace test cases")
    tags = re.findall(r"→ (escalated:[\w-]+|dismissed:[\w-]+|new-task|fixed)", sec10)
    tags += re.findall(r"\b(new-task|escalated:ej|dismissed:out-of-scope)\b", sec10)
    assert {"escalated:ej", "dismissed:out-of-scope", "new-task"} <= set(tags)
    assert lints.lint_follow_on_without_disposition([(t, t) for t in tags]) == []
    # and the tag the run file actually used is what the lint (and V3.5) reject
    assert lints.lint_follow_on_without_disposition([("NetOutcomeResolver", "EJ decision")])


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
    # Case 3 / (i) second pass PASS; Case 1 and (ii) disclosed PASS; the undisclosed hypothetical FAILs; T1 first pass FAILs
    run3 = cases.run_case3(Journal(journal.path, "c3"), second_pass=True)
    assert lints.lint_corroboration_capped(run3.plan, run3.events) == []
    run_i = cases.run_case_i(Journal(journal.path + ".i", "ci"), second_pass=True)
    assert lints.lint_corroboration_capped(run_i.plan, run_i.events) == []
    run1 = cases.run_case1(Journal(journal.path + ".1", "c1"))
    assert lints.lint_corroboration_capped(run1.plan, run1.events) == []
    run_t1 = cases.run_t1(Journal(journal.path + ".t1", "t1"))
    assert [f.subject for f in lints.lint_corroboration_capped(run_t1.plan, run_t1.events)] == ["six-are-dead"]
    run_ii = cases.run_case_ii(Journal(journal.path + ".ii", "cii"))
    assert lints.lint_corroboration_capped(run_ii.plan, run_ii.events) == []
    run_ii.plan.exit_line = "Prove: PASS, plan cleared to owner(ej) gate."
    assert lints.lint_corroboration_capped(run_ii.plan, run_ii.events)


def test_hub_touched_without_tripwire_on_section_10_entries(journal):
    # every hub≠[] entry in §10 (T1, Case 1, (i), Case (ii)) names its tripwire and the journal shows it ran (Z4′, AA3′)
    for i, build in enumerate((cases.run_t1, cases.run_case1, cases.run_case_i, cases.run_case_ii)):
        run = build(Journal(f"{journal.path}.{i}", str(i)))
        assert any(e.hub for e in run.plan.entries)
        assert lints.lint_hub_touched_without_tripwire(run.plan, run.events) == []
    assert "Tripwire" in _section(r"10\. Trace test cases").split("### Case (ii)")[1]


def test_downstream_consumer_check_recorded_for_all_three_stakes1_entries(journal):
    """T2, T3, and Case 3's docstring edit each show a consumer_check event inline in V3.5 §10."""
    for i, build in enumerate((cases.run_t2, cases.run_t3, cases.run_case3)):
        run = build(Journal(f"{journal.path}.{i}", str(i)))
        entries = [e for e in run.plan.entries if e.stakes == 1 and not e.hub]
        assert entries
        assert lints.lint_downstream_consumer_check_unrecorded(Plan(entries), run.events) == []
    run = cases.run_t2(journal)
    assert lints.lint_downstream_consumer_check_unrecorded(Plan([PlanEntry("t3-produce", ["research/holdout_recommendation.md"], 1, [])]),
                                                           run.events)  # a different run's record does not cover it
    sec10 = _section(r"10\. Trace test cases")
    assert sec10.count("consumer_check{") == 3
