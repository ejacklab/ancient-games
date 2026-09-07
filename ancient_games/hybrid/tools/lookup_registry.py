"""Wraps `registry.lookup` (registry.py:159)."""
from ancient_games.registry import lookup

from ..types import ToolResult
from ._shared import REFS_SHAPE, internal_error, invalid_args, refs_from

MANIFEST = {
    "name": "lookup_registry", "inputs": {"refs": "list[ArtifactRef]"}, "outputs": "Lookup",
    "side_effects": "read", "cost": "cheap", "participates_in": [], "entrypoint": "run",
}


def run(env, args):
    refs = args.get("refs")
    if not isinstance(refs, list) or not all(isinstance(r, dict) for r in refs):  # H10
        return invalid_args("refs", REFS_SHAPE, refs)
    try:
        return ToolResult(ok=True, value=lookup(refs_from(refs)))
    except (ValueError, TypeError) as e:
        return ToolResult(ok=False, reason=f"invalid-args: refs: {e}")
    except Exception as e:
        return internal_error(e)
