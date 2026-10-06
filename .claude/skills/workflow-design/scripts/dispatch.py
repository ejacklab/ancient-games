#!/usr/bin/env python3
"""dispatch.py — the dispatcher layer (docs/DISPATCHER_DESIGN.md). Runs a designed workflow's nodes from a plan file,
so the method's rules for running a node (3.7–3.8) are code: two timers, the brief's three parts, the
pass-back check, the engine-reported model check, repair rounds
with the check's real output as feedback, the event log, and a short digest. It makes no routing choice: every
node's engine is the one the plan names (design §5). Stdlib only; it calls no model itself.

  dispatch.py validate PLAN           validate the plan (timers, briefs, edges, engines); exit 0/1
  dispatch.py run PLAN [--dry-run]    run it; resumes from runs/<id>/dispatch.json; prints the digest

Engines: codex · qwen · agy · claude · dsh · script — one adapter each in `engines.py`, so adding or re-enabling an
engine is one entry there rather than four edits here. `claude` was refused while the dispatcher ran inside Claude
Code (the Workflow tool already served Claude nodes); that reason does not hold on another harness. `dsh` runs a node
on the DeepSeek Harness itself (`dsh headless`, one task, answer to stdout).
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
from engines import REGISTRY as ENGINES             # noqa: E402  (the engine adapters live in engines.py)

BRIEF_PARTS = ["## Template", "## Example", "## Standard"]
LOCK = threading.Lock()
FILLED = "(filled by the dispatcher)"
DEFAULT_BUDGET = {"max_rounds": 2, "max_calls": 30}

# How many **engine processes** the dispatcher keeps alive at once — `Popen` calls that have not exited.
#
# A **machine setting**, unmeasured (n=0): how many CLI processes this box should hold. It is NOT the harness's
# `maxActiveSubagents`, and reading it from there was a mistake made and corrected on 2026-10-05: that number bounds
# **resident child sessions** — a continuable subagent holds a slot while idle, waiting for its parent — so "8
# resident sessions" and "8 processes alive" are different quantities. Deriving one from the other is the same
# mis-transcription that produced the deleted "5 roles and 3 at once" rule: a number moved between units because the
# words looked alike.
#
# Measure it before trusting it.
MAX_ENGINE_PROCESSES = 8

# The ceiling on one call (method 3.8). EJ, 2026-10-05: *"we can't let an attempt keep running for more than 8
# hours, it is not healthy"* — a call that long has hidden its failure, cannot be watched, and leaves nothing to
# resume from. The per-task timers scale with the work; this does not. Hitting it is an executor failure, so the
# node blocks and reports. n=0: EJ's number, unmeasured.
MAX_CALL_SECONDS = 8 * 3600


# ---------------------------------------------------------------- plan
def load_plan(path: Path) -> dict:
    plan = json.loads(path.read_text())
    plan["budget"] = {**DEFAULT_BUDGET, **(plan.get("budget") or {})}
    return plan


def compare_plan_to_design(design: dict, plan: dict) -> list[str]:
    """Every fact the design promised the run depends on must survive into the plan.

    Revisits decision C (2026-10-05). C said nothing compares the plan to the design — one author, both artefacts, no
    checker. A traversal the same day measured what that costs: a hand-written plan **silently dropped two of three
    nodes' checks**, plus `touched_paths`, `baseline`, `categories` and `estimate`, and `validate_plan` said "plan ok".
    Every validator agreed while two checks had vanished.

    This is deliberately asymmetric. A plan carries things the design does not — a bare engine name, an exact model,
    timers, a brief path, a role — so equality is wrong. The rule is **the design's promises survive**; the plan may
    add, and may not lose.
    """
    f: list[str] = []
    dn = {n.get("id"): n for n in design.get("nodes") or []}
    pn = {n.get("id"): n for n in plan.get("nodes") or []}

    for nid, d in dn.items():
        p = pn.get(nid)
        if p is None:
            f.append(f"design node {nid!r} is missing from the plan")
            continue
        if d.get("check") and not p.get("check"):
            f.append(f"node {nid!r}: the design states a check and the plan carries none — the run would report "
                     f"done without checking anything")
        missing_needs = [x for x in (d.get("needs") or []) if x not in (p.get("needs") or [])]
        if missing_needs:
            f.append(f"node {nid!r}: the plan drops the design's edge(s) {missing_needs}")
        if d.get("sabotage") and not p.get("sabotage"):
            f.append(f"node {nid!r}: the design carries the sabotage proof and the plan drops it")
        if d.get("category") == "code review" and p.get("role") not in ("verifier", "reviewer", "review"):
            f.append(f"node {nid!r}: the design's reviewer became role {p.get('role')!r} in the plan")

    for nid in pn:
        if nid not in dn:
            f.append(f"plan node {nid!r} is not in the design — an undeclared node is an unreviewed node")

    if design.get("touched_paths") and not plan.get("touched_paths"):
        f.append("the design names touched_paths and the plan carries none — nothing can tell afterwards which "
                 "files the run was allowed to change")
    if design.get("baseline") and not plan.get("baseline"):
        f.append("the design names a baseline and the plan carries none")
    return f


def validate_plan(plan: dict, base: Path, design: dict | None = None) -> list[str]:
    f = []
    nodes = plan.get("nodes") or []
    if not plan.get("run_id"):
        f.append("plan has no run_id")
    if not nodes:
        f.append("plan has no nodes")
    ids = [n.get("id") for n in nodes]
    if len(ids) != len(set(ids)):
        f.append("node ids are not unique")
    # `load_plan` injects DEFAULT_BUDGET, so a plan read from disk always has one. Calling `validate_plan` on a bare
    # dict raised KeyError instead (found 2026-10-05 by a test that called it directly). Default it here too.
    b = plan.get("budget") or dict(DEFAULT_BUDGET)
    # The budget's own keys were never validated (found 2026-10-05 by an expert measuring rather than reading).
    # `max_rounds: "two"` reached `rec["rounds"] >= b["max_rounds"]` and raised TypeError mid-run; `-5` and
    # `true` made that comparison true on the first failure, so the loop silently stopped after one attempt;
    # `10**9` was accepted as no bound at all.
    for key in ("max_rounds", "max_calls"):
        v = b.get(key)
        if isinstance(v, bool) or not isinstance(v, int) or v < 1:
            f.append(f"budget.{key} must be a whole number of at least 1, not {v!r} "
                     f"(a boolean is not a count; a negative or absent bound stops the run early or not at all)")
    for n in nodes:
        nid = n.get("id", "?")
        adapter = ENGINES.get(n.get("engine"))
        if adapter is None:
            f.append(f"{nid}: engine {n.get('engine')!r} is not one of {sorted(ENGINES)}")
        elif adapter.needs_model and not n.get("model"):
            f.append(f"{nid}: no model (every node names its model, EXECUTOR_KINDS)")
        if n.get("engine") != "script":
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
        chk = n.get("check")
        if chk is not None and (not isinstance(chk, dict) or not chk.get("cmd")):
            # Found 2026-10-05 by the traversal: a judged check (a fixed checklist, no `cmd` — the method's second
            # tier) was accepted here and then raised `KeyError: 'cmd'` inside verify_node_result. Accepted at validation and
            # fatal at run time is the worst of both. Until a plan can carry a judged check, refuse it loudly.
            f.append(f"{nid}: check {chk!r} has no `cmd` — a judged check cannot run yet, and accepting it here "
                     f"only moves the failure to the run")
        if not isinstance(n.get("outer_timeout_s"), (int, float)) or n["outer_timeout_s"] <= 0:
            f.append(f"{nid}: no outer_timeout_s (method 3.8 item 2)")
        # The ceiling on one call. Without this the rule was prose: the per-task timers scale with the work and
        # nothing bounded a single call, so a node could ask for a 40-hour timeout and every check would pass.
        elif n["outer_timeout_s"] > MAX_CALL_SECONDS:
            f.append(f"{nid}: outer_timeout_s {n['outer_timeout_s']}s is past the ceiling of {MAX_CALL_SECONDS}s "
                     f"(8 h, method 3.8) — cut the work into segments")
        for d in n.get("needs") or []:
            if d not in ids:
                f.append(f"{nid}: needs unknown node {d!r}")
        if n.get("repair") and n["repair"] not in ids:
            f.append(f"{nid}: repair node {n['repair']!r} not in the plan")
        # No fallback (removed 2026-10-05 at EJ's direction): a node that fails is blocked and reported, and the
        # COO decides. The fallback added a second engine, a second model and a second workdir to reason about, and
        # a plan could silently finish on an engine nobody chose — including one that turns a builder into the
        # reviewer's own kind (register 8.2). A failure that reports is simpler and loses nothing.
        for target in [n]:
            if "workdir" in target:
                workdir = base / target["workdir"]
                if workdir.exists() and not workdir.is_dir():
                    f.append(f"{nid}: workdir {target['workdir']!r} is not a folder")
    if not f and _cycle(nodes):
        f.append("dependency cycle")
    if design is not None:
        f.extend(compare_plan_to_design(design, plan))
    return f


NO_DESIGN_NOTE = ("note: no --design given, so nothing compared this plan against the design it came from. That is "
                  "how two of three checks were lost on 2026-10-05; pass --design to have them compared.")


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
            f"a header between two lines of `---` with exactly these keys, then the body the Template asks for. Write nothing before the first `---`.\n"
            f"node: {node['id']}\nattempt: {attempt}\nengine: {engine}\nmodel: {model}\n"
            f"status: ok | fail | partial\nstarted: {FILLED}\nended: {FILLED}\nevidence: <path to your proof, or none>\n"
            f"Copy node, attempt, engine, model, started and ended exactly as written; the dispatcher fills the times and\n"
            f"checks the model with the tool itself.\n"
            f"If something is unclear, do not guess: write a body line `UNCLEAR: <question> / <best guess>`.\n")


# build_command and final_answer now live in engines.py, one adapter per engine. This module keeps only what is
# engine-neutral: the plan validation, the loop, the timers, the process group, the pass-back and model checks.


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
    adapter = ENGINES[engine]
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
    cmd = adapter.build(node, model, prompt, out_file, cwd, attempt)
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
            status = next((st for m, st in adapter.silent_failures.items() if m in stderr), status)
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
        text, reported = adapter.parse(stdout, out_file)
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


def verify_node_result(plan: dict, node: dict, result: str, run_dir: Path, base: Path, rnd: int) -> tuple[bool, str]:
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
    """One node to done, or raise Stop. Executor failure: blocked and reported. Check failure: repair
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
            # Blocked, and reported. The engine failed; that is a fact for the COO, not something to paper over by
            # quietly running the same work somewhere else (removed 2026-10-05 at EJ's direction).
            rec["status"] = "blocked"
            raise Stop(f"{node['id']} blocked: executor failed on {engine} ({r['why']})")
        if r["outcome"] == "unclear":
            rec["status"] = "unclear"; raise Stop(f"{node['id']} asks: {r['why']}")
        if r["outcome"] == "dry":
            rec["status"] = "done"; return
        if r["why"]:
            log(f"{node['id']} a{attempt}: {r['why']}")
        ok, out = verify_node_result(plan, node, r["result"], run_dir, base, rec["rounds"] + 1)
        if ok:
            rec.update(status="done", result=r["result"]); log(f"{node['id']} done (a{attempt}, {engine})"); return
        rec["rounds"] += 1
        log(f"{node['id']} check failed (round {rec['rounds']})")
        limit = b["max_rounds"] if isinstance(b.get("max_rounds"), int) and not isinstance(b.get("max_rounds"), bool) else 0
        if rec["rounds"] >= limit or not node.get("repair"):
            rec["status"] = "blocked"; raise Stop(f"{node['id']} blocked: check failed {rec['rounds']} round(s)")
        target = by_id[node["repair"]] if node["repair"] != node["id"] else node
        feedback = out


