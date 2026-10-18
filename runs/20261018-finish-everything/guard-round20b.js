export const meta = {
  name: 'guard-round20b',
  description: 'Guard Round 20 review fixes (CR1a, DL5, XB2, XB3): tests by Claude red first, code by opencode, verify, one repair',
  phases: [{ title: 'Tests' }, { title: 'Code' }, { title: 'Verify' }],
}
const RUN = 'runs/20261018-finish-everything'
const NODES = `${RUN}/nodes`
const G = '.claude/skills/workflow-design/guard'
const COMMON = name => `You are step ${name} of a workflow in this repository (its root is your working folder).
Another session also commits here: change only the files this step names; never commit, git add or stash.
First run: bun ${G}/src/cli.ts deadline status --session 1159cce6-66c2-47bb-8a08-d44519140778
If it prints "time is up", do nothing else and return time_up true with every other field empty.
Use the Bash tool's timeout 600000 ms for long commands. Report what commands printed, not what you expect.
Append \`- <date -Iseconds> · ${name} · start|done · <note>\` to ${NODES}/r20b.progress.md as you start and end.
`
const T = { time_up: { type: 'boolean' } }
const TESTS = { type: 'object', properties: { ...T, red: { type: 'array', items: { type: 'string' } }, not_red: { type: 'array', items: { type: 'string' } }, problem: { type: 'string' } }, required: ['time_up', 'red', 'not_red', 'problem'] }
const CODE = { type: 'object', properties: { ...T, exit: { type: 'number' }, status: { type: 'string' }, problem: { type: 'string' } }, required: ['time_up', 'exit', 'status', 'problem'] }
const VERIFY = { type: 'object', properties: { ...T, pass: { type: 'boolean' }, failing: { type: 'array', items: { type: 'string' } }, summary: { type: 'string' } }, required: ['time_up', 'pass', 'failing', 'summary'] }

phase('Tests')
const t = await agent(`${COMMON('tests')}
Step: write tests for the last paragraph of ${G}/SPEC.md ("Round 20, after its review": CR1a, DL5, XB2, XB3). You write
tests only; another engine writes the code. Read first and assert the way they do: ${G}/test/round20-deadline.test.ts,
${G}/test/round20-criteria.test.ts, the path-ask tests (grep -ln "record the path" ${G}/test/*.ts), and
tests/workflows/crossed_build_check_harness.mjs (its XB1 cases).
1. ${G}/test/round20b.test.ts (Write tool): CR1a — inside an open, not-up deadline, a session with a met criteria file and
   a success record gets the path ask at Stop exactly as with no deadline (the reviewer's input: criteria all met, a
   success journal record with check test-run, a 10-min deadline with 2 used); DL5 — \`deadline wait --id <id> --mark 50\`
   and \`--run <dir> --mark 50\` exit 2 with the --mark message and do not wait (use a long deadline so a wait would time out).
2. tests/workflows/crossed_build_check_harness.mjs: XB2 — with args.timeout 900, every write, review, fail-first and head
   prompt holds the form "( timeout 900 " … "echo \\"exit $?\\" >" … ".exit ) &" and says a missing .exit file is a failed
   step; XB3 — with args.timeout 120 and with the default, the fail-first and head prompts hold "timeout 120 <test_cmd>"
   (resp. "timeout 580 <test_cmd>"), and no prompt holds "600000" when the timeout is below 580. Add cases the way the
   file does.
Red runs: cd ${G} && bun src/cli.ts expect-fail --run "bun test test/round20b.test.ts" --out ../../../../${NODES}/r20b-tests.red.txt ;
and \`node tests/workflows/crossed_build_check_harness.mjs > ${NODES}/r20b-harness.red.txt 2>&1; echo "exit $?" >> ${NODES}/r20b-harness.red.txt\`.
red: the new tests failing now for the reason named; not_red: passing now, with why. The rest of the guard suite passes
(cd ${G} && bun test; only round20b may fail).`, { label: 'tests', phase: 'Tests', schema: TESTS })
if (!t || t.time_up) return { tests: t }

const code = (tag, extra) => agent(`${COMMON('code-' + tag)}
Step: have opencode write the code. Wait until no opencode runs: \`ps -eo args | grep -c "[o]pencode run"\` must print 0
(sleep 60 between checks, up to 45 minutes; if still busy return status "busy" without starting it).${extra ? ` Then write ${RUN}/briefs/r20b-code-${tag}.md with the Write tool: a copy of ${RUN}/briefs/r20b-code.md with this at the end:\n## Still failing after the first pass\n${extra}` : ''}
Run in the background (Bash run_in_background) and wait for it to end:
  timeout 2400 opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent build --variant high "Read ${RUN}/briefs/r20b-code${extra ? '-' + tag : ''}.md and do what it says. Use relative paths only." </dev/null > ${NODES}/r20b-code-${tag}.opencode.log 2>&1
Record its exit; read ${NODES}/r20b-code.result.md (status from it, else "none") and the log's last lines.`, { label: 'code-' + tag, phase: 'Code', schema: CODE })
const verify = tag => agent(`${COMMON('verify-' + tag)}
Step: verify. Run: cd ${G} && bun test; cd ${G} && ./node_modules/.bin/tsgo --noEmit -p .; node tests/workflows/crossed_build_check_harness.mjs.
git diff --stat -- ${G}/src .claude/workflows: only ${G}/src/hooks.ts, ${G}/src/cli.ts, ${G}/src/deadline.ts and
.claude/workflows/crossed-build-check.js may show changes (Round 20 is uncommitted, so earlier changes show too). The
test files ${G}/test/round20b.test.ts and tests/workflows/crossed_build_check_harness.mjs must be unchanged by the code
step: compare their sha256sum now with the values in ${NODES}/r20b-test-hashes.txt. pass only when all hold.`, { label: 'verify-' + tag, phase: 'Verify', schema: VERIFY, model: 'claude-sonnet-5-5' })

const hashes = await agent(`${COMMON('hashes')}
Step: run \`sha256sum ${G}/test/round20b.test.ts tests/workflows/crossed_build_check_harness.mjs > ${NODES}/r20b-test-hashes.txt\` and return its output as summary; pass true.`, { label: 'hashes', phase: 'Tests', schema: VERIFY, model: 'claude-haiku-5-5', effort: 'low' })
phase('Code')
let c = await code('a')
phase('Verify')
let v = c && !c.time_up && c.status !== 'busy' ? await verify('a') : null
if (v && !v.pass && !v.time_up) {
  log('verify a failed: ' + v.failing.join('; '))
  c = await code('b', v.failing.join('; '))
  v = c && !c.time_up && c.status !== 'busy' ? await verify('b') : null
}
return { tests: t, hashes, code: c, verify: v }
