#!/usr/bin/env bash
# The full algorithm, one pass, four engines, identical inlined evidence (brief-overall.txt).
# No engine needs a tool: the whole algorithm is in the prompt, which is also what lets agy take part at all.
set -u
cd "$(dirname "$0")"
P="$(cat brief-overall.txt)"

one() {                       # one <engine> <timeout> <cmd...>
  local name=$1 tmo=$2; shift 2
  local s e rc
  s=$(date +%s)
  timeout "$tmo" "$@" > "${name}.out" 2> "${name}.err"
  rc=$?; e=$(date +%s)
  printf '  %-9s rc=%-3s %4ss  %6s bytes\n' "$name" "$rc" "$((e - s))" "$(wc -c < "${name}.out")"
}

echo "overall algorithm review, four engines, $(date -u +%Y-%m-%dT%H:%MZ)  brief=$(wc -c < brief-overall.txt) bytes"
one agy      1800 agy -p "$P" --mode plan --model gemini-3.8-flash-high --output-format text
one claude   1800 claude -p "$P" --model claude-opus-5-5 --output-format text --permission-mode plan
one codex    1800 codex exec -m gpt-6.1-sol -s read-only -C /home/smoke01/dev/ancient-games -o codex.md "$P"
one opencode 1800 opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent plan "$P"
echo "done $(date -u +%Y-%m-%dT%H:%MZ)"
