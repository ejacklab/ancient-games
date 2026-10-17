#!/usr/bin/env bash
# C4: run the bridge (guard `evaluation ingest`) on the evaluator's real K2 verdicts (6 hidden faults, one per run) and
# compare, per verdict: FAIL requirements in verdict.json vs failures found_by evaluator in the guard's journal, and
# UNKNOWN requirements vs notes. Reads the evaluator worktree only; writes in a scratch git repo and the run folder.
# Run from the repository root: bash runs/20261017-evaluator-wiring/measure.sh
set -u
out=runs/20261017-evaluator-wiring/nodes/measure${BASELINE:+-baseline}.txt
cli=$PWD/.claude/skills/workflow-design/guard/src/cli.ts
: > "$out"
for v in /home/smoke01/dev/ancient-games-evaluator/runs/20261013-eval-k2-*/verdict.json; do
  name=$(basename "$(dirname "$v")")
  dir=$(mktemp -d /tmp/measure-XXXXXX); git -C "$dir" init -q; mkdir -p "$dir/runs/x"; cp "$v" "$dir/runs/x/verdict.json"
  cp /home/smoke01/dev/ancient-games-evaluator/runs/20261013-eval-k1d/verdict.json "$dir/runs/x/baseline.json"
  line=$(cd "$dir" && BUN_RUNTIME_TRANSPILER_CACHE_PATH=0 bun "$cli" evaluation ingest runs/x/verdict.json --run runs/x --session m ${BASELINE:+--baseline runs/x/baseline.json} 2>&1 | tail -1)
  read -r vf vu <<<"$(python3 -c "import json;d=json.load(open('$v'));r=d['requirements'];print(sum(x['verdict']=='FAIL' for x in r), sum(x['verdict']=='UNKNOWN' for x in r))")"
  gf=$(grep -c '"found_by":"evaluator"' "$dir/.harness-guard/journal.jsonl" 2>/dev/null || echo 0)
  gn=$(grep -c ' · UNKNOWN · ' "$dir/runs/x/evaluator-notes.md" 2>/dev/null || echo 0)
  echo "$name: verdict FAIL $vf → guard failures $gf; verdict UNKNOWN $vu → notes $gn; [$line]" | tee -a "$out"
  rm -rf "$dir"
done
