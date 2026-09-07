"""Wraps `journal.check_executed` (journal.py:202)."""
from ancient_games.journal import Journal

from ..types import ToolResult
from ._shared import internal_error

MANIFEST = {
    "name": "record_check",
    "inputs": {"claim_id": "str", "mechanism": "str", "command": "str", "expected": "str|int", "observed": "str|int",
               "pre_fix_result": "str", "falsifies": "str"},
    "outputs": "check_executed event", "side_effects": "none", "cost": "cheap", "participates_in": [], "entrypoint": "run",
}


def run(env, args):
    try:
        journal = Journal(env.journal_path, env.run_id)
        ev = journal.check_executed(args["claim_id"], args["mechanism"], args.get("command", ""), args.get("expected", ""),
                                    args.get("observed", ""), args.get("pre_fix_result"), args.get("falsifies"))
        return ToolResult(ok=True, value=ev)
    except Exception as e:
        return internal_error(e)
