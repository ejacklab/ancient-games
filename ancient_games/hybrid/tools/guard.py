"""D — wraps `stages.guard` (R7). `action_id` and `refs-paths` are journaled by the loop (§6)."""
from ancient_games import registry as reg
from ancient_games.journal import Journal
from ancient_games.stages import guard as _guard

from ..types import ToolResult
from ._shared import ctx_restore, ctx_snapshot, guard_action, internal_error, invalid_args

MANIFEST = {
    "name": "guard", "inputs": {"action": "ActionInput"}, "outputs": "GuardExit",
    "side_effects": "read", "cost": "cheap", "participates_in": ["I1", "I4"], "entrypoint": "run",
}


def unmatched_tripwire_keys(action, registry=reg.REGISTRY) -> tuple[list[str], list[str]]:
    """H11 (ABLATION_2): a declared tripwire must land on a hub element of this action — keyed by the hub's
    name or by the path of a ref that matched into it (H6). A key that resolves to no hub was silently
    dropped (UC2J: `tripwire: {}`); now it is the caller's error, named. Returns (unmatched keys, hubs)."""
    hit = reg.lookup(action.refs, registry)
    allowed = {k for h in hit.hubs for k in hit.tripwire_keys(h)}
    return [k for k in action.tripwires if k not in allowed], list(hit.hubs)


def run(env, args):
    try:
        action = guard_action(args)
    except (ValueError, TypeError, KeyError) as e:
        return ToolResult(ok=False, reason=f"invalid-args: action: {e}")
    unmatched, hubs = unmatched_tripwire_keys(action)
    if unmatched:
        return invalid_args("action.tripwires", f"keyed by a hub element of this action (hubs: {hubs}) or the path of a "
                            "ref that matched into one; a hub reached only through a mutate ref must be declared in that "
                            "ref's `consumers` first", unmatched)
    snapshot = ctx_snapshot(env.ctx)
    try:
        journal = Journal(env.journal_path, env.run_id)
        return ToolResult(ok=True, value=_guard(env.ctx, action, journal))
    except Exception as e:
        ctx_restore(env.ctx, snapshot)
        return internal_error(e)
