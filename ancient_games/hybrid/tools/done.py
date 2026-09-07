"""NEW — `done`, a real executed tool running I2′'s two clauses (K8):
(a) freshness — the latest non-refused `prove` PASS postdates every non-refused
    `mutate`-side-effect tool_call (`commit` is categorically excluded);
(b) clean tree — `git diff --name-only HEAD` is empty.
Declines return ok=False with the reason; the loop journals an ordinary tool_call
and continues — `refused_by` is never populated by I2."""
from ancient_games.journal import Journal

from ..types import ToolResult
from ._shared import changed_files, internal_error

MANIFEST = {
    "name": "done", "inputs": {}, "outputs": "DONE", "side_effects": "none", "cost": "cheap",
    "participates_in": ["I2", "I3"], "entrypoint": "run",
}


def run(env, args):
    try:
        events = [e for e in Journal(env.journal_path, env.run_id).read() if e["run_id"] == env.run_id]
        proves = [i for i, e in enumerate(events) if e.get("event") == "tool_call" and e["tool"] == "prove"
                  and e["refused_by"] is None and e.get("exit_type") == "PASS"]
        if not proves:
            return ToolResult(ok=False, reason="no-prove-pass")
        latest = proves[-1]
        staling = [e for i, e in enumerate(events) if i > latest and e.get("event") == "tool_call"
                   and e["refused_by"] is None and e["tool"] in env.tools
                   and env.tools[e["tool"]].manifest["side_effects"] == "mutate"]
        if staling:
            return ToolResult(ok=False, reason=f"prove-stale: {staling[-1]['tool']}")
        changed = changed_files(env.cwd)
        if changed:
            return ToolResult(ok=False, reason=f"uncommitted-changes: {changed}")
        return ToolResult(ok=True, value="DONE")
    except Exception as e:
        return internal_error(e)
