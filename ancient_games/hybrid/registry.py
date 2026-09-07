"""HYBRID_SPEC §2 — tool discovery: a directory of modules, each a `MANIFEST`
dict plus one entrypoint `run(env, args) -> ToolResult`.

Discovery (R1, A2): manifests are read once at run start. A malformed
manifest (missing field, enum violation) or an entrypoint whose signature
is not exactly `(env, args)` never registers — `ManifestError`. Adding a
tool = dropping a module into a scanned directory (UC9).
"""
from __future__ import annotations

import importlib.util
import inspect
import os
from dataclasses import dataclass
from typing import Callable

from .types import ToolEnv, ToolResult

REQUIRED = ("name", "inputs", "outputs", "side_effects", "cost", "participates_in", "entrypoint")
SIDE_EFFECTS = ("none", "read", "invoke", "mutate", "commit")
COSTS = ("cheap", "agent", "suite")
INVARIANTS = ("I1", "I2", "I3", "I4", "I5")
TOOLS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools")


class ManifestError(ValueError):
    pass


@dataclass(frozen=True)
class RegisteredTool:
    name: str
    manifest: dict
    fn: Callable[[ToolEnv, dict], ToolResult]

    @property
    def side_effects(self) -> str:
        return self.manifest["side_effects"]


def validate_manifest(manifest: object, where: str = "<manifest>") -> dict:
    if not isinstance(manifest, dict):
        raise ManifestError(f"{where}: MANIFEST must be a dict")
    missing = [k for k in REQUIRED if k not in manifest]
    if missing:
        raise ManifestError(f"{where}: MANIFEST missing {missing}")
    if not isinstance(manifest["name"], str) or not manifest["name"]:
        raise ManifestError(f"{where}: name must be a non-empty str")
    if manifest["side_effects"] not in SIDE_EFFECTS:
        raise ManifestError(f"{where}: side_effects {manifest['side_effects']!r} not in {SIDE_EFFECTS}")
    if manifest["cost"] not in COSTS:
        raise ManifestError(f"{where}: cost {manifest['cost']!r} not in {COSTS}")
    if not isinstance(manifest["inputs"], dict):
        raise ManifestError(f"{where}: inputs must be a dict")
    pi = manifest["participates_in"]
    if not isinstance(pi, list) or any(i not in INVARIANTS for i in pi):
        raise ManifestError(f"{where}: participates_in must be a list drawn from {INVARIANTS}, got {pi!r}")
    if not isinstance(manifest["entrypoint"], str):
        raise ManifestError(f"{where}: entrypoint must name a module attribute")
    return manifest


def check_signature(fn: object, where: str = "<entrypoint>") -> Callable:
    """The uniform check (§2 item 2): exactly `(env, args)`, positional, no defaults, no *args/**kwargs."""
    if not callable(fn):
        raise ManifestError(f"{where}: entrypoint is not callable")
    params = list(inspect.signature(fn).parameters.values())
    ok = (len(params) == 2 and [p.name for p in params] == ["env", "args"]
          and all(p.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD and p.default is inspect.Parameter.empty
                  for p in params))
    if not ok:
        raise ManifestError(f"{where}: entrypoint signature must be exactly (env, args), got {inspect.signature(fn)}")
    return fn  # type: ignore[return-value]


def load_module(path: str):
    stem = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(f"ancient_games.hybrid.tools.{stem}", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def register(path: str) -> RegisteredTool:
    mod = load_module(path)
    manifest = validate_manifest(getattr(mod, "MANIFEST", None), path)
    fn = check_signature(getattr(mod, manifest["entrypoint"], None), f"{path}:{manifest['entrypoint']}")
    return RegisteredTool(manifest["name"], manifest, fn)


def load_tools(*dirs: str) -> dict[str, RegisteredTool]:
    """Discover every `*.py` (not `_`-prefixed) in the built-in tools dir plus `dirs`."""
    out: dict[str, RegisteredTool] = {}
    for d in (TOOLS_DIR, *dirs):
        for name in sorted(os.listdir(d)):
            if not name.endswith(".py") or name.startswith("_"):
                continue
            tool = register(os.path.join(d, name))
            if tool.name in out:
                raise ManifestError(f"duplicate tool name {tool.name!r} ({name})")
            out[tool.name] = tool
    return out
