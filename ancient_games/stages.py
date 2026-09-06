"""§4 — the five algorithms, spine parts only.

Each function takes `ctx` plus the `[LLM]`-cell inputs as explicit
parameters (never computed here), mutates and returns `ctx`, emits its exit
line via the journal, and early-exits exactly as §4 specifies.

All source-counting for B lives in one pure function, `count_sources`, so a
later dispatch (V3.4's self-exclusion rule) replaces that function only.
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
    whether cheap means answered) arrive here as values."""

    name: str
    stop_criterion: str
    difficulty: str  # LOW | MED | HIGH (F1)
    capability: list[str] = field(default_factory=list)  # one entry per independent angle/agent needed
    role: str = "MAIN"
    probe: ArtifactRef | None = None  # C·1's cheap-means probe target
    probe_action: "ActionInput | None" = None  # D inputs, if the probe must be guarded
    resolved_by: str | None = None  # C·1 answered the task by this means
    known_facts: list[tuple[str, str, str, str]] = field(default_factory=list)
    governance_gated: str = "none"  # registry row id, only when stop_criterion IS a decision on an owner-gated row
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
    capability MAIN lacks; a LOW task with none needed is MAIN only.
    (May exceed 3 here; C·4 splits, never raises the cap.)"""
    needs = list(capability)
    if difficulty == "LOW" and not needs:
        return 0
    return len(needs)


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
    ref: str = ""
    lookup: Lookup | None = None
    steps_fired: list[str] = field(default_factory=list)

    @property
    def gate_label(self) -> str:
        return f"owner({self.owner})" if self.gate == "owner" else self.gate


def _ref_key(refs: Iterable[ArtifactRef]) -> str:
    return "+".join(r.path for r in refs if r.mode != "read")


def guard(ctx: Ctx, action: ActionInput, journal: Journal, registry: list[Row] = REGISTRY) -> GuardExit:
    fired = ["D·1", "D·2"]
    # D·1 refs
    ctx.artifact_refs = list(action.refs)
    # D·2 registry — runs on every action, no exit before it
    hit = reg.lookup(action.refs, registry)
    ctx.hub = list(hit.hubs)
    ctx.stakes = hit.stakes
    ctx.write_boundary = list(hit.hubs)
    ref_key = _ref_key(action.refs)
    journal.consumer_check(ref_key, hit.consumer_answer, action.consumer_reasoning)
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
        return GuardExit("NO_GATE", line, action.name, 1, list(hit.hubs), rev, "none", ref=ref_key, lookup=hit,
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
                     dict(ctx.tripwire), backup, action.fallback, action.permissions, ref_key, hit, fired)


# ---------------------------------------------------------------------------
# B — Corroborate(claims, stakes)
# ---------------------------------------------------------------------------

REMEDY_TEXT = {
    "add-claim-specific-check": "add a claim-specific check for {claim}",
    "add-differently-framed-source": "add a differently-framed source for {claim}",
    "gate-checkpoint": "disclose at the checkpoint gate: {claim}",
    "gate-owner": "disclose at the owner gate: {claim}",
}


@dataclass(frozen=True)
class Claim:
    claim_id: str
    kind: str  # executable | judgment (§2 X3 test — an [LLM] classification, passed in)
    has_command: bool = True  # B·4: a claim lacking a cited command is dropped (UNVERIFIED)
    n_required: int | None = None  # filled by corroborate()
    stakes: int | None = None  # the action's own stakes (D·2), filled by corroborate()


@dataclass
class CapState:
    """CAP=3 bounds category-(a) dispatched-agent fan-out cumulatively across the plan."""

    dispatched_so_far: int = 0
    cap: int = CAP

    @property
    def room(self) -> int:
        return max(0, self.cap - self.dispatched_so_far)


def _qualifying_check(ev: dict) -> bool:
    """D9′ item 5: a recorded pre-fix FAIL, or a constructed case with a stated expected value."""
    return ev.get("pre_fix_result") == "FAIL" or ev.get("expected") not in (None, "")


def count_sources(claim: Claim, events: list[dict], cap_state: CapState, framings: list[str]) -> tuple[int, str | None]:
    """§4 B·1 as written in V3_3_SPEC — the single owner of the source-counting rule.

    (a) one source per distinct non-MAIN author whose `claim_recorded` framing
        differs from every other (a) source already counted on this claim;
    (b) MAIN's own `claim_recorded` on this claim, only with
        evidence_type∈{command,file:line} and a non-empty evidence_ref, and —
        judgment claims only — a framing distinct from every (a) framing;
    (c) executable claims only: an executed check (`check_executed` with a
        pre-fix FAIL or a stated expected value); repeats of the same command
        count once (DECISIONS.md #6).
    Then new category-(a) dispatches for the shortfall, bounded by CAP room and
    by the distinct framings B·2 can assign. Remedy by kind (X1′).

    Returns (n_available, remedy); remedy is None when not capped.
    NOTE: the actor/producer self-exclusion (V3.4, Y2) is deliberately absent —
    this implements V3.3 literally.
    """
    if claim.n_required is None:
        raise ValueError("claim.n_required must be set before counting")
    recs = [e for e in events if e.get("event") == "claim_recorded" and e.get("claim_id") == claim.claim_id]
    a_framings: list[str | None] = []
    for e in recs:
        if e["author"] == "MAIN":
            continue
        if e.get("framing") in a_framings:
            continue
        a_framings.append(e.get("framing"))
    a = len(a_framings)
    b = 0
    for e in recs:
        if e["author"] != "MAIN":
            continue
        if e.get("evidence_type") not in ("command", "file:line") or not e.get("evidence_ref"):
            continue
        if claim.kind == "judgment" and e.get("framing") in a_framings:
            continue
        b = 1
        break
    c = 0
    if claim.kind == "executable":
        cmds = {e["command"] for e in events
                if e.get("event") == "check_executed" and e.get("claim_id") == claim.claim_id and _qualifying_check(e)}
        c = len(cmds)
    existing = a + b + c
    shortfall = max(0, claim.n_required - existing)
    new_framings = [f for f in framings if f not in a_framings]
    new = min(shortfall, cap_state.room, len(new_framings))
    n_available = existing + new
    if n_available >= claim.n_required:
        return n_available, None
    if claim.kind == "executable":
        return n_available, "add-claim-specific-check"
    if cap_state.dispatched_so_far + new < cap_state.cap:
        return n_available, "add-differently-framed-source"
    tier = claim.n_required
    return n_available, ("gate-owner" if tier == 3 else "gate-checkpoint")


@dataclass
class ClaimResult:
    claim: Claim
    exit_type: str  # SINGLE_SOURCE | SOURCES | CAPPED | UNVERIFIED
    n_available: int
    n_required: int
    remedy: str | None = None
    new_dispatches: list[str] = field(default_factory=list)  # agent ids dispatched by B·3
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


def corroborate(ctx: Ctx, claims: list[Claim], journal: Journal, cap_state: CapState,
                framings: dict[str, list[str]] | None = None, reconciliation: str | None = "agree",
                dominance: str | None = None, registry: list[Row] = REGISTRY,
                output_dir: str = "/corroboration") -> CorroborateExit:
    framings = framings or {}
    events = journal.read()
    fired = ["B·1"]
    results: list[ClaimResult] = []
    n_req = n_required_for(ctx, registry)
    for c in claims:
        c = replace(c, n_required=n_req, stakes=ctx.stakes or 1)
        ctx.claim_kind[c.claim_id] = c.kind
        if n_req == 1:
            ctx.n_sources[c.claim_id] = 1
            results.append(ClaimResult(c, "SINGLE_SOURCE", 1, 1))
            continue
        fr = list(framings.get(c.claim_id, []))
        n_avail, remedy = count_sources(c, events, cap_state, fr)
        n_existing, _ = count_sources(c, events, CapState(cap_state.cap, cap_state.cap), [])
        new = n_avail - n_existing
        # B·2 framings (given) + B·3 dispatch in parallel, each to its own file
        agent_ids: list[str] = []
        if new:
            fired.extend(s for s in ("B·2", "B·3") if s not in fired)
            used = {e.get("framing") for e in events
                    if e.get("event") == "claim_recorded" and e.get("claim_id") == c.claim_id and e["author"] != "MAIN"}
            for i, f in enumerate([f for f in fr if f not in used][:new], start=1):
                aid = f"{c.claim_id}-corroborator-{cap_state.dispatched_so_far + 1}"
                journal.dispatch(aid, "researcher", f, ["INTENT", "STOP", "FRAMING", "OUTPUT"], f"{output_dir}/{aid}.md")
                agent_ids.append(aid)
                cap_state.dispatched_so_far += 1
                ctx.framing = f
            ctx.siblings = [f"{output_dir}/{a}.md" for a in agent_ids]
        ctx.n_sources[c.claim_id] = n_avail
        capped = None
        if remedy is not None:
            capped = CappedClaim(c.claim_id, c.kind, n_req, n_req, n_avail, remedy)
            ctx.corroboration_capped = [x for x in ctx.corroboration_capped if x.claim_id != c.claim_id] + [capped]
            if remedy in ("gate-checkpoint", "gate-owner"):
                who = f"owner({_owner_for(ctx, registry)})" if remedy == "gate-owner" else "human(checkpoint)"
                ctx.gate_reason.append(GateReason(who, "corroboration-capped", c.claim_id))
        results.append(ClaimResult(c, "CAPPED" if capped else "SOURCES", n_avail, n_req, remedy, agent_ids, capped))
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
    # corroboration_capped entries (with remedy) carry forward on ctx for A to read — nothing to do here
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
    ref: str = ""
    stakes: int = 1
    hub: list[str] = field(default_factory=list)
    tripwires: dict[str, str] = field(default_factory=dict)
    claims: list[Claim] = field(default_factory=list)
    capped: list[CappedClaim] = field(default_factory=list)
    dispatched_total: int = 0  # the plan's category-(a) dispatched agents, structurally
    has_failable_check: bool = True  # A·2 ([LLM])
    metrics_named: bool = True  # A·3 ([LLM])

    @classmethod
    def from_stages(cls, name: str, g: GuardExit | None, b: CorroborateExit | None, dispatched_total: int = 0,
                    has_failable_check: bool = True, metrics_named: bool = True) -> "PlanEntry":
        claims = [replace(r.claim) for r in b.results] if b else []
        capped = [r.capped for r in b.results if r.capped] if b else []
        return cls(name, g.ref if g else "", g.stakes if g else 1, list(g.hub) if g else [],
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
    gate_part = plan.gate
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
