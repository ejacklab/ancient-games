## test-edit

- call Bash cat /tmp/agent-lessons-p8-hRA2SQ/test-edit/test/math.test.ts; echo "---"; ls /tmp/agent-l…
  result (ok): import { expect, test } from "bun:test"; import { add } from "../src/math.ts"; test("adds", () => { expect(add(1, 1)).toBe(2); }); --- LESSONS.md mat…
- call Edit /tmp/agent-lessons-p8-hRA2SQ/test-edit/test/math.test.ts
  result (error): PreToolUse:Edit hook error: harness-guard lesson — not a block for a mistake: read it, then send the call again, changed only if the lesson applies t…
- says: The hook's lessons don't change this edit: I already read the existing test, and I'm using the same `expect(...).toBe(...)` form. The expected value …
- call Edit /tmp/agent-lessons-p8-hRA2SQ/test-edit/test/math.test.ts
  result (ok): The file /tmp/agent-lessons-p8-hRA2SQ/test-edit/test/math.test.ts has been updated successfully.
- says: I added the test case to `test/math.test.ts`, and that's the only file I changed: ```ts test("adds 2 and 3 to get 5", () => { expect(add(2, 3)).toBe(…
- end: is_error=False turns=4

calls 3, results carrying a lesson hold 1

## fact-edit

- call Read /tmp/agent-lessons-p8-hRA2SQ/fact-edit/src/math.ts
  result (ok): 1 export function add(a: number, b: number): number { 2 return a + b; 3 } 4
- call Edit /tmp/agent-lessons-p8-hRA2SQ/fact-edit/src/math.ts
  result (error): PreToolUse:Edit hook error: harness-guard lesson — not a block for a mistake: read it, then send the call again, changed only if the lesson applies t…
- says: The hook's note concerns type narrowing and new test cases, and this rename changes neither, so I'm retrying the same edit unchanged.
- call Edit /tmp/agent-lessons-p8-hRA2SQ/fact-edit/src/math.ts
  result (ok): The file /tmp/agent-lessons-p8-hRA2SQ/fact-edit/src/math.ts has been updated successfully. (file state is current in your context — no need to Read i…
- says: I renamed the `add` parameters in `src/math.ts` from `a` and `b` to `x` and `y`, and updated the body to `return x + y;`. No other file was touched. …
- end: is_error=False turns=4

calls 3, results carrying a lesson hold 1

## command

- call Bash jq '.nmae' /home/smoke01/.claude/jobs/1159cce6/tmp/p8/command/data.json
  result (error): PreToolUse:Bash hook error: harness-guard lesson — not a block for a mistake: read it, then send the call again, changed only if the lesson applies t…
- call Bash jq 'keys' /home/smoke01/.claude/jobs/1159cce6/tmp/p8/command/data.json
  result (ok): [ "name", "tags", "version" ]
- call Bash jq '.name' /home/smoke01/.claude/jobs/1159cce6/tmp/p8/command/data.json
  result (ok): "ancient"
- says: The value of `name` in `data.json` is `"ancient"`. You asked for `nmae`, which isn't a key in the file. The top-level keys are `name`, `tags`, and `v…
- end: is_error=False turns=4

calls 3, results carrying a lesson hold 1

## control

- call Read /home/smoke01/.claude/jobs/1159cce6/tmp/p8/control/README.md
  result (ok): 1 Scratch project for the P8 delivery test.
- says: The first line of `README.md` is: "Scratch project for the P8 delivery test."
- end: is_error=False turns=2

calls 1, results carrying a lesson hold 0

