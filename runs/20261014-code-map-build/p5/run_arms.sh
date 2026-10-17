#!/bin/bash
# L2 round 1: six claude -p runs, same model, map arm vs reading arm. Output: p5/out-<module>-<arm>.json
cd /home/smoke01/dev/ancient-games/runs/20261014-opencode-code-map/src/opencode
for id in m1-session m2-tools m3-ai; do
  for arm in map read; do
    if [ $arm = map ]; then tools=(--allowedTools "Bash(bun:*)" Read Grep Glob); else tools=(--allowedTools Read Grep Glob --disallowedTools Bash); fi
    ( s=$(date +%s); timeout 2400 env -u ANTHROPIC_API_KEY claude -p --model claude-sonnet-5-5 --output-format json "${tools[@]}" < /home/smoke01/dev/ancient-games/runs/20261014-code-map-build/p5/prompt-$id-$arm.md > /home/smoke01/dev/ancient-games/runs/20261014-code-map-build/p5/out-$id-$arm.json 2> /home/smoke01/dev/ancient-games/runs/20261014-code-map-build/p5/out-$id-$arm.err; echo "$id $arm exit=$? wall=$(($(date +%s)-s))s" >> /home/smoke01/dev/ancient-games/runs/20261014-code-map-build/p5/runs.log ) &
  done
done
wait
echo all-done >> /home/smoke01/dev/ancient-games/runs/20261014-code-map-build/p5/runs.log
