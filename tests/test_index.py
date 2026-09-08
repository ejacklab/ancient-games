"""The SQLite read index (ancient_games/index.py) against its oracle, the Python lints in
ancient_games/lints.py — never a re-derivation. Every differential assertion calls the real lint
on the real events and the SQL query on the index built from the same journal, and compares."""
from __future__ import annotations

import glob
import json
import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

import cases
from ancient_games import index, lints
from ancient_games.ctx import CappedClaim, Ctx
from ancient_games.hybrid.tools._plan import plan_from_journal
from ancient_games.hybrid.tools._shared import guard_action
from ancient_games.journal import Journal, read_events
from ancient_games.stages import CapState, Claim, Plan, PlanEntry, count_sources

ROOT = Path(__file__).resolve().parent.parent
REAL_JOURNALS = sorted(glob.glob(str(ROOT / "ablation" / "runs" / "attempt*" / "*.journal.jsonl")))
SPEC_CASES = [cases.run_t2, cases.run_t1, cases.run_t3, cases.run_case1, cases.run_case2, cases.run_case3,
              cases.run_case_i, cases.run_case_ii]
QUERIES = ("claims-without-evidence", "follow-on-without-disposition", "corroboration-capped",
           "hub-touched-without-tripwire", "downstream-consumer-check-unrecorded")


def _run_id(events: list[dict]) -> str:
    ids = {e["run_id"] for e in events}
    assert len(ids) == 1, ids
    return ids.pop()


def _plan_for_real(events: list[dict], run_id: str) -> Plan:
    """The plan `prove`/`run_lint` rebuild from a real journal. The CLI's persisted ctx is not in the fixture
    set, so it is re-derived from the same journaled facts: `guard` sets actor MAIN per action
    (stages.guard, main_executes), dispatches count toward dispatch_count."""
    ctx = Ctx()
    for e in events:
        if e.get("event") == "tool_call" and e["refused_by"] is None and e["reason"] is None:
            if e["tool"] == "guard":
                ctx.actor.setdefault(guard_action(e["args"]).name, "MAIN")
            elif e["tool"] == "dispatch":
                ctx.dispatch_count += 1
    return plan_from_journal(events, ctx, {}, run_id=run_id)


def python_findings(plan: Plan | None, events: list[dict]) -> dict[str, list[lints.Finding]]:
    out = {q: [] for q in QUERIES}
    for ev in events:
        if ev.get("event") == "return":
            fields = ev.get("fields", {})
            out["claims-without-evidence"] += lints.lint_claims_without_evidence(fields.get("CLAIMS", []) or [])
            out["follow-on-without-disposition"] += lints.lint_follow_on_without_disposition(fields.get("FOLLOW_ON", []) or [])
    if plan is not None:
        out["corroboration-capped"] = lints.lint_corroboration_capped(plan, events)
        out["hub-touched-without-tripwire"] = lints.lint_hub_touched_without_tripwire(plan, events)
        out["downstream-consumer-check-unrecorded"] = lints.lint_downstream_consumer_check_unrecorded(plan, events)
    return out


def sql_findings(plan: Plan | None, con: sqlite3.Connection, run_id: str) -> dict[str, list[lints.Finding]]:
    out = {"claims-without-evidence": index.claims_without_evidence(con, run_id),
           "follow-on-without-disposition": index.follow_on_without_disposition(con, run_id),
           "corroboration-capped": [], "hub-touched-without-tripwire": [], "downstream-consumer-check-unrecorded": []}
    if plan is not None:
        out["corroboration-capped"] = index.corroboration_capped(plan, con, run_id)
        out["hub-touched-without-tripwire"] = index.hub_touched_without_tripwire(plan, con, run_id)
        out["downstream-consumer-check-unrecorded"] = index.downstream_consumer_check_unrecorded(plan, con, run_id)
    return out


def _build(journal_path: str, tmp_path: Path, name: str = "index.sqlite") -> sqlite3.Connection:
    db = str(tmp_path / name)
    index.rebuild(journal_path, db)
    return index.connect(db)


# --- 1. differential on real data ----------------------------------------------------------
def test_real_journal_set_is_the_expected_one():
    """11 since ablation 4 (attempt5/GM1, 26 events). The pin is what stops a journal appearing or
    vanishing unnoticed, so a new run updates it deliberately — the differential test below then
    runs over the new journal too, which is how a fresh run's events get lint-checked at all."""
    assert len(REAL_JOURNALS) == 11
    assert sum(len(read_events(p)) for p in REAL_JOURNALS) == 518


