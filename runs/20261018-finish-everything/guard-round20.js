export const meta = {
  name: 'guard-round20',
  description: 'Guard Round 20 (deadline --id/--run, end never guesses, criteria at the end, C17 alone, crossed-build-check timeout): tests by Claude red first, code by mcode, verify, one repair, review',
  phases: [
    { title: 'Tests', detail: 'Claude writes round20 tests + the C17 fake ps + the harness check; red runs' },
    { title: 'Code', detail: 'opencode from briefs/r20-code.md (mcode launch refused by the classifier)' },
    { title: 'Verify', detail: 'full guard suite, tsgo, workflow harness' },
    { title: 'Review', detail: 'read-only review of the diff against SPEC Round 20' },
  ],
}
const RUN = 'runs/20261018-finish-everything'
const NODES = `${RUN}/nodes`
const G = '.claude/skills/workflow-design/guard'
const COMMON = name => `You are step ${name} of a workflow in this repository (its root is your working folder).
Another session also commits here: change only the files this step names; never commit, git add or stash.
First run: bun ${G}/src/cli.ts deadline status
If it prints "time is up", do nothing else and return time_up true with every other field empty.
Use the Bash tool's timeout 600000 ms for long commands. Report what commands printed, not what you expect.
Append \`- <date -Iseconds> · ${name} · start|done · <note>\` to ${NODES}/r20.progress.md as you start and end.
`
const T = { time_up: { type: 'boolean' } }
const TESTS = { type: 'object', properties: { ...T, test_files: { type: 'array', items: { type: 'string' } }, red: { type: 'array', items: { type: 'string' } }, not_red: { type: 'array', items: { type: 'string' } }, c17_with_other_opencode: { type: 'string' }, problem: { type: 'string' } }, required: ['time_up', 'test_files', 'red', 'not_red', 'c17_with_other_opencode', 'problem'] }
const CODE = { type: 'object', properties: { ...T, exit: { type: 'number' }, status: { type: 'string' }, problem: { type: 'string' } }, required: ['time_up', 'exit', 'status', 'problem'] }
const VERIFY = { type: 'object', properties: { ...T, pass: { type: 'boolean' }, failing: { type: 'array', items: { type: 'string' } }, summary: { type: 'string' } }, required: ['time_up', 'pass', 'failing', 'summary'] }
const REVIEW = { type: 'object', properties: { ...T, findings: { type: 'array', items: { type: 'object', properties: { spec_line: { type: 'string' }, where: { type: 'string' }, problem: { type: 'string' }, input: { type: 'string' } }, required: ['spec_line', 'where', 'problem', 'input'] } } }, required: ['time_up', 'findings'] }

phase('Tests')
const t = await agent(`${COMMON('tests')}
Step: write the tests for guard Round 20 — read the last section of ${G}/SPEC.md ("Round 20"). You write tests only;
another engine writes the code. Read first, and assert the way they do: ${G}/test/round10*.test.ts (deadline tests),
the criteria-step tests (grep -l "criteria-state\\|criteriaStep\\|not scored yet" ${G}/test/*.ts), and
tests/workflows/crossed_build_check_harness.mjs.
1. ${G}/test/round20-deadline.test.ts: DL1, DL2, DL3 (two open deadlines, end with neither flag ends none and exits 2;
   one open ends it), DL4 (unchanged choice). Name each test by its rule id.
2. ${G}/test/round20-criteria.test.ts: CR1 — a Stop inside an open, not-up deadline is not blocked by an unmarked
   criteria file and writes no criteria failure, and gives the context line; after the deadline is ended, or when it
   is up, the same stop is blocked as today; a session with no deadline is blocked as today.
3. C17 in ${G}/test/round3.test.ts: replace requireNoOtherOpencode with a fake \`ps\` put first on PATH for the CLI
   runs (a small script in the test's temp folder that runs the real ps by absolute path and drops every line matching
   "opencode run" that does not hold the test's own marker or "second task"), so the three C17 tests pass while another
   opencode runs. Change nothing else in that file.
4. tests/workflows/crossed_build_check_harness.mjs: XB1 cases — the default 580 reaches every engine call and test
   command; args.timeout 1200 reaches them and the prompt says to run in the background; 30, 4000 and "x" are refused
   with the spec's message. Add cases the way the file already does.
Red runs (expected to fail now; save each):
  cd ${G} && bun src/cli.ts expect-fail --run "bun test test/round20-deadline.test.ts test/round20-criteria.test.ts" --out ../../../../${NODES}/r20-tests.red.txt
  bun ${G}/src/cli.ts expect-fail --run "node tests/workflows/crossed_build_check_harness.mjs" --out ${NODES}/r20-harness.red.txt
red: test names that fail now for the reason the spec names; not_red: those that pass now (say why — e.g. DL4 freezes
today's behaviour, which is expected to pass). C17: start your own background \`bash -c 'sleep 120; :' opencode run other-session\`,
run \`cd ${G} && bun test test/round3.test.ts -t C17\`, kill the sleeper, and put the result line in c17_with_other_opencode.
Every other existing guard test must still pass: cd ${G} && bun test (only round20 files may fail).`,
  { label: 'tests', phase: 'Tests', schema: TESTS })
