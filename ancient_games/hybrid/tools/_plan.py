"""Plan reconstruction from the journal, shared by `prove` and `run_lint`.

`prove`/`done` receive the stripped ctx (I3′), so the plan A checks is
rebuilt from journaled facts only: each non-refused `guard` tool_call is
one entry (refs, stakes/hub via the registry, tripwires from its own
args); the latest Corroborate exit line per action supplies the claims'
n_required / capped status — counts come from `corroborate`'s journaled
result, never from the agent or from ctx.
"""
from __future__ import annotations

from ancient_games import registry as reg
from ancient_games.ctx import CappedClaim
from ancient_games.registry import REGISTRY, Row
from ancient_games.stages import Claim, Plan, PlanEntry, unused_framing
from ancient_games.trace import parse_corroborate_line

from ._shared import guard_action


def plan_from_journal(events: list[dict], ctx, args: dict, registry: list[Row] = REGISTRY) -> Plan:
    corroborates = [e for e in events if e.get("event") == "tool_call" and e["tool"] == "corroborate"
                    and e["refused_by"] is None and e["reason"] is None]
    b_exits = [e for e in events if e.get("event") == "exit" and e.get("algorithm") == "B"]
    entries: list[PlanEntry] = []
    for g in events:
        if not (g.get("event") == "tool_call" and g["tool"] == "guard" and g["refused_by"] is None and g["reason"] is None):
            continue
        action = guard_action(g["args"])
        hit = reg.lookup(action.refs, registry)
        claims, capped = _claims_for(action.name, corroborates, b_exits, ctx, events)
        entries.append(PlanEntry(action.name, g["args"].get("refs-paths", []), hit.stakes, list(hit.hubs),
                                 {h: action.tripwires[h] for h in hit.hubs if h in action.tripwires}, claims, capped,
                                 getattr(ctx, "dispatch_count", 0), args.get("has_failable_check", True),
                                 args.get("metrics_named", True)))
    return Plan(entries, args.get("gate", "checkpoint"), getattr(ctx, "governance_gated", "none"), args.get("gate_at"))


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
