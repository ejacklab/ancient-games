"""A — wraps `stages.prove` (R7). `env.ctx` is the stripped view (I3′): the plan is
rebuilt from the journal, so every count A checks is `corroborate`'s journaled one."""
from ancient_games.journal import Journal
from ancient_games.stages import prove as _prove

from ..types import ToolResult
from ._plan import plan_from_journal
from ._shared import internal_error

MANIFEST = {
    "name": "prove", "inputs": {"gate": "str", "gate_at": "str", "has_failable_check": "bool", "metrics_named": "bool"},
    "outputs": "ProveExit", "side_effects": "read", "cost": "cheap", "participates_in": ["I2", "I3"], "entrypoint": "run",
}


def run(env, args):
    try:
        journal = Journal(env.journal_path, env.run_id)
        plan = plan_from_journal(journal.read(), env.ctx, args)
        return ToolResult(ok=True, value=_prove(env.ctx, plan, journal, disclose=args.get("disclose", True)))
    except Exception as e:
        return internal_error(e)
