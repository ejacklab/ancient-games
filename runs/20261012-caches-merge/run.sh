#!/usr/bin/env bash
# Driver for run 20261012-caches-merge. Stages: r1 (3 reviewers, parallel) -> r2 (3, parallel) -> merge (dsh).
# Usage: bash run.sh [r1|r2|merge|all]. Each engine call is recorded here as evidence of the exact command line.
set -u
M=/home/smoke01/dev/ancient-games/runs/20261012-caches-merge
export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$HOME/.opencode/bin:$PATH"
cd /home/smoke01/dev/ancient-games
log() { echo "- $(date -u +%FT%TZ) $*" >> "$M/state.md"; }

run_engine() {  # $1 engine, $2 round, $3 prompt
  local e=$1 r=$2 p=$3
  local out="$M/reviews/$r-$e"
  case $e in
    agy)      timeout 1500 agy -p "$p" --mode plan --model gemini-3.1-pro-high --output-format text \
                > "$out.md" 2> "$out.stderr.txt" ;;
    codex)    timeout 1500 codex exec -m gpt-6.1-sol -c model_reasoning_effort=high --sandbox read-only "$p" \
                > "$out.md" 2> "$out.stderr.txt" ;;
    opencode) timeout 1500 opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent plan "$p" \
                > "$out.md" 2> "$out.stderr.txt" ;;
  esac
  echo "exit=$?" > "$out.status"
}

r1() {
  local p; p="$(cat "$M/briefs/r1-review.md")"
  for e in agy codex opencode; do run_engine $e r1 "$p" & done; wait
  log "R1 done: $(for e in agy codex opencode; do printf '%s %s %sB; ' $e "$(cat $M/reviews/r1-$e.status)" "$(wc -c < $M/reviews/r1-$e.md)"; done)"
}

r2() {
  for e in agy codex opencode; do
    local p; p="$(cat "$M/briefs/r2-discuss.md")"
    for o in agy codex opencode; do
      local who="another reviewer"; [ "$o" = "$e" ] && who="YOU (your own round-1 review)"
      p+=$'\n\n'"#### Round-1 review by $o — $who"$'\n\n'"$(cat "$M/reviews/r1-$o.md")"
    done
    run_engine $e r2 "$p" &
  done; wait
  log "R2 done: $(for e in agy codex opencode; do printf '%s %s %sB; ' $e "$(cat $M/reviews/r2-$e.status)" "$(wc -c < $M/reviews/r2-$e.md)"; done)"
}

merge() {
  { cat "$M/briefs/m-merge.md"
    printf '\n\n## Version A\n\n'; cat "$M/inputs/version-A.md"
    printf '\n\n## Version B\n\n'; cat "$M/inputs/version-B.md"
    for r in r1 r2; do for e in agy codex opencode; do
      printf '\n\n## %s review by %s\n\n' "$r" "$e"; cat "$M/reviews/$r-$e.md"; done; done
  } > "$M/merge/prompt.md"
  timeout 1500 dsh --profile headless - < "$M/merge/prompt.md" > "$M/merge/dsh.stdout.md" 2> "$M/merge/dsh.stderr.txt"
  echo "exit=$?" > "$M/merge/dsh.status"
  python3 - "$M" <<'PY'
import re, sys
M = sys.argv[1]; t = open(f"{M}/merge/dsh.stdout.md").read()
for tag, f in (("MERGED", "CACHES.merged.md"), ("NOTES", "merge-notes.md")):
    m = re.search(rf"BEGIN_{tag}\s*\n(.*?)\n\s*END_{tag}", t, re.S)
    open(f"{M}/merge/{f}", "w").write(m.group(1).strip() + "\n" if m else "")
    print(f, "found" if m else "MISSING")
PY
  log "MERGE done: dsh $(cat $M/merge/dsh.status), prompt $(wc -c < $M/merge/prompt.md)B, stdout $(wc -c < $M/merge/dsh.stdout.md)B"
}

enough_r1() {  # design stop condition: fewer than two non-empty R1 reviews -> stop and report
  local n=0; for e in agy codex opencode; do [ -s "$M/reviews/r1-$e.md" ] && n=$((n+1)); done
  [ "$n" -ge 2 ] || { log "STOP: only $n non-empty R1 reviews"; exit 1; }
}
case "${1:-all}" in r1) r1;; r2) enough_r1; r2;; merge) merge;; all) r1; enough_r1; r2; merge;; esac
