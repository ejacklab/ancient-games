"""C — wraps `stages.gate` (R7)."""
from ancient_games.journal import Journal
from ancient_games.stages import TaskInput, gate as _gate

from ..types import ToolResult, hydrate
from ._shared import internal_error

MANIFEST = {
    "name": "gate", "inputs": {"task": "TaskInput"}, "outputs": "GateExit",
    "side_effects": "none", "cost": "cheap", "participates_in": [], "entrypoint": "run",
}


def run(env, args):
    try:
        journal = Journal(env.journal_path, env.run_id)
        task = hydrate(TaskInput, args.get("task", args))
        return ToolResult(ok=True, value=_gate(env.ctx, task, journal))
    except Exception as e:
        return internal_error(e)
