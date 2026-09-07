"""Wraps `journal.read` (journal.py:189) — every UC's observe step."""
from ancient_games.journal import Journal

from ..types import ToolResult
from ._shared import internal_error

MANIFEST = {
    "name": "read_journal", "inputs": {}, "outputs": "list[event]",
    "side_effects": "read", "cost": "cheap", "participates_in": [], "entrypoint": "run",
}


def run(env, args):
    try:
        return ToolResult(ok=True, value=Journal(env.journal_path, env.run_id).read())
    except Exception as e:
        return internal_error(e)
