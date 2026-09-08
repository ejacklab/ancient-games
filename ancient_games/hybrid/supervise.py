"""AUTONOMY_DESIGN v2 §7 — driving a run to its terminus, and gating on what it left behind.

Two pieces, deliberately separate:

`terminal_state` answers "is this run finished, and finished cleanly?" from the journal alone.
Every input is journal-derived, so it gives the same answer in a fresh process after a crash as
it did before — which is what makes an unattended run resumable rather than merely long.

`drive` is the unattended loop. It is `loop.run` with the one `[LLM]` cell moved out of process:
a chooser COMMAND is invoked with the observation on stdin and answers with one tool call on
stdout. That keeps the supervisor testable without a model (a three-line script is a valid
chooser) and makes an LLM-backed chooser just one such program.

The queue gate lives here: a run that finishes with unreviewed deferrals exits non-zero. §6 is
explicit that the queue is a record and not a gate — nothing downstream reads it — so this exit
code is the only teeth it has, and it is deliberately outside the invariant floor.
"""
from __future__ import annotations

import json
import shlex
import subprocess
from typing import Callable

from ancient_games.ctx import Ctx
from ancient_games.journal import Journal

from . import autonomy, loop
from .tools._shared import event_ok
from .types import Call

# `status`/`drive` exit codes. 0 means, and only means, "finished with nothing outstanding".
EXIT_DONE, EXIT_UNFINISHED, EXIT_PAUSED, EXIT_DEFERRED = 0, 1, 3, 4
STATE_EXIT = {"DONE": EXIT_DONE, "DONE_WITH_DEFERRALS": EXIT_DEFERRED, "PAUSED": EXIT_PAUSED,
              "CEILING_REACHED": EXIT_UNFINISHED, "RUNNING": EXIT_UNFINISHED, "NO_CHOICE": EXIT_UNFINISHED}


def deferrals(events: list[dict]) -> list[dict]:
    return [e for e in events if e.get("event") == "deferred_decision"]


def spent(events: list[dict]) -> int:
    return sum(1 for e in events if e.get("event") == "tool_call")


def terminal_state(events: list[dict], rules: list[dict], ceiling: int) -> dict:
    """The run's state, computed from the journal only.

    Order matters: a finished run is reported as finished even if its last call also tripped a
    pause boundary, because a boundary after `done` has nothing left to gate. DONE_WITH_DEFERRALS
    outranks DONE so an unattended run cannot end silently with disclosures nobody read.
    """
    if any(e.get("event") == "tool_call" and e["tool"] == "done" and event_ok(e) for e in events):
        q = deferrals(events)
        if q:
            return {"state": "DONE_WITH_DEFERRALS", "deferred": len(q),
                    "detail": f"{len(q)} deferred decision(s) nobody reviewed; list them with `queue`"}
        return {"state": "DONE", "deferred": 0, "detail": "done"}
    b = autonomy.open_boundary(events, rules)
    if b is not None:
        return {"state": "PAUSED", "deferred": len(deferrals(events)), "paused_at": b.id,
                "detail": autonomy.pause_message(b)}
    used = spent(events)
    if used >= autonomy.effective_ceiling(events, rules, ceiling):
        return {"state": "CEILING_REACHED", "deferred": len(deferrals(events)),
                "detail": f"{used} tool calls >= ceiling {ceiling}"}
    return {"state": "RUNNING", "deferred": len(deferrals(events)),
            "detail": f"{used}/{ceiling} tool calls spent"}


def default_plan_from(events: list[dict]) -> list[str]:
    """`loop.run`'s `default_plan` rebuilt from the journal — the one piece of a run's state that
    does not live there (§7). Replays the loop's own rule: a `prove` that returned to the planner
    resets to REPLAN, otherwise an EXECUTED call matching the head pops it. `loop.py` pops on
    execution, ok or declined, so this does too."""
    plan = list(loop.DEFAULT_PLAN)
    for e in events:
        if e.get("event") != "tool_call" or e.get("refused_by") is not None:
            continue
        if e["tool"] == "prove" and e.get("exit_type") == "RETURN_TO_PLANNER":
            plan = list(loop.REPLAN)
        elif plan and e["tool"] == plan[0]:
            plan.pop(0)
    return plan


def command_chooser(command: str) -> Callable[[dict, dict], Call | None]:
    """A chooser backed by an external program: observation JSON on stdin, one
    `{"tool": ..., "args": {...}}` object on stdout. Anything falsy (empty output, `null`, `{}`)
    means "no choice", which ends the run rather than guessing one."""
    argv = shlex.split(command)

    def choose(obs: dict, tools: dict) -> Call | None:
        p = subprocess.run(argv, input=json.dumps(obs), capture_output=True, text=True)
        if p.returncode != 0:
            raise RuntimeError(f"chooser exited {p.returncode}: {p.stderr.strip()[:400]}")
        out = p.stdout.strip()
        if not out:
            return None
        spec = json.loads(out)
        if not spec or not spec.get("tool"):
            return None
        return Call(spec["tool"], spec.get("args") or {})

    return choose


def drive(tools: dict, choose: Callable[[dict, dict], Call | None], journal: Journal, ceiling: int,
          ctx: Ctx, cwd: str, save_ctx: Callable[[Ctx], None] | None = None,
          max_calls: int | None = None) -> dict:
    """Run until a terminus, re-deriving the state from the journal every iteration.

    `max_calls` bounds THIS invocation only (so a supervisor can checkpoint); the run's own
    budget is `ceiling`, and reaching the max is not a terminus — the state stays RUNNING and a
    later invocation continues from the same journal.
    """
    calls = 0
    while True:
        events = journal.read()
        rules = autonomy.rules_from_events(events)
        state = terminal_state(events, rules, ceiling)
        if state["state"] != "RUNNING":
            return state
        if max_calls is not None and calls >= max_calls:
            return dict(state, detail=f"{state['detail']}; stopped after {calls} call(s) this invocation")
        obs = {"ctx": ctx.as_dict(), "events": events, "suggested_next": default_plan_from(events),
               # A journal records result SUMMARIES, not return values, so a resumed run cannot
               # rebuild them. `scripted`'s {"$from": ...} therefore does not work under `drive`;
               # an external chooser reads the journal, which is the durable record.
               "last_results": {}}
        call = choose(obs, tools)
        if call is None:
            return {"state": "NO_CHOICE", "deferred": len(deferrals(events)),
                    "detail": "the chooser returned no call"}
        before = spent(events)
        loop.step(tools, call, journal, ctx, before, cwd=cwd, events=events)
        # Liveness: every `loop.step` journals a tool_call, refused or not, so the budget must
        # advance. If it ever does not, this loop's terminus is unreachable — fail loudly rather
        # than spin. (A sabotage that stopped `drive` re-reading the journal hung the suite
        # instead of failing it; this converts that class into a diagnosable error.)
        if spent(journal.read()) <= before:
            raise RuntimeError(f"drive made no progress at call {before}: {call.tool!r} journaled nothing")
        calls += 1
        if save_ctx is not None:
            save_ctx(ctx)


def as_json(state: dict) -> str:
    return json.dumps(state, indent=2, sort_keys=True)


__all__ = ["EXIT_DONE", "EXIT_UNFINISHED", "EXIT_PAUSED", "EXIT_DEFERRED", "STATE_EXIT",
           "terminal_state", "default_plan_from", "command_chooser", "drive", "deferrals", "spent", "as_json"]
