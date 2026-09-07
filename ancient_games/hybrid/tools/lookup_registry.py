"""Wraps `registry.lookup` (registry.py:159)."""
from ancient_games.registry import lookup

from ..types import ToolResult
from ._shared import internal_error, refs_from

MANIFEST = {
    "name": "lookup_registry", "inputs": {"refs": "list[ArtifactRef]"}, "outputs": "Lookup",
    "side_effects": "read", "cost": "cheap", "participates_in": [], "entrypoint": "run",
}


def run(env, args):
    try:
        return ToolResult(ok=True, value=lookup(refs_from(args["refs"])))
    except Exception as e:
        return internal_error(e)
