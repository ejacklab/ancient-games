"""Wraps `journal.claim_recorded` (journal.py:208)."""
from ancient_games.journal import Journal

from ..types import ToolResult
from ._shared import internal_error

MANIFEST = {
    "name": "record_claim",
    "inputs": {"claim_id": "str", "author": "str", "actor": "str", "kind": "str", "text": "str",
               "evidence_type": "str", "evidence_ref": "str", "framing": "str"},
    "outputs": "claim_recorded event", "side_effects": "none", "cost": "cheap", "participates_in": [], "entrypoint": "run",
}


def run(env, args):
    try:
        journal = Journal(env.journal_path, env.run_id)
        ev = journal.claim_recorded(args["claim_id"], args["author"], args.get("actor", "MAIN"), args["kind"],
                                    args.get("text", args["claim_id"]), args["evidence_type"], args.get("evidence_ref", ""),
                                    args.get("framing"))
        return ToolResult(ok=True, value=ev)
    except Exception as e:
        return internal_error(e)
