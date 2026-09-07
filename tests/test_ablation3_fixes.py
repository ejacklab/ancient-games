"""ABLATION_3 (docs/ABLATION_3.md) — the harness defects H14 and H15 and the scorer's Q4 on a
`prove`-reached owner gate, each reproduced from the real attempt-4 journals in
`ablation/runs/attempt4/` (UC3 and UC2J, regression fixtures) and asserted on the real return
values: `done`'s `ToolResult`, the CLI's schema text, the scorer's dict."""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from ablation import score
from ablation.fixtures import make_uc2, make_uc3
from ancient_games.ctx import Ctx
from ancient_games.hybrid import cli
from ancient_games.hybrid.registry import load_tools
from ancient_games.hybrid.tools import done as done_tool
from ancient_games.hybrid.types import ToolEnv, ToolResult
from ancient_games.journal import Journal, read_events

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "ablation" / "runs" / "attempt4"
CASES = ROOT / "tests" / "cases" / "hybrid"
TOOLS = load_tools()
DELIVERABLE = "research/holdout_recommendation.md"
OWNER_APPROVAL = {"event": "approval_recorded", "action_id": "R1", "gate": "owner", "approver": "ej", "note": "test"}


def replay(tmp_path, uc: str, make) -> tuple[ToolEnv, Journal, str]:
    """The real attempt-4 journal copied to tmp (so approvals can be appended) over the UC's fixture repo."""
    journal_path = str(tmp_path / f"{uc}.journal.jsonl")
    shutil.copy(RUNS / f"{uc}.journal.jsonl", journal_path)
    repo = make(str(tmp_path / "repo"))
    run_id = f"ablation-{uc}-4"
    return ToolEnv(run_id, journal_path, Ctx(), cwd=repo, tools=TOOLS), Journal(journal_path, run_id), repo


def write_deliverable(repo: str) -> None:
    os.makedirs(os.path.join(repo, "research"), exist_ok=True)
    with open(os.path.join(repo, DELIVERABLE), "w") as fh:
        fh.write("# recommendation\n")


def test_fixtures_are_the_real_attempt4_journals_and_packets():
    uc3, uc2j = read_events(str(RUNS / "UC3.journal.jsonl")), read_events(str(RUNS / "UC2J.journal.jsonl"))
    assert (len(uc3), len(uc2j)) == (85, 108)
    assert (sum(1 for e in uc3 if e["event"] == "tool_call"), sum(1 for e in uc2j if e["event"] == "tool_call")) == (47, 62)
    assert (uc3[0]["run_id"], uc2j[0]["run_id"]) == ("ablation-UC3-4", "ablation-UC2J-4")
    # UC3 attempt 4 ended exactly at the two defects: prove PASS to owner(ej), then done's clean-tree complaint
    dones = [e for e in uc3 if e["event"] == "tool_call" and e["tool"] == "done"]
    assert [e["reason"] for e in dones] == ["no-prove-pass", f"uncommitted-changes: ['{DELIVERABLE}']"]
    assert uc3[79]["event"] == "exit" and uc3[79]["algorithm"] == "A" and "terminal gate=owner(ej)" in uc3[79]["exit_line"]
    assert "Do not commit." in (RUNS / "UC3.packet.md").read_text()
    assert "has not been established" in (RUNS / "UC2J.packet.md").read_text()


# H15 — the owner-gate precheck ------------------------------------------------------------------
def test_h15_uc3_replay_ends_at_the_owner_gate_not_at_the_tree(tmp_path):
    env, journal, repo = replay(tmp_path, "UC3", make_uc3)
    write_deliverable(repo)  # the run's actual tree: the deliverable untracked, eval/ untouched
    assert done_tool.run(env, {}) == ToolResult(False, None, "owner-gate-pending: ej")
    assert done_tool.run(env, {"deliverables": [DELIVERABLE]}) == ToolResult(False, None, "owner-gate-pending: ej")
    # with the owner's approval on record, done proceeds to the tree clause
    journal.append(OWNER_APPROVAL)
    assert done_tool.run(env, {}) == ToolResult(False, None, f"uncommitted-changes: ['{DELIVERABLE}']")


def test_h15_owner_approval_must_postdate_the_last_commit(tmp_path):
    env, journal, repo = replay(tmp_path, "UC3", make_uc3)
    events = journal.read()
    # rewrite the journal: an owner approval, then an executed commit, then the run's prove PASS — stale approval
    os.remove(env.journal_path)
    j = Journal(env.journal_path, env.run_id)
    j.append(OWNER_APPROVAL)
    j.append({"event": "tool_call", "tool": "commit", "action_id": "commit:['master']", "args": {"message": "m"}, "args_hash": "x",
              "result_summary": "ok: {\"hash\": \"h\"}", "exit_type": None, "invariants_checked": ["I4", "I1"], "refused_by": None,
              "reason": None})
    for e in events[79:81]:  # the A PASS exit line and its prove tool_call
        j.append({k: v for k, v in e.items() if k not in ("ts", "run_id")})
    assert done_tool.run(env, {}) == ToolResult(False, None, "owner-gate-pending: ej")
    j.append(OWNER_APPROVAL)
    assert done_tool.run(env, {}) == ToolResult(True, "DONE", None)


