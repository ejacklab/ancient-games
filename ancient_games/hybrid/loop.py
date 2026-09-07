"""HYBRID_SPEC §5 — the main-agent loop: observe → choose → check → execute → journal.

`choose(obs, tools) -> Call | None` is the one `[LLM]` cell — a callback.
The stage order C→D→B→E→A is the default plan, offered in `obs` as
`suggested_next` and never enforced. `ceiling` is the one mechanical bound.
`injected_events` are the orchestrator-written events (`approval_recorded`,
`dispatch_failed`) a scripted case supplies, appended after the named step.
"""
from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import Callable, Iterable

from ancient_games.ctx import Ctx
from ancient_games.journal import Journal
from ancient_games.registry import REGISTRY, Row

from .invariants import RESTRICTED, check_invariants, invariants_for, pick_by_priority
from .registry import RegisteredTool
from .tools._shared import tool_call_event
from .types import Call, ToolEnv, ToolResult

DEFAULT_PLAN = ("gate", "guard", "corroborate", "filter_candidates", "prove")
REPLAN = ("corroborate", "filter_candidates", "prove")


@dataclass
class Step:
    index: int
    call: Call
    result: ToolResult | None  # None when refused before execution
    refused_by: str | None = None


@dataclass
class RunResult:
    ctx: Ctx
    status: str  # DONE | CEILING_REACHED | NO_CHOICE
    steps: list[Step] = field(default_factory=list)


def strip_corroboration(ctx: Ctx) -> Ctx:
    """I3′ (DECISIONS_HYBRID_4 L1): still a Ctx, the four corroboration fields None."""
    return dataclasses.replace(ctx, n_sources=None, corroboration_capped=None, framing=None, siblings=None)


def run(tools: dict[str, RegisteredTool], choose: Callable[[dict, dict], Call | None], journal: Journal,
        ceiling: int, ctx: Ctx | None = None, registry: list[Row] = REGISTRY, cwd: str = ".",
        injected_events: Iterable[dict] = (), after_step: Callable[[int], None] | None = None) -> RunResult:
    ctx = ctx if ctx is not None else Ctx()
    injected = list(injected_events)
    default_plan = list(DEFAULT_PLAN)
    last_results: dict[str, object] = {}
    out = RunResult(ctx, "CEILING_REACHED")
    for i in range(ceiling):
        obs = {"ctx": ctx.as_dict(), "events": journal.read(), "suggested_next": list(default_plan),
               "last_results": dict(last_results)}
        call = choose(obs, tools)
        if call is None:
            out.status = "NO_CHOICE"
            return out
        checked = invariants_for(call)
        if call.tool not in tools:
            result = ToolResult(ok=False, reason=f"unknown-tool: {call.tool}")
            journal.append(tool_call_event(call, checked, result))
            out.steps.append(Step(i, call, result))
            _after(i, injected, journal, after_step)
            continue
        refusals = check_invariants(call, ctx, obs["events"], tools, registry, cwd)
        if refusals:
            r = pick_by_priority(refusals)
            journal.append(tool_call_event(call, checked, refused_by=r.invariant, reason=r.reason))
            out.steps.append(Step(i, call, None, r.invariant))
            _after(i, injected, journal, after_step)
            continue
        ctx_for_call = strip_corroboration(ctx) if call.tool in RESTRICTED else ctx
        env = ToolEnv(run_id=journal.run_id, journal_path=journal.path, ctx=ctx_for_call, cwd=cwd, tools=tools)
        result = tools[call.tool].fn(env, call.args)
        journal.append(tool_call_event(call, checked, result))
        out.steps.append(Step(i, call, result))
        if result.ok:
            last_results[call.tool] = result.value
        _after(i, injected, journal, after_step)
        if call.tool == "done" and result.ok:
            out.status = "DONE"
            return out
        if call.tool == "prove" and getattr(result.value, "exit_type", None) == "RETURN_TO_PLANNER":
            default_plan = list(REPLAN)
        elif default_plan and call.tool == default_plan[0]:
            default_plan.pop(0)
    return out


def _after(i: int, injected: list[dict], journal: Journal, after_step) -> None:
    for inj in injected:
        if inj.get("after_step") == i:
            journal.append(dict(inj["event"]))
    if after_step is not None:
        after_step(i)


def scripted(tool_calls: list[dict]) -> Callable[[dict, dict], Call | None]:
    """`mode="scripted"`: pop `tool_calls` in order, ignoring `obs` — except that an
    arg of the form {"$from": <tool>, "field": <key>} is resolved from the latest
    successful result of that tool (UC7's localize reads run_suite's output)."""
    queue = list(tool_calls)

    def choose(obs: dict, tools: dict) -> Call | None:
        if not queue:
            return None
        spec = queue.pop(0)
        return Call(spec["tool"], _resolve(spec.get("args", {}), obs.get("last_results", {})))

    return choose


def _resolve(args, last_results: dict):
    if isinstance(args, dict):
        if "$from" in args:
            src = last_results.get(args["$from"])
            key = args.get("field")
            if src is None:
                return None
            return src[key] if key is not None and isinstance(src, dict) else src
        return {k: _resolve(v, last_results) for k, v in args.items()}
    if isinstance(args, list):
        return [_resolve(v, last_results) for v in args]
    return args
