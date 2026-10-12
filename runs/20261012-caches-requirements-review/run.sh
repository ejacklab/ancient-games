#!/usr/bin/env bash
# Run 20261012-caches-requirements-review: codex and opencode review the caches requirements, read-only, in parallel.
# A third review is a Claude subagent launched from the session (reviews/claude.md).
set -u
R=/home/smoke01/dev/ancient-games/runs/20261012-caches-requirements-review
export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$HOME/.opencode/bin:$PATH"
cd /home/smoke01/dev/ancient-games
P="Read $R/briefs/review.md and do what it says."
( timeout 1500 codex exec -m gpt-6.1-sol -c model_reasoning_effort=high --sandbox read-only "$P" \
    > "$R/reviews/codex.md" 2> "$R/reviews/codex.stderr.txt"; echo "exit=$?" > "$R/reviews/codex.status" ) &
( timeout 1500 opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent plan "$P" \
    > "$R/reviews/opencode.md" 2> "$R/reviews/opencode.stderr.txt"; echo "exit=$?" > "$R/reviews/opencode.status" ) &
wait
echo "codex $(cat $R/reviews/codex.status) $(wc -c < $R/reviews/codex.md)B; opencode $(cat $R/reviews/opencode.status) $(wc -c < $R/reviews/opencode.md)B"