@pytest.mark.parametrize("journal_path", REAL_JOURNALS, ids=[os.path.relpath(p, ROOT / "ablation" / "runs") for p in REAL_JOURNALS])
def test_differential_real_journal(journal_path, tmp_path):
    events = read_events(journal_path)
    run_id = _run_id(events)
    plan = _plan_for_real(events, run_id)
    con = _build(journal_path, tmp_path)
    assert sql_findings(plan, con, run_id) == python_findings(plan, events)


@pytest.mark.parametrize("build", SPEC_CASES, ids=[f.__name__ for f in SPEC_CASES])
def test_differential_spec_case(build, tmp_path):
    journal = Journal(str(tmp_path / "journal.jsonl"), run_id="test")
    run = build(journal)
    events = journal.read()
    con = _build(journal.path, tmp_path)
    got, want = sql_findings(run.plan, con, "test"), python_findings(run.plan, events)
    assert got == want


def test_corroboration_capped_recounts_on_real_data(tmp_path):
    """The (b) branch — count_sources in SQL — is actually reached: attempt4/UC3 carries capped claims with
    re-plannable remedies, and count_sources agrees with the Python on every claim of every real journal."""
    claims, replannable = 0, 0
    for i, journal_path in enumerate(REAL_JOURNALS):
        events = read_events(journal_path)
        run_id = _run_id(events)
        plan = _plan_for_real(events, run_id)
        con = _build(journal_path, tmp_path, f"{i}.sqlite")
        for e in plan.entries:
            replannable += sum(1 for cap in e.capped if cap.remedy in ("add-claim-specific-check", "add-differently-framed-source"))
            for c in e.claims:
                n_py, _ = count_sources(c, events, CapState(), [])
                assert index.count_sources(con, run_id, c) == n_py, (journal_path, c.claim_id)
                claims += 1
    assert claims > 0 and replannable > 0


# --- 2. multi-run collision ----------------------------------------------------------------
COLLIDING = [str(ROOT / "ablation" / "runs" / p) for p in ("attempt2/UC1.journal.jsonl", "attempt2/UC3.journal.jsonl",
                                                            "attempt4/UC3.journal.jsonl")]


def test_multi_run_collision(tmp_path):
    per_run = {}
    lines = []
    for p in COLLIDING:
        events = read_events(p)
        per_run[_run_id(events)] = events
        lines += [ln for ln in Path(p).read_text().splitlines() if ln.strip()]
    assert len(per_run) == 3
    # the collision is real: C1 is recorded in every one of these runs
    for run_id, events in per_run.items():
        assert "C1" in {e["claim_id"] for e in events if e["event"] == "claim_recorded"}, run_id
    merged = tmp_path / "merged.jsonl"
    merged.write_text("\n".join(lines) + "\n")
    merged_events = read_events(str(merged))
    con = _build(str(merged), tmp_path)
    assert con.execute("SELECT COUNT(DISTINCT run_id) FROM claim_recorded").fetchone()[0] == 3
    # every query equals its per-run Python result
    for run_id, events in per_run.items():
        plan = _plan_for_real(events, run_id)
        assert sql_findings(plan, con, run_id) == python_findings(plan, events), run_id
    # ... and the run_id filter is load-bearing: without it, the "ran" set and C1's source count change
    for run_id, events in per_run.items():
        plan = _plan_for_real(events, run_id)
        ran_all = {r[0] for r in con.execute("SELECT DISTINCT command FROM check_executed")}
        ran_run = {r[0] for r in con.execute("SELECT DISTINCT command FROM check_executed WHERE run_id = ?", (run_id,))}
        assert ran_run < ran_all
    c1 = Claim("C1", "executable", n_required=3, actor="MAIN")
    counts = {run_id: index.count_sources(con, run_id, c1) for run_id in per_run}
    unscoped = count_sources(c1, merged_events, CapState(), [])[0]
    assert any(n != unscoped for n in counts.values()), (unscoped, counts)  # per-run != whole-DB for some run


# --- 3. rebuild contract --------------------------------------------------------------------
def test_rebuild_twice_is_byte_identical(tmp_path):
    src = COLLIDING[2]
    db = str(tmp_path / "i.sqlite")
    r1 = index.rebuild(src, db)
    dump1 = "\n".join(sqlite3.connect(db).iterdump())
    r2 = index.rebuild(src, db)
    dump2 = "\n".join(sqlite3.connect(db).iterdump())
    assert r1 == r2 and dump1 == dump2
    assert r1["rows"] > 0 and r1["events"] == 85 and set(r1["tables"]) == set(index.TABLES)


