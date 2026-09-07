"""HYBRID_BRIEF O3/R5 — every case file under tests/cases/hybrid runs through the
runner; pass = exit lines, invariant events and expected_final all match the
journal, and live_dispatches == 0 at the end. Every figure asserted is read back
from the real journal the real tools wrote (never re-derived)."""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from ancient_games.hybrid import runner
from ancient_games.hybrid.loop import run as loop_run, scripted
from ancient_games.hybrid.registry import load_tools
from ancient_games.hybrid.tools._shared import live_dispatches
from ancient_games.journal import Journal
from ancient_games.ctx import Ctx

CASES = Path(__file__).parent / "cases" / "hybrid"
CASE_FILES = sorted(p for p in CASES.glob("*.json"))
IDS = [p.stem for p in CASE_FILES]


def _run(case_path: Path, tmp_path: Path, journal_path: str | None = None) -> runner.Report:
    case = runner.load_case(str(case_path))
    repo = str(tmp_path / f"repo-{case_path.stem}")
    runner.setup_fixture(case, repo)
    return runner.run_case(case, journal_path or str(tmp_path / f"{case_path.stem}.jsonl"), repo)


def test_twelve_cases_present():
    assert IDS == ["ADV_A", "ADV_B", "ADV_C", "UC1", "UC2", "UC3", "UC4", "UC5", "UC6", "UC7", "UC8", "UC9"]


@pytest.mark.parametrize("case_path", CASE_FILES, ids=IDS)
def test_case(case_path, tmp_path):
    if case_path.stem == "UC8":
        replay_of = json.loads(case_path.read_text())["replay_of"]
        source = _run(CASES / f"{replay_of}.json", tmp_path)
        assert source.passed, source.mismatches
        journal = str(tmp_path / f"{replay_of}.jsonl")
        report = _run(case_path, tmp_path, journal_path=journal)
        assert report.status is None  # replay never calls the loop
    else:
        report = _run(case_path, tmp_path)
    assert report.mismatches == [], report.mismatches
    assert live_dispatches(report.events) == 0
    assert all(e["run_id"] for e in report.events)


def test_uc1_zero_dispatch_and_real_commit(tmp_path):
    """R6/O4: T2 runs with zero dispatches; the commit landed for real (hash in the journal == HEAD)."""
    report = _run(CASES / "UC1.json", tmp_path)
    assert report.status == "DONE"
    calls = [e for e in report.events if e["event"] == "tool_call"]
    assert not any(e["tool"] == "dispatch" for e in calls)
    commit = next(e for e in calls if e["tool"] == "commit")
    head = os.popen(f"git -C {tmp_path / 'repo-UC1'} rev-parse HEAD").read().strip()
    assert json.loads(commit["result_summary"][len("ok: "):])["hash"] == head
    assert os.popen(f"git -C {tmp_path / 'repo-UC1'} log -1 --format=%s").read().strip() == \
        "fix research.stability import; add importability test"
    guard = next(e for e in calls if e["tool"] == "guard")
    assert guard["args"]["refs-paths"] == ["research/stability.py", "tests/test_research_importable.py"]
    assert guard["action_id"] == "mutate:['research/stability.py', 'tests/test_research_importable.py']"
    assert commit["action_id"] == "commit:['master']"


def test_uc7_suite_really_goes_red_then_green(tmp_path):
    """O6: the debug loop's run_suite results are real pytest runs on the fixture repo."""
    report = _run(CASES / "UC7.json", tmp_path)
    assert report.status == "DONE"
    suites = [e for e in report.events if e["event"] == "tool_call" and e["tool"] == "run_suite"]
    summaries = [json.loads(e["result_summary"][len("ok: "):]) for e in suites]
    assert [(s["passed"], s["failed"], s["returncode"]) for s in summaries] == [(1, 1, 1), (2, 0, 0), (2, 0, 0)]
    loc = next(e for e in report.events if e["event"] == "tool_call" and e["tool"] == "localize")
    assert loc["reason"] is None
    assert "ImportError" in loc["result_summary"] and "research/stability.py" in loc["result_summary"]
    assert "test_research_module_imports[stability]" in loc["result_summary"]


def test_uc9_tool_dropped_in_is_used_without_loop_change(tmp_path):
    report = _run(CASES / "UC9.json", tmp_path)
    cl = next(e for e in report.events if e["event"] == "tool_call" and e["tool"] == "count_lines")
    assert cl["reason"] is None and json.loads(cl["result_summary"][len("ok: "):]) == {"lines": 3}


def test_adv_a_refusal_is_journaled_with_the_invariant_id(tmp_path):
    report = _run(CASES / "ADV_A.json", tmp_path)
    refused = [e for e in report.events if e["event"] == "tool_call" and e["refused_by"]]
    assert [(e["tool"], e["refused_by"], e["reason"]) for e in refused] == [("dispatch", "I5", "live_dispatches=3, CAP=3, no slot")]
    assert refused[0]["invariants_checked"] == ["I5"]


def test_adv_c_refusal_names_the_unguarded_file(tmp_path):
    report = _run(CASES / "ADV_C.json", tmp_path)
    refused = [e for e in report.events if e["event"] == "tool_call" and e["refused_by"]]
    assert [(e["tool"], e["refused_by"], e["reason"]) for e in refused] == [("commit", "I1", "unguarded changed files: ['a.py']")]


def test_ceiling_bounds_the_loop(tmp_path):
    """R3: the iteration ceiling is the one mechanical bound."""
    case = runner.load_case(str(CASES / "UC1.json"))
    repo = str(tmp_path / "repo"); runner.setup_fixture(case, repo)
    journal = Journal(str(tmp_path / "j.jsonl"), "ceiling")
    result = loop_run(load_tools(), scripted(case["tool_calls"]), journal, ceiling=3, ctx=Ctx(), cwd=repo)
    assert result.status == "CEILING_REACHED" and len(result.steps) == 3
    assert [e["tool"] for e in journal.read() if e["event"] == "tool_call"] == ["gate", "guard", "guard"]


def test_default_plan_is_offered_and_resets_on_return_to_planner(tmp_path):
    """R3: the stage order is a suggestion in `obs`, never enforced; it resets after RETURN_TO_PLANNER."""
    case = runner.load_case(str(CASES / "UC2.json"))
    repo = str(tmp_path / "repo"); runner.setup_fixture(case, repo)
    journal = Journal(str(tmp_path / "j.jsonl"), "plan")
    seen = []
    inner = scripted(case["tool_calls"])

    def choose(obs, tools):
        seen.append(list(obs["suggested_next"]))
        return inner(obs, tools)

    loop_run(load_tools(), choose, journal, ceiling=44, ctx=Ctx(), cwd=repo,
             injected_events=case["injected_events"])
    assert seen[0] == ["gate", "guard", "corroborate", "filter_candidates", "prove"]
    assert seen[1] == ["guard", "corroborate", "filter_candidates", "prove"]  # gate consumed; dispatch (off-plan) allowed
    assert seen[13] == ["corroborate", "filter_candidates", "prove"]  # after prove RETURN_TO_PLANNER at step 12
    assert seen[17] == ["filter_candidates", "prove"]  # corroborate (head) consumed at step 16
    assert seen[18] == ["filter_candidates", "prove"]  # prove at step 17 was off-head: suggestion only, nothing popped
