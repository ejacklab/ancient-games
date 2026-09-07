"""B — wraps `stages.corroborate` (R7); I3's sole producer, ordinary ctx access."""
from ancient_games.journal import Journal
from ancient_games.stages import Claim, corroborate as _corroborate

from ..types import ToolResult, hydrate
from ._shared import internal_error

MANIFEST = {
    "name": "corroborate",
    "inputs": {"action": "str", "claims": "list[Claim]", "framings": "dict", "reconciliation": "str", "dominance": "str"},
    "outputs": "CorroborateExit", "side_effects": "read", "cost": "cheap", "participates_in": ["I3"], "entrypoint": "run",
}


def run(env, args):
    try:
        journal = Journal(env.journal_path, env.run_id)
        claims = [hydrate(Claim, c) for c in args["claims"]]
        result = _corroborate(env.ctx, claims, journal, args["action"], args.get("framings"),
                              args.get("reconciliation", "agree"), args.get("dominance"))
        return ToolResult(ok=True, value=result)
    except Exception as e:
        return internal_error(e)
