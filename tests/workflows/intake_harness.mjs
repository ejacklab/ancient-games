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

const NO_BLUEPRINT = { task_kind: 'not a product change', reason: 'a question about the repo', map: '', sections: [] }
const READY = { state_file: `${RUN}/state.md`, readiness_file: `${RUN}/readiness.md`, tools_checked: 1, missing: [], blueprint: NO_BLUEPRINT }
const VERDICT_OK = { check_file: `${RUN}/check.md`, items: ['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8'].map(id => ({ id, pass: true, note: 'read' })) }
const step = (id, extra) => ({ id, action: `do ${id}`, clear: true, check: `pytest -q -k ${id}`, check_kind: 'script', ...extra })

const ALGO_SMALL = { algorithm_file: `${RUN}/algorithm.md`, steps: [step('s1'), step('s2')], unclear_spots: [], risk: 'low', risk_reason: 'easy to undo' }
const ALGO_BIG = {
  algorithm_file: `${RUN}/algorithm.md`,
  steps: [step('s1'), step('s2'), step('s3', { clear: false, check: '', check_kind: 'none' }), step('s4'), step('s5')],
  unclear_spots: [
    { id: 'u1', what: 'format unknown', kind: 'information', blueprint_section: '', blocks: ['s3'], depends_on: [] },
    { id: 'u2', what: 'which option', kind: 'decision', blueprint_section: '', blocks: ['s5'], depends_on: [], question: 'A or B?', assumption: 'A' },
  ],
  risk: 'low', risk_reason: 'easy to undo',
}
const PROMPT_OK = { output_file: `${RUN}/prompt.md`, task: 'do it', steps: ['one', 'two'], check: 'pytest -q', check_kind: 'script', independent_check: '', acceptance_criteria: [], must_not_change: 'anything outside README.md', questions_for_ej: [] }

