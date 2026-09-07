"""HYBRID_SPEC §2 — the one calling convention every tool shares, plus `hydrate`.

`run(env: ToolEnv, args: dict) -> ToolResult`, no exceptions. Tools never
raise across this boundary (each adapter wraps its body in try/except).
`hydrate` (DECISIONS_HYBRID_4 L2) turns the plain-JSON `args` a case file
or a live chooser supplies into the dataclasses the wrapped stage
functions need.
"""
from __future__ import annotations

import dataclasses
import os
import typing
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ToolEnv:
    run_id: str
    journal_path: str
    ctx: Any  # the loop's own Ctx (same reference) — or the stripped view for prove/done (I3′)
    cwd: str = field(default_factory=os.getcwd)  # where git / suites run (DECISIONS.md, Hybrid)
    tools: dict = field(default_factory=dict)  # name -> RegisteredTool; read by `done` (side_effects lookup)


@dataclass(frozen=True)
class ToolResult:
    ok: bool
    value: Any = None
    reason: str | None = None


@dataclass(frozen=True)
class Call:
    """What `choose` returns: a tool name and its plain-JSON args."""

    tool: str
    args: dict = field(default_factory=dict)


def hydrate(cls: type, d: Any) -> Any:
    """JSON → dataclass, recursively (DECISIONS_HYBRID_4 L2).

    For each dataclass field of `cls`: a dataclass-typed field with a dict
    value recurses; a `list[T]` with `T` a dataclass and a list of dicts
    recurses per element; tuple-typed fields coerce lists to tuples (so
    frozen refs compare equal); everything else is assigned as-is. Missing
    keys use the field default; unknown keys raise ValueError naming them.
    """
    if not isinstance(d, dict):
        return d
    if not dataclasses.is_dataclass(cls):
        return d
    hints = typing.get_type_hints(cls)
    names = {f.name for f in dataclasses.fields(cls)}
    unknown = set(d) - names
    if unknown:
        raise ValueError(f"{cls.__name__}: unknown keys {sorted(unknown)}")
    kwargs = {}
    for f in dataclasses.fields(cls):
        if f.name not in d:
            continue
        kwargs[f.name] = _coerce(hints.get(f.name, Any), d[f.name])
    return cls(**kwargs)


def _coerce(hint: Any, value: Any) -> Any:
    origin = typing.get_origin(hint)
    args = typing.get_args(hint)
    if dataclasses.is_dataclass(hint) and isinstance(hint, type):
        return hydrate(hint, value)
    if origin in (typing.Union, getattr(__import__("types"), "UnionType", ())):
        inner = [a for a in args if a is not type(None)]
        if value is None or len(inner) != 1:
            return value
        return _coerce(inner[0], value)
    if origin is list and isinstance(value, list) and args:
        return [_coerce(args[0], v) for v in value]
    if origin is tuple and isinstance(value, list):
        return tuple(value)
    return value
