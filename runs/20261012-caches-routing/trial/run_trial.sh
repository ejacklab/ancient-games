#!/usr/bin/env bash
# Node 4: real token cost. Each question is asked of claude-sonnet-5-5 twice (headless, one fresh session each):
#   arm "grep"  - Read, Grep, Glob and rg only
#   arm "cache" - the same plus the bench query CLI (fts, vec, hybrid, graph routes)
# usage comes from --output-format json. n=1 per cell: a single sample, not a distribution.
set -u
R=/home/smoke01/dev/ancient-games/runs/20261012-caches-routing
PY=/tmp/claude-1000/-home-smoke01-dev-ancient-games/343bf18f-e2d9-4dcf-8db5-0ed3524f59db/scratchpad/caches-venv/bin/python
Q="$R/bench/query.py"
cd /home/smoke01/dev/ancient-games
IDS="${*:-B03 B07 C01 C06 D01 D07}"
for id in $IDS; do
  question=$(python3 -c "import json,sys;print(next(x['question'] for x in json.load(open('$R/queries.json')) if x['id']=='$id'))")
  base="Answer this question about the repository in the current directory: $question
Reply with only the answer: the file path(s), and the function name where it applies, one per line, at most 8 lines. Do not edit any file."
  cache_note="
You also have a prebuilt search CLI over this repo's .py and .md files (derived caches, read-only). Call it as:
  $PY $Q --route ROUTE --query-json '{\"question\": \"...\", \"terms\": [\"...\"], \"symbol\": null, \"file\": null}'
Routes: fts (SQLite full-text over the given terms, bm25-ranked), vec (embedding search on the question), hybrid (both, fused),
graph (needs symbol or file: callers of a symbol, tests reaching a symbol, or tests reaching a file). It prints JSON with ranked paths."
  for arm in grep cache; do
    out="$R/trial/$id.$arm.json"
    [ -s "$out" ] && continue
    if [ "$arm" = grep ]; then prompt="$base"; tools=(Read Grep Glob "Bash(rg:*)")
    else prompt="$base$cache_note"; tools=(Read Grep Glob "Bash(rg:*)" "Bash($PY $Q:*)"); fi
    timeout 600 claude -p "$prompt" --model claude-sonnet-5-5 --output-format json --no-session-persistence \
      --strict-mcp-config --allowedTools "${tools[@]}" --disallowedTools Edit Write NotebookEdit \
      > "$out" 2> "$R/trial/$id.$arm.stderr.txt"
    echo "$id $arm exit=$?" >> "$R/trial/status.txt"
  done
done
