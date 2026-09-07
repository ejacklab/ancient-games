"""Tool-layer plumbing shared by the adapters, the invariants and the loop
(HYBRID_SPEC 31′): `action_id`, git helpers, journal-window helpers, and
the `tool_call` event constructor.

Ordering rule (DECISIONS.md, Hybrid): "postdates" is journal position, not
`ts` — the journal is append-only with one writer, so position is the
order it actually guarantees; `ts` has microsecond resolution and can tie.
"""
from __future__ import annotations

import copy
import dataclasses
import hashlib
import json
import os
import subprocess
from typing import Any

from ancient_games.ctx import ArtifactRef
from ancient_games.stages import ActionInput

from ..types import Call, ToolResult, hydrate

COMMIT_ACTION_ID_ARGS = ("commit", ["master"])


def action_id(verb: str, refs: list[str]) -> str:
    return f"{verb}:{sorted(refs)}"


ACTION_SHAPE = "a JSON object (ActionInput: {name, refs: [{path, mode, verb?, consumers?}], tripwires?, ...})"
REFS_SHAPE = "a list of JSON objects (ArtifactRef: {path, mode, verb?, consumers?})"


def guard_action(args: dict) -> ActionInput:
    """Hydrate `args["action"]`; a wrong shape is a ValueError naming the expected one (H10, ABLATION_2)
    — never an AttributeError later in an invariant or the stage."""
    action = args.get("action") if isinstance(args, dict) else None
    if not isinstance(action, dict):
        raise ValueError(f"must be {ACTION_SHAPE}, got {action!r} ({type(action).__name__})")
    out = hydrate(ActionInput, action)
    if not isinstance(out.refs, list) or not all(isinstance(r, ArtifactRef) for r in out.refs):
        raise ValueError(f"refs must be {REFS_SHAPE}, got {action.get('refs')!r} ({type(action.get('refs')).__name__})")
    if not isinstance(out.name, str):
        raise ValueError(f"name must be a str, got {out.name!r} ({type(out.name).__name__})")
    if not isinstance(out.tripwires, dict):
        raise ValueError(f"tripwires must be {{hub-name-or-matched-ref-path: command}}, got {out.tripwires!r}")
    return out


def guard_paths(action: ActionInput) -> list[str]:
    return [r.path for r in action.refs]


def guard_mutate_paths(action: ActionInput) -> list[str]:
    """The action's invoke/mutate paths — `consumer_check.ref` as `stages.guard` emits it (H9)."""
    return [r.path for r in action.refs if r.mode != "read"]


def guard_action_id(action: ActionInput) -> str:
    first = action.refs[0]
    return action_id(first.verb or first.mode, guard_paths(action))


def call_action_id(call: Call) -> str | None:
    """The computed formula (§2) for guard and commit; None for every other tool."""
    if call.tool == "commit":
        return action_id(*COMMIT_ACTION_ID_ARGS)
    if call.tool == "guard":
        try:
            return guard_action_id(guard_action(call.args))
        except Exception:
            return None
    return None


def journal_args(call: Call) -> dict:
    """JSON-safe copy of the call's args; guard additionally carries `refs-paths` (§6, I1′'s input)."""
    args = json.loads(json.dumps(call.args, default=str))
    if call.tool == "guard":
        try:
            args["refs-paths"] = guard_paths(guard_action(call.args))
        except Exception:
            pass
    return args


def args_hash(args: dict) -> str:
    return hashlib.sha256(json.dumps(args, sort_keys=True, default=str).encode()).hexdigest()[:16]


def result_summary(result: ToolResult) -> str:
    if not result.ok:
        return f"declined: {result.reason}"
    v = result.value
    et = getattr(v, "exit_type", None)
    if et is not None:
        lb = getattr(v, "lint_backend", None)  # prove: which lint backend checked the plan
        return f"ok: {et}" + (f" [lint_backend={lb}]" if lb else "")
    if isinstance(v, (str, int, float, bool)) or v is None:
        return f"ok: {v}"
    if isinstance(v, dict):
        return "ok: " + json.dumps({k: v[k] for k in v if k != "output"}, default=str)[:200]
    return f"ok: {type(v).__name__}"


def tool_call_event(call: Call, invariants_checked: list[str], result: ToolResult | None = None,
                    refused_by: str | None = None, reason: str | None = None) -> dict:
    """§6 shape. `ok` is derivable: refused_by is None and reason is None."""
    args = journal_args(call)
    if result is not None:
        summary = result_summary(result)
        exit_type = getattr(result.value, "exit_type", None) if result.ok else None
        reason = result.reason
    else:
        summary, exit_type = f"refused: {refused_by}", None
    return {"event": "tool_call", "tool": call.tool, "action_id": call_action_id(call), "args": args,
            "args_hash": args_hash(args), "result_summary": summary, "exit_type": exit_type,
            "invariants_checked": list(invariants_checked), "refused_by": refused_by, "reason": reason}