def cmd_run(a) -> int:
    plan_path = Path(a.plan)
    plan = load_plan(plan_path)
    base = Path(a.root).resolve()
    design = json.loads(Path(a.design).read_text()) if getattr(a, "design", None) else None
    problems = validate_plan(plan, base, design=design)
    if design is None:
        print(NO_DESIGN_NOTE, file=sys.stderr)
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
                with ThreadPoolExecutor(max_workers=MAX_ENGINE_PROCESSES) as ex:
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
    c = sub.add_parser("validate"); c.add_argument("plan")
    c.add_argument("--design", help="the design.json this plan came from; without it nothing compares the two")
    r = sub.add_parser("run"); r.add_argument("plan"); r.add_argument("--dry-run", action="store_true")
    r.add_argument("--design", help="the design.json this plan came from; the run refuses a plan that loses it")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "validate":
            plan = load_plan(Path(a.plan))
            design = json.loads(Path(a.design).read_text()) if getattr(a, "design", None) else None
            problems = validate_plan(plan, Path(a.root).resolve(), design=design)
            print("plan ok" if not problems else "plan refused:\n  " + "\n  ".join(problems))
            if design is None:
                print(NO_DESIGN_NOTE, file=sys.stderr)
            return 0 if not problems else 1
        return cmd_run(a)
    except (OSError, ValueError, KeyError) as e:
        print(f"dispatch: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
