---
node: m3-tests
attempt: 1
engine: opencode
model: minimax-coding-plan/MiniMax-M3.1-Flash-Preview
status: ok
started: 2026-10-15T08:15:34Z
ended: 2026-10-15T08:18:56Z
evidence: runs/20261015-ts-hybrid/nodes/m3-tests-1.evidence.txt
---
72 acceptance tests pin every M3 Fails-if line and call all five M3 exports with the exact SPEC.md signatures; the file loads and fails only because `src/insight.ts` does not exist.
- Files written: tools/harness-guard/test/insight.test.ts, runs/20261015-ts-hybrid/nodes/m3-tests-1.evidence.txt, runs/20261015-ts-hybrid/nodes/m3-tests-1.result.md
- Check: `cd tools/harness-guard && bun test test/insight.test.ts` → loads, then `0 pass, 1 fail, 1 error` — `error: Cannot find module '../src/insight.ts' from '/home/smoke01/dev/ancient-games-ts-hybrid/tools/harness-guard/test/insight.test.ts'` (the only failure).
- Check: `cd tools/harness-guard && ./node_modules/.bin/tsgo --noEmit -p .` → only `test/insight.test.ts(5,86): error TS2307: Cannot find module '../src/insight.ts'` for my file; no other type error in it. (The other two errors, `test/journal.test.ts` and `test/traps.test.ts`, belong to other nodes' files, which I did not touch.)
- Check (supplementary, outside the repository): the same test file against a throwaway reference implementation in /tmp — `72 pass, 0 fail`; and seven mutations of that reference (drop the option-evidence rule, stop reading a root cause on the next non-empty line, return unsorted paths, let `answered` accept sections with fail findings, keep the last answering file instead of the first, narrow the person heuristic, keep duplicate ids) — every mutation is caught except the duplicate-id one, which SPEC.md does not describe.
- CONTRADICTS:
  - tools/harness-guard/SPEC.md line 112 lists exactly four allowed option kinds (`[rule]`, `[check]`, `[tool]`, `[config-advice]`), so an unknown kind such as `[policy]` should arguably fail `R12.3-option-kind`; tools/harness-guard/src/types.ts line 107 says `kind: string; // rule | check | tool | config-advice, or what was written`, which lets any bracketed kind pass. Unresolved, so the tests pin only the missing-kind case (`kind: ""`) and assert nothing about an unknown kind.
  - The brief says `src/journal.ts` (M2) is already built and tested; it does not exist (tsgo: `test/journal.test.ts(16,8): error TS2307: Cannot find module '../src/journal.ts'`). The M3 tests therefore write `.harness-guard/journal.jsonl` lines and `.harness-guard/evidence/<id>.json` files themselves instead of importing journal.ts, and do not assert anything about journal validation.
  - SPEC.md line 105 writes the pattern `runs/**/insight*.md` without saying whether `**` matches zero directories, so `runs/insight.md` is left untested; the tests only use files one or two directories below `runs/`.
  - SPEC.md does not say whether `findInsightFiles`, `answered` and `openFailures` call `guardRoot(root)` themselves (Common, line 22) or trust their argument; the tests pass a real `git init` root, so both readings give the same result.