def event_ok(e: dict) -> bool:
    return e.get("event") == "tool_call" and e["refused_by"] is None and e["reason"] is None


# --- journal windows ---------------------------------------------------------
def last_commit_index(events: list[dict]) -> int:
    """Position of the most recent executed commit (non-refused, ok), or -1."""
    idx = -1
    for i, e in enumerate(events):
        if e.get("event") == "tool_call" and e["tool"] == "commit" and event_ok(e):
            idx = i
    return idx


def approvals_after(events: list[dict], gate: str, action_id_: str, after: int) -> list[dict]:
    return [e for i, e in enumerate(events) if i > after and e.get("event") == "approval_recorded"
            and e["gate"] == gate and e["action_id"] == action_id_]


def live_dispatches(events: list[dict]) -> int:
    """I5′ (DECISIONS_HYBRID_4 L3): computed from the journal, never a counter."""
    started = sum(1 for e in events if e.get("event") == "tool_call" and e["tool"] == "dispatch" and event_ok(e))
    returned = sum(1 for e in events if e.get("event") == "tool_call" and e["tool"] == "ingest_return" and event_ok(e))
    failed = sum(1 for e in events if e.get("event") == "dispatch_failed")
    return max(0, started - returned - failed)


# --- git -----------------------------------------------------------------------
def git(cwd: str, *argv: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *argv], cwd=cwd, capture_output=True, text=True)


def diff_name_only_head(cwd: str) -> list[str]:
    p = git(cwd, "diff", "--name-only", "HEAD")
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or "git diff failed")
    return [ln for ln in p.stdout.splitlines() if ln]


def untracked_files(cwd: str) -> list[str]:
    p = git(cwd, "ls-files", "--others", "--exclude-standard")
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or "git ls-files failed")
    return [ln for ln in p.stdout.splitlines() if ln]


def changed_files(cwd: str) -> list[str]:
    """I1′/I2′'s `changed` (v1.1, D-A): `git diff --name-only HEAD` ∪ untracked files not ignored."""
    seen = diff_name_only_head(cwd)
    return seen + [f for f in untracked_files(cwd) if f not in seen]


def refs_from(dicts: list[dict]) -> list[ArtifactRef]:
    return [hydrate(ArtifactRef, d) for d in dicts]


def internal_error(e: Exception) -> ToolResult:
    return ToolResult(ok=False, value=None, reason=f"internal-error: {e}")


def invalid_args(field: str, accepted: str, got: Any) -> ToolResult:
    """H2 (ABLATION_1): a bad input is the caller's error, named by field and accepted values —
    never an `internal-error`."""
    return ToolResult(ok=False, value=None,
                      reason=f"invalid-args: {field} must be {accepted}, got {got!r} ({type(got).__name__})")


def resolve_backend(args: dict) -> tuple[str | None, ToolResult | None]:
    """The §8 lint backend: `args["backend"]` when given, else `$AG_LINT_BACKEND`.

    Either being invalid is the caller's error — `invalid-args` naming the field and the
    accepted values — never a ValueError raised across the tool boundary, which `loop.step`
    does not catch (it would kill the loop and journal nothing). The environment default is
    consulted ONLY when no explicit backend was passed, so a bad `$AG_LINT_BACKEND` cannot
    reject a call that named a valid backend of its own.
    """
    from ancient_games.lints import BACKENDS, ENV_BACKEND, default_backend
    accepted = " | ".join(BACKENDS)
    got = args.get("backend") if isinstance(args, dict) else None
    if got is not None:
        return (got, None) if got in BACKENDS else (None, invalid_args("backend", accepted, got))
    try:
        return default_backend(), None
    except ValueError:
        return None, invalid_args(f"${ENV_BACKEND}", accepted, os.environ.get(ENV_BACKEND))


def require_str(args: dict, *names: str, allow_empty: bool = False) -> ToolResult | None:
    """`invalid-args` for the first required arg that is absent or not a str — checked BEFORE the
    adapter's broad try, so a missing required arg is the caller's error and not an `internal-error`
    (`invalid_args`' own contract; `cli.cmd_call` exits 2 only on an `invalid-args:` reason)."""
    for name in names:
        got = args.get(name) if isinstance(args, dict) else None
        if not isinstance(got, str) or (not got and not allow_empty):
            return invalid_args(name, "a str" if allow_empty else "a non-empty str", got)
    return None


def ctx_snapshot(ctx: Any) -> Any:
    return copy.deepcopy(ctx)


def ctx_restore(ctx: Any, snapshot: Any) -> None:
    """H7 (ABLATION_1): a stage that raised half-way must leave no partial ctx write behind —
    the loop and the CLI hold `ctx` by reference, so restore it field by field."""
    for f in dataclasses.fields(ctx):
        setattr(ctx, f.name, getattr(snapshot, f.name))


def json_safe(v: Any) -> Any:
    return json.loads(json.dumps(v, default=str))
