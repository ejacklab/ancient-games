"""C — wraps `stages.gate` (R7). Inputs are validated before the stage runs (H2/H7, ABLATION_1)."""
from ancient_games import registry as reg
from ancient_games.journal import Journal
from ancient_games.stages import TaskInput, gate as _gate

from ..types import ToolResult, hydrate
from ._shared import ctx_restore, ctx_snapshot, internal_error, invalid_args

MANIFEST = {
    "name": "gate", "inputs": {"task": "TaskInput"}, "outputs": "GateExit",
    "side_effects": "none", "cost": "cheap", "participates_in": [], "entrypoint": "run",
}


def owner_row_ids(registry=reg.REGISTRY) -> list[str]:
    return [r.id for r in registry if r.gate == "owner"]


def run(env, args):
    task_args = args.get("task", args)
    if not isinstance(task_args, dict):
        return invalid_args("task", "a JSON object (TaskInput)", task_args)
    gg = task_args.get("governance_gated", "none")
    if not isinstance(gg, str) or (gg != "none" and gg not in owner_row_ids()):
        return invalid_args("governance_gated", '"none" or an owner-gated registry row id (one of '
                            + "|".join(owner_row_ids()) + "), never a bool", gg)
    try:
        task = hydrate(TaskInput, task_args)
    except (ValueError, TypeError, KeyError) as e:
        return ToolResult(ok=False, reason=f"invalid-args: task: {e}")
    snapshot = ctx_snapshot(env.ctx)
    try:
        journal = Journal(env.journal_path, env.run_id)
        return ToolResult(ok=True, value=_gate(env.ctx, task, journal))
    except Exception as e:
        ctx_restore(env.ctx, snapshot)
        return internal_error(e)
