"""HYBRID_SPEC §9 — the ablation harness: the CLI is the loop's own `step`, one process per
call; the scorer answers Q1–Q4 from the journal alone. Every assertion reads real return values
(exit codes, printed JSON, the journal on disk, git HEAD) — nothing is re-derived."""
from __future__ import annotations

import dataclasses
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from ablation import fixtures, score
from ancient_games.ctx import ArtifactRef, Ctx
from ancient_games.hybrid import runner
from ancient_games.hybrid.cli import load_ctx, save_ctx, tools_table
from ancient_games.hybrid.registry import load_tools
from ancient_games.hybrid.cli import default_ceiling
from ancient_games.journal import Journal, read_events

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "tests" / "cases" / "hybrid"


def cli(manifest: str | None, *argv: str) -> tuple[int, dict | str, str]:
    cmd = [sys.executable, "-m", "ancient_games.hybrid"] + (["--manifest", manifest] if manifest else []) + list(argv)
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    try:
        out = json.loads(p.stdout)
    except json.JSONDecodeError:
        out = p.stdout
    return p.returncode, out, p.stderr


def git(repo: str, *argv: str) -> str:
    return subprocess.run(["git", *argv], cwd=repo, capture_output=True, text=True, check=True).stdout.strip()


# --- CLI round-trip ----------------------------------------------------------------------
def test_cli_round_trip_init_gate_guard_refused_commit_approve_commit(tmp_path):
    repo = fixtures.make_uc1(str(tmp_path / "repo"))
    journal = str(tmp_path / "j.jsonl")
    rc, out, err = cli(None, "init", "--run-id", "rt", "--journal", journal, "--cwd", repo)
    assert rc == 0, err
    manifest = out["manifest"]
    assert os.path.exists(manifest) and out["ceiling"] == default_ceiling() >= 92 and out["run_id"] == "rt"  # H13

    rc, out, _ = cli(manifest, "call", "gate", json.dumps({
        "name": "fix import", "stop_criterion": "import-succeeds", "difficulty": "LOW", "capability": [],
        "probe": {"path": "research/stability.py", "mode": "read"}}))
    assert rc == 0 and out["ok"] is True and out["refused_by"] is None and out["step"] == 0
    assert out["value"]["exit_line"] == "Gate: plan needed, N=0, execution_status=main_executes, stop=import-succeeds."
    assert load_ctx(json.load(open(manifest))["ctx_path"]).stop_criterion == "import-succeeds"  # ctx persisted

    (Path(repo) / "research" / "stability.py").write_text("from research.walkforward import _WF_GRID\n")
    rc, out, _ = cli(manifest, "call", "commit", '{"message": "x"}')
    assert rc == 2 and out["refused_by"] == "I1" and out["reason"] == "unguarded changed files: ['research/stability.py']"
    assert out["ok"] is False and out["value"] is None

    rc, out, _ = cli(manifest, "call", "guard", json.dumps({"action": {"name": "edit",
        "refs": [{"path": "research/stability.py", "mode": "mutate"}]}}))
    assert rc == 0 and out["ok"] and out["value"]["exit_line"] == "Guard: edit stakes=1, no hub."
    rc, out, _ = cli(manifest, "call", "guard", json.dumps({"action": {"name": "commit-to-master",
        "refs": [{"path": "master", "mode": "mutate", "verb": "commit"}],
        "tripwires": {"default-branch-history": "git diff --stat"}}}))
    assert rc == 0 and out["value"]["gate"] == "checkpoint"

    rc, out, _ = cli(manifest, "call", "commit", '{"message": "x"}')
    assert rc == 0 and out["ok"] is False and out["reason"] == "checkpoint-not-cleared" and out["refused_by"] is None

    rc, out, _ = cli(manifest, "approve", "--gate", "checkpoint", "--action-id", "commit:['master']", "--approver", "ej")
    assert rc == 0 and out["event"] == "approval_recorded" and out["run_id"] == "rt"

    rc, out, _ = cli(manifest, "call", "commit", '{"message": "fix import"}')
    assert rc == 0 and out["ok"] is True
    assert out["value"]["hash"] == git(repo, "rev-parse", "HEAD") and git(repo, "log", "-1", "--format=%s") == "fix import"

    events = read_events(journal)
    calls = [e for e in events if e["event"] == "tool_call"]
    assert [(e["tool"], e["refused_by"], e["reason"]) for e in calls] == [
        ("gate", None, None), ("commit", "I1", "unguarded changed files: ['research/stability.py']"),
        ("guard", None, None), ("guard", None, None), ("commit", None, "checkpoint-not-cleared"), ("commit", None, None)]
    assert calls[1]["invariants_checked"] == ["I1", "I4"] and calls[2]["args"]["refs-paths"] == ["research/stability.py"]
    assert [e["event"] for e in events].count("approval_recorded") == 1
    assert all(e["run_id"] == "rt" for e in events)


