"""AUTONOMY_DESIGN v2 (docs/AUTONOMY_DESIGN.md) — the three autonomy modes, the path-scoped
pre-authorisation, and the deferral queue, as e2e cases over the real tools and the real journal.

Numbered against §10 of the design. Every case here exists because the adversarial review
(docs/AUTONOMY_REVIEW.md) showed a v1 version of it either could not fail or asserted the wrong
thing — most importantly case 5, whose v1 form was vacuous because I4 runs in the loop before
`commit`'s body ever executes, so the grant code it claimed to test never ran.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from ancient_games.ctx import Ctx
from ancient_games.hybrid import autonomy, cli, loop
from ancient_games.hybrid.registry import load_tools
from ancient_games.hybrid.tools import commit as commit_tool
from ancient_games.hybrid.tools import done as done_tool
from ancient_games.hybrid.types import Call, ToolEnv
from ancient_games.journal import Journal, read_events

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "ablation" / "runs" / "attempt4"
TOOLS = load_tools()
STEP_RULES = [{"name": "step", "tool": "*"}]


def git(root, *argv):
    return subprocess.run(["git", *argv], cwd=root, check=True, capture_output=True, text=True)


def repo_at(path) -> str:
    root = str(path)
    os.makedirs(root, exist_ok=True)
    for argv in (("init", "-q"), ("config", "user.email", "t@t"), ("config", "user.name", "t"),
                 ("config", "commit.gpgsign", "false")):
        git(root, *argv)
    write(root, "a.py", "x = 1\n")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "init")
    return root


def write(root, rel, content):
    os.makedirs(os.path.dirname(os.path.join(root, rel)) or root, exist_ok=True)
    with open(os.path.join(root, rel), "w") as fh:
        fh.write(content)


def journal_at(tmp_path, run_id="R", autonomy_mode="auto", pause_after=None, ceiling=50) -> Journal:
    j = Journal(str(tmp_path / "j.jsonl"), run_id)
    j.append({"event": "run_config", "autonomy": autonomy_mode,
              "pause_after": autonomy.rules_for(autonomy_mode, pause_after), "ceiling": ceiling})
    return j


def grant(j: Journal, paths, max_uses=1, allow_overrides=False, gid="grant:1"):
    return j.append({"event": "preauthorization_recorded", "grant_id": gid, "approver": "ej",
                     "scope_paths": list(paths), "max_uses": max_uses,
                     "allow_kind_overrides": allow_overrides, "note": ""})


def override_claim(j: Journal, claim_id="C1"):
    return j.append({"event": "claim_recorded", "claim_id": claim_id, "author": "MAIN", "actor": "MAIN",
                     "kind": "executable", "text": "x is dead", "evidence_type": "command",
                     "evidence_ref": "grep -r x", "framing": "static-scan", "kind_override": True,
                     "closed_world": "AST over every .py plus grep; no reflective idioms"})


def env_for(j: Journal, repo: str) -> ToolEnv:
    return ToolEnv(j.run_id, j.path, Ctx(), cwd=repo, tools=TOOLS)


# --- 1-2: the modes pause where they say they do -------------------------------------------
def test_1_step_mode_pauses_after_every_call_and_one_resume_clears_exactly_one(tmp_path):
    j = journal_at(tmp_path, autonomy_mode="step")
    r = loop.run(TOOLS, loop.scripted([{"tool": "read_journal"}, {"tool": "read_journal"}]), j, 50, Ctx())
    assert (r.status, r.paused_at, len(r.steps)) == ("PAUSED", "pause:step@1", 1)

    j.append({"event": "approval_recorded", "action_id": "pause:step@1", "gate": "resume",
              "approver": "ej", "note": ""})
    r = loop.run(TOOLS, loop.scripted([{"tool": "read_journal"}, {"tool": "read_journal"}]), j, 50, Ctx())
    # exactly one more call ran: the resume cleared @1 and the run stopped again at @2
    assert (r.status, r.paused_at, len(r.steps)) == ("PAUSED", "pause:step@2", 1)


def test_2_phase_mode_runs_a_whole_phase_and_a_refused_call_does_not_close_one(tmp_path):
    rules = [{"name": "research", "tool": "read_journal"}]
    j = journal_at(tmp_path, autonomy_mode="phase", pause_after=rules)
    # a call that is NOT the phase's tool does not pause the run
    r = loop.run(TOOLS, loop.scripted([{"tool": "rebuild_index", "args": {"db_path": str(tmp_path / "x.sqlite")}},
                                       {"tool": "read_journal"}, {"tool": "read_journal"}]), j, 50, Ctx())
    assert (r.status, r.paused_at) == ("PAUSED", "pause:research@2")
    assert [s.call.tool for s in r.steps] == ["rebuild_index", "read_journal"]

    # a REFUSED call matching the rule must not close a phase: event_ok is false for it
    refused = {"event": "tool_call", "tool": "read_journal", "action_id": None, "args": {}, "args_hash": "h",
               "result_summary": "refused: I5", "exit_type": None, "invariants_checked": [],
               "refused_by": "I5", "reason": "no slot"}
    assert autonomy.boundaries([dict(refused, run_id="R", ts="t")], rules) == []


# --- 3: exit_type, not ok-ness (review B2) --------------------------------------------------
def test_3_a_returned_to_planner_prove_does_not_satisfy_a_pass_rule():
    """`tools/prove.py` returns ok=True unconditionally, so a failed prove is journaled
    `"ok: ...Prove: FAIL ... returned to planner"`. A rule keyed on ok-ness would announce the
    phase complete at the exact moment prove bounced. Asserted on the REAL attempt-4 journal."""
    events = read_events(str(RUNS / "UC3.journal.jsonl"))
    proves = [e for e in events if e.get("event") == "tool_call" and e["tool"] == "prove" and e["refused_by"] is None]
    exits = [e["exit_type"] for e in proves]
    assert "RETURN_TO_PLANNER" in exits and "PASS" in exits, exits  # the fixture really has both

    pass_rule = [{"name": "implement", "tool": "prove", "exit_type": "PASS"}]
    ok_rule = [{"name": "implement", "tool": "prove"}]
    n_pass = len(autonomy.boundaries(events, pass_rule))
    n_any = len(autonomy.boundaries(events, ok_rule))
    assert n_pass == exits.count("PASS") and n_any == len(proves) and n_pass < n_any


# --- 4: auto is today's behaviour -----------------------------------------------------------
def test_4_a_journal_with_no_run_config_is_auto_and_spends_its_whole_ceiling():
    events = read_events(str(RUNS / "UC2J.journal.jsonl"))
    assert not [e for e in events if e.get("event") == "run_config"]
    assert autonomy.rules_from_events(events) == []
    assert autonomy.effective_ceiling(events, [], 92) == 92
    assert autonomy.open_boundary(events, []) is None


# --- 5: the floor is unmovable, asserted where the grant code actually runs ------------------
def test_5_a_grant_covering_an_owner_gated_path_is_still_refused_by_I4(tmp_path):
    """v1's version of this case could not fail: I4 runs in `loop.step` BEFORE `commit`'s body, so
    the grant code never executed. This runs the real path and asserts the refusal is I4, that no
    commit landed, and that the grant minted nothing."""
    repo = repo_at(tmp_path / "repo")
    write(repo, "eval/protocol.json", '{"one_shot": true}\n')  # R1: gate=owner, ej
    j = journal_at(tmp_path)
    grant(j, ["eval/**"])  # scope DOES cover the changed path
    before = git(repo, "rev-parse", "HEAD").stdout.strip()

    st = loop.step(TOOLS, Call("commit", {"message": "m"}), j, Ctx(), cwd=repo)
    assert st.refused_by == "I4" and st.result is None
    assert git(repo, "rev-parse", "HEAD").stdout.strip() == before
    assert [e for e in j.read() if e["event"] == "approval_derived"] == []


# --- 6-7: scope binding ----------------------------------------------------------------------
def test_6_a_research_grant_does_not_authorise_a_commit_that_also_touches_engine(tmp_path):
    repo = repo_at(tmp_path / "repo")
    write(repo, "research/a.md", "# a\n")
    write(repo, "engine/x.py", "y = 2\n")
    j = journal_at(tmp_path)
    grant(j, ["research/**"])
    before = git(repo, "rev-parse", "HEAD").stdout.strip()

    res = commit_tool.run(env_for(j, repo), {"message": "m"})
    assert res.ok is False and "engine/x.py" in res.reason and "outside scope" in res.reason
    assert git(repo, "rev-parse", "HEAD").stdout.strip() == before


@pytest.mark.parametrize("patterns,path,covered", [
    (["research/**"], "research/a.md", True),
    (["research/**"], "research/deep/nested/a.md", True),
    (["research/**"], "research/../engine/x.py", False),   # fnmatch's * crosses / — ours does not
    (["research*"], "researchx/y", False),
    (["research/*"], "research/deep/a.md", False),
    (["research/**"], "/etc/passwd", False),
])
def test_7_scope_matching_is_segment_aware(patterns, path, covered):
    assert autonomy.scope_covers(patterns, path) is covered


# --- 8-9: liveness ---------------------------------------------------------------------------
def test_8_max_uses_exhaustion_falls_back_to_checkpoint_not_cleared(tmp_path):
    repo = repo_at(tmp_path / "repo")
    write(repo, "research/a.md", "# a\n")
    j = journal_at(tmp_path)
    grant(j, ["research/**"], max_uses=1)
    assert commit_tool.run(env_for(j, repo), {"message": "one"}).ok is True

    write(repo, "research/b.md", "# b\n")
    res = commit_tool.run(env_for(j, repo), {"message": "two"})
    assert res.ok is False and res.reason.startswith("checkpoint-not-cleared") and "max_uses exhausted" in res.reason


def test_9_a_kind_override_makes_a_grant_not_live_unless_it_allows_them(tmp_path):
    repo = repo_at(tmp_path / "repo")
    write(repo, "research/a.md", "# a\n")
    j = journal_at(tmp_path)
    grant(j, ["research/**"])
    override_claim(j)
    before = git(repo, "rev-parse", "HEAD").stdout.strip()

    res = commit_tool.run(env_for(j, repo), {"message": "m"})
    assert res.ok is False and "allow_kind_overrides is false" in res.reason
    # the disclosure is STILL shown verbatim, exactly as it is at a human checkpoint
    assert "closed_world" in res.reason and "C1" in res.reason
    assert git(repo, "rev-parse", "HEAD").stdout.strip() == before


# --- 10-11: continue-and-queue, and the audit record --------------------------------------------
def test_10_11_allowing_overrides_commits_queues_the_disclosure_and_never_mints_an_approval(tmp_path):
    repo = repo_at(tmp_path / "repo")
    write(repo, "research/a.md", "# a\n")
    j = journal_at(tmp_path)
    grant(j, ["research/**"], allow_overrides=True)
    override_claim(j)

    res = commit_tool.run(env_for(j, repo), {"message": "m"})
    assert res.ok is True

    events = j.read()
    # 11: the grant path mints NO approval_recorded — every commit shares one action_id, so a
    # stored derived approval would clear a LATER commit its scope never covered (review C1).
    assert [e for e in events if e["event"] == "approval_recorded"] == []
    derived = [e for e in events if e["event"] == "approval_derived"]
    assert len(derived) == 1 and derived[0]["grant_id"] == "grant:1" and derived[0]["paths"] == ["research/a.md"]
    # 10: one deferred_decision per unreviewed override, and the audit records come last —
    # they are written only after `git commit` returned 0
    deferred = [e for e in events if e["event"] == "deferred_decision"]
    assert len(deferred) == 1 and deferred[0]["kind"] == "kind-override" and "C1" in deferred[0]["payload"]
    assert [e["event"] for e in events[-2:]] == ["approval_derived", "deferred_decision"]


def test_11b_a_failing_commit_under_a_live_grant_records_nothing(tmp_path):
    """The sharp form of "the audit record authorises nothing": if `git commit` does not return 0,
    no `approval_derived` and no `deferred_decision` exist — so a grant's use is never spent, and
    an unreviewed disclosure is never marked as having been passed over, on a commit that never
    happened. Here the tree is clean, so git refuses."""
    repo = repo_at(tmp_path / "repo")
    j = journal_at(tmp_path)
    grant(j, ["**"], allow_overrides=True)
    override_claim(j)
    head = git(repo, "rev-parse", "HEAD").stdout.strip()

    res = commit_tool.run(env_for(j, repo), {"message": "m"})
    assert res.ok is False
    assert git(repo, "rev-parse", "HEAD").stdout.strip() == head
    assert [e for e in j.read() if e["event"] in ("approval_derived", "deferred_decision")] == []
    assert autonomy.uses_of(j.read(), "grant:1") == 0  # the grant was not spent


def test_10b_done_reports_the_queue_and_the_cli_exits_non_zero_while_it_stands(tmp_path):
    repo = repo_at(tmp_path / "repo")
    j = journal_at(tmp_path)
    j.append({"event": "deferred_decision", "kind": "kind-override", "payload": "C1 (...)",
              "boundary": "commit:['master']", "reason": "committed under grant:1"})
    j.append({"event": "tool_call", "tool": "prove", "action_id": None, "args": {}, "args_hash": "h",
              "result_summary": "ok: PASS", "exit_type": "PASS", "invariants_checked": ["I3"],
              "refused_by": None, "reason": None})
    res = done_tool.run(env_for(j, repo), {})
    assert res.ok is True and res.value == "DONE" and "deferred-decisions: 1" in res.reason

    manifest = cli.write_manifest("R", j.path, repo, [], 50, resume=True)
    rc = cli.main(["--manifest", manifest, "queue"])
    assert rc != 0  # a record, not a gate — but a wrapper or CI can notice


# --- 12-14: configuration, resume, and where the mode lives -------------------------------------
def test_12_phase_without_a_pause_after_list_is_refused(tmp_path):
    repo = repo_at(tmp_path / "repo")
    with pytest.raises(ValueError, match="requires a non-empty pause_after"):
        cli.write_manifest("R", str(tmp_path / "j.jsonl"), repo, [], 50, autonomy_mode="phase", pause_after=[])


def test_12b_the_manifest_reports_the_resolved_rules_and_resume_adopts_the_journals_mode(tmp_path):
    repo = repo_at(tmp_path / "repo")
    jp = str(tmp_path / "j.jsonl")
    m = json.load(open(cli.write_manifest("R", jp, repo, [], 50, autonomy_mode="step")))
    assert (m["autonomy"], m["pause_after"]) == ("step", STEP_RULES)  # never a misleading []
    # a second init that contradicts the run loses: the journal is where the mode lives
    m2 = json.load(open(cli.write_manifest("R", jp, repo, [], 50, autonomy_mode="auto", resume=True)))
    assert (m2["autonomy"], m2["pause_after"]) == ("step", STEP_RULES)


def test_13_resume_reuses_the_journal_and_keeps_ctx_and_the_ceiling_count(tmp_path):
    repo = repo_at(tmp_path / "repo")
    jp = str(tmp_path / "j.jsonl")
    manifest = cli.write_manifest("R", jp, repo, [], 50, autonomy_mode="step")
    ctx_path = json.load(open(manifest))["ctx_path"]
    cli.save_ctx(ctx_path, Ctx(stop_criterion="the deliverable exists"))
    Journal(jp, "R").append({"event": "tool_call", "tool": "gate", "action_id": None, "args": {},
                             "args_hash": "h", "result_summary": "ok: GATED", "exit_type": "GATED",
                             "invariants_checked": [], "refused_by": None, "reason": None})

    cli.write_manifest("R", jp, repo, [], 50, autonomy_mode="step", resume=True)
    assert cli.load_ctx(ctx_path).stop_criterion == "the deliverable exists"  # not clobbered
    events = Journal(jp, "R").read()
    assert len([e for e in events if e["event"] == "run_config"]) == 1  # not duplicated
    assert len([e for e in events if e["event"] == "tool_call"]) == 1   # budget survives the restart


def test_14_the_mode_lives_in_the_journal_and_a_tool_mutating_ctx_cannot_change_it(tmp_path):
    """§8: ctx is a mutable dataclass handed to every non-RESTRICTED tool by reference, and
    `load_ctx` fails OPEN to a fresh Ctx() when its file is missing. A journal event cannot be
    unwritten, so that is where the mode lives."""
    j = journal_at(tmp_path, autonomy_mode="step")
    ctx = Ctx()
    ctx.stop_criterion = "mutated by a tool"          # a tool CAN do this
    assert autonomy.rules_from_events(j.read()) == STEP_RULES  # and it changes nothing
    assert "autonomy" not in {f for f in Ctx().as_dict()}
    r = loop.run(TOOLS, loop.scripted([{"tool": "read_journal"}, {"tool": "read_journal"}]), j, 50, ctx)
    assert r.status == "PAUSED"
