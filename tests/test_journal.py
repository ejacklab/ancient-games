"""§7 — absolute path enforcement, append/read round-trip, shape validation."""
from __future__ import annotations

import pytest

from ancient_games.journal import Journal, classify_event, read_events, validate_event


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
    j.claim_recorded("import-succeeds", "MAIN", "MAIN", "executable", "imports", "command", 'python3 -c "import x"')
    j.check_executed("import-succeeds", "pytest-fail-first", "pytest -q", "14 passed", "14 passed", "FAIL")
    j.consumer_check(["research/stability.py"], "no", "grep finds no consumer")
    j.dispatch("a1", "researcher", "f1", ["INTENT"], "/agents/a1.md")
    evs = read_events(j.path)
    assert [e["event"] for e in evs] == ["exit", "claim_recorded", "check_executed", "consumer_check", "dispatch"]
    assert all(e["run_id"] == "r1" and e["ts"] for e in evs)
    assert evs[1]["framing"] is None and evs[1]["actor"] == "MAIN"
    assert evs[2]["pre_fix_result"] == "FAIL" and evs[2]["falsifies"] == "import-succeeds" and evs[2]["mechanism"] == "pytest-fail-first"
    assert evs[3]["ref"] == ["research/stability.py"]
    assert j.read() == evs
    assert read_events(str(tmp_path / "missing.jsonl")) == []


def test_missing_typed_field_is_rejected(tmp_path):
    j = Journal(str(tmp_path / "j.jsonl"))
    with pytest.raises(ValueError, match="missing typed field 'evidence_ref'"):
        j.append({"event": "claim_recorded", "claim_id": "x", "author": "MAIN", "actor": "MAIN", "kind": "executable",
                  "text": "t", "evidence_type": "command", "framing": None})
    with pytest.raises(ValueError, match="missing typed field 'command_or_reasoning'"):
        j.append({"event": "consumer_check", "ref": ["a"], "answer": "no"})
    with pytest.raises(ValueError, match="missing typed field 'mechanism'"):
        j.append({"event": "check_executed", "claim_id": "c", "falsifies": "c", "command": "x", "expected": 1,
                  "observed": 1, "pre_fix_result": None})
    with pytest.raises(ValueError, match="missing typed field 'actor'"):
        j.append({"event": "claim_recorded", "claim_id": "x", "author": "MAIN", "kind": "executable",
                  "text": "t", "evidence_type": "command", "evidence_ref": "r", "framing": None})
    assert j.read() == []  # nothing was written


def test_wrong_type_unknown_event_and_extra_field_are_rejected():
    base = {"ts": "t", "run_id": "r"}
    with pytest.raises(ValueError, match="steps_fired must be"):
        validate_event({**base, "event": "exit", "algorithm": "C", "steps_fired": "C·1", "exit_type": "X",
                        "exit_line": "l", "ctx_keys_set": []})
    with pytest.raises(ValueError, match="unknown event type"):
        validate_event({**base, "event": "bogus"})
    with pytest.raises(ValueError, match="undeclared fields"):
        validate_event({**base, "event": "consumer_check", "ref": ["a"], "answer": "no", "command_or_reasoning": "c", "x": 1})
    with pytest.raises(ValueError, match="ref must be"):
        validate_event({**base, "event": "consumer_check", "ref": "a", "answer": "no", "command_or_reasoning": "c"})
    with pytest.raises(ValueError, match="pre_fix_result must be one of"):
        validate_event({**base, "event": "check_executed", "claim_id": "c", "falsifies": "c", "mechanism": "hash-compare",
                        "command": "x", "expected": 1, "observed": 1, "pre_fix_result": "PASS"})
    with pytest.raises(ValueError, match="mechanism must be one of"):
        validate_event({**base, "event": "check_executed", "claim_id": "c", "falsifies": "c", "mechanism": "vibes",
                        "command": "x", "expected": 1, "observed": 1, "pre_fix_result": None})
    ok = {**base, "event": "check_executed", "claim_id": "c", "falsifies": "c", "mechanism": "other:manual-diff",
          "command": "x", "expected": 1, "observed": 1, "pre_fix_result": None}
    assert validate_event(ok) is ok
    none_actor = {**base, "event": "claim_recorded", "claim_id": "x", "author": "a", "actor": "none", "kind": "judgment",
                  "text": "t", "evidence_type": "file:line", "evidence_ref": "r", "framing": "f"}
    assert validate_event(none_actor) is none_actor


def test_classify_event_z2_prime():
    """§7: check_executed iff an explicit expected value / falsifying condition is named."""
    assert classify_event({"command": "sha256sum f", "expected": "fdfa84bc", "observed": "fdfa84bc"}) == "check_executed"
    assert classify_event({"command": "pytest -q", "pre_fix_result": "FAIL", "observed": "14 passed"}) == "check_executed"
    assert classify_event({"claim_id": "x", "falsifies": "y", "command": "c"}) == "check_executed"
    # a bare citation of a command's output, even when MAIN ran it
    assert classify_event({"command": "grep -o event_type f | uniq -c", "observed": "proposed 12, guard_passed 12"}) == "claim_recorded"
    assert classify_event({"evidence_type": "command", "evidence_ref": "ast scan + grep -rnw", "expected": ""}) == "claim_recorded"


def test_returned_writes_only_the_return_event(tmp_path):
    """5c: the CLAIMS mirror used to live here, which made this module a second, unguarded writer of
    `claim_recorded` and `check_executed`. It is now `hybrid/tools/ingest_return`, which delegates to
    the tools that own those events; the mapping it inherited is pinned by
    tests/test_interface_fixes.py::test_ingest_return_mirrors_claims_through_the_guarded_writers."""
    j = Journal(str(tmp_path / "j.jsonl"))
    ev = j.returned("tester-1", {
        "REPORT_BACK": "/agents/t.md",
        "CLAIMS": [{"claim_id": "c1", "kind": "judgment", "evidence_type": "file:line", "evidence_ref": "a.py:3"}],
        "FOLLOW_ON": [], "NOT_DONE": []})
    assert ev["event"] == "return" and ev["agent_id"] == "tester-1"
    assert [e["event"] for e in j.read()] == ["return"]
    assert not hasattr(j, "ingest_return")
