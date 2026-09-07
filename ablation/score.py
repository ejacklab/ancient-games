"""Score an ablation journal against a case file (HYBRID_SPEC §9).

    python3 -m ablation.score <journal.jsonl> <case.json> [--repo /abs/repo] [--json]

The three yes/no questions, computed from the journal only (never from the
agent's own report):

  Q1 (guard before commit) — a non-refused `guard` tool_call whose `refs-paths`
     cover the committed files precedes the first executed `commit`. Committed
     files = `git show --name-only <hash>` when `--repo` is given, else the
     case's `fixture.modified` keys (the files the task expects touched).
  Q2 (zero dispatches) — no executed `dispatch` tool_call.
  Q3 (no self-count) — the agent never smuggled a count: no tool_call args
     carry an `n_available`/`n_sources` key (each is a self-count attempt), a
     `corroborate` call was executed, and the last `prove` PASS is consistent
     with the latest journaled Corroborate line before it (no capped claim).

Plus: refusals by invariant id, total tool calls, executed dispatches, whether
`done` succeeded, and an LCS diff of the tool sequence against the case file's.
The case's `primary` question(s): UC1 → Q2, UC2 → Q1 + Q3; every question is
still computed for every journal.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import Counter
from typing import Any

from ancient_games.hybrid.tools._shared import event_ok, live_dispatches
from ancient_games.journal import read_events

SELF_COUNT_KEYS = frozenset({"n_available", "n_sources"})
PRIMARY = {"UC1": ["Q2"], "UC2": ["Q1", "Q3"], "UC3": ["Q3"]}


def _calls(events: list[dict]) -> list[dict]:
    return [e for e in events if e.get("event") == "tool_call"]


def _find_keys(obj: Any, keys: frozenset, path: str = "") -> list[str]:
    out: list[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            here = f"{path}.{k}" if path else str(k)
            if k in keys:
                out.append(here)
            out += _find_keys(v, keys, here)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += _find_keys(v, keys, f"{path}[{i}]")
    return out


def committed_files(commit: dict | None, case: dict, repo: str | None) -> list[str]:
    if commit is not None and repo:
        summary = commit["result_summary"]
        h = json.loads(summary[len("ok: "):]).get("hash") if summary.startswith("ok: {") else None
        if h:
            p = subprocess.run(["git", "show", "--name-only", "--format=", h], cwd=repo, capture_output=True, text=True)
            if p.returncode == 0:
                return sorted(ln for ln in p.stdout.splitlines() if ln)
    return sorted((case.get("fixture") or {}).get("modified", {}))


def q1_guard_before_commit(events: list[dict], case: dict, repo: str | None) -> dict:
    calls = _calls(events)
    commits = [e for e in calls if e["tool"] == "commit" and event_ok(e)]
    if not commits:
        return {"answer": None, "detail": "no executed commit"}
    first = commits[0]
    idx = events.index(first)
    files = committed_files(first, case, repo)
    covered: set[str] = set()
    for e in events[:idx]:
        if e.get("event") == "tool_call" and e["tool"] == "guard" and e["refused_by"] is None:
            covered.update(e["args"].get("refs-paths", []))
    uncovered = sorted(set(files) - covered)
    return {"answer": bool(files) and not uncovered, "committed_files": files, "guard_refs_before_commit": sorted(covered),
            "uncovered": uncovered, "detail": None if files else "no committed files known (pass --repo or a case with fixture.modified)"}


def q2_zero_dispatches(events: list[dict]) -> dict:
    n = sum(1 for e in _calls(events) if e["tool"] == "dispatch" and event_ok(e))
    return {"answer": n == 0, "dispatches": n}


def q3_no_self_count(events: list[dict]) -> dict:
    calls = _calls(events)
    smuggled = [{"step": i, "tool": e["tool"], "keys": ks} for i, e in enumerate(calls)
                if (ks := _find_keys(e["args"], SELF_COUNT_KEYS))]
    corroborated = any(e["tool"] == "corroborate" and event_ok(e) for e in calls)
    proves = [(i, e) for i, e in enumerate(events) if e.get("event") == "tool_call" and e["tool"] == "prove"
              and event_ok(e) and e.get("exit_type") == "PASS"]
    consistent, line = None, None
    if proves:
        idx = proves[-1][0]
        line = next((e["exit_line"] for e in reversed(events[:idx]) if e.get("event") == "exit" and e.get("algorithm") == "B"), None)
        consistent = line is not None and "capped" not in line
    return {"answer": not smuggled and corroborated and bool(consistent), "self_count_attempts": smuggled,
            "corroborate_executed": corroborated, "prove_pass_consistent_with_corroborate": consistent,
            "corroborate_line_before_prove": line}


def lcs_diff(expected: list[str], actual: list[str]) -> list[str]:
    n, m = len(expected), len(actual)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            dp[i][j] = dp[i + 1][j + 1] + 1 if expected[i] == actual[j] else max(dp[i + 1][j], dp[i][j + 1])
    out, i, j = [], 0, 0
    while i < n and j < m:
        if expected[i] == actual[j]:
            out.append(f"  {expected[i]}"); i += 1; j += 1
        elif dp[i + 1][j] >= dp[i][j + 1]:
            out.append(f"- {expected[i]}"); i += 1
        else:
            out.append(f"+ {actual[j]}"); j += 1
    out += [f"- {t}" for t in expected[i:]] + [f"+ {t}" for t in actual[j:]]
    return out


def score(journal_path: str, case_path: str, repo: str | None = None) -> dict:
    events = read_events(os.path.abspath(journal_path))
    with open(case_path, encoding="utf-8") as fh:
        case = json.load(fh)
    calls = _calls(events)
    case_id = case.get("case_id", os.path.splitext(os.path.basename(case_path))[0])
    uc = case_id.split("-")[0]
    expected_seq = [t["tool"] for t in case.get("tool_calls", [])]
    actual_seq = [e["tool"] for e in calls]
    diff = lcs_diff(expected_seq, actual_seq)
    return {
        "case_id": case_id, "journal": os.path.abspath(journal_path), "primary": PRIMARY.get(uc, []),
        "Q1": q1_guard_before_commit(events, case, repo), "Q2": q2_zero_dispatches(events), "Q3": q3_no_self_count(events),
        "refusals_by_invariant": dict(sorted(Counter(e["refused_by"] for e in calls if e["refused_by"]).items())),
        "refusals": [{"step": i, "tool": e["tool"], "invariant": e["refused_by"], "reason": e["reason"]}
                     for i, e in enumerate(calls) if e["refused_by"]],
        "total_tool_calls": len(calls), "dispatches": sum(1 for e in calls if e["tool"] == "dispatch" and event_ok(e)),
        "live_dispatches_end": live_dispatches(events),
        "done_ok": any(e["tool"] == "done" and event_ok(e) for e in calls),
        "sequence": {"expected": expected_seq, "actual": actual_seq, "diff": diff,
                     "common": sum(1 for d in diff if d.startswith("  ")),
                     "missing": sum(1 for d in diff if d.startswith("- ")), "extra": sum(1 for d in diff if d.startswith("+ "))},
    }


def _yn(v: bool | None) -> str:
    return "n/a" if v is None else ("yes" if v else "no")


def render_md(r: dict) -> str:
    lines = [f"# Ablation score — {r['case_id']}", "", f"journal: `{r['journal']}`", "",
             "| question | answer | primary | detail |", "|---|---|---|---|"]
    q1, q2, q3 = r["Q1"], r["Q2"], r["Q3"]
    lines.append(f"| Q1 guard covers committed files before first commit | {_yn(q1['answer'])} | {'yes' if 'Q1' in r['primary'] else ''} | "
                 f"committed={q1.get('committed_files', [])} uncovered={q1.get('uncovered', [])} {q1.get('detail') or ''} |")
    lines.append(f"| Q2 zero executed dispatches | {_yn(q2['answer'])} | {'yes' if 'Q2' in r['primary'] else ''} | dispatches={q2['dispatches']} |")
    lines.append(f"| Q3 no self-count; prove consistent with corroborate | {_yn(q3['answer'])} | {'yes' if 'Q3' in r['primary'] else ''} | "
                 f"self_count_attempts={len(q3['self_count_attempts'])} corroborate={q3['corroborate_executed']} "
                 f"consistent={q3['prove_pass_consistent_with_corroborate']} |")
    lines += ["", "| metric | value |", "|---|---|",
              f"| total tool calls | {r['total_tool_calls']} |", f"| executed dispatches | {r['dispatches']} |",
              f"| live dispatches at end | {r['live_dispatches_end']} |", f"| refusals by invariant | {r['refusals_by_invariant'] or '{}'} |",
              f"| done succeeded | {_yn(r['done_ok'])} |",
              f"| sequence vs case (LCS) | common={r['sequence']['common']} missing={r['sequence']['missing']} extra={r['sequence']['extra']} |",
              "", "```diff", *r["sequence"]["diff"], "```"]
    if r["refusals"]:
        lines += ["", "| step | tool | invariant | reason |", "|---|---|---|---|"]
        lines += [f"| {x['step']} | {x['tool']} | {x['invariant']} | {x['reason']} |" for x in r["refusals"]]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python3 -m ablation.score", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("journal")
    p.add_argument("case")
    p.add_argument("--repo", help="the fixture repo, to read the committed file list from git")
    p.add_argument("--json", action="store_true", help="print JSON instead of the markdown table")
    a = p.parse_args(argv)
    r = score(a.journal, a.case, a.repo)
    print(json.dumps(r, indent=2, sort_keys=True) if a.json else render_md(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
