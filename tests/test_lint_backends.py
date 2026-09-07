"""`lints.run_all_on_plan`'s three backends. Python is the oracle (docs/STORE_DESIGN_DECISION.md §Tests):
every assertion here compares the *real* return values of the real backends on real journals — never a
re-derivation — and the differential mode is shown able to fail."""
from __future__ import annotations

import json
import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

import cases
import test_index as ti
from ancient_games import index, lints
from ancient_games.ctx import CappedClaim, Ctx
from ancient_games.hybrid.tools import prove as prove_tool, run_lint as run_lint_tool
from ancient_games.hybrid.types import ToolEnv
from ancient_games.journal import Journal, read_events
from ancient_games.stages import Claim, Plan, PlanEntry

ROOT = ti.ROOT
LARGEST = max(ti.REAL_JOURNALS, key=os.path.getsize)


def _spec_case(build, tmp_path):
    journal = Journal(str(tmp_path / "journal.jsonl"), run_id="test")
    run = build(journal)
    # a case that stops before Guard has no Plan; Plan([]) still runs the two return-shaped lints on its events
    return run.plan if run.plan is not None else Plan([]), journal.read()


def _all_five_fire(tmp_path) -> tuple[Plan, list[dict]]:
    """One journal + plan on which every SQL-backed lint has at least one finding."""
    j = Journal(str(tmp_path / "five.jsonl"), "five")
    j.append({"event": "return", "agent_id": "a", "fields": {
        "CLAIMS": [{"claim_id": "bad", "evidence_type": "command", "evidence_ref": ""},
                   {"claim_id": "ok", "evidence_type": "(opinion)"}],
        "FOLLOW_ON": [{"finding": "f1", "disposition": "later"}, {"finding": "f2", "disposition": "fixed"}]}})
    j.check_executed("X", "hash-compare", "sha256sum a", "h", "h")
    j.consumer_check(["a.py"], "yes", "grep")
    claim = Claim("X", "executable", n_required=2, actor="MAIN")
    cap = CappedClaim("X", "executable", 2, 2, 1, "add-claim-specific-check", "hash-compare")
    plan = Plan([PlanEntry("act", ["p"], 1, claims=[claim], capped=[cap]),
                 PlanEntry("hubby", ["x"], 2, ["loop/program_db.jsonl"], {"loop/program_db.jsonl": "never ran"}),
                 PlanEntry("edit", ["a.py", "b.py"], 1, [])])
    return plan, j.read()


# --- (a) the three backends agree on every real input, and the agreement is not vacuous --------------
@pytest.mark.parametrize("journal_path", ti.REAL_JOURNALS,
                         ids=[os.path.relpath(p, ROOT / "ablation" / "runs") for p in ti.REAL_JOURNALS])
def test_backends_agree_on_real_journal(journal_path):
    events = read_events(journal_path)
    run_id = ti._run_id(events)
    plan = ti._plan_for_real(events, run_id)
    py = lints.run_all_on_plan(plan, events, backend="python")
    sql = lints.run_all_on_plan(plan, events, backend="sql")
    diff = lints.run_all_on_plan(plan, events, backend="differential")
    assert py == sql == diff
    assert py == lints.run_all_on_plan(plan, events, backend="python", run_id=run_id)


@pytest.mark.parametrize("build", ti.SPEC_CASES, ids=[f.__name__ for f in ti.SPEC_CASES])
def test_backends_agree_on_spec_case(build, tmp_path):
    plan, events = _spec_case(build, tmp_path)
    py = lints.run_all_on_plan(plan, events, backend="python")
    assert py == lints.run_all_on_plan(plan, events, backend="sql") == lints.run_all_on_plan(plan, events, backend="differential")


def test_real_inputs_carry_findings():
    """The agreement above covers real findings: at least some real journals produce some."""
    total = 0
    for journal_path in ti.REAL_JOURNALS:
        events = read_events(journal_path)
        plan = ti._plan_for_real(events, ti._run_id(events))
        total += len(lints.run_all_on_plan(plan, events, backend="python"))
    assert total >= 13  # attempt2/UC1 (1 hub), attempt2/UC3 (8 capped), attempt3/UC3 (3), attempt4/UC3 (1) as of 27320a8


def test_backends_agree_when_every_sql_lint_fires(tmp_path):
    plan, events = _all_five_fire(tmp_path)
    py = lints.run_all_on_plan(plan, events, backend="python")
    assert {f.lint for f in py} >= set(lints.SQL_LINTS)
    assert py == lints.run_all_on_plan(plan, events, backend="sql") == lints.run_all_on_plan(plan, events, backend="differential")


