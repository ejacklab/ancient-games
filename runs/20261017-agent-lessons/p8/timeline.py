"""Print each P8 arm's tool calls in order: the call, any hook decision, and its result's first line.

Run from the repository root: python3 runs/20261017-agent-lessons/p8/timeline.py > runs/20261017-agent-lessons/p8/timeline.md
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
HOLD = "harness-guard lesson"


def short(value, n=150):
    text = " ".join(str(value).split())
    return text if len(text) <= n else text[: n - 1] + "…"


for arm in ("test-edit", "fact-edit", "command", "control"):
    print(f"## {arm}\n")
    holds = calls = 0
    for line in (HERE / f"{arm}.jsonl").read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        kind = event.get("type")
        if kind == "assistant":
            for block in event.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    calls += 1
                    inp = block.get("input", {})
                    target = inp.get("file_path") or inp.get("command") or ""
                    print(f"- call {block.get('name')} {short(target, 90)}")
                elif block.get("type") == "text" and block.get("text", "").strip():
                    print(f"- says: {short(block['text'])}")
        elif kind == "system" and "decision_reason" in event:
            print(f"- hook {event.get('subtype')} on {event.get('tool_name')}: {short(event.get('decision_reason'))}")
        elif kind == "user":
            for block in event.get("message", {}).get("content", []):
                if block.get("type") == "tool_result":
                    content = block.get("content")
                    if isinstance(content, list):
                        content = " ".join(part.get("text", "") for part in content if isinstance(part, dict))
                    if HOLD in str(content):
                        holds += 1
                    flag = "error" if block.get("is_error") else "ok"
                    print(f"  result ({flag}): {short(content)}")
        elif kind == "result":
            print(f"- end: is_error={event.get('is_error')} turns={event.get('num_turns')}")
    print(f"\ncalls {calls}, results carrying a lesson hold {holds}\n")
