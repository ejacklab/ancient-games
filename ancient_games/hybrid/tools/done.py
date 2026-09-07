"""NEW — `done`, a real executed tool running I2′'s two clauses (K8) after the owner-gate precheck (H15):
(0) owner gate — the latest `prove` PASS cleared the plan to an `owner(<name>)` gate and no in-window
    `approval_recorded{gate=owner}` exists ⇒ ok=False, reason="owner-gate-pending: <name>" (ABLATION_3);
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
from ._shared import (changed_files, event_ok, guard_action, guard_mutate_paths, internal_error, invalid_args,
                      last_commit_index)

MANIFEST = {
    "name": "done", "inputs": {"deliverables": "list[str]"}, "outputs": "DONE", "side_effects": "none", "cost": "cheap",
    "participates_in": ["I2", "I3"], "entrypoint": "run",
}
# the A exit line `stages.prove` writes: "... plan cleared to terminal gate=owner(ej) [governance-gated] ..."
# (governance-gated plan) or "... plan cleared to owner(ej) gate (at commit)" (the prove call's own gate arg)
_OWNER_GATE = re.compile(r"plan cleared to (?:terminal gate=)?owner\(([^)]+)\)")


def terminal_owner(events: list[dict], prove_index: int) -> str | None:
    """The owner the plan's terminal gate names, read off the A exit line the prove call at `prove_index` wrote."""
    line = next((e["exit_line"] for e in reversed(events[:prove_index]) if e.get("event") == "exit" and e.get("algorithm") == "A"), "")
    m = _OWNER_GATE.search(line)
    return m.group(1) if m else None


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
        owner = terminal_owner(events, latest)
        if owner is not None:
            after = last_commit_index(events)
            approved = any(i > after and e.get("event") == "approval_recorded" and e["gate"] == "owner"
                           for i, e in enumerate(events))
            if not approved:
                return ToolResult(ok=False, reason=f"owner-gate-pending: {owner}")
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