def test_cli_exit_codes_and_orchestrator_events(tmp_path):
    repo = fixtures.make_uc3(str(tmp_path / "repo"))
    journal = str(tmp_path / "j.jsonl")
    rc, out, _ = cli(None, "init", "--run-id", "x", "--journal", journal, "--cwd", repo, "--ceiling", "2")
    manifest = out["manifest"]
    rc, out, err = cli(manifest, "call", "gate", "not json")
    assert rc == 1 and "args must be JSON" in err
    rc, out, _ = cli(manifest, "call", "bogus", "{}")
    assert rc == 1 and out["reason"] == "unknown-tool: bogus"  # journaled as the loop journals it
    rc, out, _ = cli(manifest, "fail-dispatch", "--agent-id", "historian", "--reason", "timeout")
    assert rc == 0 and out["event"] == "dispatch_failed" and out["agent_id"] == "historian"
    rc, out, _ = cli(manifest, "call", "read_journal", "{}")
    assert rc == 0 and out["ok"] and [e["event"] for e in out["value"]] == ["tool_call", "dispatch_failed"]
    rc, out, err = cli(manifest, "call", "read_journal", "{}")
    assert rc == 1 and "ceiling reached: 2" in err
    rc, out, err = cli(None, "call", "gate", "{}")
    assert rc == 1 and "no run manifest" in err
    rc, out, err = cli(None, "init", "--run-id", "x", "--journal", "rel.jsonl", "--cwd", repo)
    assert rc == 1 and "must be absolute" in err


def test_tools_listing_has_all_eighteen_and_the_packets_carry_it_verbatim():
    tools = load_tools()
    table = tools_table(tools, inputs=True)
    lines = table.splitlines()
    assert lines[0].split() == ["name", "side_effects", "cost", "participates_in", "doc", "inputs"]
    assert [ln.split()[0] for ln in lines[1:]] == sorted(tools) and len(tools) == 18
    assert "approve" not in table and "dispatch_failed" not in [ln.split()[0] for ln in lines]
    for uc in ("UC1", "UC2", "UC3"):
        packet = (ROOT / "ablation" / "packets" / f"{uc}.md").read_text()
        assert table in packet
        assert json.loads((CASES / f"{uc}.json").read_text())["task"] in packet
        for ph in ("{{CWD}}", "{{RUN_ID}}", "{{JOURNAL}}", "{{MANIFEST}}", "{{HARNESS}}"):
            assert ph in packet
        assert "Never run `python3 -m ancient_games.hybrid approve`" in packet and "`call done`" in packet
        low = packet.lower()
        for hint in ("suggested_next", "default plan", "stage order", "call gate first", "gate → guard", "gate -> guard", "c→d→b"):
            assert hint not in low, hint


def test_ctx_round_trips_through_the_cli_files(tmp_path):
    ctx = Ctx(stop_criterion="s", capability=["x"], known_facts=[("a", "b", "c", "d")],
              artifact_refs=[ArtifactRef("p", "mutate", "commit", ("q",))], actor={"a": "MAIN"}, dispatch_count=2)
    p = str(tmp_path / "ctx.json")
    save_ctx(p, ctx)
    back = load_ctx(p)
    assert back == ctx and dataclasses.asdict(back) == dataclasses.asdict(ctx)
    assert load_ctx(str(tmp_path / "missing.json")) == Ctx()


# --- fixtures ----------------------------------------------------------------------------
def test_fixtures_materialize_the_unfixed_task_state(tmp_path):
    r1 = fixtures.make_uc1(str(tmp_path / "uc1"))
    p = subprocess.run([sys.executable, "-c", "import research.stability"], cwd=r1, capture_output=True, text=True)
    assert p.returncode != 0 and "ImportError" in p.stderr or "ModuleNotFoundError" in p.stderr
    assert git(r1, "status", "--short") == "" and git(r1, "branch", "--show-current") == "master"
    r2 = fixtures.make_uc2(str(tmp_path / "uc2"))
    src = (Path(r2) / "loop" / "program_db.py").read_text()
    assert sum(1 for i in range(1, 7) if f"def _helper_{i}(" in src) == 6
    assert "_helper_" not in (Path(r2) / "loop" / "main.py").read_text()
    assert (Path(r2) / "loop" / "program_db.jsonl").read_text().count("\n") == 2
    r3 = fixtures.make_uc3(str(tmp_path / "uc3"))
    assert json.loads((Path(r3) / "eval" / "protocol.json").read_text())["holdout"] == "sealed"
    with pytest.raises(ValueError):
        fixtures.make_uc1("relative/path")


