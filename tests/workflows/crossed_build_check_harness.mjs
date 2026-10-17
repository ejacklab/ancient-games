// Offline harness for .claude/workflows/crossed-build-check.js. No agents run and no tokens are spent: `agent` is a
// stub that returns canned answers by label, after a short delay so that overlaps and ordering are real.
// Each check is run on the script, then on a planted copy of the script that breaks exactly that check (a text
// replacement); the check must pass on the first and fail on the second, so it is shown able to fail.
// Run from the repository root:  node tests/workflows/crossed_build_check_harness.mjs

import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const here = dirname(fileURLToPath(import.meta.url))
const SRC = readFileSync(join(here, '../../.claude/workflows/crossed-build-check.js'), 'utf8').replace('export const meta', 'const meta')
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor
const clone = x => JSON.parse(JSON.stringify(x))
const sleep = ms => new Promise(r => setTimeout(r, ms))

// A planted copy: each [from, to] must occur exactly once, so a plant can never be a silent no-op.
function load(plant = []) {
  let src = SRC
  for (const [from, to] of plant) {
    const n = src.split(from).length - 1
    if (n !== 1) throw new Error(`plant anchor found ${n} times: ${from}`)
    src = src.replace(from, to)
  }
  return new AsyncFunction('agent', 'phase', 'log', 'args', 'parallel', 'pipeline', src)
}

const parallel = thunks => Promise.all(thunks.map(t => Promise.resolve().then(t).catch(() => null)))
const pipeline = (items, ...stages) => Promise.all(items.map(async (item, i) => {
  let prev = item
  try { for (const stage of stages) prev = await stage(prev, item, i) } catch { return null }
  return prev
}))

const RUN = 'runs/20261017-harness'
const T = (id, engine) => ({ id, engine, brief: `${RUN}/briefs/${id}.md`, test_cmd: `bun test tests/${id}.test.ts` })
const ARGS = { run: RUN, base: 'abc1234', code_engine: 'claude', tests: [T('c1', 'codex'), T('d1', 'dsh')], review: { engine: 'codex', brief: `${RUN}/briefs/review.md` } }
const withArgs = fn => { const x = clone(ARGS); fn(x); return x }

const DEFAULTS = {
  write: id => ({ time_up: false, id, exit: 0, result_file: `${RUN}/nodes/${id}.result.md`, status: 'written', test_files: [`tests/${id}.test.ts`], problem: '' }),
  failfirst: id => ({ time_up: false, id, failed_on_base: [`${id} > new case`], passed_on_base: [], output_file: `${RUN}/nodes/${id}.base.txt`, problem: '' }),
  head: id => ({ time_up: false, id, pass: true, failing: [], output_file: `${RUN}/nodes/${id}.head.txt` }),
  review: () => ({ time_up: false, file: `${RUN}/nodes/review.last.txt`, findings_count: 2 }),
}
const TIME_UP = { time_up: true, id: '', exit: 0, result_file: '', status: '', test_files: [], problem: '' }

// over: label -> canned answer (replaces the default); delay: label -> ms (default 5).
async function runCase(wf, args, { over = {}, delay = {} } = {}) {
  const calls = [], events = []
  const agent = async (prompt, o) => {
    calls.push({ label: o.label, prompt })
    events.push({ label: o.label, kind: 'start' })
    await sleep(delay[o.label] ?? 5)
    events.push({ label: o.label, kind: 'end' })
    if (o.label in over) return clone(over[o.label])
    const [kind, id] = o.label.split(':')
    if (!DEFAULTS[kind]) throw new Error(`no canned answer for ${o.label}`)
    return DEFAULTS[kind](id)
  }
  const result = await wf(agent, () => {}, () => {}, args, parallel, pipeline)
  return { result, calls, events }
}

// A check returns '' when it holds, or what went wrong.
async function holds(check, wf) {
  try { return await check(wf) } catch (e) { return `threw: ${e.message}` }
}

