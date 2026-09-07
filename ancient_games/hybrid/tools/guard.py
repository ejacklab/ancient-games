"""D — wraps `stages.guard` (R7). `action_id` and `refs-paths` are journaled by the loop (§6)."""
from ancient_games.journal import Journal
from ancient_games.stages import guard as _guard

from ..types import ToolResult
from ._shared import guard_action, internal_error

MANIFEST = {
    "name": "guard", "inputs": {"action": "ActionInput"}, "outputs": "GuardExit",
    "side_effects": "read", "cost": "cheap", "participates_in": ["I1", "I4"], "entrypoint": "run",
}


def run(env, args):
    try:
        journal = Journal(env.journal_path, env.run_id)
        return ToolResult(ok=True, value=_guard(env.ctx, guard_action(args), journal))
    except Exception as e:
        return internal_error(e)
