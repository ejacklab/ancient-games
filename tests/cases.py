"""The eight §10 trace cases (V3_5_SPEC), built from the spec's case text.

Each `run_*` drives C→D→B→E→A through the real stage functions against a
real journal and returns everything the tests assert on. The `[LLM]` cells
(difficulty, capability, actors, claim kinds, framings, remedy mechanisms,
cut/merge decisions, reconciliation) are the literal values the spec's case
text states.

Journal construction rule (DECISIONS.md #8): a `claim_recorded` /
`check_executed` event exists in a case's journal iff §10's case text lists
it; D·4's tripwire runs are recorded as `check_executed` events (AA3′) —
against the executable claim they falsify when there is one, else against
`hub-integrity:<hub>`.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from ancient_games.ctx import ArtifactRef, Ctx
from ancient_games.journal import Journal
from ancient_games.stages import (ActionInput, Candidate, Claim, CorroborateExit, FilterDecisions, FilterExit,
                                  GateExit, GuardExit, Plan, PlanEntry, ProveExit, TaskInput, corroborate,
                                  dispatch_source, filter_candidates, gate, guard, prove)


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


def _tripwire_run(journal: Journal, hub: str, command: str, mechanism: str = "hash-compare",
                  expected: str = "unchanged", observed: str = "unchanged") -> None:
    """D·4's tripwire, run by MAIN and recorded once (AA3′) against hub-integrity:<hub>."""
    journal.check_executed(f"hub-integrity:{hub}", mechanism, command, expected, observed)


# ---------------------------------------------------------------------------
def run_t2(journal: Journal) -> Run:
    """T2 — research/stability.py unimportable (REAL). Agents: 0, actor=MAIN."""
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
    # §10 T2: every event names an explicit expected value (Z2′) ⇒ all four are check_executed
    journal.check_executed("import-succeeds", "interpreter-import", 'python3 -c "import research.stability"',
                           "exits 0, no ImportError", "exit 0")
    journal.check_executed("import-succeeds", "pytest-fail-first", "pytest tests/test_research_importable.py -q",
                           "1 failed pre-fix, 14 passed post-fix", "14 passed", "FAIL")
    journal.check_executed("no-regression", "suite-count", "make test", 274, 274)
    journal.check_executed("no-regression", "git-diff-scope", "git diff --stat",  # also the commit's tripwire (AA3′)
                           "exactly research/stability.py + tests/test_research_importable.py, no other files", "2 files, matches")
    run.corroborate = corroborate(ctx, [Claim("import-succeeds", "executable"), Claim("no-regression", "executable")],
                                  journal, action="commit-to-master", reconciliation="agree")
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
    """T1 — delete six dead helpers (REAL; DIVERGES on six-are-dead). Agents: 1, actor=MAIN."""
    ctx = Ctx()
    run = Run(ctx, journal)
    run.gate = gate(ctx, TaskInput("delete six dead helpers", "verify-and-delete-dead-code", "MED",
                                   ["historian: dispatch-code-path read"], role="researcher",
                                   probe=ArtifactRef("loop/program_db.py", "read"),
                                   known_facts=[("six at zero refs", "AST scan + grep -rnw", "0 refs each", "2026-09-06")],
                                   actors={"delete-six-helpers": "MAIN"}), journal)
    _dispatch(journal, "historian", "researcher", "schema-dispatch-read")
    run.guards["delete"] = guard(ctx, ActionInput(
        "delete-six-helpers", [ArtifactRef("loop/program_db.py", "mutate", consumers=("loop/program_db.jsonl",))],
        irreversible_clause="b", tripwires={"loop/program_db.jsonl": "sha256sum loop/program_db.jsonl"},
        fallback="N−1: re-audit and restore any helper with a live caller", permissions="checkpoint-before-commit",
        consumer_reasoning="loop/program_db.jsonl (R4) is written by program_db.py"), journal)
    journal.returned("historian", {
        "REPORT_BACK": "/agents/historian.md",
        "CLAIMS": [{"claim_id": "six-are-dead", "kind": "judgment", "evidence_type": "file:line",
                    "evidence_ref": "loop/program_db.py:573,611,648", "text": "all six TRULY_DEAD"}],
        "SCOPE_DELTA": "N/A", "FOLLOW_ON": [], "NOT_DONE": [],
        "VERDICT": "VERIFIED", "NOT_ESTABLISHED": []})
    # the return's one CLAIMS entry, mirrored. `tools/ingest_return` does this from the entry; this
    # fixture writes the journal directly, so it states the mirrored event itself.
    journal.claim_recorded("six-are-dead", "historian", "MAIN", "judgment", "all six TRULY_DEAD", "file:line",
                           "loop/program_db.py:573,611,648", framing="schema-dispatch-read")
    journal.claim_recorded("six-are-dead", "MAIN", "MAIN", "judgment", "six helpers have zero live references", "command",
                           "ast scan + grep -rnw", framing="text-reference-scan")
    h = "fdfa84bc"
    for _ in range(3):  # the tripwire, run ×3 by MAIN — identical command ⇒ counts once (Z5′); dual role (AA3′)
        journal.check_executed("journal-untouched", "hash-compare", "sha256sum loop/program_db.jsonl",
                               f"{h} (pre-deletion hash)", f"{h} unchanged")
    journal.check_executed("journal-untouched", "git-diff-scope", "git status --short",
                           "only loop/program_db.py modified", "M loop/program_db.py only")
    journal.claim_recorded("journal-untouched", "MAIN", "MAIN", "executable", "no jsonl event type tied to the six",
                           "command", "grep -o event_type loop/program_db.jsonl | sort | uniq -c")  # bare citation (Z2′)
    run.corroborate = corroborate(ctx, [Claim("six-are-dead", "judgment"), Claim("journal-untouched", "executable")],
                                  journal, action="delete-six-helpers",
                                  framings={"six-are-dead": ["independent-static-scan"]}, reconciliation="agree")
    ctx.scope_items = ["loop/program_db.py"]
    run.filter = filter_candidates(ctx, [Candidate("delete six + orphaned Tuple import"), Candidate("NetOutcomeResolver")],
                                   FilterDecisions(cut={"NetOutcomeResolver": "eval/ is the frozen-oracle surface"},
                                                   follow_on=[("eval/forecast.py:255 NetOutcomeResolver, dead by both methods, in eval/", "escalated:ej"),
                                                              ("11 stale .claude/worktrees/agent-* trees hold an older program_db.py", "dismissed:out-of-scope"),
                                                              ("loop/program_db.py DB_PATH per-worktree fork", "escalated:ej")]), journal)
    run.plan = Plan([PlanEntry.from_stages("delete-six-helpers", run.guards["delete"], run.corroborate, ctx.dispatch_count)],
                    gate="checkpoint")
    run.prove = prove(ctx, run.plan, journal)
    return run