def test_relative_paths_raise(tmp_path):
    with pytest.raises(ValueError, match="journal_path must be absolute"):
        index.rebuild("j.jsonl", str(tmp_path / "i.sqlite"))
    with pytest.raises(ValueError, match="db_path must be absolute"):
        index.rebuild(COLLIDING[0], "i.sqlite")
    with pytest.raises(ValueError, match="db_path must be absolute"):
        index.connect("i.sqlite")


def test_user_version_and_tables(tmp_path):
    con = _build(COLLIDING[0], tmp_path)
    assert con.execute("PRAGMA user_version").fetchone()[0] == 1
    names = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
    assert names == set(index.TABLES)
    assert con.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'index' AND name LIKE 'ix_%'").fetchone()[0] == 5
    cols = [r[1] for r in con.execute("PRAGMA table_info(claim_recorded)")]
    assert cols == ["run_id", "ts", "claim_id", "author", "actor", "kind", "text", "evidence_type", "evidence_ref",
                    "framing", "kind_override", "closed_world"]
    for t in index.TABLES:
        assert "run_id" in [r[1] for r in con.execute(f'PRAGMA table_info("{t}")')], t


# --- 4./5. minimal FAIL and PASS inputs per query, each checked against the lint ----------------
def _journal(tmp_path, name="j.jsonl", run_id="r"):
    return Journal(str(tmp_path / name), run_id)


def _both(plan, journal, tmp_path):
    con = _build(journal.path, tmp_path)
    return sql_findings(plan, con, journal.run_id), python_findings(plan, journal.read())


def test_claims_without_evidence_fail_and_pass(tmp_path):
    j = _journal(tmp_path)
    j.append({"event": "return", "agent_id": "a", "fields": {"CLAIMS": [
        {"claim_id": "bad1", "evidence_type": "command", "evidence_ref": ""},   # FAIL: empty ref
        {"kind": "executable"},                                                  # FAIL: no evidence, no id -> #1
        {"claim_id": "ok1", "evidence_type": "(opinion)"},                       # PASS
        {"claim_id": "ok2", "evidence_type": "file:line", "evidence_ref": "x:1"}]}})
    got, want = _both(None, j, tmp_path)
    assert got == want and [f.subject for f in got["claims-without-evidence"]] == ["bad1", "#1"]


def test_follow_on_without_disposition_fail_and_pass(tmp_path):
    j = _journal(tmp_path)
    entries = [("a", "fixed"), ("b", "new-task"), ("c", "dismissed:out-of-scope"), ("d", "escalated:ej"),
               ("e", "EJ decision"), ("f", "dismissed:"), ("g", "escalated:"), ("h", None), ("i", "fixed\n"),
               ("j", "dismissed: x"), ("k", "escalated:e j"), ("l", "dismissed:x\ny"), {"finding": "m"}, {"disposition": "fixed"}]
    j.append({"event": "return", "agent_id": "a", "fields": {"FOLLOW_ON": entries}})
    got, want = _both(None, j, tmp_path)
    assert got == want
    assert [f.subject for f in got["follow-on-without-disposition"]] == ["e", "f", "g", "h", "j", "k", "l", "m"]


def test_corroboration_capped_fail_and_pass(tmp_path):
    j = _journal(tmp_path)
    claim = Claim("X", "executable", n_required=2, actor="MAIN")
    cap = CappedClaim("X", "executable", 2, 2, 1, "add-claim-specific-check", "hash-compare")
    plan = Plan([PlanEntry("act", ["p"], 1, claims=[claim], capped=[cap])])
    j.check_executed("X", "hash-compare", "sha256sum p", "h", "h")
    got, want = _both(plan, j, tmp_path)
    assert got == want and [f.lint for f in got["corroboration-capped"]] == ["corroboration-capped"]
    j.check_executed("X", "hash-compare", "sha256sum p", "h", "h")   # identical command: still 1
    j.check_executed("X", "git-diff-scope", "sha256sum p", "h", "h")  # identical command, other mechanism: still 1
    got, want = _both(plan, j, tmp_path)
    assert got == want and got["corroboration-capped"]
    j.check_executed("X", "git-diff-scope", "git diff --stat", "0", "0")  # second mechanism: 2/2
    got, want = _both(plan, j, tmp_path)
    assert got == want and got["corroboration-capped"] == []


