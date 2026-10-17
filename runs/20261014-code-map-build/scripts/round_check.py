#!/usr/bin/env python3
"""P3 round check, run by the COO after each build attempt.

usage: round_check.py freeze                      # record the snapshot of code_map/ outside src/
       round_check.py check <req> <attempt> [--holdout <cases.json>]...   # needs $CM_PRIVATE
           [--met <req,...>]                      # requirements MET in earlier rounds

Writes runs/20261014-code-map-build/p3/<req>-a<attempt>/ and prints one verdict line.
"""
import hashlib, json, os, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CM = REPO / "code_map"
RUN = REPO / "runs/20261014-code-map-build"
SNAP = RUN / "p3/snapshot.json"


def snapshot():
    out = {}
    for p in sorted(CM.rglob("*")):
        rel = p.relative_to(CM).as_posix()
        if rel.startswith(("src/", "node_modules/")) or not p.is_file():
            continue
        out[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def run(cmd, log):
    r = subprocess.run(cmd, cwd=CM, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=1800)
    log.write_text(f"$ {' '.join(cmd)}\nexit={r.returncode}\n{r.stdout}\n{r.stderr}")
    return r.returncode


def statuses(report):
    data = json.loads(report.read_text())
    return {x["requirement"]: x["status"] for x in data["requirements"]}


def main():
    if sys.argv[1] == "freeze":
        SNAP.parent.mkdir(parents=True, exist_ok=True)
        SNAP.write_text(json.dumps(snapshot(), indent=1))
        print(f"frozen {len(json.loads(SNAP.read_text()))} files")
        return
    req, attempt = sys.argv[2], sys.argv[3]
    args = sys.argv[4:]
    holdouts = [args[i + 1] for i, a in enumerate(args) if a == "--holdout"]
    met = args[args.index("--met") + 1].split(",") if "--met" in args else []
    reqs = req.split(",")  # several requirements in one run: each must be MET (time-boxed run, 2026-10-17)
    req = req.replace(",", "+")
    out = RUN / f"p3/{req}-a{attempt}"
    out.mkdir(parents=True, exist_ok=True)
    problems = []

    before, now = json.loads(SNAP.read_text()), snapshot()
    changed = sorted(k for k in set(before) | set(now) if before.get(k) != now.get(k))
    if changed:
        problems.append(f"files outside src/ changed: {', '.join(changed)}")
    if run(["bun", "test"], out / "bun-test.txt"):
        problems.append("bun test failed")
    if run(["bunx", "tsgo", "--noEmit"], out / "tsgo.txt"):
        problems.append("tsgo failed")
    run(["bun", "eval/run.ts", "--tool", "bun src/cli.ts", "--cases", "eval/cases/fixtures.json",
         "--out", str(out / "eval")], out / "eval.txt")
    st = statuses(out / "eval/report.json")
    for rq in reqs:
        if not st.get(rq, "").startswith("MET"):
            problems.append(f"{rq} is {st.get(rq)} on the fixtures")
    for r in met:
        if not st.get(r, "").startswith("MET"):
            problems.append(f"regression: {r} is {st.get(r)}")
    for n, holdout in enumerate(holdouts):
        # The held-out report names expected values; it is written to $CM_PRIVATE, outside the repo.
        priv = Path(os.environ["CM_PRIVATE"]) / f"holdout-runs/{req}-a{attempt}-{n}"
        priv.mkdir(parents=True, exist_ok=True)
        run(["bun", "eval/run.ts", "--tool", f"bun {CM}/src/cli.ts", "--cases", holdout,
             "--out", str(priv)], priv / "run.txt")
        hs = statuses(priv / "report.json")
        for rq in reqs:
            if hs.get(rq) == "NOT MET":
                problems.append(f"{rq} is {hs.get(rq)} on held-out set {n}")
    verdict = "PASS" if not problems else "FAIL"
    (out / "verdict.json").write_text(json.dumps({"req": req, "attempt": attempt, "verdict": verdict,
                                                  "problems": problems, "fixtures": st}, indent=1))
    print(verdict, req, f"a{attempt}", "; ".join(problems))


if __name__ == "__main__":
    main()
