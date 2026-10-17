#!/usr/bin/env python3
"""Run the round check's measures on a build copy, for comparing two builders of one round.

usage: compare_build.py <copy of code_map> <label>      # needs $CM_PRIVATE for the held-out sets

Checks, as round_check.py does: files outside src/ unchanged against code_map/ (src/ and node_modules/ excluded),
bun test, tsgo, the evaluator on its bundled cases, and the three held-out sets (written under $CM_PRIVATE).
Prints one JSON line; held-out reports name expected values, so only statuses are printed.
"""
import hashlib, json, os, subprocess, sys, time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
copy, label = Path(sys.argv[1]).resolve(), sys.argv[2]
priv = Path(os.environ["CM_PRIVATE"])
SETS = [priv / "holdout/fixtures.json", priv / "opencode-cases/core.json", priv / "opencode-cases/ai.json"]


def files(root):
    out = {}
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root).as_posix()
        # test/a1/ was added to the copies (with the COO's fix in both); test/a3/ was added to code_map/ after they
        # were taken. Both are known differences, not the builder's.
        if rel.startswith(("src/", "node_modules/", "test/a1/", "test/a3/")) or rel == "node_modules" or not p.is_file():
            continue
        out[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def run(cmd):
    t = time.time()
    r = subprocess.run(cmd, cwd=copy, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=1800)
    return r, round(time.time() - t)


def statuses(report):
    return {x["requirement"]: x["status"] for x in json.loads(report.read_text())["requirements"]}


res = {"label": label}
base = files(REPO / "code_map")
mine = files(copy)
res["outside_src_changed"] = sorted(k for k in set(base) | set(mine) if base.get(k) != mine.get(k))
r, s = run(["bun", "test"])
tail = [l.strip() for l in (r.stdout + r.stderr).splitlines() if l.strip().endswith((" pass", " fail"))]
res["bun_test"] = {"exit": r.returncode, "counts": tail[-2:], "secs": s}
r, s = run(["bunx", "tsgo", "--noEmit"])
res["tsgo_exit"] = r.returncode
out = REPO / f"runs/20261014-code-map-build/builds/compare-{label}"
r, s = run(["bun", "eval/run.ts", "--tool", f"bun {copy}/src/cli.ts", "--cases", "eval/cases/fixtures.json",
            "--out", str(out)])
res["bundled"] = statuses(out / "report.json")
res["bundled_secs"] = s
for n, cases in enumerate(SETS):
    d = priv / f"holdout-runs/compare-{label}-{n}"
    d.mkdir(parents=True, exist_ok=True)
    run(["bun", "eval/run.ts", "--tool", f"bun {copy}/src/cli.ts", "--cases", str(cases), "--out", str(d)])
    rep = json.loads((d / "report.json").read_text())
    res[f"heldout_{n}"] = {k: v for k, v in statuses(d / "report.json").items() if v != "NOT CHECKED"}
    res[f"heldout_{n}_cases_met"] = f"{sum(c.get('status') == 'MET' for c in rep['cases'])}/{len(rep['cases'])}"
print(json.dumps(res))
