"""NEW — `done`, a real executed tool running I2′'s two clauses (K8) after the owner-gate precheck (H15):
(0) owner gate — the latest `prove` PASS cleared the plan to an `owner(<name>)` gate and no in-window
    `approval_recorded{gate=owner, action_id=<the gate's own subject>}` exists ⇒ ok=False,
    reason="owner-gate-pending: <name> (approve action_id=<id>)" (ABLATION_3; the action_id match is
    REVIEW_B F1 — matching on the gate alone let an owner approval recorded for an unrelated action
    clear a governance-gated decision the owner never saw). The subject is the governance-gated
    registry row when the plan is governance-gated (the same key `i4_at_commit` uses, 25'), else
    `plan:<run_id>` — the prove call's own `gate=owner(...)` arg clears this run's plan and the
    journal names no narrower subject. A governance-gated plan whose row cannot be read back from
    the journal fails closed: the subject is `governance-gated:<unknown>`, which no approval matches;
(a) freshness — the latest non-refused `prove` PASS postdates every non-refused
    `mutate`-side-effect tool_call (`commit` is categorically excluded);
(b) accounted tree — every path in `git diff --name-only HEAD` ∪ untracked is committed, or is listed in
    `deliverables` AND was an invoke/mutate ref of an executed `guard` in this run (ABLATION_3 H14);
    anything else refuses, naming it — a native edit still cannot hide.
Declines return ok=False with the reason; the loop journals an ordinary tool_call
and continues — `refused_by` is never populated by I2."""
import re

from ancient_games.journal import Journal

from ..types import ToolResult
from ._shared import (approvals_after, changed_files, event_ok, guard_action, guard_mutate_paths, internal_error,
                      invalid_args, last_commit_index)

MANIFEST = {
    "name": "done", "inputs": {"deliverables": "list[str]"}, "outputs": "DONE", "side_effects": "none", "cost": "cheap",
    "participates_in": ["I2", "I3"], "entrypoint": "run",
}
# the A exit line `stages.prove` writes: "... plan cleared to terminal gate=owner(ej) [governance-gated] ..."
# (governance-gated plan) or "... plan cleared to owner(ej) gate (at commit)" (the prove call's own gate arg)
_OWNER_GATE = re.compile(r"plan cleared to (?:terminal gate=)?owner\(([^)]+)\)")
_GOVERNANCE_MARK = "[governance-gated]"
UNKNOWN_ROW = "governance-gated:<unknown>"  # fail-closed subject: no approval can carry it


def governance_row(events: list[dict], prove_index: int) -> str | None:
    """The registry row this run's governance gate names: `task.governance_gated` of the latest executed
    `gate` call before the prove — the same value `stages.prove` read off `ctx.governance_gated` when it
    wrote `[governance-gated]` into the exit line. Read from the journaled args, not from the exit line,
    so no free-text stop-criterion can spoof it."""
    for e in reversed(events[:prove_index]):
        if e.get("event") == "tool_call" and e["tool"] == "gate" and event_ok(e):
            args = e.get("args") or {}
            task = args.get("task", args)
            gg = task.get("governance_gated", "none") if isinstance(task, dict) else "none"
            return gg if isinstance(gg, str) and gg != "none" else None
    return None


def terminal_gate(events: list[dict], prove_index: int, run_id: str) -> tuple[str, str] | None:
    """(owner, action_id) of the owner gate the A exit line at `prove_index` cleared the plan to,
    or None when it cleared to no owner gate. `action_id` is the subject the owner must approve —
    see clause (0) in the module docstring."""
    line = next((e["exit_line"] for e in reversed(events[:prove_index]) if e.get("event") == "exit" and e.get("algorithm") == "A"), "")
    m = _OWNER_GATE.search(line)
    if not m:
        return None
    if _GOVERNANCE_MARK in line:
        return m.group(1), governance_row(events, prove_index) or UNKNOWN_ROW
    return m.group(1), f"plan:{run_id}"


def guarded_mutate_paths(events: list[dict]) -> set[str]:
    """Paths an executed `guard` in this run declared with mode invoke/mutate."""
    out: set[str] = set()
    for e in events:
        if event_ok(e) and e["tool"] == "guard":
            try:
                out.update(guard_mutate_paths(guard_action(e["args"])))
            except Exception:
                continue
    return out


def run(env, args):
    deliverables = args.get("deliverables", [])
    if not isinstance(deliverables, list) or not all(isinstance(p, str) for p in deliverables):
        return invalid_args("deliverables", "a list of paths (str)", deliverables)
    try:
        events = [e for e in Journal(env.journal_path, env.run_id).read() if e["run_id"] == env.run_id]
        proves = [i for i, e in enumerate(events) if e.get("event") == "tool_call" and e["tool"] == "prove"
                  and e["refused_by"] is None and e.get("exit_type") == "PASS"]
        if not proves:
            return ToolResult(ok=False, reason="no-prove-pass")
        latest = proves[-1]
        gate = terminal_gate(events, latest, env.run_id)
        if gate is not None:
            owner, aid = gate
            if not approvals_after(events, "owner", aid, last_commit_index(events)):
                return ToolResult(ok=False, reason=f"owner-gate-pending: {owner} (approve action_id={aid})")
        staling = [e for i, e in enumerate(events) if i > latest and e.get("event") == "tool_call"
                   and e["refused_by"] is None and e["tool"] in env.tools
                   and env.tools[e["tool"]].manifest["side_effects"] == "mutate"]
        if staling:
            return ToolResult(ok=False, reason=f"prove-stale: {staling[-1]['tool']}")
        changed = changed_files(env.cwd)
        if changed:
            accounted = set(deliverables) & guarded_mutate_paths(events)
            unaccounted = [f for f in changed if f not in accounted]
            if unaccounted:
                return ToolResult(ok=False, reason=f"uncommitted-changes: {unaccounted}")
        return ToolResult(ok=True, value="DONE")
    except Exception as e:
        return internal_error(e)