# --- (b) differential must be able to fail -------------------------------------------------------------
def test_differential_raises_when_sql_drops_a_finding(tmp_path, monkeypatch):
    plan, events = _all_five_fire(tmp_path)
    real = index.claims_without_evidence

    def lossy(con, run_id):
        return real(con, run_id)[:-1]  # the SQL "forgets" one finding

    monkeypatch.setattr(index, "claims_without_evidence", lossy)
    assert lints.run_all_on_plan(plan, events, backend="sql") != lints.run_all_on_plan(plan, events, backend="python")
    with pytest.raises(lints.LintBackendDivergence) as ei:
        lints.run_all_on_plan(plan, events, backend="differential")
    e = ei.value
    assert e.lint == "claims-without-evidence" and e.run_id == "five"
    assert e.python == [lints.Finding("claims-without-evidence", "bad", "claim bad lacks command|file:line|URL|(opinion)")]
    assert e.sql == []
    assert "python (oracle)" in str(e) and "run_id='five'" in str(e) and "'claims-without-evidence'" in str(e)
    # ... and through the prove tool, where the divergence surfaces as the tool's declined result, never a PASS
    env = ToolEnv("five", str(tmp_path / "five.jsonl"), Ctx(), cwd=str(tmp_path))
    r = prove_tool.run(env, {"gate": "checkpoint", "backend": "differential"})
    assert not r.ok and r.reason.startswith("internal-error: lint backend divergence on 'claims-without-evidence'")


def test_differential_raises_when_sql_adds_a_finding(tmp_path, monkeypatch):
    plan, events = _all_five_fire(tmp_path)
    extra = lints.Finding("hub-touched-without-tripwire", "ghost", "ghost")
    real = index.hub_touched_without_tripwire
    monkeypatch.setattr(index, "hub_touched_without_tripwire", lambda plan, con, run_id: real(plan, con, run_id) + [extra])
    with pytest.raises(lints.LintBackendDivergence, match="hub-touched-without-tripwire") as ei:
        lints.run_all_on_plan(plan, events, backend="differential")
    assert ei.value.sql[-1] == extra and extra not in ei.value.python


# --- (c) backend=sql end to end through the CLI on a real journal ----------------------------------------
def _cli(manifest, *argv):
    cmd = [sys.executable, "-m", "ancient_games.hybrid", "--manifest", manifest, *argv]
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def test_cli_sql_backend_on_real_journal(tmp_path):
    src = str(ROOT / "ablation" / "runs" / "attempt4" / "UC3.journal.jsonl")
    events = read_events(src)
    run_id = ti._run_id(events)
    journal = str(tmp_path / "j.jsonl")
    shutil.copy(src, journal)
    rc, out, err = _cli(str(tmp_path / "m.json"), "init", "--run-id", run_id, "--journal", journal, "--cwd", str(tmp_path))
    assert rc == 0, err
    rc, out, err = _cli(str(tmp_path / "m.json"), "call", "run_lint", json.dumps({"backend": "sql"}))
    assert rc == 0, err
    got = json.loads(out)
    assert got["ok"] and got["value"]["backend"] == "sql"
    # the CLI's ctx is empty, so the oracle is run in-process over the same events with the same (empty) ctx
    from ancient_games.hybrid.tools._plan import plan_from_journal
    want = lints.run_all_on_plan(plan_from_journal(events, Ctx(), {}), events, backend="python")
    # the CLI renders each Finding with str() (json_safe's default=str) — as it did before `backend` existed
    assert got["value"]["findings"] == [str(f) for f in want]
    assert any(f.lint == "corroboration-capped" for f in want)  # attempt4/UC3 has a real capped-claim finding
    rc, out, err = _cli(str(tmp_path / "m.json"), "call", "prove", json.dumps({"gate": "checkpoint", "backend": "sql"}))
    assert rc == 0, err
    got = json.loads(out)
    # the oracle: the python-backend prove tool in-process on a second copy of the same journal, same empty ctx
    # (prove discloses the capped claim in its own exit line, so run_lint's disclosure finding is not prove's)
    other = str(tmp_path / "oracle.jsonl")
    shutil.copy(src, other)
    oracle = prove_tool.run(ToolEnv(run_id, other, Ctx(), cwd=str(tmp_path)), {"gate": "checkpoint", "backend": "python"})
    assert oracle.ok and oracle.value.lint_backend == "python"
    assert got["ok"] and got["value"]["lint_backend"] == "sql"
    assert (got["value"]["exit_type"], got["value"]["exit_line"], got["value"]["findings"]) == \
        (oracle.value.exit_type, oracle.value.exit_line, oracle.value.findings)
    assert got["value"]["exit_type"] == "PASS"  # attempt4/UC3 with an empty ctx: the lints alone pass
    # the journal says how each was checked
    calls = [e for e in read_events(journal) if e.get("event") == "tool_call" and e["tool"] in ("run_lint", "prove")]
    assert calls[-2]["tool"] == "run_lint" and '"backend": "sql"' in calls[-2]["result_summary"]
    assert calls[-1]["tool"] == "prove" and calls[-1]["result_summary"] == "ok: PASS [lint_backend=sql]"
    # a bad backend is the caller's error, named (H2), exit 2
    rc, out, err = _cli(str(tmp_path / "m.json"), "call", "prove", json.dumps({"backend": "mysql"}))
    assert rc == 2 and json.loads(out)["reason"] == "invalid-args: backend must be python | sql | differential, got 'mysql' (str)"


