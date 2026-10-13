#!/bin/sh
# R2's check: count.py on the hand-written fixture must give exactly fixture/expected.json. Usage: test_count.sh [SHEET]
cd "$(dirname "$0")"
got=$(python3 count.py --key fixture/key.json "${1:-fixture/sheet.jsonl}" --names fixture --totals)
want=$(python3 -c "import json;print(json.dumps(json.load(open('fixture/expected.json'))))")
if [ "$got" = "$want" ]; then echo "R2 check: PASS — $got"; else echo "R2 check: FAIL — got $got, want $want"; exit 1; fi
