#!/usr/bin/env bash
# Read-only canary: prove each engine can read a file in this repo headlessly, before the real review.
set -u
cd "$(dirname "$0")"
ROOT=/home/smoke01/dev/ancient-games
P="$(cat canary-brief.txt)"
one() { local name=$1 tmo=$2; shift 2; local s e; s=$(date +%s)
  timeout "$tmo" "$@" > "canary-${name}.out" 2> "canary-${name}.err"; local rc=$?; e=$(date +%s)
  printf '  %-9s rc=%-3s %4ss out=%s err=%s\n' "$name" "$rc" "$((e-s))" "$(wc -c < canary-${name}.out)" "$(wc -c < canary-${name}.err)"; }
one codex    300 codex exec -m gpt-6.1-sol -s read-only -C "$ROOT" -o "canary-codex.md" "$P"
one claude   300 claude -p "$P" --model claude-opus-5-5 --output-format text --permission-mode plan
one agy      300 agy -p "$P" --mode plan --model gemini-3.8-flash-medium --output-format text
one opencode 300 opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent plan "$P"
