#!/usr/bin/env bash
# Code-graph research node, read-only (--agent plan). Recorded so the exact command line is evidence.
set -u
R=/home/smoke01/dev/ancient-games/runs/20261012-memory-caches
export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$HOME/.opencode/bin:$PATH"
PLANT='Which languages does the `tarnline` code-graph CLI support, according to its README?'
STORE='

## Your store: the code graph

Also read `/home/smoke01/dev/ancient-games/code_graph/code_graph.py` (a stdlib Python code graph already built here)
and `/home/smoke01/dev/ancient-games/docs/KNOWLEDGE_GRAPH_DESIGN.md`. One specific question: the design (line 75 of
SOURCE_OF_TRUTH.md) has a script with no model call mark a decision or fact when its code changed with no earlier
change to the entry. Does that check need a code graph (symbol and call edges, as in s3-F4), or is git on the
`covers:` paths enough? Give evidence for both sides.

Print your whole answer to stdout as markdown. Do not write any file.'
BRIEF="$(sed "s|{{PLANT}}|$PLANT|" "$R/brief.md")$STORE"
cd /home/smoke01/dev/ancient-games
timeout 1800 opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent plan "$BRIEF" \
  > "$R/nodes/code-graph.opencode.stdout.md" 2> "$R/nodes/code-graph.opencode.stderr.txt"
echo "exit=$?" > "$R/nodes/code-graph.opencode.status"
