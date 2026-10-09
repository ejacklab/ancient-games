#!/usr/bin/env python3
"""feature_gate.py — the script gate of the build-a-feature pipeline (docs/TASK_TYPES.md, step 4). Stdlib only,
no model calls. It does the mechanical part of review so that nobody spends judgment on it.

  baseline  record the per-test baseline before anything builds, from one or more JUnit XML reports of the full
            suite (pytest --junitxml=FILE). A test whose outcome differs between reports is marked flaky.
              feature_gate.py baseline --junit run1.xml --junit run2.xml --out runs/<id>/baseline.json
  check     after the dev's change:
              feature_gate.py check --plan runs/<id>/plan.json --base-ref <commit> \\
                                    --baseline runs/<id>/baseline.json --junit current.xml [--root .] [--json]

The plan (written by the COO with the design) names globs, matched against repo-relative paths:
  {"may_change": ["src/feature/*", "tests/unit/*"], "must_not_change": ["src/billing/*"],
   "protected": ["tests/acceptance/*", "tests/goldens/*"], "reasons": {"pyproject.toml": "new dependency"}}

Checks (all must pass):
  tests      every test that is new since the baseline passes (the dev's unit tests); tests that failed or were
             flaky in the baseline are listed, not judged — the gate does not block on old failures
  baseline   every test that passed in the baseline is present now and passes (flaky tests are listed, not judged);
             a missing test fails — deleting a test is not a way through
  scope      every changed or new file matches may_change or has a listed reason
  must-not   no changed file matches must_not_change
  tamper     no changed file matches protected (the verifier's cases, goldens)
Changed files = `git diff --name-only <base-ref>` plus untracked files, so staged, unstaged and new files all count.
Exit: 0 pass, 1 a check failed, 2 usage or input error.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def junit_outcomes(path: Path) -> dict[str, str]:
    """{test id: pass|fail|skip} from a JUnit XML report."""
    root = ET.parse(path).getroot()
    out = {}
    for tc in root.iter("testcase"):
        tid = f"{tc.get('classname', '')}::{tc.get('name', '')}"
        if tc.find("failure") is not None or tc.find("error") is not None:
            out[tid] = "fail"
        elif tc.find("skipped") is not None:
            out[tid] = "skip"
        else:
            out[tid] = "pass"
    if not out:
        raise ValueError(f"{path}: no testcase elements")
    return out


def cmd_baseline(a) -> int:
    runs = [junit_outcomes(Path(p)) for p in a.junit]
    ids = set().union(*runs)
    base = {}
    for tid in sorted(ids):
        seen = {r.get(tid, "missing") for r in runs}
        base[tid] = seen.pop() if len(seen) == 1 else "flaky"
    Path(a.out).write_text(json.dumps(base, indent=1, sort_keys=True) + "\n")
    counts = {k: sum(1 for v in base.values() if v == k) for k in ("pass", "fail", "skip", "flaky", "missing")}
    print(f"baseline: {len(base)} tests from {len(runs)} run(s): " + ", ".join(f"{k} {v}" for k, v in counts.items() if v))
    return 0


def changed_files(root: Path, base_ref: str) -> list[str]:
    def git(*args):
        p = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
        if p.returncode != 0:
            raise ValueError(f"git {' '.join(args)}: {p.stderr.strip()}")
        return [l for l in p.stdout.splitlines() if l.strip()]
    return sorted(set(git("diff", "--name-only", base_ref)) | set(git("ls-files", "--others", "--exclude-standard")))


def matches(path: str, globs: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, g) for g in globs)


def cmd_check(a) -> int:
    plan = json.loads(Path(a.plan).read_text())
    base = json.loads(Path(a.baseline).read_text())
    now = junit_outcomes(Path(a.junit))
    changed = changed_files(Path(a.root), a.base_ref)
    reasons = plan.get("reasons") or {}
    results = {
        "tests": [f"{t} {o}" for t, o in sorted(now.items()) if t not in base and o == "fail"],
        "baseline": [f"{t} {'missing' if t not in now else now[t]}" for t, o in sorted(base.items())
                     if o == "pass" and now.get(t) != "pass"],
        "must-not": [f for f in changed if matches(f, plan.get("must_not_change") or [])],
        "tamper": [f for f in changed if matches(f, plan.get("protected") or [])],
    }
    named = set(results["must-not"]) | set(results["tamper"])      # one reason per file
    results["scope"] = [f for f in changed if f not in named and f not in reasons
                        and not matches(f, plan.get("may_change") or [])]
    results = {k: results[k] for k in ("tests", "baseline", "scope", "must-not", "tamper")}
    flaky = sorted(t for t, o in base.items() if o == "flaky")
    old_fail = sorted(t for t, o in base.items() if o == "fail")
    ok = not any(results.values())
    if a.json:
        print(json.dumps({"pass": ok, "checks": results, "flaky": flaky, "failing_before": old_fail,
                          "changed": changed}, indent=1))
    else:
        for name, bad in results.items():
            print(f"{'ok  ' if not bad else 'FAIL'} {name}" + ("" if not bad else f": {len(bad)}"))
            for b in bad[:20]:
                print(f"       {b}")
            if len(bad) > 20:
                print(f"       … {len(bad) - 20} more")
        print(f"gate {'PASS' if ok else 'FAIL'}: {len(now)} tests now, {len(base)} in baseline"
              f" ({len(flaky)} flaky and {len(old_fail)} failing before: not judged), {len(changed)} changed file(s)")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("baseline")
    b.add_argument("--junit", action="append", required=True); b.add_argument("--out", required=True)
    c = sub.add_parser("check")
    c.add_argument("--plan", required=True); c.add_argument("--base-ref", required=True)
    c.add_argument("--baseline", required=True); c.add_argument("--junit", required=True)
    c.add_argument("--root", default="."); c.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        return cmd_baseline(a) if a.cmd == "baseline" else cmd_check(a)
    except (OSError, ValueError, ET.ParseError) as e:
        print(f"feature_gate: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