# --- scorer ------------------------------------------------------------------------------
def _scripted_journal(uc: str, tmp_path) -> tuple[str, str]:
    case = runner.load_case(str(CASES / f"{uc}.json"))
    repo = str(tmp_path / f"repo-{uc}"); runner.setup_fixture(case, repo)
    journal = str(tmp_path / f"{uc}.jsonl")
    report = runner.run_case(case, journal, repo)
    assert report.passed, report.mismatches
    return journal, repo


def test_scorer_on_uc1_scripted_journal_answers_q2_yes(tmp_path):
    journal, repo = _scripted_journal("UC1", tmp_path)
    r = score.score(journal, str(CASES / "UC1.json"), repo)
    assert r["primary"] == [score.Q2] and r[score.Q2] == {"answer": True, "dispatches": 0}
    assert r[score.Q1]["answer"] is True and r[score.Q1]["committed_files"] == ["research/stability.py", "tests/test_research_importable.py"]
    assert r[score.Q1]["uncovered"] == [] and r[score.Q3]["answer"] is True and r[score.Q3]["self_count_attempts"] == []
    assert r["refusals_by_invariant"] == {} and r["total_tool_calls"] == 12 and r["done_ok"] is True
    assert r["sequence"]["missing"] == 0 and r["sequence"]["extra"] == 0 and r["sequence"]["common"] == 12
    md = score.render_md(r)
    assert "| Q2 zero executed dispatches | yes | yes |" in md and "```diff" in md
    # without --repo the committed set falls back to the case's fixture.modified keys — same answer
    assert score.score(journal, str(CASES / "UC1.json"))[score.Q1]["committed_files"] == r[score.Q1]["committed_files"]


def test_scorer_on_uc2_scripted_journal(tmp_path):
    journal, repo = _scripted_journal("UC2", tmp_path)
    r = score.score(journal, str(CASES / "UC2.json"), repo)
    assert r["primary"] == [score.Q1, score.Q3]
    assert r[score.Q1]["answer"] is True and r[score.Q1]["committed_files"] == ["loop/program_db.py"]
    assert r[score.Q2] == {"answer": False, "dispatches": 2}
    assert r[score.Q3]["answer"] is True and r[score.Q3]["corroborate_line_before_prove"].startswith("Corroborate: six-are-dead: n=2/2")
    assert r["live_dispatches_end"] == 0 and r["sequence"]["missing"] == 0


def _hand_journal(path: str, events: list[dict]) -> str:
    j = Journal(path, "hand")
    for e in events:
        j.append(e)
    return path


def _tc(tool: str, args: dict | None = None, refused_by: str | None = None, reason: str | None = None,
        exit_type: str | None = None, summary: str = "ok: x") -> dict:
    return {"event": "tool_call", "tool": tool, "action_id": None, "args": args or {}, "args_hash": "0" * 16,
            "result_summary": summary, "exit_type": exit_type, "invariants_checked": [], "refused_by": refused_by,
            "reason": reason}


def test_scorer_q1_no_when_guard_missing(tmp_path):
    journal = _hand_journal(str(tmp_path / "h.jsonl"), [
        _tc("gate"), _tc("commit", {"message": "m"}, summary='ok: {"hash": "abc"}'), _tc("done", summary="ok: DONE")])
    r = score.score(journal, str(CASES / "UC2.json"))
    assert r[score.Q1] == {"answer": False, "committed_files": ["loop/program_db.py"], "guard_refs_before_commit": [],
                       "uncovered": ["loop/program_db.py"], "detail": None}
    assert r["done_ok"] is True and r["sequence"]["missing"] == 18 and r["sequence"]["extra"] == 0
    # a guard that names a different file, or one refused, or one after the commit, does not count
    journal2 = _hand_journal(str(tmp_path / "h2.jsonl"), [
        _tc("guard", {"refs-paths": ["loop/other.py"]}), _tc("guard", {"refs-paths": ["loop/program_db.py"]}, "I4", "hard_blocked"),
        _tc("commit", {"message": "m"}, summary='ok: {"hash": "abc"}'), _tc("guard", {"refs-paths": ["loop/program_db.py"]})])
    r2 = score.score(journal2, str(CASES / "UC2.json"))
    assert r2[score.Q1]["answer"] is False and r2[score.Q1]["guard_refs_before_commit"] == ["loop/other.py"]
    assert r2["refusals_by_invariant"] == {"I4": 1}
    journal3 = _hand_journal(str(tmp_path / "h3.jsonl"), [_tc("guard", {"refs-paths": ["loop/program_db.py"]}),
                                                          _tc("commit", {"message": "m"}, summary='ok: {"hash": "abc"}')])
    assert score.score(journal3, str(CASES / "UC2.json"))[score.Q1]["answer"] is True
    assert score.score(_hand_journal(str(tmp_path / "h4.jsonl"), [_tc("gate")]), str(CASES / "UC2.json"))[score.Q1]["answer"] is None


