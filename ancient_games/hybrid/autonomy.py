"""AUTONOMY_DESIGN v2 §3-§5 — the autonomy policy, as pure functions over journal events.

Three modes (`auto` | `phase` | `step`) answer one question: *what counts as a gate?*
They are expressed not as a new refusal path but as an **effective ceiling** — the
framework already owns exactly one mechanical, journal-derived, restart-proof stop, and
`cmd_call` already recomputes the used budget from the journal on every process. So a
pause is "this run's budget ends here until someone records a resume", which the existing
bound checks in `cli.cmd_call` and `loop.run` enforce unchanged.

That is why nothing here can weaken the invariant floor (§2): a mode contributes a
*budget*, never a verdict on a call. There is no branch in which it evaluates to
"proceed" — the only thing it can do is lower a number.

`scope_covers` is used by the pre-authorisation path (§5.3) and is deliberately NOT
`fnmatch`: `fnmatch`'s `*` crosses `/`, so `research/**` there matches
`research/../engine/x.py` and `research*` matches `researchx/y`.
"""
from __future__ import annotations

import posixpath
import re
from dataclasses import dataclass
from typing import Any

from .tools._shared import event_ok

MODES = ("auto", "phase", "step")
STEP_RULES: list[dict] = [{"name": "step", "tool": "*"}]
RESUME_GATE = "resume"


@dataclass(frozen=True)
class Boundary:
    """A pause point: the rule that fired, the tool-call ordinal it fired at, and whether a
    resume approval has cleared it. `ordinal` is the count of this run's `tool_call` events —
    the same number `cmd_call` computes and prints as `step`, never a journal file position."""
    name: str
    ordinal: int
    cleared: bool

    @property
    def id(self) -> str:
        return f"pause:{self.name}@{self.ordinal}"


def rules_for(autonomy: str, pause_after: list[dict] | None) -> list[dict]:
    """The pause rules a mode implies. `phase` carries its own per-task list (EJ: named per
    task); `step` is the same machinery with one wildcard rule; `auto` has none."""
    if autonomy not in MODES:
        raise ValueError(f"autonomy must be one of {MODES}, got {autonomy!r}")
    if autonomy == "auto":
        return []
    if autonomy == "step":
        return list(STEP_RULES)
    if not pause_after:
        raise ValueError("autonomy 'phase' requires a non-empty pause_after list "
                         "(there is deliberately no default: phases are named per task)")
    return list(pause_after)


def validate_rules(rules: list[dict]) -> list[dict]:
    for r in rules:
        if not isinstance(r, dict) or not isinstance(r.get("name"), str) or not r["name"]:
            raise ValueError(f"pause rule needs a non-empty str name: {r!r}")
        if not isinstance(r.get("tool"), str) or not r["tool"]:
            raise ValueError(f"pause rule {r['name']!r} needs a non-empty str tool (or \"*\")")
        if "exit_type" in r and not isinstance(r["exit_type"], str):
            raise ValueError(f"pause rule {r['name']!r}: exit_type must be a str")
        extra = set(r) - {"name", "tool", "exit_type"}
        if extra:
            raise ValueError(f"pause rule {r['name']!r} carries unknown keys {sorted(extra)}")
    return rules


def rule_matches(rule: dict, event: dict) -> bool:
    """A rule fires on a call that actually EXECUTED AND SUCCEEDED, and — when the rule names
    one — carried that `exit_type`.

    Matching on `exit_type` rather than on ok-ness is load-bearing, not a refinement:
    `tools/prove.py` returns `ok=True` unconditionally, so a failed prove is journaled
    `"ok: ...Prove: FAIL ... returned to planner"`. A rule keyed on ok-ness would hand control
    back announcing the phase complete at the exact moment prove bounced to the planner.
    """
    if event.get("event") != "tool_call" or not event_ok(event):
        return False
    if rule["tool"] != "*" and event.get("tool") != rule["tool"]:
        return False
    if "exit_type" in rule and event.get("exit_type") != rule["exit_type"]:
        return False
    return True


def boundaries(events: list[dict], rules: list[dict]) -> list[Boundary]:
    """Every pause point this run has reached, in order, each marked cleared or open.

    `events` must already be run-scoped (`Journal.read()`); passing a whole file would let one
    run's calls and another run's resume approvals be read as if they were this run's.
    """
    if not rules:
        return []
    resumed = {e["action_id"] for e in events
               if e.get("event") == "approval_recorded" and e.get("gate") == RESUME_GATE}
    out: list[Boundary] = []
    ordinal = 0
    for e in events:
        if e.get("event") != "tool_call":
            continue
        ordinal += 1
        for r in rules:
            if rule_matches(r, e):
                b = Boundary(r["name"], ordinal, False)
                out.append(Boundary(r["name"], ordinal, b.id in resumed))
                break
    return out


