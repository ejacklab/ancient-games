#!/usr/bin/env bash
# Driver for run 20261012-index-md-algorithm. Stage 1: four blind literature reviews (parallel).
# Stage 2: each engine reads all the reviews and writes one proposal (parallel).
# claude runs as a Claude Code subagent from the COO session, not from this script; this script runs the other three.
# Usage: bash run.sh [1|2]. Each engine call is recorded here as evidence of the exact command line.
set -u
R=/home/smoke01/dev/ancient-games/runs/20261012-index-md-algorithm
export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$HOME/.opencode/bin:$PATH"
cd /home/smoke01/dev/ancient-games
log() { echo "- $(date -u +%FT%TZ) $*" >> "$R/state.md"; }
prefix() { case $1 in codex) echo X;; opencode) echo O;; agy) echo A;; esac; }

run_engine() {  # $1 engine, $2 output file without extension, $3 prompt
  local e=$1 out=$2 p=$3
  case $e in
    agy)      timeout 2400 agy -p "$p" --mode plan --model gemini-3.1-pro-high --output-format text \
                > "$out.md" 2> "$out.stderr.txt" ;;
    codex)    timeout 2400 codex exec -m gpt-6.1-sol -c model_reasoning_effort=high --sandbox read-only "$p" \
                > "$out.md" 2> "$out.stderr.txt" ;;
    opencode) timeout 2400 opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent plan "$p" \
                > "$out.md" 2> "$out.stderr.txt" ;;
  esac
  echo "exit=$?" > "$out.status"
}

agy_note=' Shell commands are not available to you here: use your file-reading and web tools only.'

stage1() {
  for e in codex opencode agy; do
    local p="Read $R/briefs/1-lit-review.md and do what it says. Your engine name: $e. Your finding-id prefix: $(prefix $e). Print the whole report as your final answer; the launcher saves it to $R/lit-review/$e.md."
    [ $e = agy ] && p+="$agy_note"
    run_engine $e "$R/lit-review/$e" "$p" &
  done; wait
  log "STAGE 1 done: $(for e in codex opencode agy; do printf '%s %s %sB; ' $e "$(cat $R/lit-review/$e.status)" "$(wc -c < $R/lit-review/$e.md)"; done)"
}

stage2() {
  for e in codex opencode; do
    local p="Read $R/briefs/2-proposal.md and do what it says. Your engine name: $e. Your own stage-1 review is $R/lit-review/$e.md. Print the whole report as your final answer; the launcher saves it to $R/proposals/$e.md."
    [ $e = agy ] && p+="$agy_note"
    run_engine $e "$R/proposals/$e" "$p" &
  done; wait
  log "STAGE 2 done: $(for e in codex opencode; do printf '%s %s %sB; ' $e "$(cat $R/proposals/$e.status)" "$(wc -c < $R/proposals/$e.md)"; done)"
}

stage3() {  # EJ, 2026-10-12: "ask codex, agy and opencode to review the claude's version algorithm"
  mkdir -p "$R/reviews"
  local agy_local=' Shell commands are not available to you here, and you need no web access: every file you need is local. Use your file-reading tools only.'
  for e in codex opencode agy; do
    local p="Read $R/briefs/3-review.md and do what it says. Your engine name: $e. Print the whole report as your final answer; the launcher saves it to $R/reviews/$e.md."
    [ $e = agy ] && p+="$agy_local"
    run_engine $e "$R/reviews/$e" "$p" &
  done; wait
  log "STAGE 3 done: $(for e in codex opencode agy; do printf '%s %s %sB; ' $e "$(cat $R/reviews/$e.status)" "$(wc -c < $R/reviews/$e.md)"; done)"
}

case "${1:-}" in 1) stage1;; 2) stage2;; 3) stage3;; *) echo "usage: $0 1|2|3" >&2; exit 2;; esac