if (!t || t.time_up) return { tests: t }

const code = tag => agent(`${COMMON('code-' + tag)}
Step: have opencode write the code. First wait until no opencode runs: \`ps -eo args | grep -c "[o]pencode run"\` must print 0 (check with sleep 60 between checks, up to 45 minutes; if still busy, return status "busy" and do not start it). Check the brief ${RUN}/briefs/r20-code.md exists${tag === 'a' ? '' : `, then write ${RUN}/briefs/r20-code-${tag}.md with the Write tool: a copy of it with this added at the end under "## Still failing": ${'${FAILING}'}`}.
Run in the background with the Bash tool (run_in_background) and wait for it to end:
  timeout 2400 opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent build --variant high "Read ${RUN}/briefs/r20-code${tag === 'a' ? '' : '-' + tag}.md and do what it says. Use relative paths only." </dev/null > ${NODES}/r20-code-${tag}.opencode.log 2>&1
Record its exit; read ${NODES}/r20-code.result.md if it exists (status from it, else "none"), and the last lines of the log.
If opencode wrote nothing (git diff --stat ${G}/src .claude/workflows/crossed-build-check.js is empty) say so in problem.`,
  { label: 'code-' + tag, phase: 'Code', schema: CODE })
const verify = tag => agent(`${COMMON('verify-' + tag)}
Step: verify. Run: cd ${G} && bun test; cd ${G} && ./node_modules/.bin/tsgo --noEmit -p .; node tests/workflows/crossed_build_check_harness.mjs;
git diff --stat (changes allowed only in ${G}/src/, ${G}/test/, ${G}/SPEC.md, .claude/workflows/crossed-build-check.js,
tests/workflows/crossed_build_check_harness.mjs, ${RUN}/; ignore other sessions' files: CLAUDE.md, docs/TASK_TYPES_LEDGER.md,
docs/code-graph/CODE_GRAPH.md, runs/20261012-index-md-build/*, runs/20261014-code-map-build/*, and memory_check/ or
tools/memory_index.py or tests/test_memory_index* which another step of this run changes). Also: git diff ${G}/test/
must show no change to a test file other than round3.test.ts's C17 block and the new round20 files (the coder may not
edit tests). pass only when all hold. failing: test names or the check that did not hold.`,
  { label: 'verify-' + tag, phase: 'Verify', schema: VERIFY, model: 'claude-sonnet-5-5' })

phase('Code')
let c = await code('a')
phase('Verify')
let v = c && !c.time_up ? await verify('a') : null
if (v && !v.pass && !v.time_up) {
  log('verify a failed: ' + v.failing.join('; '))
  const FAILING = v.failing.join('; ')
  c = await agent(`${COMMON('code-b')}
Step: one repair by opencode. Wait the same way until no opencode runs. Write ${RUN}/briefs/r20-code-b.md with the Write tool: a copy of ${RUN}/briefs/r20-code.md with this added at the end:
"## Still failing after the first pass\n${FAILING}"
Run in the background (run_in_background) and wait:
  timeout 2400 opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent build --variant high "Read ${RUN}/briefs/r20-code-b.md and do what it says. Use relative paths only." </dev/null > ${NODES}/r20-code-b.opencode.log 2>&1
Record its exit and status as before.`, { label: 'code-b', phase: 'Code', schema: CODE })
  v = c && !c.time_up ? await verify('b') : null
}
phase('Review')
const r = v && v.pass ? await agent(`${COMMON('review')}
Step: a read-only review. Read the last section of ${G}/SPEC.md (Round 20) and the diff: git diff -- ${G}/src .claude/workflows/crossed-build-check.js.
Find places where the code breaks a Round 20 line or a Fails-if, or breaks behaviour the spec calls unchanged. For each:
the spec line quoted, file:line, the problem, an input that shows it. Probe with read-only commands where cheap. Change
no file. An empty list is a fine answer.`, { label: 'review', phase: 'Review', schema: REVIEW, model: 'claude-sonnet-5-5' }) : null
return { tests: t, code: c, verify: v, review: r }
