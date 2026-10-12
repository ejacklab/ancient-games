#!/usr/bin/env bash
set -u
R=/home/smoke01/dev/ancient-games/runs/20261012-caches-numbers
export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$PATH"
cd /home/smoke01/dev/ancient-games
( timeout 1800 dsh --profile headless - < $R/verify/review-prompt.md > $R/verify/review.dsh.md 2> $R/verify/review.dsh.stderr.txt; echo "exit=$?" > $R/verify/review.dsh.status ) &
( timeout 1800 agy -p "$(cat $R/verify/review-prompt.md)" --mode plan --model gemini-3.1-pro-high --output-format text > $R/verify/review.agy.md 2> $R/verify/review.agy.stderr.txt; echo "exit=$?" > $R/verify/review.agy.status ) &
wait
for e in dsh agy; do echo "- $(date -u +%FT%TZ) review $e $(cat $R/verify/review.$e.status) $(wc -c < $R/verify/review.$e.md)B" >> $R/state.md; done
