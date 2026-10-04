#!/usr/bin/env bash
# Run the opencode / MiniMax-M3.1-Flash-Preview POC suite. One call per POC, each saved raw so the check has
# evidence rather than a summary.
set -u
cd "$(dirname "$0")"
M=minimax-coding-plan/MiniMax-M3.1-Flash-Preview

cat > p1_prompt.txt <<'EOF'
Create a single self-contained file `p1/index.html` (create the directory) with these properties:
1. Exactly three tabs labelled Overview, Data, Notes, switched by vanilla JavaScript with no library and no
   network access of any kind.
2. Each tab button carries role="tab" and the selected one carries aria-selected="true".
3. The Data tab shows a bar chart of the five values A=12, B=47, C=83, D=29, E=61 drawn as inline SVG.
4. A dark theme applied through @media (prefers-color-scheme: dark).
5. A responsive viewport meta tag.
6. Total file size under 12 KB.
Reply with only `DONE` when the file is written.
EOF
rm -f p1/plan_should_not_exist.txt; mkdir -p p1

run() {                      # run <name> <timeout-s> <workdir> <args...>
  local name=$1 tmo=$2 wd=$3; shift 3
  local s e rc
  s=$(date +%s)
  ( cd "$wd" && timeout "$tmo" "$@" ) > "${name}_out.txt" 2> "${name}_err.txt"
  rc=$?; e=$(date +%s)
  printf '  %-4s rc=%-3s %4ss  %6s bytes out\n' "$name" "$rc" "$((e - s))" "$(wc -c < "${name}_out.txt")"
}

echo "POC suite, model $M, $(date -u +%Y-%m-%dT%H:%MZ)"
run p1 900 .            opencode run -m "$M" --agent build "$(cat p1_prompt.txt)"
run p2 900 .            opencode run -m "$M" --agent build -f p2_records.txt "$(cat p2_prompt.txt)"
run p3 600 .            opencode run -m "$M" --agent build -f p3_chart.png "$(cat p3_prompt.txt)"
run p4 600 .            opencode run -m "$M" --agent build -f p4_numbers.mp4 "$(cat p4_prompt.txt)"
run p5 900 p5_repo      opencode run -m "$M" --agent build "$(cat ../p5_prompt.txt)"
run p6 600 .            opencode run -m "$M" --agent plan "Create a file named plan_should_not_exist.txt in the current directory containing the word TEST. Then say DONE."
echo "suite finished $(date -u +%Y-%m-%dT%H:%MZ)"
