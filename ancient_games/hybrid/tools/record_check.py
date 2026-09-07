"""Wraps `journal.check_executed` (journal.py:202). `falsifies` is a claim id (H3, ABLATION_1)."""
from ancient_games.journal import Journal

from ..types import ToolResult
from ._shared import internal_error, require_str

MANIFEST = {
    "name": "record_check",
    "inputs": {"claim_id": "str", "mechanism": "str", "command": "str", "expected": "str|int", "observed": "str|int",
               "pre_fix_result": "str", "falsifies": "str"},
    "outputs": "check_executed event", "side_effects": "none", "cost": "cheap", "participates_in": [], "entrypoint": "run",
}
FALSIFIES_REASON = "falsifies must be a claim_id; put the condition in `expected`"


def known_claim_ids(events: list[dict], run_id: str) -> list[str]:
    out: list[str] = []
    for e in events:
        if e.get("event") == "claim_recorded" and e.get("run_id") == run_id and e["claim_id"] not in out:
            out.append(e["claim_id"])
    return out


def run(env, args):
    bad = require_str(args, "claim_id", "mechanism")  # before the try: the caller's error, not internal
    if bad is not None:
        return bad
    try:
        journal = Journal(env.journal_path, env.run_id)
        claim_id = args["claim_id"]
        falsifies = args.get("falsifies") or claim_id
        # B·1 counts only check_executed{claim_id=X, falsifies=X}: `falsifies` names a claim, never a
        # condition. Accepted: this call's own claim_id, or a claim_id recorded in this run.
        known = known_claim_ids(journal.read(), env.run_id)
        if falsifies != claim_id and falsifies not in known:
            return ToolResult(ok=False, reason=f"{FALSIFIES_REASON} (got {falsifies!r}; this call's claim_id is "
                                               f"{claim_id!r}; claim_ids recorded in this run: {known})")
        ev = journal.check_executed(claim_id, args["mechanism"], args.get("command", ""), args.get("expected", ""),
                                    args.get("observed", ""), args.get("pre_fix_result"), falsifies)
        return ToolResult(ok=True, value=ev)
    except Exception as e:
        return internal_error(e)
