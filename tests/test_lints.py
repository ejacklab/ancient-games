"""§8 — every lint has a minimal FAIL input and a minimal PASS input
(v3_2_review.md / v3_3_review.md §D/§E)."""
from __future__ import annotations

import pytest

from ancient_games import lints
from ancient_games.ctx import CappedClaim
from ancient_games.schema import FIELDS, RETURN_CONTRACT
from ancient_games.stages import Claim, Plan, PlanEntry


def _names(findings):
    return [f.lint for f in findings]


# 1 claims-without-evidence -------------------------------------------------
def test_claims_without_evidence():
    fail = [{"claim_id": "x", "kind": "executable"}]  # no evidence at all
    assert _names(lints.lint_claims_without_evidence(fail)) == ["claims-without-evidence"]
    assert lints.lint_claims_without_evidence([{"claim_id": "x", "evidence_type": "command", "evidence_ref": ""}])
    assert lints.lint_claims_without_evidence([{"claim_id": "x", "evidence_type": "command", "evidence_ref": "pytest -q"}]) == []
    assert lints.lint_claims_without_evidence([{"claim_id": "x", "evidence_type": "(opinion)"}]) == []


# 2 follow-on-without-disposition ------------------------------------------
def test_follow_on_without_disposition():
    # T1's real "EJ decision" tag is not in the enum (v3_3_review Y5) — a genuine FAIL
    fail = [("eval/forecast.py:255 NetOutcomeResolver", "EJ decision")]
    assert _names(lints.lint_follow_on_without_disposition(fail)) == ["follow-on-without-disposition"]
    assert lints.lint_follow_on_without_disposition([("a", "fixed"), ("b", "new-task"), ("c", "dismissed:out-of-scope")]) == []
    # V3.5's fourth value: escalated:<owner>
    assert lints.lint_follow_on_without_disposition([("eval/forecast.py:255 NetOutcomeResolver", "escalated:ej")]) == []
    assert lints.lint_follow_on_without_disposition([("x", "escalated:")])  # owner required
    assert lints.lint_follow_on_without_disposition([{"finding": "d", "disposition": "dismissed:"}])  # reason required


# 3 scope-delta-missing-when-SCOPE-present ---------------------------------
def test_scope_delta_missing():
    assert _names(lints.lint_scope_delta_missing({"CLAIMS": []}, {"SCOPE": ["a.py"]})) == ["scope-delta-missing-when-SCOPE-present"]
    assert lints.lint_scope_delta_missing({"CLAIMS": [], "SCOPE_DELTA": "none"}, {"SCOPE": ["a.py"]}) == []
    assert lints.lint_scope_delta_missing({"CLAIMS": []}, {}) == []  # SCOPE never sent


# 4 schema-field-without-escape-value ---------------------------------------
def test_schema_field_without_escape_value():
    fail = [{"field": "VERIFY", "escape_value": ""}]
    assert _names(lints.lint_schema_field_without_escape_value(fail)) == ["schema-field-without-escape-value"]
    assert lints.lint_schema_field_without_escape_value([{"field": "VERIFY", "escape_value": "—"}])
    assert lints.lint_schema_field_without_escape_value(FIELDS) == []


# 5 evidence-after-verdict --------------------------------------------------
def test_evidence_after_verdict():
    fail = "## Method\n## Verdict\nVERIFIED\n## Findings\nstuff\n"
    f = lints.lint_evidence_after_verdict(fail)
    assert set(_names(f)) == {"evidence-after-verdict"} and "## Verdict appears before ## Findings" in [x.message for x in f]
    fail2 = "## Method\n## Findings\n## Verdict\n## Evidence\n## Follow-on\n"
    assert [f.subject for f in lints.lint_evidence_after_verdict(fail2)] == ["## Evidence"]
    ok = "## Method\n## Findings\n## Extra section\n## Verdict\n## Not established\n## Follow-on\n"
    assert lints.lint_evidence_after_verdict(ok) == []


