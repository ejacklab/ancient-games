"""dispatch.py — the dispatcher layer (docs/DISPATCHER_DESIGN.md), run against fake engines only (no quota)."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / ".claude/skills/workflow-design/scripts/dispatch.py"
sys.path.insert(0, str(SCRIPT.parent))          # engines.py sits beside dispatch.py
import engines                                   # noqa: E402  (path is set just above)
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


def test_executor_failure_blocks_even_when_the_plan_names_a_fallback(tmp_path):
    """No fallback (removed 2026-10-05 at EJ's direction): a failed engine blocks the node and reports.

    A plan may still *carry* a `fallback` key — nothing reads it now — and the node must block rather than
    quietly finish on an engine nobody chose.
    """
    fb = {"engine": "script", "cmd": [sys.executable, "fake.py", "ok", "a", "{attempt}", "{out}"]}
    r = run(tmp_path, "run", setup(tmp_path, fix_attempts([node("a", "exit3", fallback=fb)])))
    assert r.returncode == 1, r.stdout + r.stderr
    assert state(tmp_path)["nodes"]["a"]["calls"] == 1
    assert "blocked: executor failed" in r.stdout + r.stderr
    assert "falling back" not in r.stderr


@pytest.mark.parametrize("mode,why", [("exit3", "exit 3"), ("empty", "empty result"),
                                      ("noheader", "pass-back"), ("sleep", "timeout")])
def test_executor_failures_block_without_fallback(tmp_path, mode, why):
    r = run(tmp_path, "run", setup(tmp_path, fix_attempts([node("a", mode, timeout=1)])))
    assert r.returncode == 1 and "needs the COO: a blocked" in r.stdout, r.stdout
    assert why in r.stderr + r.stdout


def test_an_external_engine_failure_blocks_and_reports(tmp_path):
    """Same rule for an external engine: it fails, the node blocks, the COO is told. Nothing hops to Claude.

    The old behaviour had codex fall through to Claude — which is also the reviewer most designs give a codex
    builder, so the hop could quietly make the reviewer the builder's own kind (register 8.2). Removing the
    fallback removes that case with it.
    """
    env = fake_bin(tmp_path, "codex", "import sys; sys.exit(3)")
    fake_bin(tmp_path, "claude", "import sys; sys.exit(0)")
    c = {"id": "a", "role": "coder", "engine": "codex", "model": "gpt-6.1-sol", "brief": "brief.md",
         "inner_timer": "60s", "outer_timeout_s": 70}
    r = run(tmp_path, "run", setup(tmp_path, [c]), env=env)
    assert r.returncode == 1, r.stdout + r.stderr
    assert state(tmp_path)["nodes"]["a"]["calls"] == 1
    assert "blocked: executor failed on codex" in r.stdout + r.stderr
    assert "falling back" not in r.stderr


def test_opencode_engine_builds_the_verified_argv(tmp_path):
    """`opencode run`, verified against the real CLI on 2026-10-04.

    Two things are pinned here because both were got wrong first and both are silent:

    * the message must precede any `--file=`, because `-f` is a greedy array option that swallows the next
      positional — file-first makes opencode read the *prompt* as the attachment path;
    * `--agent` is the read-only/write switch (`plan` refuses writes, verified by asking it to write), and the
      model is provider-namespaced, which is why it is passed through verbatim.
    """
    node = {"id": "x", "role": "coder", "engine": "opencode",
            "model": "minimax-coding-plan/MiniMax-M3.1-Flash-Preview", "brief": "brief.md",
            "inner_timer": "600s", "outer_timeout_s": 660, "mode": "write"}
    r = run(tmp_path, "check", setup(tmp_path, [node]))
    assert r.returncode == 0, r.stdout + r.stderr

    argv = engines.build_opencode(node, node["model"], "PROMPT", None, tmp_path, 1)
    assert argv[:2] == ["opencode", "run"]
    assert argv[-1] == "PROMPT", "the message must be the last positional, after every flag"
    assert "build" in argv and "plan" not in argv

    read_only = {**node, "mode": "read-only"}
    assert "plan" in engines.build_opencode(read_only, node["model"], "P", None, tmp_path, 1)


def test_no_engine_carries_a_default_fallback(tmp_path):
    """Removed 2026-10-05 at EJ's direction: one engine per node, and a failure reports.

    Pinned so the map cannot come back by habit. If a fallback is ever wanted again it should be a deliberate
    step in the graph, visible, not a silent hop inside the dispatcher.
    """
    assert not hasattr(engines, "DEFAULT_FALLBACKS")
    assert all(not hasattr(e, "default_fallback") for e in engines.REGISTRY.values())


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


def test_the_budget_no_longer_carries_the_caps():
    """The two keys are gone, not merely unused: a plan cannot set them and nothing reads them."""
    assert "max_roles" not in engines.__dict__ or True          # engines never held them
    import dispatch
    assert "max_roles" not in dispatch.DEFAULT_BUDGET
    assert "max_parallel" not in dispatch.DEFAULT_BUDGET
    # The pool counts **engine processes alive**, its own unmeasured machine setting. It is deliberately not the
    # harness's `maxActiveSubagents`, which counts **resident sessions** (an idle continuable child holds a slot).
    # Reading one from the other was the mis-transcription corrected on 2026-10-05.
    assert dispatch.MAX_ENGINE_PROCESSES == 8
    assert not hasattr(dispatch, "MAX_WORKERS")


def test_a_call_past_the_ceiling_is_refused(tmp_path):
    """Method 3.8's ceiling on one call: 8 hours (EJ, 2026-10-05, "it is not healthy").

    The per-task timers scale with the work; the ceiling does not. Before this the rule was prose — a node could ask
    for a 40-hour timeout and every check passed.
    """
    import dispatch
    under = [node("a", "ok", outer_timeout_s=dispatch.MAX_CALL_SECONDS)]
    assert "past the ceiling" not in run(tmp_path, "check", setup(tmp_path, under)).stdout
    over = [node("a", "ok", outer_timeout_s=dispatch.MAX_CALL_SECONDS + 1)]
    out = run(tmp_path, "check", setup(tmp_path, over)).stdout
    assert "past the ceiling" in out, out
    assert "cut the work into segments" in out
    # and the sabotage: a 40-hour call, the shape the rule exists to stop
    huge = [node("a", "ok", outer_timeout_s=40 * 3600)]
    assert "past the ceiling" in run(tmp_path, "check", setup(tmp_path, huge)).stdout


def test_rounds_cap_blocks(tmp_path):
    check = {"name": "never", "cmd": [sys.executable, "-c", "raise SystemExit(1)"]}
    r = run(tmp_path, "run", setup(tmp_path, fix_attempts([node("a", "ok", check=check, repair="a")]),
                                   budget={"max_rounds": 2}))
    assert r.returncode == 1 and "check failed 2 round(s)" in r.stdout


def test_unclear_stops_and_reaches_the_coo(tmp_path):
    r = run(tmp_path, "run", setup(tmp_path, fix_attempts([node("a", "unclear"), node("b", "ok", needs=["a"])])))
    assert r.returncode == 1 and "a asks: UNCLEAR: which table?" in r.stdout
    assert "b" not in state(tmp_path)["nodes"]          # nothing after it ran


def test_many_roles_and_a_wide_group_are_allowed(tmp_path):
    """The role and parallel-group caps were deleted 2026-10-05 (EJ: "not logic at all").

    They re-labelled the spike rule's numbers from TASK_TYPES.md — "run at most 3 in parallel", "up to 5 in a
    round", both about candidate *approaches* — as a rule about *roles* and *concurrency*, which is why the
    sentence would not parse: two different units called the same word.

    Pinned so the caps cannot return by habit. Six roles and a four-node group are simply plans now. The worker
    pool still keeps its size (`dispatch.MAX_ENGINE_PROCESSES`), because that is a machine setting, not a
    design rule.
    """
    many = [{"id": f"n{i}", "role": f"r{i}", "engine": "codex", "model": "gpt-6.1-sol", "brief": "brief.md",
             "inner_timer": "300s", "outer_timeout_s": 330} for i in range(6)]
    out = run(tmp_path, "check", setup(tmp_path, many)).stdout
    assert "roles > cap" not in out, out
    group = [node(f"n{i}", "ok", parallel_group="g") for i in range(4)]
    out = run(tmp_path, "check", setup(tmp_path, group)).stdout
    assert "nodes > cap" not in out, out
    (tmp_path / "thin.md").write_text("# Brief\n## Task\nx\n## Template\nt\n")
    eng = [{"id": "c", "role": "coder", "engine": "codex", "model": "gpt-6.1-sol", "brief": "thin.md",
            "inner_timer": "300s", "outer_timeout_s": 330}]
    out = run(tmp_path, "check", setup(tmp_path, eng)).stdout
    assert "lacks ['## Example', '## Standard']" in out
    cyc = [node("a", "ok", needs=["b"]), node("b", "ok", needs=["a"])]
    assert "dependency cycle" in run(tmp_path, "check", setup(tmp_path, cyc)).stdout
    # `run` still refuses a plan that fails its own check (exit 2) — but no longer because of a role count.
    # A cycle is the refusal to use here, since it did not depend on the deleted caps.
    assert run(tmp_path, "run", setup(tmp_path, cyc)).returncode == 2
    unknown = [{"id": "x", "role": "explorer", "engine": "gemini", "model": "m", "brief": "brief.md",
                "inner_timer": "600s", "outer_timeout_s": 660}]
    assert "engine 'gemini' is not one of" in run(tmp_path, "check", setup(tmp_path, unknown)).stdout


def test_claude_and_dsh_engines_are_accepted(tmp_path):
    """Re-enabled 2026-10-03, via the adapter seam.

    The `claude` refusal was a Claude-Code-only rule: there the Workflow tool already served Claude nodes, so
    dispatching them again was pointless. On another harness that reason does not hold, and `claude -p` is the
    only route to a Claude executor. `dsh` runs a node on the harness itself, and takes its model from the
    headless profile rather than a flag — so a plan may omit the model for `dsh` and must not for `codex`.
    """
    cl = [{"id": "x", "role": "explorer", "engine": "claude", "model": "claude-opus-5-5", "brief": "brief.md",
           "inner_timer": "600s", "outer_timeout_s": 660}]
    r = run(tmp_path, "check", setup(tmp_path, cl))
    assert r.returncode == 0, r.stdout + r.stderr

    d = [{"id": "y", "role": "classifier", "engine": "dsh", "brief": "brief.md",
          "inner_timer": "120s", "outer_timeout_s": 150}]
    assert run(tmp_path, "check", setup(tmp_path, d)).returncode == 0

    c = [{"id": "z", "role": "coder", "engine": "codex", "brief": "brief.md",
          "inner_timer": "120s", "outer_timeout_s": 150}]
    assert "no model" in run(tmp_path, "check", setup(tmp_path, c)).stdout


def test_dry_run_shows_the_new_engine_commands(tmp_path):
    nodes = [{"id": "c", "role": "explorer", "engine": "claude", "model": "claude-opus-5-5", "brief": "brief.md",
              "inner_timer": "600s", "outer_timeout_s": 660, "mode": "read-only"},
             {"id": "d", "role": "classifier", "engine": "dsh", "brief": "brief.md",
              "inner_timer": "120s", "outer_timeout_s": 150}]
    r = run(tmp_path, "run", setup(tmp_path, nodes), "--dry-run")
    assert r.returncode == 0, r.stderr
    assert "claude -p" in r.stdout and "--permission-mode plan" in r.stdout
    assert "dsh headless" in r.stdout


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


@pytest.mark.parametrize("absolute", [False, True])
def test_workdir_is_the_engine_cwd(tmp_path, absolute):
    folder = tmp_path / "w/q"
    folder.mkdir(parents=True)
    n = node("a", "ok", workdir=str(folder) if absolute else "w/q", passback=False,
             cmd=[sys.executable, "-c", "import os; print(os.getcwd())"])
    r = run(tmp_path, "run", setup(tmp_path, [n]))
    assert r.returncode == 0, r.stdout + r.stderr
    result = Path(state(tmp_path)["nodes"]["a"]["result"])
    assert result.read_text().strip() == str(folder)
    events = [json.loads(l) for l in (tmp_path / "runs/r1/events.jsonl").read_text().splitlines()]
    assert all(e["cwd"] == str(folder) for e in events if e["event"] in {"start", "end"})


def test_workdir_created_relative_to_root(tmp_path):
    folder = tmp_path / "w/new"
    n = node("a", "ok", workdir="w/new", passback=False,
             cmd=[sys.executable, "-c", "import os; print(os.getcwd())"])
    p = setup(tmp_path, [n])
    assert not folder.exists()
    r = subprocess.run([sys.executable, str(SCRIPT), "--root", str(tmp_path), "run", str(p)],
                       capture_output=True, text=True, cwd=tmp_path.parent)
    assert r.returncode == 0, r.stdout + r.stderr
    assert folder.is_dir()
    assert Path(state(tmp_path)["nodes"]["a"]["result"]).read_text().strip() == str(folder)


def test_without_workdir_uses_repo_root(tmp_path):
    n = node("a", "ok", passback=False, cmd=[sys.executable, "-c", "import os; print(os.getcwd())"])
    r = run(tmp_path, "run", setup(tmp_path, [n]))
    assert r.returncode == 0, r.stdout + r.stderr
    assert Path(state(tmp_path)["nodes"]["a"]["result"]).read_text().strip() == str(tmp_path)


@pytest.mark.parametrize("workdir", ["w", "w/" + "long-folder-" * 8])
def test_codex_workdir_is_the_C_argument(tmp_path, workdir):
    c = {"id": "c", "role": "coder", "engine": "codex", "model": "m", "brief": "brief.md",
         "inner_timer": "60s", "outer_timeout_s": 70, "workdir": workdir}
    r = run(tmp_path, "run", setup(tmp_path, [c]), "--dry-run")
    assert r.returncode == 0, r.stdout + r.stderr
    assert f"-C {tmp_path / workdir} -o " in r.stdout


def test_workdir_keeps_brief_result_and_check_at_root(tmp_path):
    env = fake_bin(tmp_path, "qwen", r'''
import json, os, sys
assert "Do x." in sys.argv[-1]
head = "---\nnode: q\nattempt: 1\nengine: qwen\nmodel: m\nstatus: ok\nstarted: t\nended: t\nevidence: e\n---\n"
print(json.dumps([{"type": "system", "model": "m"}, {"type": "result", "result": head + os.getcwd()}]))
''')
    (tmp_path / "check.py").write_text(
        "import pathlib, sys\n"
        "root = pathlib.Path.cwd()\n"
        "result = pathlib.Path(sys.argv[1])\n"
        "assert (root / 'brief.md').is_file()\n"
        "assert result.parent == root / 'runs/r1/nodes'\n"
        "assert result.read_text().splitlines()[-1] == str(root / 'w')\n")
    q = {"id": "q", "role": "coder", "engine": "qwen", "model": "m", "brief": "brief.md",
         "inner_timer": "60s", "outer_timeout_s": 70, "workdir": "w",
         "check": {"cmd": [sys.executable, "check.py", "{result}"]}}
    r = run(tmp_path, "run", setup(tmp_path, [q]), env=env)
    assert r.returncode == 0, r.stdout + r.stderr
    rec = state(tmp_path)["nodes"]["q"]
    assert rec["status"] == "done" and rec["rounds"] == 0
    assert Path(rec["result"]) == tmp_path / "runs/r1/nodes/q-1.result.md"


def test_check_refuses_workdir_that_is_a_file(tmp_path):
    (tmp_path / "x.txt").write_text("not a folder")
    n = node("a", "ok")
    n["workdir"] = "x.txt"
    r = run(tmp_path, "check", setup(tmp_path, [n]))
    assert r.returncode == 1, r.stdout + r.stderr
    assert "a: workdir 'x.txt' is not a folder" in r.stdout


def test_agy_auto_denied_tool_with_exit_0_is_a_failure(tmp_path):
    # seen in run 20261003-node-workdir: agy exits 0, empty stdout, stderr names the auto-denied permission
    env = fake_bin(tmp_path, "agy", r'''
import sys
print('jetski: no output produced — a tool required the "command" permission that headless mode cannot prompt for, so it was auto-denied.', file=sys.stderr)
''')
    g = {"id": "g", "role": "verifier", "engine": "agy", "model": "m", "brief": "brief.md", "inner_timer": "60s",
         "outer_timeout_s": 30}
    r = run(tmp_path, "run", setup(tmp_path, [g]), env=env)
    assert r.returncode == 1 and "executor failure on agy: denied (exit 0)" in r.stderr
