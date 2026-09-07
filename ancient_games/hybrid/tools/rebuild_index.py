"""NEW — wraps `ancient_games.index.rebuild(journal_path, db_path)`, decided-not-yet-built
(docs/SQLITE_INDEX_DESIGN.md): the sole `side_effects=mutate` tool, so the only one
that can stale a `prove` PASS through I2's clause (a). Declines until the index exists."""
from ..types import ToolResult
from ._shared import internal_error

MANIFEST = {
    "name": "rebuild_index", "inputs": {"db_path": "str"}, "outputs": "{rows}",
    "side_effects": "mutate", "cost": "cheap", "participates_in": [], "entrypoint": "run",
}


def run(env, args):
    try:
        try:
            from ancient_games.index import rebuild  # type: ignore[import-not-found]
        except ImportError:
            return ToolResult(ok=False, reason="index-not-built: ancient_games.index.rebuild is absent")
        return ToolResult(ok=True, value=rebuild(env.journal_path, args["db_path"]))
    except Exception as e:
        return internal_error(e)
