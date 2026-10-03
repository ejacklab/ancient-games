"""harvest_run.py and runlog.py: the feedback log (docs/research/20261002-workflow-feedback, options A and B)."""
import json
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / ".claude/skills/workflow-design/scripts"
SECRET = "SECRET-PROMPT-TEXT-7f3a"


def run(script, *args, cwd=None):
    return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)],
                          capture_output=True, text=True, cwd=cwd)


def usage_line(mid, inp, cw, cr, out, tool=False):
    content = [{"type": "text", "text": SECRET}]
    if tool:
        content.append({"type": "tool_use", "id": "t", "name": "Bash", "input": {"command": SECRET}})
    return json.dumps({"type": "assistant", "message": {"id": mid, "model": "claude-opus-5-5", "content": content,
                       "usage": {"input_tokens": inp, "cache_creation_input_tokens": cw,
                                 "cache_read_input_tokens": cr, "output_tokens": out}}})


def make_workflow(projects, wf="wf_test-1", agents=None):
    session = projects / "proj" / "sess"
    (session / "workflows").mkdir(parents=True)
    adir = session / "subagents" / "workflows" / wf
    adir.mkdir(parents=True)
    progress = [{"type": "workflow_phase", "index": 1, "title": "P"}]
    for i, a in enumerate(agents or []):
        progress.append({"type": "workflow_agent", "index": i + 1, "label": a["label"], "agentId": a["id"],
                         "state": "done", "model": "claude-opus-5-5", "startedAt": 1790949267000 + i * 1000,
                         "durationMs": a.get("ms", 1000), "tokens": a.get("reported"), "toolCalls": 1,
                         "cached": a.get("cached", False), "promptPreview": SECRET, "resultPreview": SECRET})
        if "lines" in a:
            (adir / f"agent-{a['id']}.jsonl").write_text("\n".join(a["lines"]) + "\n")
    (session / "workflows" / f"{wf}.json").write_text(json.dumps(
        {"runId": wf, "status": "completed", "durationMs": 5000, "totalTokens": 1, "workflowProgress": progress,
         "script": SECRET}))
    return wf


def test_workflow_parts_rounds_cached_and_no_text_leak(tmp_path):
    projects = tmp_path / "projects"
    wf = make_workflow(projects, agents=[
        {"label": "plan", "id": "a1", "reported": 150, "ms": 4000,
         # the same message id twice (streamed): only the last usage counts
         "lines": [usage_line("m1", 1, 9, 1000, 5), usage_line("m1", 10, 90, 1000, 20, tool=True),
                   usage_line("m2", 5, 45, 2000, 10)]},
        {"label": "plan #2", "id": "a2", "reported": 60, "lines": [usage_line("m3", 6, 54, 500, 7)]},
        {"label": "critic", "id": "a3", "cached": True},
    ])
    r = run("harvest_run.py", "--run", "r1", "--runs-root", tmp_path / "runs", "--workflow", wf,
            "--claude-projects", projects, "--codex-sessions", tmp_path / "none")
    assert r.returncode == 0, r.stderr
    rows = [json.loads(l) for l in (tmp_path / "runs/r1/feedback.jsonl").read_text().splitlines()]
    plan = [x for x in rows if x["node_id"] == "plan"]
    assert sorted(x["round"] for x in plan) == [1, 2]
    first = next(x for x in plan if x["round"] == 1)
    assert (first["tokens_in"], first["tokens_cache_write"], first["tokens_cache_read"], first["tokens_out"]) == \
        (15, 135, 3000, 30)
    assert first["api_calls"] == 2 and first["tool_calls_transcript"] == 1
    critic = next(x for x in rows if x["node_id"] == "critic")
    assert critic["cost_known"] is False                      # cached: never counted as zero cost
    assert "nodes with more than one round: plan" in r.stdout
    assert "cost unknown: 1" in r.stdout
    assert "ledger Actual cost" in r.stdout and len(r.stdout.splitlines()) <= 20
    blob = (tmp_path / "runs/r1/feedback.jsonl").read_text() + r.stdout
    assert SECRET not in blob                                 # public repo: no prompt or response text


def test_format_change_fails_loud(tmp_path):
    projects = tmp_path / "projects"
    wf = make_workflow(projects, agents=[{"label": "x", "id": "a1", "lines": [
        json.dumps({"type": "assistant", "message": {"id": "m", "content": []}})]}])   # usage missing
    r = run("harvest_run.py", "--run", "r1", "--runs-root", tmp_path / "runs", "--workflow", wf,
            "--claude-projects", projects)
    assert r.returncode == 3 and "FORMAT CHANGED" in r.stderr
    assert not (tmp_path / "runs/r1/feedback.jsonl").exists()
    r = run("harvest_run.py", "--run", "r1", "--runs-root", tmp_path / "runs", "--workflow", "wf_nope",
            "--claude-projects", projects)
    assert r.returncode == 3 and "found 0" in r.stderr


