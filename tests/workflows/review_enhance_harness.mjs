// Offline harness for .claude/workflows/review-enhance.js. No agents run and no tokens are spent: `agent` and the
// nested `workflow` are stubs that answer by label. Each check runs on the script, then on a planted copy that
// breaks exactly that check; it must pass on the first and fail on the second.
// Run from the repository root:  node tests/workflows/review_enhance_harness.mjs

import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const here = dirname(fileURLToPath(import.meta.url))
const SRC = readFileSync(join(here, '../../.claude/workflows/review-enhance.js'), 'utf8').replace('export const meta', 'const meta')
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor
const clone = x => JSON.parse(JSON.stringify(x))

function load(plant = []) {
  let src = SRC
  for (const [from, to] of plant) {
    const n = src.split(from).length - 1
    if (n !== 1) throw new Error(`plant anchor found ${n} times: ${from}`)
    src = src.replace(from, to)
  }
  return new AsyncFunction('agent', 'phase', 'log', 'args', 'parallel', 'workflow', src)
}
const parallel = thunks => Promise.all(thunks.map(t => Promise.resolve().then(t).catch(() => null)))

const RUN = 'runs/20261017-harness'
const ARGS = { run: RUN, rounds: 3, tool: 'memory_check', extra_paths: ['tools/memory_index.py'], test_cmd: 'cd memory_check && bun test',
  review_brief: `${RUN}/briefs/review.md`, fix_template: `${RUN}/briefs/fix-template.md`, enhance_question: `${RUN}/enhance-question.md` }
const F = id => ({ id, requirement: 'C2', summary: 's', input: 'i' })

const DEFAULTS = {
  readiness: () => ({ time_up: false, pass: true, summary: 'ok' }),
  review: label => ({ time_up: false, engine: label.split('-')[2], file: `${RUN}/review/${label}.md`, usable: true, redone_by_step: false, problem: '' }),
  judge: label => ({ time_up: false, file: `${RUN}/findings-${label.split('-')[1]}.md`, accepted: [F(`R${label.split('-')[1].slice(1)}-1`)], dropped: 0 }),
  reproduce: label => ({ time_up: false, test_file: `memory_check/test/${label}.test.ts`, reproduced: ['x'], not_reproduced: [], red_file: '' }),
  fix: () => ({ time_up: false, exit: 0, status: 'done', result_file: 'r', problem: '' }),
  verify: () => ({ time_up: false, pass: true, failing: [], summary: 'ok' }),
  pick: () => ({ time_up: false, file: `${RUN}/enhance.md`, picks: [F('E-1')] }),
  report: () => ({ time_up: false, file: `${RUN}/report.md` }),
}

async function runCase(wf, args, over = {}) {
  const labels = [], nested = []
  const agent = async (prompt, o) => {
    labels.push(o.label)
    if (o.label in over) return clone(typeof over[o.label] === 'function' ? over[o.label]() : over[o.label])
    const kind = o.label.split('-')[0]
    if (!DEFAULTS[kind]) throw new Error(`no canned answer for ${o.label}`)
    return DEFAULTS[kind](o.label)
  }
  const workflow = async (name, a) => { nested.push({ name, a }); return { status: 'done' } }
  const out = await wf(agent, () => {}, () => {}, clone(args), parallel, workflow)
  return { out, labels, nested }
}

const checks = []
const check = (name, fn, plant) => checks.push({ name, fn, plant })

check('bad args are refused before any agent runs', async wf => {
  const { out, labels } = await runCase(wf, { ...ARGS, rounds: 0 })
  return out.status === 'refused' && labels.length === 0
}, [["a.rounds < 1) errors.push", "a.rounds < -1) errors.push"]])

check('the round limit holds: judge always accepts, exactly `rounds` judge steps', async wf => {
  const { labels } = await runCase(wf, ARGS)
  return labels.filter(l => l.startsWith('judge-')).length === 3
}, [['round <= a.rounds &&', 'round <= a.rounds + 1 &&']])

check('a dry round stops the loop and skips reproduce, then enhance still runs', async wf => {
  const { labels, nested } = await runCase(wf, ARGS, { 'judge-r1': { time_up: false, file: 'f', accepted: [], dropped: 2 } })
  return !labels.some(l => l.startsWith('reproduce-r')) && !labels.includes('judge-r2') && nested.length === 1 && labels.includes('pick')
}, [["log(`round ${round}: nothing accepted — the review is dry`); break }", "log(`round ${round}: nothing accepted — the review is dry`) }"]])

check('a finding that does not reproduce gets no fix', async wf => {
  const { labels } = await runCase(wf, { ...ARGS, rounds: 1 }, { 'reproduce-r1': { time_up: false, test_file: 't', reproduced: [], not_reproduced: ['R1-1'], red_file: '' } })
  return !labels.includes('fix-r1')
}, [["if (!usable(rp) || !(rp.reproduced || []).length) return", "if (!usable(rp)) return"]])

check('a failed verify gets exactly one more fix and verify', async wf => {
  const { labels } = await runCase(wf, { ...ARGS, rounds: 1 }, { 'verify-r1': { time_up: false, pass: false, failing: ['t'], summary: 'red' } })
  return labels.includes('fix-r1b') && labels.includes('verify-r1b') && !labels.includes('fix-r1bb')
}, [['if (usable(vf) && !vf.pass) {', 'if (false) {']])

check('time up stops every later step, and the report is not written', async wf => {
  const { out, labels } = await runCase(wf, ARGS, { 'judge-r1': { time_up: true, file: '', accepted: [], dropped: 0 } })
  return out.stopped === 'time is up' && !labels.some(l => l.startsWith('reproduce') || l === 'report' || l === 'pick')
}, [['  if (stopped) return null\n  const r = await agent', '  const r = await agent']])

check('no usable review ends the rounds with a problem', async wf => {
  const { out, labels } = await runCase(wf, ARGS, { 'review-r1-codex': null, 'review-r1-agy': null })
  return !labels.includes('judge-r1') && out.problems.some(p => p.includes('no review came back'))
}, [["if (!reviews.length) { problems.push(`round ${round}: no review came back`); break }", "if (false) {}"]])

check('a judge that returns nothing is retried once, then the rounds stop with a problem and nothing is fixed or enhanced', async wf => {
  let calls = 0
  const { out, labels, nested } = await runCase(wf, ARGS, { 'judge-r1': () => { calls++; return null } })
  return calls === 2 && !labels.some(l => l.startsWith('reproduce') || l.startsWith('fix')) && nested.length === 0
    && out.problems.some(p => p.includes('the judge returned nothing twice'))
}, [['if (!stopped && !judgeFailed) {', 'if (!stopped) {']])

let failed = 0
for (const c of checks) {
  const real = await c.fn(load()).catch(e => { console.log(`  error: ${e.message}`); return false })
  const planted = await c.fn(load(c.plant)).catch(() => false)
  const ok = real === true && planted === false
  if (!ok) failed++
  console.log(`${ok ? 'ok  ' : 'FAIL'} ${c.name}${ok ? '' : ` (real ${real}, planted ${planted})`}`)
}
console.log(failed ? `${failed} failed` : 'all passed')
process.exit(failed ? 1 : 0)
