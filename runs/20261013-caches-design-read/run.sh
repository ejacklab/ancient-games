#!/usr/bin/env bash
# Run 20261013-caches-design-read: three rounds of four readers on the memory caches design.
# Usage: bash run.sh r1|r2|r3. This script runs codex, opencode and agy for one round, in parallel;
# claude runs as a Claude Code subagent from the COO session and writes reviews/<round>-claude.md.
set -u
R=/home/smoke01/dev/ancient-games/runs/20261013-caches-design-read
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
r=${1:?round r1|r2|r3}
case $r in r1) b=r1-read.md;; r2) b=r2-discuss.md;; r3) b=r3-final.md;; *) echo "bad round"; exit 2;; esac
for e in codex opencode agy; do
  p="Read $R/briefs/$b and do what it says. Your reader name: $e. Print the whole report as your final answer; the launcher saves it to $R/reviews/$r-$e.md."
  [ $e = agy ] && p+=' Shell commands are not available to you here, and you need no web access: every file you need is local. Use your file-reading tools only.'
  run_engine $e "$R/reviews/$r-$e" "$p" &
done; wait
log "$r done: $(for e in codex opencode agy; do printf '%s %s %sB; ' $e "$(cat $R/reviews/$r-$e.status)" "$(wc -c < $R/reviews/$r-$e.md)"; done)"
