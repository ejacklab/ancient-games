export const meta = {
  name: 'crossed-build-check',
  description: 'Have engines other than the one that wrote the code write its tests, show each new test fails on the base commit, run them on the current code, then review read-only. Reports; decides nothing.',
  whenToUse: 'After a build, to check it with tests written by other engines (plan B). args: {run: "runs/<id>", base: "<commit before the build>", code_engine: "opencode|codex|dsh|claude", tests: [{id, engine, brief, test_cmd}], review: {engine: "codex|dsh", brief}}. Briefs are files inside the repo. A brief on the code engine is refused. Design: runs/20261017-workflows/design.md.',
  phases: [
    { title: 'Write tests', detail: 'one engine run per brief; opencode briefs one after another, the others in parallel' },
    { title: 'Fail first', detail: 'in a temporary worktree at base, with only the new test files copied in; every new test must fail there' },
    { title: 'Head', detail: 'run each brief\'s test command in the repo' },
    { title: 'Review', detail: 'read-only review on its own brief, after every test step' },
  ],
}

// Design: runs/20261017-workflows/design.md, "crossed-build-check". Every step is an agent (the script API has no shell
// step). Command-only steps run on haiku at low effort; Fail first reads and judges, so it runs on the session model.
// The script cannot read the clock: each step's agent runs `deadline status` first and returns time_up; after that the
// script starts no further step. The script decides nothing: the main agent reads the return and decides.

const ENGINES = ['opencode', 'codex', 'dsh', 'claude']
const REVIEW_ENGINES = ['codex', 'dsh'] // the design gives a read-only command only for these two
const CHEAP = { model: 'claude-haiku-5-5', effort: 'low' }

const a = args && typeof args === 'object' && !Array.isArray(args) ? args : {}
const errors = []
const str = v => typeof v === 'string' && v.trim() !== ''
const ID = /^[a-z0-9][a-z0-9-]*$/
const REPO_PATH = /^[A-Za-z0-9_][A-Za-z0-9._/-]*$/ // relative, no spaces or quotes; `..` refused below
const repoPath = v => str(v) && REPO_PATH.test(v) && !v.split('/').includes('..')

if (!str(a.run) || !/^runs\/[0-9]{8}-[a-z0-9][a-z0-9-]*$/.test(a.run)) errors.push('args.run must look like runs/20261017-short-name')
if (!str(a.base) || !/^[A-Za-z0-9._/~^-]+$/.test(a.base)) errors.push('args.base must be a commit (a hash or a ref, no spaces)')
if (!ENGINES.includes(a.code_engine)) errors.push(`args.code_engine must be one of ${ENGINES.join(', ')}`)
const tests = Array.isArray(a.tests) ? a.tests : []
if (!tests.length) errors.push('args.tests must list at least one {id, engine, brief, test_cmd}')
const ids = new Set()
tests.forEach((t, i) => {
  const at = `args.tests[${i}]`
  if (!t || typeof t !== 'object') { errors.push(`${at} is not an object`); return }
  if (!str(t.id) || !ID.test(t.id)) errors.push(`${at}: id must be lower-case letters, digits and dashes`)
  else if (ids.has(t.id)) errors.push(`${at}: id ${t.id} is used twice`)
  else ids.add(t.id)
  if (!ENGINES.includes(t.engine)) errors.push(`${at}: engine must be one of ${ENGINES.join(', ')}`)
  else if (t.engine === a.code_engine) errors.push(`${at}: engine ${t.engine} wrote the code; a test brief must run on another engine`)
  if (!repoPath(t.brief)) errors.push(`${at}: brief must be a file path inside the repo`)
  if (!str(t.test_cmd)) errors.push(`${at}: test_cmd is missing`)
})
const review = a.review && typeof a.review === 'object' ? a.review : null
if (!review) errors.push('args.review must be {engine, brief}')
else {
  if (!ENGINES.includes(review.engine)) errors.push(`args.review: engine must be one of ${ENGINES.join(', ')}`)
  else if (review.engine === a.code_engine) errors.push(`args.review: engine ${review.engine} wrote the code; the review must run on another engine`)
  else if (!REVIEW_ENGINES.includes(review.engine)) errors.push(`args.review: engine must be ${REVIEW_ENGINES.join(' or ')} (the only read-only commands in the design)`)
  if (!repoPath(review.brief)) errors.push('args.review: brief must be a file path inside the repo')
}
if (errors.length) return { status: 'error', errors }

