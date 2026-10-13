#!/usr/bin/env bash
# Format token test: instruction + the same content as markdown / xml / json (indented, compact), per engine.
# Text tokens = recorded prompt tokens - the engine's baseline call (in <engine>/baseline.*). Run from token-test/.
P="Reply with only the word OK. Do not use any tools."
e=$1
for f in markdown.md xml.xml json_indented.json json_compact.json; do
  b=${f%%.*}; T="$P

$(cat formats/$f)"
  case $e in
    claude)   timeout 600 env -u ANTHROPIC_API_KEY claude -p --model claude-opus-5-5 --output-format json "$T" </dev/null >formats/$e-$b.out 2>formats/$e-$b.err ;;
    codex)    timeout 600 codex -m gpt-6.1-sol exec -s read-only --skip-git-repo-check --json "$T" </dev/null >formats/$e-$b.out 2>formats/$e-$b.err ;;
    agy)      timeout 600 agy -p "$T" --mode plan --model gemini-3.8-flash-medium --output-format json </dev/null >formats/$e-$b.out 2>formats/$e-$b.err ;;
    opencode) timeout 600 opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent plan --format json "$T" </dev/null >formats/$e-$b.out 2>formats/$e-$b.err ;;
    dsh)      timeout 600 dsh headless --json "$T" </dev/null >formats/$e-$b.out 2>formats/$e-$b.err ;;
  esac
  echo "$e $b exit=$?" >> formats/exits.txt
done
