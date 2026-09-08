"""Wraps `journal.ingest_return` (journal.py:218): the `return` event plus its classified CLAIMS."""
from ancient_games.journal import Journal

from ..types import ToolResult
from ._shared import author_refusal, internal_error, require_str

MANIFEST = {
    "name": "ingest_return", "inputs": {"agent_id": "str", "fields": "dict", "actor": "str", "framing": "str"},
    "outputs": "list[event]", "side_effects": "none", "cost": "cheap", "participates_in": ["I5"], "entrypoint": "run",
}


def run(env, args):
    bad = require_str(args, "agent_id")  # before the try: a missing agent_id is the caller's error
    if bad is not None:
        return bad
    journal = Journal(env.journal_path, env.run_id)
    # F1: journal.py:271 passes `agent_id` through as the mirrored claims' `author`. Checked BEFORE
    # `ingest_return`, which writes the `return` event and its claims together — a partial write
    # would leave a `return` with no claims. Constraining only record_claim leaves this path, which
    # is stronger: the forged journal also reads as genuine agent returns.
    bad = author_refusal(args["agent_id"], journal.read())
    if bad is not None:
        return bad
    try:
        evs = journal.ingest_return(args["agent_id"], args.get("fields") or {}, args.get("actor", "MAIN"), args.get("framing"))
        return ToolResult(ok=True, value=[e["event"] for e in evs])
    except Exception as e:
        return internal_error(e)