const RUN = a.run
const NODES = `${RUN}/nodes`
const PROGRESS = `${NODES}/crossed-build-check.progress.md`

const COMMON = label => `
You are one step (${label}) of the crossed-build-check workflow in this repository; its root is your working folder.
Run folder: ${RUN}/. Another session also commits in this working tree: never \`git add\`, never commit, never
\`git stash\`, and change no file except the ones this step names.

1. First run \`bun .claude/skills/workflow-design/guard/src/cli.ts deadline status\`. If it prints "time is up" (exit 1),
   return at once with time_up true and every other field empty ("", 0, false or []), and do nothing else. Otherwise
   (exit 0, or exit 2 when no deadline is recorded) go on with time_up false.
2. Append one line to ${PROGRESS} with a shell \`echo ... >>\`:
   \`- <output of date -Iseconds> · ${label} · start · <short note>\`
   and one more when you finish, with \`done\` or \`fail\` in place of \`start\`.
3. Run each long command with the Bash tool's timeout set to 600000 ms. Report what the commands printed and returned,
   not what you expect them to.
`

const ask = brief => `"Read ${brief} and do what it says."`
const resultFile = (engine, id) => `${NODES}/${id}.${engine === 'codex' ? 'last.txt' : 'result.md'}`
function engineCommand(engine, brief, out, readOnly) {
  if (engine === 'opencode') return `opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent build --variant high ${ask(brief)} </dev/null > ${out}`
  if (engine === 'codex') return `codex exec -m gpt-6.1-sol -c model_reasoning_effort=medium -s ${readOnly ? 'read-only' : 'workspace-write'} --skip-git-repo-check -o ${out} ${ask(brief)} </dev/null`
  if (engine === 'dsh') return `dsh headless ${ask(brief)} </dev/null > ${out}`
  return `claude -p --model claude-opus-5-5 ${ask(brief)} </dev/null > ${out}`
}

const s = type => ({ type })
const strings = { type: 'array', items: { type: 'string' } }
const object = properties => ({ type: 'object', properties, required: Object.keys(properties) })
const WRITE_SCHEMA = object({ time_up: s('boolean'), id: s('string'), exit: s('integer'), result_file: s('string'), status: { type: 'string', enum: ['written', 'failed', ''] }, test_files: strings, problem: s('string') })
const BASE_SCHEMA = object({ time_up: s('boolean'), id: s('string'), failed_on_base: strings, passed_on_base: strings, output_file: s('string'), problem: s('string') })
const HEAD_SCHEMA = object({ time_up: s('boolean'), id: s('string'), pass: s('boolean'), failing: strings, output_file: s('string') })
const REVIEW_SCHEMA = object({ time_up: s('boolean'), file: s('string'), findings_count: s('integer') })

let stopped = false
const problems = []
// Every step goes through here: after a step returns time_up, no further step starts.
async function step(prompt, opts) {
  if (stopped) return null
  const r = await agent(prompt, opts)
  if (!r) problems.push(`${opts.label}: the agent returned nothing`)
  else if (r.time_up === true) stopped = true
  return r
}
const usable = r => !!r && r.time_up !== true

const NAMES = 'Name each test as the test runner prints it (file and test name), the same way in every list.'

function writeStep(t) {
  const out = resultFile(t.engine, t.id)
  return step(`${COMMON(`write:${t.id}`)}
Step: have ${t.engine} write the tests that ${t.brief} asks for. First read ${t.brief}: if it has no line starting
"## Lessons" (the node-brief template's Lessons section, the text of \`lessons for\`, or "none"), do not run anything;
return status "failed" with problem "the brief has no Lessons section". Otherwise run exactly this command from the
repository root:

    timeout 580 ${engineCommand(t.engine, t.brief, out, false)}

Record its exit code; result_file is ${out}. Do not write or change any test yourself.
Then list the test files the engine wrote, relative to the repository root: read ${t.brief} for the files it asks for,
read ${out}, and check that each file exists. status is "written" when the exit code is 0 and at least one of those
files exists; otherwise "failed", with the reason in problem. Return id "${t.id}".`,
  { label: `write:${t.id}`, phase: 'Write tests', schema: WRITE_SCHEMA, ...CHEAP })
}

