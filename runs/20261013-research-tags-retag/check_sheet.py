#!/usr/bin/env python3
"""check_sheet.py — R4/R5's schema check (written by the COO, Claude). Usage: check_sheet.py control|new SHEET [--key K]
control: every line {"id","tag"}; new: a line may also be {"id","split":[{"part","tag"},..>=2]} or
{"id","stuck":[t1,t2],"why"} with t1 != t2. Tags from verified/reported/unproven/unknown; every key id exactly once."""
import json, sys
from pathlib import Path
TAGS = {"verified", "reported", "unproven", "unknown"}
mode, sheet = sys.argv[1], sys.argv[2]
key = json.load(open(sys.argv[sys.argv.index("--key") + 1] if "--key" in sys.argv else Path(__file__).parent / "key/old-labels.json"))
bad, seen = [], {}
for n, line in enumerate(Path(sheet).read_text().splitlines(), 1):
    if not line.strip(): continue
    try: r = json.loads(line)
    except json.JSONDecodeError: bad.append(f"line {n}: not JSON: {line[:60]}"); continue
    if not isinstance(r, dict): bad.append(f"line {n}: not a JSON object: {line[:60]}"); continue
    rid = r.get("id")
    if rid not in key: bad.append(f"line {n}: id {rid!r} not a row id"); continue
    if rid in seen: bad.append(f"line {n}: {rid} appears twice")
    seen[rid] = 1
    keys = set(r)
    if keys == {"id", "tag"}:
        if r["tag"] not in TAGS: bad.append(f"{rid}: tag {r['tag']!r} not one of the four")
    elif mode == "new" and keys == {"id", "split"}:
        parts = r["split"]
        if not isinstance(parts, list) or len(parts) < 2: bad.append(f"{rid}: a split needs at least 2 parts")
        else:
            texts = [str(p.get("part", "")).strip().lower() if isinstance(p, dict) else "" for p in parts]
            if any(not isinstance(p, dict) or set(p) != {"part", "tag"} or not x or p.get("tag") not in TAGS for p, x in zip(parts, texts)):
                bad.append(f"{rid}: each split part needs exactly a non-empty part and one of the four tags")
            elif len(set(texts)) != len(texts): bad.append(f"{rid}: split parts must have different text")
    elif mode == "new" and keys == {"id", "stuck", "why"}:
        s = r["stuck"]
        if not (isinstance(s, list) and len(s) == 2 and s[0] != s[1] and set(s) <= TAGS): bad.append(f"{rid}: stuck must name two different tags")
        if not str(r.get("why", "")).strip(): bad.append(f"{rid}: stuck needs a why")
    else: bad.append(f"{rid}: line shape not allowed in {mode} mode (keys {sorted(keys)})")
missing = sorted(set(key) - set(seen))
if missing: bad.append(f"{len(missing)} ids missing: {missing[:10]}")
print("\n".join(bad) if bad else f"{mode} sheet check: PASS — {len(seen)} ids, each once, shapes valid")
sys.exit(1 if bad else 0)
