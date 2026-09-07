"""A — wraps `stages.prove` (R7). `env.ctx` is the stripped view (I3′): the plan is
rebuilt from the journal, so every count A checks is `corroborate`'s journaled one.
H8 (ABLATION_1): the plan's claims are the run's recorded ones (`_plan.recorded_claim_ids`);
a recorded claim with no executed `corroborate` naming it, or a run with no recorded claim,
is a RETURN_TO_PLANNER finding — `prove` never counts, and never PASSes an empty plan."""
from ancient_games.journal import Journal
from ancient_games.stages import prove as _prove

from ..types import ToolResult
from ._plan import plan_from_journal
from ._shared import internal_error, invalid_args

MANIFEST = {
    "name": "prove", "inputs": {"gate": "str", "gate_at": "str", "has_failable_check": "bool", "metrics_named": "bool"},
    "outputs": "ProveExit", "side_effects": "read", "cost": "cheap", "participates_in": ["I2", "I3"], "entrypoint": "run",
}
FLAGS = ("has_failable_check", "metrics_named", "disclose")


def run(env, args):
    for name in FLAGS:  # H2 (ABLATION_1): typed flags
        if name in args and not isinstance(args[name], bool):
            return invalid_args(name, "true or false", args[name])
    if "gate" in args and not isinstance(args["gate"], str):
        return invalid_args("gate", "a str (checkpoint | owner(<name>) | none)", args["gate"])
    if args.get("gate_at") is not None and not isinstance(args["gate_at"], str):
        return invalid_args("gate_at", "a str or null", args["gate_at"])
    try:
        journal = Journal(env.journal_path, env.run_id)
        plan = plan_from_journal(journal.read(), env.ctx, args, run_id=env.run_id)
        return ToolResult(ok=True, value=_prove(env.ctx, plan, journal, disclose=args.get("disclose", True)))
    except Exception as e:
        return internal_error(e)
