#!/usr/bin/env python3
"""Map the three opencode modules with one copy of the tool; count link resolutions and look up the links P4's
judges found wrong. usage: map_probe.py <src dir of a tool copy> <label>   (writes builds/probe-<label>-*.json)"""
import json, subprocess, sys, time
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
src, label = Path(sys.argv[1]).resolve(), sys.argv[2]
O = (RUN / "../20261014-opencode-code-map/src/opencode/packages").resolve()
MODULES = {"session": ("core", ["src/session"], []),
           "tool": ("core", ["src/tool", "src/permission.ts"], ["--siblings", "src/tool/plugin/*.ts"]),
           "ai": ("ai", ["src"], ["--siblings", "src/protocols/*-chat.ts"])}
# (module, file, line, what the judges found): the map should resolve these to an implementation in the repository
WATCH = [("session", "src/session/runner/llm.ts", 248, "steps.attempt, labelled outside the repository"),
         ("session", "src/session/runner/step.ts", 280, "new StepFailedError, labelled outside the repository"),
         ("tool", "src/permission.ts", 233, "new DeclinedError, labelled outside the repository"),
         ("ai", "src/providers/anthropic.ts", 36, "Auth.header overload, no implementation found"),
         ("ai", "src/route/client.ts", 414, "transport.prepare, one implementation of several")]
out = {"label": label}
for name, (pkg, paths, extra) in MODULES.items():
    t = time.time()
    r = subprocess.run(["bun", str(src / "cli.ts"), "map", *paths, *extra, "--project", f"{O}/{pkg}/tsconfig.json",
                        "--root", f"{O}/{pkg}", "--tests", "test/**", "--json"], capture_output=True, text=True,
                       stdin=subprocess.DEVNULL, timeout=900)
    (RUN / f"builds/probe-{label}-{name}.json").write_text(r.stdout)
    d = json.loads(r.stdout)
    links = d["map"]["links"]
    res = {}
    for l in links:
        k = l.get("resolution", "?")
        if k == "unresolved":
            k = "unresolved-outside" if "outside the repository" in str(l.get("reason", "")) else "unresolved-other"
        res[k] = res.get(k, 0) + 1
    sib = d["map"].get("siblings")
    out[name] = {"secs": round(time.time() - t), "exit": r.returncode, "definitions": len(d["map"]["definitions"]),
                 "links": len(links), "entries": len(d["map"]["entries"]),
                 "sibling_rows": len(sib["rows"]) if sib else None,
                 "limits": len(d.get("limits", [])),
                 "resolution": dict(sorted(res.items(), key=lambda kv: -kv[1])[:6])}
    for mod, f, line, what in WATCH:
        if mod != name:
            continue
        hits = [l for l in links if (l.get("site") or {}).get("file") == f and (l.get("site") or {}).get("line") == line]
        out[name][f"{f}:{line}"] = [{"resolution": h.get("resolution"), "to": h.get("to"),
                                     "reason": str(h.get("reason", ""))[:80],
                                     "candidates": len(h.get("candidates") or [])} for h in hits][:3]
print(json.dumps(out, indent=1))
