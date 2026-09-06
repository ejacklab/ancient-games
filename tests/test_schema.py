"""§5/§6 — payload(ctx) and return_contract(ctx) for T2, T1, T3."""
from __future__ import annotations

import pytest

import cases
from ancient_games import schema
from ancient_games.journal import Journal
from ancient_games.schema import FIELDS, RETURN_CONTRACT, TEMPLATE_HEADINGS, payload, return_contract


@pytest.fixture
def journal(tmp_path):
    return Journal(str(tmp_path / "j.jsonl"))


CORE_NAMES = [f.field for f in schema.CORE]


def test_t2_count0_no_payload_but_return_contract(journal):
    run = cases.run_t2(journal)
    assert run.ctx.count == 0
    assert payload(run.ctx) == {}
    rc = return_contract(run.ctx)
    assert set(rc) == {r.field for r in RETURN_CONTRACT} and len(rc) == 12
    # the five MAIN-at-count=0 fields fire; SCOPE was present (E·4's two files)
    assert schema.required_return_fields(run.ctx) == ["REPORT_BACK", "CLAIMS", "SCOPE_DELTA", "FOLLOW_ON", "NOT_DONE"]
    assert rc["VERIFY_OUTPUT"] == "N/A (VERIFY not present in the dispatch)"
    assert rc["VERDICT"].startswith("N/A (role∈{coder, MAIN}")
    assert rc["HUB_INTEGRITY_RESULT"] == "N/A (hub=∅, HUB_INTEGRITY not sent)"


def test_t1_payload_fields(journal):
    run = cases.run_t1(journal)
    p = payload(run.ctx)
    core = [n for n in CORE_NAMES if n != "STANDING_INSTRUCTIONS"]  # standing_clauses empty ⇒ line omitted
    assert [n for n in p if n in CORE_NAMES] == core
    conditional = [n for n in p if n not in CORE_NAMES]
    assert conditional == ["KNOWN_FACTS", "SCOPE", "FRAMING", "TEMPLATE", "WRITE_BOUNDARY", "HUB_INTEGRITY", "HUMAN_GATE"]
    assert p["HUB_INTEGRITY"] == {"loop/program_db.jsonl": "sha256sum loop/program_db.jsonl"}
    assert p["WRITE_BOUNDARY"] == ["loop/program_db.jsonl"]  # paths, never function names
    assert p["HUMAN_GATE"] == ["do not act past the gated step without approval from human(checkpoint) (reason=stakes-2-checkpoint)"]
    assert p["DISPATCH"] == "researcher" and p["STOP"] == "verify-and-delete-dead-code"
    rc = return_contract(run.ctx)
    assert schema.required_return_fields(run.ctx) == ["REPORT_BACK", "CLAIMS", "SCOPE_DELTA", "FOLLOW_ON", "NOT_DONE",
                                                      "HUB_INTEGRITY_RESULT", "VERDICT", "NOT_ESTABLISHED"]
    assert rc["RESIDUAL_RISK"] == "N/A (role≠tester)"


def test_t3_payload_fields(journal):
    run = cases.run_t3(journal)
    p = payload(run.ctx)
    conditional = [n for n in p if n not in CORE_NAMES]
    assert conditional == ["FRAMING", "TEMPLATE", "WRITE_BOUNDARY", "HUMAN_GATE"]
    assert p["HUMAN_GATE"] == ["do not act past the gated step without approval from owner(ej) (reason=governance-gated)"]
    assert "HUB_INTEGRITY" not in p and "SCOPE" not in p
    assert p["TEMPLATE"]["headings"] == list(TEMPLATE_HEADINGS)


def test_every_generated_field_has_a_non_empty_escape_value(journal):
    for build in (cases.run_t1, cases.run_t3):
        run = build(Journal(journal.path, "x"))
        for name in payload(run.ctx):
            row = next(f for f in FIELDS if f.field == name)
            assert row.escape_value.strip(), name
    assert all(f.escape_value.strip() for f in FIELDS)
    assert all(r.escape_value.strip() for r in RETURN_CONTRACT)


def test_template_headings_in_d7_order():
    assert TEMPLATE_HEADINGS == ("## Method", "## Findings", "## Verdict", "## Not established", "## Follow-on")
    row = next(f for f in FIELDS if f.field == "TEMPLATE")
    assert " → ".join(TEMPLATE_HEADINGS) in row.type


def test_return_contract_has_twelve_rows():
    assert [r.field for r in RETURN_CONTRACT] == ["REPORT_BACK", "CLAIMS", "SCOPE_DELTA", "FOLLOW_ON", "NOT_DONE",
                                                  "VERIFY_OUTPUT", "COMMIT", "PRE_FIX_PROOF", "HUB_INTEGRITY_RESULT",
                                                  "VERDICT", "NOT_ESTABLISHED", "RESIDUAL_RISK"]
