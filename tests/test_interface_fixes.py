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
import subprocess
import sys
from pathlib import Path

import pytest

from ablation import fixtures

from ancient_games.ctx import Ctx
from ancient_games.hybrid import cli
from ancient_games.hybrid.registry import load_tools
from ancient_games.hybrid.tools import (corroborate as corroborate_tool, dispatch as dispatch_tool,
                                        guard as guard_tool,
                                        ingest_return as ingest_tool, record_check as record_check_tool,
                                        record_claim as record_claim_tool)
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


# --- step 2 (F2): record_check validates its fields, and a bad one exits 2 ---------------------
VALID_CHECK = {"claim_id": CLAIM, "mechanism": "suite-count", "command": "pytest -q",
               "expected": "318 passed", "observed": "318 passed"}
BAD_CHECKS = {
    "mechanism": dict(VALID_CHECK, mechanism="eyeballed-it"),
    "bare-other": dict(VALID_CHECK, mechanism="other:"),
    "pre_fix_result": dict(VALID_CHECK, pre_fix_result="PASS"),
    "expected": dict(VALID_CHECK, expected=["318 passed"]),
    "observed": dict(VALID_CHECK, observed={"n": 318}),
    "falsifies": dict(VALID_CHECK, falsifies="0 matches or file missing"),
}


@pytest.mark.parametrize("name", sorted(BAD_CHECKS))
def test_bad_record_check_field_is_invalid_args_never_internal_error(name, tmp_path):
    r = record_check_tool.run(_env(tmp_path), dict(BAD_CHECKS[name]))
    assert r.ok is False
    field = "mechanism" if name == "bare-other" else name
    assert r.reason.startswith(f"invalid-args: {field} must be "), r.reason


def test_bad_falsifies_still_enumerates_the_admissible_claim_ids(tmp_path):
    """The prefix is gained WITHOUT losing the enumerated detail — that detail is the
    admissible-alternatives content, and is why this field has had 0 failures since it was added."""
    env = _env(tmp_path)
    assert record_claim_tool.run(env, {"claim_id": CLAIM, "author": "MAIN", "actor": "agent-1", "kind": "judgment",
                                       "text": "the thing holds", "evidence_type": "command",
                                       "evidence_ref": "$ true"}).ok is True
    r = record_check_tool.run(env, dict(VALID_CHECK, falsifies="0 matches or file missing"))
    assert r.reason == ("invalid-args: falsifies must be a claim_id — put the condition in `expected` "
                        f"(this call's claim_id is {CLAIM!r}; claim_ids recorded in this run: ['{CLAIM}']), "
                        "got '0 matches or file missing' (str)")


def test_other_prefixed_mechanism_is_still_accepted(tmp_path):
    r = record_check_tool.run(_env(tmp_path), dict(VALID_CHECK, mechanism="other:my-thing"))
    assert r.ok is True, r.reason
    assert r.value["mechanism"] == "other:my-thing"


def test_a_valid_call_writes_the_same_event_as_before(tmp_path):
    """The validators are a gate, not a rewrite: a sound call's event is unchanged."""
    r = record_check_tool.run(_env(tmp_path), dict(VALID_CHECK))
    assert r.ok is True, r.reason
    assert {k: v for k, v in r.value.items() if k not in ("ts", "run_id")} == {
        "event": "check_executed", "claim_id": CLAIM, "falsifies": CLAIM, "mechanism": "suite-count",
        "command": "pytest -q", "expected": "318 passed", "observed": "318 passed", "pre_fix_result": None}


