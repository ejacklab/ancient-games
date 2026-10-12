#!/usr/bin/env bash
set -u
R=/home/smoke01/dev/ancient-games/runs/20261012-caches-routing
export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$PATH"
cd /home/smoke01/dev/ancient-games
timeout 1500 codex exec -m gpt-6.1-sol -c model_reasoning_effort=high --sandbox read-only "$(cat "$R/brief-6-review.md")" \
  > "$R/nodes/review.codex.stdout.md" 2> "$R/nodes/review.codex.stderr.txt"
echo "exit=$?" > "$R/nodes/review.codex.status"
