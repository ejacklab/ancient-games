#!/usr/bin/env bash
# Writing-speed test: each engine copies UDHR Articles 1-25 back, once per language (n=1), plus two "OK" calls for
# the fixed startup time. Wall time per call goes to speed/times.tsv. Run from token-test/: bash speed/run.sh
set -u
L="english chinese_simplified chinese_traditional spanish korean japanese"
OK="Reply with only the word OK. Do not use any tools."
COPY="Copy the text below back exactly, character for character, with no other words before or after it. Do not use any tools."
call() { # engine label prompt
  local e=$1 l=$2 p=$3 t0 t1
  t0=$(date +%s.%N)
  case $e in
    claude)   timeout 900 env -u ANTHROPIC_API_KEY claude -p --model claude-opus-5-5 --output-format json "$p" </dev/null >speed/$e-$l.out 2>speed/$e-$l.err ;;
    codex)    timeout 900 codex -m gpt-6.1-sol exec -s read-only --skip-git-repo-check --json -o speed/$e-$l.txt "$p" </dev/null >speed/$e-$l.out 2>speed/$e-$l.err ;;
    agy)      timeout 900 agy -p "$p" --mode plan --model gemini-3.8-flash-medium --print-timeout 800s --output-format json </dev/null >speed/$e-$l.out 2>speed/$e-$l.err ;;
    dsh)      timeout 900 dsh headless --json "$p" </dev/null >speed/$e-$l.out 2>speed/$e-$l.err ;;
    opencode) timeout 900 opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent plan --format json "$p" </dev/null >speed/$e-$l.out 2>speed/$e-$l.err ;;
  esac
  local rc=$?; t1=$(date +%s.%N)
  printf '%s\t%s\t%s\t%s\n' "$e" "$l" "$(echo "$t1 - $t0" | bc)" "$rc" >> speed/times.tsv
}
engine() {
  local e=$1
  call $e ok1 "$OK"; call $e ok2 "$OK"
  for l in $L; do call $e $l "$COPY

$(cat opencode/text_$l.txt)"; done
}
if [ "${1:-}" = dsh ]; then engine dsh; exit; fi   # added later at EJ's request: bash speed/run.sh dsh
engine claude & engine codex & engine agy & (sleep 20; engine opencode) &
wait
