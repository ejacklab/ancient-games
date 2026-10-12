#!/usr/bin/env bash
# agy produced nothing in R1/R2 of run.sh: headless mode auto-denies the shell ("command") tool. This re-runs agy with
# both versions inline and an instruction to use file-read tools only, then re-runs the dsh merge with all reviews.
# Asymmetry, recorded: codex and opencode do not get to answer agy's R2.
set -u
M=/home/smoke01/dev/ancient-games/runs/20261012-caches-merge
export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$PATH"
cd /home/smoke01/dev/ancient-games
log() { echo "- $(date -u +%FT%TZ) $*" >> "$M/state.md"; }
note=$'\n\n**Tool note for this run:** shell commands are not available to you here. Use only your file-reading tools to open sources. Both versions are also given in full below.\n'
inline=$'\n\n## Version A (full text)\n\n'"$(cat $M/inputs/version-A.md)"$'\n\n## Version B (full text)\n\n'"$(cat $M/inputs/version-B.md)"
p1="$(cat $M/briefs/r1-review.md)$note$inline"
timeout 1500 agy -p "$p1" --mode plan --model gemini-3.1-pro-high --output-format text \
  > "$M/reviews/r1-agy.md" 2> "$M/reviews/r1-agy.stderr.txt"; echo "exit=$?" > "$M/reviews/r1-agy.status"
[ -s "$M/reviews/r1-agy.md" ] || { log "AGY-FIX STOP: r1-agy still empty"; exit 1; }
p2="$(cat $M/briefs/r2-discuss.md)$note"
for o in agy codex opencode; do
  who="another reviewer"; [ "$o" = agy ] && who="YOU (your own round-1 review)"
  p2+=$'\n\n'"#### Round-1 review by $o — $who"$'\n\n'"$(cat $M/reviews/r1-$o.md)"
done
for o in codex opencode; do p2+=$'\n\n'"#### Round-2 discussion by $o (written before your review existed)"$'\n\n'"$(cat $M/reviews/r2-$o.md)"; done
timeout 1500 agy -p "$p2" --mode plan --model gemini-3.1-pro-high --output-format text \
  > "$M/reviews/r2-agy.md" 2> "$M/reviews/r2-agy.stderr.txt"; echo "exit=$?" > "$M/reviews/r2-agy.status"
log "AGY-FIX: r1-agy $(cat $M/reviews/r1-agy.status) $(wc -c < $M/reviews/r1-agy.md)B; r2-agy $(cat $M/reviews/r2-agy.status) $(wc -c < $M/reviews/r2-agy.md)B"
mkdir -p "$M/merge/first-merge-2-reviewers" && mv "$M"/merge/{CACHES.merged.md,merge-notes.md,dsh.stdout.md,dsh.stderr.txt,dsh.status,prompt.md} "$M/merge/first-merge-2-reviewers/" 2>/dev/null
bash "$M/run.sh" merge
