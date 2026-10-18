# Judge of the Codex review (Claude; read-only probes)

## 1 — reproduced
A SessionStart hook command that reads the cache and has 'not' later in the line ('cat project-memory/.cache/index.sqlite || echo not found') is treated as negated, so Rd1 does not fail.

Evidence: Contract memory_check/guidelines/CACHES.md:447 'Fails if a start hook or instruction opens any file under project-memory/.cache/'. Code memory_check/src/cachechecks.ts:145 'if (reading.negated) return;'. Probe (scratch copy of src with readLine exported, bun): readLine('cat project-memory/.cache/index.sqlite || echo not found') -> {opens:true, negated:true}; the bare cat -> {opens:true, negated:false}. So the hook command is skipped before reaching breaks.push.

## 2 — reproduced
headerDelimiters (entry.ts:84) stops at the first '---' pair that holds no field line, so a later second header is missed. A body pair with a 'key:' line ('Note: keep UTC timestamps.') is counted as a second header block, which makes W6.1a fail wrongly.

Evidence: Code memory_check/src/entry.ts:84 'break; // not a header, so no later pair is read as one'. idLines are collected only inside the first header (entry.ts:110-127). gitrequirements.ts:80-82 uses idLines>1 or headerBlocks>1. Probe parseEntry: entry + '---\nSee below.\n---' + second header 'id: b' -> idLines [2], headerBlocks 1 (second entry missed). Entry + body '---\nNote: keep UTC timestamps.\n---' -> headerBlocks 2 (false W6.1a break).

## 3 — reproduced
The K4.1 deletion warning has no file name. filesIn matches only INDEX.md/AGENTS.md by regex plus staged entries by name, and a deleted entry is not among the staged entries.

Evidence: Contract memory_check/REQUIREMENTS.md:68-69 R2 'with ids and file names'. Code warn.ts:15 FILE_NAME=/(project-memory\/INDEX\.md|AGENTS\.md)/g; warn.ts:55-62 matches only stagedEntries. Evidence text from gitrequirements.ts:104 'deleted <path>'. Probe renderWarning({stagedEntries:[], results:[K4.1 fail, evidence 'staged deleted project-memory/entries/2026-10-01-only.md ...']}) printed 'memory-check: SoT:K4.1 fails — an entry file was deleted, superseded without a link, or retired without a reason' with no files: part. Assumption (my reading of checks.ts:118 comment): a staged deletion is absent from stagedEntries. I did not run end to end with git.

## 4 — reproduced
fgCommand/bgCommand put 'timeout N' in front of the raw test_cmd without grouping it, so in a compound command only the first part is bounded.

Evidence: Contract guard/SPEC.md:927-928 XB1 'the limit of every engine call and test command'. Code .claude/workflows/crossed-build-check.js:70-72 fgCommand = `timeout ${TIMEOUT} ${command}`; :108 testRun passes t.test_cmd straight through. Probe: bash -c 'timeout 1 true && sleep 3' took 3s, past the 1s limit.

## 5 — reproduced
The C17 fake ps keeps every 'opencode run' line that contains 'second task', not only the test's marked lines. Another session running opencode run "second task" would stay visible, and the test that expects no trap would fail.

Evidence: Contract guard/SPEC.md:924-925 'every other process's opencode run line removed (the tests' own marked lines kept)'. Code round3.test.ts:858 awk '... || index($0, "second task")'. Probe on that awk with marker tmp-MARK kept '111 opencode run "second task"' (an external line with no marker) and dropped 'opencode run "other"'. The test at round3.test.ts:909-915 expects no trap:opencode-parallel. Only the filter was probed. I did not run the full test with a real external process (the collision needs another session to use that exact text).

## 6 — reproduced
An explicit timeout: null is turned into the 580 default instead of being rejected.

Evidence: Contract guard/SPEC.md:927-931 XB1 '(seconds, a whole number from 60 to 3600, default 580) ... Anything else is `args.timeout must be a whole number of seconds from 60 to 3600`'. Code crossed-build-check.js:54 'a.timeout === undefined || a.timeout === null ? 580 : a.timeout'. Read only, not run. My reading: 'default' covers an omitted value, and null is a given value that is not a whole number, so it falls under 'anything else'. If the owner counts null as 'not given', this is not a defect.


## Main agent
6 is dropped (my reading): JSON args often send null for "not given", which the spec's default covers.