@pytest.fixture(scope="module")
def manifest(tmp_path_factory):
    d = tmp_path_factory.mktemp("if-cli")
    repo = fixtures.make_uc1(str(d / "repo"))
    p = subprocess.run([sys.executable, "-m", "ancient_games.hybrid", "init", "--run-id", "if",
                        "--journal", str(d / "j.jsonl"), "--cwd", repo], cwd=ROOT, capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    return json.loads(p.stdout)["manifest"]


def _call(manifest, tool, args):
    return subprocess.run([sys.executable, "-m", "ancient_games.hybrid", "--manifest", manifest,
                           "call", tool, json.dumps(args)], cwd=ROOT, capture_output=True, text=True)


@pytest.mark.parametrize("name", sorted(BAD_CHECKS))
def test_cli_exits_2_on_every_bad_record_check_field(name, manifest):
    """The exit code IS the defect: `cmd_call` keys EXIT_REFUSED on the `invalid-args:` prefix, so
    before F2 a bad `falsifies` returned a bare reason and the process exited 0 — a caller error
    reporting success."""
    p = _call(manifest, "record_check", BAD_CHECKS[name])
    out = json.loads(p.stdout)
    assert out["ok"] is False and out["refused_by"] is None, out
    assert out["reason"].startswith("invalid-args: "), out
    assert p.returncode == 2, p.stdout + p.stderr


# --- step 3 (F3): JSON in the tool-name slot is refused before anything is spent ---------------
def _cli(manifest, *argv):
    p = subprocess.run([sys.executable, "-m", "ancient_games.hybrid"]
                       + (["--manifest", manifest] if manifest else []) + list(argv),
                       cwd=ROOT, capture_output=True, text=True)
    return p


def test_json_in_the_tool_name_slot_is_refused_and_costs_nothing(tmp_path):
    """It was journaling a `tool_call` with `unknown-tool: {"claim_id"...` and spending budget:
    6 of the 8 live interface failures on harness >= v1.3, all in one run, 5.5% of its budget."""
    repo = fixtures.make_uc1(str(tmp_path / "repo"))
    journal = tmp_path / "j.jsonl"
    init = _cli(None, "init", "--run-id", "f3", "--journal", str(journal), "--cwd", repo)
    assert init.returncode == 0, init.stderr
    m = json.loads(init.stdout)["manifest"]
    before = journal.read_text(encoding="utf-8")
    p = _cli(m, "call", '{"claim_id": "C1", "author": "MAIN"}', "{}")
    assert p.returncode == 2, p.stdout + p.stderr
    assert "the tool NAME goes first" in json.loads(p.stderr)["error"]
    assert journal.read_text(encoding="utf-8") == before  # nothing appended, no budget spent


def test_a_genuine_unknown_tool_is_unaffected(tmp_path):
    """The refusal is keyed on a leading `{`, not on "not a known tool": an ordinary typo must
    still journal `unknown-tool: bogus` exactly as before (tests/test_ablation_harness.py pins it)."""
    repo = fixtures.make_uc1(str(tmp_path / "repo"))
    journal = tmp_path / "j.jsonl"
    m = json.loads(_cli(None, "init", "--run-id", "f3b", "--journal", str(journal), "--cwd", repo).stdout)["manifest"]
    p = _cli(m, "call", "bogus", "{}")
    assert p.returncode == 1 and json.loads(p.stdout)["reason"] == "unknown-tool: bogus"
    assert '"unknown-tool: bogus"' in journal.read_text(encoding="utf-8")


# --- step 4 (F4): a note keyed by (owner, field), and the class of error it prevents -----------
NEVER_PASSED = "never passed by the caller"


def test_no_note_claims_a_field_is_never_caller_passed_when_a_tool_requires_it():
    """The point of the fix: `NOTES` was keyed by bare field name, so Claim.actor's note printed
    against `record_claim.actor` — a REQUIRED input — telling every agent not to pass it. This
    catches the class, not the instance."""
    offenders = [(name, arg) for name, t in TOOLS.items() for arg in t.manifest["inputs"]
                 if NEVER_PASSED in (cli.note_for(name, arg) or "")]
    assert offenders == []


def test_the_dataclass_note_survived_the_re_keying():
    """It was moved, not deleted: Claim.actor really is filled by corroborate."""
    assert NEVER_PASSED in cli.note_for("Claim", "actor")
    assert NEVER_PASSED in cli.NOTES[("Claim", "actor")]
    schema = cli.tools_schema(TOOLS)
    assert schema.count(NEVER_PASSED) == 3  # Claim.n_required, Claim.stakes, Claim.actor — no tool input
    assert "actor: str  # the actor of the action the claim is about" in schema


def test_note_for_falls_back_to_the_bare_key():
    """Bare keys still apply to every owner — only the collisions are re-keyed."""
    assert cli.note_for("record_claim", "kind") == cli.NOTES["kind"]
    assert cli.note_for("anything-at-all", "governance_gated") == cli.NOTES["governance_gated"]
    assert cli.note_for("record_claim", "no-such-field") is None


# --- step 5 (F5): rejections enumerate their legal values --------------------------------------
def test_unknown_action_names_the_actions_that_have_an_actor(tmp_path):
    env = _env(tmp_path)
    env.ctx.actor = {"land-spec": "designer", ACTION: "MAIN"}
    r = corroborate_tool.run(env, {"action": "no-such-action", "claims": [{"claim_id": CLAIM, "kind": "judgment"}]})
    assert r.ok is False
    assert r.reason == ("ctx.actor has no entry for action 'no-such-action' (set at C·3/C·4 or by D); "
                        f"actions with an actor: ['{ACTION}', 'land-spec']")


def test_a_legal_action_is_unchanged(tmp_path):
    env = _env(tmp_path)
    assert _corroborate(env).ok is True


COMMIT_TO_MASTER = {"name": "commit-to-master", "refs": [{"path": "master", "mode": "mutate", "verb": "commit"}]}


def test_a_tripwire_keyed_by_a_matched_ref_path_alias_is_accepted(tmp_path):
    """hubs is ['default-branch-history'], but 'master' — the path of the ref that matched into it —
    is equally legal (H6). Printing hubs alone would have misreported exactly this case."""
    env = _env(tmp_path)
    r = guard_tool.run(env, {"action": dict(COMMIT_TO_MASTER, tripwires={"master": "git diff --stat"})})
    assert r.ok is True, r.reason
    unmatched, allowed = guard_tool.unmatched_tripwire_keys(
        guard_tool.guard_action({"action": dict(COMMIT_TO_MASTER, tripwires={"master": "x"})}))
    assert unmatched == [] and allowed == ["default-branch-history", "master"]


def test_a_bad_tripwire_key_enumerates_both_admissible_keys(tmp_path):
    r = guard_tool.run(_env(tmp_path), {"action": dict(COMMIT_TO_MASTER, tripwires={"nonsense": "x"})})
    assert r.ok is False
    assert r.reason.startswith("invalid-args: action.tripwires must be one of "
                               "['default-branch-history', 'master'] — a hub element of this action"), r.reason


def test_the_empty_hub_case_still_carries_the_consumers_clause(tmp_path):
    """Where there are no hubs the admissible set is empty, and an empty set is not guidance —
    the `consumers` clause is the only part telling the caller what to do next."""
    action = {"name": "edit", "refs": [{"path": "research/stability.py", "mode": "mutate"}],
              "tripwires": {"loop/program_db.jsonl": "x"}}
    r = guard_tool.run(_env(tmp_path), {"action": action})
    assert r.ok is False
    assert "must be one of [] — " in r.reason
    assert "must be declared in that ref's `consumers` first" in r.reason


# --- step 5a: validation is split from the write, and the split changed nothing ----------------
def test_validate_is_pure_and_agrees_with_run(tmp_path):
    """`validate` must reach the same verdict `run` does on every arg-shape case, without touching
    the journal — that equivalence is what lets `ingest_return` check a whole batch before writing."""
    cases = [
        (record_claim_tool, {"claim_id": CLAIM, "author": "MAIN", "kind": "judgment", "text": "t",
                             "evidence_type": "command", "evidence_ref": "r"}, None),
        (record_claim_tool, {"claim_id": "", "author": "MAIN", "kind": "judgment",
                             "evidence_type": "command"}, "claim_id"),
        (record_claim_tool, {"claim_id": CLAIM, "author": "MAIN", "kind": "suite",
                             "evidence_type": "command"}, "kind"),
        (record_claim_tool, {"claim_id": CLAIM, "author": "MAIN", "kind": "judgment",
                             "evidence_type": "(opinion)"}, "evidence_type"),
        (record_check_tool, dict(VALID_CHECK), None),
        (record_check_tool, dict(VALID_CHECK, mechanism="eyeballed-it"), "mechanism"),
        (record_check_tool, dict(VALID_CHECK, pre_fix_result="PASS"), "pre_fix_result"),
        (record_check_tool, dict(VALID_CHECK, expected=["a"]), "expected"),
    ]
    for tool, args, field in cases:
        v = tool.validate(dict(args))
        if field is None:
            assert v is None, (tool.MANIFEST["name"], args, v)
        else:
            assert v is not None and v.reason.startswith(f"invalid-args: {field} must be "), (args, v)
        run = tool.run(_env(tmp_path), dict(args))
        assert (v is None) == run.ok, (tool.MANIFEST["name"], args, v, run)


def test_validate_writes_nothing(tmp_path):
    env = _env(tmp_path)
    record_claim_tool.validate({"claim_id": CLAIM, "author": "MAIN", "kind": "judgment",
                                "evidence_type": "command", "evidence_ref": "r"})
    record_check_tool.validate(dict(VALID_CHECK))
    assert not Path(env.journal_path).exists()