function failFirstStep(t, w) {
  const out = `${NODES}/${t.id}.base.txt`
  return step(`${COMMON(`failfirst:${t.id}`)}
Step: show that the new tests of brief ${t.id} fail on the base commit ${a.base}, before the build.
The new test files: ${w.test_files.join(', ')}.

1. \`dir=$(mktemp -d /tmp/crossed-${t.id}-XXXXXX)\` and \`git worktree add --detach "$dir" ${a.base}\`.
2. Copy into "$dir", at the same relative paths, only those new test files (create parent folders as needed).
3. From "$dir", with a 580-second limit, run the brief's test command and save all its output to
   ${out} in the main repository (use its absolute path):

       ${t.test_cmd}

4. Always remove the worktree at the end, even when a step failed: \`git worktree remove --force "$dir"\`.
   Check with \`git worktree list\` that it is gone.

failed_on_base: every new test that failed or errored there. passed_on_base: every new test that passed there.
${NAMES} If the run broke for a reason that is not the new tests (a missing dependency of the worktree, a bad
command), say so in problem. output_file is ${out}. Return id "${t.id}".`,
  { label: `failfirst:${t.id}`, phase: 'Fail first', schema: BASE_SCHEMA })
}

function headStep(t) {
  const out = `${NODES}/${t.id}.head.txt`
  return step(`${COMMON(`head:${t.id}`)}
Step: run brief ${t.id}'s tests on the current code. From the repository root, with a 580-second limit, run this
command and save all its output to ${out}:

    ${t.test_cmd}

pass is true only when the command exits 0. failing: every test that failed or errored. ${NAMES}
output_file is ${out}. Return id "${t.id}".`,
  { label: `head:${t.id}`, phase: 'Head', schema: HEAD_SCHEMA, ...CHEAP })
}

function runReview() {
  const out = resultFile(review.engine, 'review')
  return step(`${COMMON('review')}
Step: a read-only review on ${review.engine}. Run exactly this command from the repository root:

    timeout 580 ${engineCommand(review.engine, review.brief, out, true)}

file is ${out}, where the engine's final message is saved. findings_count is the number of findings in that file:
count them the way ${review.brief} asks them to be listed; if it does not say, count the top-level list items under a
heading named Findings. Change no file other than ${out} and the progress file.`,
  { label: 'review', phase: 'Review', schema: REVIEW_SCHEMA, ...CHEAP })
}

// One brief's chain: write, then fail first, then head. A brief whose tests were not written stops after the write.
const chain = [
  (_prev, t) => writeStep(t).then(w => ({ t, w })),
  async x => {
    if (!usable(x.w)) return x
    if (x.w.status !== 'written' || !(x.w.test_files || []).length) {
      problems.push(`${x.t.id}: the engine wrote no tests (status ${x.w.status || 'none'}, exit ${x.w.exit}${x.w.problem ? `: ${x.w.problem}` : ''})`)
      return x
    }
    return { ...x, f: await failFirstStep(x.t, x.w) }
  },
  async x => (usable(x.w) && x.w.status === 'written' && usable(x.f) ? { ...x, h: await headStep(x.t) } : x),
]

const others = tests.filter(t => t.engine !== 'opencode')
const oc = tests.filter(t => t.engine === 'opencode')
const lanes = [
  () => pipeline(others, ...chain),
  async () => { // opencode briefs one after another: never two opencode runs at once
    const done = []
    for (const t of oc) {
      let x = null
      for (const stage of chain) x = await stage(x, t)
      done.push(x)
    }
    return done
  },
]
const laneResults = await parallel(lanes)
const results = laneResults.filter(Boolean).flat().filter(Boolean)

const tests_written = [], failed_first = [], passed_on_base = [], failing_on_head = []
for (const x of results) {
  const id = x.t.id
  if (usable(x.w) && x.w.status === 'written') tests_written.push({ id, test_files: x.w.test_files })
  if (usable(x.f)) {
    // A test that passed on base is reported as passed_on_base, never as failing first, even when also listed as failed.
    const passed = new Set(x.f.passed_on_base || [])
    for (const test of passed) passed_on_base.push({ id, test })
    for (const test of x.f.failed_on_base || []) if (!passed.has(test)) failed_first.push({ id, test })
    if (x.f.problem) problems.push(`${id} fail first: ${x.f.problem}`)
  }
  if (usable(x.h)) for (const test of x.h.failing || []) failing_on_head.push({ id, test })
}

const rv = await runReview()
const out = {
  tests_written, failed_first, passed_on_base, failing_on_head,
  review_file: usable(rv) ? rv.file : '',
  findings_count: usable(rv) ? rv.findings_count : null,
  problems,
}
if (stopped) out.stopped = 'time is up'
return out
