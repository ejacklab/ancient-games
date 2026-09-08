"""Wraps `journal.claim_recorded` (journal.py:208). D-KIND (ABLATION_2): `kind` is assigned by rule —
absence / universal-negative text (`ctx.ABSENCE_PATTERNS`) is `judgment`; the author's `executable`
is accepted only with a non-empty `closed_world` reason, and that override is journaled."""
from ancient_games.ctx import CLAIM_KINDS, kind_by_rule
from ancient_games.journal import EVIDENCE_TYPES, Journal

from ..types import ToolResult
from ._shared import author_refusal, internal_error, invalid_args

MANIFEST = {
    "name": "record_claim",
    "inputs": {"claim_id": "str", "author": "str", "actor": "str", "kind": "str", "text": "str",
               "evidence_type": "str", "evidence_ref": "str", "framing": "str", "closed_world": "str"},
    "outputs": "claim_recorded event", "side_effects": "none", "cost": "cheap", "participates_in": [], "entrypoint": "run",
}


def assign_kind(declared: str, text: str, closed_world) -> tuple[str, bool]:
    """(kind, kind_override): the rule's `judgment` stands over a declared `executable` unless
    `closed_world` is a non-empty reason; a claim the rule does not touch keeps the author's kind."""
    if kind_by_rule(text) == "judgment" and declared == "executable":
        if isinstance(closed_world, str) and closed_world.strip():
            return "executable", True
        return "judgment", False
    return declared, False


def validate(args) -> ToolResult | None:
    """Every check that needs no I/O, split out so a caller holding several claims can validate them
    ALL before writing any (`ingest_return`: the `return` event and its claims are one unit). The
    author gate stays in `run` — it reads the journal. Same shape as `corroborate._validate`."""
    for name in ("claim_id", "author"):
        if not isinstance(args.get(name), str) or not args[name]:
            return invalid_args(name, "a non-empty str", args.get(name))
    if args.get("kind") not in CLAIM_KINDS:
        return invalid_args("kind", "one of " + "|".join(CLAIM_KINDS), args.get("kind"))
    closed_world = args.get("closed_world")
    if closed_world is not None and not isinstance(closed_world, str):
        return invalid_args("closed_world", "a str stating why the check space is complete, or omitted", closed_world)
    if args.get("evidence_type") not in EVIDENCE_TYPES:
        return invalid_args("evidence_type", " | ".join(EVIDENCE_TYPES), args.get("evidence_type"))
    return None


def run(env, args):
    bad = validate(args)
    if bad is not None:
        return bad
    closed_world = args.get("closed_world")
    journal = Journal(env.journal_path, env.run_id)  # no I/O; constructed here so the F1 check can read it
    bad = author_refusal(args["author"], journal.read())  # F1: `author` is load-bearing for B·1 (a)
    if bad is not None:
        return bad
    try:
        text = args.get("text", args["claim_id"])
        kind, override = assign_kind(args["kind"], text, closed_world)
        ev = journal.claim_recorded(args["claim_id"], args["author"], args.get("actor", "MAIN"), kind, text,
                                    args["evidence_type"], args.get("evidence_ref", ""), args.get("framing"),
                                    kind_override=override, closed_world=closed_world if override else None)
        return ToolResult(ok=True, value=ev)
    except Exception as e:
        return internal_error(e)
