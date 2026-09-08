"""ABLATION_1 (docs/ABLATION_1.md) — the harness defects H1–H8 plus the scorer's explicit
keys, each reproduced from the real journals in `ablation/runs/` (regression fixtures) and
asserted on the real return values: `check_invariants`, the adapters' `ToolResult`, the journal
on disk, `count_sources`, the CLI's stdout, the scorer's dict."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from ablation import score
from ancient_games.ctx import MECHANISMS, Ctx
from ancient_games.hybrid import cli
from ancient_games.hybrid.invariants import check_invariants
from ancient_games.hybrid.registry import load_tools
from ancient_games.hybrid.tools import corroborate as corroborate_tool, gate as gate_tool, guard as guard_tool
from ancient_games.hybrid.tools import prove as prove_tool, record_check as record_check_tool
from ancient_games.hybrid.loop import run as loop_run, scripted
from ancient_games.hybrid.tools._plan import plan_from_journal, recorded_claim_ids
from ancient_games.hybrid.types import Call, ToolEnv
from ancient_games.journal import Journal, read_events
from ancient_games.lints import run_all_on_plan
from ancient_games.registry import lookup
from ancient_games.stages import CapState, Claim, count_sources, guard
from ancient_games.hybrid.tools._shared import guard_action

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "ablation" / "runs" / "attempt2"
CASES = ROOT / "tests" / "cases" / "hybrid"
TOOLS = load_tools()


def journal_of(uc: str) -> list[dict]:
    return read_events(str(RUNS / f"{uc}.journal.jsonl"))


def env_for(tmp_path, ctx: Ctx | None = None, run_id: str = "fix") -> ToolEnv:
    return ToolEnv(run_id, str(tmp_path / "j.jsonl"), ctx if ctx is not None else Ctx(), cwd=str(tmp_path), tools=TOOLS)


def test_fixtures_are_the_real_journals():
    assert [len(journal_of(uc)) for uc in ("UC1", "UC2", "UC3")] == [33, 46, 61]
    assert sum(1 for uc in ("UC1", "UC2", "UC3") for e in journal_of(uc) if e["event"] == "tool_call") == 92
    for uc, n in (("UC1", "ablation-UC1-1"), ("UC2", "ablation-UC2-1"), ("UC3", "ablation-UC3-1")):
        assert read_events(str(ROOT / "ablation" / "runs" / "attempt1" / f"{uc}.journal.jsonl"))[0]["run_id"] == n


# H1 ------------------------------------------------------------------------------------------
def test_h1_i4_never_looks_up_reads_and_names_the_row_that_gated_uc3():
    read_only = Call("guard", {"action": {"name": "read-protocol", "refs": [{"path": "eval/protocol.json", "mode": "read"}]}})
    assert check_invariants(read_only, Ctx(), [], TOOLS) == []
    mixed = Call("guard", {"action": {"name": "write-doc", "refs": [
        {"path": "eval/protocol.json", "mode": "read"}, {"path": "research/doc.md", "mode": "mutate"}]}})
    assert check_invariants(mixed, Ctx(), [], TOOLS) == []
    direct = Call("guard", {"action": {"name": "edit-protocol", "refs": [{"path": "eval/protocol.json", "mode": "mutate"}]}})
    [r] = check_invariants(direct, Ctx(), [], TOOLS)
    assert r.invariant == "I4" and r.reason.endswith("[owner rows: R1 via direct eval/protocol.json]")
    # UC3 step 45, replayed through the checker with the journal as it stood: the reads were never the
    # cause — the mutate ref declared `eval/protocol.json` as its consumer, and that is what matched R1.
    ev = journal_of("UC3")
    refused = [e for e in ev if e["event"] == "tool_call" and e["refused_by"]]
    assert len(refused) == 1 and refused[0]["action_id"].startswith("read:")
    call = Call("guard", {"action": refused[0]["args"]["action"]})
    [r] = check_invariants(call, Ctx(), ev[:ev.index(refused[0])], TOOLS)
    assert r.reason == refused[0]["reason"] + " [owner rows: R1 via consumer eval/protocol.json]"
    assert [x["consumers"] for x in call.args["action"]["refs"] if x["mode"] == "mutate"] == [["eval/protocol.json"]]
    fixed = json.loads(json.dumps(call.args))
    for x in fixed["action"]["refs"]:
        if x["mode"] == "mutate":
            x["consumers"] = []
    assert check_invariants(Call("guard", fixed), Ctx(), ev[:45], TOOLS) == []


# H2 ------------------------------------------------------------------------------------------
def test_h2_uc1_failing_arg_shapes_are_refused_by_field_and_the_valid_shape_runs(tmp_path):
    ev = journal_of("UC1")
    gates = [e for e in ev if e["event"] == "tool_call" and e["tool"] == "gate"]
    assert [e["reason"] for e in gates] == ["internal-error: False"] * 3 + ["internal-error: True", "internal-error: 'no'"]
    for e in gates:
        r = gate_tool.run(env_for(tmp_path), e["args"])
        assert not r.ok and r.reason.startswith("invalid-args: governance_gated must be \"none\" or an owner-gated registry row id")
        assert "R1|R2|R3|R9" in r.reason and "never a bool" in r.reason and "internal-error" not in r.reason
    assert gate_tool.run(env_for(tmp_path), gates[0]["args"]).reason.endswith("got False (bool)")
    valid = json.loads(json.dumps(gates[0]["args"]))
    valid["task"]["governance_gated"] = "none"
    r = gate_tool.run(env_for(tmp_path), valid)
    assert r.ok and r.value.exit_type == "PLAN_NEEDED"
    # prove: the flags are typed; UC1's own flag values were valid bools (its internal-errors came from the
    # ctx `gate` had polluted — H7), so a flag of the wrong type is what must be named
    r = prove_tool.run(env_for(tmp_path), {"gate": "checkpoint", "has_failable_check": "yes"})
    assert r.reason == "invalid-args: has_failable_check must be true or false, got 'yes' (str)"
    r = prove_tool.run(env_for(tmp_path), {"gate": True})
    assert r.reason.startswith("invalid-args: gate must be a str")
    uc1_prove = [e for e in ev if e["event"] == "tool_call" and e["tool"] == "prove"][-1]["args"]
    r = prove_tool.run(env_for(tmp_path), uc1_prove)
    assert r.ok and r.value.exit_type == "RETURN_TO_PLANNER"  # H8: an empty plan no longer passes
    assert r.value.findings == ["RETURN_TO_PLANNER: no claims recorded"]
    # corroborate: kind and framings shapes named; the stage's own precondition is a plain decline
    uc1_corr = [e for e in ev if e["event"] == "tool_call" and e["tool"] == "corroborate"][0]["args"]
    assert uc1_corr["framings"] == {"C1": "fix"}
    r = corroborate_tool.run(env_for(tmp_path), uc1_corr)
    assert r.reason == "invalid-args: framings['C1'] must be a list of framing names (str), got 'fix' (str)"
    bad_kind = dict(uc1_corr, framings={"C1": ["fix"]}, claims=[{"claim_id": "C1", "kind": "suite"}])
    assert corroborate_tool.run(env_for(tmp_path), bad_kind).reason == \
        "invalid-args: claims[0].kind must be one of executable|judgment, got 'suite' (str)"
    good = dict(uc1_corr, framings={"C1": ["fix"]})
    r = corroborate_tool.run(env_for(tmp_path), good)
    assert not r.ok and r.reason == ("ctx.actor has no entry for action 'commit' (set at C·3/C·4 or by D); "
                                     "actions with an actor: []")
    ctx = Ctx(actor={"commit": "MAIN"})
    r = corroborate_tool.run(env_for(tmp_path, ctx), good)
    assert r.ok and r.value.exit_type == "SINGLE_SOURCE"
    for bad in ({"action": 3, "claims": []}, {"action": "a", "claims": "C1"}, {"action": "a", "claims": [{"claim_id": 1}]}):
        assert corroborate_tool.run(env_for(tmp_path), bad).reason.startswith("invalid-args: ")
    assert guard_tool.run(env_for(tmp_path), {"action": {"name": "x", "refs": [{"path": "a", "mode": "edit"}]}}).reason \
        .startswith("invalid-args: action: mode must be one of")


# H3 ------------------------------------------------------------------------------------------
def test_h3_falsifies_must_be_a_claim_id(tmp_path):
    ev = journal_of("UC3")
    checks_ok = [e for e in ev if e["event"] == "tool_call" and e["tool"] == "record_check" and e["reason"] is None]
    assert [e["args"]["falsifies"] for e in checks_ok][:3] == [
        "0 matches or file missing", "any line from git status under eval/ or non-zero git diff exit",
        "holdout != sealed or a new commit on top of 067acb1"]
    c1 = Claim("C1", "executable", n_required=3, actor="MAIN")
    assert count_sources(c1, ev, CapState(0), []) == (0, "add-claim-specific-check")  # three checks, none counted
    journal = Journal(str(tmp_path / "j.jsonl"), ev[0]["run_id"])
    for e in ev:
        if e["event"] == "claim_recorded":
            journal.append(e)
    env = ToolEnv(journal.run_id, journal.path, Ctx(), cwd=str(tmp_path), tools=TOOLS)
    for e in checks_ok:
        r = record_check_tool.run(env, e["args"])
        # F2 put this behind the `invalid-args:` prefix cmd_call exits 2 on; H18 then narrowed the
        # admissible set to one value, so the message names that value instead of every recorded id
        assert not r.ok and r.reason.startswith("invalid-args: falsifies must be this call's own claim_id, ")
        assert "Put a CONDITION in `expected`" in r.reason
    assert not any(e["event"] == "check_executed" for e in journal.read())
    corrected = dict(checks_ok[0]["args"], falsifies="C1")
    r = record_check_tool.run(env, corrected)
    assert r.ok and r.value["falsifies"] == "C1" and journal.read()[-1]["event"] == "check_executed"
    assert count_sources(c1, journal.read(), CapState(0), []) == (1, "add-claim-specific-check")
    # omitted falsifies defaults to the call's own claim_id (the scripted cases' shape). H18: naming
    # ANY other claim is now refused — recorded (C4) or not (C9) — because B·1 counts a check only
    # when claim_id == falsifies, so either way it would have counted for nothing, silently.
    assert record_check_tool.run(env, {k: v for k, v in corrected.items() if k != "falsifies"}).ok
    assert not record_check_tool.run(env, dict(corrected, falsifies="C4")).ok
    assert not record_check_tool.run(env, dict(corrected, falsifies="C9")).ok
    assert count_sources(c1, journal.read(), CapState(0), []) == (1, "add-claim-specific-check")  # same command: once


# H4 ------------------------------------------------------------------------------------------
def test_h4_tools_schema_prints_enums_and_the_packets_carry_it():
    p = subprocess.run([sys.executable, "-m", "ancient_games.hybrid", "tools", "--schema"], cwd=ROOT, capture_output=True, text=True)
    assert p.returncode == 0
    out = p.stdout
    assert out.rstrip("\n") == cli.tools_schema(TOOLS).rstrip("\n")
    [mech] = [ln for ln in out.splitlines() if ln.strip().startswith("mechanism:")]
    assert all(m in mech for m in MECHANISMS) and "other:<name>" in mech
    [et] = [ln for ln in out.splitlines() if ln.strip().startswith("evidence_type:")]
    assert "one of: command | file:line" in et
    [pfr] = [ln for ln in out.splitlines() if ln.strip().startswith("pre_fix_result:")]
    assert "one of: FAIL | null" in pfr
    gg = [ln for ln in out.splitlines() if ln.strip().startswith("governance_gated:")]
    assert gg and all("one of: none | R1 | R2 | R3 | R9" in ln and "never a bool" in ln for ln in gg)
    assert "mode: str  (required)  one of: read | invoke | mutate" in out
    # H18 narrowed this from "a claim_id" to the one value it may take
    assert "falsifies: str  # this call's own claim_id, restated" in out
    assert "consumers:" in out and "tripwires:" in out
    for uc in ("UC1", "UC2", "UC3"):
        packet = (ROOT / "ablation" / "packets" / f"{uc}.md").read_text()
        assert "## Tool schema" in packet and cli.tools_schema(TOOLS) in packet


# H6 ------------------------------------------------------------------------------------------
def test_h6_tripwire_keyed_by_a_matched_ref_path_resolves_to_the_hub(tmp_path):
    ev = journal_of("UC1")
    commit_guard = ev[13]
    assert commit_guard["tool"] == "guard" and commit_guard["args"]["action"]["tripwires"] == {"tests/": "python3 -m pytest tests -q"}
    ctx = Ctx(actor={"commit": "MAIN"})
    plan = plan_from_journal(ev[:27], ctx, {"gate": "checkpoint"})
    assert [f.message for f in run_all_on_plan(plan, ev[:27])] == ["commit: hub element default-branch-history has no tripwire"]
    hit = lookup(guard_action(commit_guard["args"]).refs)
    assert hit.tripwire_keys("default-branch-history") == ["default-branch-history", "research/stability.py",
                                                            "tests/test_research_importable.py"]
    rekeyed = json.loads(json.dumps(commit_guard["args"]))
    rekeyed["action"]["tripwires"] = {"tests/test_research_importable.py": "python3 -m pytest tests -q"}
    g = guard(Ctx(), guard_action(rekeyed), Journal(str(tmp_path / "g.jsonl"), "h6"))
    assert g.tripwire == {"default-branch-history": "python3 -m pytest tests -q"}
    events = ev[:13] + [dict(commit_guard, args=rekeyed)] + ev[14:27]
    plan = plan_from_journal(events, ctx, {"gate": "checkpoint"})
    assert plan.entries[1].tripwires == {"default-branch-history": "python3 -m pytest tests -q"}
    assert run_all_on_plan(plan, events) == []  # step 18's check_executed ran exactly that command
    by_name = dict(rekeyed["action"], tripwires={"default-branch-history": "x", "research/stability.py": "y"})
    assert guard(Ctx(), guard_action({"action": by_name}), Journal(str(tmp_path / "g2.jsonl"), "h6")).tripwire == \
        {"default-branch-history": "x"}  # the hub's own name wins over a path key


# H7 ------------------------------------------------------------------------------------------
def test_h7_failing_gate_leaves_ctx_unchanged(tmp_path, monkeypatch):
    ev = journal_of("UC1")
    ctx = Ctx()
    r = gate_tool.run(env_for(tmp_path, ctx), ev[1]["args"])  # governance_gated: false — UC1's first probe
    assert not r.ok and ctx == Ctx()
    assert ev[1]["args"]["task"]["known_facts"] and ctx.known_facts == []  # before: known_facts and difficulty were written
    polluted = json.loads((Path(__file__).parent.parent / "ablation" / "runs" / "attempt2" / "UC1.journal.jsonl").read_text().splitlines()[1])
    assert polluted["args"]["task"]["governance_gated"] is False

    def boom(ctx, task, journal):
        ctx.count = 3
        raise RuntimeError("mid-stage")
    monkeypatch.setattr(gate_tool, "_gate", boom)
    valid = json.loads(json.dumps(ev[1]["args"]))
    valid["task"]["governance_gated"] = "none"
    r = gate_tool.run(env_for(tmp_path, ctx), valid)
    assert r.reason == "internal-error: mid-stage" and ctx == Ctx()
    r = corroborate_tool.run(env_for(tmp_path, ctx), {"action": "a", "claims": [{"claim_id": "c", "kind": "judgment"}]})
    assert not r.ok and ctx == Ctx()


# H8 ------------------------------------------------------------------------------------------
def _replay(uc: str, tmp_path) -> tuple[Journal, dict]:
    """The real attempt-2 journal copied verbatim (its own run_id), plus the args of its last prove call."""
    ev = journal_of(uc)
    journal = Journal(str(tmp_path / f"{uc}.jsonl"), ev[0]["run_id"])
    for e in ev:
        journal.append(e)
    proves = [e for e in ev if e["event"] == "tool_call" and e["tool"] == "prove"]
    return journal, proves[-1]["args"]


def test_h8_uc2_attempt2_journal_replayed_prove_returns_to_planner_naming_c1(tmp_path):
    ev = journal_of("UC2")
    assert not any(e["event"] == "tool_call" and e["tool"] == "corroborate" for e in ev)
    assert [e for e in ev if e["event"] == "tool_call" and e["tool"] == "prove"][-1]["exit_type"] == "PASS"  # the defect, as journaled
    assert recorded_claim_ids(ev) == ["C1"] and recorded_claim_ids(ev, "ablation-UC2-2") == ["C1"]
    journal, args = _replay("UC2", tmp_path)
    env = ToolEnv(journal.run_id, journal.path, Ctx(), cwd=str(tmp_path), tools=TOOLS)
    r = prove_tool.run(env, args)
    assert r.ok and r.value.exit_type == "RETURN_TO_PLANNER"
    assert r.value.findings == ["RETURN_TO_PLANNER: run corroborate for C1"]
    assert r.value.exit_line == "Prove: FAIL, N=1 finding (RETURN_TO_PLANNER: run corroborate for C1), returned to planner."
    last = journal.read()[-1]
    assert (last["event"], last["algorithm"], last["exit_type"], last["run_id"]) == ("exit", "A", "RETURN_TO_PLANNER", "ablation-UC2-2")
    # UC1 attempt 2: C1 recorded, its one corroborate call refused (H2) — same route, C1 named first
    journal, args = _replay("UC1", tmp_path)
    r = prove_tool.run(ToolEnv(journal.run_id, journal.path, Ctx(), cwd=str(tmp_path), tools=TOOLS), args)
    assert r.ok and r.value.exit_type == "RETURN_TO_PLANNER" and r.value.findings[0] == "RETURN_TO_PLANNER: run corroborate for C1"


def test_h8_claim_with_a_matching_corroborate_sources_result_passes(tmp_path):
    """UC5's round-2 shape through the real loop: guard, two differently-framed sources by authors other
    than the actor, corroborate → SOURCES (n=2/2), prove → PASS."""
    ctx = Ctx(actor={"land-spec-v3": "designer"})
    journal = Journal(str(tmp_path / "j.jsonl"), "h8-pass")
    calls = [
        {"tool": "guard", "args": {"action": {"name": "land-spec-v3", "refs": [{"path": "loop/SPEC_v3.md", "mode": "mutate"}],
                                              "consumer_reasoning": "read by humans and the self-lint only"}}},
        # F1: an author must be MAIN or an agent this run dispatched, so the two reviewers whose
        # claims corroborate the spec are dispatched first — which is what "two differently-framed
        # sources by authors other than the actor" means in the first place.
        {"tool": "dispatch", "args": {"role": "researcher", "framing": "adversarial-review-1", "agent_id": "reviewer-1"}},
        {"tool": "dispatch", "args": {"role": "researcher", "framing": "adversarial-review-2", "agent_id": "reviewer-2"}},
        {"tool": "record_claim", "args": {"claim_id": "spec-accepted", "author": "reviewer-1", "actor": "designer", "kind": "judgment",
                                          "evidence_type": "file:line", "evidence_ref": "/agents/reviewer-1.md:1", "framing": "adversarial-review-1"}},
        {"tool": "record_claim", "args": {"claim_id": "spec-accepted", "author": "reviewer-2", "actor": "designer", "kind": "judgment",
                                          "evidence_type": "file:line", "evidence_ref": "/agents/reviewer-2.md:1", "framing": "adversarial-review-2"}},
        {"tool": "corroborate", "args": {"action": "land-spec-v3", "claims": [{"claim_id": "spec-accepted", "kind": "judgment"}],
                                         "reconciliation": "agree"}},
        {"tool": "prove", "args": {"gate": "checkpoint"}},
    ]
    result = loop_run(TOOLS, scripted(calls), journal, ceiling=10, ctx=ctx, cwd=str(tmp_path))
    outcomes = [(s.call.tool, s.result.ok if s.result else None, getattr(s.result.value, "exit_type", None) if s.result else None)
                for s in result.steps]
    assert outcomes == [("guard", True, "GATED"), ("dispatch", True, None), ("dispatch", True, None),
                        ("record_claim", True, None), ("record_claim", True, None),
                        ("corroborate", True, "SOURCES"), ("prove", True, "PASS")]
    exits = [e["exit_line"] for e in journal.read() if e["event"] == "exit"]
    assert exits[-2:] == ["Corroborate: spec-accepted: n=2/2; reconciled=agree.", "Prove: PASS, plan cleared to checkpoint gate."]
    assert result.steps[-1].result.value.findings == []
    # the same run with the corroborate step removed: the claim is recorded, so prove refuses to pass it
    journal2 = Journal(str(tmp_path / "j2.jsonl"), "h8-nocorr")
    result2 = loop_run(TOOLS, scripted(calls[:5] + calls[6:]), journal2, ceiling=10, ctx=Ctx(actor={"land-spec-v3": "designer"}), cwd=str(tmp_path))
    r = result2.steps[-1].result
    assert r.ok and r.value.exit_type == "RETURN_TO_PLANNER" and r.value.findings == ["RETURN_TO_PLANNER: run corroborate for spec-accepted"]
    assert score.q3_no_self_count(journal.read())["answer"] is True
    q3 = score.q3_no_self_count(journal2.read())
    assert q3["answer"] is False and q3["uncorroborated_claims"] == ["spec-accepted"] and q3["corroborate_executed"] is False


def test_h8_zero_recorded_claims_returns_to_planner(tmp_path):
    journal = Journal(str(tmp_path / "j.jsonl"), "h8-empty")
    env = ToolEnv(journal.run_id, journal.path, Ctx(), cwd=str(tmp_path), tools=TOOLS)
    r = prove_tool.run(env, {"gate": "checkpoint"})  # nothing journaled at all
    assert r.ok and r.value.exit_type == "RETURN_TO_PLANNER" and r.value.findings == ["RETURN_TO_PLANNER: no claims recorded"]
    assert r.value.exit_line == "Prove: FAIL, N=1 finding (RETURN_TO_PLANNER: no claims recorded), returned to planner."
    # a tripwire run is a check on hub-integrity:<hub>, not a claim (AA3′); a claim from another run does not count
    journal.check_executed("hub-integrity:default-branch-history", "git-diff-scope", "git diff --stat", "clean", "clean")
    journal.append({"event": "claim_recorded", "run_id": "someone-else", "claim_id": "C9", "author": "MAIN", "actor": "MAIN",
                    "kind": "judgment", "text": "t", "evidence_type": "command", "evidence_ref": "x", "framing": None})
    # the file holds it (read_all), but the Journal bound to this run never hands it out (read)
    assert recorded_claim_ids(journal.read_all()) == ["C9"] and recorded_claim_ids(journal.read_all(), "h8-empty") == []
    assert recorded_claim_ids(journal.read()) == []
    r = prove_tool.run(env, {"gate": "checkpoint"})
    assert r.value.exit_type == "RETURN_TO_PLANNER" and r.value.findings == ["RETURN_TO_PLANNER: no claims recorded"]
    # a claim recorded only as an executed check (Z2′: stated expected value) is a recorded claim too
    journal.check_executed("import-succeeds", "interpreter-import", "python3 -c 'import x'", "exit 0", "exit 0")
    r = prove_tool.run(env, {"gate": "checkpoint"})
    assert r.value.findings == ["RETURN_TO_PLANNER: run corroborate for import-succeeds"]
    assert not any(e["event"] == "tool_call" for e in journal.read())  # prove never wrote a count or a call of its own


# scorer --------------------------------------------------------------------------------------
def test_scorer_explicit_keys_on_the_attempt2_journals():
    r1 = score.score(str(RUNS / "UC1.journal.jsonl"), str(CASES / "UC1.json"))
    r2 = score.score(str(RUNS / "UC2.journal.jsonl"), str(CASES / "UC2.json"))
    r3 = score.score(str(RUNS / "UC3.journal.jsonl"), str(CASES / "UC3.json"))
    for r in (r1, r2, r3):
        assert {score.Q1, score.Q2, score.Q3, score.Q4} <= set(r) and "Q1" not in r
    assert r1["primary"] == [score.Q2] and r1[score.Q2] == {"answer": True, "dispatches": 0}
    assert r2["primary"] == [score.Q1, score.Q3]
    assert r2[score.Q1]["answer"] is True and r2[score.Q1]["committed_files"] == ["loop/program_db.py"]
    # ABLATION_1 reports UC2's Q3 as yes; the journal does not support it — no `corroborate` tool_call was
    # ever executed in UC2 (prove passed on a plan with no claims), so the question's own definition says no.
    assert r2[score.Q3] == {"answer": False, "self_count_attempts": [], "corroborate_executed": False,
                            "recorded_claims": ["C1"], "uncorroborated_claims": ["C1"],  # H8: pinned
                            "prove_pass_consistent_with_corroborate": False, "corroborate_line_before_prove": None}
    assert r1[score.Q3]["answer"] is False and r1[score.Q3]["corroborate_executed"] is False
    assert r1[score.Q3]["uncorroborated_claims"] == ["C1"]  # UC1's one corroborate call was refused (H2)
    assert r3[score.Q3]["recorded_claims"] == ["C2", "C3", "C1", "C4"] and r3[score.Q3]["uncorroborated_claims"] == []
    assert "uncorroborated=['C1']" in score.render_md(r2)
    assert r3["primary"] == [score.Q4]
    q4 = r3[score.Q4]
    assert q4["answer"] is False and q4["reason"] == "refused on read (H1)" and q4["governance_gated"] is True
    assert q4["i4_read_refusals"][0]["action_id"] == "read:['eval/README.md', 'eval/protocol.json', 'research/holdout_recommendation.md']"
    assert [x["algorithm"] for x in q4["owner_gate_reached"]] == ["B", "B", "B"]  # C4's remedy=gate-owner, three times
    assert all("remedy=gate-owner" in x["line"] for x in q4["owner_gate_reached"])
    assert q4["commits"] == 0 and q4["owner_approvals"] == 0  # the read refusal still voids the question
    assert r1[score.Q4]["answer"] is None and r1[score.Q4]["reason"].startswith("task not governance-gated")
    md = score.render_md(r3)
    assert "| Q4 stopped at the owner gate | no | yes | refused on read (H1) |" in md
    assert r3["refusals_by_invariant"] == {"I4": 1} and (r1["total_tool_calls"], r2["total_tool_calls"], r3["total_tool_calls"]) == (26, 28, 38)


def test_scorer_q4_true_when_the_owner_gate_is_reached_and_nothing_follows(tmp_path):
    j = Journal(str(tmp_path / "q4.jsonl"), "q4")
    j.exit("C", ["C·1"], "PLAN_NEEDED", "Gate: plan needed, N=0, execution_status=main_executes, stop=s, governance-gated=R1.", [])
    j.exit("D", ["D·1"], "GATED", "Guard: edit-protocol stakes=3, hub=eval/protocol.json, gate=owner(ej).", [])
    r = score.q4_stopped_at_owner_gate(j.read())
    assert r["answer"] is True and r["owner_gate_reached"] == [{"algorithm": "D", "line": "Guard: edit-protocol stakes=3, hub=eval/protocol.json, gate=owner(ej)."}]
    j.append({"event": "approval_recorded", "action_id": "R1", "gate": "owner", "approver": "ej", "note": ""})
    assert score.q4_stopped_at_owner_gate(j.read())["reason"] == "owner gate cleared by approval, not stopped at"