def test_scorer_q3_no_when_n_available_is_smuggled(tmp_path):
    good_line = {"event": "exit", "algorithm": "B", "steps_fired": ["B·1"], "exit_type": "PASS",
                 "exit_line": "Corroborate: six-are-dead: n=2/2; reconciled=agree.", "ctx_keys_set": []}
    base = [_tc("gate"), _tc("guard"), _tc("corroborate", {"action": "a", "claims": []}), good_line,
            _tc("prove", {"gate": "checkpoint"}, exit_type="PASS", summary="ok: PASS"), _tc("done", summary="ok: DONE")]
    assert score.score(_hand_journal(str(tmp_path / "ok.jsonl"), base), str(CASES / "UC2.json"))[score.Q3]["answer"] is True
    smug = list(base)
    smug[2] = _tc("corroborate", {"action": "a", "claims": [{"claim_id": "six-are-dead", "kind": "judgment", "n_available": 2}]})
    r = score.score(_hand_journal(str(tmp_path / "smug.jsonl"), smug), str(CASES / "UC2.json"))
    assert r[score.Q3]["answer"] is False
    assert r[score.Q3]["self_count_attempts"] == [{"step": 2, "tool": "corroborate", "keys": ["claims[0].n_available"]}]
    smug2 = list(base); smug2[4] = _tc("prove", {"gate": "checkpoint", "n_sources": {"six-are-dead": 2}}, exit_type="PASS", summary="ok: PASS")
    assert score.score(_hand_journal(str(tmp_path / "smug2.jsonl"), smug2), str(CASES / "UC2.json"))[score.Q3]["self_count_attempts"] == \
        [{"step": 3, "tool": "prove", "keys": ["n_sources"]}]
    # a PASS after a capped Corroborate line is inconsistent with the journaled count
    capped = list(base); capped[3] = dict(good_line, exit_line="Corroborate: six-are-dead: n=1/2, capped, remedy=add-differently-framed-source; reconciled=agree, corroboration-capped=true.")
    r = score.score(_hand_journal(str(tmp_path / "capped.jsonl"), capped), str(CASES / "UC2.json"))
    assert r[score.Q3]["answer"] is False and r[score.Q3]["prove_pass_consistent_with_corroborate"] is False
    # no corroborate at all → no
    nocorr = [base[0], base[1], base[4], base[5]]
    assert score.score(_hand_journal(str(tmp_path / "nocorr.jsonl"), nocorr), str(CASES / "UC2.json"))[score.Q3]["answer"] is False


def test_lcs_diff():
    assert score.lcs_diff(["gate", "guard", "commit"], ["gate", "commit", "done"]) == ["  gate", "- guard", "  commit", "+ done"]
    assert score.lcs_diff([], ["a"]) == ["+ a"] and score.lcs_diff(["a"], []) == ["- a"]


def test_score_cli_prints_markdown_and_json(tmp_path):
    journal, repo = _scripted_journal("UC1", tmp_path)
    p = subprocess.run([sys.executable, "-m", "ablation.score", journal, str(CASES / "UC1.json"), "--repo", repo],
                       cwd=ROOT, capture_output=True, text=True)
    assert p.returncode == 0 and p.stdout.startswith("# Ablation score — UC1-T2") and "| done succeeded | yes |" in p.stdout
    p = subprocess.run([sys.executable, "-m", "ablation.score", journal, str(CASES / "UC1.json"), "--json"],
                       cwd=ROOT, capture_output=True, text=True)
    assert json.loads(p.stdout)[score.Q2]["answer"] is True
