#!/usr/bin/env bash
# Node 1a: question set, codex read-only. Exact command line kept as evidence.
set -u
R=/home/smoke01/dev/ancient-games/runs/20261012-caches-routing
export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$PATH"
cd /home/smoke01/dev/ancient-games
timeout 2400 codex exec -m gpt-6.1-sol -c model_reasoning_effort=high --sandbox read-only "$(cat "$R/brief-1a-queries.md")" \
  > "$R/nodes/queries.codex.stdout.md" 2> "$R/nodes/queries.codex.stderr.txt"
echo "exit=$?" > "$R/nodes/queries.codex.status"
