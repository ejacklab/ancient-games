#!/usr/bin/env python3
"""journal.py JOURNAL — one line per workflow journal entry: type, label, and the start of its result."""
import json
import sys

for line in open(sys.argv[1], encoding="utf-8"):
    d = json.loads(line)
    label = d.get("label") or d.get("agentLabel") or d.get("opts", {}).get("label", "") if isinstance(d.get("opts"), dict) else d.get("label", "")
    print(d.get("type"), "|", str(label)[:22], "|", json.dumps(d.get("result", d))[:220])