const piece = (id, extra) => ({
  id, name: id, steps: ['a', 'b'], over_three_reason: '', pattern: 'step', resolves_spot: '', builds: false, blueprint_sections: [], acceptance_criteria: [],
  check: 'pytest -q', check_kind: 'script',
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
  questions_for_ej: [{ spot: 'u2', question: 'A or B?', assumption: 'A', must_answer: false }],
  acceptance_criteria: [],
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
const DECISION = { id: 'u1', what: 'which wording', kind: 'decision', blueprint_section: '', blocks: ['s2'], depends_on: [], question: 'A or B?', assumption: 'A' }
{
  const a = clone(ALGO_SMALL); a.unclear_spots = [DECISION]
  const p = { ...PROMPT_OK, questions_for_ej: [{ spot: 'u1', question: 'A or B?', assumption: 'A', must_answer: false }] }
  const { result } = await runCase({ ...base, '2-': a, '4-': p })
  expect('2 steps + a decision with a default -> small, question comes out', result.status === 'verified' && result.size === 'small' && result.questions_for_ej.length === 1, JSON.stringify(result))
}
{
  const a = clone(ALGO_SMALL); a.unclear_spots = [DECISION]
  const { result } = await runCase({ ...base, '2-': a, '4-': PROMPT_OK })
  expect('sabotage: small task whose prompt drops the decision -> named', result.status === 'unverified' && named(result, 'u1: a decision must appear'), JSON.stringify(result.failed_items))
}
{
  const a = clone(ALGO_SMALL); a.unclear_spots = [{ id: 'u1', what: 'format unknown', kind: 'information', blueprint_section: '', blocks: ['s2'], depends_on: [] }]
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
  expect('verifier omits V8 -> unverified', result.status === 'unverified' && named(result, 'V8: the verifier did not report it'), JSON.stringify(result.failed_items))
}

// ---- Blueprint check (method 3.1): a product change needs a fixed target, and the run ends at its criteria ----

const sec = (section, status, needed = true) => ({ section, needed, status, file: status === 'missing' ? '' : `docs/blueprint/${section}.md` })
const BP_FEATURE = {
  task_kind: 'feature', reason: 'adds an export', map: 'docs/blueprint/README.md',
  sections: [sec('vision', 'settled'), sec('requirements', 'draft'), sec('data model', 'missing'), sec('ui/ux', 'settled', false)],
}
const READY_FEATURE = { ...READY, blueprint: BP_FEATURE }
const B_REQ = { id: 'b1', what: 'R1 export is only a draft', kind: 'decision', blueprint_section: 'requirements', blocks: ['s4'], depends_on: [], question: 'Accept 02-requirements.md R1 as written?', assumption: 'accepted as written' }
const B_DATA = { id: 'b2', what: 'no data model', kind: 'information', blueprint_section: 'data model', blocks: ['s3'], depends_on: [] }
const ALGO_FEATURE = {
  algorithm_file: `${RUN}/algorithm.md`,
  steps: [step('s1'), step('s2'), step('s3', { clear: false, check: '', check_kind: 'none' }), step('s4'), step('s5')],
  unclear_spots: [B_REQ, B_DATA], risk: 'low', risk_reason: 'easy to undo',
}
const BUILD_STOP = c => `${c} passes, the baseline still passes, nothing off limits changed`
const DESIGN_FEATURE = {
  output_file: `${RUN}/workflow-design.md`,
  pieces: [
    piece('p1', { resolves_spot: 'b2', check: 'EJ accepts 06-data-model.md', check_kind: 'ej', blueprint_sections: ['requirements'] }),
    piece('p2', { builds: true, blueprint_sections: ['requirements', 'data model'], acceptance_criteria: ['R1.1'], needs: ['p1'], stop: BUILD_STOP('R1.1') }),
    piece('p3', { builds: true, blueprint_sections: ['requirements'], acceptance_criteria: ['R1.2'], needs: ['p2'], stop: BUILD_STOP('R1.2') }),
  ],
  order: ['p1', 'p2', 'p3'], joins: [], parallel_candidates: [],
  questions_for_ej: [{ spot: 'b1', question: B_REQ.question, assumption: B_REQ.assumption, must_answer: true }],
  acceptance_criteria: ['R1.1', 'R1.2'],
  agent_count: 5, cost_estimate: '200k tokens, guessed', success_criteria: 'R1.1 and R1.2 pass',
}
const feature = { ...base, '1-': READY_FEATURE, '2-': ALGO_FEATURE }
const mutateF = fn => { const d = clone(DESIGN_FEATURE); fn(d); return d }
{
  const { result, calls } = await runCase({ ...feature, '4-': DESIGN_FEATURE })
  expect('feature with a draft and a missing section -> verified design, 4 agents', result.status === 'verified' && result.size === 'design' && calls.length === 4, JSON.stringify(result))
  expect('feature -> not-settled sections and criteria come out', result.blueprint.not_settled.length === 2 && result.acceptance_criteria.length === 2, JSON.stringify(result))
  expect('feature -> the design prompt says what a piece that builds must name', calls.some(c => c.label.startsWith('4-design') && c.prompt.includes('acceptance criteria it covers')), 'blueprint rules not in the design prompt')
}

// Readiness sabotage: the blueprint report itself must hang together; bounded at two readiness attempts.
const readySabotage = [
  ['a feature that does not need the requirements', b => { b.sections = b.sections.filter(x => x.section !== 'requirements') }, 'a feature needs the requirements section'],
  ['a fix that does not need the requirements', b => { b.task_kind = 'fix'; b.sections = [sec('data model', 'settled')] }, 'a fix needs the requirements section'],
  ['a new product that skips a section', b => { b.task_kind = 'new product' }, 'a new product needs the architecture section'],
  ['not a product change, but a section is needed', b => { b.task_kind = 'not a product change' }, 'needs no sections'],
  ['a settled section with no file', b => { b.sections[0].file = '' }, 'vision is settled but names no file'],
  ['a section listed twice', b => { b.sections.push(sec('vision', 'draft')) }, 'vision is listed twice'],
  ['no reason for the kind of task', b => { b.reason = '' }, 'no reason is given'],
]
for (const [name, fn, text] of readySabotage) {
  const b = clone(BP_FEATURE); fn(b)
  const { result, calls } = await runCase({ ...feature, '1-': { ...READY, blueprint: b } })
  expect(`sabotage readiness: ${name} -> stops at step 1, named, 2 agents`, result.status === 'unverified' && result.step === 1 && named(result, text) && calls.length === 2, JSON.stringify(result))
}
{ // readiness repair: the failed item reaches attempt 2
  const b = clone(BP_FEATURE); b.reason = ''
  const { result, calls } = await runCase({ ...feature, '1-': [{ ...READY, blueprint: b }, READY_FEATURE], '4-': DESIGN_FEATURE })
  const second = calls.find(c => c.label === '1-readiness#2')
  expect('readiness repair: bad then good -> verified', result.status === 'verified', JSON.stringify(result))
  expect('readiness repair: the failed item is fed back', !!second && second.prompt.includes('no reason is given'), 'feedback text not in the prompt')
  expect('readiness repair: attempt 2 keeps the baseline and does not recreate files', !!second && second.prompt.includes('Do not take a new baseline') && !second.prompt.includes('Create runs/'), 'repair prompt still recreates the files')
}

// Algorithm sabotage: every needed, unsettled section becomes the right kind of spot.
const algoSabotage = [
  ['a draft section with no spot', a => { a.unclear_spots = [B_DATA] }, 'requirements is draft: it needs an unclear spot of kind decision'],
  ['a missing section asked as a decision', a => { a.unclear_spots = [B_REQ, { ...B_DATA, kind: 'decision', question: 'Q?', assumption: 'A' }] }, 'data model is missing: it needs an unclear spot of kind information'],
  ['a spot about a settled section', a => { a.unclear_spots.push({ ...B_REQ, id: 'b3', blueprint_section: 'vision' }) }, 'b3: vision is not a needed, unsettled blueprint section'],
]
{ // an incomplete section (it does not cover the task) must be drafted, not just accepted
  const bp = clone(BP_FEATURE); bp.sections[1].status = 'incomplete'
  const { result } = await runCase({ ...feature, '1-': { ...READY, blueprint: bp }, '2-': ALGO_FEATURE })
  expect('sabotage algorithm: an incomplete section asked as a decision -> named', result.status === 'unverified' && result.step === 2 && named(result, 'requirements is incomplete: it needs an unclear spot of kind information'), JSON.stringify(result))
}
for (const [name, fn, text] of algoSabotage) {
  const a = clone(ALGO_FEATURE); fn(a)
  const { result } = await runCase({ ...feature, '2-': a })
  expect(`sabotage algorithm: ${name} -> stops at step 2, named`, result.status === 'unverified' && result.step === 2 && named(result, text), JSON.stringify(result))
}

// Design sabotage: pieces that build stop at their criteria and wait for their sections.
const designSabotage = [
  ['no acceptance criteria in scope', d => { d.acceptance_criteria = [] }, 'a product change must list the acceptance criteria in scope'],
  ['a piece that builds with no criteria', d => { d.pieces[2].acceptance_criteria = [] }, 'p3: it builds but names no acceptance criteria'],
  ['a piece criterion outside the scope', d => { d.pieces[2].acceptance_criteria = ['R9.9'] }, 'p3: criterion R9.9 is not in the design'],
  ['a criterion no piece covers', d => { d.acceptance_criteria.push('R1.3') }, 'criterion R1.3: no piece that builds covers it'],
  ['a piece that builds with no sections', d => { d.pieces[2].blueprint_sections = [] }, 'p3: it builds but names no blueprint section'],
  ['a piece that builds on a section not marked needed', d => { d.pieces[2].blueprint_sections = ['ui/ux'] }, 'p3: it depends on the ui/ux section, which readiness did not mark as needed'],
  ['building on a missing section without its drafter', d => { d.pieces[1].needs = [] }, 'p2: it builds on the missing data model section but does not need the piece that drafts it'],
  ['a drafted section settled by a script, not EJ', d => { d.pieces[0].check_kind = 'script' }, 'p1: it drafts a blueprint section'],
  ['a blueprint question answerable by silence', d => { d.questions_for_ej[0].must_answer = false }, 'b1: a blueprint question must be marked must_answer'],
  ['a builder whose stop is an open-ended review', d => { d.pieces[1].stop = 'the reviewer finds nothing more to improve' }, 'p2: its stop condition does not name criterion R1.1'],
  ['a judged builder check that is not the criteria', d => { Object.assign(d.pieces[1], { pattern: 'loop', attempt_limit: 9, feedback: 'the review', exit_on_limit: 'to EJ', check_kind: 'judged', check: 'a reviewer tries to reject it' }) }, 'p2: a judged check must be a checklist of its criteria'],
  ['success criteria that do not name a criterion', d => { d.success_criteria = 'reviewer satisfied' }, 'the success criteria do not name criterion R1.1'],
  ['a product change where no piece builds', d => { d.pieces[1].builds = false; d.pieces[2].builds = false }, 'criterion R1.1: no piece that builds covers it'],
]
for (const [name, fn, text] of designSabotage) {
  const { result, calls } = await runCase({ ...feature, '4-': mutateF(fn) })
  expect(`sabotage design: ${name} -> unverified and named, 5 agents`, result.status === 'unverified' && named(result, text) && calls.length === 5, JSON.stringify(result.failed_items))
}
{ // a piece that builds in a task that is not a product change
  const d = mutate(x => { x.pieces[1].builds = true })
  const { result } = await runCase({ ...base, '2-': ALGO_BIG, '4-': d })
  expect('sabotage design: building in a task that is not a product change -> named', named(result, 'p2: it builds, but readiness says the task is not a product change'), JSON.stringify(result.failed_items))
}
{ // acceptance criteria in a task that is not a product change
  const d = mutate(x => { x.acceptance_criteria = ['R1.1'] })
  const r1 = await runCase({ ...base, '2-': ALGO_BIG, '4-': d })
  expect('sabotage design: criteria in a task that is not a product change -> named', named(r1.result, 'not a product change, so it has no acceptance criteria'), JSON.stringify(r1.result.failed_items))
  const r2 = await runCase({ ...base, '2-': ALGO_SMALL, '4-': { ...PROMPT_OK, acceptance_criteria: ['R1.1'], check: 'R1.1 passes' } })
  expect('sabotage prompt: criteria in a task that is not a product change -> named', named(r2.result, 'not a product change, so it has no acceptance criteria'), JSON.stringify(r2.result.failed_items))
}
{ // an incomplete section is drafted by a blueprint piece that every builder on it needs
  const bp = clone(BP_FEATURE); bp.sections[1].status = 'incomplete'
  const a = clone(ALGO_FEATURE); a.unclear_spots = [{ ...B_DATA }, { id: 'b1', what: 'no requirement for the export', kind: 'information', blueprint_section: 'requirements', blocks: ['s4'], depends_on: [] }]
  const d = mutateF(x => {
    x.pieces.unshift(piece('p0', { resolves_spot: 'b1', check: 'EJ accepts the new R1 block in 02-requirements.md', check_kind: 'ej' }))
    x.pieces[1].needs = ['p0']; x.pieces[2].needs = ['p0', 'p1']; x.order = ['p0', 'p1', 'p2', 'p3']; x.questions_for_ej = []
  })
  const r1 = await runCase({ ...feature, '1-': { ...READY, blueprint: bp }, '2-': a, '4-': d })
  expect('incomplete requirements drafted by a blueprint piece -> verified design', r1.result.status === 'verified' && r1.result.size === 'design', JSON.stringify(r1.result))
  const r2 = await runCase({ ...feature, '1-': { ...READY, blueprint: bp }, '2-': a, '4-': mutateF(x => {
    x.pieces.unshift(piece('p0', { resolves_spot: 'b1', check: 'EJ accepts', check_kind: 'ej' })); x.pieces[1].needs = ['p0']; x.pieces[2].needs = []
    x.order = ['p0', 'p1', 'p2', 'p3']; x.questions_for_ej = []
  }) })
  expect('sabotage design: building on an incomplete section without its drafter -> named', named(r2.result, 'p2: it builds on the incomplete requirements section but does not need the piece that drafts it'), JSON.stringify(r2.result.failed_items))
}

// Size with a blueprint: a draft section alone keeps a task small; a missing one never does.
{
  const a = clone(ALGO_SMALL); a.unclear_spots = [{ ...B_REQ, blocks: ['s2'] }]
  const bp = { ...BP_FEATURE, sections: [sec('vision', 'settled'), sec('requirements', 'draft')] }
  const p = { ...PROMPT_OK, acceptance_criteria: ['R1.1'], check: 'pytest -q: R1.1 passes, the rest of the suite still passes', questions_for_ej: [{ spot: 'b1', question: B_REQ.question, assumption: B_REQ.assumption, must_answer: true }] }
  const r1 = await runCase({ ...base, '1-': { ...READY, blueprint: bp }, '2-': a, '4-': p })
  expect('2 steps + a draft requirement -> small, must-answer question comes out', r1.result.status === 'verified' && r1.result.size === 'small' && r1.result.questions_for_ej[0].must_answer === true, JSON.stringify(r1.result))
  const r2 = await runCase({ ...base, '1-': { ...READY, blueprint: bp }, '2-': a, '4-': { ...p, questions_for_ej: [{ ...p.questions_for_ej[0], must_answer: false }] } })
  expect('sabotage prompt: blueprint question answerable by silence -> named', r2.result.status === 'unverified' && named(r2.result, 'b1: a blueprint question must be marked must_answer'), JSON.stringify(r2.result.failed_items))
  const r3 = await runCase({ ...base, '1-': { ...READY, blueprint: bp }, '2-': a, '4-': { ...p, acceptance_criteria: [] } })
  expect('sabotage prompt: product change with no criteria -> named', r3.result.status === 'unverified' && named(r3.result, 'must name the acceptance criteria'), JSON.stringify(r3.result.failed_items))
  const r4 = await runCase({ ...base, '1-': { ...READY, blueprint: bp }, '2-': a, '4-': { ...p, check: 'pytest -q' } })
  expect('sabotage prompt: a check that does not name its criterion -> named', r4.result.status === 'unverified' && named(r4.result, 'the check does not name criterion R1.1'), JSON.stringify(r4.result.failed_items))
}
{
  const a = clone(ALGO_SMALL); a.unclear_spots = [{ ...B_DATA, blocks: ['s2'] }]
  const bp = { ...BP_FEATURE, sections: [sec('vision', 'settled'), sec('requirements', 'settled'), sec('data model', 'missing')] }
  const d = { ...DESIGN_FEATURE, questions_for_ej: [] }
  const { result } = await runCase({ ...base, '1-': { ...READY, blueprint: bp }, '2-': a, '4-': d })
  expect('2 steps + a missing section -> design, not small', result.size === 'design' && result.status === 'verified', JSON.stringify(result))
}
{
  const a = clone(ALGO_SMALL); a.unclear_spots = [{ ...B_DATA, blocks: ['s2'] }]
  const bp = { ...BP_FEATURE, sections: [sec('vision', 'settled'), sec('requirements', 'settled'), sec('data model', 'incomplete')] }
  const { result } = await runCase({ ...base, '1-': { ...READY, blueprint: bp }, '2-': a, '4-': { ...DESIGN_FEATURE, questions_for_ej: [] } })
  expect('2 steps + an incomplete section -> design, not small', result.size === 'design' && result.status === 'verified', JSON.stringify(result))
}

// ---- Round 2 of the review: criteria ids, who needs the drafter, exits, the kind of task ----

const designSabotage2 = [
  ['a criterion that is not an id', d => { d.acceptance_criteria.push(''); d.success_criteria += ' ' }, 'criterion "" is not an id'],
  ['a prose criterion', d => { d.pieces[2].acceptance_criteria = ['nothing more to improve'] }, 'p3: criterion "nothing more to improve" is not an id'],
  ['a builder covering R1.1 without the requirements section', d => { d.pieces[1].blueprint_sections = ['data model'] }, 'p2: it covers R1.1 but does not list the requirements section'],
  ['a piece that does not build carrying criteria', d => { d.pieces.push(piece('p4', { acceptance_criteria: ['R1.1'] })); d.order.push('p4') }, 'p4: only a piece that builds, or a blueprint piece proposing them'],
  ['a piece that does not build on a missing section, without its drafter', d => { d.pieces.push(piece('p4', { blueprint_sections: ['data model'] })); d.order.push('p4') }, 'p4: it depends on the missing data model section but does not need the piece that drafts it'],
  ['a loop whose exit is another round', d => { Object.assign(d.pieces[1], { pattern: 'loop', attempt_limit: 3, feedback: 'the test output', exit_on_limit: 'start a fresh review round' }) }, 'p2: when the limit is hit it goes back to the unclear list or to EJ'],
]
for (const [name, fn, text] of designSabotage2) {
  const { result } = await runCase({ ...feature, '4-': mutateF(fn) })
  expect(`sabotage design: ${name} -> unverified and named`, result.status === 'unverified' && named(result, text), JSON.stringify(result.failed_items))
}
{ // a builder must need the blueprint piece that proposes its criterion
  const bp = clone(BP_FEATURE); bp.sections[1].status = 'incomplete'
  const a = clone(ALGO_FEATURE); a.unclear_spots = [{ ...B_DATA }, { id: 'b1', what: 'no requirement for the export', kind: 'information', blueprint_section: 'requirements', blocks: ['s4'], depends_on: [] }]
  const d = mutateF(x => {
    x.pieces.unshift(piece('p0', { resolves_spot: 'b1', check: 'EJ accepts the new R1 block', check_kind: 'ej', acceptance_criteria: ['R1.1', 'R1.2'] }))
    x.pieces[1].needs = ['p0']; x.pieces[2].blueprint_sections = ['requirements']; x.pieces[2].needs = ['p1']
    x.order = ['p0', 'p1', 'p2', 'p3']; x.questions_for_ej = []
  })
  const ok = await runCase({ ...feature, '1-': { ...READY, blueprint: bp }, '2-': a, '4-': d })
  expect('a blueprint piece proposing the criteria, needed by the builders -> verified', ok.result.status === 'verified', JSON.stringify(ok.result))
  const bad = clone(d); bad.pieces[2].needs = []; bad.pieces[2].blueprint_sections = ['data model', 'requirements']; bad.pieces[2].needs = ['p1']; bad.pieces[1].needs = []
  const r = await runCase({ ...feature, '1-': { ...READY, blueprint: bp }, '2-': a, '4-': bad })
  expect('sabotage design: a builder that does not need the piece proposing its criterion -> named', named(r.result, 'which it does not need') || named(r.result, 'does not need the piece that drafts it'), JSON.stringify(r.result.failed_items))
}
{ // one unclear spot per unsettled section
  const a = clone(ALGO_FEATURE); a.unclear_spots.push({ ...B_REQ, id: 'b3' })
  const { result } = await runCase({ ...feature, '2-': a })
  expect('sabotage algorithm: two spots on one section -> named', result.step === 2 && named(result, 'requirements has more than one unclear spot'), JSON.stringify(result))
}
{ // a fix the requirements do not describe is a feature
  const b = clone(BP_FEATURE); b.task_kind = 'fix'; b.sections[1].status = 'incomplete'
  const { result, calls } = await runCase({ ...feature, '1-': { ...READY, blueprint: b } })
  expect('sabotage readiness: a fix the requirements do not describe -> stops at step 1', result.step === 1 && named(result, 'so the task is a feature') && calls.length === 2, JSON.stringify(result))
}
{ // a prompt file with no off-limits
  const { result } = await runCase({ ...base, '2-': ALGO_SMALL, '4-': { ...PROMPT_OK, must_not_change: '' } })
  expect('sabotage prompt: nothing said about what is off limits -> named', named(result, 'prompt: it does not say what is off limits'), JSON.stringify(result.failed_items))
}
{ // the verifier finds the kind of task wrong: stop at step 1, do not spend the repair on step 4
  const v = clone(VERDICT_OK); v.items[7] = { id: 'V8', pass: false, note: 'the challenge adds a CSV export: a feature' }
  const { result, calls } = await runCase({ ...base, '2-': ALGO_SMALL, '4-': PROMPT_OK, '5-': v })
  expect('verifier fails V8 -> stops at step 1, 4 agents, no step-4 repair', result.status === 'unverified' && result.step === 1 && named(result, 'a feature') && calls.length === 4, JSON.stringify(result))
}

console.log(failures ? `\n${failures} FAILED` : '\nall passed')
process.exit(failures ? 1 : 0)
