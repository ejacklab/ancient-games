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

# `invariants_checked` is an audit record, so it names only invariants that actually ran.
# LOOP_CHECKED is what `evaluate_loop_invariants` evaluates, tool by tool — the two are kept
# honest by `tests/test_hybrid_invariants.py::test_invariants_checked_names_only_checks_that_ran`,
# which reads the evaluated ids back off a real call rather than trusting this table.
LOOP_CHECKED: dict[str, tuple[str, ...]] = {"commit": ("I1", "I4"), "guard": ("I4",), "dispatch": ("I5",)}
# Invariants evaluated outside `check_invariants`, each with where it runs: I2 is executed by
# `done`'s own adapter body (`tools/done.py`), I3 is static — the loader's signature check plus the
# stripped ctx `loop.step` hands prove/done. `ingest_return` declared I5 here until it was removed:
# it never ran (only `dispatch` evaluates I5), and running it would be wrong anyway — I5 refuses when
# the cap is full, and refusing the return that frees a slot would deadlock the run. `ingest_return`
# still *participates in* I5's computation (`live_dispatches`), which its manifest records; that is
# a different claim from "a check ran on this call".
ELSEWHERE_CHECKED: dict[str, tuple[str, ...]] = {"done": ("I2", "I3"), "prove": ("I3",)}


@dataclass(frozen=True)
class Refusal:
    invariant: str
    reason: str


def invariants_for(call: Call) -> list[str]:
    """The invariant ids journaled as `invariants_checked` for this call — every one of them
    evaluated: the loop-checked set (`evaluate_loop_invariants`) plus the set that runs
    elsewhere (`ELSEWHERE_CHECKED`, which records where each of those runs)."""
    return list(LOOP_CHECKED.get(call.tool, ())) + list(ELSEWHERE_CHECKED.get(call.tool, ()))


def evaluate_loop_invariants(call: Call, ctx, events: list[dict], tools: dict, registry: list[Row] = REGISTRY,
                             cwd: str = ".") -> tuple[list[str], list[Refusal]]:
    """(the invariant ids this call actually evaluated, the refusals they produced).

    The ids come back from the evaluation itself, so `LOOP_CHECKED` — and therefore the journal's
    `invariants_checked` — can be checked against what ran instead of asserted."""
    evaluated: list[str] = []
    out: list[Refusal] = []
    if call.tool == "guard":
        evaluated.append("I4")
        r = i4_declared(call, events, registry)
        if r:
            out.append(r)
    if call.tool == "commit":
        changed = changed_files(cwd)
        evaluated += ["I1", "I4"]
        out += i4_at_commit(changed, events, registry)
        r = i1(changed, events)
        if r:
            out.append(r)
    if call.tool == "dispatch":
        evaluated.append("I5")
        r = i5(events)
        if r:
            out.append(r)
    return evaluated, sorted(out, key=lambda r: PRIORITY.index(r.invariant))


def check_invariants(call: Call, ctx, events: list[dict], tools: dict, registry: list[Row] = REGISTRY,
                     cwd: str = ".") -> list[Refusal]:
    return evaluate_loop_invariants(call, ctx, events, tools, registry, cwd)[1]


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


__all__ = ["Refusal", "check_invariants", "evaluate_loop_invariants", "pick_by_priority", "invariants_for",
           "LOOP_CHECKED", "ELSEWHERE_CHECKED", "PRIORITY", "RESTRICTED",
           "I4_MODES", "live_dispatches", "event_ok"]
