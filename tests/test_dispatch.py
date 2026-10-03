"""dispatch.py — the dispatcher layer (docs/DISPATCHER_DESIGN.md), run against fake engines only (no quota)."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / ".claude/skills/workflow-design/scripts/dispatch.py"
BRIEF = "# Brief\n## Task\nDo x.\n## Template\nresult-file.md\n## Example\none row\n## Standard\nthe check passes\n"

FAKE = r'''
import sys, time, pathlib
mode, node, attempt, out = sys.argv[1], sys.argv[2], sys.argv[3], pathlib.Path(sys.argv[4])
prompt = pathlib.Path(sys.argv[5]).read_text() if len(sys.argv) > 5 and pathlib.Path(sys.argv[5]).exists() else ""
head = f"---\nnode: {node}\nattempt: {attempt}\nengine: script\nmodel: fake\nstatus: ok\nstarted: t\nended: t\nevidence: e\n---\n"
if mode == "ok":        out.write_text(head + "done\n")
elif mode == "exit3":   sys.exit(3)
elif mode == "empty":   pass
elif mode == "noheader": out.write_text("just text\n")
elif mode == "sleep":   time.sleep(5)
elif mode == "unclear": out.write_text(head + "UNCLEAR: which table? / guess: users\n")
elif mode == "fixed-if-feedback": out.write_text(head + ("FIXED\n" if "fail-marker" in prompt else "first try\n"))
'''


def node(nid, mode, **kw):
    n = {"id": nid, "role": kw.pop("role", "worker"), "engine": "script", "outer_timeout_s": kw.pop("timeout", 10),
         "cmd": [sys.executable, "fake.py", mode, nid, "{attempt}", "{out}", "{prompt_file}"]}
    n.update(kw)
    return n


def setup(tmp_path, nodes, budget=None):
    (tmp_path / "fake.py").write_text(FAKE)
    (tmp_path / "brief.md").write_text(BRIEF)
    plan = {"run_id": "r1", "nodes": nodes, **({"budget": budget} if budget else {})}
    (tmp_path / "plan.json").write_text(json.dumps(plan))
    return tmp_path / "plan.json"


def run(tmp_path, *args, env=None):
    return subprocess.run([sys.executable, str(SCRIPT), "--root", str(tmp_path), *args], capture_output=True,
                          text=True, cwd=tmp_path, env=env)


def fix_attempts(nodes):
    return nodes        # the fake echoes the dispatcher's {attempt}


def state(tmp_path):
    return json.loads((tmp_path / "runs/r1/dispatch.json").read_text())


def test_happy_path_with_dependency_and_parallel_group(tmp_path):
    nodes = fix_attempts([node("a", "ok"), node("b", "ok", needs=["a"], parallel_group="g", role="dev"),
                          node("c", "ok", needs=["a"], parallel_group="g", role="verifier")])
    r = run(tmp_path, "run", setup(tmp_path, nodes))
    assert r.returncode == 0, r.stdout + r.stderr
    assert "DONE — 3/3 nodes done, 3 call(s)" in r.stdout
    ev = [json.loads(l) for l in (tmp_path / "runs/r1/events.jsonl").read_text().splitlines()]
    assert [e["event"] for e in ev].count("end") == 3


def test_executor_failure_retries_once_on_fallback(tmp_path):
    fb = {"engine": "script", "cmd": [sys.executable, "fake.py", "ok", "a", "{attempt}", "{out}"]}
    r = run(tmp_path, "run", setup(tmp_path, fix_attempts([node("a", "exit3", fallback=fb)])))
    assert r.returncode == 0, r.stdout + r.stderr
    assert state(tmp_path)["nodes"]["a"]["calls"] == 2 and "executor failure" in r.stderr


@pytest.mark.parametrize("mode,why", [("exit3", "exit 3"), ("empty", "empty result"),
                                      ("noheader", "pass-back"), ("sleep", "timeout")])
def test_executor_failures_block_without_fallback(tmp_path, mode, why):
    r = run(tmp_path, "run", setup(tmp_path, fix_attempts([node("a", mode, timeout=1)])))
    assert r.returncode == 1 and "needs the COO: a blocked" in r.stdout, r.stdout
    assert why in r.stderr + r.stdout


def test_check_failure_repairs_with_real_feedback_then_passes(tmp_path):
    check = {"name": "has-FIXED", "cmd": [sys.executable, "-c",
             "import sys; t=open(sys.argv[1]).read(); print('fail-marker: no FIXED'); sys.exit(0 if 'FIXED' in t else 1)",
             "{result}"]}
    n = node("a", "fixed-if-feedback", check=check, repair="a")
    r = run(tmp_path, "run", setup(tmp_path, [n]))
    # attempt 2 carries the check's output ("fail-marker") as feedback; the fake then writes FIXED
    assert r.returncode == 0, r.stdout + r.stderr
    assert "a check failed (round 1)" in r.stderr
    rec = state(tmp_path)["nodes"]["a"]
    assert rec["rounds"] == 1 and rec["status"] == "done" and "FIXED" in Path(rec["result"]).read_text()


def test_rounds_cap_blocks(tmp_path):
    check = {"name": "never", "cmd": [sys.executable, "-c", "raise SystemExit(1)"]}
    r = run(tmp_path, "run", setup(tmp_path, fix_attempts([node("a", "ok", check=check, repair="a")]),
                                   budget={"max_rounds": 2}))
    assert r.returncode == 1 and "check failed 2 round(s)" in r.stdout


def test_unclear_stops_and_reaches_the_coo(tmp_path):
    r = run(tmp_path, "run", setup(tmp_path, fix_attempts([node("a", "unclear"), node("b", "ok", needs=["a"])])))
    assert r.returncode == 1 and "a asks: UNCLEAR: which table?" in r.stdout
    assert "b" not in state(tmp_path)["nodes"]          # nothing after it ran


def test_plan_refusals(tmp_path):
    many = [{"id": f"n{i}", "role": f"r{i}", "engine": "codex", "model": "gpt-6.1-sol", "brief": "brief.md",
             "inner_timer": "300s", "outer_timeout_s": 330} for i in range(6)]
    p = setup(tmp_path, many)
    assert run(tmp_path, "check", p).returncode == 1
    assert "6 roles > cap 5" in run(tmp_path, "check", p).stdout
    group = [node(f"n{i}", "ok", parallel_group="g") for i in range(4)]
    assert "4 nodes > cap 3" in run(tmp_path, "check", setup(tmp_path, group)).stdout
    (tmp_path / "thin.md").write_text("# Brief\n## Task\nx\n## Template\nt\n")
    eng = [{"id": "c", "role": "coder", "engine": "codex", "model": "gpt-6.1-sol", "brief": "thin.md",
            "inner_timer": "300s", "outer_timeout_s": 330}]
    out = run(tmp_path, "check", setup(tmp_path, eng)).stdout
    assert "lacks ['## Example', '## Standard']" in out
    cyc = [node("a", "ok", needs=["b"]), node("b", "ok", needs=["a"])]
    assert "dependency cycle" in run(tmp_path, "check", setup(tmp_path, cyc)).stdout
    assert run(tmp_path, "run", setup(tmp_path, many)).returncode == 2
    cl = [{"id": "x", "role": "explorer", "engine": "claude", "model": "claude-opus-5-5", "brief": "brief.md",
           "inner_timer": "600s", "outer_timeout_s": 660}]
    assert "Claude nodes run with the Workflow tool" in run(tmp_path, "check", setup(tmp_path, cl)).stdout


def test_resume_skips_done_nodes(tmp_path):
    p = setup(tmp_path, fix_attempts([node("a", "ok"), node("b", "unclear", needs=["a"])]))
    assert run(tmp_path, "run", p).returncode == 1
    plan = json.loads(p.read_text()); plan["nodes"][1]["cmd"][2] = "ok"; p.write_text(json.dumps(plan))
    r = run(tmp_path, "run", p)
    assert r.returncode == 0 and "a already done (resume)" in r.stderr
    assert state(tmp_path)["nodes"]["a"]["calls"] == 1


def fake_bin(tmp_path, name, body):
    b = tmp_path / "bin"; b.mkdir(exist_ok=True)
    f = b / name
    f.write_text(f"#!{sys.executable}\n" + body)
    f.chmod(0o755)
    return {**os.environ, "PATH": f"{b}:{os.environ['PATH']}"}


def test_qwen_adapter_catches_a_silent_model_swap(tmp_path):
    # qwen exits 0 and runs another model when -m is wrong (EXECUTOR_KINDS, 2026-10-02)
    env = fake_bin(tmp_path, "qwen", r'''
import json, sys
m = sys.argv[sys.argv.index("-m") + 1]
head = "---\nnode: q\nattempt: 1\nengine: qwen\nmodel: x\nstatus: ok\nstarted: t\nended: t\nevidence: e\n---\nok\n"
print(json.dumps([{"type": "system", "model": "qwen3.7-plus"}, {"type": "result", "result": head}]))
''')
    q = {"id": "q", "role": "classifier", "engine": "qwen", "model": "qwen3.8-flash", "brief": "brief.md",
         "inner_timer": "60s", "outer_timeout_s": 70}
    r = run(tmp_path, "run", setup(tmp_path, [q]), env=env)
    assert r.returncode == 1 and "tool reports model 'qwen3.7-plus'" in r.stderr
    q["model"] = "qwen3.7-plus"
    import shutil; shutil.rmtree(tmp_path / "runs")      # a fresh run, not a resume of the blocked one
    r = run(tmp_path, "run", setup(tmp_path, [q]), env=env)
    assert r.returncode == 0, r.stdout + r.stderr


def test_dry_run_prints_engine_commands_without_running(tmp_path):
    nodes = [{"id": e, "role": e, "engine": e, "model": "m", "brief": "brief.md", "inner_timer": "90s",
              "outer_timeout_s": 100, "mode": "write" if e == "codex" else "read-only"}
             for e in ["codex", "qwen", "agy"]]
    r = run(tmp_path, "run", setup(tmp_path, nodes), "--dry-run")
    assert r.returncode == 0, r.stderr
    assert "codex exec -m m -s workspace-write" in r.stdout
    assert "qwen --approval-mode plan --max-wall-time 90s -m m --output-format json" in r.stdout
    assert "--mode plan --model m --print-timeout 90s" in r.stdout
    assert not (tmp_path / "runs/r1/events.jsonl").exists()


def test_engine_repair_prompt_carries_the_checks_output(tmp_path):
    env = fake_bin(tmp_path, "qwen", r'''
import json, sys
prompt = sys.argv[-1]
att = prompt.split("attempt: ")[1].split("\n")[0]
body = "FIXED" if "Feedback from the last attempt" in prompt and "needs FIXED" in prompt else "first"
head = f"---\nnode: q\nattempt: {att}\nengine: qwen\nmodel: m\nstatus: ok\nstarted: t\nended: t\nevidence: e\n---\n{body}\n"
print(json.dumps([{"type": "system", "model": "m"}, {"type": "result", "result": head}]))
''')
    check = {"name": "fixed", "cmd": [sys.executable, "-c",
             "import sys; t=open(sys.argv[1]).read(); print('needs FIXED'); sys.exit(0 if 'FIXED' in t else 1)", "{result}"]}
    q = {"id": "q", "role": "coder", "engine": "qwen", "model": "m", "brief": "brief.md", "inner_timer": "60s",
         "outer_timeout_s": 70, "check": check, "repair": "q"}
    r = run(tmp_path, "run", setup(tmp_path, [q]), env=env)
    assert r.returncode == 0, r.stdout + r.stderr
    assert state(tmp_path)["nodes"]["q"]["rounds"] == 1


def test_call_budget_stops_the_run(tmp_path):
    r = run(tmp_path, "run", setup(tmp_path, [node("a", "ok"), node("b", "ok", needs=["a"])], budget={"max_calls": 1}))
    assert r.returncode == 1 and "budget: 1 calls reached before b" in r.stdout


def test_agy_inner_timer_with_exit_0_is_a_timeout(tmp_path):
    # agy --print-timeout fires: exit 0, partial output, a stderr notice (seen live 2026-10-03)
    env = fake_bin(tmp_path, "agy", r'''
import sys
head = "---\nnode: g\nattempt: 1\nengine: agy\nmodel: m\nstatus: ok\nstarted: t\nended: t\nevidence: e\n---\npartial\n"
print(head)
print("[agy] print timeout after 1s with turn in progress; returning partial output", file=sys.stderr)
''')
    g = {"id": "g", "role": "classifier", "engine": "agy", "model": "m", "brief": "brief.md", "inner_timer": "1s",
         "outer_timeout_s": 30}
    r = run(tmp_path, "run", setup(tmp_path, [g]), env=env)
    assert r.returncode == 1 and "executor failure on agy: timeout" in r.stderr


def test_timeout_kills_the_whole_process_group(tmp_path):
    # qwen is a wrapper whose node child outlived a plain kill (seen live 2026-10-03)
    marker = tmp_path / "grandchild-still-alive"
    env = fake_bin(tmp_path, "qwen", rf'''
import subprocess, sys, time
subprocess.Popen([sys.executable, "-c", "import time, pathlib; time.sleep(3); pathlib.Path({str(marker)!r}).write_text('x')"])
time.sleep(30)
''')
    q = {"id": "q", "role": "classifier", "engine": "qwen", "model": "m", "brief": "brief.md", "inner_timer": "60s",
         "outer_timeout_s": 1}
    r = run(tmp_path, "run", setup(tmp_path, [q]), env=env)
    assert r.returncode == 1 and "timeout" in r.stderr
    import time; time.sleep(4)
    assert not marker.exists(), "a grandchild survived the timeout"
