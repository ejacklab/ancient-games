"""§7 — the trace journal: append-only JSONL at an absolute path, one writer.

Seven event types, each with the typed fields §7 states inline (X6). A
write with a missing or mistyped field raises ValueError before anything
touches the file.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from typing import Any, TypedDict

from .ctx import MECHANISMS


class ExitEvent(TypedDict):
    ts: str
    run_id: str
    event: str
    algorithm: str
    steps_fired: list[str]
    exit_type: str
    exit_line: str
    ctx_keys_set: list[str]


class DispatchEvent(TypedDict):
    ts: str
    run_id: str
    event: str
    agent_id: str
    role: str
    framing: str
    payload_fields: list[str]
    output_path: str


class ReturnEvent(TypedDict):
    ts: str
    run_id: str
    event: str
    agent_id: str
    fields: dict


class RuleFireEvent(TypedDict):
    ts: str
    run_id: str
    event: str
    rule_id: str
    algorithm_step: str
    field: str
    ctx_value: Any


class CheckExecutedEvent(TypedDict):
    ts: str
    run_id: str
    event: str
    claim_id: str
    falsifies: str
    mechanism: str
    command: str
    expected: str | int | float
    observed: str | int | float
    pre_fix_result: str | None


class ClaimRecordedEvent(TypedDict):
    ts: str
    run_id: str
    event: str
    claim_id: str
    author: str
    actor: str  # "MAIN" | agent id | "none" (Z3′)
    kind: str
    text: str
    evidence_type: str
    evidence_ref: str
    framing: str | None


class ConsumerCheckEvent(TypedDict):
    ts: str
    run_id: str
    event: str
    ref: list[str]
    answer: str
    command_or_reasoning: str


_ANY = object()
_NUM_OR_STR = (str, int, float)

# event -> {field: accepted types (or _ANY)}; ts/run_id/event are common.
SHAPES: dict[str, dict[str, Any]] = {
    "exit": {"algorithm": str, "steps_fired": list, "exit_type": str, "exit_line": str, "ctx_keys_set": list},
    "dispatch": {"agent_id": str, "role": str, "framing": str, "payload_fields": list, "output_path": str},
    "return": {"agent_id": str, "fields": dict},
    "rule_fire": {"rule_id": str, "algorithm_step": str, "field": str, "ctx_value": _ANY},
    "check_executed": {
        "claim_id": str, "falsifies": str, "mechanism": str, "command": str, "expected": _NUM_OR_STR,
        "observed": _NUM_OR_STR, "pre_fix_result": (str, type(None)),
    },
    "claim_recorded": {
        "claim_id": str, "author": str, "actor": str, "kind": str, "text": str, "evidence_type": str,
        "evidence_ref": str, "framing": (str, type(None)),
    },
    "consumer_check": {"ref": list, "answer": str, "command_or_reasoning": str},
    # hybrid tool layer (HYBRID_SPEC §6): one event per tool call, plus the two orchestrator-written events
    "tool_call": {
        "tool": str, "action_id": (str, type(None)), "args": dict, "args_hash": str, "result_summary": str,
        "exit_type": (str, type(None)), "invariants_checked": list, "refused_by": (str, type(None)),
        "reason": (str, type(None)),
    },
    "approval_recorded": {"action_id": str, "gate": str, "approver": str, "note": str},
    "dispatch_failed": {"agent_id": str, "reason": str},
}
_ENUMS: dict[tuple[str, str], tuple[Any, ...]] = {
    ("check_executed", "pre_fix_result"): ("FAIL", None),
    ("claim_recorded", "kind"): ("executable", "judgment"),
    ("claim_recorded", "evidence_type"): ("command", "file:line"),
    ("tool_call", "refused_by"): ("I1", "I4", "I5", None),  # I2/I3 never populate this (HYBRID_SPEC §4)
    ("approval_recorded", "gate"): ("checkpoint", "owner"),
}


def validate_event(event: dict) -> dict:
    """Return the event if it has exactly the typed fields §7 states; else ValueError."""
    if not isinstance(event, dict):
        raise ValueError("event must be a dict")
    for common in ("ts", "run_id", "event"):
        if common not in event or not isinstance(event[common], str):
            raise ValueError(f"event missing typed field {common!r}")
    shape = SHAPES.get(event["event"])
    if shape is None:
        raise ValueError(f"unknown event type {event['event']!r}")
    for name, typ in shape.items():
        if name not in event:
            raise ValueError(f"{event['event']} event missing typed field {name!r}")
        if typ is _ANY:
            continue
        if not isinstance(event[name], typ):
            raise ValueError(f"{event['event']}.{name} must be {typ}, got {type(event[name]).__name__}")
        enum = _ENUMS.get((event["event"], name))
        if enum is not None and event[name] not in enum:
            raise ValueError(f"{event['event']}.{name} must be one of {enum}, got {event[name]!r}")
    if event["event"] == "check_executed":
        m = event["mechanism"]
        if m not in MECHANISMS and not (m.startswith("other:") and len(m) > 6):
            raise ValueError(f"check_executed.mechanism must be one of {MECHANISMS} or other:<name>, got {m!r}")
    if event["event"] == "consumer_check" and not all(isinstance(r, str) for r in event["ref"]):
        raise ValueError("consumer_check.ref must be a list of str")
    extra = set(event) - set(shape) - {"ts", "run_id", "event"}
    if extra:
        raise ValueError(f"{event['event']} event carries undeclared fields {sorted(extra)}")
    return event


def classify_event(evidence: dict) -> str:
    """§7 (Z2′): a piece of evidence is a `check_executed` event iff it names an
    explicit expected value or falsifying condition the observed result could
    have failed to match; a bare citation of a command's output is a
    `claim_recorded` event even when MAIN ran the command."""
    expected = evidence.get("expected")
    stated = expected not in (None, "") or evidence.get("pre_fix_result") == "FAIL" or bool(evidence.get("falsifies"))
    return "check_executed" if stated else "claim_recorded"


def _check_absolute(path: str) -> str:
    if not isinstance(path, str) or not os.path.isabs(path):
        raise ValueError(f"journal path must be absolute, got {path!r}")
    return path


@dataclass
class Journal:
    """The one writer. `path` must be absolute — never derived from cwd or __file__."""

    path: str
    run_id: str = "run"
    _count: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        _check_absolute(self.path)

    def append(self, event: dict) -> dict:
        ev = dict(event)
        ev.setdefault("run_id", self.run_id)
        ev.setdefault("ts", _now())
        validate_event(ev)
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(ev, sort_keys=True) + "\n")
        self._count += 1
        return ev

    def read(self) -> list[dict]:
        return read_events(self.path)

    # --- convenience constructors, one per §7 shape -------------------------
    def exit(self, algorithm: str, steps_fired: list[str], exit_type: str, exit_line: str,
             ctx_keys_set: list[str]) -> dict:
        return self.append({"event": "exit", "algorithm": algorithm, "steps_fired": list(steps_fired),
                            "exit_type": exit_type, "exit_line": exit_line, "ctx_keys_set": list(ctx_keys_set)})

    def dispatch(self, agent_id: str, role: str, framing: str, payload_fields: list[str], output_path: str) -> dict:
        return self.append({"event": "dispatch", "agent_id": agent_id, "role": role, "framing": framing,
                            "payload_fields": list(payload_fields), "output_path": output_path})

    def check_executed(self, claim_id: str, mechanism: str, command: str, expected, observed,
                       pre_fix_result: str | None = None, falsifies: str | None = None) -> dict:
        return self.append({"event": "check_executed", "claim_id": claim_id, "falsifies": falsifies or claim_id,
                            "mechanism": mechanism, "command": command, "expected": expected, "observed": observed,
                            "pre_fix_result": pre_fix_result})

    def claim_recorded(self, claim_id: str, author: str, actor: str, kind: str, text: str, evidence_type: str,
                       evidence_ref: str, framing: str | None = None) -> dict:
        return self.append({"event": "claim_recorded", "claim_id": claim_id, "author": author, "actor": actor,
                            "kind": kind, "text": text, "evidence_type": evidence_type, "evidence_ref": evidence_ref,
                            "framing": framing})

    def consumer_check(self, ref: list[str], answer: str, command_or_reasoning: str) -> dict:
        return self.append({"event": "consumer_check", "ref": list(ref), "answer": answer,
                            "command_or_reasoning": command_or_reasoning})

    def ingest_return(self, agent_id: str, fields: dict, actor: str, framing: str | None = None) -> list[dict]:
        """§6: record the `return` event and mirror each CLAIMS entry into the
        event `classify_event` (§7, Z2′) picks — classification happens here,
        at write time, so B·1 only ever reads already-classified events."""
        out = [self.append({"event": "return", "agent_id": agent_id, "fields": fields})]
        for c in fields.get("CLAIMS", []) or []:
            if classify_event(c) == "check_executed":
                out.append(self.check_executed(c.get("falsifies") or c["claim_id"], c.get("mechanism", "other:unlabelled"),
                                               c.get("command", c.get("evidence_ref", "")), c.get("expected", ""),
                                               c.get("observed", ""), c.get("pre_fix_result"), c.get("falsifies")))
            elif c.get("evidence_type") in ("command", "file:line"):
                out.append(self.claim_recorded(c["claim_id"], agent_id, actor, c["kind"], c.get("text", c["claim_id"]),
                                               c["evidence_type"], c.get("evidence_ref", ""),
                                               c.get("framing", framing)))
        return out


def read_events(path: str) -> list[dict]:
    _check_absolute(path)
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(validate_event(json.loads(line)))
    return out


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()) + f".{int((time.time() % 1) * 1e6):06d}Z"
