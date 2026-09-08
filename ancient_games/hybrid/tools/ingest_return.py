"""§6: the `return` event, and its CLAIMS mirrored into the guarded writers.

Each mirrored claim is written by the tool that owns that event type — `record_claim` or
`record_check` — so the F1 author gate, the F2 field validation and D-KIND's `kind` rule apply
to a dispatched agent's report exactly as they do to MAIN's own calls, by construction rather
than by remembering. There is no second writer to keep in step.

The whole batch is validated before anything is written. The `return` event and its claims are
one unit: a bad entry half-way down the list used to leave the earlier ones and the `return`
event on disk while the call reported failure, so a retry duplicated them.
"""
from ancient_games.journal import EVIDENCE_TYPES, Journal, classify_event

from ..types import ToolResult
from . import record_check, record_claim
from ._shared import author_refusal, internal_error, invalid_args, require_str

MANIFEST = {
    "name": "ingest_return", "inputs": {"agent_id": "str", "fields": "dict", "actor": "str", "framing": "str"},
    "outputs": "list[event]", "side_effects": "none", "cost": "cheap", "participates_in": ["I5"], "entrypoint": "run",
}


def delegate(entry: dict, agent_id: str, actor: str, framing: str | None):
    """(tool, args) for one CLAIMS entry, or (None, None) when the `return` event carries it alone.

    The classification (§7 Z2′, `classify_event`) and the field mapping are the ones the journal
    mirror used, unchanged — including the `claim_id` collapse below.
    """
    if classify_event(entry) == "check_executed":
        # B·1 (c) counts only check_executed{claim_id=X, falsifies=X}, so an entry naming the claim
        # it falsifies is recorded against THAT claim, not against the entry's own id.
        return record_check, {"claim_id": entry.get("falsifies") or entry.get("claim_id"),
                              "mechanism": entry.get("mechanism", "other:unlabelled"),
                              "command": entry.get("command", entry.get("evidence_ref", "")),
                              "expected": entry.get("expected", ""), "observed": entry.get("observed", ""),
                              "pre_fix_result": entry.get("pre_fix_result"), "falsifies": entry.get("falsifies")}
    if entry.get("evidence_type") in EVIDENCE_TYPES:
        return record_claim, {"claim_id": entry.get("claim_id"), "author": agent_id, "actor": actor,
                              "kind": entry.get("kind"), "text": entry.get("text", entry.get("claim_id")),
                              "evidence_type": entry.get("evidence_type"),
                              "evidence_ref": entry.get("evidence_ref", ""),
                              "framing": entry.get("framing", framing),
                              # D-KIND reaches returns through record_claim's own rule: a helper keeps
                              # `executable` on absence text only by stating why its space is complete,
                              # and that override is then journaled, gated and disclosed like any other.
                              "closed_world": entry.get("closed_world")}
    return None, None


def plan(args, claims: list) -> tuple[list, ToolResult | None]:
    """Every write this call will make, or the first refusal — nothing is written either way."""
    out = []
    for i, entry in enumerate(claims):
        if not isinstance(entry, dict):
            return [], invalid_args(f"fields.CLAIMS[{i}]", "an object with a claim_id", entry)
        tool, targs = delegate(entry, args["agent_id"], args.get("actor", "MAIN"), args.get("framing"))
        if tool is None:
            continue  # not a mirrored event type (e.g. evidence_type "(opinion)") — the return carries it
        bad = tool.validate(targs)
        if bad is not None:
            return [], ToolResult(ok=False, reason=bad.reason.replace(
                "invalid-args: ", f"invalid-args: fields.CLAIMS[{i}].", 1))
        out.append((tool, targs))
    return out, None


def run(env, args):
    bad = require_str(args, "agent_id")  # before the try: a missing agent_id is the caller's error
    if bad is not None:
        return bad
    fields = args.get("fields") or {}
    if not isinstance(fields, dict):
        return invalid_args("fields", "a JSON object", fields)
    claims = fields.get("CLAIMS") or []
    if not isinstance(claims, list):
        return invalid_args("fields.CLAIMS", "a list of claim objects", claims)
    journal = Journal(env.journal_path, env.run_id)
    # F1: `agent_id` is the author of every mirrored claim. Checked once here, before any write.
    bad = author_refusal(args["agent_id"], journal.read())
    if bad is not None:
        return bad
    writes, bad = plan(args, claims)
    if bad is not None:
        return bad
    try:
        evs = [journal.returned(args["agent_id"], fields)]
        for tool, targs in writes:
            r = tool.run(env, targs)
            if not r.ok:
                # Unreachable for planned args: `validate` has passed, and the two journal-dependent
                # checks left in `run` cannot fail here — the author is the `agent_id` already
                # accepted above, and `delegate` always makes falsifies == claim_id, which short-
                # circuits record_check's known-ids test. Reported rather than swallowed if it ever is.
                return ToolResult(ok=False, reason=f"partial-return: {r.reason}")
            evs.append(r.value)
        return ToolResult(ok=True, value=[e["event"] for e in evs])
    except Exception as e:
        return internal_error(e)