let failures = 0
const report = (name, ok, detail) => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok ? '' : ` -- ${detail}`}`); if (!ok) failures++ }
const REAL = load()
async function check(name, fn, plant) {
  const onReal = await holds(fn, REAL)
  report(name, onReal === '', onReal)
  const onPlant = await holds(fn, load(plant))
  report(`${name} -- the plant is caught${onPlant ? ` (${onPlant.slice(0, 110)})` : ''}`, onPlant !== '', 'the check passed on the planted copy')
}
const refusedBeforeAgents = (r, text) => r.result.status !== 'error' ? `not an error: ${JSON.stringify(r.result)}`
  : r.calls.length ? `${r.calls.length} agents ran` : text && !r.result.errors.some(e => e.includes(text)) ? `no error names "${text}": ${JSON.stringify(r.result.errors)}` : ''

// 1. A missing arg stops before any agent.
await check('missing args -> error, no agents', async wf => {
  for (const args of [undefined, {}, withArgs(x => { delete x.review }), withArgs(x => { x.tests = [] }), withArgs(x => { delete x.tests[1].test_cmd }), withArgs(x => { delete x.base })]) {
    const bad = refusedBeforeAgents(await runCase(wf, args))
    if (bad) return `${JSON.stringify(args)}: ${bad}`
  }
  return ''
}, [["if (errors.length) return { status: 'error', errors }", "if (false) return { status: 'error', errors }"]])

// 2. A brief on the code's own engine is refused; so is an engine outside the four.
await check('a test brief on the code engine is refused', async wf =>
  refusedBeforeAgents(await runCase(wf, withArgs(x => { x.tests[1].engine = 'claude' })), 'wrote the code'),
[['else if (t.engine === a.code_engine)', 'else if (false)']])
await check('a review brief on the code engine is refused', async wf =>
  refusedBeforeAgents(await runCase(wf, withArgs(x => { x.code_engine = 'codex'; x.tests[0].engine = 'opencode' })), 'the review must run on another engine'),
[['else if (review.engine === a.code_engine)', 'else if (false)']])
await check('an engine outside opencode, codex, dsh, claude is refused', async wf =>
  refusedBeforeAgents(await runCase(wf, withArgs(x => { x.tests[0].engine = 'agy' })), 'engine must be one of'),
[["const ENGINES = ['opencode', 'codex', 'dsh', 'claude']", "const ENGINES = ['opencode', 'codex', 'dsh', 'claude', 'agy']"]])

// 3. Two opencode briefs never overlap (the others still run).
await check('two opencode briefs never overlap', async wf => {
  const args = withArgs(x => { x.tests = [T('o1', 'opencode'), T('c1', 'codex'), T('o2', 'opencode')] })
  const { result, events } = await runCase(wf, args, { delay: { 'write:o1': 20, 'write:o2': 20 } })
  let active = 0, most = 0
  for (const e of events) if (/^write:o/.test(e.label)) { active += e.kind === 'start' ? 1 : -1; most = Math.max(most, active) }
  if (most > 1) return `${most} opencode writes at once`
  const written = result.tests_written.map(x => x.id).sort().join(',')
  return written === 'c1,o1,o2' ? '' : `written: ${written}`
}, [["const others = tests.filter(t => t.engine !== 'opencode')", 'const others = tests'], ["const oc = tests.filter(t => t.engine === 'opencode')", 'const oc = []']])

// 4. A test that passes on base is passed_on_base, never failing first — even when the step also lists it as failed.
await check('a test passing on base is reported as passed_on_base, not failed_first', async wf => {
  const over = { 'failfirst:c1': { ...DEFAULTS.failfirst('c1'), failed_on_base: ['c1 > a', 'c1 > b'], passed_on_base: ['c1 > b'] } }
  const { result } = await runCase(wf, ARGS, { over })
  const ff = result.failed_first.filter(x => x.id === 'c1').map(x => x.test).join(',')
  const pb = result.passed_on_base.map(x => `${x.id}:${x.test}`).join(',')
  return ff === 'c1 > a' && pb === 'c1:c1 > b' ? '' : `failed_first c1: ${ff}; passed_on_base: ${pb}`
}, [['if (!passed.has(test)) failed_first.push', 'failed_first.push']])

// 5. A time_up step stops the rest: nothing starts after it returns.
await check('a time_up step stops the rest', async wf => {
  const seq = await runCase(wf, withArgs(x => { x.tests = [T('o1', 'opencode'), T('o2', 'opencode')] }), { over: { 'write:o1': TIME_UP } })
  if (seq.result.stopped !== 'time is up') return `opencode: not stopped: ${JSON.stringify(seq.result)}`
  if (seq.calls.map(c => c.label).join(',') !== 'write:o1') return `opencode: agents after time up: ${seq.calls.map(c => c.label).join(',')}`
  const par = await runCase(wf, withArgs(x => { x.tests = [T('c1', 'codex'), T('c2', 'codex')] }), { over: { 'write:c1': TIME_UP }, delay: { 'write:c1': 5, 'write:c2': 30 } })
  const at = par.events.findIndex(e => e.label === 'write:c1' && e.kind === 'end')
  const late = par.events.slice(at + 1).filter(e => e.kind === 'start').map(e => e.label)
  if (late.length) return `parallel: started after time up: ${late.join(',')}`
  return par.result.stopped === 'time is up' && par.result.review_file === '' ? '' : `parallel: ${JSON.stringify(par.result)}`
}, [['if (stopped) return null', 'if (false) return null']])

// 6. Review starts after every test step has ended.
await check('review starts after every test step', async wf => {
  const args = withArgs(x => { x.tests = [T('c1', 'codex'), T('d1', 'dsh'), T('o1', 'opencode')] })
  const { result, events } = await runCase(wf, args, { delay: { 'write:c1': 10, 'head:d1': 25, 'failfirst:o1': 15 } })
  const reviewAt = events.findIndex(e => e.label === 'review' && e.kind === 'start')
  if (reviewAt < 0) return 'review never started'
  const lastTestEnd = events.map((e, i) => (e.label !== 'review' && e.kind === 'end' ? i : -1)).reduce((m, i) => Math.max(m, i), -1)
  if (reviewAt < lastTestEnd) return `review started at event ${reviewAt}, a test step ended at ${lastTestEnd}`
  const steps = events.filter(e => e.kind === 'start' && e.label !== 'review').length
  return steps === 9 && result.review_file && result.findings_count === 2 ? '' : `${steps} test steps; ${JSON.stringify(result)}`
}, [['const laneResults = await parallel(lanes)', 'const early = runReview(); const laneResults = await parallel(lanes); await early']])

// The good path: the return carries every field, Fail first gets the written files, and the brief engine's command.
{
  const { result, calls } = await runCase(REAL, ARGS)
  const keys = ['tests_written', 'failed_first', 'passed_on_base', 'failing_on_head', 'review_file', 'findings_count']
  report('good run -> every return field, 7 agents, not stopped', keys.every(k => k in result) && calls.length === 7 && !result.stopped && result.failed_first.length === 2 && !result.problems.length, JSON.stringify(result))
  const ff = calls.find(c => c.label === 'failfirst:c1').prompt
  report('fail first is told the new files, the base commit and to remove its worktree', ff.includes('tests/c1.test.ts') && ff.includes('git worktree add --detach "$dir" abc1234') && ff.includes('git worktree remove --force'), ff)
  const w = calls.find(c => c.label === 'write:c1').prompt
  report('write runs the engine with </dev/null and a 580 s limit', w.includes('timeout 580 codex exec') && w.includes('</dev/null') && w.includes('-s workspace-write'), w)
  const rv = calls.find(c => c.label === 'review').prompt
  report('review runs read-only', rv.includes('-s read-only') && !rv.includes('workspace-write'), rv)
}
{ // a brief whose engine wrote nothing: no fail first or head for it, and the problem is reported
  const { result, calls } = await runCase(REAL, ARGS, { over: { 'write:d1': { ...DEFAULTS.write('d1'), exit: 1, status: 'failed', test_files: [], problem: 'engine error' } } })
  report('an engine that wrote no tests -> no later steps for it, problem named', !calls.some(c => c.label === 'failfirst:d1' || c.label === 'head:d1') && result.problems.some(p => p.includes('d1: the engine wrote no tests')), JSON.stringify(result))
}

console.log(failures ? `\n${failures} FAILED` : '\nall passed')
process.exit(failures ? 1 : 0)
