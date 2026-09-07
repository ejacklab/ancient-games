"""UC9 — a tool dropped into a scanned directory at run start: manifest + function, no loop change."""
import os

from ancient_games.hybrid.types import ToolResult

MANIFEST = {
    "name": "count_lines", "inputs": {"path": "str"}, "outputs": "{lines}",
    "side_effects": "read", "cost": "cheap", "participates_in": [], "entrypoint": "run",
}


def run(env, args):
    try:
        with open(os.path.join(env.cwd, args["path"]), encoding="utf-8") as fh:
            return ToolResult(ok=True, value={"lines": sum(1 for _ in fh)})
    except Exception as e:
        return ToolResult(ok=False, reason=f"internal-error: {e}")