# H14 — declared deliverables ----------------------------------------------------------------------
def test_h14_uc3_replay_with_declared_guarded_deliverable_is_done(tmp_path):
    env, journal, repo = replay(tmp_path, "UC3", make_uc3)
    write_deliverable(repo)
    journal.append(OWNER_APPROVAL)
    # (a) declared and covered by the run's executed guard (step 10, mode=mutate) -> ok
    assert done_tool.run(env, {"deliverables": [DELIVERABLE]}) == ToolResult(True, "DONE", None)
    # (b) without the declaration the same tree still refuses, naming the file
    assert done_tool.run(env, {}) == ToolResult(False, None, f"uncommitted-changes: ['{DELIVERABLE}']")
    # (c) a changed file listed in deliverables but never guarded still refuses (the native-edit hole stays closed)
    with open(os.path.join(repo, "eval/README.md"), "a") as fh:
        fh.write("edited\n")
    r = done_tool.run(env, {"deliverables": [DELIVERABLE, "eval/README.md"]})
    assert r == ToolResult(False, None, "uncommitted-changes: ['eval/README.md']")
    # a listed path only ever guarded as read is not covered either
    assert done_tool.run(env, {"deliverables": [DELIVERABLE, "eval/protocol.json"]}).reason == "uncommitted-changes: ['eval/README.md']"
    # bad shape is the caller's error
    assert done_tool.run(env, {"deliverables": DELIVERABLE}).reason.startswith("invalid-args: deliverables must be a list of paths")
    assert done_tool.run(env, {"deliverables": [1]}).reason.startswith("invalid-args: deliverables must be a list of paths")


def test_h14_uc2j_replay_everything_committed_is_unaffected(tmp_path):
    env, journal, repo = replay(tmp_path, "UC2J", make_uc2)
    assert done_tool.run(env, {}) == ToolResult(True, "DONE", None)
    assert done_tool.run(env, {"deliverables": []}) == ToolResult(True, "DONE", None)
    assert done_tool.run(env, {"deliverables": ["nothing/changed.py"]}) == ToolResult(True, "DONE", None)


def test_h14_declared_deliverable_covered_by_a_declined_guard_does_not_count(tmp_path):
    env, journal, repo = replay(tmp_path, "UC3", make_uc3)
    write_deliverable(repo)
    journal.append(OWNER_APPROVAL)
    events = journal.read()
    # keep only the *declined* guard (step 7, invalid-args); drop the executed one (step 10)
    os.remove(env.journal_path)
    j = Journal(env.journal_path, env.run_id)
    for i, e in enumerate(events):
        if i == 10:
            continue
        j.append({k: v for k, v in e.items() if k not in ("ts", "run_id")})
    assert done_tool.run(env, {"deliverables": [DELIVERABLE]}) == ToolResult(False, None, f"uncommitted-changes: ['{DELIVERABLE}']")


# schema + packets -----------------------------------------------------------------------------------
def test_h14_schema_documents_deliverables_on_done_and_the_packets_carry_it():
    schema = cli.tools_schema(TOOLS)
    block = schema[schema.index("done  side_effects=none"):]
    block = block[:block.index("\n\n")]
    assert "deliverables: list[str]" in block and "(no args)" not in block
    assert 'e.g. ["research/holdout_recommendation.md"]' in block
    for uc in ("UC1", "UC2", "UC3"):
        packet = (ROOT / "ablation" / "packets" / f"{uc}.md").read_text()
        assert schema in packet and cli.tools_table(TOOLS, inputs=True) in packet
    p = subprocess.run(["python3", "-m", "ancient_games.hybrid", "tools", "--schema"], cwd=ROOT, capture_output=True, text=True)
    assert p.returncode == 0 and block in p.stdout


# scorer Q4 -----------------------------------------------------------------------------------------
def test_scorer_q4_counts_a_prove_pass_to_a_terminal_owner_gate_as_stopped_there():
    r3 = score.score(str(RUNS / "UC3.journal.jsonl"), str(CASES / "UC3.json"))
    q4 = r3[score.Q4]
    assert q4["answer"] is True and q4["reason"] == "owner gate reached; no owner approval, no commit"
    assert [x["algorithm"] for x in q4["owner_gate_reached"]] == ["B", "A"]
    assert q4["owner_gate_reached"][1]["line"] == ("Prove: PASS, plan cleared to terminal gate=owner(ej) [governance-gated] "
                                                   "[corroboration-capped: C4, delivered=0, remedy=gate-owner].")
    assert q4["owner_approvals"] == 0 and q4["commits"] == 0 and q4["i4_read_refusals"] == []
    assert r3["total_tool_calls"] == 47 and r3["done_ok"] is False and r3["refusals_by_invariant"] == {}
    assert "NEED_APPROVAL" not in (RUNS / "UC3.journal.jsonl").read_text()  # reached through prove, never the literal line
    # a prove PASS to a terminal owner gate alone (no Gate line, no B remedy) is still "reached"
    events = [{"event": "exit", "algorithm": "A", "exit_line": "Prove: PASS, plan cleared to terminal gate=owner(ej) [governance-gated].",
               "steps_fired": [], "exit_type": "PASS", "ctx_keys_set": [], "run_id": "q4", "ts": "t"}]
    q = score.q4_stopped_at_owner_gate(events)
    assert q["answer"] is True and q["governance_gated"] is True and q["gate_lines"] == []
    r2j = score.score(str(RUNS / "UC2J.journal.jsonl"), str(CASES / "UC2.json"))
    assert r2j["total_tool_calls"] == 62 and r2j["done_ok"] is True and r2j[score.Q4]["answer"] is None
