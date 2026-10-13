#!/usr/bin/env bash
# Run 20261012-sot-w53-rd53-read: one blind round of four readers on W5.3 and Rd5.3 of SOURCE_OF_TRUTH.md.
# claude runs as a Claude Code subagent from the COO session; this script runs codex, opencode and agy.
set -u
R=/home/smoke01/dev/ancient-games/runs/20261012-sot-w53-rd53-read
export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$HOME/.opencode/bin:$PATH"
cd /home/smoke01/dev/ancient-games
log() { echo "- $(date -u +%FT%TZ) $*" >> "$R/state.md"; }
run_engine() {  # $1 engine, $2 output file without extension, $3 prompt
  local e=$1 out=$2 p=$3
  case $e in
    agy)      timeout 1500 agy -p "$p" --mode plan --model gemini-3.1-pro-high --output-format text > "$out.md" 2> "$out.stderr.txt" ;;
    codex)    timeout 1500 codex exec -m gpt-6.1-sol -c model_reasoning_effort=high --sandbox read-only "$p" > "$out.md" 2> "$out.stderr.txt" ;;
    opencode) timeout 1500 opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent plan "$p" > "$out.md" 2> "$out.stderr.txt" ;;
  esac
  echo "exit=$?" > "$out.status"
}
for e in codex opencode agy; do
  p="Read $R/briefs/review.md and do what it says. Your engine name: $e. Print the whole report as your final answer; the launcher saves it to $R/reviews/$e.md."
  [ $e = agy ] && p+=' Shell commands are not available to you here, and you need no web access: every file you need is local. Use your file-reading tools only.'
  run_engine $e "$R/reviews/$e" "$p" &
done; wait
log "ROUND 1 done: $(for e in codex opencode agy; do printf '%s %s %sB; ' $e "$(cat $R/reviews/$e.status)" "$(wc -c < $R/reviews/$e.md)"; done)"
