#!/bin/bash
# P6: three design tasks x two arms (with the code-map plugin, without). Same model, same tools; only the plugin differs.
cd /home/smoke01/dev/ancient-games/runs/20261014-opencode-code-map/src/opencode
tools=(--allowedTools "Bash(bun:*)" Read Grep Glob Skill)
for arm in with without; do
  for id in task1 task2 task3; do
    extra=(); [ $arm = with ] && extra=(--plugin-dir /home/smoke01/dev/ancient-games/runs/20261014-code-map-build/p6/plugin)
    ( s=$(date +%s); timeout 2100 env -u ANTHROPIC_API_KEY claude -p --model claude-sonnet-5-5 --output-format json "${tools[@]}" "${extra[@]}" < /home/smoke01/dev/ancient-games/runs/20261014-code-map-build/p6/prompt-$id.md > /home/smoke01/dev/ancient-games/runs/20261014-code-map-build/p6/out-$id-$arm.json 2> /home/smoke01/dev/ancient-games/runs/20261014-code-map-build/p6/out-$id-$arm.err; echo "$id $arm exit=$? wall=$(($(date +%s)-s))s" >> /home/smoke01/dev/ancient-games/runs/20261014-code-map-build/p6/runs.log ) &
  done
  wait
done
echo all-done >> /home/smoke01/dev/ancient-games/runs/20261014-code-map-build/p6/runs.log