def open_boundary(events: list[dict], rules: list[dict]) -> Boundary | None:
    return next((b for b in boundaries(events, rules) if not b.cleared), None)


def effective_ceiling(events: list[dict], rules: list[dict], ceiling: int) -> int:
    """The budget this run may actually spend: the manifest ceiling, or — if an uncleared pause
    boundary exists — the ordinal it fired at, which is a budget already fully spent."""
    b = open_boundary(events, rules)
    return b.ordinal if b is not None else ceiling


def pause_message(b: Boundary) -> str:
    return (f"paused-at: {b.id} (autonomy boundary {b.name!r}); resume with: "
            f"python3 -m ancient_games.hybrid approve --gate resume "
            f"--action-id {b.id} --approver <you>")


# --- scope matching (§5.3) ---------------------------------------------------------------
def _seg_re(pattern: str) -> re.Pattern:
    """`*` matches within one segment, `**` matches any number of segments, `?` one character."""
    out = ["(?s:"]
    i, n = 0, len(pattern)
    while i < n:
        c = pattern[i]
        if c == "*":
            if pattern[i:i + 2] == "**":
                j = i + 2
                if pattern[j:j + 1] == "/":  # `a/**/b` must also match `a/b`
                    out.append("(?:.*/)?")
                    i = j + 1
                    continue
                out.append(".*")
                i = j
                continue
            out.append("[^/]*")
        elif c == "?":
            out.append("[^/]")
        else:
            out.append(re.escape(c))
        i += 1
    out.append(")\\Z")
    return re.compile("".join(out))


def safe_path(path: str) -> bool:
    """Reject anything that could climb out of the scope it appears to be inside: absolute
    paths, and any `..` segment. `research/../engine/x.py` is NOT inside `research/`."""
    if not path or path.startswith("/") or (len(path) > 1 and path[1] == ":"):
        return False
    return ".." not in posixpath.normpath(path).split("/") and ".." not in path.split("/")


def scope_covers(patterns: list[str], path: str) -> bool:
    if not safe_path(path):
        return False
    return any(_seg_re(p).match(path) for p in patterns)


def uncovered(patterns: list[str], paths: list[str]) -> list[str]:
    """Every path the scope does not cover. One unmatched path fails the whole commit — the
    same all-or-nothing shape as I1's exact-path rule."""
    return sorted(p for p in paths if not scope_covers(patterns, p))


# --- grants (§5.3) -----------------------------------------------------------------------
def grants(events: list[dict]) -> list[dict]:
    return [e for e in events if e.get("event") == "preauthorization_recorded"]


def uses_of(events: list[dict], grant_id: str) -> int:
    return sum(1 for e in events if e.get("event") == "approval_derived" and e.get("grant_id") == grant_id)


def live_grant(events: list[dict], changed: list[str], has_overrides: bool) -> tuple[dict | None, str]:
    """(the grant that authorises committing exactly `changed`, or None with the reason).

    Evaluated FRESH at every commit against the actual changed files, and it mints nothing:
    §5.2 — every commit shares the constant action_id ("commit", ["master"]), so a stored
    derived approval would sit in-window and clear a LATER commit its scope never covered.
    """
    reasons: list[str] = []
    for g in grants(events):
        gid = g["grant_id"]
        left = g["max_uses"] - uses_of(events, gid)
        if left <= 0:
            reasons.append(f"{gid}: max_uses exhausted ({g['max_uses']})")
            continue
        miss = uncovered(g["scope_paths"], changed)
        if miss:
            reasons.append(f"{gid}: paths outside scope {g['scope_paths']}: {miss}")
            continue
        if has_overrides and not g["allow_kind_overrides"]:
            reasons.append(f"{gid}: run carries a closed_world kind override and allow_kind_overrides is false")
            continue
        return g, ""
    return None, ("; ".join(reasons) if reasons else "")


def config_from(events: list[dict]) -> dict[str, Any]:
    """The run's `run_config`, or the `auto` default. A run with no such event is `auto`, which
    is exactly today's behaviour — and the floor is identical in every mode, so the default is
    the backward-compatible reading rather than a weakened one."""
    cfgs = [e for e in events if e.get("event") == "run_config"]
    if not cfgs:
        return {"autonomy": "auto", "pause_after": []}
    c = cfgs[0]
    return {"autonomy": c["autonomy"], "pause_after": list(c["pause_after"])}


def rules_from_events(events: list[dict]) -> list[dict]:
    c = config_from(events)
    return rules_for(c["autonomy"], c["pause_after"])
