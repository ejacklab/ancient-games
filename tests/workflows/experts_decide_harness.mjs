// Offline harness for .claude/workflows/experts-decide.js. No agents run and no tokens are spent: `agent` is a stub
// that returns canned answers by label, after a short delay so the parallel steps really overlap. Each case is also
// run against a planted copy of the script (one line changed) and must fail there, so every check is shown able to fail.
// Run from the repository root:  node tests/workflows/experts_decide_harness.mjs

import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const here = dirname(fileURLToPath(import.meta.url))
const SOURCE = readFileSync(join(here, '../../.claude/workflows/experts-decide.js'), 'utf8')
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor
const build = src => new AsyncFunction('agent', 'phase', 'log', 'args', 'parallel', 'pipeline', src.replace('export const meta', 'const meta'))

const RUN = 'runs/20261017-harness'
const ARGS = { run: RUN, question: `${RUN}/question.md`, out: 'q1' }
const IDS = ['linus', 'fan-li', 'sun-tzu', 'lao-tzu', 'dave', 'dario']
const clone = x => JSON.parse(JSON.stringify(x))
const ask = (sid, extra) => ({ time_up: false, sid, exit: 0, ok: true, answer_bytes: 1200, problem: '', ...extra })
const check = (sid, failures = []) => ({ time_up: false, sid, pass: failures.length === 0, failures })
const COMPARE = { time_up: false, file: `${RUN}/q1/compare.md`, agree: ['a'], disagree: ['b'], dissent: ['c'], questions: [{ question: 'q?', options: ['x', 'y'] }] }
const UP = { time_up: true }
const sidOf = label => label.split(' ')[1]
const defaults = label => {
  const kind = label.split(' ')[0]
  if (kind === 'ask' || kind === 'rerun') return ask(sidOf(label))
  if (kind === 'check' || kind === 'recheck') return check(sidOf(label))
  if (kind === 'compare') return COMPARE
  if (kind === 'research') return { time_up: false, file: `${RUN}/research/q1.md`, digest: 'found' }
  throw new Error(`no canned answer for ${label}`)
}

// answers: exact label -> answer, or a list used one per call. delays: label prefix -> ms.
async function runCase({ answers = {}, delays = {} } = {}, args = ARGS, src = SOURCE) {
  const calls = [], events = [], counts = {}
  const agent = async (prompt, o) => {
    calls.push({ label: o.label, prompt, opts: o })
    events.push(['start', o.label])
    const key = Object.keys(delays).find(k => o.label.startsWith(k))
    await new Promise(r => setTimeout(r, key ? delays[key] : 1))
    let v = answers[o.label]
    if (Array.isArray(v)) { counts[o.label] = (counts[o.label] || 0) + 1; v = v[Math.min(counts[o.label], v.length) - 1] }
    events.push(['end', o.label])
    return clone(v === undefined ? defaults(o.label) : v)
  }
  const parallel = thunks => Promise.all(thunks.map(t => t()))
  const pipeline = async () => { throw new Error('pipeline is not used by experts-decide') }
  const result = await build(src)(agent, () => {}, () => {}, args, parallel, pipeline)
  return { result, calls, events, labels: calls.map(c => c.label) }
}

