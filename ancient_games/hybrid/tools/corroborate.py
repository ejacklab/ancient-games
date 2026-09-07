"""B — wraps `stages.corroborate` (R7); I3's sole producer, ordinary ctx access."""
from ancient_games.ctx import CLAIM_KINDS
from ancient_games.journal import Journal
from ancient_games.stages import Claim, corroborate as _corroborate

from ..types import ToolResult, hydrate
from ._shared import ctx_restore, ctx_snapshot, internal_error, invalid_args

MANIFEST = {
    "name": "corroborate",
    "inputs": {"action": "str", "claims": "list[Claim]", "framings": "dict[str, list[str]]", "reconciliation": "str", "dominance": "str"},
    "outputs": "CorroborateExit", "side_effects": "read", "cost": "cheap", "participates_in": ["I3"], "entrypoint": "run",
}


def _validate(args: dict) -> ToolResult | None:
    """H2 (ABLATION_1): shape and enum checks before the stage runs; None when the args are sound."""
    if not isinstance(args.get("action"), str):
        return invalid_args("action", "the action name (str)", args.get("action"))
    claims = args.get("claims")
    if not isinstance(claims, list):
        return invalid_args("claims", "a list of {claim_id, kind}", claims)
    for i, c in enumerate(claims):
        if not isinstance(c, dict) or not isinstance(c.get("claim_id"), str):
            return invalid_args(f"claims[{i}]", "an object with a str claim_id", c)
        if c.get("kind") not in CLAIM_KINDS:
            return invalid_args(f"claims[{i}].kind", "one of " + "|".join(CLAIM_KINDS), c.get("kind"))
    framings = args.get("framings")
    if framings is not None:
        if not isinstance(framings, dict):
            return invalid_args("framings", "{claim_id: [framing, ...]}", framings)
        for k, v in framings.items():
            if not isinstance(v, list) or not all(isinstance(f, str) for f in v):
                return invalid_args(f"framings[{k!r}]", "a list of framing names (str)", v)
    for name in ("reconciliation", "dominance"):
        if name in args and args[name] is not None and not isinstance(args[name], str):
            return invalid_args(name, "a str or null", args[name])
    return None


def recorded_kinds(events: list[dict], run_id: str) -> dict[str, str]:
    """claim_id -> the kind its latest `claim_recorded` event in this run carries (D-KIND: assigned by
    `record_claim`'s rule, so `corroborate` cannot be handed a cheaper kind than the one recorded)."""
    out: dict[str, str] = {}
    for e in events:
        if e.get("event") == "claim_recorded" and e.get("run_id") == run_id:
            out[e["claim_id"]] = e["kind"]
    return out


def run(env, args):
    bad = _validate(args)
    if bad is not None:
        return bad
    try:
        journal = Journal(env.journal_path, env.run_id)
        kinds = recorded_kinds(journal.read(), env.run_id)
        for i, c in enumerate(args["claims"]):
            rk = kinds.get(c["claim_id"])
            if rk is not None and c["kind"] != rk:
                return invalid_args(f"claims[{i}].kind", f"the recorded kind {rk!r} for {c['claim_id']} (assigned by rule at "
                                    "record_claim — D-KIND; an executable override needs `closed_world` there)", c["kind"])
        claims = [hydrate(Claim, c) for c in args["claims"]]
    except (ValueError, TypeError) as e:
        return ToolResult(ok=False, reason=f"invalid-args: claims: {e}")
    snapshot = ctx_snapshot(env.ctx)
    try:
        result = _corroborate(env.ctx, claims, journal, args["action"], args.get("framings"),
                              args.get("reconciliation", "agree"), args.get("dominance"))
        return ToolResult(ok=True, value=result)
    except ValueError as e:  # the stage's own precondition (e.g. no ctx.actor entry for the action)
        ctx_restore(env.ctx, snapshot)
        return ToolResult(ok=False, reason=str(e))
    except Exception as e:
        ctx_restore(env.ctx, snapshot)
        return internal_error(e)
