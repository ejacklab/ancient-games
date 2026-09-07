"""Tool-layer plumbing shared by the adapters, the invariants and the loop
(HYBRID_SPEC 31′): `action_id`, git helpers, journal-window helpers, and
the `tool_call` event constructor.

Ordering rule (DECISIONS.md, Hybrid): "postdates" is journal position, not
`ts` — the journal is append-only with one writer, so position is the
order it actually guarantees; `ts` has microsecond resolution and can tie.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from typing import Any

from ancient_games.ctx import ArtifactRef
from ancient_games.stages import ActionInput

from ..types import Call, ToolResult, hydrate

COMMIT_ACTION_ID_ARGS = ("commit", ["master"])


def action_id(verb: str, refs: list[str]) -> str:
    return f"{verb}:{sorted(refs)}"


def guard_action(args: dict) -> ActionInput:
    return hydrate(ActionInput, args["action"])


def guard_paths(action: ActionInput) -> list[str]:
    return [r.path for r in action.refs]


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
        return f"ok: {et}"
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


def json_safe(v: Any) -> Any:
    return json.loads(json.dumps(v, default=str))
