"""HYBRID_SPEC §4 — I1′–I5′ as predicates over (call, ctx, events).

Loop-level pre-execution checks are I1 (commit coverage), I4 (owner gate)
and I5 (dispatch cap); a refusal is journaled into the `tool_call` event
with the invariant id. I2 runs inside `done`'s own body and I3 is static
(the loader's signature check + the stripped ctx the loop hands prove/done)
— neither ever populates `refused_by`. Priority, fixed: I4 > I1 > I5 > I2 > I3.
"""
from __future__ import annotations

from dataclasses import dataclass

from ancient_games import registry as reg
from ancient_games.ctx import ArtifactRef
from ancient_games.registry import CAP, REGISTRY, Row

from .tools._shared import (approvals_after, changed_files, event_ok, guard_action, guard_action_id,
                            last_commit_index, live_dispatches)
from .types import Call

PRIORITY = ("I4", "I1", "I5", "I2", "I3")
RESTRICTED = frozenset({"prove", "done"})  # I3′ consumers: receive the stripped ctx view


@dataclass(frozen=True)
class Refusal:
    invariant: str
    reason: str


def invariants_for(call: Call) -> list[str]:
    """Which invariant ids apply to this call (journaled as `invariants_checked`)."""
    return {"commit": ["I1", "I4"], "guard": ["I4"], "dispatch": ["I5"], "ingest_return": ["I5"],
            "done": ["I2", "I3"], "prove": ["I3"]}.get(call.tool, [])


def check_invariants(call: Call, ctx, events: list[dict], tools: dict, registry: list[Row] = REGISTRY,
                     cwd: str = ".") -> list[Refusal]:
    out: list[Refusal] = []
    if call.tool == "guard":
        r = i4_declared(call, events, registry)
        if r:
            out.append(r)
    if call.tool == "commit":
        changed = changed_files(cwd)
        out += i4_at_commit(changed, events, registry)
        r = i1(changed, events)
        if r:
            out.append(r)
    if call.tool == "dispatch":
        r = i5(events)
        if r:
            out.append(r)
    return sorted(out, key=lambda r: PRIORITY.index(r.invariant))


def pick_by_priority(refusals: list[Refusal]) -> Refusal:
    return min(refusals, key=lambda r: PRIORITY.index(r.invariant))


# I1′ ---------------------------------------------------------------------------
def i1(changed: list[str], events: list[dict]) -> Refusal | None:
    """Scope match at commit: every changed file is named by a non-refused guard's
    `refs-paths` that postdates the last executed commit. Exact-path equality (M3)."""
    after = last_commit_index(events)
    covered: set[str] = set()
    for i, g in enumerate(events):
        if i > after and g.get("event") == "tool_call" and g["tool"] == "guard" and g["refused_by"] is None:
            covered.update(g["args"].get("refs-paths", []))
    uncovered = sorted(set(changed) - covered)
    if uncovered:
        return Refusal("I1", f"unguarded changed files: {uncovered}")
    return None


# I4′ ---------------------------------------------------------------------------
I4_MODES = frozenset({"invoke", "mutate"})  # H1 (ABLATION_1): reads are exempt (S2)


def i4_declared(call: Call, events: list[dict], registry: list[Row]) -> Refusal | None:
    """(a) a declared action whose invoke/mutate refs match a gate=owner row needs an in-window
    owner approval. Refs with mode=read are never looked up (S2; H1) — the registry already
    returns nothing for them, and the invariant states it too. A consumer declared on a
    mutate ref counts (D2′ hub union); the reason names which row matched and how."""
    try:
        action = guard_action(call.args)
    except Exception:
        return None  # malformed args: the adapter reports invalid-args itself
    refs = [r for r in action.refs if r.mode in I4_MODES]
    if not refs:
        return None
    hit = reg.lookup(refs, registry)
    if hit.gate != "owner":
        return None
    aid = guard_action_id(action)
    after = last_commit_index(events)
    if approvals_after(events, "owner", aid, after):
        return None
    rows = ", ".join(f"{m.row.id} via {m.via} {m.ref}" for m in hit.matched if m.row.gate == "owner")
    stale = approvals_after(events, "owner", aid, -1)
    if stale:
        return Refusal("I4", f"hard_blocked: approval stale (predates last commit) for {aid} [owner rows: {rows}]")
    return Refusal("I4", f"hard_blocked: no owner approval on record for {aid} [owner rows: {rows}]")


def i4_at_commit(changed: list[str], events: list[dict], registry: list[Row]) -> list[Refusal]:
    """(b) an undeclared mutation: each changed file whose own registry row is owner-gated
    needs an in-window approval keyed by the row id (25′)."""
    after = last_commit_index(events)
    for f in changed:
        hit = reg.lookup([ArtifactRef(f, "mutate")], registry)
        if hit.gate != "owner":
            continue
        rows = [m.row.id for m in hit.matched if m.row.gate == "owner"]
        if not any(approvals_after(events, "owner", rid, after) for rid in rows):
            return [Refusal("I4", f"hard_blocked: owner-gated file {f} ({','.join(rows)}) changed without approval")]
    return []


# I5′ ---------------------------------------------------------------------------
def i5(events: list[dict]) -> Refusal | None:
    live = live_dispatches(events)
    if live >= CAP:
        return Refusal("I5", f"live_dispatches={live}, CAP={CAP}, no slot")
    return None


__all__ = ["Refusal", "check_invariants", "pick_by_priority", "invariants_for", "PRIORITY", "RESTRICTED",
           "I4_MODES", "live_dispatches", "event_ok"]
