#!/usr/bin/env bash
# Plant one break at a time in a copy of the guard and run the Round 18 tests there; each must fail.
# Run from the repository root: bash runs/20261017-agent-lessons/mutants.sh
set -u
guard=.claude/skills/workflow-design/guard
out=runs/20261017-agent-lessons/nodes/mutants.txt
: > "$out"
plant() { # name, file, old line (fixed string), new line
  local name=$1 file=$2 old=$3 new=$4
  local dir
  dir=$(mktemp -d "$CLAUDE_JOB_DIR/tmp/mutant-XXXXXX")
  cp -r "$guard"/. "$dir"/
  rm -rf "$dir/node_modules"; ln -s "$PWD/$guard/node_modules" "$dir/node_modules"
  if ! grep -qF -- "$old" "$dir/src/$file"; then echo "$name: PLANT MISSED (line not found)" >> "$out"; return; fi
  OLD=$old NEW=$new perl -0pi -e 's/\Q$ENV{OLD}\E/$ENV{NEW}/' "$dir/src/$file"
  if grep -qF -- "$old" "$dir/src/$file"; then echo "$name: PLANT MISSED (line still there)" >> "$out"; return; fi
  if (cd "$dir" && BUN_RUNTIME_TRANSPILER_CACHE_PATH=0 bun test test/round18-lessons.test.ts > "$dir/run.txt" 2>&1); then
    echo "$name: SURVIVED (tests passed)" >> "$out"
  else
    echo "$name: killed ($(grep -cE '^\(fail\)' "$dir/run.txt") failing)" >> "$out"
  fi
  rm -rf "$dir"
}
plant once-per-session lessons.ts 'const fresh = [...new Set(keys)].filter((key) => !seen.has(key));' 'const fresh = [...new Set(keys)];'
plant agent-filter lessons.ts 'if (!lesson.agents.includes("all") && !lesson.agents.includes(query.agent)) return false;' 'if (false) return false;'
plant fact-name lessons.ts 'return match !== null && match[1] === name ?' 'return match !== null ?'
cat "$out"
