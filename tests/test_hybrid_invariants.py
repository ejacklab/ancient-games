"""HYBRID_SPEC §4 — one FAIL input and one PASS input per invariant, each asserted on the
real predicate's return (`check_invariants`) or the real tool's `ToolResult` (`done`,
`commit`, the loader). Journals are built with the real `Journal` and `tool_call_event`."""
from __future__ import annotations

import os
import subprocess
import textwrap

import pytest

from ancient_games.ctx import Ctx
from ancient_games.hybrid.invariants import PRIORITY, check_invariants, pick_by_priority, Refusal, RESTRICTED
from ancient_games.hybrid.loop import strip_corroboration
from ancient_games.hybrid.registry import ManifestError, load_tools, register
from ancient_games.hybrid.tools import _shared as shared
from ancient_games.hybrid.tools import done as done_tool, commit as commit_tool, prove as prove_tool
from ancient_games.hybrid.types import Call, ToolEnv, ToolResult
from ancient_games.journal import Journal

TOOLS = load_tools()
GUARD_A = Call("guard", {"action": {"name": "edit-a", "refs": [{"path": "a.py", "mode": "mutate"}]}})
GUARD_COMMIT = Call("guard", {"action": {"name": "commit-to-master", "refs": [{"path": "master", "mode": "mutate", "verb": "commit"}]}})
COMMIT = Call("commit", {"message": "m"})
PROBE = Call("guard", {"action": {"name": "run-load_holdout-probe", "refs": [{"path": "eval.partitions.load_holdout", "mode": "invoke"}]}})
OWNER_AID = "invoke:['eval.partitions.load_holdout']"
OWNER_ROWS = " [owner rows: R3 via direct eval.partitions.load_holdout]"  # H1: the reason names the matched row


@pytest.fixture
def repo(tmp_path):
    root = str(tmp_path / "repo")
    os.makedirs(root)
    for argv in (("init", "-q"), ("config", "user.email", "t@t"), ("config", "user.name", "t"), ("config", "commit.gpgsign", "false")):
        subprocess.run(["git", *argv], cwd=root, check=True, capture_output=True)
    _write(root, "a.py", "x = 1\n")
    _write(root, "eval/protocol.json", "{}\n")
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=root, check=True, capture_output=True)
    return root


def _write(root, rel, content):
    os.makedirs(os.path.dirname(os.path.join(root, rel)) or root, exist_ok=True)
    with open(os.path.join(root, rel), "w") as fh:
        fh.write(content)


@pytest.fixture
def journal(tmp_path):
    return Journal(str(tmp_path / "j.jsonl"), "inv")


def ok(journal, call, value=None, exit_type=None):
    class V:
        pass
    v = V()
    if exit_type:
        v.exit_type = exit_type
    return journal.append(shared.tool_call_event(call, [], ToolResult(True, v if exit_type else value)))


def refused(journal, call, inv):
    return journal.append(shared.tool_call_event(call, [inv], refused_by=inv, reason="test"))


def approve(journal, gate, aid):
    return journal.append({"event": "approval_recorded", "action_id": aid, "gate": gate, "approver": "ej", "note": "t"})


def env_for(journal, repo, ctx=None):
    return ToolEnv(journal.run_id, journal.path, ctx if ctx is not None else Ctx(), cwd=repo, tools=TOOLS)


def check(call, journal, repo):
    return check_invariants(call, Ctx(), journal.read(), TOOLS, cwd=repo)


# I1′ -------------------------------------------------------------------------------
def test_i1_fail_unguarded_change(journal, repo):
    _write(repo, "a.py", "x = 2\n")
    ok(journal, GUARD_COMMIT)
    assert check(COMMIT, journal, repo) == [Refusal("I1", "unguarded changed files: ['a.py']")]


def test_i1_pass_covered_change(journal, repo):
    _write(repo, "a.py", "x = 2\n")
    ok(journal, GUARD_A)
    ok(journal, GUARD_COMMIT)
    assert check(COMMIT, journal, repo) == []


def test_i1_guard_before_commit_1_then_reedit_then_commit_2_refused(journal, repo):
    """Adversarial C, as a predicate: the window is post-last-commit; a fresh guard re-covers."""
    _write(repo, "a.py", "x = 2\n")
    ok(journal, GUARD_A)
    ok(journal, GUARD_COMMIT)
    approve(journal, "checkpoint", "commit:['master']")
    r = commit_tool.run(env_for(journal, repo), {"message": "edit a.py"})
    assert r.ok and r.value["hash"]
    ok(journal, COMMIT, r.value)
    _write(repo, "a.py", "x = 3\n")  # silent re-edit
    ok(journal, GUARD_COMMIT)
    assert check(COMMIT, journal, repo) == [Refusal("I1", "unguarded changed files: ['a.py']")]
    ok(journal, Call("guard", {"action": {"name": "edit-a-again", "refs": [{"path": "a.py", "mode": "mutate"}]}}))
    assert check(COMMIT, journal, repo) == []