# 6 corroboration-capped ----------------------------------------------------
def _case3_plan(exit_line: str = "") -> Plan:
    claim = Claim("liquidity-module-correctness", "executable", n_required=2, stakes=2, actor="module-coder")
    cap = CappedClaim("liquidity-module-correctness", "executable", 2, 2, 1, "add-claim-specific-check", "pytest-fail-first")
    return Plan([PlanEntry("add-liquidity-module", ["engine/liquidity.py"], 2, [], {}, [claim], [cap], 2)],
                gate="checkpoint", exit_line=exit_line)


def _check(claim_id, mechanism, command, expected="pass", pre_fix=None):
    return {"ts": "t", "run_id": "r", "event": "check_executed", "claim_id": claim_id, "falsifies": claim_id,
            "mechanism": mechanism, "command": command, "expected": expected, "observed": expected, "pre_fix_result": pre_fix}


_CASE3_IMPORT = _check("liquidity-module-correctness", "interpreter-import", 'python3 -c "import engine.liquidity"', "exit 0")
_CASE3_CHECK = _check("liquidity-module-correctness", "pytest-fail-first", "pytest tests/test_liquidity.py -q", "pass", "FAIL")


def test_corroboration_capped_b_fail_then_resolved():
    # FAIL (b): Case 3 first pass — only the module-coder's own import check (1 mechanism)
    f = lints.lint_corroboration_capped(_case3_plan(), [_CASE3_IMPORT])
    assert [x.message for x in f] == ["RETURN_TO_PLANNER: add a claim-specific check with mechanism pytest-fail-first for liquidity-module-correctness"]
    # PASS (b resolved): Case 3 second pass — a second, distinct-mechanism check is journal-recorded → n=2=mandated
    assert lints.lint_corroboration_capped(_case3_plan(), [_CASE3_IMPORT, _CASE3_CHECK]) == []
    # Z5′: identical command strings count once regardless of mechanism label
    relabelled = dict(_CASE3_IMPORT, mechanism="adversarial-case")
    assert lints.lint_corroboration_capped(_case3_plan(), [_CASE3_IMPORT, relabelled])


def _case1_plan(exit_line: str) -> Plan:
    claim = Claim("backoff-safe-at-100ms", "judgment", n_required=3, stakes=3, actor="coder")
    cap = CappedClaim("backoff-safe-at-100ms", "judgment", 3, 3, 2, "gate-owner")
    return Plan([PlanEntry("lower-backoff-and-land", ["config.py"], 3, ["Binance-rate-limit-state"],
                           {"Binance-rate-limit-state": "headroom"}, [claim], [cap], 3)], gate="owner(ej)", exit_line=exit_line)


def test_corroboration_capped_c_disclosed_passes_undisclosed_fails():
    disclosed = "Prove: PASS, plan cleared to owner(ej) gate [corroboration-capped: backoff-safe-at-100ms, remedy=gate-owner]."
    assert lints.lint_corroboration_capped(_case1_plan(disclosed), []) == []
    # FAIL (c, hypothetical): the same Case 1 facts with the cap silently omitted
    f = lints.lint_corroboration_capped(_case1_plan("Prove: PASS, plan cleared to owner(ej) gate."), [])
    assert _names(f) == ["corroboration-capped"] and "not disclosed" in f[0].message


def test_corroboration_capped_c_case_ii_disclosed():
    claim = Claim("log-line-properly-certified", "judgment", n_required=3, stakes=3, actor="MAIN")
    cap = CappedClaim("log-line-properly-certified", "judgment", 3, 3, 0, "gate-owner")
    line = ("Prove: PASS, plan cleared to owner(ej) gate "
            "[corroboration-capped: log-line-properly-certified, delivered=0, remedy=gate-owner].")
    plan = Plan([PlanEntry("certify-log-line", ["eval/holdout_access.log"], 3, ["eval/holdout_access.log"],
                           {"eval/holdout_access.log": "sha256sum"}, [claim], [cap], 3)], exit_line=line)
    assert lints.lint_corroboration_capped(plan, []) == []


