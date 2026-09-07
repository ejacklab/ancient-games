"""Plan reconstruction from the journal, shared by `prove` and `run_lint`.

`prove`/`done` receive the stripped ctx (I3′), so the plan A checks is
rebuilt from journaled facts only: each non-refused `guard` tool_call is
one entry (refs, stakes/hub via the registry, tripwires from its own
args); the latest Corroborate exit line per action supplies the claims'
n_required / capped status — counts come from `corroborate`'s journaled
result, never from the agent or from ctx.

H8 (ABLATION_1): the claims A must see are the run's *recorded* claims, not
the ones `corroborate` happened to be called on. `recorded_claim_ids` lists
them; every one without an executed `corroborate` call naming it is a
RETURN_TO_PLANNER finding on the plan, and a run with none recorded is one
too — so `prove` cannot PASS an empty plan.
"""
from __future__ import annotations

from ancient_games import registry as reg
from ancient_games.ctx import CappedClaim
from ancient_games.registry import REGISTRY, Row
from ancient_games.stages import Claim, Plan, PlanEntry, tripwires_for, unused_framing
from ancient_games.trace import parse_corroborate_line

from ._shared import guard_action, guard_mutate_paths


HUB_INTEGRITY_PREFIX = "hub-integrity:"  # D·4 tripwire runs (AA3′) are recorded as checks, not claims


def _this_run(events: list[dict], run_id: str | None) -> list[dict]:
    return events if run_id is None else [e for e in events if e.get("run_id") == run_id]


def recorded_claim_ids(events: list[dict], run_id: str | None = None) -> list[str]:
    """The claims this run recorded, deduped by claim_id in first-seen order: every `claim_recorded`
    and every `check_executed` claim_id (a claim with a stated expected value is journaled as a
    check — `journal.classify_event`, Z2′ — so it is a recorded claim too). `hub-integrity:*` is a
    tripwire run, never a claim."""
    out: list[str] = []
    for e in _this_run(events, run_id):
        if e.get("event") in ("claim_recorded", "check_executed"):
            cid = e.get("claim_id")
            if isinstance(cid, str) and not cid.startswith(HUB_INTEGRITY_PREFIX) and cid not in out:
                out.append(cid)
    return out


def _executed_corroborates(events: list[dict]) -> list[dict]:
    return [e for e in events if e.get("event") == "tool_call" and e["tool"] == "corroborate"
            and e["refused_by"] is None and e["reason"] is None]


def corroborated_claim_ids(events: list[dict], run_id: str | None = None) -> set[str]:
    """Every claim_id an executed `corroborate` call in this run was asked to count."""
    out: set[str] = set()
    for call in _executed_corroborates(_this_run(events, run_id)):
        for c in call["args"].get("claims", []) or []:
            if isinstance(c, dict) and isinstance(c.get("claim_id"), str):
                out.add(c["claim_id"])
    return out


def claim_coverage_findings(events: list[dict], run_id: str | None = None) -> list[str]:
    """H8: one RETURN_TO_PLANNER finding per recorded claim with no corroborate result, or one for
    a run that recorded no claims at all."""
    recorded = recorded_claim_ids(events, run_id)
    if not recorded:
        return ["RETURN_TO_PLANNER: no claims recorded"]
    covered = corroborated_claim_ids(events, run_id)
    return [f"RETURN_TO_PLANNER: run corroborate for {c}" for c in recorded if c not in covered]


def plan_from_journal(events: list[dict], ctx, args: dict, registry: list[Row] = REGISTRY,
                      run_id: str | None = None) -> Plan:
    corroborates = _executed_corroborates(events)
    b_exits = [e for e in events if e.get("event") == "exit" and e.get("algorithm") == "B"]
    entries: list[PlanEntry] = []
    for g in events:
        if not (g.get("event") == "tool_call" and g["tool"] == "guard" and g["refused_by"] is None and g["reason"] is None):
            continue
        action = guard_action(g["args"])
        hit = reg.lookup(action.refs, registry)
        claims, capped = _claims_for(action.name, corroborates, b_exits, ctx, events)
        # H9 (ABLATION_2): the entry's ref is the action's invoke/mutate paths — what `guard` wrote as the
        # consumer_check ref — never the read refs, which no consumer check is ever expected to cover.
        entries.append(PlanEntry(action.name, guard_mutate_paths(action), hit.stakes, list(hit.hubs),
                                 tripwires_for(hit, action.tripwires), claims, capped,
                                 getattr(ctx, "dispatch_count", 0), args.get("has_failable_check", True),
                                 args.get("metrics_named", True)))
    return Plan(entries, args.get("gate", "checkpoint"), getattr(ctx, "governance_gated", "none"), args.get("gate_at"),
                findings=claim_coverage_findings(events, run_id))


def _claims_for(action_name: str, corroborates: list[dict], b_exits: list[dict], ctx, events: list[dict]):
    calls = [c for c in corroborates if c["args"].get("action") == action_name]
    if not calls:
        return [], []
    call = calls[-1]
    # the B exit line written by that same corroborate call: the last B exit at or before it
    idx = events.index(call)
    line = next((e["exit_line"] for e in reversed(events[:idx]) if e.get("event") == "exit" and e.get("algorithm") == "B"), None)
    rows = {r.claim_id: r for r in parse_corroborate_line(line)} if line else {}
    actor = (getattr(ctx, "actor", None) or {}).get(action_name)
    claims, capped = [], []
    for c in call["args"].get("claims", []):
        row = rows.get(c["claim_id"])
        n_req = row.n_required if row else 1
        claim = Claim(c["claim_id"], c["kind"], action_name, c.get("has_command", True), c.get("remedy_mechanism"),
                      n_req, n_req, actor)
        claims.append(claim)
        if row and row.capped and row.remedy:
            detail = None
            if row.remedy == "add-differently-framed-source":
                detail = unused_framing(claim, events, list(call["args"].get("framings", {}).get(c["claim_id"], [])))
            elif row.remedy == "add-claim-specific-check":
                detail = c.get("remedy_mechanism")
            capped.append(CappedClaim(c["claim_id"], c["kind"], n_req, n_req, row.n_available, row.remedy, detail))
    return claims, capped
