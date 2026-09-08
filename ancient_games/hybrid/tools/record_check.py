"""Wraps `journal.check_executed` (journal.py:202). `falsifies` is a claim id (H3, ABLATION_1).

F2: every field §7 constrains is checked HERE, before the write, so a bad value is
`invalid-args` (CLI exit 2) rather than the `internal-error` a ValueError out of
`validate_event` would become — `cli.cmd_call` keys its exit code on the `invalid-args:`
prefix, so an unprefixed decline exits 0.
"""
from ancient_games.ctx import MECHANISMS
from ancient_games.journal import _ENUMS, _NUM_OR_STR, Journal, valid_mechanism

from ..types import ToolResult
from ._shared import internal_error, invalid_args, require_str

MANIFEST = {
    "name": "record_check",
    "inputs": {"claim_id": "str", "mechanism": "str", "command": "str", "expected": "str|int", "observed": "str|int",
               "pre_fix_result": "str", "falsifies": "str"},
    "outputs": "check_executed event", "side_effects": "none", "cost": "cheap", "participates_in": [], "entrypoint": "run",
}
PRE_FIX_RESULTS = _ENUMS[("check_executed", "pre_fix_result")]  # ("FAIL", None)


def known_claim_ids(events: list[dict], run_id: str) -> list[str]:
    out: list[str] = []
    for e in events:
        if e.get("event") == "claim_recorded" and e.get("run_id") == run_id and e["claim_id"] not in out:
            out.append(e["claim_id"])
    return out


def validate(args) -> ToolResult | None:
    """Every check that needs no I/O (F2), split out so `ingest_return` can validate a whole CLAIMS
    list before writing any of it. The `falsifies` check stays in `run` — it reads the journal."""
    bad = require_str(args, "claim_id", "mechanism")  # the caller's error, not internal
    if bad is not None:
        return bad
    if not valid_mechanism(args["mechanism"]):  # one definition, shared with journal.validate_event
        return invalid_args("mechanism", "one of " + " | ".join(MECHANISMS) + ", or other:<name>", args["mechanism"])
    if args.get("pre_fix_result") not in PRE_FIX_RESULTS:
        return invalid_args("pre_fix_result", "FAIL, or omitted", args.get("pre_fix_result"))
    for name in ("expected", "observed"):
        if name in args and not isinstance(args[name], _NUM_OR_STR):
            return invalid_args(name, "a str or a number", args[name])
    return None


def run(env, args):
    bad = validate(args)
    if bad is not None:
        return bad
    journal = Journal(env.journal_path, env.run_id)
    claim_id = args["claim_id"]
    falsifies = args.get("falsifies") or claim_id
    # B·1 counts only check_executed{claim_id=X, falsifies=X}: `falsifies` names a claim, never a
    # condition. Accepted: this call's own claim_id, or a claim_id recorded in this run.
    known = known_claim_ids(journal.read(), env.run_id)
    if falsifies != claim_id and falsifies not in known:
        # `invalid_args` for the prefix cmd_call's exit code needs, keeping the enumerated detail —
        # that detail is the admissible-alternatives content and is why this field has had 0 failures.
        return invalid_args("falsifies", f"a claim_id — put the condition in `expected` (this call's claim_id "
                                         f"is {claim_id!r}; claim_ids recorded in this run: {known})", falsifies)
    try:
        ev = journal.check_executed(claim_id, args["mechanism"], args.get("command", ""), args.get("expected", ""),
                                    args.get("observed", ""), args.get("pre_fix_result"), falsifies)
        return ToolResult(ok=True, value=ev)
    except Exception as e:
        return internal_error(e)
