#!/usr/bin/env bash
# agy, opencode and codex slices for run 20261012-caches-numbers, in parallel. Each prints to stdout only.
set -u
R=/home/smoke01/dev/ancient-games/runs/20261012-caches-numbers
export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$HOME/.opencode/bin:$PATH"
cd /home/smoke01/dev/ancient-games
C="$(cat $R/briefs/common.md)"
run_agy() { timeout 1800 agy -p "$(cat $R/briefs/agy.md)"$'\n\n'"$C" --mode plan --model gemini-3.1-pro-high --output-format text > $R/nodes/agy.md 2> $R/nodes/agy.stderr.txt; echo "exit=$?" > $R/nodes/agy.status; }
run_opencode() { timeout 1800 opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent plan "$(cat $R/briefs/opencode.md)"$'\n\n'"$C" > $R/nodes/opencode.md 2> $R/nodes/opencode.stderr.txt; echo "exit=$?" > $R/nodes/opencode.status; }
run_codex() { timeout 1800 codex exec -m gpt-6.1-sol -c model_reasoning_effort=high --sandbox read-only --skip-git-repo-check "$(cat $R/briefs/codex.md)"$'\n\n'"$C" < /dev/null > $R/nodes/codex.md 2> $R/nodes/codex.stderr.txt; echo "exit=$?" > $R/nodes/codex.status; }
run_agy & run_opencode & run_codex & wait
for e in agy opencode codex; do echo "- $(date -u +%FT%TZ) $e $(cat $R/nodes/$e.status) $(wc -c < $R/nodes/$e.md)B" >> $R/state.md; done
