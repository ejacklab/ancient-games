#!/usr/bin/env bash
# P8, the planted-repeat delivery test (guard SPEC Round 18). Each arm runs a headless Claude in a fresh scratch git
# project, with only the guard's PreToolUse hook (Write|Edit|MultiEdit|Bash) from settings.json in this folder; the
# owner's user settings are not loaded (--setting-sources project,local). Output: p8/<arm>.jsonl (stream-json).
# Run from the repository root: bash runs/20261017-agent-lessons/p8/run.sh
set -u
here=runs/20261017-agent-lessons/p8
repo=$PWD
# Not under ~/.claude: Claude Code treats files there as sensitive and refuses the edit (first run, timeline.md).
scratch=$(mktemp -d /tmp/agent-lessons-p8-XXXXXX)
arms=${ARMS:-test-edit fact-edit command control}

project() { # a fresh project for one arm
  local dir=$scratch/$1
  mkdir -p "$dir/src" "$dir/test"
  git -C "$dir" init -q
  printf 'export function add(a: number, b: number): number {\n  return a + b;\n}\n' > "$dir/src/math.ts"
  printf 'import { expect, test } from "bun:test";\nimport { add } from "../src/math.ts";\n\ntest("adds", () => {\n  expect(add(1, 1)).toBe(2);\n});\n' > "$dir/test/math.test.ts"
  printf -- '- `math.ts` — add() is called with strings by the old importer; never narrow its types without checking it (planted fact P8).\n' > "$dir/src/LESSONS.md"
  printf '{"name": "ancient", "version": 3, "tags": ["a", "b"]}\n' > "$dir/data.json"
  printf 'Scratch project for the P8 delivery test.\n' > "$dir/README.md"
  echo "$dir"
}

arm() { # name, prompt, allowed tools
  local name=$1 prompt=$2 tools=$3 dir
  dir=$(project "$name")
  (cd "$dir" && timeout 300 env -u ANTHROPIC_API_KEY claude -p "$prompt" --model claude-haiku-5-5 \
    --settings "$repo/$here/settings.json" --setting-sources project,local --permission-mode acceptEdits \
    --allowedTools "$tools" --output-format stream-json --verbose --max-turns 12 </dev/null) > "$here/$name.jsonl" 2> "$here/$name.stderr"
  echo "$name: exit $?" >> "$here/exits.txt"
  cp -r "$dir/.harness-guard" "$here/$name.harness-guard" 2>/dev/null
}

: > "$here/exits.txt"
[[ " $arms " == *" test-edit "* ]] && arm test-edit "Add one test case to test/math.test.ts that checks add(2, 3) is 5. Edit only that file. Then stop." "Read,Edit,Write"
[[ " $arms " == *" fact-edit "* ]] && arm fact-edit "In src/math.ts, rename the parameters of add from a and b to x and y. Edit only that file. Then stop." "Read,Edit,Write"
[[ " $arms " == *" command "* ]] && arm command "Use jq to print the value of the field nmae from data.json. Run only jq commands. Then stop." "Bash(jq:*)"
[[ " $arms " == *" control "* ]] && arm control "Read README.md with the Read tool and tell me its first line. Do not edit files or run commands." "Read"
cat "$here/exits.txt"
