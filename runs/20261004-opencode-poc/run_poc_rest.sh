#!/usr/bin/env bash
# The four POCs that failed on argument parsing, re-run with corrected flags.
#   - p1 and p6 succeeded on the first pass and are not repeated.
#   - `--file=<path>`: the bare `-f <path>` form consumed the prompt positional, because -f is a yargs array.
#   - p5's prompt path is relative to THIS script, not to the workdir the call runs in.
set -u
cd "$(dirname "$0")"
M=minimax-coding-plan/MiniMax-M3.1-Flash-Preview

run() {
  local name=$1 tmo=$2 wd=$3; shift 3
  local s e rc
  s=$(date +%s)
  ( cd "$wd" && timeout "$tmo" "$@" ) > "${name}_out.txt" 2> "${name}_err.txt"
  rc=$?; e=$(date +%s)
  printf '  %-4s rc=%-3s %4ss  %6s bytes out\n' "$name" "$rc" "$((e - s))" "$(wc -c < "${name}_out.txt")"
}

echo "POC suite part 2, model $M, $(date -u +%Y-%m-%dT%H:%MZ)"
run p2 1200 .       opencode run -m "$M" --agent build "--file=p2_records.txt" "$(cat p2_prompt.txt)"
run p3  600 .       opencode run -m "$M" --agent build "--file=p3_chart.png"   "$(cat p3_prompt.txt)"
run p4  600 .       opencode run -m "$M" --agent build "--file=p4_numbers.mp4" "$(cat p4_prompt.txt)"
run p5  900 p5_repo opencode run -m "$M" --agent build "$(cat p5_prompt.txt)"
echo "part 2 finished $(date -u +%Y-%m-%dT%H:%MZ)"