let failures = 0
const expect = (name, ok, detail) => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok ? '' : ` -- ${detail}`}`); if (!ok) failures++ }
const plant = (from, to) => {
  if (!SOURCE.includes(from)) throw new Error(`plant does not apply: ${from}`)
  return SOURCE.replace(from, to)
}
// A case: a name, a run, a judge returning '' (holds) or what is wrong, and a planted script it must fail on.
async function testCase(name, run, judge, planted) {
  const why = judge(await run(SOURCE))
  expect(name, why === '', why)
  const whyPlanted = judge(await run(planted))
  expect(`  planted: ${name} -> fails`, whyPlanted !== '', 'the check passed on the planted script')
}
const at = (events, kind, label) => events.findIndex(([k, l]) => k === kind && l === label)
const lastEnd = (events, pred) => Math.max(-1, ...events.map(([k, l], i) => (k === 'end' && pred(l) ? i : -1)))

// 0. The plain run: every expert asked with its own subfolder and flags, checked, compared; done.
{
  const { result, calls, labels } = await runCase({}, { ...ARGS, insights: 'instruction,check', needsWeb: true })
  expect('plain run -> done, 13 agents, compare returned', result.status === 'done' && calls.length === 13 && result.compare.file === COMPARE.file, JSON.stringify({ status: result.status, labels }))
  const bad = []
  for (const sid of IDS) {
    const c = calls.find(x => x.label === `ask ${sid}`)
    if (!c) { bad.push(`no ask ${sid}`); continue }
    for (const part of [`--only ${sid} `, `--out ${RUN}/q1/${sid} `, `--question-file ${RUN}/question.md `, `--progress ${RUN}/nodes/q1.progress.md`, '--timeout 540 </dev/null', '--needs-web', 'timeout 590000 ms', 'deadline status'])
      if (!c.prompt.includes(part)) bad.push(`ask ${sid} lacks "${part}"`)
    if (c.prompt.includes('--insights') !== (sid === 'dave')) bad.push(`ask ${sid}: --insights only for dave`)
    if (c.opts.model !== 'claude-haiku-5-5' || c.opts.effort !== 'low') bad.push(`ask ${sid} not on haiku/low`)
  }
  const cmp = calls.find(x => x.label === 'compare')
  if (cmp.opts.model) bad.push('compare should use the session model')
  if (!cmp.opts.schema || cmp.opts.schema.type !== 'object') bad.push('compare has no object schema')
  expect('plain run -> commands carry each expert\'s flags; command steps on haiku', bad.length === 0, bad.join('; '))
  expect('plain run -> every expert usable, none rerun', result.experts.every(e => e.usable && !e.rerun), JSON.stringify(result.experts))
}

// 1. Missing args: an error, and no agent runs.
for (const missing of ['run', 'question', 'out']) {
  const a = { ...ARGS }; delete a[missing]
  await testCase(`missing args.${missing} -> error, no agents`, src => runCase({}, a, src),
    ({ result, calls }) => (result.status === 'error' && result.reason.includes(`args.${missing} is missing`) && calls.length === 0) ? '' : JSON.stringify({ result, n: calls.length }),
    plant(`if (!${missing === 'run' ? 'RUN' : missing === 'question' ? 'QUESTION' : 'OUT'}) return err(`, 'if (false) return err('))
}

// 2. A question path outside the repo, and an unknown expert id, are refused before any agent.
for (const q of ['/etc/passwd', '../other/q.md', 'runs/x/../../../q.md']) {
  await testCase(`question "${q}" outside the repo -> refused`, src => runCase({}, { ...ARGS, question: q }, src),
    ({ result, calls }) => (result.status === 'error' && result.reason.includes('relative path inside the repo') && calls.length === 0) ? '' : JSON.stringify({ result, n: calls.length }),
    plant(`QUESTION.startsWith('/') || QUESTION.split('/').includes('..')`, 'false'))
}
await testCase('unknown expert id -> refused, no agents', src => runCase({}, { ...ARGS, only: ['linus', 'bogus'] }, src),
  ({ result, calls }) => (result.status === 'error' && result.reason.includes('bogus') && calls.length === 0) ? '' : JSON.stringify({ result, n: calls.length }),
  plant('const unknown = ONLY.filter(s => !IDS.includes(s))', 'const unknown = []'))

// 3. A time_up step stops the rest: no agent starts after it returns, and the result says why.
const NO_STOP = plant('if (r && r.time_up) stopped = true', 'if (false) stopped = true')
const stoppedClean = label => ({ result, events }) => {
  const upEnd = at(events, 'end', label)
  const later = events.slice(upEnd + 1).filter(([k]) => k === 'start').map(([, l]) => l)
  return (upEnd >= 0 && result.status === 'stopped' && result.stopped === 'time is up' && later.length === 0) ? '' : JSON.stringify({ status: result.status, later })
}
await testCase('a time_up ask stops the rest', src => runCase({ answers: { 'ask linus': UP } }, ARGS, src), stoppedClean('ask linus'), NO_STOP)
await testCase('a time_up research stops before any ask', src => runCase({ answers: { research: UP } }, { ...ARGS, research: 'what is known?' }, src), stoppedClean('research'), NO_STOP)
await testCase('a time_up check of 老子 stops before compare', src => runCase({ answers: { 'check lao-tzu': UP } }, ARGS, src), stoppedClean('check lao-tzu'), NO_STOP)

// 4. 老子 never starts before the other Ask steps (reruns included) end.
await testCase('老子 starts only after every other ask and rerun ends', src => runCase({
  answers: { 'ask linus': ask('linus', { ok: false, problem: 'exit 1' }) },
  delays: { 'ask sun-tzu': 15, 'rerun linus': 10, 'ask dave': 8 },
}, ARGS, src), ({ events }) => {
  const laoStart = at(events, 'start', 'ask lao-tzu')
  const others = lastEnd(events, l => /^(ask|rerun) /.test(l) && sidOf(l) !== 'lao-tzu')
  return (laoStart > others && others >= 0) ? '' : `ask lao-tzu started at ${laoStart}, the last other ask/rerun ended at ${others}`
}, plant("const ALONE = 'lao-tzu'", "const ALONE = 'nobody'"))

// 5. An expert with no usable answer is rerun once, and only once; a usable one is never rerun.
const rerunOnce = sid => ({ result, labels }) => {
  const n = labels.filter(l => l === `rerun ${sid}`).length
  const others = labels.filter(l => l.startsWith('rerun ') && l !== `rerun ${sid}`)
  const e = result.experts.find(x => x.sid === sid)
  return (n === 1 && others.length === 0 && e.rerun && labels.includes(`recheck ${sid}`)) ? '' : JSON.stringify({ reruns: n, others, e })
}
const NEVER_RERUN = plant('if (stopped || usable(sid, r.ask, r.check)) return r', 'if (true) return r')
const RERUN_TWICE = plant('  r.recheck = await step(', "  r.rerun = await step(`rerun ${sid}`, askPrompt(sid, true), { phase: 'Ask', schema: ASK_SCHEMA, ...CMD_MODEL })\n  r.recheck = await step(")
const failsTwice = { answers: { 'ask fan-li': ask('fan-li', { ok: false, problem: 'timeout after 540 s' }), 'rerun fan-li': ask('fan-li', { ok: false, problem: 'timeout after 540 s' }), 'recheck fan-li': check('fan-li', ['fan-li: no answer file']) } }
await testCase('an expert failing twice -> rerun once, only once', src => runCase(failsTwice, ARGS, src), rerunOnce('fan-li'), NEVER_RERUN)
await testCase('an expert failing twice -> no second rerun',src => runCase(failsTwice, ARGS, src), rerunOnce('fan-li'), RERUN_TWICE)
{
  const { result } = await runCase(failsTwice)
  const e = result.experts.find(x => x.sid === 'fan-li')
  expect('an expert failing twice -> reported not usable, the run still compares', !e.usable && result.status === 'done' && result.agents.includes('compare'), JSON.stringify(e))
}
await testCase('a missing section with exit ok -> rerun once', src => runCase({ answers: { 'check dave': check('dave', ['dave: missing section ## Answer']) } }, ARGS, src), rerunOnce('dave'), NEVER_RERUN)
{
  const { labels } = await runCase({ answers: { 'check linus': check('linus', ['linus: cites #99, but its list has items 1–20']) } })
  expect('a check failing on a citation only -> no rerun (the answer is there)', !labels.some(l => l.startsWith('rerun ')), labels.join(', '))
}

// 6. Compare starts only after every check (rechecks included) ends, and runs once.
await testCase('compare starts after every check and recheck', src => runCase({
  answers: { 'ask lao-tzu': ask('lao-tzu', { ok: false, problem: 'database is locked' }) },
  delays: { 'recheck lao-tzu': 10, 'check dario': 12 },
}, ARGS, src), ({ events, labels }) => {
  const cmp = at(events, 'start', 'compare')
  const checks = lastEnd(events, l => /^(check|recheck) /.test(l))
  const n = labels.filter(l => l === 'compare').length
  return (n === 1 && cmp > checks && labels.includes('recheck lao-tzu')) ? '' : `compare x${n} started at ${cmp}, the last check ended at ${checks}`
}, plant('if (SIDS.includes(ALONE)) await expert(ALONE)', 'if (SIDS.includes(ALONE)) expert(ALONE)'))

// 7. only: a subset runs, 老子 left out runs no alone step; research changes the question file the experts get.
{
  const { result, labels } = await runCase({}, { ...ARGS, only: 'linus,dave' })
  expect('only linus,dave -> just those two asked', labels.filter(l => l.startsWith('ask ')).join(',') === 'ask linus,ask dave' && result.status === 'done', labels.join(', '))
  const r = await runCase({}, { ...ARGS, research: 'what is known?' })
  const askP = r.calls.find(c => c.label === 'ask linus').prompt
  expect('research -> runs first, experts asked from the question copy with findings', r.labels[0] === 'research' && askP.includes(`--question-file ${RUN}/research/q1.question.md`), r.labels.slice(0, 2).join(', '))
}

// 8. COO, after the review: every progress piece id is one word — `deadline status` reads a piece as one token (\S+),
// so a name with a space is skipped as a bad line and the step never shows as done.
{
  const pieces = [...SOURCE.matchAll(/progressLine\((['"`])(.*?)\1\)/g)].map(m => m[2])
  expect('every progress piece id has no space', pieces.length > 0 && pieces.every(p => !/\s/.test(p)), pieces.join(' | '))
  const planted = [...'progressLine(`check ${sid}`)'.matchAll(/progressLine\((['"`])(.*?)\1\)/g)].map(m => m[2])
  expect('sabotage: a piece id with a space is caught', planted.some(p => /\s/.test(p)), planted.join(' | '))
}

console.log(failures ? `\n${failures} FAILED` : '\nall passed')
process.exit(failures ? 1 : 0)
