#!/usr/bin/env bash
# E4 (prediction.md): one live run of claude-haiku-5-5 in a fresh sandbox, arm A (rules only) or B (rules + hooks).
# Usage: run_e4.sh A|B N   — writes e4/runs/<arm><n>/ with the agent's final message, the shim log, the journal and
# any insight file. No harness config is edited: hooks come only from --settings in arm B.
set -u
ARM=$1; N=$2
HERE=$(cd "$(dirname "$0")" && pwd)
GUARD=/home/smoke01/dev/ancient-games-ts-hybrid/tools/harness-guard
OUT="$HERE/runs3/$ARM$N"; rm -rf "$OUT"; mkdir -p "$OUT"
SB=$(mktemp -d /tmp/hg-e4-XXXX)
cp -r "$HERE/template2/." "$SB/"; mkdir -p "$SB/out"
sed -i "s#\$GUARD#$GUARD#g" "$SB/RULES.md"
( cd "$SB" && git init -q . && printf '.harness-guard/\n' > .gitignore && git add -A && git -c user.email=e4@local -c user.name=e4 commit -qm sandbox )
SETTINGS=()
if [ "$ARM" = B ]; then
  python3 - "$GUARD" "$SB/settings.json" <<'EOF'
import json, sys
g, out = sys.argv[1], sys.argv[2]
h = {"type": "command", "command": f"bun {g}/src/cli.ts hook claude"}
json.dump({"hooks": {
  "PreToolUse": [{"matcher": "Bash", "hooks": [h]}],
  "PostToolUse": [{"matcher": "Bash|Write|Edit|MultiEdit", "hooks": [h]}],
  "PostToolUseFailure": [{"matcher": "Bash", "hooks": [h]}],
  "Stop": [{"hooks": [h]}], "SubagentStop": [{"hooks": [h]}], "SessionStart": [{"hooks": [h]}]}}, open(out, "w"), indent=1)
EOF
  cp "$SB/settings.json" "$OUT/settings-used.json"
  SETTINGS=(--settings "$SB/settings.json")
fi
cd "$SB" || exit 2
START=$(date +%s)
PATH="$SB/bin:$PATH" timeout 900 env -u ANTHROPIC_API_KEY claude -p "Read TASK.md and do what it says." \
  --model claude-haiku-5-5 --setting-sources project "${SETTINGS[@]}" \
  --allowedTools "Bash" "Read" "Write" "Edit" </dev/null > "$OUT/final.txt" 2> "$OUT/stderr.txt"
RC=$?
echo "{\"arm\":\"$ARM\",\"n\":$N,\"exit\":$RC,\"seconds\":$(( $(date +%s) - START ))}" > "$OUT/run.json"
cp "$SB/.shim-calls.log" "$OUT/shim-calls.log" 2>/dev/null
cp "$SB/.harness-guard/journal.jsonl" "$OUT/journal.jsonl" 2>/dev/null
cp "$SB/insight.md" "$OUT/insight.md" 2>/dev/null
ls -la "$SB" > "$OUT/sandbox-ls.txt"
echo "E4 $ARM$N exit=$RC sandbox=$SB"
