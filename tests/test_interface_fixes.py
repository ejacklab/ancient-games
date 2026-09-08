"""The five tool-interface fixes (docs/INTERFACE_FIXES_IMPL.md).

Step 0 pins the two forge reproductions BEFORE the fix exists: both are
`xfail(strict=True)` here, so they must FAIL at this commit — that is what proves they
test the hole and not the fix. This repo has twice shipped a green test that could not
fail; a test written after its fix cannot demonstrate it ever could.

The forge: `author` was a free caller string, and B·1 counts a category-(a) source as
`author != actor` (stages.py:325). Three invented author names bought n=3/3 with zero
dispatches — at stakes 3 (`ctx.governance_gated = "R1"`); at stakes 1 B·1 short-circuits
to `n=1 (single source)` and the forge does not reproduce.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

from ancient_games.ctx import Ctx
from ancient_games.hybrid.registry import load_tools
from ancient_games.hybrid.tools import (corroborate as corroborate_tool, dispatch as dispatch_tool,
                                        ingest_return as ingest_tool, record_claim as record_claim_tool)
from ancient_games.hybrid.types import ToolEnv

ROOT = Path(__file__).resolve().parent.parent
TOOLS = load_tools()
ACTION = "claim the thing"
CLAIM = "C1"
FORGED = ("ghost-a", "ghost-b", "ghost-c")
FRAMINGS = ("f1", "f2", "f3")


def _env(tmp_path):
    """stakes 3 via governance_gated=R1 — n_required 3, so three sources are needed."""
    ctx = Ctx()
    ctx.actor = {ACTION: "MAIN"}
    ctx.governance_gated = "R1"
    return ToolEnv("tif", str(tmp_path / "j.jsonl"), ctx, cwd=str(tmp_path), tools=TOOLS)


def _corroborate(env):
    return corroborate_tool.run(env, {"action": ACTION, "claims": [{"claim_id": CLAIM, "kind": "judgment"}]})


# --- step 0: the two forges ---------------------------------------------------------------
def test_forge_via_record_claim_is_refused(tmp_path):
    env = _env(tmp_path)
    for author, framing in zip(FORGED, FRAMINGS):
        r = record_claim_tool.run(env, {"claim_id": CLAIM, "author": author, "actor": "MAIN", "kind": "judgment",
                                        "text": "the thing holds", "evidence_type": "command",
                                        "evidence_ref": "$ true", "framing": framing})
        assert r.ok is False, f"a claim authored by the never-dispatched {author!r} was recorded"
    assert "n=3/3" not in _corroborate(env).value.exit_line


def test_forge_via_ingest_return_is_refused(tmp_path):
    env = _env(tmp_path)
    for agent_id, framing in zip(FORGED, FRAMINGS):
        r = ingest_tool.run(env, {"agent_id": agent_id, "actor": "MAIN", "framing": framing,
                                  "fields": {"CLAIMS": [{"claim_id": CLAIM, "kind": "judgment",
                                                         "text": "the thing holds", "evidence_type": "command",
                                                         "evidence_ref": "$ true", "framing": framing}]}})
        assert r.ok is False, f"a return from the never-dispatched {agent_id!r} was ingested"
    assert "n=3/3" not in _corroborate(env).value.exit_line


# --- step 1 (F1): the refusal names the admissible set, and the legal writers still write ------
def test_refusal_names_the_admissible_authors(tmp_path):
    env = _env(tmp_path)
    r = record_claim_tool.run(env, {"claim_id": CLAIM, "author": "ghost-a", "actor": "MAIN", "kind": "judgment",
                                    "text": "the thing holds", "evidence_type": "command", "evidence_ref": "$ true"})
    assert r.reason == ("invalid-args: author must be MAIN, or an agent_id this run dispatched (MAIN), "
                        "got 'ghost-a' (str)")


def test_main_still_authors(tmp_path):
    env = _env(tmp_path)
    r = record_claim_tool.run(env, {"claim_id": CLAIM, "author": "MAIN", "actor": "agent-1", "kind": "judgment",
                                   "text": "the thing holds", "evidence_type": "command", "evidence_ref": "$ true"})
    assert r.ok is True, r.reason
    assert r.value["author"] == "MAIN"


def test_a_dispatched_agent_still_authors_by_both_writers(tmp_path):
    """The cost of authoring is now a journaled, I5-capped dispatch — not a typed string."""
    env = _env(tmp_path)
    d = dispatch_tool.run(env, {"role": "researcher", "framing": "f1", "agent_id": "adv-1"})
    assert d.ok is True, d.reason
    r = record_claim_tool.run(env, {"claim_id": CLAIM, "author": "adv-1", "actor": "MAIN", "kind": "judgment",
                                    "text": "the thing holds", "evidence_type": "command",
                                    "evidence_ref": "$ true", "framing": "f1"})
    assert r.ok is True, r.reason
    i = ingest_tool.run(env, {"agent_id": "adv-1", "actor": "MAIN", "framing": "f2",
                              "fields": {"CLAIMS": [{"claim_id": CLAIM, "kind": "judgment", "text": "the thing holds",
                                                     "evidence_type": "command", "evidence_ref": "$ true"}]}})
    assert i.ok is True, i.reason


def test_another_runs_dispatch_does_not_authorise_this_run(tmp_path):
    """`eligible_authors` reads `Journal.read()` (run-scoped). Were it `read_all()`, a dispatch
    recorded by run A would buy run B an author."""
    path = tmp_path / "j.jsonl"  # both runs write the same file; only the run_id differs
    a = ToolEnv("run-a", str(path), Ctx(), cwd=str(tmp_path), tools=TOOLS)
    assert dispatch_tool.run(a, {"role": "researcher", "framing": "f1", "agent_id": "adv-1"}).ok is True
    b = _env(tmp_path)  # run "tif", same journal file
    r = record_claim_tool.run(b, {"claim_id": CLAIM, "author": "adv-1", "actor": "MAIN", "kind": "judgment",
                                  "text": "the thing holds", "evidence_type": "command", "evidence_ref": "$ true"})
    assert r.ok is False and "this run dispatched (MAIN)" in r.reason


# --- step 1 (F1): the historic journals already satisfy the new rule ---------------------------
def test_historic_journals_authored_only_under_eligible_names():
    """Pins the "breaks nothing" claim rather than asserting it: F1 changes what `corroborate`
    counts, so every stored journal must already obey the rule, per run_id."""
    journals = sorted(ROOT.glob("ablation/runs/**/*.jsonl"))
    assert journals, "no stored journals found — this test would pass vacuously"
    for path in journals:
        by_run: dict[str, tuple[set[str], set[str]]] = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            e = json.loads(line)
            authors, dispatched = by_run.setdefault(e.get("run_id"), (set(), set()))
            if e.get("event") == "claim_recorded":
                authors.add(e["author"])
            elif e.get("event") == "dispatch":
                dispatched.add(e["agent_id"])
        for run_id, (authors, dispatched) in by_run.items():
            assert authors <= {"MAIN"} | dispatched, (path, run_id, sorted(authors - ({"MAIN"} | dispatched)))


# --- step 1 (F1): a third `claim_recorded` writer must not appear silently ---------------------
SANCTIONED_CLAIM_RECORDED_WRITERS = {
    "ancient_games/journal.py",                    # the ingest_return mirror (guarded in ingest_return.py)
    "ancient_games/hybrid/tools/record_claim.py",  # the direct writer
}


def _claim_recorded_writers() -> set[str]:
    """Every shipped module (never the tests) that CALLS `.claim_recorded(...)`, by repo-relative
    path. The definition site inside journal.py is a FunctionDef, not a Call, so it is not counted;
    journal.py appears here only for the `ingest_return` mirror at journal.py:271."""
    out = set()
    for path in sorted(ROOT.glob("ancient_games/**/*.py")) + sorted(ROOT.glob("ablation/**/*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "claim_recorded"):
                out.add(path.relative_to(ROOT).as_posix())
    return out


def test_claim_recorded_writers_are_the_sanctioned_set():
    """A third writer would re-open the F1 hole quietly: the author check lives at the two call
    sites, not in `journal.py`, which records events and is not the gate."""
    assert _claim_recorded_writers() == SANCTIONED_CLAIM_RECORDED_WRITERS
