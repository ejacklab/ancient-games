"""Text tokens per language on four real engines: each engine's recorded prompt tokens for (instruction + UDHR
Articles 1-25 text) minus its baseline call (instruction only). Inputs: codex/, agy/, claude/, opencode/ call logs."""
import json, pathlib
L = ["english", "chinese_simplified", "chinese_traditional", "spanish", "korean", "japanese"]
def codex(f):
    for l in open(f):
        e = json.loads(l)
        if e.get("type") == "turn.completed": return e["usage"]["input_tokens"]
def agy(f):
    u = json.load(open(f))["usage"]; return u["input_tokens"] + u.get("cache_read_tokens", 0)
def claude(f):
    u = json.load(open(f))["usage"]
    return u["input_tokens"] + u["cache_creation_input_tokens"] + u["cache_read_input_tokens"]
def opencode(f):
    for l in open(f):
        e = json.loads(l)
        if e.get("type") == "step_finish":
            t = e["part"]["tokens"]; return t["input"] + t["cache"]["read"] + t["cache"]["write"]
def dsh(f):
    n = 0
    for l in open(f):
        e = json.loads(l)
        if e.get("phase") == "step_end" and "usage" in e:
            u = e["usage"]; n += u["inputTokens"] + u["cacheReadTokens"] + u["cacheWriteTokens"]
    return n
engines = {"Claude Opus 5.5 (claude -p)": ("claude", claude, ".json"),
           "Codex gpt-6.1-sol": ("codex", codex, ".jsonl"),
           "agy gemini-3.8-flash-medium": ("agy", agy, ".json"),
           "opencode MiniMax-M3.1-Flash-Preview": ("opencode", opencode, ".jsonl"),
           "dsh deepseek-flash (dsh headless)": ("dsh", dsh, ".jsonl")}
out = []
for name, (d, fn, ext) in engines.items():
    base = fn(f"{d}/baseline{ext}")
    n = {l: fn(f"{d}/{l}{ext}") - base for l in L}
    out.append(f"{name}  (baseline prompt {base} tokens)")
    for l in L:
        out.append(f"  {l:20} {n[l]:5}  {n[l]/n['english']:.2f}x English")
print("\n".join(out)); open("engines_result.txt", "w").write("\n".join(out) + "\n")
