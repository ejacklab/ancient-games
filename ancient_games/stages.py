"""§4 — the five algorithms, spine parts only (V3_5_SPEC + V3.6 AA1′–AA3′).

Each function takes `ctx` plus the `[LLM]`-cell inputs as explicit
parameters (never computed here), mutates and returns `ctx`, emits its exit
line via the journal, and early-exits exactly as §4 specifies.

All source-counting for B lives in one pure function, `count_sources`,
released in V3.5 as the complete rule (Y2′ + Z1′–Z6′). Every branch cites
the spec sentence it implements.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, replace
from typing import Iterable

from . import registry as reg
from .ctx import CappedClaim, Ctx, ArtifactRef, GateReason
from .journal import Journal
from .registry import CAP, Lookup, Row, REGISTRY

# ---------------------------------------------------------------------------
# C — Gate(task)
# ---------------------------------------------------------------------------


@dataclass
class TaskInput:
    """C's inputs. The `[LLM]` cells (difficulty, capability, stop criterion,
    whether cheap means answered, which agent is the actor of which action)
    arrive here as values."""

    name: str
    stop_criterion: str
    difficulty: str  # LOW | MED | HIGH (F1; AA2′)
    capability: list[str] = field(default_factory=list)  # one entry per independent angle/agent needed
    role: str = "MAIN"
    probe: ArtifactRef | None = None  # C·1's cheap-means probe target
    probe_action: "ActionInput | None" = None  # D inputs, if the probe must be guarded
    resolved_by: str | None = None  # C·1 answered the task by this means
    known_facts: list[tuple[str, str, str, str]] = field(default_factory=list)
    governance_gated: str = "none"  # registry row id, only when stop_criterion IS a decision on an owner-gated row
    actors: dict[str, str] = field(default_factory=dict)  # C·3: drafted action -> agent-id | MAIN | none (Z3′)
    time_box: str = "one drafting pass"
    tools_required: list[str] = field(default_factory=list)
    standing_clauses: str = ""
    env_policy: str = ""


@dataclass
class GateExit:
    exit_type: str  # RESOLVED | PLAN_NEEDED | PLAN_NEEDED[]
    exit_line: str
    count: int = 0
    difficulty: str | None = None
    stop_criterion: str | None = None
    governance_gated: str = "none"
    execution_status: str | None = None
    evidence: str | None = None
    groups: list["GateExit"] = field(default_factory=list)
    steps_fired: list[str] = field(default_factory=list)
    probe_guard: "GuardExit | None" = None


def decision_tree(difficulty: str, capability: Iterable[str]) -> int:
    """F1: MAIN only / +1 / +2 / +3 — one agent per independent angle or
    capability MAIN lacks. (May exceed 3 here; C·4 splits, never raises the cap.)"""
    return len(list(capability))


def gate(ctx: Ctx, task: TaskInput, journal: Journal, registry: list[Row] = REGISTRY) -> GateExit:
    fired: list[str] = []
    probe_guard: GuardExit | None = None
    # C·1 cheap means; a non-read probe on a registry hub goes through D first.
    fired.append("C·1")
    ctx.known_facts = list(task.known_facts)
    if task.probe is not None:
        ctx.artifact_refs = [task.probe]
        if task.probe.mode != "read":
            hit = reg.lookup([task.probe], registry)
            if hit.hubs and task.probe_action is not None:
                probe_guard = guard(ctx, task.probe_action, journal, registry)
                # execute only if D returns stakes=1 (no gate); otherwise not run.
    if task.resolved_by is not None and probe_guard is None:
        line = f"Gate: resolved by {task.resolved_by}, no dispatch."
        journal.exit("C", fired, "RESOLVED", line, ctx.keys_set())
        return GateExit("RESOLVED", line, evidence=task.resolved_by, steps_fired=fired)
    # C·2
    fired.append("C·2")
    ctx.role = task.role
    ctx.difficulty = task.difficulty
    ctx.capability = list(task.capability)
    ctx.tools_required = list(task.tools_required)
    ctx.standing_clauses = task.standing_clauses
    ctx.env_policy = task.env_policy
    ctx.governance_gated = task.governance_gated
    if task.governance_gated != "none" and reg.row_by_id(task.governance_gated, registry).gate != "owner":
        raise ValueError("governance_gated may only name a row whose gate=owner (C·2)")
    # C·3
    fired.append("C·3")
    count = decision_tree(task.difficulty, task.capability)
    # C·4
    if count > 3:
        fired.append("C·4")
        k = math.ceil(count / 3)
        groups: list[GateExit] = []
        caps = list(task.capability)
        size = math.ceil(len(caps) / k)
        for i in range(k):
            sub = replace(task, capability=caps[i * size:(i + 1) * size], probe=None, probe_action=None)
            groups.append(gate(Ctx(), sub, journal, registry))
        line = f"Gate: split into {k} groups, each re-planned, N≤3 each."
        journal.exit("C", fired, "PLAN_NEEDED[]", line, ctx.keys_set())
        return GateExit("PLAN_NEEDED[]", line, groups=groups, steps_fired=fired)
    ctx.count = count
    if probe_guard is not None and ctx.execution_status == "hard_blocked":
        pass  # D·5's override stands (Case 2)
    else:
        ctx.execution_status = "dispatched" if count >= 1 else "main_executes"
    # C·3: "set ctx.actor for each drafted action ...; increment ctx.dispatch_count
    # once per category-(a) agent this plan dispatches"
    ctx.actor.update(task.actors)
    ctx.dispatch_count += count
    # C·5
    fired.append("C·5")
    ctx.stop_criterion = task.stop_criterion
    ctx.time_box = task.time_box
    line = (f"Gate: plan needed, N={count}, execution_status={ctx.execution_status}, stop={ctx.stop_criterion}"
            + (f", governance-gated={ctx.governance_gated}" if ctx.governance_gated != "none" else "") + ".")
    journal.exit("C", fired, "PLAN_NEEDED", line, ctx.keys_set())
    return GateExit("PLAN_NEEDED", line, count, task.difficulty, ctx.stop_criterion, ctx.governance_gated,
                    ctx.execution_status, steps_fired=fired, probe_guard=probe_guard)


# ---------------------------------------------------------------------------
# D — Guard(action)
# ---------------------------------------------------------------------------


@dataclass
class ActionInput:
    name: str
    refs: list[ArtifactRef]
    irreversible_clause: str | None = None  # 'a' | 'b' | None  ([LLM] part of D·3)
    backup_exists: bool = False
    tripwires: dict[str, str] = field(default_factory=dict)  # hub element -> command ([LLM] part of D·4)
    fallback: str = "retry, then revert"
    permissions: str = "explicit tool grants scaled to terrain"
    consumer_reasoning: str = "no registered stakes≥2 consumer declared"
    approval_on_record: bool = False
    only_candidate_for_count0: bool = False


@dataclass
class GuardExit:
    exit_type: str  # NO_GATE | GATED
    exit_line: str
    action: str
    stakes: int
    hub: list[str]
    reversibility: str
    gate: str  # none | checkpoint | owner
    owner: str | None = None
    tripwire: dict[str, str] = field(default_factory=dict)
    backup: str = "none"
    fallback: str | None = None
    permissions: str | None = None
    refs: list[str] = field(default_factory=list)
    lookup: Lookup | None = None
    steps_fired: list[str] = field(default_factory=list)

    @property
    def gate_label(self) -> str:
        return f"owner({self.owner})" if self.gate == "owner" else self.gate


def _ref_paths(refs: Iterable[ArtifactRef]) -> list[str]:
    return [r.path for r in refs if r.mode != "read"]


def guard(ctx: Ctx, action: ActionInput, journal: Journal, registry: list[Row] = REGISTRY) -> GuardExit:
    fired = ["D·1", "D·2"]
    # D·1 refs
    ctx.artifact_refs = list(action.refs)
    # §2 actor: "or D at execution_status=main_executes"
    if ctx.execution_status == "main_executes":
        ctx.actor.setdefault(action.name, "MAIN")
    # D·2 registry — runs on every action, no exit before it
    hit = reg.lookup(action.refs, registry)
    ctx.hub = list(hit.hubs)
    ctx.stakes = hit.stakes
    ctx.write_boundary = list(hit.hubs)
    paths = _ref_paths(action.refs)
    journal.consumer_check(paths, hit.consumer_answer, action.consumer_reasoning)
    # D·3 reversibility — shape of the fallback only, never whether the action gates
    fired.append("D·3")
    if action.irreversible_clause in ("a", "b"):
        rev = "irreversible"
    elif action.backup_exists:
        rev = "restorable"
    else:
        rev = "git-revertible"
    ctx.reversibility = rev
    if hit.stakes == 1:
        line = f"Guard: {action.name} stakes=1, no hub."
        journal.exit("D", fired, "NO_GATE", line, ctx.keys_set())
        return GuardExit("NO_GATE", line, action.name, 1, list(hit.hubs), rev, "none", refs=paths, lookup=hit,
                         steps_fired=fired)
    # D·4 fallback/tripwire — one tripwire per hub element
    fired.append("D·4")
    ctx.tripwire = {h: action.tripwires[h] for h in hit.hubs if h in action.tripwires}
    backup = "exists" if action.backup_exists else "none"
    # D·5 gate
    fired.append("D·5")
    if hit.gate == "owner":
        who = f"owner({hit.owner})"
        reason = "stakes-3-owner"
    else:
        who = "human(checkpoint)"
        reason = "stakes-2-checkpoint"
    ctx.gate_reason = [g for g in ctx.gate_reason if g.reason not in ("stakes-2-checkpoint", "stakes-3-owner")]
    ctx.gate_reason.append(GateReason(who, reason))
    if hit.gate == "owner" and not action.approval_on_record and action.only_candidate_for_count0:
        ctx.execution_status = "hard_blocked"
    label = who if hit.gate == "owner" else "checkpoint"
    line = f"Guard: {action.name} stakes={hit.stakes}, hub={','.join(hit.hubs) if hit.hubs else '[]'}, gate={label}."
    journal.exit("D", fired, "GATED", line, ctx.keys_set())
    return GuardExit("GATED", line, action.name, hit.stakes, list(hit.hubs), rev, hit.gate, hit.owner,
                     dict(ctx.tripwire), backup, action.fallback, action.permissions, paths, hit, fired)


# ---------------------------------------------------------------------------
# B — Corroborate(claims, stakes)
# ---------------------------------------------------------------------------


def remedy_text(remedy: str, claim_id: str, detail: str | None = None) -> str:
    """The RETURN_TO_PLANNER / disclosure text a remedy carries (V3.5 §10's forms)."""
    if remedy == "add-claim-specific-check":
        return (f"add a claim-specific check with mechanism {detail} for {claim_id}" if detail
                else f"add a claim-specific check for {claim_id}")
    if remedy == "add-differently-framed-source":
        return (f"add source with framing {detail} for {claim_id}" if detail
                else f"add a differently-framed source for {claim_id}")
    if remedy == "gate-checkpoint":
        return f"disclose at the checkpoint gate: {claim_id}"
    return f"disclose at the owner gate: {claim_id}"


@dataclass(frozen=True)
class Claim:
    claim_id: str
    kind: str  # executable | judgment (§2 X3 test — an [LLM] classification, passed in)
    action: str | None = None  # the action this claim is about; actor(X) = ctx.actor[action]
    has_command: bool = True  # B·4: a claim lacking a cited command is dropped (UNVERIFIED)
    remedy_mechanism: str | None = None  # [LLM]: the mechanism an add-claim-specific-check remedy names
    n_required: int | None = None  # filled by corroborate()
    stakes: int | None = None  # the action's own stakes (D·2), filled by corroborate()
    actor: str | None = None  # agent-id | MAIN | none, filled by corroborate() from ctx.actor


@dataclass
class CapState:
    """cap_state = (ctx.dispatch_count, CAP=3) — §2 Z1′; a slot remains iff dispatch_count < 3."""

    dispatch_count: int = 0
    cap: int = CAP

    @property
    def slot_remains(self) -> bool:
        return self.dispatch_count < self.cap


def _a_events(claim: Claim, events: list[dict]) -> list[dict]:
    recorded = [e for e in events if e.get("event") == "claim_recorded" and e.get("claim_id") == claim.claim_id]
    # B·1 (a): "each claim_recorded event on X whose author ≠ actor(X) — vacuously
    # true for every author when actor(X)=none (Z3′)"
    if claim.actor == "none":
        return list(recorded)
    return [e for e in recorded if e["author"] != claim.actor]


def unused_framing(claim: Claim, events: list[dict], framings: list[str]) -> str | None:
    """B·2's framing enumeration for this task, minus every framing already used
    on X by a counted (a) source — the first unused entry, or None."""
    used = {e.get("framing") for e in _a_events(claim, events)}
    for f in framings:
        if f not in used:
            return f
    return None


def count_sources(claim: Claim, events: list[dict], cap_state: CapState, framings: list[str]) -> tuple[int, str | None]:
    """V3_5_SPEC §4 B·1 — the complete source-counting rule, as a pure function.

    Reads already-classified events: classification (§7, Z2′) happens at
    journal-write time (`journal.classify_event`, called by `ingest_return`),
    never here — the reviewer's AA4 reading.
    Returns (n_available, remedy); remedy is None when not capped.
    """
    if claim.n_required is None or claim.actor is None:
        raise ValueError("claim.n_required and claim.actor must be set before counting")
    X = claim.claim_id
    # B·1: "if n_required(X)=1: exit trivially, SINGLE_SOURCE"
    if claim.n_required == 1:
        return 1, None
    recorded = [e for e in events if e.get("event") == "claim_recorded" and e.get("claim_id") == X]
    # B·1: "check_executed{claim_id=X, falsifies=X}"
    executed = [e for e in events if e.get("event") == "check_executed" and e.get("claim_id") == X
                and e.get("falsifies") == X]

    # (a) "each claim_recorded event on X whose author ≠ actor(X) ... counted once
    #     per distinct framing among these"
    a_events = _a_events(claim, events)
    n_a = len({e.get("framing") for e in a_events})

    # (b) "MAIN's own claim_recorded event on X, counted only when actor(X) ≠ MAIN and
    #     it carries evidence_type ∈ {command, file:line} with a non-empty evidence_ref
    #     — at most once per claim" (Z6′)
    #     v1.1 (D-B, one author one source): an author contributes at most ONE source per claim
    #     across (a)/(b) — MAIN's event already counted under (a) is not counted again here.
    n_b = 0
    if claim.actor != "MAIN" and not any(e["author"] == "MAIN" for e in a_events):
        main_events = [e for e in recorded if e["author"] == "MAIN"
                       and e.get("evidence_type") in ("command", "file:line") and e.get("evidence_ref")]
        if main_events:
            n_b = 1

    # (c) "only when kind(X) = executable, each check_executed{claim_id=X, falsifies=X}
    #     event, counted once per distinct mechanism ... regardless of who ran it — but
    #     two check_executed events on X whose command strings are identical count once
    #     regardless of their mechanism labels" (Z5′ item 2). Identical-command dedup
    #     runs first, then distinct-mechanism (the reviewer's AA5 ordering).
    #     AA3′: a D·4 tripwire recorded as check_executed{falsifies=X} is counted here
    #     like any other — one event, two roles.
    n_c = 0
    if claim.kind == "executable":
        seen_commands: set[str] = set()
        deduped: list[dict] = []
        for e in executed:
            if e["command"] in seen_commands:
                continue
            seen_commands.add(e["command"])
            deduped.append(e)
        n_c = len({e["mechanism"] for e in deduped})
    # "a judgment claim's originating evidence can never pass that test ... the
    # self-exclusion": a judgment claim gets nothing from (c), and its actor's own
    # claim_recorded already failed (a) and (b) above.

    n_available = n_a + n_b + n_c
    if n_available >= claim.n_required:
        return n_available, None
    # "kind=executable ⇒ remedy=add-claim-specific-check"
    if claim.kind == "executable":
        return n_available, "add-claim-specific-check"
    # "kind=judgment ⇒ remedy=add-differently-framed-source only if cap_state's
    #  dispatch_count < 3 (a slot remains) and B·2's framing enumeration for this
    #  task names a framing not yet used on X"
    if cap_state.slot_remains and unused_framing(claim, events, framings) is not None:
        return n_available, "add-differently-framed-source"
    # "otherwise remedy=gate-checkpoint (stakes≤2) or remedy=gate-owner (stakes=3)"
    return n_available, ("gate-owner" if claim.n_required == 3 else "gate-checkpoint")


@dataclass
class ClaimResult:
    claim: Claim
    exit_type: str  # SINGLE_SOURCE | SOURCES | CAPPED | UNVERIFIED
    n_available: int
    n_required: int
    remedy: str | None = None
    capped: CappedClaim | None = None

    @property
    def line_part(self) -> str:
        if self.exit_type == "SINGLE_SOURCE":
            return f"{self.claim.claim_id}: n=1 (single source)"
        s = f"{self.claim.claim_id}: n={self.n_available}/{self.n_required}"
        if self.capped:
            s += f", capped, remedy={self.remedy}"
        return s


@dataclass
class CorroborateExit:
    exit_type: str  # SINGLE_SOURCE | SOURCES | CAPPED | UNVERIFIED (rolled up)
    exit_line: str
    results: list[ClaimResult]
    reconciliation: str | None
    dominance: str | None
    steps_fired: list[str] = field(default_factory=list)

    def result(self, claim_id: str) -> ClaimResult:
        for r in self.results:
            if r.claim.claim_id == claim_id:
                return r
        raise KeyError(claim_id)


def n_required_for(ctx: Ctx, registry: list[Row] = REGISTRY) -> int:
    """max(the action's own stakes from D·2, the registry stakes tier of governance_gated's row if set)."""
    stakes = ctx.stakes or 1
    if ctx.governance_gated != "none":
        stakes = max(stakes, reg.row_by_id(ctx.governance_gated, registry).stakes)
    return stakes


def corroborate(ctx: Ctx, claims: list[Claim], journal: Journal, action: str,
                framings: dict[str, list[str]] | None = None, reconciliation: str | None = "agree",
                dominance: str | None = None, registry: list[Row] = REGISTRY) -> CorroborateExit:
    """B. `action` names the action the claims are about; actor(X) = ctx.actor[action]."""
    framings = framings or {}
    events = journal.read()
    fired = ["B·1"]
    results: list[ClaimResult] = []
    n_req = n_required_for(ctx, registry)
    if action not in ctx.actor:
        raise ValueError(f"ctx.actor has no entry for action {action!r} (set at C·3/C·4 or by D)")
    cap_state = CapState(ctx.dispatch_count)
    for c in claims:
        c = replace(c, n_required=n_req, stakes=ctx.stakes or 1, actor=ctx.actor[action], action=c.action or action)
        ctx.claim_kind[c.claim_id] = c.kind
        if n_req == 1:
            ctx.n_sources[c.claim_id] = 1
            results.append(ClaimResult(c, "SINGLE_SOURCE", 1, 1))
            continue
        fr = list(framings.get(c.claim_id, []))
        if fr and "B·2" not in fired:
            fired.append("B·2")
        n_avail, remedy = count_sources(c, events, cap_state, fr)
        ctx.n_sources[c.claim_id] = n_avail
        capped = None
        if remedy is not None:
            detail = None
            if remedy == "add-differently-framed-source":
                detail = unused_framing(c, events, fr)
            elif remedy == "add-claim-specific-check":
                detail = c.remedy_mechanism
            capped = CappedClaim(c.claim_id, c.kind, n_req, n_req, n_avail, remedy, detail)
            ctx.corroboration_capped = [x for x in ctx.corroboration_capped if x.claim_id != c.claim_id] + [capped]
            if remedy in ("gate-checkpoint", "gate-owner"):
                who = f"owner({_owner_for(ctx, registry)})" if remedy == "gate-owner" else "human(checkpoint)"
                ctx.gate_reason.append(GateReason(who, "corroboration-capped", c.claim_id))
        results.append(ClaimResult(c, "CAPPED" if capped else "SOURCES", n_avail, n_req, remedy, capped))
    # B·4 drop UNVERIFIED
    fired.append("B·4")
    for r in results:
        if not r.claim.has_command:
            r.exit_type = "UNVERIFIED"
    survivors = [r for r in results if r.exit_type != "UNVERIFIED"]
    # B·5 reconcile (LLM input)
    if survivors and reconciliation is not None:
        fired.append("B·5")
    parts = [r.line_part for r in survivors]
    line = "Corroborate: " + "; ".join(parts)
    if survivors and reconciliation is not None and not all(r.exit_type == "SINGLE_SOURCE" for r in survivors):
        line += f"; reconciled={reconciliation}"
        if dominance:
            line += f", dominance={dominance}"
        if any(r.capped for r in survivors):
            line += ", corroboration-capped=true"
    line += "."
    if all(r.exit_type == "SINGLE_SOURCE" for r in survivors) and survivors:
        exit_type = "SINGLE_SOURCE"
    elif any(r.capped for r in survivors):
        exit_type = "CAPPED"
    elif survivors:
        exit_type = "SOURCES"
    else:
        exit_type = "UNVERIFIED"
    journal.exit("B", fired, exit_type, line, ctx.keys_set())
    return CorroborateExit(exit_type, line, results, reconciliation, dominance, fired)


def dispatch_source(ctx: Ctx, journal: Journal, agent_id: str, framing: str, role: str = "researcher",
                    output_dir: str = "/corroboration") -> dict:
    """B·3 for a RETURN_TO_PLANNER-triggered category-(a) dispatch: its own file,
    and `ctx.dispatch_count` incremented (B·1's last sentence)."""
    ev = journal.dispatch(agent_id, role, framing, ["INTENT", "STOP", "FRAMING", "OUTPUT"], f"{output_dir}/{agent_id}.md")
    ctx.dispatch_count += 1
    ctx.framing = framing
    ctx.siblings = ctx.siblings + [f"{output_dir}/{agent_id}.md"]
    return ev


def _owner_for(ctx: Ctx, registry: list[Row]) -> str:
    for g in ctx.gate_reason:
        if g.who.startswith("owner("):
            return g.who[6:-1]
    if ctx.governance_gated != "none":
        return reg.row_by_id(ctx.governance_gated, registry).owner or "ej"
    return "ej"


# ---------------------------------------------------------------------------
# E — Filter(candidates)
# ---------------------------------------------------------------------------


@dataclass
class Candidate:
    name: str
    scores: dict[str, float] | None = None  # cost, value, risk, confidence (cost/permissions from D, confidence from B)
    guard: GuardExit | None = None
    corroboration: CorroborateExit | None = None
    governance_gated: str = "none"
    payload_size: int = 0
    size_limit: int = 0  # 0 = unbounded
    labels: dict[str, str] = field(default_factory=dict)  # generic label -> domain name (E·7)


@dataclass
class FilterDecisions:
    """E's [LLM] cells: what to cut/merge/follow on, with the deciding rule per entry."""

    cut: dict[str, str] = field(default_factory=dict)  # candidate -> rule
    merged: dict[str, str] = field(default_factory=dict)  # candidate -> rule (e.g. discovered-not-planned)
    follow_on: list[tuple[str, str]] = field(default_factory=list)  # (finding, disposition)
    intents: dict[str, str] = field(default_factory=dict)  # candidate -> restated intent


@dataclass
class FilterExit:
    exit_type: str
    exit_line: str
    keep: list[tuple[str, str]]
    merged: list[tuple[str, str]]
    cut: list[tuple[str, str]]
    follow_on: list[tuple[str, str]]
    governance_terminal: list[tuple[str, str]] = field(default_factory=list)  # (candidate, owner)
    trims: list[tuple[str, int, int]] = field(default_factory=list)
    steps_fired: list[str] = field(default_factory=list)


def _dominated(x: dict[str, float], y: dict[str, float]) -> bool:
    """x dominated by y on every axis: y cheaper, more valuable, less risky, more confident."""
    return (y["cost"] < x["cost"] and y["value"] > x["value"] and y["risk"] < x["risk"]
            and y["confidence"] > x["confidence"])


def filter_candidates(ctx: Ctx, candidates: list[Candidate], decisions: FilterDecisions, journal: Journal,
                      registry: list[Row] = REGISTRY) -> FilterExit:
    if not candidates:
        line = "Filter: no candidates, nothing to filter."
        journal.exit("E", [], "EMPTY", line, ctx.keys_set())
        return FilterExit("EMPTY", line, [], [], [], [])
    fired = ["E·1"]
    cut: list[tuple[str, str]] = []
    scored = [c for c in candidates if c.scores]
    for c in scored:
        if any(o is not c and _dominated(c.scores, o.scores) for o in scored):  # type: ignore[arg-type]
            cut.append((c.name, "pareto-dominated"))
    dropped = {n for n, _ in cut}
    # E·2–E·4 are [LLM]: cut/merge/follow_on/intents arrive as decisions
    fired.extend(["E·2", "E·3", "E·4"])
    for name, rule in decisions.cut.items():
        if name not in dropped:
            cut.append((name, rule))
            dropped.add(name)
    merged = [(n, r) for n, r in decisions.merged.items() if n not in dropped]
    keep = [(c.name, decisions.intents.get(c.name, "kept")) for c in candidates
            if c.name not in dropped and c.name not in decisions.merged]
    follow_on = list(decisions.follow_on)
    # E·5 doctrine/topology/precedence + terminal governance gate
    fired.append("E·5")
    terminal: list[tuple[str, str]] = []
    surviving = [c for c in candidates if c.name not in dropped]
    for c in surviving:
        gg = c.governance_gated if c.governance_gated != "none" else ctx.governance_gated
        if gg != "none":
            owner = reg.row_by_id(gg, registry).owner or "ej"
            terminal.append((c.name, owner))
            if not any(g.reason == "governance-gated" for g in ctx.gate_reason):
                ctx.gate_reason.append(GateReason(f"owner({owner})", "governance-gated"))
    # E·6 size bound
    fired.append("E·6")
    trims = [(c.name, c.payload_size, c.size_limit) for c in surviving if c.size_limit and c.payload_size > c.size_limit]
    # E·7 domain naming
    fired.append("E·7")
    line = f"Filter: kept={len(keep)}, merged={len(merged)}, cut={len(cut)}, follow_on={len(follow_on)}"
    if terminal:
        line += f", governance-gated={len(terminal)}(terminal)"
    line += "."
    journal.exit("E", fired, "TAGGED", line, ctx.keys_set())
    return FilterExit("TAGGED", line, keep, merged, cut, follow_on, terminal, trims, fired)


# ---------------------------------------------------------------------------
# A — Prove(plan)
# ---------------------------------------------------------------------------


@dataclass
class PlanEntry:
    """One KEEP/MERGED entry with its D/B annotations attached."""

    name: str
    ref: list[str] = field(default_factory=list)  # the action's invoke/mutate paths (consumer_check.ref)
    stakes: int = 1
    hub: list[str] = field(default_factory=list)
    tripwires: dict[str, str] = field(default_factory=dict)
    claims: list[Claim] = field(default_factory=list)
    capped: list[CappedClaim] = field(default_factory=list)
    dispatched_total: int = 0  # ctx.dispatch_count at plan time (the plan's category-(a) agents, structurally)
    has_failable_check: bool = True  # A·2 ([LLM])
    metrics_named: bool = True  # A·3 ([LLM])

    @classmethod
    def from_stages(cls, name: str, g: GuardExit | None, b: CorroborateExit | None, dispatched_total: int = 0,
                    has_failable_check: bool = True, metrics_named: bool = True) -> "PlanEntry":
        claims = [replace(r.claim) for r in b.results] if b else []
        capped = [r.capped for r in b.results if r.capped] if b else []
        return cls(name, list(g.refs) if g else [], g.stakes if g else 1, list(g.hub) if g else [],
                   dict(g.tripwire) if g else {}, claims, capped, dispatched_total, has_failable_check, metrics_named)


@dataclass
class Plan:
    entries: list[PlanEntry]
    gate: str = "checkpoint"  # checkpoint | owner(<name>)
    governance_gated: str = "none"
    gate_at: str | None = None  # e.g. "commit" -> "(at commit)"
    exit_line: str = ""  # A composes it; the corroboration-capped lint reads it for disclosure


@dataclass
class ProveExit:
    exit_type: str  # PASS | RETURN_TO_PLANNER
    exit_line: str
    findings: list[str]
    steps_fired: list[str] = field(default_factory=list)


def disclosure(capped: Iterable[CappedClaim]) -> str:
    parts = []
    for c in capped:
        if c.remedy in ("gate-checkpoint", "gate-owner"):
            parts.append(f"corroboration-capped: {c.claim_id}" + (", delivered=0" if c.delivered == 0 else "")
                         + f", remedy={c.remedy}")
    return "; ".join(parts)


def prove(ctx: Ctx, plan: Plan, journal: Journal, registry: list[Row] = REGISTRY, disclose: bool = True) -> ProveExit:
    from . import lints  # lazy: lints imports count_sources from this module

    fired = ["A·1", "A·2", "A·3"]
    findings: list[str] = []
    for e in plan.entries:
        for c in e.claims:
            if not c.has_command:
                findings.append(f"claim {c.claim_id} shows no command")
        if not e.has_failable_check:
            findings.append(f"action {e.name} has no check that can fail")
        if not e.metrics_named:
            findings.append(f"action {e.name} names a metric without its true quantity")
    # compose the exit line (with disclosure) before the lints, which read it
    all_capped = [c for e in plan.entries for c in e.capped]
    if plan.governance_gated != "none":
        owner = reg.row_by_id(plan.governance_gated, registry).owner or "ej"
        gate_part = f"terminal gate=owner({owner}) [governance-gated]"
    else:
        gate_part = f"{plan.gate} gate" + (f" (at {plan.gate_at})" if plan.gate_at else "")
    disc = disclosure(all_capped) if disclose else ""
    pass_line = f"Prove: PASS, plan cleared to {gate_part}" + (f" [{disc}]" if disc else "") + "."
    plan.exit_line = pass_line
    events = journal.read()
    lint_findings = lints.run_all_on_plan(plan, events)
    findings.extend(f.message for f in lint_findings)
    if findings:
        n = len(findings)
        line = f"Prove: FAIL, N={n} finding{'s' if n != 1 else ''} ({'; '.join(findings)}), returned to planner."
        plan.exit_line = line
        journal.exit("A", fired, "RETURN_TO_PLANNER", line, ctx.keys_set())
        return ProveExit("RETURN_TO_PLANNER", line, findings, fired)
    journal.exit("A", fired, "PASS", pass_line, ctx.keys_set())
    return ProveExit("PASS", pass_line, [], fired)
