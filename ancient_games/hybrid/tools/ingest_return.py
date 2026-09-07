"""Wraps `journal.ingest_return` (journal.py:218): the `return` event plus its classified CLAIMS."""
from ancient_games.journal import Journal

from ..types import ToolResult
from ._shared import internal_error

MANIFEST = {
    "name": "ingest_return", "inputs": {"agent_id": "str", "fields": "dict", "actor": "str", "framing": "str"},
    "outputs": "list[event]", "side_effects": "none", "cost": "cheap", "participates_in": ["I5"], "entrypoint": "run",
}


def run(env, args):
    try:
        journal = Journal(env.journal_path, env.run_id)
        evs = journal.ingest_return(args["agent_id"], args.get("fields") or {}, args.get("actor", "MAIN"), args.get("framing"))
        return ToolResult(ok=True, value=[e["event"] for e in evs])
    except Exception as e:
        return internal_error(e)
