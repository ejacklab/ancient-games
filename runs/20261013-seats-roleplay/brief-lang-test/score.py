"""Score the brief test: six known answers, template followed, reply in English, tokens and time."""
import json, re, pathlib
here = pathlib.Path(__file__).parent
times = {tuple(l.split("\t")[:2]): float(l.split("\t")[2]) for l in open(here / "times.tsv")}
def reply_and_usage(e, c):
    raw = (here / f"{e}-{c}.out").read_text(errors="ignore")
    if e == "claude":
        d = json.loads(raw); u = d["usage"]
        return d["result"], u["input_tokens"] + u["cache_creation_input_tokens"] + u["cache_read_input_tokens"], u["output_tokens"]
    if e == "agy":
        d = json.loads(raw); u = d["usage"]; return d["response"], u["input_tokens"], u["output_tokens"] + u.get("thinking_tokens", 0)
    if e == "codex":
        u = [json.loads(x)["usage"] for x in raw.splitlines() if '"turn.completed"' in x][-1]
        return (here / f"{e}-{c}.txt").read_text(), u["input_tokens"], u["output_tokens"] + u["reasoning_output_tokens"]
    if e == "opencode":
        t, i, o = [], 0, 0
        for x in raw.splitlines():
            ev = json.loads(x)
            if ev.get("type") == "text": t.append(ev["part"]["text"])
            if ev.get("type") == "step_finish":
                k = ev["part"]["tokens"]; i += k["input"] + k["cache"]["read"]; o += k["output"] + k.get("reasoning", 0)
        return "".join(t), i, o
    if e == "dsh":
        t, i, o = "", 0, 0
        for x in raw.splitlines():
            ev = json.loads(x)
            if ev.get("type") == "final": t = ev["text"]
            if ev.get("phase") == "step_end": u = ev["usage"]; i += u["inputTokens"] + u["cacheReadTokens"]; o += u["outputTokens"]
        return t, i, o
CHECK = {1: lambda r: re.search(r"\b1\b", r), 2: lambda r: re.search(r"\b(4|four)\b", r, re.I),
         3: lambda r: re.search(r"[謀谋]攻", r), 4: lambda r: re.search(r"\b5\b", r),
         5: lambda r: re.search(r"\b(5|five)\b", r, re.I) and re.search(r"\b(7|seven)\b", r, re.I),
         6: lambda r: re.search(r"(walled )?cit(y|ies)|攻城", r, re.I)}
rows = ["engine    brief   right  template  CJK-outside-names  in tokens  out tokens  wall s"]
for e, c in [("opencode","en_md"),("opencode","en_xml"),("opencode","zh_xml"),("dsh","en_md"),("dsh","en_xml"),("dsh","zh_xml"),
             ("claude","en_md"),("claude","en_xml"),("codex","en_md"),("codex","en_xml"),("agy","en_md"),("agy","en_xml")]:
    r, i, o = reply_and_usage(e, c)
    table = {int(m.group(1)): m.group(0) for m in re.finditer(r"^\|\s*(\d)\s*\|.*$", r, re.M)}
    right = sum(1 for q, f in CHECK.items() if q in table and f(table[q].split("|", 2)[2]))
    tmpl = r.strip().startswith("---") and "node: q1" in r and len(table) == 6 and r.strip().endswith("|")
    cjk = len(re.findall(r"[㐀-鿿]", re.sub(r"[謀谋]攻第三|孫子|孙子", "", r)))
    rows.append(f"{e:9} {c:7} {right}/6    {'yes' if tmpl else 'NO':8}  {cjk:17}  {i:9}  {o:10}  {times[(e,c)]:6.1f}")
    (here / f"{e}-{c}.reply.md").write_text(r)
print("\n".join(rows)); (here / "result.txt").write_text("\n".join(rows) + "\n")
