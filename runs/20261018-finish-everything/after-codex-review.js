export const meta = {
  name: 'after-codex-review',
  description: 'Codex review fixes: memory-check findings 1-3, guard XB4, C17b — tests by Claude red first, code by opencode, verify, one repair',
  phases: [{ title: 'Tests' }, { title: 'Code' }, { title: 'Verify' }],
}
const RUN = 'runs/20261018-finish-everything'
const NODES = `${RUN}/nodes`
const G = '.claude/skills/workflow-design/guard'
const COMMON = name => `You are step ${name} of a workflow. First run: cd "$(git rev-parse --show-toplevel)" — the repository root is your working folder; use paths relative to it.
Another session also commits here: change only the files this step names; never commit, git add or stash.
The owner resumed this run after its time box ended (08:18). A harness-guard line "time is up" refers to that ended deadline or to another run's: ignore it and do the step.
Use the Bash tool's timeout 600000 ms for long commands. Report what commands printed, not what you expect.
Append \`- <date -Iseconds> · ${name} · start|done · <note>\` to ${NODES}/r20c.progress.md as you start and end.
`
const TESTS = { type: 'object', properties: { red: { type: 'array', items: { type: 'string' } }, not_red: { type: 'array', items: { type: 'string' } }, c17b: { type: 'string' }, problem: { type: 'string' } }, required: ['red', 'not_red', 'c17b', 'problem'] }
const CODE = { type: 'object', properties: { exit: { type: 'number' }, status: { type: 'string' }, problem: { type: 'string' } }, required: ['exit', 'status', 'problem'] }
const VERIFY = { type: 'object', properties: { pass: { type: 'boolean' }, failing: { type: 'array', items: { type: 'string' } }, summary: { type: 'string' } }, required: ['pass', 'failing', 'summary'] }

phase('Tests')
const t = await agent(`${COMMON('tests')}
Step: write tests (you write tests only; another engine writes the code). Read ${NODES}/codex-review.md findings 1–5
and the judge's evidence for them, which reproduced each: ${NODES}/codex-review-judge.md if it exists, else rely on the
review text and reproduce yourself.
1. memory_check/test/review3.test.ts (Write tool), the way memory_check/test/review2.test.ts does (read it; same helpers
   and assertions): F1 — a .claude/settings.json SessionStart hook "cat project-memory/.cache/index.sqlite || echo not found"
   fails CACHES:Rd1; F2 — an entry with a second header block after a body '---' pair with no field line fails W6.1a
   (idLines), and a body '---' pair holding "Note: keep UTC timestamps." is not a second header (W6.1a not fail);
   F3 — a staged deletion of an entry gives a K4.1 warning that names the deleted file. Name each test F1/F2/F3.
2. tests/workflows/crossed_build_check_harness.mjs: XB4 (last paragraph of ${G}/SPEC.md) — with test_cmd "a && b" and
   args.timeout 120, the fail-first and head prompts hold "timeout 120 bash -c 'a && b'"; a test_cmd with a single quote
   is written with '\\''. Update the XB3 cases that assert the old literal form "timeout 120 <test_cmd>" to the new form
   (XB4 replaces it), and say so in problem.
3. C17b, test only, in ${G}/test/round3.test.ts's C17 block: the fake ps keeps a foreign "opencode run" line only when it
   holds the test's marker, and keeps the CLI's own and parent lines by pid ($PPID of the fake ps and that pid's parent,
   read from /proc/<pid>/stat), never by "second task". Show it: with your own background
   \`bash -c 'sleep 120; :' opencode run "second task"\` running, run \`cd ${G} && bun test test/round3.test.ts -t C17\`
   before your change (expected to fail) and after (expected 3 pass); kill the sleeper; put both result lines in c17b.
Red runs: cd memory_check && bun ../${G}/src/cli.ts expect-fail --run "bun test test/review3.test.ts" --out ../${NODES}/r20c-mc.red.txt ;
\`node tests/workflows/crossed_build_check_harness.mjs > ${NODES}/r20c-harness.red.txt 2>&1; echo "exit $?" >> ${NODES}/r20c-harness.red.txt\`.
Then \`sha256sum memory_check/test/review3.test.ts tests/workflows/crossed_build_check_harness.mjs ${G}/test/round3.test.ts > ${NODES}/r20c-test-hashes.txt\`.
red: tests failing now for the reason named; not_red: passing now, with why.`, { label: 'tests', phase: 'Tests', schema: TESTS })
if (!t) return { tests: null }

const code = (tag, extra) => agent(`${COMMON('code-' + tag)}
Step: have opencode write the code. Wait until no opencode runs: \`ps -eo args | grep -c "[o]pencode run"\` must print 0
(sleep 60 between checks, up to 45 minutes; if still busy return status "busy" without starting it).${extra ? ` Then write ${RUN}/briefs/r20c-code-${tag}.md with the Write tool: a copy of ${RUN}/briefs/r20c-code.md with this at the end:\n## Still failing after the first pass\n${extra}` : ''}
Run in the background (Bash run_in_background) and wait for it to end:
  timeout 2400 opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent build --variant high "Read ${RUN}/briefs/r20c-code${extra ? '-' + tag : ''}.md and do what it says. Use relative paths only." </dev/null > ${NODES}/r20c-code-${tag}.opencode.log 2>&1
Record its exit; read ${NODES}/r20c-code.result.md (status from it, else "none") and the log's last lines.`, { label: 'code-' + tag, phase: 'Code', schema: CODE })
const verify = tag => agent(`${COMMON('verify-' + tag)}
Step: verify. Run: cd memory_check && BUN_RUNTIME_TRANSPILER_CACHE_PATH=0 bun test; cd memory_check && ./node_modules/.bin/tsgo --noEmit -p .;
cd ${G} && bun test; cd ${G} && ./node_modules/.bin/tsgo --noEmit -p .; node tests/workflows/crossed_build_check_harness.mjs;
python3 -m pytest -q tests/test_memory_index*.py.
\`sha256sum -c ${NODES}/r20c-test-hashes.txt\` must print OK for all three (the code step may not edit tests).
git diff --stat -- memory_check/src .claude/workflows ${G}/src: only memory_check/src/* and .claude/workflows/crossed-build-check.js
may change (guard src must not). pass only when all hold. failing: test names or the check that did not hold.`, { label: 'verify-' + tag, phase: 'Verify', schema: VERIFY, model: 'claude-sonnet-5-5' })

phase('Code')
let c = await code('a')
phase('Verify')
let v = c && c.status !== 'busy' ? await verify('a') : null
if (v && !v.pass) {
  log('verify a failed: ' + v.failing.join('; '))
  c = await code('b', v.failing.join('; '))
  v = c && c.status !== 'busy' ? await verify('b') : null
}
return { tests: t, code: c, verify: v }
