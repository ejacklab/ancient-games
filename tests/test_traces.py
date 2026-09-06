"""§10 — all eight trace cases (V3_5_SPEC), each run through the real
C→D→B→E→A and asserted on exit lines, agent count, stakes, hubs,
execution_status, actor, dispatch_count, and per-claim
n_required / n_available / remedy.

T2 must additionally match the literal fields recorded in
tests/fixtures/T2_trace.md; T1 matches every field except its recorded
outcome, which V3.5 §10 declares a divergence (six-are-dead 1/2).
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

import cases
from ancient_games import trace
from ancient_games.journal import Journal
from ancient_games.stages import dispatch_source

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def journal(tmp_path):
    return Journal(str(tmp_path / "journal.jsonl"), run_id="test")


def _claim(run: cases.Run, cid: str):
    return run.corroborate.result(cid)


# ---------------------------------------------------------------------------
def test_t2(journal):
    run = cases.run_t2(journal)
    assert run.exit_lines == [
        "Gate: plan needed, N=0, execution_status=main_executes, stop=import-succeeds-plus-smoke-test.",
        "Guard: research-and-tests-edit stakes=1, no hub.",
        "Guard: commit-to-master stakes=2, hub=default-branch-history, gate=checkpoint.",
        "Corroborate: import-succeeds: n=2/2; no-regression: n=2/2; reconciled=agree.",
        "Filter: kept=3, merged=0, cut=1, follow_on=2.",
        "Prove: PASS, plan cleared to checkpoint gate.",
    ]
    assert run.agents == 0 and run.ctx.dispatch_count == 0
    assert (run.ctx.count, run.ctx.execution_status, run.ctx.difficulty) == (0, "main_executes", "LOW")
    assert run.ctx.actor == {"research-and-tests-edit": "MAIN", "commit-to-master": "MAIN"}
    assert run.ctx.governance_gated == "none"
    assert (run.guards["edit"].stakes, run.guards["edit"].hub) == (1, [])
    assert (run.guards["commit"].stakes, run.guards["commit"].hub, run.guards["commit"].gate) == (2, ["default-branch-history"], "checkpoint")
    for cid in ("import-succeeds", "no-regression"):
        r = _claim(run, cid)
        assert (r.n_required, r.n_available, r.remedy, r.claim.kind, r.claim.actor) == (2, 2, None, "executable", "MAIN")
    assert run.ctx.corroboration_capped == []
    assert run.prove.exit_type == "PASS"
    # X4: the stakes=1 ∧ hub=[] edit carries its consumer_check record (ref is a list, V3.5 §7)
    cc = [e for e in run.events if e["event"] == "consumer_check" and e["ref"] == ["research/stability.py", "tests/test_research_importable.py"]]
    assert cc and cc[0]["answer"] == "no"
    assert cc[0]["command_or_reasoning"] == "grep -rl research.stability across eval/,loop/ finds no registered stakes≥2 consumer"


def test_t2_matches_run_file(journal):
    """Every field T2_trace.md literally records (its own bare `n=1` summary line is
    the documented divergence — V3_2_SPEC §10 T2 — and is not asserted)."""
    run = cases.run_t2(journal)
    text = (FIXTURES / "T2_trace.md").read_text()
    m = re.search(r"Gate:\s+PLAN_NEEDED\(count=(\d+), difficulty=(\w+)\)", text)
    assert int(m.group(1)) == run.ctx.count == 0
    assert m.group(2) == run.ctx.difficulty == "LOW"
    assert "MAIN executes" in text and run.ctx.execution_status == "main_executes"
    assert re.search(r"research/ \+ tests/ edits → REVERSIBLE stakes 1", text) and run.guards["edit"].stakes == 1
    assert re.search(r"commit to master → stakes 2, checkpoint", text) and run.guards["commit"].stakes == 2
    assert run.guards["commit"].gate == "checkpoint"
    assert re.search(r"^(\d+) agents", text, re.M).group(1) == str(run.agents) == "0"
    assert re.search(r"Prove:\s+PASS", text) and run.prove.exit_type == "PASS"
    assert re.search(r"KEEP import fix, docstring fix, importability test", text) and len(run.filter.keep) == 3
    assert "CUT Makefile change" in text and len(run.filter.cut) == 1
    assert "274 passed" in text
    check = [e for e in run.events if e["event"] == "check_executed" and e["claim_id"] == "no-regression" and e["mechanism"] == "suite-count"][0]
    assert (check["expected"], check["observed"]) == (274, 274)


# ---------------------------------------------------------------------------
def test_t1(journal):
    run = cases.run_t1(journal)
    assert run.exit_lines == [
        "Gate: plan needed, N=1, execution_status=dispatched, stop=verify-and-delete-dead-code.",
        "Guard: delete-six-helpers stakes=2, hub=loop/program_db.jsonl, gate=checkpoint.",
        "Corroborate: six-are-dead: n=1/2, capped, remedy=add-differently-framed-source; journal-untouched: n=2/2; "
        "reconciled=agree, corroboration-capped=true.",
        "Filter: kept=1, merged=0, cut=1, follow_on=3.",
        "Prove: FAIL, N=1 finding (RETURN_TO_PLANNER: add source with framing independent-static-scan for six-are-dead), "
        "returned to planner.",
    ]
    assert run.agents == 1 and run.ctx.dispatch_count == 1
    assert (run.ctx.count, run.ctx.execution_status, run.ctx.role, run.ctx.difficulty) == (1, "dispatched", "researcher", "MED")
    assert run.ctx.actor["delete-six-helpers"] == "MAIN"
    g = run.guards["delete"]
    assert (g.stakes, g.hub, g.gate, g.reversibility) == (2, ["loop/program_db.jsonl"], "checkpoint", "irreversible")
    assert g.lookup.row_ids == ["R7", "R4"]  # D2′ union: direct R7 (hub?=no) ∪ consumer R4 (hub?=yes)
    assert run.prove.exit_type == "RETURN_TO_PLANNER"


def test_t1_per_claim(journal):
    """V3.5 §10 T1: six-are-dead 1/2 (MAIN's own scan is author=actor=MAIN ⇒ 0; the
    historian is one (a) source) ⇒ RETURN_TO_PLANNER; journal-untouched 2/2
    (hash-compare + git-diff-scope), the grep scan reclassified to claim_recorded."""
    run = cases.run_t1(journal)
    six = _claim(run, "six-are-dead")
    assert (six.n_required, six.n_available, six.remedy, six.claim.kind, six.claim.actor) == (2, 1, "add-differently-framed-source", "judgment", "MAIN")
    assert six.capped.detail == "independent-static-scan"
    ju = _claim(run, "journal-untouched")
    assert (ju.n_required, ju.n_available, ju.remedy, ju.claim.kind) == (2, 2, None, "executable")
    assert [c.claim_id for c in run.ctx.corroboration_capped] == ["six-are-dead"]
    # the sha256 tripwire ran ×3 with one command string: one (c) source, and it is also D·4's hub tripwire (AA3′)
    hashes = [e for e in run.events if e["event"] == "check_executed" and e["mechanism"] == "hash-compare"]
    assert len(hashes) == 3 and {e["command"] for e in hashes} == {run.guards["delete"].tripwire["loop/program_db.jsonl"]}


def test_t1_resume_with_second_head_passes(journal):
    """V7 resume: the remedy's dispatch increments dispatch_count; a second non-actor
    source with the unused framing brings six-are-dead to 2/2."""
    run = cases.run_t1(journal)
    dispatch_source(run.ctx, journal, "static-scanner", "independent-static-scan")
    assert run.ctx.dispatch_count == 2 and run.agents == 2
    journal.claim_recorded("six-are-dead", "static-scanner", "MAIN", "judgment", "zero refs by independent scan",
                           "command", "vulture loop/", framing="independent-static-scan")
    second = cases.prove(run.ctx, run.plan, journal)
    assert second.exit_type == "PASS" and second.exit_line == "Prove: PASS, plan cleared to checkpoint gate."


def test_t1_matches_run_file_except_declared_divergence(journal):
    run = cases.run_t1(journal)
    text = (FIXTURES / "T1_trace.md").read_text()
    m = re.search(r"PLAN_NEEDED\(count=(\d+), role=(\w+)/historian, difficulty=(\w+)\)", text)
    assert int(m.group(1)) == run.ctx.count == 1
    assert m.group(2) == run.ctx.role == "researcher"
    assert m.group(3) == run.ctx.difficulty == "MED"
    assert re.search(r"mutate loop/program_db.py → stakes 2; hub = loop/program_db.jsonl", text)
    assert (run.guards["delete"].stakes, run.guards["delete"].hub) == (2, ["loop/program_db.jsonl"])
    assert "checkpoint before commit" in text and run.guards["delete"].gate == "checkpoint"
    assert re.search(r"^(\d+) agent", text, re.M).group(1) == str(run.agents) == "1"
    assert "tripwire = sha256" in text and run.guards["delete"].tripwire == {"loop/program_db.jsonl": "sha256sum loop/program_db.jsonl"}
    assert "unchanged all three times" in text
    assert "`git status --short`" in text  # the second (c) source V3.5 §10 finds in the run's own table
    # the declared divergence: the run file records n=2 and PASS; V3.5's rule gives six-are-dead 1/2 → RETURN_TO_PLANNER
    assert re.search(r"Corroborate: n=2", text) and run.ctx.n_sources["six-are-dead"] == 1
    assert re.search(r"Prove:\s+PASS", text) and run.prove.exit_type == "RETURN_TO_PLANNER"


# ---------------------------------------------------------------------------
def test_t3(journal):
    run = cases.run_t3(journal)
    assert run.exit_lines == [
        "Gate: plan needed, N=3, execution_status=dispatched, stop=recommendation-ready-3-part, governance-gated=R1.",
        "Guard: produce-holdout-recommendation stakes=1, no hub.",
        "Corroborate: unseal-recommendation: n=3/3; reconciled=disagree, dominance=irreversibility-finding.",
        "Filter: kept=1, merged=3, cut=1, follow_on=1, governance-gated=1(terminal).",
        "Prove: PASS, plan cleared to terminal gate=owner(ej) [governance-gated].",
    ]
    assert run.agents == 3 and run.ctx.dispatch_count == 3
    assert (run.ctx.count, run.ctx.execution_status, run.ctx.governance_gated) == (3, "dispatched", "R1")
    assert run.ctx.actor["produce-holdout-recommendation"] == "none"  # Z3′: co-equal authors from the outset
    assert (run.guards["produce"].stakes, run.guards["produce"].hub) == (1, [])
    r = _claim(run, "unseal-recommendation")
    assert (r.n_required, r.n_available, r.remedy, r.claim.kind, r.claim.actor) == (3, 3, None, "judgment", "none")
    assert run.filter.governance_terminal == [("unseal recommendation", "ej")]
    assert run.prove.exit_type == "PASS"
    cc = [e for e in run.events if e["event"] == "consumer_check"]
    assert cc == [dict(cc[0], ref=["research/holdout_recommendation.md"], answer="no")]


# ---------------------------------------------------------------------------
def test_case1(journal):
    """Y2′: the coder's own claim_recorded (author=actor) counts 0; two corroborators → 2/3;
    dispatch_count=3=CAP ⇒ gate-owner, disclosed."""
    run = cases.run_case1(journal)
    assert run.exit_lines == [
        "Gate: plan needed, N=3, execution_status=dispatched, stop=backoff-verified-safe.",
        "Guard: lower-backoff-and-land stakes=3, hub=Binance-rate-limit-state, gate=owner(ej).",
        "Corroborate: backoff-safe-at-100ms: n=2/3, capped, remedy=gate-owner; reconciled=agree, corroboration-capped=true.",
        "Filter: kept=1, merged=0, cut=1, follow_on=1.",
        "Prove: PASS, plan cleared to owner(ej) gate [corroboration-capped: backoff-safe-at-100ms, remedy=gate-owner].",
    ]
    g = run.guards["land"]
    assert (g.stakes, g.hub, g.gate, g.owner, g.reversibility) == (3, ["Binance-rate-limit-state"], "owner", "ej", "irreversible")
    assert g.lookup.row_ids == ["R9"]  # same-ref specificity: R9 suppresses R7 on config.py
    assert run.agents == 3 and run.ctx.dispatch_count == 3
    r = _claim(run, "backoff-safe-at-100ms")
    assert (r.n_required, r.n_available, r.remedy, r.claim.kind, r.claim.actor) == (3, 2, "gate-owner", "judgment", "coder")
    assert run.prove.exit_type == "PASS"


# ---------------------------------------------------------------------------
def test_case2(journal):
    run = cases.run_case2(journal)
    assert run.exit_lines == [
        "Guard: run-load_holdout-probe stakes=3, hub=eval.partitions.load_holdout, gate=owner(ej).",
        "Gate: plan needed, N=0, execution_status=hard_blocked, stop=owner-clearance-or-declared-blocked.",
    ]
    assert run.agents == 0 and run.ctx.dispatch_count == 0
    assert (run.ctx.count, run.ctx.execution_status) == (0, "hard_blocked")
    g = run.guards["probe"]
    assert (g.stakes, g.hub, g.gate, g.owner, g.reversibility) == (3, ["eval.partitions.load_holdout"], "owner", "ej", "irreversible")
    assert g.lookup.row_ids == ["R3"]
    assert run.corroborate is None and run.filter is None and run.prove is None  # B/E/A never run


# ---------------------------------------------------------------------------
def test_case3_first_and_second_pass(journal):
    run = cases.run_case3(journal, second_pass=True)
    assert run.exit_lines == [
        "Gate: plan needed, N=2, execution_status=dispatched, stop=liquidity-module-plus-docstrings-done.",
        "Guard: add-liquidity-module stakes=2, hub=[], gate=checkpoint.",
        "Guard: update-docstrings stakes=1, no hub.",
        "Guard: commit-to-master stakes=2, hub=default-branch-history, gate=checkpoint.",
        "Corroborate: liquidity-module-correctness: n=1/2, capped, remedy=add-claim-specific-check; "
        "reconciled=agree, corroboration-capped=true.",
        "Filter: kept=2, merged=0, cut=0, follow_on=0.",
        "Prove: FAIL, N=1 finding (RETURN_TO_PLANNER: add a claim-specific check with mechanism pytest-fail-first "
        "for liquidity-module-correctness), returned to planner.",
        "Prove: PASS, plan cleared to checkpoint gate (at commit).",
    ]
    assert run.agents == 2 and run.ctx.dispatch_count == 2  # V3.5: no agent dispatch attempted for this claim
    assert (run.guards["module"].stakes, run.guards["module"].hub) == (2, [])  # R7 directly, hub?=no
    assert (run.guards["docstrings"].stakes, run.guards["docstrings"].hub) == (1, [])
    assert (run.guards["commit"].stakes, run.guards["commit"].hub) == (2, ["default-branch-history"])
    r = _claim(run, "liquidity-module-correctness")
    assert (r.n_required, r.n_available, r.remedy, r.claim.kind, r.claim.actor) == (2, 1, "add-claim-specific-check", "executable", "module-coder")
    assert run.ctx.corroboration_capped[0].delivered == 1 and run.ctx.corroboration_capped[0].mandated == 2
    assert run.prove.exit_type == "RETURN_TO_PLANNER"
    assert run.prove_second.exit_type == "PASS"


# ---------------------------------------------------------------------------
def test_case_i_first_and_second_pass(journal):
    """V3.5 (i): the fix+verify agent is the actor ⇒ excluded; two readers → 2/3;
    executable ⇒ add-claim-specific-check (other:manual-diff), then PASS."""
    run = cases.run_case_i(journal, second_pass=True)
    assert run.exit_lines == [
        "Gate: plan needed, N=3, execution_status=dispatched, stop=docstring-and-synced-protocol-text-match.",
        "Guard: fix-docstring stakes=3, hub=eval/protocol.json, gate=owner(ej).",
        "Corroborate: docstring-sync-match: n=2/3, capped, remedy=add-claim-specific-check; reconciled=agree, corroboration-capped=true.",
        "Filter: kept=1, merged=0, cut=0, follow_on=1.",
        "Prove: FAIL, N=1 finding (RETURN_TO_PLANNER: add a claim-specific check with mechanism other:manual-diff "
        "for docstring-sync-match), returned to planner.",
        "Prove: PASS, plan cleared to owner(ej) gate.",
    ]
    assert run.agents == 3 and run.ctx.dispatch_count == 3
    g = run.guards["fix"]
    assert (g.stakes, g.hub, g.gate, g.owner, g.reversibility) == (3, ["eval/protocol.json"], "owner", "ej", "irreversible")
    assert g.lookup.row_ids == ["R8", "R1"]  # direct R8 (stakes 1, hub?=no) ∪ consumer R1 (stakes 3, hub?=yes)
    r = _claim(run, "docstring-sync-match")
    assert (r.n_required, r.n_available, r.remedy, r.claim.kind, r.claim.actor) == (3, 2, "add-claim-specific-check", "executable", "fix-verify-agent")
    assert run.prove.exit_type == "RETURN_TO_PLANNER" and run.prove_second.exit_type == "PASS"


# ---------------------------------------------------------------------------
def test_case_ii(journal):
    run = cases.run_case_ii(journal)
    assert run.exit_lines == [
        "Gate: plan needed, N=3, execution_status=dispatched, stop=log-line-certified-or-declared-blocked.",
        "Guard: certify-log-line stakes=3, hub=eval/holdout_access.log, gate=owner(ej).",
        "Corroborate: log-line-properly-certified: n=0/3, capped, remedy=gate-owner.",
        "Filter: kept=1, merged=0, cut=0, follow_on=0.",
        "Prove: PASS, plan cleared to owner(ej) gate "
        "[corroboration-capped: log-line-properly-certified, delivered=0, remedy=gate-owner].",
    ]
    assert run.agents == 3 and run.ctx.dispatch_count == 3
    g = run.guards["certify"]
    assert (g.stakes, g.hub, g.gate, g.reversibility) == (3, ["eval/holdout_access.log"], "owner", "irreversible")
    # Z4′: the tripwire is stated and ran
    tw = "wc -l eval/holdout_access.log && sha256sum eval/holdout_access.log"
    assert g.tripwire == {"eval/holdout_access.log": tw}
    assert any(e["event"] == "check_executed" and e["command"] == tw and e["mechanism"] == "hash-compare" for e in run.events)
    r = _claim(run, "log-line-properly-certified")
    assert (r.n_required, r.n_available, r.remedy, r.claim.kind) == (3, 0, "gate-owner", "judgment")
    assert run.ctx.corroboration_capped[0].delivered == 0
    assert any(gr.reason == "corroboration-capped" and gr.claim_id == "log-line-properly-certified" for gr in run.ctx.gate_reason)
    assert run.prove.exit_type == "PASS"


# ---------------------------------------------------------------------------
# trace.py replays
# ---------------------------------------------------------------------------
def test_trace_replay_t2(journal):
    run = cases.run_t2(journal)
    md = trace.render_trace(run.events, "Run trace — T2")
    for line in run.exit_lines:
        assert line in md
    rows = {r.claim_id: r for r in trace.claim_rows(run.events)}
    assert (rows["import-succeeds"].n_available, rows["import-succeeds"].n_required) == (2, 2)
    assert (rows["no-regression"].n_available, rows["no-regression"].n_required) == (2, 2)
    assert any(s.startswith("(c) [interpreter-import] python3") for s in rows["import-succeeds"].sources)
    assert any(s.startswith("(c) [pytest-fail-first] pytest") and "pre_fix=FAIL" in s for s in rows["import-succeeds"].sources)
    assert "| `research/stability.py, tests/test_research_importable.py` | no |" in md
    assert "## Dispatches (0 agents)" in md


def test_trace_replay_case_ii_table(journal):
    run = cases.run_case_ii(journal)
    rows = trace.claim_rows(run.events)
    assert [(r.claim_id, r.n_available, r.n_required, r.remedy, r.capped) for r in rows] == [
        ("log-line-properly-certified", 0, 3, "gate-owner", True)]


def _journal_from_spec_events(journal: Journal, events: list[dict]) -> list[dict]:
    """Build a replay journal from the events §10 lists for a case — nothing else."""
    for ev in events:
        journal.append(ev)
    return journal.read()


def test_trace_replay_t3_consumer_check_from_spec_events(journal):
    """V3.5 §10 T3 lists the consumer_check event inline (Y4′), so a replay built from §10 alone finds it."""
    events = [{"event": "exit", "algorithm": "D", "steps_fired": ["D·1", "D·2", "D·3"], "exit_type": "NO_GATE",
               "exit_line": "Guard: produce-holdout-recommendation stakes=1, no hub.", "ctx_keys_set": []},
              {"event": "consumer_check", "ref": ["research/holdout_recommendation.md"], "answer": "no",
               "command_or_reasoning": "a freshly-authored research doc has no existing consumer yet"}]
    for aid, fr in cases.T3_AGENTS:
        events.append({"event": "claim_recorded", "claim_id": "unseal-recommendation", "author": aid, "actor": "none",
                       "kind": "judgment", "text": "recommendation", "evidence_type": "file:line",
                       "evidence_ref": f"/agents/{aid}.md:1", "framing": fr})
    evs = _journal_from_spec_events(journal, events)
    assert "research/holdout_recommendation.md" in trace.consumer_check_refs(evs)
    assert "| `research/holdout_recommendation.md` | no |" in trace.render_trace(evs)


def test_trace_replay_case3_docstring_consumer_check_from_spec_events(journal):
    events = [{"event": "exit", "algorithm": "D", "steps_fired": ["D·1", "D·2", "D·3"], "exit_type": "NO_GATE",
               "exit_line": "Guard: update-docstrings stakes=1, no hub.", "ctx_keys_set": []},
              {"event": "consumer_check", "ref": ["research/*.py"], "answer": "no",
               "command_or_reasoning": "docstring text isn't consumed/synced anywhere, unlike case (i)'s report.py"}]
    evs = _journal_from_spec_events(journal, events)
    assert "research/*.py" in trace.consumer_check_refs(evs)
