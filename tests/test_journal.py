"""§7 — absolute path enforcement, append/read round-trip, shape validation."""
from __future__ import annotations

import pytest

from ancient_games.journal import Journal, read_events, validate_event


def test_relative_path_raises():
    with pytest.raises(ValueError, match="absolute"):
        Journal("journal.jsonl")
    with pytest.raises(ValueError, match="absolute"):
        Journal("./out/journal.jsonl")
    with pytest.raises(ValueError, match="absolute"):
        read_events("journal.jsonl")


def test_append_read_round_trip(tmp_path):
    j = Journal(str(tmp_path / "j.jsonl"), run_id="r1")
    j.exit("C", ["C·1", "C·2"], "PLAN_NEEDED", "Gate: plan needed, N=0, execution_status=main_executes, stop=x.", ["count"])
    j.claim_recorded("import-succeeds", "MAIN", "executable", "imports", "command", 'python3 -c "import x"')
    j.check_executed("import-succeeds", "pytest -q", "14 passed", "14 passed", "FAIL")
    j.consumer_check("research/stability.py", "no", "grep finds no consumer")
    j.dispatch("a1", "researcher", "f1", ["INTENT"], "/agents/a1.md")
    evs = read_events(j.path)
    assert [e["event"] for e in evs] == ["exit", "claim_recorded", "check_executed", "consumer_check", "dispatch"]
    assert all(e["run_id"] == "r1" and e["ts"] for e in evs)
    assert evs[1]["framing"] is None and evs[2]["pre_fix_result"] == "FAIL"
    assert j.read() == evs
    assert read_events(str(tmp_path / "missing.jsonl")) == []


def test_missing_typed_field_is_rejected(tmp_path):
    j = Journal(str(tmp_path / "j.jsonl"))
    with pytest.raises(ValueError, match="missing typed field 'evidence_ref'"):
        j.append({"event": "claim_recorded", "claim_id": "x", "author": "MAIN", "kind": "executable",
                  "text": "t", "evidence_type": "command", "framing": None})
    with pytest.raises(ValueError, match="missing typed field 'command_or_reasoning'"):
        j.append({"event": "consumer_check", "ref": "a", "answer": "no"})
    assert j.read() == []  # nothing was written


def test_wrong_type_unknown_event_and_extra_field_are_rejected():
    base = {"ts": "t", "run_id": "r"}
    with pytest.raises(ValueError, match="steps_fired must be"):
        validate_event({**base, "event": "exit", "algorithm": "C", "steps_fired": "C·1", "exit_type": "X",
                        "exit_line": "l", "ctx_keys_set": []})
    with pytest.raises(ValueError, match="unknown event type"):
        validate_event({**base, "event": "bogus"})
    with pytest.raises(ValueError, match="undeclared fields"):
        validate_event({**base, "event": "consumer_check", "ref": "a", "answer": "no", "command_or_reasoning": "c", "x": 1})
    with pytest.raises(ValueError, match="pre_fix_result must be one of"):
        validate_event({**base, "event": "check_executed", "claim_id": "c", "command": "x", "expected": 1,
                        "observed": 1, "pre_fix_result": "PASS"})


def test_ingest_return_mirrors_claims(tmp_path):
    j = Journal(str(tmp_path / "j.jsonl"))
    j.ingest_return("tester-1", {
        "REPORT_BACK": "/agents/t.md",
        "CLAIMS": [{"claim_id": "c1", "kind": "judgment", "evidence_type": "file:line", "evidence_ref": "a.py:3"},
                   {"claim_id": "c1-check", "kind": "executable", "falsifies": "c1", "command": "pytest -q",
                    "expected": "pass", "observed": "pass", "pre_fix_result": "FAIL"},
                   {"claim_id": "c2", "kind": "judgment", "evidence_type": "(opinion)"}],
        "FOLLOW_ON": [], "NOT_DONE": []}, framing="adversarial")
    evs = j.read()
    assert [e["event"] for e in evs] == ["return", "claim_recorded", "check_executed"]
    assert evs[1]["author"] == "tester-1" and evs[1]["framing"] == "adversarial"
    assert evs[2]["claim_id"] == "c1" and evs[2]["pre_fix_result"] == "FAIL"
