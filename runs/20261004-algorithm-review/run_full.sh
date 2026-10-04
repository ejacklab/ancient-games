#!/usr/bin/env bash
# The FULL algorithm (3202 lines, 14 artefacts, 259 KB), four engines, one pass.
#
# Every engine gets the brief on **stdin**, because 259 KB exceeds Linux's MAX_ARG_STRLEN (128 KB) — an argv call
# fails with E2BIG before the model sees anything. Each CLI needed its own way in:
#   claude    -p reads stdin
#   codex     "Reading prompt from stdin..." (needs a trusted -C)
#   opencode  run reads stdin
#   agy       no stdin in text mode; --input-format stream-json takes one NDJSON message per line, and the message
#             needs an "event" field: {"event":"user","message":{...}} — found by probing four shapes.
set -u
cd "$(dirname "$0")"
B=brief-full.txt

run() {                        # run <name> <timeout> <cmd...>
  local name=$1 tmo=$2; shift 2
  local s e rc
  s=$(date +%s)
  timeout "$tmo" "$@" > "${name}.out" 2> "${name}.err"
  rc=$?; e=$(date +%s)
  printf '  %-9s rc=%-3s %4ss %8s bytes out\n' "$name" "$rc" "$((e - s))" "$(wc -c < "${name}.out")"
}

echo "FULL algorithm review, $(date -u +%Y-%m-%dT%H:%MZ)  brief=$(wc -c < $B) bytes $(wc -l < $B) lines"

# agy: NDJSON on stdin, then lift the answer out of its stream-json result
python3 -c "
import json
body = open('$B').read()
print(json.dumps({'event': 'user', 'message': {'role': 'user', 'content': [{'type': 'text', 'text': body}]}}))
" > agy-full.ndjson
s=$(date +%s)
timeout 2400 agy --print= --input-format stream-json --output-format stream-json \
        --mode plan --model gemini-3.8-flash-high < agy-full.ndjson > agy-full.raw 2> agy-full.err
rc=$?
python3 - <<'PY' > agy-full.out 2> agy-full.parse.err
import json
for line in open("agy-full.raw"):
    line = line.strip()
    if not line:
        continue
    try:
        d = json.loads(line)
    except ValueError:
        continue
    r = d.get("result") or {}
    if r.get("response"):
        print(r["response"])
PY
printf '  %-9s rc=%-3s %4ss %8s bytes out\n' "agy" "$rc" "$(( $(date +%s) - s ))" "$(wc -c < agy-full.out)"
grep -o '"status":"[A-Z]*"' agy-full.raw | tail -1 | sed 's/^/            agy status: /'

run claude   2400 claude -p --model claude-opus-5-5 --output-format text --permission-mode plan < "$B"
run codex    2400 codex exec -m gpt-6.1-sol -s read-only -C /home/smoke01/dev/ancient-games -o codex-full.md < "$B"
run opencode 2400 opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent plan < "$B"
echo "done $(date -u +%Y-%m-%dT%H:%MZ)"
