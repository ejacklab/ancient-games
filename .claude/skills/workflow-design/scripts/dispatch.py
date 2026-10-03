#!/usr/bin/env python3
"""dispatch.py — the dispatcher layer (docs/DISPATCHER_DESIGN.md). Runs a designed workflow's nodes from a plan file,
so the method's rules for running a node (3.7–3.8) are code: caps, two timers, the brief's three parts, the
pass-back check, the engine-reported model check, one retry of an executor failure on the fallback, repair rounds
with the check's real output as feedback, the event log, and a short digest. It makes no routing choice: every
node's engine is the one the plan names (design §5). Stdlib only; it calls no model itself.

  dispatch.py check PLAN              validate the plan (caps, timers, briefs, edges); exit 0/1
  dispatch.py run PLAN [--dry-run]    run it; resumes from runs/<id>/dispatch.json; prints the digest

Engines: codex · qwen · agy · script (a local command, for tests and checks). Claude nodes are not dispatched here:
they run with the Workflow tool (EJ, 2026-10-03), and a plan naming engine `claude` is refused.
The node's result file is the engine's final answer: header + body (docs/workflow-templates/result-file.md).
The dispatcher writes runs/<id>/dispatch.json (its own state) and events.jsonl; it never edits the COO's state.md.
Exit (run): 0 all done · 1 stopped on a blocked node, an UNCLEAR question or a budget limit · 2 plan or usage error.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from runlog import append, now                      # noqa: E402  (same folder)
from validate_result import check_result            # noqa: E402

ENGINES = {"codex", "qwen", "agy", "script"}
BRIEF_PARTS = ["## Template", "## Example", "## Standard"]
LOCK = threading.Lock()
FILLED = "(filled by the dispatcher)"
# stderr notices that mean the call did not finish although the exit code is 0 (verified 2026-10-03)
SILENT_FAILURES = {"agy": {"print timeout": "timeout", "auto-denied": "denied"}}   # also: a tool needing a permission headless
# mode cannot grant ("jetski: no output produced — ... was auto-denied"), seen in run 20261003-node-workdir
DEFAULT_BUDGET = {"max_roles": 5, "max_parallel": 3, "max_rounds": 2, "max_calls": 30}


# ---------------------------------------------------------------- plan
def load_plan(path: Path) -> dict:
    plan = json.loads(path.read_text())
    plan["budget"] = {**DEFAULT_BUDGET, **(plan.get("budget") or {})}
    return plan


def check_plan(plan: dict, base: Path) -> list[str]:
    f = []
    nodes = plan.get("nodes") or []
    if not plan.get("run_id"):
        f.append("plan has no run_id")
    if not nodes:
        f.append("plan has no nodes")
    ids = [n.get("id") for n in nodes]
    if len(ids) != len(set(ids)):
        f.append("node ids are not unique")
    b = plan["budget"]
    roles = {n.get("role") for n in nodes if n.get("engine") != "script"}
    if len(roles) > b["max_roles"]:
        f.append(f"{len(roles)} roles > cap {b['max_roles']}: cut the run into slices (method 3.7)")
    groups: dict[str, int] = {}
    for n in nodes:
        nid = n.get("id", "?")
        if n.get("parallel_group"):
            groups[n["parallel_group"]] = groups.get(n["parallel_group"], 0) + 1
        if n.get("engine") == "claude":
            f.append(f"{nid}: Claude nodes run with the Workflow tool, not the dispatcher (EJ, 2026-10-03)")
        elif n.get("engine") not in ENGINES:
            f.append(f"{nid}: engine {n.get('engine')!r} is not one of {sorted(ENGINES)}")
        if n.get("engine") != "script":
            if not n.get("model"):
                f.append(f"{nid}: no model (every node names its model, EXECUTOR_KINDS)")
            if not n.get("inner_timer"):
                f.append(f"{nid}: no inner_timer (method 3.8 item 2)")
            brief = base / n.get("brief", "")
            if not n.get("brief") or not brief.is_file():
                f.append(f"{nid}: brief {n.get('brief')!r} not found")
            else:
                missing = [p for p in BRIEF_PARTS if p not in brief.read_text()]
                if missing:
                    f.append(f"{nid}: brief lacks {missing} (method 3.8 item 8)")
        elif not n.get("cmd"):
            f.append(f"{nid}: a script node needs cmd")
        if not isinstance(n.get("outer_timeout_s"), (int, float)) or n["outer_timeout_s"] <= 0:
            f.append(f"{nid}: no outer_timeout_s (method 3.8 item 2)")
        for d in n.get("needs") or []:
            if d not in ids:
                f.append(f"{nid}: needs unknown node {d!r}")
        if n.get("repair") and n["repair"] not in ids:
            f.append(f"{nid}: repair node {n['repair']!r} not in the plan")
        fb = n.get("fallback")
        if fb and (fb.get("engine") not in ENGINES or (fb.get("engine") != "script" and not fb.get("model"))):
            f.append(f"{nid}: fallback needs a known engine and a model")
        for target in [n, fb] if fb else [n]:
            if "workdir" in target:
                workdir = base / target["workdir"]
                if workdir.exists() and not workdir.is_dir():
                    f.append(f"{nid}: workdir {target['workdir']!r} is not a folder")
    for g, k in groups.items():
        if k > b["max_parallel"]:
            f.append(f"parallel group {g!r} has {k} nodes > cap {b['max_parallel']}")
    if not f and _cycle(nodes):
        f.append("dependency cycle")
    return f


def _cycle(nodes: list[dict]) -> bool:
    deps = {n["id"]: set(n.get("needs") or []) for n in nodes}
    done: set = set()
    while deps:
        ready = [k for k, v in deps.items() if v <= done]
        if not ready:
            return True
        for k in ready:
            done.add(k); deps.pop(k)
    return False


# ---------------------------------------------------------------- engines
def passback_note(node: dict, engine: str, model: str, attempt: int) -> str:
    return (f"\n\n## Pass-back (from the dispatcher)\nYour final answer must be the result file itself and nothing else:\n"
            f"a header between two lines of `---` with exactly these keys, then the body the Template asks for.\n"
            f"node: {node['id']}\nattempt: {attempt}\nengine: {engine}\nmodel: {model}\n"
            f"status: ok | fail | partial\nstarted: {FILLED}\nended: {FILLED}\nevidence: <path to your proof, or none>\n"
            f"Copy node, attempt, engine, model, started and ended exactly as written; the dispatcher fills the times and\n"
            f"checks the model with the tool itself.\n"
            f"If something is unclear, do not guess: write a body line `UNCLEAR: <question> / <best guess>`.\n")


def build_command(node: dict, engine: str, model: str, prompt: str, out_file: Path, cwd: Path,
                  attempt: int = 1) -> list[str]:
    t = node.get("inner_timer", "")
    mode = node.get("mode", "read-only")
    if engine == "codex":
        cmd = ["codex", "exec", "-m", model, "-s", "workspace-write" if mode == "write" else "read-only",
               "-C", str(cwd), "-o", str(out_file)]
        if node.get("effort"):
            cmd += ["-c", f"model_reasoning_effort={node['effort']}"]
        return cmd + [prompt]
    if engine == "qwen":
        return ["qwen", "--approval-mode", "auto-edit" if mode == "write" else "plan", "--max-wall-time", t,
                "-m", model, "--output-format", "json", prompt]
    if engine == "agy":
        return ["agy", "-p", prompt, "--mode", "accept-edits" if mode == "write" else "plan", "--model", model,
                "--print-timeout", t, "--output-format", "text"]
    return [str(x).replace("{prompt_file}", str(out_file.with_suffix(".prompt"))).replace("{out}", str(out_file))
            .replace("{attempt}", str(attempt)) for x in node["cmd"]]


def final_answer(engine: str, stdout: str, out_file: Path) -> tuple[str, str | None]:
    """(result text, the model the tool itself reported, or None). Raises ValueError on an unreadable stream."""
    if engine == "codex":
        return (out_file.read_text() if out_file.exists() else ""), None
    if engine == "qwen":
        events = json.loads(stdout)
        res = next((e for e in events if e.get("type") == "result"), None)
        init = next((e for e in events if e.get("type") == "system"), {})
        if res is None:
            raise ValueError("qwen stream has no result event")
        return res.get("result") or "", init.get("model")
    if engine == "script" and out_file.exists():
        return out_file.read_text(), None
    return stdout, None


# ---------------------------------------------------------------- one call
def run_group(cmd: list[str], timeout: float, cwd: Path) -> tuple[int, str, str]:
    """Run cmd in its own process group; on timeout kill the whole group, not only the first process: `qwen` is a
    wrapper whose node child survived a plain kill and kept running (seen 2026-10-03). No stdin: an engine must
    never wait on ours. Raises TimeoutExpired carrying whatever was printed before the timer fired."""
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, text=True,
                         cwd=cwd, start_new_session=True)
    try:
        out, err = p.communicate(timeout=timeout)
        return p.returncode, out, err
    except subprocess.TimeoutExpired:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        out, err = p.communicate()
        raise subprocess.TimeoutExpired(cmd, timeout, output=out, stderr=err)


def call(plan: dict, node: dict, attempt: int, run_dir: Path, base: Path, engine: str, model: str,
         feedback: str | None, dry: bool) -> dict:
    """Run one engine call; return {'outcome': ok|executor|unclear, 'why', 'result'}."""
    nid = node["id"]
    nodes_dir = run_dir / "nodes"; nodes_dir.mkdir(parents=True, exist_ok=True)
    out_file = nodes_dir / f"{nid}-{attempt}.result.md"
    prompt = ""
    if engine != "script":
        prompt = (base / node["brief"]).read_text() + passback_note(node, engine, model, attempt)
        if feedback:
            prompt += f"\n## Feedback from the last attempt (the check's real output)\n{feedback}\n"
    else:
        out_file.with_suffix(".prompt").write_text(feedback or "")
    cwd = (base / node["workdir"]).resolve() if "workdir" in node else base
    cmd = build_command(node, engine, model, prompt, out_file, cwd, attempt)
    if dry:
        print(f"[dry-run] {nid} attempt {attempt}: " + " ".join(
            c if len(c) < 60 or ("workdir" in node and c == str(cwd)) else c[:57] + "..." for c in cmd))
        return {"outcome": "dry", "why": "", "result": ""}
    cwd.mkdir(parents=True, exist_ok=True)
    raw = run_dir / "raw"; raw.mkdir(exist_ok=True)
    ev = {"run_id": plan["run_id"], "node_id": nid, "attempt": attempt, "engine": engine, "model": model,
          "cwd": str(cwd)}
    started = now()
    append(run_dir, {**ev, "event": "start", "ts": started})
    t0 = time.monotonic()
    status, code, stdout, stderr = "ok", 0, "", ""
    try:
        code, stdout, stderr = run_group(cmd, node["outer_timeout_s"], cwd)
        (raw / f"{nid}-{attempt}-{engine}.stdout").write_text(stdout)
        (raw / f"{nid}-{attempt}-{engine}.stderr").write_text(stderr)
        status = "ok" if code == 0 else "fail"
        if status == "ok":                                 # exit 0, yet the tool says it did not finish
            status = next((st for m, st in SILENT_FAILURES.get(engine, {}).items() if m in stderr), status)
    except subprocess.TimeoutExpired as e:
        status, code = "timeout", 124                      # keep whatever it printed before the timer fired
        for name, data in (("stdout", e.stdout), ("stderr", e.stderr)):
            if data:
                (raw / f"{nid}-{attempt}-{engine}.{name}").write_text(
                    data if isinstance(data, str) else data.decode(errors="replace"))
    except OSError as e:
        status, code = "fail", 127
        (raw / f"{nid}-{attempt}-{engine}.stderr").write_text(str(e))
    append(run_dir, {**ev, "event": "end", "ts": now(), "status": status, "exit_code": code,
                     "duration_ms": int((time.monotonic() - t0) * 1000)})
    if status != "ok":
        return {"outcome": "executor", "why": f"{status} (exit {code})", "result": ""}
    try:
        text, reported = final_answer(engine, stdout, out_file)
    except (ValueError, json.JSONDecodeError) as e:
        return {"outcome": "executor", "why": f"unreadable output: {e}", "result": ""}
    if engine != "script" and reported and reported != model:
        return {"outcome": "executor", "why": f"tool reports model {reported!r}, plan says {model!r}", "result": ""}
    if not text.strip():
        return {"outcome": "executor", "why": "empty result (exit 0 with no answer)", "result": ""}
    ended = now()
    text = text.replace(f"started: {FILLED}", f"started: {started}").replace(f"ended: {FILLED}", f"ended: {ended}")
    out_file.write_text(text if text.endswith("\n") else text + "\n")
    if node.get("passback") is False:                 # a plain script step: no result header expected
        return {"outcome": "ok", "why": "", "result": str(out_file)}
    findings, body, _ = check_result(text, node=nid, attempt=str(attempt))
    if findings:
        return {"outcome": "executor", "why": "pass-back: " + "; ".join(findings), "result": str(out_file)}
    if any(l.strip().startswith("UNCLEAR:") for l in body.splitlines()):
        q = next(l.strip() for l in body.splitlines() if l.strip().startswith("UNCLEAR:"))
        return {"outcome": "unclear", "why": q, "result": str(out_file)}
    return {"outcome": "ok", "why": "" if reported else "model unverified (tool did not report it)",
            "result": str(out_file)}


def run_check(plan: dict, node: dict, result: str, run_dir: Path, base: Path, rnd: int) -> tuple[bool, str]:
    chk = node.get("check")
    if not chk:
        return True, ""
    cmd = [str(x).replace("{result}", result).replace("{run_dir}", str(run_dir)) for x in chk["cmd"]]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=chk.get("timeout_s", 600), cwd=base)
        ok, out = p.returncode == 0, (p.stdout + p.stderr)
    except (subprocess.TimeoutExpired, OSError) as e:
        ok, out = False, f"check could not run: {e}"
    append(run_dir, {"run_id": plan["run_id"], "node_id": node["id"], "round": rnd, "event": "verdict",
                     "ts": now(), "check": chk.get("name", "check"), "pass": ok})
    return ok, out[-4000:]


# ---------------------------------------------------------------- the loop
class Stop(Exception):
    pass


def run_node(plan, node, by_id, state, run_dir, base, dry, log) -> None:
    """One node to done, or raise Stop. Executor failure: one fresh rerun on the fallback. Check failure: repair
    rounds up to max_rounds, each with the check's real output as feedback."""
    b = plan["budget"]
    with LOCK:
        rec = state["nodes"].setdefault(node["id"], {"status": "todo", "rounds": 0, "calls": 0})
    feedback, target = None, node
    while True:
        attempt = rec["calls"] + 1
        engine, model = target["engine"], target.get("model", "")
        with LOCK:
            if state["calls"] >= b["max_calls"]:
                raise Stop(f"budget: {b['max_calls']} calls reached before {node['id']}")
            state["calls"] += 1; rec["calls"] += 1
        r = call(plan, target, attempt, run_dir, base, engine, model, feedback, dry)
        if r["outcome"] == "executor":
            log(f"{node['id']} a{attempt}: executor failure on {engine}: {r['why']}")
            fb = target.get("fallback")
            if not fb or rec.get("fell_back"):
                rec["status"] = "blocked"; raise Stop(f"{node['id']} blocked: executor failed ({r['why']})")
            rec["fell_back"] = True
            target = {**target, **fb, "id": node["id"], "fallback": None}
            feedback = (feedback or "") + f"\nHandoff: the previous call on {engine} failed: {r['why']}."
            continue
        if r["outcome"] == "unclear":
            rec["status"] = "unclear"; raise Stop(f"{node['id']} asks: {r['why']}")
        if r["outcome"] == "dry":
            rec["status"] = "done"; return
        if r["why"]:
            log(f"{node['id']} a{attempt}: {r['why']}")
        ok, out = run_check(plan, node, r["result"], run_dir, base, rec["rounds"] + 1)
        if ok:
            rec.update(status="done", result=r["result"]); log(f"{node['id']} done (a{attempt}, {engine})"); return
        rec["rounds"] += 1
        log(f"{node['id']} check failed (round {rec['rounds']})")
        if rec["rounds"] >= b["max_rounds"] or not node.get("repair"):
            rec["status"] = "blocked"; raise Stop(f"{node['id']} blocked: check failed {rec['rounds']} round(s)")
        target = by_id[node["repair"]] if node["repair"] != node["id"] else node
        feedback = out