def write_rollout(sessions, ts, cwd, name, inp=100, cached=60, out=7, error=None):
    day = sessions / ts[:10].replace("-", "/")
    day.mkdir(parents=True, exist_ok=True)
    lines = [{"timestamp": ts, "type": "session_meta", "payload": {"timestamp": ts, "cwd": cwd,
                                                                    "creator_user_id": "user-SECRET"}},
             {"type": "turn_context", "payload": {"model": "gpt-6.1-sol"}},
             {"type": "token_usage_record", "payload": {"usage": {"input_tokens": inp, "cached_input_tokens": cached,
                                                                   "output_tokens": out, "reasoning_output_tokens": 3}}},
             {"type": "event_msg", "payload": {"type": "task_complete", "duration_ms": 900, "error": error,
                                               "last_agent_message": SECRET}}]
    f = day / f"rollout-{name}.jsonl"
    f.write_text("\n".join(json.dumps(x) for x in lines) + "\n")
    return f


def test_runlog_exec_verdict_and_codex_join(tmp_path):
    runs = tmp_path / "runs"
    r = run("runlog.py", "--runs-root", runs, "exec", "--run", "r2", "--node", "n1", "--attempt", "1",
            "--engine", "codex", "--brief-variant", "with-example", "--", sys.executable, "-c", "print('hi')",
            cwd=tmp_path)
    assert r.returncode == 0, r.stderr
    events = [json.loads(l) for l in (runs / "r2/events.jsonl").read_text().splitlines()]
    assert [e["event"] for e in events] == ["start", "end"] and events[1]["status"] == "ok"
    assert (runs / "r2/raw/n1-1-codex.stdout").read_text().strip() == "hi"     # raw output kept out of events
    assert "hi" not in (runs / "r2/events.jsonl").read_text()
    assert run("runlog.py", "--runs-root", runs, "verdict", "--run", "r2", "--node", "n1", "--round", "1",
               "--check", "pytest", "--pass", "yes").returncode == 0
    # a codex session that started inside the call's window, in the same cwd, is joined; one elsewhere is not
    start = events[0]["ts"]
    sessions = tmp_path / "sessions"
    write_rollout(sessions, start, str(tmp_path), "here")
    write_rollout(sessions, start, "/some/other/dir", "elsewhere")
    h = run("harvest_run.py", "--run", "r2", "--runs-root", runs, "--codex-sessions", sessions)
    assert h.returncode == 0, h.stderr
    row = json.loads((runs / "r2/feedback.jsonl").read_text().splitlines()[0])
    assert row["cost_known"] and row["model"] == "gpt-6.1-sol" and row["tokens_cache_read"] == 60
    assert row["tokens_in"] == 40          # codex input_tokens 100 includes the 60 cached: new input is 40
    assert row["brief_variant"] == "with-example"
    assert "checks: 1/1 pass; first-try 1/1" in h.stdout
    blob = (runs / "r2/feedback.jsonl").read_text() + h.stdout
    assert SECRET not in blob and "user-SECRET" not in blob


def test_codex_join_refuses_to_guess(tmp_path):
    runs = tmp_path / "runs"
    run("runlog.py", "--runs-root", runs, "exec", "--run", "r3", "--node", "n1", "--engine", "codex", "--",
        sys.executable, "-c", "pass", cwd=tmp_path)
    start = json.loads((runs / "r3/events.jsonl").read_text().splitlines()[0])["ts"]
    sessions = tmp_path / "sessions"
    write_rollout(sessions, start, str(tmp_path), "first")
    write_rollout(sessions, start, str(tmp_path), "second")  # two sessions match the same window and cwd
    h = run("harvest_run.py", "--run", "r3", "--runs-root", runs, "--codex-sessions", sessions)
    assert h.returncode == 0, h.stderr
    row = json.loads((runs / "r3/feedback.jsonl").read_text().splitlines()[0])
    assert row["cost_known"] is False and "unlinked: 2" in row["note"]


def test_runlog_timeout_and_failure_status(tmp_path):
    runs = tmp_path / "runs"
    r = run("runlog.py", "--runs-root", runs, "exec", "--run", "r4", "--node", "n1", "--engine", "qwen",
            "--timeout", "0.5", "--", sys.executable, "-c", "import time; time.sleep(5)")
    assert r.returncode == 124
    r = run("runlog.py", "--runs-root", runs, "exec", "--run", "r4", "--node", "n2", "--engine", "agy",
            "--", sys.executable, "-c", "raise SystemExit(3)")
    assert r.returncode == 3
    ends = [json.loads(l) for l in (runs / "r4/events.jsonl").read_text().splitlines() if '"end"' in l]
    assert [(e["node_id"], e["status"], e["exit_code"]) for e in ends] == [("n1", "timeout", 124), ("n2", "fail", 3)]
