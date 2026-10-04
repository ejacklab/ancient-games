#!/usr/bin/env bash
# Four independent reviews of workflow-design step 1, one per engine, run blind to each other.
# Read-only everywhere: codex -s read-only, claude --permission-mode plan, agy --mode plan, opencode --agent plan.
# Model ids and flags are the verified ones from docs/EXECUTOR_KINDS.md.
set -u
cd "$(dirname "$0")"
ROOT=/home/smoke01/dev/ancient-games
P="$(cat brief.txt)"

one() {                       # one <engine> <timeout> <cmd...>
  local name=$1 tmo=$2; shift 2
  local s e rc
  s=$(date +%s)
  timeout "$tmo" "$@" > "${name}.out" 2> "${name}.err"
  rc=$?; e=$(date +%s)
  printf '  %-9s rc=%-3s %4ss  %6s bytes\n' "$name" "$rc" "$((e - s))" "$(wc -c < "${name}.out")"
}

echo "step 1 review, four engines, $(date -u +%Y-%m-%dT%H:%MZ)"
one codex    1200 codex exec -m gpt-6.1-sol -s read-only -C "$ROOT" -o codex.md "$P"
one claude   1200 claude -p "$P" --model claude-opus-5-5 --output-format text --permission-mode plan
one agy      1200 agy -p "$P" --mode plan --model gemini-3.8-flash-high --output-format text
one opencode 1200 opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent plan "$P"
echo "done $(date -u +%Y-%m-%dT%H:%MZ)"
