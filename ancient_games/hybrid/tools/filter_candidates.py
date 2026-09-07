"""E — wraps `stages.filter_candidates` (R7); real ctx, real args (K3)."""
from ancient_games.journal import Journal
from ancient_games.stages import Candidate, FilterDecisions, filter_candidates as _filter

from ..types import ToolResult, hydrate
from ._shared import internal_error

MANIFEST = {
    "name": "filter_candidates",
    "inputs": {"candidates": "list[Candidate|str]", "cut": "dict", "merged": "dict", "follow_on": "list", "intents": "dict"},
    "outputs": "FilterExit", "side_effects": "read", "cost": "cheap", "participates_in": [], "entrypoint": "run",
}


def run(env, args):
    try:
        journal = Journal(env.journal_path, env.run_id)
        cands = [Candidate(c) if isinstance(c, str) else hydrate(Candidate, c) for c in args.get("candidates", [])]
        decisions = hydrate(FilterDecisions, {k: args[k] for k in ("cut", "merged", "follow_on", "intents") if k in args})
        if "scope_items" in args:
            env.ctx.scope_items = list(args["scope_items"])
        return ToolResult(ok=True, value=_filter(env.ctx, cands, decisions, journal))
    except Exception as e:
        return internal_error(e)
