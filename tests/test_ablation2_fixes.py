"""ABLATION_2 (docs/ABLATION_2.md) — the design finding D-KIND, the harness defects H9–H13 and the
scorer's Q5, each reproduced from the real attempt-3 journals in `ablation/runs/attempt3/` (UC3 and
UC2J, regression fixtures) and asserted on the real return values: the adapters' `ToolResult`, the
journal on disk, the lints, the CLI's exit code and stdout, the scorer's dict."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from ablation import score
from ancient_games.ctx import ABSENCE_PATTERNS, Ctx, kind_by_rule
from ancient_games.hybrid import cli
from ancient_games.hybrid.invariants import check_invariants
from ancient_games.hybrid.registry import load_tools
from ancient_games.hybrid.tools import (commit as commit_tool, corroborate as corroborate_tool,
                                        filter_candidates as filter_tool, guard as guard_tool,
                                        lookup_registry as lookup_tool, prove as prove_tool,
                                        record_claim as record_claim_tool, render_trace as render_trace_tool)
from ancient_games.hybrid.tools._plan import plan_from_journal
from ancient_games.hybrid.types import Call, ToolEnv
from ancient_games.journal import Journal, kind_overrides, read_events
from ancient_games.lints import lint_downstream_consumer_check_unrecorded, run_all_on_plan

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "ablation" / "runs" / "attempt3"
CASES = ROOT / "tests" / "cases" / "hybrid"
TOOLS = load_tools()
HELPERS = [f"helper-{i}-dead" for i in range(1, 7)]
CLOSED_WORLD = "AST over every .py in the HEAD tree + grep for the name as a string + no getattr/globals()/import_module idioms"


def journal_of(uc: str) -> list[dict]:
    return read_events(str(RUNS / f"{uc}.journal.jsonl"))


def calls(events: list[dict], tool: str) -> list[dict]:
    return [e for e in events if e.get("event") == "tool_call" and e["tool"] == tool]


def env_for(tmp_path, ctx: Ctx | None = None, run_id: str = "fix") -> ToolEnv:
    return ToolEnv(run_id, str(tmp_path / "j.jsonl"), ctx if ctx is not None else Ctx(), cwd=str(tmp_path), tools=TOOLS)


def test_fixtures_are_the_real_attempt3_journals_and_packets():
    uc3, uc2j = journal_of("UC3"), journal_of("UC2J")
    assert (len(uc3), len(uc2j)) == (69, 85)
    assert (sum(1 for e in uc3 if e["event"] == "tool_call"), sum(1 for e in uc2j if e["event"] == "tool_call")) == (37, 46)
    assert (uc3[0]["run_id"], uc2j[0]["run_id"]) == ("ablation-UC3-3", "ablation-UC2J-3")
    # the UC2J variant is defined by its rewritten task text, kept beside the journal
    packet = (RUNS / "UC2J.packet.md").read_text()
    assert "Someone believes they are unused, but that has not been established" in packet
    assert "Your determination that a helper is dead or live is itself a claim; record it as such." in packet
    assert "governance-gated" in (RUNS / "UC3.packet.md").read_text()
    # journals written before v1.4 lack the two D-KIND fields and still read (optional on read, always written)
    assert all("kind_override" not in e for e in uc2j if e["event"] == "claim_recorded")


# D-KIND ----------------------------------------------------------------------------------------
def test_dkind_rule_is_data_word_bounded_and_case_insensitive():
    assert ABSENCE_PATTERNS == ("dead", "unused", "no references?", "never", "nothing calls", "not reachable", "no callers?",
                                "unreferenced")
    for text in ("_helper_1 is dead", "these are UNUSED", "No references to foo", "never called", "Nothing calls it",
                 "not reachable from main", "no caller exists", "no callers exist", "an unreferenced symbol"):
        assert kind_by_rule(text) == "judgment", text
    for text in ("import succeeds", "the deadline passed", "deadlock-free", "suite is green", ""):
        assert kind_by_rule(text) is None, text


def test_dkind_uc2j_six_helper_claims_replayed_become_judgment_unless_closed_world(tmp_path):
    ev = journal_of("UC2J")
    recorded = [e for e in ev if e["event"] == "claim_recorded" and e["claim_id"] in HELPERS]
    assert [e["kind"] for e in recorded] == ["executable"] * 6  # as the actor declared them in the run
    args = [e["args"] for e in calls(ev, "record_claim") if e["args"]["claim_id"] in HELPERS]
    assert len(args) == 6 and all("closed_world" not in a for a in args)
    env = env_for(tmp_path, run_id="dkind")
    results = [record_claim_tool.run(env, a) for a in args]
    assert all(r.ok for r in results)
    assert [r.value["kind"] for r in results] == ["judgment"] * 6  # after: assigned by rule
    assert all(r.value["kind_override"] is False and r.value["closed_world"] is None for r in results)
    journaled = [e for e in read_events(env.journal_path) if e["event"] == "claim_recorded"]
    assert [(e["claim_id"], e["kind"], e["kind_override"]) for e in journaled] == [(c, "judgment", False) for c in HELPERS]
    # with a closed_world reason the author's `executable` is accepted, and the override is journaled
    env2 = env_for(tmp_path / "cw", run_id="dkind-cw")
    (tmp_path / "cw").mkdir()
    results = [record_claim_tool.run(env2, dict(a, closed_world=CLOSED_WORLD)) for a in args]
    assert [(r.value["kind"], r.value["kind_override"], r.value["closed_world"]) for r in results] == \
        [("executable", True, CLOSED_WORLD)] * 6
    assert kind_overrides(read_events(env2.journal_path)) == [{"claim_id": c, "author": "MAIN", "closed_world": CLOSED_WORLD}
                                                              for c in HELPERS]
    # an empty reason is no reason
    r = record_claim_tool.run(env2, dict(args[0], closed_world="   "))
    assert r.ok and r.value["kind"] == "judgment" and r.value["kind_override"] is False
    assert not record_claim_tool.run(env2, dict(args[0], closed_world=True)).ok
    # a claim the rule does not touch keeps its kind, needs no closed_world, and journals no override
    r = record_claim_tool.run(env2, {"claim_id": "import-succeeds", "author": "MAIN", "actor": "MAIN", "kind": "executable",
                                     "text": "import succeeds", "evidence_type": "command", "evidence_ref": "python3 -c 'import x'"})
    assert r.ok and (r.value["kind"], r.value["kind_override"], r.value["closed_world"]) == ("executable", False, None)
    r = record_claim_tool.run(env2, {"claim_id": "import-succeeds", "author": "MAIN", "kind": "executable", "text": "import succeeds",
                                     "evidence_type": "command", "evidence_ref": "x", "closed_world": "not needed"})
    assert r.ok and (r.value["kind"], r.value["kind_override"], r.value["closed_world"]) == ("executable", False, None)
    # an author's `judgment` on absence text is simply judgment
    r = record_claim_tool.run(env2, dict(args[0], kind="judgment"))
    assert r.ok and (r.value["kind"], r.value["kind_override"]) == ("judgment", False)
    assert record_claim_tool.run(env2, dict(args[0], kind="suite")).reason == \
        "invalid-args: kind must be one of executable|judgment, got 'suite' (str)"


def test_dkind_corroborate_is_bound_to_the_recorded_kind_and_caps_the_judgments(tmp_path):
    ev = journal_of("UC2J")
    args = [e["args"] for e in calls(ev, "record_claim") if e["args"]["claim_id"] in HELPERS]
    ctx = Ctx(actor={"delete-helpers": "MAIN"}, stakes=2, execution_status="main_executes", dispatch_count=0)
    env = env_for(tmp_path, ctx, run_id="dkind-b")
    for a in args:
        assert record_claim_tool.run(env, a).value["kind"] == "judgment"
    corr = [e["args"] for e in calls(ev, "corroborate") if e["reason"] is None][-1]  # the 2/2 SOURCES call of the run
    corr = dict(corr, claims=[c for c in corr["claims"] if c["claim_id"] in HELPERS])
    assert [c["kind"] for c in corr["claims"]] == ["executable"] * 6
    r = corroborate_tool.run(env, corr)  # the cheaper kind cannot be re-declared at corroborate
    assert not r.ok and r.reason == ("invalid-args: claims[0].kind must be the recorded kind 'judgment' for helper-1-dead "
                                     "(assigned by rule at record_claim — D-KIND; an executable override needs `closed_world` "
                                     "there), got 'executable' (str)")
    honest = dict(corr, claims=[dict(c, kind="judgment") for c in corr["claims"]],
                  framings={c: ["adversarial-review", "runtime-trace"] for c in HELPERS})
    r = corroborate_tool.run(env, honest)
    assert r.ok and r.value.exit_type == "CAPPED"
    assert [(x.claim.claim_id, x.n_available, x.n_required, x.remedy, x.capped.detail) for x in r.value.results] == \
        [(c, 0, 2, "add-differently-framed-source", "adversarial-review") for c in HELPERS]
    assert r.value.exit_line.startswith("Corroborate: helper-1-dead: n=0/2, capped, remedy=add-differently-framed-source; ")
    # with closed_world the same claims are executable again, and the run's own two mechanisms count (2/2)
    ctx2 = Ctx(actor={"delete-helpers": "MAIN"}, stakes=2, execution_status="main_executes")
    env2 = env_for(tmp_path / "cw", ctx2, run_id="dkind-b-cw")
    (tmp_path / "cw").mkdir()
    for a in args:
        assert record_claim_tool.run(env2, dict(a, closed_world=CLOSED_WORLD)).value["kind"] == "executable"
    j = Journal(env2.journal_path, env2.run_id)
    for e in ev:
        if e["event"] == "check_executed" and e["claim_id"] in HELPERS:
            j.append(dict(e, run_id=env2.run_id))
    r = corroborate_tool.run(env2, corr)
    assert r.ok and r.value.exit_type == "SOURCES" and [x.n_available for x in r.value.results] == [2] * 6


def test_dkind_overrides_are_shown_at_the_checkpoint_gate_and_in_the_trace(tmp_path):
    ev = journal_of("UC2J")
    args = [e["args"] for e in calls(ev, "record_claim") if e["args"]["claim_id"] in HELPERS]
    env = env_for(tmp_path, run_id="dkind-gate")
    assert commit_tool.run(env, {"message": "m"}).reason == "checkpoint-not-cleared"  # no override: the bare reason
    record_claim_tool.run(env, args[0])  # judgment by rule — nothing to show
    assert commit_tool.run(env, {"message": "m"}).reason == "checkpoint-not-cleared"
    record_claim_tool.run(env, dict(args[1], closed_world=CLOSED_WORLD))
    record_claim_tool.run(env, dict(args[2], closed_world="grep only"))
    r = commit_tool.run(env, {"message": "m"})
    assert not r.ok and r.reason == ("checkpoint-not-cleared; kind overrides for the gate to accept or reject: "
                                     f"helper-2-dead (executable by closed_world: {CLOSED_WORLD!r}); "
                                     "helper-3-dead (executable by closed_world: 'grep only')")
    md = render_trace_tool.run(env, {"title": "t"}).value
    assert "## Claim kind overrides (D-KIND: author's `executable` over the rule's `judgment`)" in md
    assert f"| `helper-2-dead` | MAIN | {CLOSED_WORLD} |" in md and "| `helper-3-dead` | MAIN | grep only |" in md
    assert "| `helper-1-dead` |" not in md.split("## Claim kind overrides")[1].split("## Consumer checks")[0]
    # an override from another run is not this run's business at the gate
    Journal(env.journal_path, "other").claim_recorded("x-dead", "MAIN", "MAIN", "executable", "x is dead", "command", "c",
                                                       kind_override=True, closed_world="elsewhere")
    assert "x-dead" not in commit_tool.run(env, {"message": "m"}).reason
    assert "| none | | |" in render_trace_tool.run(env_for(tmp_path / "empty", run_id="e"), {}).value if (tmp_path / "empty").mkdir() is None else True


# H9 --------------------------------------------------------------------------------------------
def test_h9_consumer_check_lint_compares_against_mutate_and_invoke_refs_only(tmp_path):
    ev = journal_of("UC3")
    last_prove = calls(ev, "prove")[-1]
    assert "no consumer_check event for ref ['research/holdout_recommendation.md', 'eval/protocol.json', 'eval/README.md']" \
        in ev[ev.index(last_prove) - 1]["exit_line"]  # the defect, as journaled: the read refs were expected to be checked
    plan = plan_from_journal(ev, Ctx(actor={"write-recommendation": "MAIN"}), last_prove["args"], run_id="ablation-UC3-3")
    entries = [e for e in plan.entries if e.name == "write-recommendation"]
    assert entries and all(e.ref == ["research/holdout_recommendation.md"] for e in entries)
    assert lint_downstream_consumer_check_unrecorded(plan, ev) == []
    assert [f.message for f in run_all_on_plan(plan, ev) if f.lint == "downstream-consumer-check-unrecorded"] == []
    # replayed through the real prove adapter: no consumer-check finding survives
    journal = Journal(str(tmp_path / "uc3.jsonl"), ev[0]["run_id"])
    for e in ev:
        journal.append(e)
    r = prove_tool.run(ToolEnv(journal.run_id, journal.path, Ctx(), cwd=str(tmp_path), tools=TOOLS), last_prove["args"])
    assert r.ok and not any("consumer_check" in f for f in r.value.findings)
    # a stakes=1 mutate with no consumer_check at all is still a finding
    plan.entries[0].ref = ["research/other.md"]
    assert [f.subject for f in lint_downstream_consumer_check_unrecorded(plan, ev)] == ["write-recommendation"]


# H10 -------------------------------------------------------------------------------------------
def _init(tmp_path) -> str:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    p = subprocess.run([sys.executable, "-m", "ancient_games.hybrid", "init", "--run-id", "h10", "--journal", str(tmp_path / "j.jsonl"),
                        "--cwd", str(repo)], cwd=ROOT, capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    return json.loads(p.stdout)["manifest"]


def _call(manifest: str, tool: str, args) -> tuple[int, dict, str]:
    p = subprocess.run([sys.executable, "-m", "ancient_games.hybrid", "--manifest", manifest, "call", tool, json.dumps(args)],
                       cwd=ROOT, capture_output=True, text=True)
    return p.returncode, json.loads(p.stdout) if p.stdout.strip().startswith("{") else p.stdout, p.stderr


def test_h10_hydration_errors_are_declined_with_the_expected_shape_exit_2_never_a_traceback(tmp_path):
    manifest = _init(tmp_path)
    for args, expect in ((
        {"action": "write research/x.md"},
        "invalid-args: action: must be a JSON object (ActionInput: {name, refs: [{path, mode, verb?, consumers?}], tripwires?, ...}), "
        "got 'write research/x.md' (str)"), (
        {"action": {"name": "x", "refs": "research/x.md"}},
        "invalid-args: action: refs must be a list of JSON objects (ArtifactRef: {path, mode, verb?, consumers?}), got 'research/x.md' (str)"), (
        {"action": {"name": "x", "refs": ["research/x.md"]}},
        "invalid-args: action: refs must be a list of JSON objects (ArtifactRef: {path, mode, verb?, consumers?}), got ['research/x.md'] (list)"),
    ):
        rc, out, err = _call(manifest, "guard", args)
        assert rc == 2 and "Traceback" not in err, (args, err)
        assert out["ok"] is False and out["refused_by"] is None and out["reason"] == expect
        assert check_invariants(Call("guard", args), Ctx(), [], TOOLS) == []  # the invariant no longer raises either
        assert guard_tool.run(env_for(tmp_path), args).reason == expect
    assert not guard_tool.run(env_for(tmp_path), {"action": {"name": "x", "refs": [], "tripwires": "cmd"}}).ok
    events = read_events(str(tmp_path / "j.jsonl"))
    assert [e["reason"].startswith("invalid-args: action:") for e in events if e["event"] == "tool_call"] == [True] * 3
    rc, out, _ = _call(manifest, "guard", {"action": {"name": "x", "refs": [{"path": "research/x.md", "mode": "mutate"}]}})
    assert rc == 0 and out["ok"] and out["value"]["exit_line"] == "Guard: x stakes=1, no hub."
    # every adapter that hydrates: the wrong shape is named, not a traceback and not an internal-error
    assert lookup_tool.run(env_for(tmp_path), {"refs": "research/x.md"}).reason == \
        "invalid-args: refs must be a list of JSON objects (ArtifactRef: {path, mode, verb?, consumers?}), got 'research/x.md' (str)"
    assert lookup_tool.run(env_for(tmp_path), {"refs": [{"path": "a", "mode": "edit"}]}).reason.startswith("invalid-args: refs: mode must be")
    assert filter_tool.run(env_for(tmp_path), {"candidates": {"a": 1}}).reason == \
        "invalid-args: candidates must be a list of candidate names (str) or JSON objects (Candidate), got {'a': 1} (dict)"
    assert filter_tool.run(env_for(tmp_path), {"candidates": ["a"], "cut": "a"}).reason.startswith("invalid-args: cut must be")
    rc, out, err = _call(manifest, "corroborate", {"action": "x", "claims": "C1"})
    assert rc == 2 and out["reason"].startswith("invalid-args: claims must be") and "Traceback" not in err


# H11 -------------------------------------------------------------------------------------------
def test_h11_a_tripwire_keyed_on_an_undeclared_hub_is_named_and_the_declared_consumer_matches(tmp_path):
    ev = journal_of("UC2J")
    guards = calls(ev, "guard")
    assert [g["result_summary"] for g in guards] == ["ok: GATED"] * 3
    first = guards[0]["args"]
    assert first["action"]["tripwires"] == {"loop/program_db.jsonl": first["action"]["tripwires"]["loop/program_db.jsonl"]}
    assert [r["mode"] for r in first["action"]["refs"]] == ["mutate", "read", "read", "read"]
    assert first["action"]["refs"][0]["consumers"] == ["loop/main.py", "tests/test_loop.py"]  # the jsonl was never declared
    d_lines = [e["exit_line"] for e in ev if e["event"] == "exit" and e["algorithm"] == "D"]
    assert all("hub=[]" in ln for ln in d_lines)  # the defect, as journaled: hub [] and tripwire {} on every guard
    # replayed: the silently dropped tripwire key is now the caller's error, and the reason says what to declare
    r = guard_tool.run(env_for(tmp_path), first)
    # F5: the rejection enumerates the keys it would accept (here none — the `consumers` clause is
    # what tells the caller what to do next)
    assert not r.ok and r.reason == ("invalid-args: action.tripwires must be one of [] — a hub element of this action, or "
                                     "the path of a ref that matched into one; a hub reached only through a mutate ref must be "
                                     "declared in that ref's `consumers` first, got ['loop/program_db.jsonl'] (list)")
    for g in guards[1:]:  # re-keyed by the mutate path (R7, hub?=no): resolves to no hub either
        assert guard_tool.run(env_for(tmp_path), g["args"]).reason.endswith("got ['loop/program_db.py'] (list)")
    # the corrected declaration — the jsonl named as a consumer of the mutate ref, the read ref kept — matches R4
    fixed = json.loads(json.dumps(first))
    fixed["action"]["refs"][0]["consumers"].append("loop/program_db.jsonl")
    ctx = Ctx()
    r = guard_tool.run(env_for(tmp_path, ctx), fixed)
    assert r.ok and r.value.hub == ["loop/program_db.jsonl"] and r.value.stakes == 2 and r.value.gate == "checkpoint"
    assert r.value.tripwire == first["action"]["tripwires"] and ctx.tripwire == first["action"]["tripwires"]
    assert r.value.exit_line == "Guard: delete-dead-helpers stakes=2, hub=loop/program_db.jsonl, gate=checkpoint."
    assert r.value.lookup.consumer_answer == "R4" and read_events(str(tmp_path / "j.jsonl"))[-2]["answer"] == "R4"
    # the read ref to the same path neither adds nor suppresses anything: identical result without it
    no_read = json.loads(json.dumps(fixed))
    no_read["action"]["refs"] = [no_read["action"]["refs"][0]]
    r2 = guard_tool.run(env_for(tmp_path), no_read)
    assert (r2.value.hub, r2.value.tripwire, r2.value.stakes) == (r.value.hub, r.value.tripwire, r.value.stakes)
    # a tripwire keyed by a hub's own name, or by the path of a ref that matched into it (H6), still passes
    commit_guard = {"action": {"name": "commit", "refs": [{"path": "loop/program_db.py", "mode": "mutate", "verb": "commit"}],
                               "tripwires": {"default-branch-history": "git diff --stat HEAD~1 HEAD"}}}
    assert guard_tool.run(env_for(tmp_path), commit_guard).value.tripwire == {"default-branch-history": "git diff --stat HEAD~1 HEAD"}
    by_path = json.loads(json.dumps(commit_guard))
    by_path["action"]["tripwires"] = {"loop/program_db.py": "git diff --stat HEAD~1 HEAD"}
    assert guard_tool.run(env_for(tmp_path), by_path).value.tripwire == {"default-branch-history": "git diff --stat HEAD~1 HEAD"}


# H12 -------------------------------------------------------------------------------------------
def test_h12_schema_states_framings_as_dict_of_lists_with_an_example():
    p = subprocess.run([sys.executable, "-m", "ancient_games.hybrid", "tools", "--schema"], cwd=ROOT, capture_output=True, text=True)
    assert p.returncode == 0
    [line] = [ln for ln in p.stdout.splitlines() if ln.strip().startswith("framings:")]
    assert line.startswith("  framings: dict[str, list[str]]  # {claim_id: [framing, ...]} — a LIST per claim, e.g. "
                           '{"C1": ["static-scan", "runtime-trace"]}; keyed by claim_id, not by author')
    assert TOOLS["corroborate"].manifest["inputs"]["framings"] == "dict[str, list[str]]"
    kinds = [ln for ln in p.stdout.splitlines() if ln.strip().startswith("kind:")]  # record_claim's arg and Claim.kind
    assert kinds and all("one of: executable | judgment" in ln and "assigned by rule (D-KIND)" in ln
                         and "|".join(ABSENCE_PATTERNS) in ln for ln in kinds)
    [cw] = [ln for ln in p.stdout.splitlines() if ln.strip().startswith("closed_world:")]
    assert "shown verbatim at the checkpoint gate" in cw
    for uc in ("UC1", "UC2", "UC3"):
        assert cli.tools_schema(TOOLS) in (ROOT / "ablation" / "packets" / f"{uc}.md").read_text()
    # both attempt-3 agents passed a prose string under the author's name — the shape the note now rules out
    for uc in ("UC3", "UC2J"):
        bad = [e for e in calls(journal_of(uc), "corroborate") if (e["reason"] or "").startswith("invalid-args: framings")]
        assert bad and isinstance(bad[0]["args"]["framings"]["MAIN"], str)


# H13 -------------------------------------------------------------------------------------------
def test_h13_default_ceiling_is_twice_the_longest_journal_under_runs(tmp_path):
    assert cli.default_ceiling() == 2 * 62 == 124  # UC2J attempt 4 is the longest free-agent trace so far
    assert cli.default_ceiling(str(tmp_path / "nothing")) == cli.FALLBACK_CEILING == 44
    repo = tmp_path / "repo"
    repo.mkdir()
    p = subprocess.run([sys.executable, "-m", "ancient_games.hybrid", "init", "--run-id", "h13", "--journal", str(tmp_path / "j.jsonl"),
                        "--cwd", str(repo)], cwd=ROOT, capture_output=True, text=True)
    assert p.returncode == 0 and json.loads(p.stdout)["ceiling"] >= 2 * 62
    assert json.load(open(tmp_path / "j.jsonl.run.json"))["ceiling"] == cli.default_ceiling()
    p = subprocess.run([sys.executable, "-m", "ancient_games.hybrid", "init", "--run-id", "h13", "--journal", str(tmp_path / "k.jsonl"),
                        "--cwd", str(repo), "--ceiling", "10"], cwd=ROOT, capture_output=True, text=True)
    assert json.loads(p.stdout)["ceiling"] == 10  # still overridable per run


# scorer Q5 -------------------------------------------------------------------------------------
def test_scorer_q5_on_the_attempt3_journals():
    r2j = score.score(str(RUNS / "UC2J.journal.jsonl"), str(CASES / "UC2.json"))
    r3 = score.score(str(RUNS / "UC3.journal.jsonl"), str(CASES / "UC3.json"))
    assert score.Q5 == "q5_second_head_for_judgment" and score.PRIMARY["UC2J"] == [score.Q1, score.Q3, score.Q5]
    # UC2J: n/a as declared — every claim was recorded executable, so no judgment claim exists to ask about
    assert r2j[score.Q5] == {"answer": None, "judgment_claims": [], "per_claim": [],
                             "detail": "n/a as declared: no judgment claim recorded (every recorded claim carries kind=executable)"}
    assert r2j[score.Q1]["answer"] is True and r2j[score.Q3]["answer"] is True and r2j[score.Q2]["answer"] is True
    assert r2j["total_tool_calls"] == 46 and r2j["done_ok"] is True and r2j["refusals_by_invariant"] == {}
    # UC3: the one judgment claim, C3, was routed to the owner gate by corroborate — no second head, but a human
    assert r3[score.Q5] == {"answer": True, "judgment_claims": ["C3"], "detail": None,
                            "per_claim": [{"claim_id": "C3", "actor": "MAIN", "category_a_sources": [], "routed_to_gate": True, "ok": True}]}
    assert r3[score.Q4]["answer"] is True and r3[score.Q4]["reason"] == "owner gate reached; no owner approval, no commit"
    assert r3["total_tool_calls"] == 37 and r3["done_ok"] is False
    md = score.render_md(r3)
    assert "| Q5 second head (or a human gate) for every judgment claim | yes |  | C3: (a)=0 gate=yes |" in md  # UC3's primary is Q4
    assert "| Q5 second head (or a human gate) for every judgment claim | n/a |  | n/a as declared" in score.render_md(r2j)


def test_scorer_q5_counts_only_a_differently_framed_other_author_or_a_gate(tmp_path):
    j = Journal(str(tmp_path / "q5.jsonl"), "q5")
    j.claim_recorded("h-dead", "MAIN", "MAIN", "judgment", "h is dead", "command", "grep", "static-scan")
    r = score.q5_second_head_for_judgment(j.read())
    assert r["answer"] is False and r["per_claim"][0]["category_a_sources"] == [] and r["per_claim"][0]["routed_to_gate"] is False
    j.claim_recorded("h-dead", "reviewer-1", "MAIN", "judgment", "h is dead", "file:line", "/agents/r1.md:1", "static-scan")
    assert score.q5_second_head_for_judgment(j.read())["answer"] is False  # same framing as the actor's own: not a second head
    j.claim_recorded("h-dead", "reviewer-2", "MAIN", "judgment", "h is dead", "file:line", "/agents/r2.md:1", "runtime-trace")
    r = score.q5_second_head_for_judgment(j.read())
    assert r["answer"] is True and r["per_claim"][0]["category_a_sources"] == [{"author": "reviewer-2", "framing": "runtime-trace"}]
    j.claim_recorded("g-unused", "MAIN", "MAIN", "judgment", "g is unused", "command", "grep")
    assert score.q5_second_head_for_judgment(j.read())["answer"] is False
    j.exit("B", ["B·1"], "CAPPED", "Corroborate: g-unused: n=0/2, capped, remedy=gate-checkpoint; reconciled=agree.", [])
    r = score.q5_second_head_for_judgment(j.read())
    assert r["answer"] is True and [c["routed_to_gate"] for c in r["per_claim"]] == [False, True]
    # executable claims never enter Q5
    j.claim_recorded("import-ok", "MAIN", "MAIN", "executable", "import succeeds", "command", "python3 -c 'import x'")
    assert score.q5_second_head_for_judgment(j.read())["judgment_claims"] == ["h-dead", "g-unused"]