def cmd_run(a) -> int:
    plan_path = Path(a.plan)
    plan = load_plan(plan_path)
    base = Path(a.root).resolve()
    problems = check_plan(plan, base)
    if problems:
        print("plan refused:\n  " + "\n  ".join(problems), file=sys.stderr)
        return 2
    run_dir = base / a.runs_root / plan["run_id"]; run_dir.mkdir(parents=True, exist_ok=True)
    st_path = run_dir / "dispatch.json"
    state = json.loads(st_path.read_text()) if st_path.exists() and not a.dry_run else {"calls": 0, "nodes": {}}
    lines: list[str] = []
    log = lambda m: (lines.append(m), print(m, file=sys.stderr))
    by_id = {n["id"]: n for n in plan["nodes"]}
    done = {k for k, v in state["nodes"].items() if v.get("status") == "done"}
    for k in done:
        log(f"{k} already done (resume)")
    stopped = None
    try:
        while len(done) < len(plan["nodes"]):
            ready = [n for n in plan["nodes"] if n["id"] not in done and set(n.get("needs") or []) <= done]
            if not ready:
                raise Stop("no node is ready (a blocked dependency)")
            group = ready[0].get("parallel_group")
            batch = [n for n in ready if group and n.get("parallel_group") == group] or [ready[0]]
            if len(batch) == 1:
                run_node(plan, batch[0], by_id, state, run_dir, base, a.dry_run, log)
            else:
                with ThreadPoolExecutor(max_workers=plan["budget"]["max_parallel"]) as ex:
                    futs = [ex.submit(run_node, plan, n, by_id, state, run_dir, base, a.dry_run, log) for n in batch]
                    errs = [f.exception() for f in futs if f.exception()]
                if errs:
                    raise errs[0] if isinstance(errs[0], Stop) else Stop(str(errs[0]))
            done |= {n["id"] for n in batch}
            if not a.dry_run:
                st_path.write_text(json.dumps(state, indent=1, sort_keys=True))
    except Stop as e:
        stopped = str(e)
    finally:
        if not a.dry_run:
            st_path.write_text(json.dumps(state, indent=1, sort_keys=True))
    total = len(plan["nodes"])
    n_done = sum(1 for v in state["nodes"].values() if v.get("status") == "done")
    print(f"dispatch {plan['run_id']}: {'STOPPED' if stopped else 'DONE'} — {n_done}/{total} nodes done, "
          f"{state['calls']} call(s)")
    if stopped:
        print(f"needs the COO: {stopped}")
    for n in plan["nodes"]:
        rec = state["nodes"].get(n["id"], {})
        print(f"  {n['id']:16} {rec.get('status', 'todo'):8} calls {rec.get('calls', 0)} rounds {rec.get('rounds', 0)}"
              + (f"  {rec['result']}" if rec.get("result") else ""))
    print(f"events: {run_dir / 'events.jsonl'} · state: {st_path}")
    return 1 if stopped else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".", help="repo root: briefs and commands resolve against it")
    ap.add_argument("--runs-root", default="runs")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check"); c.add_argument("plan")
    r = sub.add_parser("run"); r.add_argument("plan"); r.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "check":
            plan = load_plan(Path(a.plan))
            problems = check_plan(plan, Path(a.root).resolve())
            print("plan ok" if not problems else "plan refused:\n  " + "\n  ".join(problems))
            return 0 if not problems else 1
        return cmd_run(a)
    except (OSError, ValueError, KeyError) as e:
        print(f"dispatch: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
