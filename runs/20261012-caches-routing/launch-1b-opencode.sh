#!/usr/bin/env bash
# Node 1b: benchmark harness, opencode build agent. Exact command line kept as evidence.
set -u
R=/home/smoke01/dev/ancient-games/runs/20261012-caches-routing
export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$HOME/.opencode/bin:$PATH"
cd /home/smoke01/dev/ancient-games
timeout 3000 opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent build "$(cat "$R/brief-1b-build.md")" \
  > "$R/nodes/build.opencode.stdout.md" 2> "$R/nodes/build.opencode.stderr.txt"
echo "exit=$?" > "$R/nodes/build.opencode.status"
