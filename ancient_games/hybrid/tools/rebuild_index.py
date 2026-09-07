"""NEW — wraps `ancient_games.index.rebuild(journal_path, db_path)`, decided-not-yet-built
(docs/SQLITE_INDEX_DESIGN.md): the sole `side_effects=mutate` tool, so the only one
that can stale a `prove` PASS through I2's clause (a). Built (docs/STORE_DESIGN_DECISION.md):
rebuilds the SQLite read index from the run's journal; `db_path` must be absolute (H2: a
relative one is the caller's error, declined as `invalid-args`)."""
import os

from ..types import ToolResult
from ._shared import internal_error, invalid_args

MANIFEST = {
    "name": "rebuild_index", "inputs": {"db_path": "str"}, "outputs": "{rows}",
    "side_effects": "mutate", "cost": "cheap", "participates_in": [], "entrypoint": "run",
}


def run(env, args):
    db_path = args.get("db_path") if isinstance(args, dict) else None
    if not isinstance(db_path, str) or not os.path.isabs(db_path):
        return invalid_args("db_path", "an absolute path (str)", db_path)
    try:
        from ancient_games.index import rebuild

        return ToolResult(ok=True, value=rebuild(env.journal_path, db_path))
    except Exception as e:
        return internal_error(e)
