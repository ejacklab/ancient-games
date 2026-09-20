// Offline harness for .claude/workflows/intake.js. No agents run and no tokens are spent: `agent` is a stub
// that returns canned answers by label. It checks the scheduling and the script's objective checks, and the
// sabotage cases show that each check can fail.
// Run from the repository root:  node tests/workflows/intake_harness.mjs

import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const here = dirname(fileURLToPath(import.meta.url))
const src = readFileSync(join(here, '../../.claude/workflows/intake.js'), 'utf8').replace('export const meta', 'const meta')
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor
const workflow = new AsyncFunction('agent', 'phase', 'log', 'args', src)

const RUN = 'runs/20260920-harness'
const ARGS = { challenge: 'harness challenge', runId: '20260920-harness' }
const clone = x => JSON.parse(JSON.stringify(x))

const READY = { state_file: `${RUN}/state.md`, readiness_file: `${RUN}/readiness.md`, tools_checked: 1, missing: [] }
const VERDICT_OK = { check_file: `${RUN}/check.md`, items: ['V1', 'V2', 'V3', 'V4', 'V5', 'V6'].map(id => ({ id, pass: true, note: 'read' })) }
const step = (id, extra) => ({ id, action: `do ${id}`, clear: true, check: `pytest -q -k ${id}`, check_kind: 'script', ...extra })

const ALGO_SMALL = { algorithm_file: `${RUN}/algorithm.md`, steps: [step('s1'), step('s2')], unclear_spots: [], risk: 'low', risk_reason: 'easy to undo' }
const ALGO_BIG = {
  algorithm_file: `${RUN}/algorithm.md`,
  steps: [step('s1'), step('s2'), step('s3', { clear: false, check: '', check_kind: 'none' }), step('s4'), step('s5')],
  unclear_spots: [
    { id: 'u1', what: 'format unknown', kind: 'information', blocks: ['s3'], depends_on: [] },
    { id: 'u2', what: 'which option', kind: 'decision', blocks: ['s5'], depends_on: [], question: 'A or B?', assumption: 'A' },
  ],
  risk: 'low', risk_reason: 'easy to undo',
}
const PROMPT_OK = { output_file: `${RUN}/prompt.md`, task: 'do it', steps: ['one', 'two'], check: 'pytest -q', check_kind: 'script', independent_check: '', questions_for_ej: [] }

const piece = (id, extra) => ({
  id, name: id, steps: ['a', 'b'], over_three_reason: '', pattern: 'step', resolves_spot: '', check: 'pytest -q', check_kind: 'script',
  attempt_limit: 1, feedback: '', exit_on_limit: '', needs: [], files_touched: [`${id}.py`], brief_given: 'algorithm.md', brief_withheld: '',
  intent: 'why', stop: 'the check passes', returns: `${id}-result.md with Findings`, must_not_change: 'anything outside the run folder',
  evidence: 'pytest output', evidence_file: `${id}-evidence.txt`, state_reads: 'the step table', state_writes: 'status and output file', ...extra,
})
const DESIGN_OK = {
  output_file: `${RUN}/workflow-design.md`,
  pieces: [
    piece('p1', { resolves_spot: 'u1' }),
    piece('p2', { pattern: 'loop', attempt_limit: 2, feedback: 'pytest output', exit_on_limit: 'back to the unclear list', needs: ['p1'] }),
    piece('p3', { needs: ['p2'] }),
  ],
  order: ['p1', 'p2', 'p3'], joins: [], parallel_candidates: [],
  questions_for_ej: [{ spot: 'u2', question: 'A or B?', assumption: 'A' }],
  agent_count: 5, cost_estimate: '200k tokens, guessed', success_criteria: 'all checks pass',
}
const mutate = fn => { const d = clone(DESIGN_OK); fn(d); return d }

// A scenario maps a label prefix to a canned answer, or to a list of answers used one per call.
async function runCase(scenario, args = ARGS) {
  const calls = [], counts = {}
  const agent = async (prompt, o) => {
    calls.push({ label: o.label, prompt })
    const key = Object.keys(scenario).find(k => o.label.startsWith(k))
    if (!key) throw new Error(`no canned answer for ${o.label}`)
    const v = scenario[key]
    if (!Array.isArray(v)) return clone(v)
    counts[key] = (counts[key] || 0) + 1
    return clone(v[Math.min(counts[key], v.length) - 1])
  }
  const result = await workflow(agent, () => {}, () => {}, args)
  return { result, calls }
}

