"""Wraps `lints.run_all_on_plan` over the journal-reconstructed plan."""
from ancient_games.journal import Journal
from ancient_games.lints import run_all_on_plan

from ..types import ToolResult
from ._plan import plan_from_journal
from ._shared import internal_error

MANIFEST = {
    "name": "run_lint", "inputs": {"gate": "str", "gate_at": "str"}, "outputs": "list[Finding]",
    "side_effects": "read", "cost": "cheap", "participates_in": [], "entrypoint": "run",
}


def run(env, args):
    try:
        events = Journal(env.journal_path, env.run_id).read()
        return ToolResult(ok=True, value=run_all_on_plan(plan_from_journal(events, env.ctx, args), events))
    except Exception as e:
        return internal_error(e)