def test_corroboration_capped_a_structural():
    plan = Plan([PlanEntry("x", ["a.py"], 2, dispatched_total=4)])
    assert _names(lints.lint_corroboration_capped(plan, [])) == ["corroboration-capped"]
    assert lints.lint_corroboration_capped(Plan([PlanEntry("x", ["a.py"], 2, dispatched_total=3)]), []) == []


def test_corroboration_capped_b_judgment_resolved_by_new_head():
    # T1: six-are-dead 1/2 → RETURN_TO_PLANNER(add source with framing ...); a second non-actor head resolves it
    claim = Claim("six-are-dead", "judgment", n_required=2, stakes=2, actor="MAIN")
    cap = CappedClaim("six-are-dead", "judgment", 2, 2, 1, "add-differently-framed-source", "independent-static-scan")
    plan = Plan([PlanEntry("delete-six-helpers", ["loop/program_db.py"], 2, [], {}, [claim], [cap], 1)])
    rec = lambda author, fr: {"ts": "t", "run_id": "r", "event": "claim_recorded", "claim_id": "six-are-dead", "author": author,
                              "actor": "MAIN", "kind": "judgment", "text": "", "evidence_type": "command", "evidence_ref": "x", "framing": fr}
    f = lints.lint_corroboration_capped(plan, [rec("MAIN", "text-reference-scan"), rec("historian", "schema-dispatch-read")])
    assert [x.message for x in f] == ["RETURN_TO_PLANNER: add source with framing independent-static-scan for six-are-dead"]
    assert lints.lint_corroboration_capped(plan, [rec("MAIN", "text-reference-scan"), rec("historian", "schema-dispatch-read"),
                                                  rec("static-scanner", "independent-static-scan")]) == []


# 7 hub-touched-without-tripwire -------------------------------------------
def test_hub_touched_without_tripwire():
    fail = Plan([PlanEntry("delete-six-helpers", ["loop/program_db.py"], 2, ["loop/program_db.jsonl"], {})])
    assert _names(lints.lint_hub_touched_without_tripwire(fail)) == ["hub-touched-without-tripwire"]
    two = Plan([PlanEntry("x", ["p"], 3, ["a", "b"], {"a": "sha256sum a"})])  # every element of the union needs one
    assert [f.message for f in lints.lint_hub_touched_without_tripwire(two)] == ["x: hub element b has no tripwire"]
    ok = Plan([PlanEntry("x", ["p"], 3, ["a", "b"], {"a": "sha256sum a", "b": "diff b"})])
    assert lints.lint_hub_touched_without_tripwire(ok) == []


def test_hub_touched_without_tripwire_event():
    """With the journal given: a named tripwire that never ran (no check_executed event
    with that command) FAILs; one that ran PASSes — and may be the (c) source of an
    executable claim at the same time (AA3′, T1's sha256)."""
    plan = Plan([PlanEntry("delete-six-helpers", ["loop/program_db.py"], 2, ["loop/program_db.jsonl"],
                           {"loop/program_db.jsonl": "sha256sum loop/program_db.jsonl"})])
    f = lints.lint_hub_touched_without_tripwire(plan, [])
    assert _names(f) == ["hub-touched-without-tripwire"] and "no check_executed event ran the tripwire" in f[0].message
    ran = _check("journal-untouched", "hash-compare", "sha256sum loop/program_db.jsonl", "fdfa84bc")
    assert lints.lint_hub_touched_without_tripwire(plan, [ran]) == []
    other = _check("journal-untouched", "hash-compare", "sha256sum somewhere/else", "fdfa84bc")
    assert lints.lint_hub_touched_without_tripwire(plan, [other])


