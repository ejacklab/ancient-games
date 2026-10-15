#!/usr/bin/env bash
# One long-session run. Usage: run.sh A|B|C N  — writes runs/<arm><n>/.
set -u
ARM=$1; N=$2
HERE=$(cd "$(dirname "$0")" && pwd)
GUARD=/home/smoke01/dev/ancient-games/.claude/skills/workflow-design/guard
OUT="$HERE/runs/$ARM$N"; rm -rf "$OUT"; mkdir -p "$OUT"
SB=$(mktemp -d /tmp/hg-long-XXXX)
cp -r "$HERE/template/." "$SB/"; mkdir -p "$SB/out"
if [ "$ARM" = C ]; then rm "$SB/RULES.md"; else sed -i "s#\$GUARD#$GUARD#g" "$SB/RULES.md"; fi
( cd "$SB" && git init -q . && printf '.harness-guard/\n__pycache__/\n' > .gitignore && git add -A && git -c user.email=t@local -c user.name=t commit -qm sandbox )
SETTINGS=()
if [ "$ARM" != A ]; then
  python3 - "$GUARD" "$SB/settings.json" <<'PY'
import json, sys
g, out = sys.argv[1], sys.argv[2]
h = {"type": "command", "command": f"bun {g}/src/cli.ts hook claude", "timeout": 15}
json.dump({"hooks": {
  "PreToolUse": [{"matcher": "Bash", "hooks": [h]}],
  "PostToolUse": [{"matcher": "Bash|Write|Edit|MultiEdit", "hooks": [h]}],
  "PostToolUseFailure": [{"matcher": "Bash", "hooks": [h]}],
  "Stop": [{"hooks": [h]}], "SubagentStop": [{"hooks": [h]}], "SessionStart": [{"hooks": [h]}]}}, open(out, "w"), indent=1)
PY
  cp "$SB/settings.json" "$OUT/settings-used.json"; SETTINGS=(--settings "$SB/settings.json")
fi
if [ "$ARM" = C ]; then PROMPT="Do the work in TASKS.md."; else PROMPT="Read RULES.md once now; it applies to the whole session. Then do the work in TASKS.md."; fi
cd "$SB" || exit 2
START=$(date +%s)
PATH="$SB/bin:$PATH" timeout 1500 env -u ANTHROPIC_API_KEY claude -p "$PROMPT" --model claude-haiku-5-5 \
  --setting-sources project "${SETTINGS[@]}" --allowedTools "Bash" "Read" "Write" "Edit" </dev/null > "$OUT/final.txt" 2> "$OUT/stderr.txt"
RC=$?
echo "{\"arm\":\"$ARM\",\"n\":$N,\"exit\":$RC,\"seconds\":$(( $(date +%s) - START )),\"sandbox\":\"$SB\"}" > "$OUT/run.json"
echo "LONG $ARM$N exit=$RC sandbox=$SB"