def test_i1_refused_guard_does_not_cover(journal, repo):
    _write(repo, "a.py", "x = 2\n")
    refused(journal, GUARD_A, "I4")
    assert check(COMMIT, journal, repo) == [Refusal("I1", "unguarded changed files: ['a.py']")]


def test_i1_exact_path_not_prefix(journal, repo):
    """M3: a directory-shaped guard ref does not cover a file under it."""
    _write(repo, "eval/protocol.json", "{\"a\": 1}\n")
    ok(journal, Call("guard", {"action": {"name": "edit-eval", "refs": [{"path": "eval/", "mode": "mutate"}]}}))
    approve(journal, "owner", "R1")
    assert check(COMMIT, journal, repo) == [Refusal("I1", "unguarded changed files: ['eval/protocol.json']")]


def test_i1_untracked_file_is_in_changed_and_ignored_file_is_not(journal, repo):
    """v1.1 D-A: changed = diff ∪ untracked (respecting .gitignore)."""
    _write(repo, ".gitignore", "*.log\n")
    subprocess.run(["git", "add", ".gitignore"], cwd=repo, check=True); subprocess.run(["git", "commit", "-q", "-m", "ignore"], cwd=repo, check=True)
    _write(repo, "new.py", "n = 1\n")
    _write(repo, "x.log", "ignored\n")
    assert shared.changed_files(repo) == ["new.py"]
    assert check(COMMIT, journal, repo) == [Refusal("I1", "unguarded changed files: ['new.py']")]
    ok(journal, Call("guard", {"action": {"name": "add-new", "refs": [{"path": "new.py", "mode": "mutate"}]}}))
    assert check(COMMIT, journal, repo) == []


def test_i2_untracked_file_is_uncommitted_changes(journal, repo):
    ok(journal, Call("prove", {}), exit_type="PASS")
    _write(repo, "new.py", "n = 1\n")
    assert done_tool.run(env_for(journal, repo), {}) == ToolResult(False, None, "uncommitted-changes: ['new.py']")


# I2 (inside done) ------------------------------------------------------------------
def test_i2_pass_mutate_prove_commit_done(journal, repo):
    ok(journal, Call("rebuild_index", {}))
    ok(journal, Call("prove", {}), exit_type="PASS")
    ok(journal, COMMIT, {"hash": "h"})
    assert done_tool.run(env_for(journal, repo), {}) == ToolResult(True, "DONE", None)


def test_i2_fail_mutate_after_prove_stales(journal, repo):
    ok(journal, Call("prove", {}), exit_type="PASS")
    ok(journal, Call("rebuild_index", {}))
    assert done_tool.run(env_for(journal, repo), {}) == ToolResult(False, None, "prove-stale: rebuild_index")


def test_i2_refused_mutate_after_prove_does_not_stale(journal, repo):
    ok(journal, Call("prove", {}), exit_type="PASS")
    refused(journal, Call("rebuild_index", {}), "I4")
    assert done_tool.run(env_for(journal, repo), {}).ok


def test_i2_no_prove_pass_and_dirty_tree(journal, repo):
    assert done_tool.run(env_for(journal, repo), {}) == ToolResult(False, None, "no-prove-pass")
    ok(journal, Call("prove", {}), exit_type="RETURN_TO_PLANNER")
    assert done_tool.run(env_for(journal, repo), {}).reason == "no-prove-pass"
    ok(journal, Call("prove", {}), exit_type="PASS")
    _write(repo, "a.py", "x = 2\n")  # a native edit, off-registry (D6): caught by clause (b)
    assert done_tool.run(env_for(journal, repo), {}) == ToolResult(False, None, "uncommitted-changes: ['a.py']")


# I3 (static + stripped ctx) --------------------------------------------------------
def test_i3_fail_non_uniform_signature_never_registers(tmp_path):
    bad = tmp_path / "bad_prove.py"
    bad.write_text(textwrap.dedent('''
        MANIFEST = {"name": "bad_prove", "inputs": {}, "outputs": "x", "side_effects": "read", "cost": "cheap",
                    "participates_in": ["I3"], "entrypoint": "run"}
        def run(ctx, journal, n_sources):
            return None
    '''))
    with pytest.raises(ManifestError, match=r"signature must be exactly \(env, args\)"):
        register(str(bad))


