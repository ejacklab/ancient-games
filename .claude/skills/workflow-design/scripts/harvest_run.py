#!/usr/bin/env python3
"""harvest_run.py — read what the engines already recorded about a run and write one feedback file
(docs/research/20261002-workflow-feedback, option A, narrowed by the critic). Stdlib only, no model calls.

Sources (all internal, undocumented formats — every parser fails loudly when an expected key is missing):
  Workflow tool   ~/.claude/projects/*/<session>/workflows/<runId>.json  (per-agent state, durationMs, tokens)
                  .../subagents/workflows/<runId>/agent-<id>.jsonl         (message.usage per API call)
  codex           ~/.codex/sessions/**/rollout-*.jsonl, joined to a runlog.py `exec` event by its time window
                  and cwd (no guessing: zero or several matches are reported as unlinked)
  runlog events   runs/<run>/events.jsonl (verdicts, exec start/end)

Writes runs/<run>/feedback.jsonl (ids, numbers, paths and status only — never prompt or response text) and
prints a digest of at most 20 lines. Exit: 0 ok, 2 usage error, 3 a source format did not match (fail loud).

Token note (verified 2026-10-02): the Workflow run JSON's per-agent `tokens` is close to input +
cache-creation tokens; it leaves out cache reads (often 10x larger) and most output. So tokens are reported
in parts, and `tokens_reported` is kept beside them only as a cross-check.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

HOME = Path.home()
ROUND_RE = re.compile(r"\s*#(\d+)$")
LINK_SLACK_S = 5


class FormatChanged(Exception):
    pass


def need(d: dict, keys: list[str], where: str) -> None:
    missing = [k for k in keys if k not in d]
    if missing:
        raise FormatChanged(f"{where}: missing {missing}")


def iso(ms: float | None) -> str | None:
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000, timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def parse_ts(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def short(p: Path) -> str:
    s = str(p)
    return "~" + s[len(str(HOME)):] if s.startswith(str(HOME)) else s


def claude_usage(path: Path) -> dict:
    """Sum message.usage over the API calls of one agent transcript (lines repeat per message id; keep the last)."""
    per_msg: dict[str, dict] = {}
    models, tools = set(), 0
    for n, line in enumerate(path.open(), 1):
        e = json.loads(line)
        if e.get("type") != "assistant":
            continue
        need(e, ["message"], f"{short(path)}:{n}")
        m = e["message"]
        if "usage" not in m:
            raise FormatChanged(f"{short(path)}:{n}: assistant message has no usage")
        per_msg[m.get("id") or e.get("requestId") or str(n)] = m["usage"]
        if m.get("model"):
            models.add(m["model"])
        tools += sum(1 for c in m.get("content") or [] if isinstance(c, dict) and c.get("type") == "tool_use")
    s = lambda k: sum((u.get(k) or 0) for u in per_msg.values())
    return {"tokens_in": s("input_tokens"), "tokens_out": s("output_tokens"),
            "tokens_cache_read": s("cache_read_input_tokens"), "tokens_cache_write": s("cache_creation_input_tokens"),
            "api_calls": len(per_msg), "tool_calls_transcript": tools, "models": sorted(models)}


def harvest_workflow(run_id: str, wf: str, projects: Path) -> list[dict]:
    hits = list(projects.glob(f"*/*/workflows/{wf}.json"))
    if len(hits) != 1:
        raise FormatChanged(f"workflow run {wf}: expected one run JSON under {short(projects)}, found {len(hits)}")
    rj = hits[0]
    d = json.loads(rj.read_text())
    need(d, ["runId", "status", "durationMs", "workflowProgress"], short(rj))
    agent_dir = rj.parent.parent / "subagents" / "workflows" / wf
    rows = []
    for p in d["workflowProgress"]:
        if p.get("type") != "workflow_agent":
            continue
        need(p, ["label", "agentId", "state"], f"{short(rj)} agent entry")
        label = p["label"]
        m = ROUND_RE.search(label)
        row = {"run_id": run_id, "source": "workflow", "workflow_run": wf, "workflow_status": d["status"],
               "node_id": ROUND_RE.sub("", label), "round": int(m.group(1)) if m else 1,
               "engine": "claude-sub", "model": p.get("model"), "status": p["state"],
               "cached": bool(p.get("cached")), "ts_start": iso(p.get("startedAt")),
               "duration_ms": p.get("durationMs"), "tokens_reported": p.get("tokens"),
               "tool_calls": p.get("toolCalls"), "agent_id": p["agentId"]}
        if row["ts_start"] and row["duration_ms"] is not None:
            row["ts_end"] = iso(p["startedAt"] + p["durationMs"])
        tx = agent_dir / f"agent-{p['agentId']}.jsonl"
        if row["cached"]:
            row["cost_known"] = False          # replayed from cache: no tokens, no time (critic)
        elif tx.exists():
            row.update(claude_usage(tx)); row["cost_known"] = True; row["source_file"] = short(tx)
        else:
            row["cost_known"] = False; row["note"] = "transcript missing"
        rows.append(row)
    if not rows:
        raise FormatChanged(f"{short(rj)}: no workflow_agent entries")
    return rows


def codex_rollout(path: Path) -> dict:
    meta, model, usage, status, dur = None, None, [], "ok", 0
    for n, line in enumerate(path.open(), 1):
        e = json.loads(line)
        t, p = e.get("type"), e.get("payload") or {}
        if t == "session_meta":
            need(p, ["timestamp", "cwd"], f"{short(path)}:{n} session_meta")
            meta = p
        elif t == "turn_context":
            model = p.get("model") or model
        elif t == "token_usage_record":
            need(p, ["usage"], f"{short(path)}:{n} token_usage_record")
            usage.append(p["usage"])
        elif t == "event_msg" and p.get("type") == "task_complete":
            dur += p.get("duration_ms") or 0
            if p.get("error"):
                status = "fail"
        elif t == "event_msg" and p.get("type") == "turn_aborted":
            status = "fail"
    if meta is None:
        raise FormatChanged(f"{short(path)}: no session_meta")
    s = lambda k: sum((u.get(k) or 0) for u in usage)
    return {"start": parse_ts(meta["timestamp"]), "cwd": meta["cwd"], "model": model, "status": status,
            "engine_duration_ms": dur, "tokens_in": s("input_tokens"), "tokens_cache_read": s("cached_input_tokens"),
            "tokens_out": s("output_tokens"), "tokens_reasoning": s("reasoning_output_tokens")}


def harvest_codex(run_id: str, events: list[dict], sessions: Path) -> list[dict]:
    calls = [e for e in events if e.get("event") == "end" and e.get("engine") == "codex"]
    starts = {(e["node_id"], e["attempt"]): e for e in events if e.get("event") == "start"}
    if not calls:
        return []
    cache: dict[Path, dict] = {}
    rows = []
    for end in calls:
        st = starts.get((end["node_id"], end["attempt"]))
        lo = parse_ts(st["ts"]) - timedelta(seconds=LINK_SLACK_S) if st else None
        hi = parse_ts(end["ts"]) + timedelta(seconds=LINK_SLACK_S)
        day_dirs = {sessions / f"{d:%Y/%m/%d}" for d in (lo or hi, hi)}
        matches = []
        for dd in day_dirs:
            for f in dd.glob("rollout-*.jsonl"):
                r = cache.get(f) or cache.setdefault(f, codex_rollout(f))
                if lo and lo <= r["start"] <= hi and r["cwd"] == end.get("cwd"):
                    matches.append((f, r))
        row = {"run_id": run_id, "source": "codex", "node_id": end["node_id"], "round": end["attempt"],
               "engine": "codex", "status": end["status"], "exit_code": end.get("exit_code"),
               "duration_ms": end.get("duration_ms"), "ts_start": st["ts"] if st else None, "ts_end": end["ts"],
               "brief_variant": end.get("brief_variant")}
        if len(matches) == 1:
            f, r = matches[0]
            row.update({k: v for k, v in r.items() if k not in ("start", "cwd", "status")})
            row["engine_status"] = r["status"]
            row["cost_known"] = True; row["source_file"] = short(f)
        else:
            row["cost_known"] = False; row["note"] = f"unlinked: {len(matches)} rollouts matched the window"
        rows.append(row)
    return rows


def read_events(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for n, line in enumerate(path.open(), 1):
        e = json.loads(line)
        need(e, ["run_id", "node_id", "event", "ts"], f"{path}:{n}")
        out.append(e)
    return out


def digest(run_id: str, rows: list[dict], events: list[dict]) -> list[str]:
    known = [r for r in rows if r.get("cost_known")]
    tot = lambda k: sum(r.get(k) or 0 for r in known)
    lines = [f"run {run_id}: {len(rows)} calls ({len(known)} with cost), engines "
             + ", ".join(sorted({r['engine'] for r in rows}))]
    lines.append(f"tokens: new input {tot('tokens_in') + tot('tokens_cache_write'):,} · cache read "
                 f"{tot('tokens_cache_read'):,} · output {tot('tokens_out'):,}")
    wall = [r for r in rows if r.get("duration_ms")]
    if wall:
        slow = max(wall, key=lambda r: r["duration_ms"])
        lines.append(f"slowest: {slow['node_id']} r{slow['round']} {slow['duration_ms'] / 1000:.0f}s")
    if known:
        cost = lambda r: (r.get("tokens_in") or 0) + (r.get("tokens_cache_write") or 0) + (r.get("tokens_out") or 0)
        big = max(known, key=cost)
        lines.append(f"most new tokens: {big['node_id']} r{big['round']} {cost(big):,}")
    rounds = sorted({r["node_id"] for r in rows if r["round"] > 1})
    lines.append("nodes with more than one round: " + (", ".join(rounds) if rounds else "none"))
    unk = [r for r in rows if not r.get("cost_known")]
    if unk:
        lines.append(f"cost unknown: {len(unk)} call(s) ({', '.join(sorted({r.get('note') or 'cached' for r in unk}))})")
    drift = [abs((r.get("tokens_in", 0) + r.get("tokens_cache_write", 0)) - r["tokens_reported"]) / r["tokens_reported"]
             for r in known if r.get("tokens_reported")]
    if drift:
        lines.append(f"cross-check run JSON tokens vs transcript (input+cache write): max drift {max(drift):.1%}")
    verdicts = [e for e in events if e.get("event") == "verdict"]
    if verdicts:
        first = [v for v in verdicts if v.get("round", 1) == 1]
        lines.append(f"checks: {sum(v['pass'] for v in verdicts)}/{len(verdicts)} pass; first-try "
                     f"{sum(v['pass'] for v in first)}/{len(first)}")
    lines.append(f"ledger Actual cost: new {tot('tokens_in') + tot('tokens_cache_write'):,} / cache-read "
                 f"{tot('tokens_cache_read'):,} / out {tot('tokens_out'):,} tokens; "
                 f"{sum(r.get('duration_ms') or 0 for r in rows) / 60000:.1f} agent-min; {len(rows)} calls")
    return lines[:20]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", required=True, help="the run id: folder name under --runs-root")
    ap.add_argument("--workflow", action="append", default=[], help="a Workflow runId (wf_...) of this run")
    ap.add_argument("--runs-root", default="runs")
    ap.add_argument("--claude-projects", default=str(HOME / ".claude" / "projects"))
    ap.add_argument("--codex-sessions", default=str(HOME / ".codex" / "sessions"))
    a = ap.parse_args(argv)
    run_dir = Path(a.runs_root) / a.run
    try:
        events = read_events(run_dir / "events.jsonl")
        rows: list[dict] = []
        for wf in a.workflow:
            rows += harvest_workflow(a.run, wf, Path(a.claude_projects))
        rows += harvest_codex(a.run, events, Path(a.codex_sessions))
    except FormatChanged as e:
        print(f"harvest: FORMAT CHANGED? {e}", file=sys.stderr)
        return 3
    if not rows and not events:
        print(f"harvest: nothing to harvest for run {a.run} (no --workflow and no events.jsonl)", file=sys.stderr)
        return 2
    run_dir.mkdir(parents=True, exist_ok=True)
    tmp = run_dir / "feedback.jsonl.tmp"
    tmp.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))
    tmp.replace(run_dir / "feedback.jsonl")
    print("\n".join(digest(a.run, rows, events)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
