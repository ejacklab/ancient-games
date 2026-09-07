"""D — wraps `stages.guard` (R7). `action_id` and `refs-paths` are journaled by the loop (§6)."""
from ancient_games.journal import Journal
from ancient_games.stages import guard as _guard

from ..types import ToolResult
from ._shared import ctx_restore, ctx_snapshot, guard_action, internal_error, invalid_args

MANIFEST = {
    "name": "guard", "inputs": {"action": "ActionInput"}, "outputs": "GuardExit",
    "side_effects": "read", "cost": "cheap", "participates_in": ["I1", "I4"], "entrypoint": "run",
}


def run(env, args):
    if not isinstance(args.get("action"), dict):
        return invalid_args("action", "a JSON object (ActionInput)", args.get("action"))
    try:
        action = guard_action(args)
    except (ValueError, TypeError, KeyError) as e:
        return ToolResult(ok=False, reason=f"invalid-args: action: {e}")
    snapshot = ctx_snapshot(env.ctx)
    try:
        journal = Journal(env.journal_path, env.run_id)
        return ToolResult(ok=True, value=_guard(env.ctx, action, journal))
    except Exception as e:
        ctx_restore(env.ctx, snapshot)
        return internal_error(e)
