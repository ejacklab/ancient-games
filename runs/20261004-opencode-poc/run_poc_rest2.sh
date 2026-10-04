#!/usr/bin/env bash
# p2/p3/p4, third attempt: the message MUST come before --file. `-f` is a greedy yargs array and swallows any
# following positional, so the prompt was being read as the attachment path (verified 2026-10-04 with a one-line
# file: message-first returned the secret, file-first returned "File not found: <prompt>").
set -u
cd "$(dirname "$0")"
M=minimax-coding-plan/MiniMax-M3.1-Flash-Preview
run() {
  local name=$1 tmo=$2 wd=$3; shift 3
  local s e rc; s=$(date +%s)
  ( cd "$wd" && timeout "$tmo" "$@" ) > "${name}_out.txt" 2> "${name}_err.txt"
  rc=$?; e=$(date +%s)
  printf '  %-4s rc=%-3s %4ss  %6s bytes out\n' "$name" "$rc" "$((e - s))" "$(wc -c < "${name}_out.txt")"
}
echo "POC suite part 3, $(date -u +%Y-%m-%dT%H:%MZ)"
run p2 1800 . opencode run -m "$M" --agent build "$(cat p2_prompt.txt)" "--file=p2_records.txt"
run p3  600 . opencode run -m "$M" --agent build "$(cat p3_prompt.txt)" "--file=p3_chart.png"
run p4  600 . opencode run -m "$M" --agent build "$(cat p4_prompt.txt)" "--file=p4_numbers.mp4"
echo "part 3 finished $(date -u +%Y-%m-%dT%H:%MZ)"
