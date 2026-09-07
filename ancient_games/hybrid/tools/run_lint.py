"""Wraps `lints.run_all_on_plan` over the journal-reconstructed plan. `backend` selects the §8 lint
backend (`lints.BACKENDS`: python — the oracle — | sql | differential); absent, `$AG_LINT_BACKEND`
decides, defaulting to python. The value is `{"backend": ..., "findings": [...]}` so the journaled
`result_summary` names how the findings were produced."""
from ancient_games.journal import Journal
from ancient_games.lints import run_all_on_plan

from ..types import ToolResult
from ._plan import plan_from_journal
from ._shared import internal_error, resolve_backend

MANIFEST = {
    "name": "run_lint", "inputs": {"gate": "str", "gate_at": "str", "backend": "str"},
    "outputs": "{backend, findings: list[Finding]}",
    "side_effects": "read", "cost": "cheap", "participates_in": [], "entrypoint": "run",
}


def run(env, args):
    backend, bad = resolve_backend(args)
    if bad is not None:
        return bad
    try:
        events = Journal(env.journal_path, env.run_id).read()
        findings = run_all_on_plan(plan_from_journal(events, env.ctx, args, run_id=env.run_id), events,
                                   backend=backend, run_id=env.run_id)
        return ToolResult(ok=True, value={"backend": backend, "findings": findings})
    except Exception as e:
        return internal_error(e)