# ---------------------------------------------------------------------------
T3_AGENTS = (("spec-reader", "spec-reader"), ("historian", "historian"), ("statistician", "statistician"))


def run_t3(journal: Journal) -> Run:
    """T3 — sealed-holdout recommendation. Agents: 3, governance_gated=R1, actor=none."""
    ctx = Ctx()
    run = Run(ctx, journal)
    run.gate = gate(ctx, TaskInput("sealed-holdout recommendation", "recommendation-ready-3-part", "HIGH",
                                   [a for a, _ in T3_AGENTS], role="researcher", governance_gated="R1",
                                   probe=ArtifactRef("eval/protocol.json", "read"),
                                   actors={"produce-holdout-recommendation": "none"}), journal)
    for aid, fr in T3_AGENTS:
        _dispatch(journal, aid, "researcher", fr)
    run.guards["produce"] = guard(ctx, ActionInput("produce-holdout-recommendation",
                                                    [ArtifactRef("research/holdout_recommendation.md", "mutate")],
                                                    consumer_reasoning="a freshly-authored research doc has no existing consumer yet"), journal)
    for aid, fr in T3_AGENTS:
        journal.claim_recorded("unseal-recommendation", aid, "none", "judgment", "should/should not unseal, on these terms",
                               "file:line", f"/agents/{aid}.md:1", framing=fr)
    run.corroborate = corroborate(ctx, [Claim("unseal-recommendation", "judgment")], journal,
                                  action="produce-holdout-recommendation",
                                  reconciliation="disagree", dominance="irreversibility-finding")
    run.filter = filter_candidates(ctx, [Candidate("unseal recommendation"), Candidate("keep sealed forever, no path")],
                                   FilterDecisions(cut={"keep sealed forever, no path": "dominated"},
                                                   merged={"uncertified-log-line finding": "discovered-not-planned",
                                                           "power-analysis bound": "discovered-not-planned",
                                                           "protocol clause reading": "discovered-not-planned"},
                                                   follow_on=[("build an automated certifier", "new-task")]), journal)
    run.plan = Plan([PlanEntry.from_stages("produce-holdout-recommendation", run.guards["produce"], run.corroborate, ctx.dispatch_count)],
                    gate="checkpoint", governance_gated="R1")
    run.prove = prove(ctx, run.plan, journal)
    return run


