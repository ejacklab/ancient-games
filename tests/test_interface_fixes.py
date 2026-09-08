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
# 5c: was two. `journal.ingest_return`'s mirror was the second, and it is gone — `ingest_return`
# now delegates to this same tool, so there is exactly ONE writer of `claim_recorded` in the tree.
SANCTIONED_CLAIM_RECORDED_WRITERS = {
    "ancient_games/hybrid/tools/record_claim.py",  # the only writer
}


def _claim_recorded_writers() -> set[str]:
    """Every shipped module (never the tests) that CALLS `.claim_recorded(...)`, by repo-relative
    path. The definition site inside journal.py is a FunctionDef, not a Call, so it is not counted."""
    out = set()
    for path in sorted(ROOT.glob("ancient_games/**/*.py")) + sorted(ROOT.glob("ablation/**/*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "claim_recorded"):
                out.add(path.relative_to(ROOT).as_posix())
    return out


def test_claim_recorded_writers_are_the_sanctioned_set():
    """A second writer would re-open the F1 hole quietly: the author check, the D-KIND rule and
    every future guard live at the one call site, not in `journal.py`, which records events and is
    not the gate."""
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


def test_bad_falsifies_names_the_one_value_it_may_take(tmp_path):
    """H18 narrowed the admissible set from "a claim_id recorded in this run" to exactly one value —
    this call's own claim_id — because B·1 counts a check only when the two agree. Naming the single
    legal value is tighter than enumerating every recorded id, and the `expected` guidance that gave
    this field 0 failures since ABLATION_1's H3 is kept verbatim."""
    r = record_check_tool.run(_env(tmp_path), dict(VALID_CHECK, falsifies="0 matches or file missing"))
    assert r.reason == (f"invalid-args: falsifies must be this call's own claim_id, {CLAIM!r} — a check is "
                        "evidence FOR the claim named in `claim_id`, and B·1 counts it only when the two "
                        "agree, so a different value here counts for nothing. Put a CONDITION in `expected`; "
                        "to back claim '0 matches or file missing', pass claim_id='0 matches or file missing', "
                        "got '0 matches or file missing' (str)")


def test_the_same_check_counts_the_same_through_both_doors(tmp_path):
    """H18 itself: one byte-identical entry used to reach n=0/2 through `record_check` and n=1/2
    through `ingest_return`, because the mirror collapsed claim_id to `falsifies` and record_check
    did not. Both doors now apply one rule, so both give the same answer — here, both refuse."""
    entry = {"claim_id": "C1-check", "falsifies": CLAIM, "mechanism": "suite-count",
             "command": "pytest -q", "expected": "111 passed", "observed": "111 passed"}
    direct = record_check_tool.run(_dispatched(tmp_path), dict(entry))
    viareturn = ingest_tool.run(_dispatched(tmp_path), {"agent_id": "adv-1", "actor": "MAIN",
                                                        "fields": {"CLAIMS": [dict(entry)]}})
    assert direct.ok is False and viareturn.ok is False
    assert direct.reason.startswith("invalid-args: falsifies must be this call's own claim_id, 'C1-check'")
    assert viareturn.reason.startswith("invalid-args: fields.CLAIMS[0].falsifies must be this call's own claim_id")
    # and the shape that DOES count is accepted identically through both
    ok_entry = dict(entry, claim_id=CLAIM)
    assert record_check_tool.run(_dispatched(tmp_path), dict(ok_entry)).ok is True
    assert ingest_tool.run(_dispatched(tmp_path), {"agent_id": "adv-1", "actor": "MAIN",
                                                   "fields": {"CLAIMS": [dict(ok_entry)]}}).ok is True


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


def test_ingest_return_schema_names_the_return_contract_and_closed_world_is_not_writer_only():
    schema = cli.tools_schema(TOOLS)
    fields = next(line for line in schema.splitlines() if line.startswith("  fields: dict"))
    assert all(name in fields for name in ("CLAIMS", "REPORT_BACK", "closed_world"))
    assert all("record_claim only" not in note for note in cli.NOTES.values())


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


# --- steps 5b/5c/5d: one guarded writer, one atomic batch, D-KIND on both paths ----------------
def _dispatched(tmp_path, agent="adv-1"):
    env = _env(tmp_path)
    assert dispatch_tool.run(env, {"role": "researcher", "framing": "f1", "agent_id": agent}).ok
    return env


def test_ingest_return_accepts_both_claims_shapes_its_schema_documents(tmp_path):
    """The contract note is an interface: its claim and check shapes must round-trip unchanged."""
    env = _dispatched(tmp_path, "contract-agent")
    r = ingest_tool.run(env, {"agent_id": "contract-agent", "actor": "MAIN", "framing": "static-scan", "fields": {
        "REPORT_BACK": "/agents/contract.md", "FOLLOW_ON": [], "NOT_DONE": [], "CLAIMS": [
            {"claim_id": "graph-memory-unused", "kind": "executable", "text": "graph memory is unused",
             "evidence_type": "command", "evidence_ref": "python3 -c 'import loop.graph_memory'",
             "closed_world": "AST scan covers every module"},
            # H18: a check is evidence FOR the claim in `claim_id`; `falsifies` restates it. The
            # collapse this used to pin is gone — both doors now apply the same rule.
            {"claim_id": "graph-memory-unused", "falsifies": "graph-memory-unused", "mechanism": "suite-count",
             "command": "pytest -q", "expected": "all pass", "observed": "all pass"},
        ]}})
    assert r.ok is True, r.reason
    evs = _events(env)
    assert [event["event"] for event in evs] == ["dispatch", "return", "claim_recorded", "check_executed"]
    assert evs[2]["closed_world"] == "AST scan covers every module"
    # counted for B·1 (c), which requires claim_id == falsifies — now the caller's own doing, not a
    # silent rewrite by the mirror
    assert evs[3]["claim_id"] == "graph-memory-unused" and evs[3]["falsifies"] == "graph-memory-unused"


def _events(env):
    from ancient_games.journal import Journal
    return Journal(env.journal_path, env.run_id).read()


def test_ingest_return_mirrors_claims_through_the_guarded_writers(tmp_path):
    """The mapping `journal.ingest_return` used, unchanged — ported here when the mirror moved into
    the tool (was tests/test_journal.py::test_ingest_return_mirrors_claims). The `claim_id` collapse
    on the second entry is load-bearing: B·1 (c) counts only check_executed{claim_id=X, falsifies=X}."""
    env = _dispatched(tmp_path, "tester-1")
    r = ingest_tool.run(env, {"agent_id": "tester-1", "actor": "coder-1", "framing": "adversarial", "fields": {
        "REPORT_BACK": "/agents/t.md",
        "CLAIMS": [{"claim_id": "c1", "kind": "judgment", "evidence_type": "file:line", "evidence_ref": "a.py:3"},
                   {"claim_id": "c1", "kind": "executable", "falsifies": "c1", "mechanism": "pytest-fail-first",
                    "command": "pytest -q", "expected": "pass", "observed": "pass", "pre_fix_result": "FAIL"},
                   {"claim_id": "c3", "kind": "executable", "evidence_type": "command", "evidence_ref": "sha256sum f",
                    "mechanism": "hash-compare", "command": "sha256sum f", "expected": "abc", "observed": "abc"},
                   {"claim_id": "c2", "kind": "judgment", "evidence_type": "(opinion)"}],
        "FOLLOW_ON": [], "NOT_DONE": []}})
    assert r.ok is True, r.reason
    evs = [e for e in _events(env) if e["event"] != "dispatch"]
    assert [e["event"] for e in evs] == ["return", "claim_recorded", "check_executed", "check_executed"]
    assert evs[1]["author"] == "tester-1" and evs[1]["actor"] == "coder-1" and evs[1]["framing"] == "adversarial"
    assert evs[2]["claim_id"] == "c1" and evs[2]["falsifies"] == "c1" and evs[2]["pre_fix_result"] == "FAIL"
    assert evs[3]["claim_id"] == "c3" and evs[3]["falsifies"] == "c3" and evs[3]["mechanism"] == "hash-compare"


def test_a_bad_entry_writes_nothing_at_all(tmp_path):
    """Atomicity: the `return` event and its claims are one unit. Before 5b a bad entry half-way
    down left the earlier claims and the `return` on disk while the call reported failure, so a
    retry duplicated them."""
    env = _dispatched(tmp_path)
    good = {"claim_id": "C{}", "kind": "judgment", "text": "t", "evidence_type": "command", "evidence_ref": "x"}
    claims = [dict(good, claim_id="C1"), dict(good, claim_id="C2"),
              {"claim_id": "C3", "falsifies": "C3", "kind": "executable", "mechanism": "eyeballed-it",
               "command": "x", "expected": "0", "observed": "0"}]
    r = ingest_tool.run(env, {"agent_id": "adv-1", "actor": "MAIN", "fields": {"CLAIMS": claims}})
    assert r.ok is False
    assert r.reason.startswith("invalid-args: fields.CLAIMS[2].mechanism must be "), r.reason
    assert [e["event"] for e in _events(env)] == ["dispatch"]  # not even the `return` event


@pytest.mark.parametrize("entry,field", [
    ({"claim_id": "C1", "kind": "suite", "evidence_type": "command", "evidence_ref": "x"}, "kind"),
    ({"claim_id": "", "kind": "judgment", "evidence_type": "command", "evidence_ref": "x"}, "claim_id"),
    ({"claim_id": "C1", "falsifies": "C1", "mechanism": "suite-count", "command": "x",
      "expected": "0", "observed": ["0"]}, "observed"),
])
def test_a_bad_claims_entry_is_invalid_args_naming_its_index(entry, field, tmp_path):
    env = _dispatched(tmp_path)
    r = ingest_tool.run(env, {"agent_id": "adv-1", "actor": "MAIN", "fields": {"CLAIMS": [entry]}})
    assert r.ok is False and r.reason.startswith(f"invalid-args: fields.CLAIMS[0].{field} must be "), r.reason


def test_a_non_object_claims_entry_is_named_not_a_traceback(tmp_path):
    env = _dispatched(tmp_path)
    r = ingest_tool.run(env, {"agent_id": "adv-1", "fields": {"CLAIMS": ["a bare string"]}})
    assert r.ok is False and r.reason.startswith("invalid-args: fields.CLAIMS[0] must be an object")
    assert "internal-error" not in r.reason  # it was an AttributeError out of classify_event


def test_cli_exits_2_on_a_bad_claims_entry(manifest):
    """F2's defect survived in the mirror: the same bad mechanism was `invalid-args` + exit 2
    through record_check and `internal-error` + exit 0 through ingest_return. Delegation ends that."""
    p = _call(manifest, "dispatch", {"role": "researcher", "framing": "f1", "agent_id": "adv-cli"})
    assert p.returncode == 0, p.stdout + p.stderr
    p = _call(manifest, "ingest_return", {"agent_id": "adv-cli", "fields": {"CLAIMS": [
        {"claim_id": "C9", "falsifies": "C9", "mechanism": "eyeballed-it", "command": "x",
         "expected": "0", "observed": "0"}]}})
    out = json.loads(p.stdout)
    assert out["ok"] is False and out["reason"].startswith("invalid-args: fields.CLAIMS[0].mechanism"), out
    assert p.returncode == 2, p.stdout + p.stderr


# --- 5d: D-KIND applies to a helper's report ---------------------------------------------------
ABSENCE = "the six helpers are dead — nothing calls them"
CLOSED_WORLD = "AST over every .py + grep for the name as a string + no getattr/globals() idioms"


def _returned_claim(env, **extra):
    r = ingest_tool.run(env, {"agent_id": "adv-1", "actor": "agent-x", "framing": "f1", "fields": {
        "CLAIMS": [dict({"claim_id": CLAIM, "kind": "executable", "text": ABSENCE,
                         "evidence_type": "command", "evidence_ref": "$ grep -r"}, **extra)]}})
    assert r.ok is True, r.reason
    return [e for e in _events(env) if e["event"] == "claim_recorded"][0]


def test_a_helper_cannot_self_declare_executable_on_absence_text(tmp_path):
    """The hole this closes: the same claim was `judgment` through record_claim and stayed
    `executable` through a helper's return, which unlocked B·1 (c) — the helper's own checks
    counting as its own corroboration."""
    ev = _returned_claim(_dispatched(tmp_path))
    assert (ev["kind"], ev["kind_override"], ev["closed_world"]) == ("judgment", False, None)


def test_a_helper_keeps_executable_by_stating_why_its_space_is_complete(tmp_path):
    """The ratified policy: a helper MAY override, only in writing, and the override is then
    journaled, disclosed at the gate and gate-controlled like MAIN's own."""
    ev = _returned_claim(_dispatched(tmp_path), closed_world=CLOSED_WORLD)
    assert (ev["kind"], ev["kind_override"], ev["closed_world"]) == ("executable", True, CLOSED_WORLD)
    assert ev["author"] == "adv-1"  # the gate sees WHOSE closed world it is


def test_a_helpers_override_is_visible_to_the_disclosure_machinery(tmp_path):
    """All four D-KIND consumers key on `kind_overrides()`. A return-sourced override was invisible
    to every one of them, which is what let it past a grant that exists to refuse exactly this."""
    from ancient_games.journal import kind_overrides
    env = _dispatched(tmp_path)
    _returned_claim(env, closed_world=CLOSED_WORLD)
    ov = kind_overrides(_events(env), env.run_id)
    assert [(o["claim_id"], o["author"], o["closed_world"]) for o in ov] == [(CLAIM, "adv-1", CLOSED_WORLD)]
