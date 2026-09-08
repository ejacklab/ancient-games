"""HYBRID_SPEC §7 — the e2e case runner.

A case = (task input, expected outcome, expected invariant events), a JSON
file. `mode="scripted"` pops `tool_calls` into the loop's `choose`;
`mode="replay"` reads an existing journal and never calls the loop (UC8).
Both compare the journal against `expected_exit_lines`,
`expected_invariant_events` and `expected_final` — every figure the report
carries is read back from the journal, never from in-memory state, so a
replay and a scripted run are judged by the same code.

Case-file keys beyond §7 (DECISIONS.md, Hybrid): `fixture` (files of the
git repo the case runs in, plus `modified` working-tree edits), `native_edits`
(off-registry edits, D6, applied after a step like `injected_events`),
`extra_tool_dirs` (UC9), `expected_final.status`.
"""
from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass, field

from ancient_games.ctx import Ctx
from ancient_games.journal import Journal, read_events

from . import loop
from .registry import RegisteredTool, load_tools
from .tools._shared import event_ok, live_dispatches


@dataclass
class Report:
    case_id: str
    status: str | None  # loop status; None in replay
    events: list[dict]
    mismatches: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.mismatches


def load_case(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        case = json.load(fh)
    case["_dir"] = os.path.dirname(os.path.abspath(path))
    return case


# --- fixture repo ----------------------------------------------------------------
def setup_fixture(case: dict, root: str) -> None:
    """Materialize `case["fixture"]` as a git repo at `root`: `files` committed, `modified` left dirty."""
    fx = case.get("fixture") or {}
    os.makedirs(root, exist_ok=True)
    for rel, content in fx.get("files", {}).items():
        _write(root, rel, content)
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "cases@ancient-games.local")
    _git(root, "config", "user.name", "ancient-games cases")
    _git(root, "config", "commit.gpgsign", "false")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "--allow-empty", "-m", "fixture")
    for rel, content in fx.get("modified", {}).items():
        _write(root, rel, content)


def _write(root: str, rel: str, content: str) -> None:
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


def _git(root: str, *argv: str) -> None:
    subprocess.run(["git", *argv], cwd=root, check=True, capture_output=True, text=True)


# --- run ------------------------------------------------------------------------------
def run_case(case: dict, journal_path: str, cwd: str, tools: dict[str, RegisteredTool] | None = None) -> Report:
    if case.get("mode") == "replay":
        # `read_events`, not `Journal.read()`: a replay case judges a journal RECORDED ELSEWHERE
        # (UC8 replays UC1's, so its own case_id/run_id names no event in the file) and the whole
        # file is the subject. One of three sanctioned unscoped readers — see
        # tests/test_review_b_fixes.py::test_f8_read_events_importers_are_the_sanctioned_set.
        events = read_events(journal_path)
        return Report(case["case_id"], None, events, compare(case, events, None))
    if tools is None:
        extra = [os.path.join(case["_dir"], d) if not os.path.isabs(d) else d for d in case.get("extra_tool_dirs", [])]
        tools = load_tools(*extra)
    journal = Journal(journal_path, case.get("run_id", case["case_id"]))
    edits = case.get("native_edits", [])

    def after_step(i: int) -> None:
        for e in edits:
            if e.get("after_step") == i:
                _write(cwd, e["path"], e["content"])

    result = loop.run(tools, loop.scripted(case["tool_calls"]), journal, int(case["ceiling"]), Ctx(), cwd=cwd,
                      injected_events=case.get("injected_events", []), after_step=after_step)
    events = journal.read()
    return Report(case["case_id"], result.status, events, compare(case, events, result.status))


# --- compare ------------------------------------------------------------------------
def compare(case: dict, events: list[dict], status: str | None) -> list[str]:
    out: list[str] = []
    calls = [e for e in events if e.get("event") == "tool_call"]
    if "expected_exit_lines" in case:
        got = [e["exit_line"] for e in events if e.get("event") == "exit"]
        if got != case["expected_exit_lines"]:
            out.append(f"exit_lines: expected {case['expected_exit_lines']!r}, got {got!r}")
    for exp in case.get("expected_invariant_events", []):
        hits = [e for e in calls if e["tool"] == exp["tool"] and exp["invariant"] in e["invariants_checked"]
                and (e["refused_by"] == exp["invariant"]) == exp["refused"]]
        if not hits:
            out.append(f"invariant event missing: {exp}")
    expected_refusals = sorted((x["tool"], x["invariant"]) for x in case.get("expected_invariant_events", []) if x["refused"])
    actual_refusals = sorted({(e["tool"], e["refused_by"]) for e in calls if e["refused_by"]})
    if sorted(set(expected_refusals)) != actual_refusals:
        out.append(f"refusals: expected {sorted(set(expected_refusals))}, got {actual_refusals}")
    final = case.get("expected_final", {})
    agents = sum(1 for e in events if e.get("event") == "dispatch")
    if "agents" in final and agents != final["agents"]:
        out.append(f"agents: expected {final['agents']}, got {agents}")
    live = live_dispatches(events)
    if "live_dispatches_end" in final and live != final["live_dispatches_end"]:
        out.append(f"live_dispatches_end: expected {final['live_dispatches_end']}, got {live}")
    if "prove_exit_type" in final:
        proves = [e for e in calls if e["tool"] == "prove" and e["refused_by"] is None]
        got_p = proves[-1]["exit_type"] if proves else None
        if got_p != final["prove_exit_type"]:
            out.append(f"prove_exit_type: expected {final['prove_exit_type']}, got {got_p}")
    if "tool_outcomes" in final:
        names = {t["tool"] for t in final["tool_outcomes"]}
        got_o = [{"tool": e["tool"], "ok": event_ok(e), "reason": e["reason"]}
                 for e in calls if e["tool"] in names and e["refused_by"] is None]
        want = [{"tool": t["tool"], "ok": t["ok"], "reason": t.get("reason")} for t in final["tool_outcomes"]]
        if got_o != want:
            out.append(f"tool_outcomes: expected {want}, got {got_o}")
    if "status" in final and status is not None and status != final["status"]:
        out.append(f"status: expected {final['status']}, got {status}")
    return out