# ---------------------------------------------------------------------------
def run_case1(journal: Journal) -> Run:
    """Case 1 — reversible-looking action, external stakes. Agents: 3 (coder + 2 corroborators), actor=coder."""
    ctx = Ctx()
    run = Run(ctx, journal)
    run.gate = gate(ctx, TaskInput("lower backoff 500ms→100ms and land it", "backoff-verified-safe", "MED",
                                   ["coder: lower the constant", "corroborator-1: headroom analysis",
                                    "corroborator-2: failure-mode review"], role="coder",
                                   actors={"lower-backoff-and-land": "coder"}), journal)
    _dispatch(journal, "coder", "coder", "proposer")
    _dispatch(journal, "corroborator-1", "researcher", "headroom-analysis")
    _dispatch(journal, "corroborator-2", "researcher", "failure-mode-review")
    run.guards["land"] = guard(ctx, ActionInput(
        "lower-backoff-and-land", [ArtifactRef("config.py", "mutate", external_state="Binance-rate-limit-state")],
        irreversible_clause="b", tripwires={"Binance-rate-limit-state": "live headroom check pre/post"},
        fallback="revert the constant; ban persists regardless", permissions="checkpoint-then-owner",
        consumer_reasoning="external system state, declared per instance (R9)"), journal)
    _tripwire_run(journal, "Binance-rate-limit-state", "live headroom check pre/post", "other:headroom-check",
                  "headroom ≥ pre-change headroom", "headroom unchanged")
    for author, fr in (("coder", "proposer"), ("corroborator-1", "headroom-analysis"), ("corroborator-2", "failure-mode-review")):
        journal.claim_recorded("backoff-safe-at-100ms", author, "coder", "judgment", "100ms will not trigger a ban",
                               "file:line", f"/agents/{author}.md:1", framing=fr)
    run.corroborate = corroborate(ctx, [Claim("backoff-safe-at-100ms", "judgment")], journal, action="lower-backoff-and-land",
                                  framings={"backoff-safe-at-100ms": ["rate-limit-policy-read"]}, reconciliation="agree")
    run.filter = filter_candidates(ctx, [Candidate("flat 100ms"), Candidate("adaptive backoff")],
                                   FilterDecisions(cut={"flat 100ms": "dominated by adaptive-backoff"},
                                                   follow_on=[("document IP+key rate-limit", "new-task")]), journal)
    run.plan = Plan([PlanEntry.from_stages("lower-backoff-and-land", run.guards["land"], run.corroborate, ctx.dispatch_count)],
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
    """Case 3 — two agents for capability, not corroboration. Agents: 2, actor=module-coder."""
    ctx = Ctx()
    run = Run(ctx, journal)
    run.gate = gate(ctx, TaskInput("add engine/liquidity.py + research docstrings", "liquidity-module-plus-docstrings-done",
                                   "MED", ["module-coder", "docstring-agent"], role="coder",
                                   actors={"add-liquidity-module": "module-coder", "update-docstrings": "docstring-agent",
                                           "commit-to-master": "MAIN"}), journal)
    _dispatch(journal, "module-coder", "coder", "spec-5.3-implementation")
    _dispatch(journal, "docstring-agent", "coder", "docstring-sync")
    run.guards["module"] = guard(ctx, ActionInput("add-liquidity-module", [ArtifactRef("engine/liquidity.py", "mutate")],
                                                  consumer_reasoning="brand-new, not-yet-consumed module"), journal)
    run.guards["docstrings"] = guard(ctx, ActionInput("update-docstrings", [ArtifactRef("research/*.py", "mutate")],
                                                      consumer_reasoning="docstring text isn't consumed/synced anywhere, unlike case (i)'s report.py"), journal)
    run.guards["commit"] = guard(ctx, ActionInput("commit-to-master", [COMMIT_REF], tripwires=COMMIT_TRIPWIRE), journal)
    _tripwire_run(journal, "default-branch-history", "git diff --stat", "git-diff-scope",
                  "engine/liquidity.py + research/*.py only", "matches")
    journal.check_executed("liquidity-module-correctness", "interpreter-import", 'python3 -c "import engine.liquidity"',
                           "exits 0, no ImportError", "exit 0")  # the module-coder's own check, immune to actor-exclusion
    run.corroborate = corroborate(ctx, [Claim("liquidity-module-correctness", "executable", remedy_mechanism="pytest-fail-first")],
                                  journal, action="add-liquidity-module", reconciliation="agree")
    run.filter = filter_candidates(ctx, [Candidate("liquidity module"), Candidate("docstrings")], FilterDecisions(), journal)
    entries = [PlanEntry.from_stages("add-liquidity-module", run.guards["module"], run.corroborate, ctx.dispatch_count),
               PlanEntry.from_stages("update-docstrings", run.guards["docstrings"], None, ctx.dispatch_count),
               PlanEntry.from_stages("commit-to-master", run.guards["commit"], None, ctx.dispatch_count)]
    run.plan = Plan(entries, gate="checkpoint", gate_at="commit")
    run.prove = prove(ctx, run.plan, journal)
    if second_pass:
        journal.check_executed("liquidity-module-correctness", "pytest-fail-first", "pytest tests/test_liquidity.py -q",
                               "fails pre-fix, passes post-fix on spec §5.3 formulas", "passed", "FAIL")
        run.prove_second = prove(ctx, run.plan, journal)
    return run


# ---------------------------------------------------------------------------
def run_case_i(journal: Journal, second_pass: bool = False) -> Run:
    """(i) — hub ≠ mutated artifact. Agents: 3, actor=fix-verify-agent."""
    ctx = Ctx()
    run = Run(ctx, journal)
    run.gate = gate(ctx, TaskInput("fix docstring typo in research/report.py", "docstring-and-synced-protocol-text-match",
                                   "MED", ["fix-verify-agent", "independent-reader", "third-corroborator"], role="coder",
                                   actors={"fix-docstring": "fix-verify-agent"}), journal)
    for aid, role, fr in (("fix-verify-agent", "coder", "fix-and-confirm"), ("independent-reader", "researcher", "sync-script-logic-read"),
                          ("third-corroborator", "researcher", "protocol-json-diff-read")):
        _dispatch(journal, aid, role, fr)
    run.guards["fix"] = guard(ctx, ActionInput(
        "fix-docstring", [ArtifactRef("research/report.py", "mutate", consumers=("eval/protocol.json",))],
        irreversible_clause="b", tripwires={"eval/protocol.json": "diff eval/protocol.json before/after the next sync run"},
        consumer_reasoning="tools/sync_protocol_doc.py copies the docstring into eval/protocol.json (R1)"), journal)
    _tripwire_run(journal, "eval/protocol.json", "diff eval/protocol.json before/after the next sync run",
                  "other:protocol-json-diff", "only the description field changes", "only description changed")
    for author, fr in (("fix-verify-agent", "fix-and-confirm"), ("independent-reader", "sync-script-logic-read"),
                       ("third-corroborator", "protocol-json-diff-read")):
        journal.claim_recorded("docstring-sync-match", author, "fix-verify-agent", "executable",
                               "docstring and synced field agree", "file:line", f"/agents/{author}.md:1", framing=fr)
    run.corroborate = corroborate(ctx, [Claim("docstring-sync-match", "executable", remedy_mechanism="other:manual-diff")],
                                  journal, action="fix-docstring", reconciliation="agree")
    run.filter = filter_candidates(ctx, [Candidate("fix docstring")], FilterDecisions(
        follow_on=[("build the general automated diff-check tool", "new-task")]), journal)
    run.plan = Plan([PlanEntry.from_stages("fix-docstring", run.guards["fix"], run.corroborate, ctx.dispatch_count)],
                    gate="owner(ej)")
    run.prove = prove(ctx, run.plan, journal)
    if second_pass:
        journal.check_executed("docstring-sync-match", "other:manual-diff",
                               "diff <(docstring-text) <(jq .description eval/protocol.json)", "no diff", "no diff")
        run.prove_second = prove(ctx, run.plan, journal)
    return run


# ---------------------------------------------------------------------------
def run_case_ii(journal: Journal) -> Run:
    """(ii) — stakes-3 action where CAP forces a claim to zero. Agents: 3 (from C, none on this claim)."""
    ctx = Ctx()
    run = Run(ctx, journal)
    run.gate = gate(ctx, TaskInput("certify the uncertified holdout_access.log line", "log-line-certified-or-declared-blocked",
                                   "HIGH", [a for a, _ in T3_AGENTS], role="researcher",
                                   actors={"certify-log-line": "MAIN"}), journal)
    for aid, fr in T3_AGENTS:
        _dispatch(journal, aid, "researcher", fr)
    tripwire = "wc -l eval/holdout_access.log && sha256sum eval/holdout_access.log"
    run.guards["certify"] = guard(ctx, ActionInput(
        "certify-log-line", [ArtifactRef("eval/holdout_access.log", "invoke")], irreversible_clause="a",
        tripwires={"eval/holdout_access.log": tripwire},
        consumer_reasoning="the ledger itself is the direct match (R2)"), journal)
    _tripwire_run(journal, "eval/holdout_access.log", tripwire, "hash-compare",
                  "line count and sha256 unchanged", "unchanged")  # Z4′: stated in §10
    run.corroborate = corroborate(ctx, [Claim("log-line-properly-certified", "judgment")], journal, action="certify-log-line",
                                  framings={"log-line-properly-certified": ["access-legitimacy-review"]}, reconciliation=None)
    run.filter = filter_candidates(ctx, [Candidate("certify-log-line")], FilterDecisions(), journal)
    run.plan = Plan([PlanEntry.from_stages("certify-log-line", run.guards["certify"], run.corroborate, ctx.dispatch_count)],
                    gate="owner(ej)")
    run.prove = prove(ctx, run.plan, journal)
    return run
