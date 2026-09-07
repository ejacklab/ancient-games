"""Wraps `trace.render_trace` (trace.py:70)."""
from ancient_games.journal import Journal
from ancient_games.trace import render_trace

from ..types import ToolResult
from ._shared import internal_error

MANIFEST = {
    "name": "render_trace", "inputs": {"title": "str"}, "outputs": "markdown str",
    "side_effects": "none", "cost": "cheap", "participates_in": [], "entrypoint": "run",
}


def run(env, args):
    try:
        events = Journal(env.journal_path, env.run_id).read()
        return ToolResult(ok=True, value=render_trace(events, args.get("title", "Run trace"), run_id=env.run_id))
    except Exception as e:
        return internal_error(e)
