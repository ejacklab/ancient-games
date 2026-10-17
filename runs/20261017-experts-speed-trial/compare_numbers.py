"""Old round 3 against the --card --vote rerun: seconds, answer bytes, Codex tokens, tool steps, verdict per expert."""
import json
import pathlib
import re

RUNS = {"old (2026-10-13)": pathlib.Path("runs/20261013-four-experts-round-3-approve-the-final"),
        "new --card --vote": pathlib.Path("runs/20261017-experts-speed-trial/round3-rerun")}


def steps(sid, log):
    t = log.read_text(errors="ignore") if log.exists() else ""
    if sid == "linus":
        return f"{len(re.findall(r'^exec$', t, re.M))} shell cmds"
    if sid == "lao-tzu":
        return f"{len(re.findall(r'(→|\$) ', t))} tool calls"
    if sid == "sun-tzu":
        return f"{t.count('dsh: reasoning')} reasoning blocks"
    return "-"


for label, d in RUNS.items():
    s = json.loads((d / "status.json").read_text())
    print(f"\n{label}")
    secs = []
    for sid in ["linus", "fan-li", "sun-tzu", "lao-tzu"]:
        v = s[sid]
        txt = (d / "answers" / f"{sid}.md").read_text(errors="ignore")
        log = d / "logs" / f"{sid}.log"
        verdict = re.search(r"^## Answer\s*\n+(.+)", txt, re.M).group(1)[:60]
        tok = re.search(r"tokens used\s*\n([\d,]+)", log.read_text(errors="ignore")) if sid == "linus" else None
        secs.append(v["seconds"])
        print(f"  {sid:8} {v['engine']:9} {v['seconds']:6}s answer={len(txt.encode()):6}B "
              f"{('codex tokens=' + tok.group(1)) if tok else '':22} {steps(sid, log):22} | {verdict}")
    print(f"  slowest engine (the round's wait): {max(secs)}s; sum of engine seconds: {round(sum(secs), 1)}s")
