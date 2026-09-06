"""The eight §10 trace cases, built from the spec's case text.

Each `run_*` drives C→D→B→E→A through the real stage functions against a
real journal and returns everything the tests assert on. The `[LLM]` cells
(difficulty, capability, claim kinds, framings, cut/merge decisions,
reconciliation) are the literal values the spec's case text states.

Journal construction rule (DECISIONS.md #8): a `claim_recorded` /
`check_executed` event exists in a case's journal iff §10's case text names
that author as producing or recording that claim / running that check.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from ancient_games.ctx import ArtifactRef, Ctx
from ancient_games.journal import Journal
from ancient_games.stages import (ActionInput, Candidate, CapState, Claim, CorroborateExit, FilterDecisions,
                                  FilterExit, GateExit, GuardExit, Plan, PlanEntry, ProveExit, TaskInput,
                                  corroborate, filter_candidates, gate, guard, prove)


@dataclass
class Run:
    ctx: Ctx
    journal: Journal
    gate: GateExit | None = None
    guards: dict[str, GuardExit] = field(default_factory=dict)
    corroborate: CorroborateExit | None = None
    filter: FilterExit | None = None
    prove: ProveExit | None = None
    prove_second: ProveExit | None = None
    plan: Plan | None = None
    cap: CapState = field(default_factory=CapState)

    @property
    def events(self) -> list[dict]:
        return self.journal.read()

    @property
    def agents(self) -> int:
        return sum(1 for e in self.events if e["event"] == "dispatch")

    @property
    def exit_lines(self) -> list[str]:
        return [e["exit_line"] for e in self.events if e["event"] == "exit"]


def _dispatch(journal: Journal, agent_id: str, role: str, framing: str) -> None:
    journal.dispatch(agent_id, role, framing, ["INTENT", "STOP", "FRAMING", "OUTPUT"], f"/agents/{agent_id}.md")


COMMIT_REF = ArtifactRef("master", "mutate", verb="commit")
COMMIT_TRIPWIRE = {"default-branch-history": "git diff --stat"}


# ---------------------------------------------------------------------------
def run_t2(journal: Journal) -> Run:
    """T2 — research/stability.py unimportable (REAL). Agents: 0."""
    ctx = Ctx()
    run = Run(ctx, journal)
    known = [("import fails", 'python3 -c "import research.stability"', "ImportError: cannot import name '_WF_GRID'", "2026-09-06"),
             ("symbol lives in walkforward", "grep -n _WF_GRID research/*.py", "research/walkforward.py:30", "2026-09-06"),
             ("new test red", "pytest tests/test_research_importable.py -q", "1 failed, 13 passed", "2026-09-06")]
    run.gate = gate(ctx, TaskInput("fix research.stability import", "import-succeeds-plus-smoke-test", "LOW", [],
                                   probe=ArtifactRef("research/stability.py", "read"), known_facts=known), journal)
    edit = ActionInput("research-and-tests-edit",
                       [ArtifactRef("research/stability.py", "mutate"), ArtifactRef("tests/test_research_importable.py", "mutate")],
                       consumer_reasoning="grep -rl research.stability across eval/,loop/ finds no registered stakes≥2 consumer")
    run.guards["edit"] = guard(ctx, edit, journal)
    run.guards["commit"] = guard(ctx, ActionInput("commit-to-master", [COMMIT_REF], tripwires=COMMIT_TRIPWIRE,
                                                  fallback="git revert", permissions="checkpoint-before-commit"), journal)
    # MAIN's own claims and checks, as §10 T2 lists them
    journal.claim_recorded("import-succeeds", "MAIN", "executable", "research.stability imports", "command",
                           'python3 -c "import research.stability"')
    journal.check_executed("import-succeeds", "pytest tests/test_research_importable.py -q", "14 passed", "14 passed", "FAIL")
    journal.claim_recorded("no-regression", "MAIN", "executable", "nothing else regressed", "command", "git diff --stat")
    journal.check_executed("no-regression", "make test", 274, 274)
    run.corroborate = corroborate(ctx, [Claim("import-succeeds", "executable"), Claim("no-regression", "executable")],
                                  journal, run.cap, reconciliation="agree")
    ctx.scope_items = ["research/stability.py", "tests/test_research_importable.py"]
    cands = [Candidate("import fix"), Candidate("docstring fix"), Candidate("importability test"), Candidate("Makefile change")]
    run.filter = filter_candidates(ctx, cands, FilterDecisions(
        cut={"Makefile change": "tests/ already globbed"},
        follow_on=[("extend importability pattern to eval/*.py and loop/*.py", "new-task"),
                   ("_scratch_pivot_dense_scan.py runs heavy work at import", "dismissed:out-of-scope")]), journal)
    run.plan = Plan([PlanEntry.from_stages("research-and-tests-edit", run.guards["edit"], run.corroborate),
                     PlanEntry.from_stages("commit-to-master", run.guards["commit"], run.corroborate)], gate="checkpoint")
    run.prove = prove(ctx, run.plan, journal)
    return run


# ---------------------------------------------------------------------------
def run_t1(journal: Journal) -> Run:
    """T1 — delete six dead helpers from loop/program_db.py (REAL). Agents: 1."""
    ctx = Ctx()
    run = Run(ctx, journal)
    run.gate = gate(ctx, TaskInput("delete six dead helpers", "verify-and-delete-dead-code", "MED",
                                   ["historian: dispatch-code-path read"], role="researcher",
                                   probe=ArtifactRef("loop/program_db.py", "read"),
                                   known_facts=[("six at zero refs", "AST scan + grep -rnw", "0 refs each", "2026-09-06")]), journal)
    _dispatch(journal, "historian", "researcher", "dispatch-code-path-read")
    run.cap.dispatched_so_far = 1
    run.guards["delete"] = guard(ctx, ActionInput(
        "delete-six-helpers", [ArtifactRef("loop/program_db.py", "mutate", consumers=("loop/program_db.jsonl",))],
        irreversible_clause="b", tripwires={"loop/program_db.jsonl": "sha256sum loop/program_db.jsonl"},
        fallback="N−1: re-audit and restore any helper with a live caller", permissions="checkpoint-before-commit",
        consumer_reasoning="loop/program_db.jsonl (R4) is written by program_db.py"), journal)
    journal.ingest_return("historian", {
        "REPORT_BACK": "/agents/historian.md",
        "CLAIMS": [{"claim_id": "six-are-dead", "kind": "judgment", "evidence_type": "file:line",
                    "evidence_ref": "loop/program_db.py:573,611,648", "text": "all six TRULY_DEAD"}],
        "SCOPE_DELTA": "N/A", "FOLLOW_ON": [], "NOT_DONE": [],
        "VERDICT": "VERIFIED", "NOT_ESTABLISHED": []}, framing="dispatch-code-path-read")
    journal.claim_recorded("six-are-dead", "MAIN", "judgment", "six helpers have zero live references", "command",
                           "ast scan + grep -rnw", framing="text-reference-scan")
    h = "fdfa84bc"
    for _ in range(3):
        journal.check_executed("journal-untouched", "sha256sum loop/program_db.jsonl", h, h)
    journal.claim_recorded("journal-untouched", "MAIN", "executable", "no jsonl event type tied to the six", "command",
                           "grep -o event_type loop/program_db.jsonl | sort | uniq -c")
    run.corroborate = corroborate(ctx, [Claim("six-are-dead", "judgment"), Claim("journal-untouched", "executable")],
                                  journal, run.cap, reconciliation="agree")
    ctx.scope_items = ["loop/program_db.py"]
    run.filter = filter_candidates(ctx, [Candidate("delete six + orphaned Tuple import"), Candidate("NetOutcomeResolver")],
                                   FilterDecisions(cut={"NetOutcomeResolver": "eval/ is the frozen-oracle surface → EJ"},
                                                   follow_on=[("stale worktree copies of program_db.py", "dismissed:out-of-scope unless a branch merges"),
                                                              ("DB_PATH per-worktree fork", "new-task")]), journal)
    run.plan = Plan([PlanEntry.from_stages("delete-six-helpers", run.guards["delete"], run.corroborate, dispatched_total=1)],
                    gate="checkpoint")
    run.prove = prove(ctx, run.plan, journal)
    return run


# ---------------------------------------------------------------------------
T3_AGENTS = (("spec-reader", "protocol-text-read"), ("historian", "access-log-history"), ("statistician", "power-analysis"))


def run_t3(journal: Journal) -> Run:
    """T3 — sealed-holdout recommendation. Agents: 3, governance_gated=R1."""
    ctx = Ctx()
    run = Run(ctx, journal)
    run.gate = gate(ctx, TaskInput("sealed-holdout recommendation", "recommendation-ready-3-part", "HIGH",
                                   [a for a, _ in T3_AGENTS], role="researcher", governance_gated="R1",
                                   probe=ArtifactRef("eval/protocol.json", "read")), journal)
    for aid, fr in T3_AGENTS:
        _dispatch(journal, aid, "researcher", fr)
    run.cap.dispatched_so_far = 3
    run.guards["produce"] = guard(ctx, ActionInput("produce-holdout-recommendation",
                                                    [ArtifactRef("research/holdout_recommendation.md", "mutate")],
                                                    consumer_reasoning="a new text doc; no registered consumer"), journal)
    for aid, fr in T3_AGENTS:
        journal.claim_recorded("unseal-recommendation", aid, "judgment", "should/should not unseal, on these terms",
                               "file:line", f"/agents/{aid}.md:1", framing=fr)
    run.corroborate = corroborate(ctx, [Claim("unseal-recommendation", "judgment")], journal, run.cap,
                                  reconciliation="disagree", dominance="irreversibility-finding")
    run.filter = filter_candidates(ctx, [Candidate("unseal recommendation"), Candidate("keep sealed forever, no path")],
                                   FilterDecisions(cut={"keep sealed forever, no path": "dominated"},
                                                   merged={"uncertified-log-line finding": "discovered-not-planned",
                                                           "power-analysis bound": "discovered-not-planned",
                                                           "protocol clause reading": "discovered-not-planned"},
                                                   follow_on=[("build an automated certifier", "new-task")]), journal)
    run.plan = Plan([PlanEntry.from_stages("produce-holdout-recommendation", run.guards["produce"], run.corroborate, 3)],
                    gate="checkpoint", governance_gated="R1")
    run.prove = prove(ctx, run.plan, journal)
    return run


# ---------------------------------------------------------------------------
def run_case1(journal: Journal, actor_records_claim: bool = True) -> Run:
    """Case 1 — reversible-looking action, external stakes. Agents: 3 (1 actor + 2 capped corroborators)."""
    ctx = Ctx()
    run = Run(ctx, journal)
    run.gate = gate(ctx, TaskInput("lower backoff 500ms→100ms and land it", "backoff-verified-safe", "MED",
                                   ["actor: lower the constant and check headroom"], role="coder"), journal)
    _dispatch(journal, "actor", "coder", "producer-headroom-probe")
    run.cap.dispatched_so_far = 1
    run.guards["land"] = guard(ctx, ActionInput(
        "lower-backoff-and-land", [ArtifactRef("config.py", "mutate", external_state="Binance-rate-limit-state")],
        irreversible_clause="b", tripwires={"Binance-rate-limit-state": "live headroom check pre/post"},
        fallback="revert the constant; ban persists regardless", permissions="checkpoint-then-owner",
        consumer_reasoning="external system state, declared per instance (R9)"), journal)
    if actor_records_claim:
        journal.ingest_return("actor", {
            "REPORT_BACK": "/agents/actor.md",
            "CLAIMS": [{"claim_id": "backoff-safe-at-100ms", "kind": "judgment", "evidence_type": "file:line",
                        "evidence_ref": "config.py:42", "text": "100ms will not trigger a ban"}],
            "SCOPE_DELTA": "N/A", "FOLLOW_ON": [], "NOT_DONE": []}, framing="producer-headroom-probe")
    run.corroborate = corroborate(ctx, [Claim("backoff-safe-at-100ms", "judgment")], journal, run.cap,
                                  framings={"backoff-safe-at-100ms": ["rate-limit-policy-read", "historical-ban-incidents"]},
                                  reconciliation="agree")
    run.filter = filter_candidates(ctx, [Candidate("flat 100ms"), Candidate("adaptive backoff")],
                                   FilterDecisions(cut={"flat 100ms": "dominated by adaptive-backoff"},
                                                   follow_on=[("document IP+key rate-limit", "new-task")]), journal)
    run.plan = Plan([PlanEntry.from_stages("lower-backoff-and-land", run.guards["land"], run.corroborate, run.cap.dispatched_so_far)],
                    gate="owner(ej)")
    run.prove = prove(ctx, run.plan, journal)
    return run


# ---------------------------------------------------------------------------
def run_case2(journal: Journal) -> Run:
    """Case 2 — the cheap check is the risky action. Agents: 0, hard_blocked."""
    ctx = Ctx()
    run = Run(ctx, journal)
    probe = ArtifactRef("eval.partitions.load_holdout", "invoke")
    run.gate = gate(ctx, TaskInput("confirm load_holdout runs", "owner-clearance-or-declared-blocked", "MED", [],
                                   probe=probe,
                                   probe_action=ActionInput("run-load_holdout-probe", [probe], irreversible_clause="a",
                                                            fallback="default do-not-run, flag the gap",
                                                            permissions="none-until-gated",
                                                            consumer_reasoning="the loader is the one-shot unseal act",
                                                            only_candidate_for_count0=True)), journal)
    run.guards["probe"] = run.gate.probe_guard
    return run


# ---------------------------------------------------------------------------
def run_case3(journal: Journal, second_pass: bool = False) -> Run:
    """Case 3 — two agents for capability, not corroboration. Agents: 3."""
    ctx = Ctx()
    run = Run(ctx, journal)
    run.gate = gate(ctx, TaskInput("add engine/liquidity.py + research docstrings", "liquidity-module-plus-docstrings-done",
                                   "MED", ["engine scaffolder", "docstring editor"], role="coder"), journal)
    _dispatch(journal, "engine-agent", "coder", "spec-5.3-implementation")
    _dispatch(journal, "docstring-agent", "coder", "docstring-sync")
    run.cap.dispatched_so_far = 2
    run.guards["module"] = guard(ctx, ActionInput("add-liquidity-module", [ArtifactRef("engine/liquidity.py", "mutate")],
                                                  tripwires=COMMIT_TRIPWIRE, consumer_reasoning="brand-new, not-yet-consumed module"), journal)
    run.guards["docstrings"] = guard(ctx, ActionInput("update-docstrings", [ArtifactRef("research/*.py", "mutate")],
                                                      consumer_reasoning="docstrings only; no registered consumer"), journal)
    run.guards["commit"] = guard(ctx, ActionInput("commit-to-master", [COMMIT_REF], tripwires=COMMIT_TRIPWIRE), journal)
    run.corroborate = corroborate(ctx, [Claim("liquidity-module-correctness", "executable")], journal, run.cap,
                                  framings={"liquidity-module-correctness": ["spec-5.3-formula-recheck"]},
                                  reconciliation="agree")
    run.filter = filter_candidates(ctx, [Candidate("liquidity module"), Candidate("docstrings")], FilterDecisions(), journal)
    # the corroborator returns before A runs
    aid = run.corroborate.result("liquidity-module-correctness").new_dispatches[0]
    journal.claim_recorded("liquidity-module-correctness", aid, "executable", "module matches spec §5.3", "file:line",
                           "engine/liquidity.py:1-80", framing="spec-5.3-formula-recheck")
    entries = [PlanEntry.from_stages("add-liquidity-module", run.guards["module"], run.corroborate, run.cap.dispatched_so_far),
               PlanEntry.from_stages("update-docstrings", run.guards["docstrings"], None, run.cap.dispatched_so_far),
               PlanEntry.from_stages("commit-to-master", run.guards["commit"], None, run.cap.dispatched_so_far)]
    run.plan = Plan(entries, gate="checkpoint", gate_at="commit")
    run.prove = prove(ctx, run.plan, journal)
    if second_pass:
        journal.check_executed("liquidity-module-correctness", "pytest tests/test_liquidity.py -q", "pass", "pass", "FAIL")
        run.prove_second = prove(ctx, run.plan, journal)
    return run


# ---------------------------------------------------------------------------
def run_case_i(journal: Journal) -> Run:
    """(i) — hub ≠ mutated artifact. Agents: 3."""
    ctx = Ctx()
    run = Run(ctx, journal)
    run.gate = gate(ctx, TaskInput("fix docstring typo in research/report.py", "docstring-and-synced-protocol-text-match",
                                   "MED", ["fix+verify agent", "sync-script reader"], role="coder"), journal)
    _dispatch(journal, "fixer", "coder", "fix-and-verify-sync-output")
    _dispatch(journal, "reader", "researcher", "sync-script-logic-read")
    run.cap.dispatched_so_far = 2
    run.guards["fix"] = guard(ctx, ActionInput(
        "fix-docstring", [ArtifactRef("research/report.py", "mutate", consumers=("eval/protocol.json",))],
        irreversible_clause="b", tripwires={"eval/protocol.json": "diff eval/protocol.json before/after the next sync run"},
        consumer_reasoning="tools/sync_protocol_doc.py copies the docstring into eval/protocol.json (R1)"), journal)
    journal.claim_recorded("docstring-sync-match", "fixer", "executable", "docstring and synced field agree", "file:line",
                           "eval/protocol.json:12", framing="fix-and-verify-sync-output")
    journal.claim_recorded("docstring-sync-match", "reader", "executable", "sync script copies verbatim", "file:line",
                           "tools/sync_protocol_doc.py:40", framing="sync-script-logic-read")
    run.corroborate = corroborate(ctx, [Claim("docstring-sync-match", "executable")], journal, run.cap,
                                  framings={"docstring-sync-match": ["independent-diff-recheck"]}, reconciliation="agree")
    run.filter = filter_candidates(ctx, [Candidate("fix docstring")], FilterDecisions(
        follow_on=[("automated diff-check between docstring and synced protocol text", "new-task")]), journal)
    run.plan = Plan([PlanEntry.from_stages("fix-docstring", run.guards["fix"], run.corroborate, run.cap.dispatched_so_far)],
                    gate="owner(ej)")
    run.prove = prove(ctx, run.plan, journal)
    return run


# ---------------------------------------------------------------------------
def run_case_ii(journal: Journal) -> Run:
    """(ii) — stakes-3 action where CAP forces a claim to zero. Agents: 3 (all from C, none on this claim)."""
    ctx = Ctx()
    run = Run(ctx, journal)
    run.gate = gate(ctx, TaskInput("certify the uncertified holdout_access.log line", "log-line-certified-or-declared-blocked",
                                   "HIGH", [a for a, _ in T3_AGENTS], role="researcher"), journal)
    for aid, fr in T3_AGENTS:
        _dispatch(journal, aid, "researcher", fr)
    run.cap.dispatched_so_far = 3
    run.guards["certify"] = guard(ctx, ActionInput(
        "certify-log-line", [ArtifactRef("eval/holdout_access.log", "invoke")], irreversible_clause="a",
        tripwires={"eval/holdout_access.log": "sha256sum eval/holdout_access.log"},
        consumer_reasoning="the ledger itself is the direct match (R2)"), journal)
    run.corroborate = corroborate(ctx, [Claim("log-line-properly-certified", "judgment")], journal, run.cap,
                                  framings={"log-line-properly-certified": ["access-legitimacy-review"]}, reconciliation=None)
    run.filter = filter_candidates(ctx, [Candidate("certify-log-line")], FilterDecisions(), journal)
    run.plan = Plan([PlanEntry.from_stages("certify-log-line", run.guards["certify"], run.corroborate, run.cap.dispatched_so_far)],
                    gate="owner(ej)")
    run.prove = prove(ctx, run.plan, journal)
    return run