# 8 downstream-consumer-check-unrecorded -----------------------------------
def test_downstream_consumer_check_unrecorded():
    entry = PlanEntry("research-and-tests-edit", ["research/stability.py", "tests/test_research_importable.py"], 1, [])
    # FAIL (constructed): stakes=1, hub=[] with no consumer_check anywhere in the journal
    f = lints.lint_downstream_consumer_check_unrecorded(Plan([entry]), [])
    assert _names(f) == ["downstream-consumer-check-unrecorded"]
    # PASS: T2's record (ref is a list, V3.5 §7)
    ev = {"ts": "t", "run_id": "r", "event": "consumer_check", "ref": list(entry.ref), "answer": "no",
          "command_or_reasoning": "grep -rl research.stability across eval/,loop/ finds no registered stakes≥2 consumer"}
    assert lints.lint_downstream_consumer_check_unrecorded(Plan([entry]), [ev]) == []
    # a different ref's record does not count
    other = dict(ev, ref=["research/report.py"])
    assert lints.lint_downstream_consumer_check_unrecorded(Plan([entry]), [other])
    # stakes≥2 or hub≠[] entries are out of this lint's scope
    assert lints.lint_downstream_consumer_check_unrecorded(Plan([PlanEntry("c", ["x"], 2, [])]), []) == []


# 9 return-field-without-escape-value ---------------------------------------
def test_return_field_without_escape_value():
    # FAIL, pre-X5′: V3_2_SPEC §6's VERIFY_OUTPUT row as it stood (no stated false-condition value)
    fail = [{"field": "VERIFY_OUTPUT", "escape_value": ""}]
    assert _names(lints.lint_return_field_without_escape_value(fail)) == ["return-field-without-escape-value"]
    assert lints.lint_return_field_without_escape_value(RETURN_CONTRACT) == []


def test_all_nine_present():
    assert len(lints.LINTS) == 9
    for name in lints.LINTS:
        fn = "lint_" + name.replace("-when-SCOPE-present", "").replace("-", "_")
        assert hasattr(lints, fn), fn


def test_scope_delta_missing_through_run_all_on_plan(tmp_path):
    """§8 #3 runs in `run_all_on_plan`: each `return` is read against its agent's journaled `dispatch`
    payload field names; identical in every backend (it is Python in all three)."""
    from ancient_games.journal import Journal
    fail = Journal(str(tmp_path / "fail.jsonl"), "scope")
    fail.dispatch("scoped-coder", "coder", "impl", ["INTENT", "SCOPE", "STOP"], "/agents/scoped-coder.md")
    fail.ingest_return("scoped-coder", {"CLAIMS": [], "FOLLOW_ON": []}, "MAIN")  # no SCOPE_DELTA at all
    want = lints.Finding("scope-delta-missing-when-SCOPE-present", "SCOPE_DELTA", "SCOPE sent but SCOPE_DELTA absent")
    for backend in lints.BACKENDS:
        got = lints.run_all_on_plan(Plan([]), fail.read(), backend=backend)
        assert got == [want], (backend, got)
    ok = Journal(str(tmp_path / "ok.jsonl"), "scope")
    ok.dispatch("scoped-coder", "coder", "impl", ["INTENT", "SCOPE", "STOP"], "/agents/scoped-coder.md")
    ok.ingest_return("scoped-coder", {"CLAIMS": [], "FOLLOW_ON": [], "SCOPE_DELTA": "N/A"}, "MAIN")  # explicit-empty
    ok.dispatch("unscoped", "researcher", "read", ["INTENT", "STOP", "FRAMING", "OUTPUT"], "/agents/unscoped.md")
    ok.ingest_return("unscoped", {"CLAIMS": [], "FOLLOW_ON": []}, "MAIN")  # SCOPE never sent
    ok.ingest_return("MAIN", {"CLAIMS": [], "FOLLOW_ON": []}, "MAIN")  # never dispatched
    for backend in lints.BACKENDS:
        assert lints.run_all_on_plan(Plan([]), ok.read(), backend=backend) == [], backend
    # scoped like the rest: another run's SCOPE dispatch of the same agent_id does not reach this run's return
    events = fail.read() + ok.read()
    for e in events[:2]:
        e["run_id"] = "other"
    assert lints.run_all_on_plan(Plan([]), events, backend="differential", run_id="scope") == []
    assert lints.run_all_on_plan(Plan([]), events, backend="python") == [want]  # unscoped: every event
