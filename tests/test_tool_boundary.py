"""The tool boundary returns results, never raises across it.

Two ways it did: an invalid `$AG_LINT_BACKEND` was resolved eagerly outside the adapter's
try (`loop.step` has no except, so the ValueError killed the loop and journalled nothing),
and adapters that dereferenced a required arg inside the broad try reported `internal-error`
where `_shared.invalid_args` mandates `invalid-args` — which is also the prefix `cli.cmd_call`
exits 2 on. Every assertion below is a real return value / exit code of the real tool.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from ablation import fixtures
from ancient_games import lints
from ancient_games.ctx import Ctx
from ancient_games.hybrid import loop
from ancient_games.hybrid.registry import load_tools
from ancient_games.hybrid.tools import (commit as commit_tool, dispatch as dispatch_tool,
                                        ingest_return as ingest_tool, prove as prove_tool,
                                        record_check as record_check_tool, record_claim as record_claim_tool,
                                        run_lint as run_lint_tool, run_suite as run_suite_tool)
from ancient_games.hybrid.types import Call, ToolEnv
from ancient_games.journal import Journal
from ancient_games.stages import Plan

ROOT = Path(__file__).resolve().parent.parent
TOOLS = load_tools()


def _env(tmp_path, journal="j.jsonl"):
    return ToolEnv("tb", str(tmp_path / journal), Ctx(), cwd=str(tmp_path), tools=TOOLS)


# --- (1) the lint backend ---------------------------------------------------------------------
BACKEND_TOOLS = {"prove": (prove_tool, {"gate": "checkpoint"}), "run_lint": (run_lint_tool, {})}


@pytest.mark.parametrize("name", sorted(BACKEND_TOOLS))
def test_invalid_env_backend_is_invalid_args_not_a_traceback(name, tmp_path, monkeypatch):
    tool, args = BACKEND_TOOLS[name]
    monkeypatch.setenv(lints.ENV_BACKEND, "postgres")
    r = tool.run(_env(tmp_path), dict(args))
    assert r.ok is False and r.value is None
    assert r.reason == "invalid-args: $AG_LINT_BACKEND must be python | sql | differential, got 'postgres' (str)"


@pytest.mark.parametrize("name", sorted(BACKEND_TOOLS))
def test_valid_explicit_backend_survives_a_bad_env_backend(name, tmp_path, monkeypatch):
    """The default is consulted only when no backend was passed: a bad env var must not
    reject a call that named a valid backend of its own."""
    tool, args = BACKEND_TOOLS[name]
    monkeypatch.setenv(lints.ENV_BACKEND, "postgres")
    r = tool.run(_env(tmp_path), dict(args, backend="python"))
    assert r.ok is True, r.reason
    got = r.value.lint_backend if name == "prove" else r.value["backend"]
    assert got == "python"


@pytest.mark.parametrize("name", sorted(BACKEND_TOOLS))
def test_invalid_env_backend_does_not_kill_the_loop(name, tmp_path, monkeypatch):
    """`loop.step` has no except: before the fix this raised out of it. The step must return
    a refused-free result the loop journals."""
    monkeypatch.setenv(lints.ENV_BACKEND, "postgres")
    journal = Journal(str(tmp_path / "loop.jsonl"), "tb")
    st = loop.step(TOOLS, Call(name, dict(BACKEND_TOOLS[name][1])), journal, Ctx(), 0, cwd=str(tmp_path))
    assert st.refused_by is None
    assert st.result.ok is False and st.result.reason.startswith("invalid-args: $AG_LINT_BACKEND")
    calls = [e for e in journal.read() if e["event"] == "tool_call"]
    assert [e["tool"] for e in calls] == [name] and calls[0]["reason"].startswith("invalid-args:")


def test_explicit_bad_backend_still_names_the_backend_field(tmp_path, monkeypatch):
    monkeypatch.delenv(lints.ENV_BACKEND, raising=False)
    r = run_lint_tool.run(_env(tmp_path), {"backend": "postgres"})
    assert r.reason == "invalid-args: backend must be python | sql | differential, got 'postgres' (str)"


# --- (2) a malformed CLAIMS entry: a finding in all three backends ------------------------------
def _bare_string_journal(tmp_path) -> tuple[Plan, list[dict]]:
    j = Journal(str(tmp_path / "bare.jsonl"), "bare")
    j.append({"event": "return", "agent_id": "a",
              "fields": {"CLAIMS": ["a bare string", {"claim_id": "ok", "evidence_type": "(opinion)"}]}})
    return Plan([]), j.read()


def test_bare_string_claims_entry_is_a_finding_in_the_python_oracle(tmp_path):
    assert lints.lint_claims_without_evidence(["a bare string"]) == \
        [lints.Finding("claims-without-evidence", "#0", "claim #0 lacks command|file:line|URL|(opinion)")]


@pytest.mark.parametrize("backend", ["python", "sql", "differential"])
def test_bare_string_claims_entry_agrees_across_backends(backend, tmp_path):
    """`differential` raises LintBackendDivergence if the two disagree — before the fix the
    Python oracle raised AttributeError and the SQL side silently skipped the entry."""
    plan, events = _bare_string_journal(tmp_path)
    got = lints.run_all_on_plan(plan, events, backend=backend, run_id="bare")
    subjects = [(f.lint, f.subject) for f in got if f.lint == "claims-without-evidence"]
    assert subjects == [("claims-without-evidence", "#0")], backend


# --- (3) required args are the caller's error, not an internal-error -----------------------------
MISSING_ARG = {
    "commit": (commit_tool, {}, "message"),
    "run_suite": (run_suite_tool, {}, "command"),
    "record_claim": (record_claim_tool, {"claim_id": "C1", "author": "a", "kind": "judgment"}, "evidence_type"),
    "dispatch": (dispatch_tool, {}, "role"),
    "record_check": (record_check_tool, {"claim_id": "C1"}, "mechanism"),
    "ingest_return": (ingest_tool, {}, "agent_id"),
}


@pytest.mark.parametrize("name", sorted(MISSING_ARG))
def test_missing_required_arg_is_invalid_args(name, tmp_path):
    tool, args, field = MISSING_ARG[name]
    r = tool.run(_env(tmp_path), dict(args))
    assert r.ok is False and r.value is None
    assert r.reason.startswith(f"invalid-args: {field} must be "), r.reason
    assert not r.reason.startswith("internal-error")


@pytest.fixture(scope="module")
def manifest(tmp_path_factory):
    d = tmp_path_factory.mktemp("cli")
    repo = fixtures.make_uc1(str(d / "repo"))
    p = subprocess.run([sys.executable, "-m", "ancient_games.hybrid", "init", "--run-id", "tb",
                        "--journal", str(d / "j.jsonl"), "--cwd", repo],
                       cwd=ROOT, capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    return json.loads(p.stdout)["manifest"]


@pytest.mark.parametrize("name", sorted(MISSING_ARG))
def test_cli_exits_2_on_a_missing_required_arg(name, manifest):
    _, args, field = MISSING_ARG[name]
    p = subprocess.run([sys.executable, "-m", "ancient_games.hybrid", "--manifest", manifest,
                        "call", name, json.dumps(args)], cwd=ROOT, capture_output=True, text=True)
    out = json.loads(p.stdout)
    assert out["refused_by"] is None, out  # not an invariant refusal: the adapter declined the args
    assert out["ok"] is False and out["reason"].startswith(f"invalid-args: {field} must be "), out
    assert p.returncode == 2, p.stdout + p.stderr
