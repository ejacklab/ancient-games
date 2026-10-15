#!/usr/bin/env bash
# Run one build node in the worktree through runlog.py (method 3.8), then check the result file exists and is not
# empty — exit 0 alone is not success (R12.1). Usage: run_node.sh NODE ATTEMPT
set -u
NODE=$1; ATT=$2
WT=/home/smoke01/dev/ancient-games-ts-hybrid
MAIN=/home/smoke01/dev/ancient-games
ENG=$(python3 -c "import json;print({n['id']:n['engine'] for n in json.load(open('$MAIN/runs/20261015-ts-hybrid/build-plan.json'))['nodes']}['$NODE'])")
BRIEF="runs/20261015-ts-hybrid/briefs/$NODE-$ATT.md"
PROMPT="Read $BRIEF and do what it says."
cd "$WT" || exit 2
[ -s "$BRIEF" ] || { echo "no brief $BRIEF"; exit 2; }
if [ "$NODE" = review ]; then
  CMD=(codex exec -m gpt-6.1-sol -c model_reasoning_effort=high -s read-only --skip-git-repo-check -o "runs/20261015-ts-hybrid/nodes/$NODE-$ATT.result.md" "$PROMPT"); MODEL=gpt-6.1-sol
elif [ "$ENG" = codex ]; then
  CMD=(codex exec -m gpt-6.1-sol -c model_reasoning_effort=high -s workspace-write --skip-git-repo-check -o "runs/20261015-ts-hybrid/nodes/$NODE-$ATT.last.txt" "$PROMPT"); MODEL=gpt-6.1-sol
else
  CMD=(opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent build --variant high "$PROMPT"); MODEL=MiniMax-M3.1-Flash-Preview
fi
python3 "$MAIN/.claude/skills/workflow-design/scripts/runlog.py" --runs-root "$MAIN/runs" exec --run 20261015-ts-hybrid \
  --node "$NODE" --attempt "$ATT" --engine "$ENG" --model "$MODEL" --timeout 2400 -- "${CMD[@]}" </dev/null
RC=$?
RES="runs/20261015-ts-hybrid/nodes/$NODE-$ATT.result.md"
if [ -s "$RES" ]; then echo "NODE $NODE-$ATT engine=$ENG exit=$RC result=present"; else echo "NODE $NODE-$ATT engine=$ENG exit=$RC result=MISSING"; exit 3; fi
exit $RC
