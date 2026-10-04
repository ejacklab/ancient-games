#!/usr/bin/env bash
# Four engines review the TEST LOG (66 KB brief: the log, TASK_TYPES.md, design_gate.py, six passing designs).
# Under the 128 KB argv limit, so no stdin dance is needed.
set -u
cd "$(dirname "$0")"
P="$(cat brief-testlog.txt)"
one() { local n=$1 t=$2; shift 2; local s e rc; s=$(date +%s)
  timeout "$t" "$@" > "${n}.out" 2> "${n}.err"; rc=$?; e=$(date +%s)
  printf '  %-9s rc=%-3s %4ss %7s bytes\n' "$n" "$rc" "$((e-s))" "$(wc -c < "${n}.out")"; }
echo "test-log review, $(date -u +%Y-%m-%dT%H:%MZ)  brief=$(wc -c < brief-testlog.txt) bytes"
one agy      1800 agy -p "$P" --mode plan --model gemini-3.8-flash-high --output-format text
one claude   1800 claude -p "$P" --model claude-opus-5-5 --output-format text --permission-mode plan
one codex    1800 codex exec -m gpt-6.1-sol -s read-only -C /home/smoke01/dev/ancient-games -o codex.out "$P"
one opencode 1800 opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent plan "$P"
echo "done $(date -u +%Y-%m-%dT%H:%MZ)"