def test_count_sources_null_framings_and_actor_none(tmp_path):
    """(a) counts NULL as one framing bucket, like the Python set; actor=none admits every author."""
    j = _journal(tmp_path)
    j.claim_recorded("J", "agent-1", "none", "judgment", "t", "command", "c1", framing=None)
    j.claim_recorded("J", "agent-2", "none", "judgment", "t", "command", "c2", framing=None)
    j.claim_recorded("J", "MAIN", "none", "judgment", "t", "command", "c3", framing="text-scan")
    j.claim_recorded("J", "agent-3", "none", "judgment", "t", "command", "c4", framing="")
    con = _build(j.path, tmp_path)
    for actor in ("none", "MAIN", "agent-1"):
        c = Claim("J", "judgment", n_required=3, actor=actor)
        assert index.count_sources(con, "r", c) == count_sources(c, j.read(), CapState(), [])[0], actor


def test_hub_touched_without_tripwire_fail_and_pass(tmp_path):
    plan = Plan([PlanEntry("delete", ["loop/program_db.py"], 2, ["loop/program_db.jsonl"],
                           {"loop/program_db.jsonl": "sha256sum loop/program_db.jsonl"})])
    j = _journal(tmp_path)
    j.check_executed("x", "hash-compare", "sha256sum somewhere/else", "h", "h")
    got, want = _both(plan, j, tmp_path)
    assert got == want and [f.lint for f in got["hub-touched-without-tripwire"]] == ["hub-touched-without-tripwire"]
    j.check_executed("journal-untouched", "hash-compare", "sha256sum loop/program_db.jsonl", "h", "h")
    got, want = _both(plan, j, tmp_path)
    assert got == want and got["hub-touched-without-tripwire"] == []


def test_downstream_consumer_check_fail_pass_and_vacuous(tmp_path):
    entry = PlanEntry("edit", ["a.py", "b.py"], 1, [])
    empty = PlanEntry("noop", [], 1, [])
    plan = Plan([entry, empty])
    j = _journal(tmp_path)
    got, want = _both(plan, j, tmp_path)  # no consumer_check at all: both entries FAIL (any([]) is False)
    assert got == want and [f.subject for f in got["downstream-consumer-check-unrecorded"]] == ["edit", "noop"]
    j.consumer_check(["a.py"], "no", "grep")  # covers a.py only: edit still FAILs, noop is vacuously covered
    got, want = _both(plan, j, tmp_path)
    assert got == want and [f.subject for f in got["downstream-consumer-check-unrecorded"]] == ["edit"]
    j.consumer_check(["b.py", "a.py", "c.py"], "no", "grep")  # superset covers edit
    got, want = _both(plan, j, tmp_path)
    assert got == want and got["downstream-consumer-check-unrecorded"] == []


# --- 6. end to end through the CLI -------------------------------------------------------------
def test_cli_rebuild_index_succeeds(tmp_path):
    journal = str(tmp_path / "j.jsonl")
    shutil.copy(COLLIDING[2], journal)
    cmd = [sys.executable, "-m", "ancient_games.hybrid"]
    p = subprocess.run(cmd + ["init", "--run-id", "ablation-UC3-4", "--journal", journal, "--cwd", str(tmp_path),
                              "--ceiling", "200"], cwd=ROOT, capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    manifest = journal + ".run.json"
    db = str(tmp_path / "index.sqlite")
    p = subprocess.run(cmd + ["--manifest", manifest, "call", "rebuild_index", json.dumps({"db_path": db})],
                       cwd=ROOT, capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    out = json.loads(p.stdout)
    assert out["ok"] is True and out["reason"] is None and out["value"]["events"] == 86  # 85 + the `run_config` event `init` now writes and out["value"]["rows"] > 0
    assert index.connect(db).execute("PRAGMA user_version").fetchone()[0] == 1
    # a relative db_path is the caller's error (H2), not an internal error
    p = subprocess.run(cmd + ["--manifest", manifest, "call", "rebuild_index", json.dumps({"db_path": "index.sqlite"})],
                       cwd=ROOT, capture_output=True, text=True)
    assert p.returncode == 2 and json.loads(p.stdout)["reason"].startswith("invalid-args: db_path must be an absolute path")