def test_prove_result_summary_names_the_backend_in_process(tmp_path):
    journal = Journal(str(tmp_path / "j.jsonl"), "t")
    run = cases.run_t1(journal)  # a spec case with a real capped finding
    from ancient_games.hybrid.tools._shared import result_summary
    from ancient_games.hybrid.types import ToolResult
    for backend in lints.BACKENDS:
        env = ToolEnv("test", journal.path, Ctx(), cwd=str(tmp_path))
        r = prove_tool.run(env, {"gate": "checkpoint", "backend": backend})
        assert r.ok and r.value.lint_backend == backend
        assert result_summary(r) == f"ok: {r.value.exit_type} [lint_backend={backend}]"
        rl = run_lint_tool.run(env, {"backend": backend})
        assert rl.ok and rl.value["backend"] == backend
        assert result_summary(rl).startswith('ok: {"backend": "%s"' % backend)
    assert result_summary(ToolResult(True, run.prove)) == "ok: " + run.prove.exit_type + " [lint_backend=differential]"  # the suite's env


# --- (d) the default ---------------------------------------------------------------------------------
def test_default_backend_is_python_without_the_env_var(monkeypatch):
    monkeypatch.delenv(lints.ENV_BACKEND, raising=False)
    assert lints.default_backend() == "python"
    monkeypatch.setenv(lints.ENV_BACKEND, "")
    assert lints.default_backend() == "python"
    monkeypatch.setenv(lints.ENV_BACKEND, "sql")
    assert lints.default_backend() == "sql"
    monkeypatch.setenv(lints.ENV_BACKEND, "postgres")
    with pytest.raises(ValueError, match="lint backend must be one of"):
        lints.default_backend()
    with pytest.raises(ValueError, match="lint backend must be one of"):
        lints.run_all_on_plan(Plan([]), [], backend="postgres")


def test_suite_runs_in_differential_mode():
    assert os.environ.get(lints.ENV_BACKEND) == "differential" and lints.default_backend() == "differential"


def test_default_backend_drives_prove_and_run_lint(tmp_path, monkeypatch):
    journal = Journal(str(tmp_path / "j.jsonl"), "test")
    cases.run_t1(journal)
    env = ToolEnv("test", journal.path, Ctx(), cwd=str(tmp_path))
    monkeypatch.delenv(lints.ENV_BACKEND, raising=False)
    assert prove_tool.run(env, {"gate": "checkpoint"}).value.lint_backend == "python"
    assert run_lint_tool.run(env, {}).value["backend"] == "python"
    monkeypatch.setenv(lints.ENV_BACKEND, "sql")
    assert prove_tool.run(env, {"gate": "checkpoint"}).value.lint_backend == "sql"
    assert run_lint_tool.run(env, {}).value["backend"] == "sql"


# --- rebuild_from_events -----------------------------------------------------------------------------
def test_rebuild_is_rebuild_from_events_over_the_journal(tmp_path):
    src = LARGEST
    events = read_events(src)
    db = str(tmp_path / "file.sqlite")
    r_file = index.rebuild(src, db)
    r_mem_con = index.memory_index(events)
    r_events = index.rebuild_from_events(events, str(tmp_path / "events.sqlite"))
    assert r_file == r_events and r_file["events"] == len(events) > 0
    dump_file = "\n".join(sqlite3.connect(db).iterdump())
    dump_mem = "\n".join(r_mem_con.iterdump())
    dump_events = "\n".join(sqlite3.connect(str(tmp_path / "events.sqlite")).iterdump())
    assert dump_file == dump_mem == dump_events
    with pytest.raises(ValueError, match="db_path must be absolute"):
        index.rebuild_from_events(events, "rel.sqlite")


def test_sql_backend_needs_run_id_for_a_multi_run_event_list(tmp_path):
    a, b = ti.COLLIDING[0], ti.COLLIDING[1]
    events = read_events(a) + read_events(b)
    with pytest.raises(ValueError, match="needs run_id= for a multi-run event list"):
        lints.run_all_on_plan(Plan([]), events, backend="sql")
    run_a = ti._run_id(read_events(a))
    plan = ti._plan_for_real(read_events(a), run_a)
    # scoped to run a, the SQL side equals the oracle run over run a's own events
    assert (lints.run_all_on_plan(plan, events, backend="sql", run_id=run_a)
            == lints.run_all_on_plan(plan, read_events(a), backend="python"))