def test_i3_pass_prove_sees_no_corroboration_counts(journal, repo):
    ctx = Ctx()
    ctx.n_sources = {"c": 99}
    ctx.corroboration_capped = []
    ctx.framing = "f"
    ctx.siblings = ["/x"]
    view = strip_corroboration(ctx)
    assert isinstance(view, Ctx) and view.n_sources is None and view.corroboration_capped is None
    assert view.framing is None and view.siblings is None
    assert ctx.n_sources == {"c": 99}  # the real ctx is untouched
    assert RESTRICTED == {"prove", "done"}
    # the real prove executes against the view (L1): keys_set() works on a Ctx
    r = prove_tool.run(env_for(journal, repo, view), {"gate": "checkpoint"})
    assert r.ok and r.value.exit_type == "PASS"


# I4′ ---------------------------------------------------------------------------------
def test_i4a_fail_owner_gated_invoke_without_approval(journal, repo):
    assert check(PROBE, journal, repo) == [Refusal("I4", f"hard_blocked: no owner approval on record for {OWNER_AID}{OWNER_ROWS}")]


def test_i4a_pass_with_approval_then_spent_by_a_commit(journal, repo):
    approve(journal, "owner", OWNER_AID)
    assert check(PROBE, journal, repo) == []
    ok(journal, COMMIT, {"hash": "h"})  # an unrelated landing
    assert check(PROBE, journal, repo) == [Refusal("I4", f"hard_blocked: approval stale (predates last commit) for {OWNER_AID}{OWNER_ROWS}")]
    approve(journal, "owner", OWNER_AID)
    assert check(PROBE, journal, repo) == []


def test_i4b_fail_undeclared_owner_gated_mutation_at_commit(journal, repo):
    _write(repo, "eval/protocol.json", "{\"a\": 1}\n")
    ok(journal, Call("guard", {"action": {"name": "edit", "refs": [{"path": "eval/protocol.json", "mode": "mutate"}]}}))
    assert check(COMMIT, journal, repo) == [Refusal("I4", "hard_blocked: owner-gated file eval/protocol.json (R1) changed without approval")]
    approve(journal, "owner", "R1")
    assert check(COMMIT, journal, repo) == []


def test_i4_outranks_i1(journal, repo):
    _write(repo, "eval/protocol.json", "{\"a\": 1}\n")
    refusals = check(COMMIT, journal, repo)
    assert [r.invariant for r in refusals] == ["I4", "I1"]
    assert pick_by_priority(refusals).invariant == "I4"
    assert PRIORITY == ("I4", "I1", "I5", "I2", "I3")


def test_checkpoint_approval_spent_by_a_commit(journal, repo):
    """D13: checkpoint clearance is commit's own precondition; one approval clears one landing."""
    _write(repo, "a.py", "x = 2\n")
    assert commit_tool.run(env_for(journal, repo), {"message": "m"}) == ToolResult(False, None, "checkpoint-not-cleared")
    approve(journal, "checkpoint", "commit:['master']")
    r = commit_tool.run(env_for(journal, repo), {"message": "m"})
    assert r.ok
    ok(journal, COMMIT, r.value)
    _write(repo, "a.py", "x = 3\n")
    assert commit_tool.run(env_for(journal, repo), {"message": "m2"}).reason == "checkpoint-not-cleared"


# I5′ ---------------------------------------------------------------------------------
def test_i5_fail_fourth_parallel_dispatch(journal, repo):
    for f in "abc":
        ok(journal, Call("dispatch", {"role": "x", "framing": f}), f.upper())
    assert check(Call("dispatch", {"role": "x", "framing": "d"}), journal, repo) == [Refusal("I5", "live_dispatches=3, CAP=3, no slot")]


def test_i5_pass_dispatch_failed_and_ingest_return_free_slots(journal, repo):
    for f in "abc":
        ok(journal, Call("dispatch", {"role": "x", "framing": f}), f.upper())
    journal.append({"event": "dispatch_failed", "agent_id": "B", "reason": "timed out"})
    assert shared.live_dispatches(journal.read()) == 2
    assert check(Call("dispatch", {"role": "x", "framing": "d"}), journal, repo) == []
    ok(journal, Call("dispatch", {"role": "x", "framing": "d"}), "D")
    ok(journal, Call("ingest_return", {"agent_id": "A"}), ["return"])
    assert shared.live_dispatches(journal.read()) == 2
    refused(journal, Call("dispatch", {"role": "x", "framing": "e"}), "I5")  # a refused dispatch never counts
    assert shared.live_dispatches(journal.read()) == 2


def test_i5_is_computed_from_the_journal_not_a_counter(journal, repo):
    """DECISIONS_HYBRID_4 L3: the same journal read twice gives the same answer; there is no state to drift."""
    ok(journal, Call("dispatch", {"role": "x", "framing": "a"}), "A")
    events = journal.read()
    assert shared.live_dispatches(events) == shared.live_dispatches(list(events)) == 1
