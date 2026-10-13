"""Writing speed per engine and language from speed/run.sh. Speed = output tokens / (wall time - startup time), where
startup = mean wall time of the engine's two "OK" calls. Output tokens include reasoning/thinking tokens (they are
generated too). Copy fidelity = difflib ratio of the copy to the source text, whitespace removed (1.00 = identical)."""
import json, re, difflib, pathlib
here = pathlib.Path(__file__).parent; src = here.parent / "opencode"
L = ["english", "chinese_simplified", "chinese_traditional", "spanish", "korean", "japanese"]
times = {}
for line in open(here / "times.tsv"):
    e, l, t, rc = line.rstrip("\n").split("\t"); times[(e, l)] = (float(t), int(rc))
def parse(e, l):
    raw = (here / f"{e}-{l}.out").read_text(errors="ignore")
    if e == "claude":
        d = json.loads(raw); u = d["usage"]; return d.get("result", ""), u["output_tokens"]
    if e == "agy":
        d = json.loads(raw); u = d["usage"]; return d.get("response", ""), u["output_tokens"] + u.get("thinking_tokens", 0)
    if e == "codex":
        u = [json.loads(x)["usage"] for x in raw.splitlines() if '"turn.completed"' in x][-1]
        txt = (here / f"{e}-{l}.txt").read_text(errors="ignore") if (here / f"{e}-{l}.txt").exists() else ""
        return txt, u["output_tokens"] + u.get("reasoning_output_tokens", 0)
    if e == "dsh":
        txt, out = "", 0
        for x in raw.splitlines():
            ev = json.loads(x)
            if ev.get("type") == "final": txt = ev.get("text", "")
            if ev.get("phase") == "step_end" and "usage" in ev: out += ev["usage"]["outputTokens"]
        return txt, out
    if e == "opencode":
        txt, out = [], 0
        for x in raw.splitlines():
            ev = json.loads(x)
            if ev.get("type") == "text": txt.append(ev["part"].get("text", ""))
            if ev.get("type") == "step_finish":
                t = ev["part"]["tokens"]; out += t["output"] + t.get("reasoning", 0)
        return "".join(txt), out
norm = lambda s: re.sub(r"\s+", "", s)
rows = ["engine    language             wall s  startup s  out tokens  tokens/s  copy fidelity  exit"]
for e in ["claude", "codex", "agy", "opencode", "dsh"]:
    try:
        start = (times[(e, "ok1")][0] + times[(e, "ok2")][0]) / 2
    except KeyError:
        rows.append(f"{e}: missing OK calls"); continue
    for l in L:
        if (e, l) not in times: rows.append(f"{e:9} {l:20} missing"); continue
        wall, rc = times[(e, l)]
        try:
            txt, out = parse(e, l)
        except Exception as ex:
            rows.append(f"{e:9} {l:20} {wall:6.1f}  parse error: {ex}"); continue
        fid = difflib.SequenceMatcher(None, norm(txt), norm((src / f"text_{l}.txt").read_text())).ratio()
        rate = out / (wall - start) if wall > start else float("nan")
        rows.append(f"{e:9} {l:20} {wall:6.1f}  {start:9.1f}  {out:10}  {rate:8.1f}  {fid:13.2f}  {rc}")
print("\n".join(rows)); (here / "result.txt").write_text("\n".join(rows) + "\n")