let failures = 0
const expect = (name, ok, detail) => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok ? '' : ` -- ${detail}`}`); if (!ok) failures++ }
const named = (r, text) => (r.failed_items || []).some(x => x.includes(text))
const base = { '1-': READY, '5-': VERDICT_OK }

{ // no args: stops before any agent
  const { result, calls } = await runCase({}, {})
  expect('missing args -> error, no agents', result.status === 'error' && calls.length === 0, JSON.stringify(result))
}
{
  const { result, calls } = await runCase({ ...base, '2-': ALGO_SMALL, '4-': PROMPT_OK })
  expect('good small task -> verified small, 4 agents', result.status === 'verified' && result.size === 'small' && calls.length === 4, JSON.stringify(result))
}
{
  const { result, calls } = await runCase({ ...base, '2-': ALGO_BIG, '4-': DESIGN_OK })
  expect('good design -> verified design, 4 agents', result.status === 'verified' && result.size === 'design' && calls.length === 4, JSON.stringify(result))
  expect('good design -> the question for EJ comes out', result.questions_for_ej.length === 1, JSON.stringify(result.questions_for_ej))
}

// Sabotage: each broken design must fail, and the failed item must be named.
const sabotage = [
  ['a piece with no check', d => { d.pieces[2].check = '' }, 'p3: it names no check'],
  ['a loop with no attempt limit', d => { d.pieces[1].attempt_limit = 0 }, 'p2: a loop needs an attempt limit'],
  ['a loop with no exit', d => { d.pieces[1].exit_on_limit = '' }, 'p2: a loop needs an exit'],
  ['a 5-step piece with no reason', d => { d.pieces[0].steps = ['a', 'b', 'c', 'd', 'e'] }, 'p1: 5 steps and no reason'],
  ['a cycle in needs', d => { d.pieces[0].needs = ['p3'] }, 'needs contains a cycle'],
  ['an order that runs a piece before what it needs', d => { d.order = ['p2', 'p1', 'p3'] }, 'p2 runs before p1'],
  ['an unclear spot nobody resolves', d => { d.pieces[0].resolves_spot = '' }, 'u1: no piece resolves it'],
  ['a decision missing from the questions for EJ', d => { d.questions_for_ej = [] }, 'u2: a decision must appear'],
  ['a parallel candidate where a point is false', d => { d.parallel_candidates = [{ pieces: ['p1', 'p3'], no_result_needed: true, no_shared_resources: true, no_method_change: false, own_checks: true, worth_the_join: true }] }, 'not all five points hold'],
  ['a parallel candidate linked by needs', d => { d.parallel_candidates = [{ pieces: ['p1', 'p3'], no_result_needed: true, no_shared_resources: true, no_method_change: true, own_checks: true, worth_the_join: true }] }, 'p1 and p3 are linked by needs'],
  ['no cost estimate', d => { d.cost_estimate = '' }, 'the cost estimate is missing'],
  ['a contract with no intent', d => { d.pieces[0].intent = '' }, 'p1: the contract has no intent'],
  ['a contract with no stop condition', d => { d.pieces[0].stop = ' ' }, 'p1: the contract has no stop condition'],
  ['a contract that does not say what comes back', d => { d.pieces[1].returns = '' }, 'p2: the contract does not say what the piece returns'],
  ['a contract with no off-limits', d => { d.pieces[1].must_not_change = '' }, 'p2: the contract does not say what must not change'],
  ['a piece with no evidence', d => { d.pieces[2].evidence = '' }, 'p3: it names no evidence'],
  ['evidence with nowhere to be saved', d => { d.pieces[2].evidence_file = '' }, 'p3: it does not say where the evidence is saved'],
  ['a piece that reads no state', d => { d.pieces[0].state_reads = '' }, 'p1: it does not say what it reads from the state file'],
  ['a piece that writes no state', d => { d.pieces[0].state_writes = '' }, 'p1: it does not say what it writes to the state file'],
]
for (const [name, fn, text] of sabotage) {
  const { result, calls } = await runCase({ ...base, '2-': ALGO_BIG, '4-': mutate(fn) })
  expect(`sabotage: ${name} -> unverified and named`, result.status === 'unverified' && named(result, text), JSON.stringify(result.failed_items))
  expect(`sabotage: ${name} -> bounded at 5 agents, verifier skipped on attempt 1`, calls.length === 5 && !calls.some(c => c.label === '5-verify#1'), calls.map(c => c.label).join(','))
}
{ // parallel candidate sharing a file
  const d = mutate(x => { x.pieces.push(piece('p4', { files_touched: ['p1.py'] })); x.order.push('p4'); x.parallel_candidates = [{ pieces: ['p1', 'p4'], no_result_needed: true, no_shared_resources: true, no_method_change: true, own_checks: true, worth_the_join: true }] })
  const { result } = await runCase({ ...base, '2-': ALGO_BIG, '4-': d })
  expect('sabotage: parallel candidate sharing a file -> named', named(result, 'both touch p1.py'), JSON.stringify(result.failed_items))
}
{ // repair: bad first, good second; the failed item must reach the second prompt
  const bad = mutate(d => { d.pieces[2].check = '' })
  const { result, calls } = await runCase({ ...base, '2-': ALGO_BIG, '4-': [bad, DESIGN_OK] })
  const second = calls.find(c => c.label === '4-design#2')
  expect('repair: bad then good -> verified', result.status === 'verified', JSON.stringify(result))
  expect('repair: the failed item is fed back to attempt 2', !!second && second.prompt.includes('p3: it names no check'), 'feedback text not in the prompt')
}
{ // algorithm sabotage: an unclear step that no spot blocks
  const a = clone(ALGO_BIG); a.unclear_spots = a.unclear_spots.filter(s => s.id !== 'u1')
  const { result, calls } = await runCase({ ...base, '2-': a })
  expect('sabotage: unclear step with no spot -> stops at step 2', result.status === 'unverified' && result.step === 2 && named(result, 's3') && calls.length === 3, JSON.stringify(result))
}
{ // small but risky needs an independent check
  const a = clone(ALGO_SMALL); a.risk = 'high'; a.risk_reason = 'cannot be undone'
  const { result } = await runCase({ ...base, '2-': a, '4-': PROMPT_OK })
  expect('sabotage: risky small task with no independent check -> named', result.status === 'unverified' && named(result, 'no independent check'), JSON.stringify(result.failed_items))
}
// Size rule (a): a decision with a provisional assumption does not make a task big.
const DECISION = { id: 'u1', what: 'which wording', kind: 'decision', blocks: ['s2'], depends_on: [], question: 'A or B?', assumption: 'A' }
{
  const a = clone(ALGO_SMALL); a.unclear_spots = [DECISION]
  const p = { ...PROMPT_OK, questions_for_ej: [{ spot: 'u1', question: 'A or B?', assumption: 'A' }] }
  const { result } = await runCase({ ...base, '2-': a, '4-': p })
  expect('2 steps + a decision with a default -> small, question comes out', result.status === 'verified' && result.size === 'small' && result.questions_for_ej.length === 1, JSON.stringify(result))
}
{
  const a = clone(ALGO_SMALL); a.unclear_spots = [DECISION]
  const { result } = await runCase({ ...base, '2-': a, '4-': PROMPT_OK })
  expect('sabotage: small task whose prompt drops the decision -> named', result.status === 'unverified' && named(result, 'u1: a decision must appear'), JSON.stringify(result.failed_items))
}
{
  const a = clone(ALGO_SMALL); a.unclear_spots = [{ id: 'u1', what: 'format unknown', kind: 'information', blocks: ['s2'], depends_on: [] }]
  const d = mutate(x => { x.questions_for_ej = [] })
  const { result } = await runCase({ ...base, '2-': a, '4-': d })
  expect('2 steps + an information spot -> design, not small', result.size === 'design' && result.status === 'verified', JSON.stringify(result))
}
{ // more than 3 steps, nothing unclear -> still a design
  const a = clone(ALGO_SMALL); a.steps = [step('s1'), step('s2'), step('s3'), step('s4')]
  const d = mutate(x => { x.pieces[0].resolves_spot = ''; x.questions_for_ej = [] })
  const { result } = await runCase({ ...base, '2-': a, '4-': d })
  expect('4 clear steps -> design, not small', result.size === 'design' && result.status === 'verified', JSON.stringify(result))
}
{ // verifier fails one item
  const v = clone(VERDICT_OK); v.items[5] = { id: 'V6', pass: false, note: 'README.md modified' }
  const { result, calls } = await runCase({ ...base, '2-': ALGO_SMALL, '4-': PROMPT_OK, '5-': v })
  expect('verifier fails V6 -> unverified, named, 6 agents', result.status === 'unverified' && named(result, 'V6: README.md modified') && calls.length === 6, JSON.stringify(result))
}
{ // verifier drops an item
  const v = clone(VERDICT_OK); v.items.pop()
  const { result } = await runCase({ ...base, '2-': ALGO_SMALL, '4-': PROMPT_OK, '5-': v })
  expect('verifier omits V6 -> unverified', result.status === 'unverified' && named(result, 'V6: the verifier did not report it'), JSON.stringify(result.failed_items))
}

console.log(failures ? `\n${failures} FAILED` : '\nall passed')
process.exit(failures ? 1 : 0)
