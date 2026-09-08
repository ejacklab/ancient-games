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
    # H18 (ABLATION_5): B·1 (c) counts `check_executed{claim_id=X, falsifies=X}` — BOTH fields. A
    # check journaled with claim_id "C1-check" falsifying "C1" counts for nothing and says nothing,
    # which is ABLATION_1's H3 recurring: "n=0/3 despite three recorded checks". H3 fixed prose in
    # `falsifies`; this is the other half. `claim_id` IS the claim the check is evidence for.
    falsifies = args.get("falsifies")
    if falsifies is not None and falsifies != args["claim_id"]:
        return invalid_args("falsifies", f"this call's own claim_id, {args['claim_id']!r} — a check is "
                            "evidence FOR the claim named in `claim_id`, and B·1 counts it only when the "
                            "two agree, so a different value here counts for nothing. Put a CONDITION in "
                            f"`expected`; to back claim {falsifies!r}, pass claim_id={falsifies!r}", falsifies)
    return None


def run(env, args):
    bad = validate(args)
    if bad is not None:
        return bad
    # H18 collapsed `falsifies`'s admissible set to a single value — this call's own claim_id — so the
    # old run-level check ("a claim_id recorded in this run") is unreachable: `validate` has already
    # established falsifies == claim_id. Naming the one legal value is tighter guidance than
    # enumerating every recorded id, which is why that enumeration is gone rather than merely moved.
    journal = Journal(env.journal_path, env.run_id)
    claim_id = args["claim_id"]
    falsifies = args.get("falsifies") or claim_id
    try:
        ev = journal.check_executed(claim_id, args["mechanism"], args.get("command", ""), args.get("expected", ""),
                                    args.get("observed", ""), args.get("pre_fix_result"), falsifies)
        return ToolResult(ok=True, value=ev)
    except Exception as e:
        return internal_error(e)
