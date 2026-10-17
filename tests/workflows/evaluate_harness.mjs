// Offline harness for .claude/workflows/evaluate-requirements.js. No agents run and no tokens are spent: `agent` is a
// stub that answers by label, and every runner's answer is a canned {exit_code, stdout_tail, stderr_tail}. It checks
// DATA.md's table after R1 — the label order and the two conditional groups (F6's repair round, F7's rerun with a
// second plant), the skip rules, the exact commands (F2, F8, F9, F18), the stops (F17's done:false and a runner that
// exits non-zero), the model each step runs on (EV-C6.1), the runId the run refuses (F12), the MEETS line it accepts
// (F19) and that the workflow never makes a verdict (EV-P1.3). The last case runs a deliberately broken copy of the
// script, so the checks above are shown to be able to fail.
// Run from the repository root:  node tests/workflows/evaluate_harness.mjs

import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const here = dirname(fileURLToPath(import.meta.url))
const SCRIPT = join(here, '../../.claude/workflows/evaluate-requirements.js')

const RUN_ID = '20261013-harness'
const RUN = `runs/${RUN_ID}`
const ARGS = { product: 'products/calc', spec: 'spec/calc', runId: RUN_ID }
const EXCLUDES = ['docs/*.md', 'build/**']
const ARGS_WITH_EXCLUDES = { ...ARGS, exclude: EXCLUDES }
const JUDGE_DIR = `/tmp/evaluator-judge-${RUN_ID}`
const clone = x => (x === null ? null : JSON.parse(JSON.stringify(x)))

// DATA.md's table after R1, in order: 30 labels, of which 9 are model steps. Two groups are conditional and the
// conditional order is a second case, so the happy path below is this table minus those two groups.
const ORDER = ['e0-start', 'e1-spec', 'e2-workspace', 'e3-classify', 'e3-check', 'e4-probes', 'e4-check', 'e5-view',
  'e5-mutants', 'e5-collect', 'e5-check', 'e6-matrix', 'e8-input', 'e8-confirm', 'e8-check',
  'e8-repair', 'e6-matrix-2', 'e8-input-2', 'e8-confirm-2', 'e8-check-2',
  'e9-input', 'e9-judge-1', 'e9-judge-2', 'e9-merge',
  'e9-input-2', 'e9-judge-1b', 'e9-judge-2b', 'e9-merge-2',
  'e10-verdict', 'e11-end']

const REPAIR = ['e8-repair', 'e6-matrix-2', 'e8-input-2', 'e8-confirm-2', 'e8-check-2']
const RERUN = ['e9-input-2', 'e9-judge-1b', 'e9-judge-2b', 'e9-merge-2']
const MODEL_STEPS = ['e3-classify', 'e4-probes', 'e8-confirm', 'e8-repair', 'e8-confirm-2',
  'e9-judge-1', 'e9-judge-2', 'e9-judge-1b', 'e9-judge-2b']
const RUNNERS = ORDER.filter(label => !MODEL_STEPS.includes(label))
const CHECKS = ['e3-check', 'e4-check', 'e5-check']
const JUDGES = ['e9-judge-1', 'e9-judge-2']
const MODEL_OF = { 'e3-classify': 'haiku' }
// Every runner is a haiku at low effort; of the model steps only classify is a haiku.
const modelFor = label => (RUNNERS.includes(label) ? 'haiku' : MODEL_OF[label] || 'sonnet')

const CMDS = {
  'e0-start': `python3 tools/evaluator/model_io.py stamp --run ${RUN} --event start`,
  'e1-spec': `python3 tools/evaluator/spec_parse.py --requirements ${ARGS.spec}/REQUIREMENTS.md --vision ${ARGS.spec}/VISION.md --out ${RUN}/requirements.json`,
  'e2-workspace': `python3 tools/evaluator/workspace.py --product ${ARGS.product} --spec ${ARGS.spec} --run ${RUN}`,
  'e3-check': `python3 tools/evaluator/model_io.py check-output --run ${RUN} --step classify`,
  'e4-check': `python3 tools/evaluator/model_io.py check-output --run ${RUN} --step probes`,
  'e5-view': `python3 tools/evaluator/model_io.py mutant-view --run ${RUN}`,
  'e5-collect': `python3 tools/evaluator/model_io.py mutant-view --run ${RUN} --collect`,
  'e5-check': `python3 tools/evaluator/model_io.py check-output --run ${RUN} --step mutants`,
  'e6-matrix': `python3 tools/evaluator/probe_matrix.py --run ${RUN}`,
  'e8-input': `python3 tools/evaluator/model_io.py confirm-input --run ${RUN}`,
  'e8-check': `python3 tools/evaluator/model_io.py confirm-check --run ${RUN}`,
  'e9-input': `python3 tools/evaluator/model_io.py judge-input --run ${RUN} --attempt 1`,
  'e9-merge': `python3 tools/evaluator/model_io.py judged-merge --run ${RUN}`,
  'e10-verdict': `python3 tools/evaluator/verdict.py --run ${RUN}`,
}

const ran = (stdout = '') => ({ exit_code: 0, stdout_tail: stdout, stderr_tail: '' })
const broke = (stderr = 'the command failed') => ({ exit_code: 1, stdout_tail: '', stderr_tail: stderr })
const WROTE = { done: true, note: 'written' }
const NOT_DONE = { done: false, note: 'ran out of what it could do' }
const checked = (voided, unfaithful) => ran(`2 checked, ${voided} voided, ${unfaithful} unfaithful`)

const HAPPY = {
  'e0-start': ran(), 'e1-spec': ran(), 'e2-workspace': ran(), 'e3-classify': WROTE, 'e3-check': ran(),
  'e4-probes': WROTE, 'e4-check': ran(), 'e5-view': ran(), 'e5-mutants': ran(), 'e5-collect': ran(),
  'e5-check': ran(), 'e6-matrix': ran(), 'e8-input': ran('2 to confirm'), 'e8-confirm': WROTE,
  'e8-check': checked(0, 0),
  'e9-input': ran(`3 to judge\nplant G2-F2`), 'e9-judge-1': WROTE, 'e9-judge-2': WROTE,
  'e9-merge': ran('plant_found: true'),
  'e10-verdict': ran(`wrote ${RUN}/verdict.json\nMEETS: yes run=${RUN_ID}\nPASS 3, FAIL 0, UNKNOWN 0`),
  'e11-end': ran(),
}

// The two conditional groups get answers for every label the new table makes them call: the repair round is five
// labels, and the rerun is four, of which only e9-input-2 runs when it prints "no other plant".
const REPAIR_ANSWERS = {
  'e8-repair': WROTE, 'e6-matrix-2': ran(), 'e8-input-2': ran('2 to confirm'),
  'e8-confirm-2': WROTE, 'e8-check-2': checked(0, 0),
}
const RERUN_ANSWERS = {
  'e9-input-2': ran('3 to judge\nplant G2-F3'), 'e9-judge-1b': WROTE,
  'e9-judge-2b': WROTE, 'e9-merge-2': ran('plant_found: true'),
}

// The happy path's labels in order: no probe was unfaithful and the plant was found, so neither group runs.
const HAPPY_ORDER = ORDER.filter(label => !REPAIR.includes(label) && !RERUN.includes(label))

// A scenario in which both conditional groups run, so the stop cases can walk every label in ORDER.
const EVERYTHING = {
  ...HAPPY, ...REPAIR_ANSWERS, ...RERUN_ANSWERS,
  'e8-check': checked(1, 1), 'e8-check-2': checked(0, 1),
  'e9-merge': ran('plant_found: false'),
}

const withGroup = (base, after, group) => {
  const at = base.indexOf(after)
  return [...base.slice(0, at + 1), ...group, ...base.slice(at + 1)]
}

const blockedAt = (result, label) => (result.status !== 'blocked' || result.step !== label)
  ? `came back ${JSON.stringify(result)}` : null

// --- loading the script under test --------------------------------------------------------------------------------------

let source
try {
  source = readFileSync(SCRIPT, 'utf8')
} catch (error) {
  console.log(`FAIL the workflow script cannot be read — ${SCRIPT} (${error.code || error.message})`)
  console.log('      This harness checks .claude/workflows/evaluate-requirements.js. Write the workflow, then run it again.')
  process.exit(1)
}
if (!source.includes('export const meta')) {
  console.log(`FAIL the workflow script is not a Workflow script — ${SCRIPT} has no \`export const meta\`.`)
  process.exit(1)
}

const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor
const build = text => new AsyncFunction('agent', 'phase', 'log', 'args', text.replace('export const meta', 'const meta'))
let workflow
try {
  workflow = build(source)
} catch (error) {
  console.log(`FAIL the workflow script does not parse — ${SCRIPT}: ${error.message}`)
  process.exit(1)
}

// --- running it with the stub ------------------------------------------------------------------------------------------

async function run(scenario, args = ARGS, script = workflow) {
  const calls = [], unasked = []
  const agent = async (prompt, o = {}) => {
    calls.push({ label: String(o.label), model: o.model, prompt: String(prompt) })
    const key = Object.keys(scenario).find(k => k === o.label)
    if (!key) unasked.push(String(o.label))
    return key ? clone(scenario[key]) : null
  }
  const result = await script(agent, () => {}, () => {}, args)
  if (unasked.length) {
    throw new Error(`the workflow called ${unasked.join(', ')}, which this scenario has no answer for: it ran a step the table does not put here`)
  }
  return { result, calls }
}

const promptOf = (calls, label) => (calls.find(c => c.label === label) || { prompt: '' }).prompt
const later = (calls, label) => calls.slice(ORDER.indexOf(label) + 1).map(c => c.label)
const calledOrder = calls => calls.map(c => c.label).join(' ')
const wanted = list => `      wanted: ${list.join(' ')}`

// A prompt carries the command when the whole command is there and nothing runs straight on from it, so that
// "--run runs/<runId>" does not pass for "--run runs/<runId>/matrix".
const carries = (prompt, cmd) => {
  const at = prompt.indexOf(cmd)
  if (at < 0) return false
  const before = at === 0 ? '' : prompt[at - 1]
  const after = prompt[at + cmd.length] || ''
  return !/[A-Za-z0-9_/]/.test(before) && !/[A-Za-z0-9_/]/.test(after)
}

// A flag may be written "--step classify" or "--step=classify"; DATA.md fixes the meaning, not the spacing.
const hasFlag = (prompt, flag, value) => new RegExp(`${flag}([ =]${value})\\b`).test(prompt)

// A value that is safe unquoted is passed as it is; anything else is single-quoted, so it reaches the shell as one
// argument. This is the workflow's own rule, written once here so the case can say what it wanted.
const shellArgument = value => /^[A-Za-z0-9_./-]+$/.test(value) ? value : `'${value.replaceAll("'", "'\\''")}'`

// --- the cases ----------------------------------------------------------------------------------------------------------

async function happyPath(script) {
  const { result, calls } = await run(HAPPY, ARGS, script)
  const order = calledOrder(calls)
  if (order !== HAPPY_ORDER.join(' ')) {
    return `the labels were called in this order: ${order}\n${wanted(HAPPY_ORDER)}\n      DATA.md runs no repair round (e8-check said 0 unfaithful) and no judge rerun (plant_found: true)`
  }
  if (result.status !== 'done') return `status ${JSON.stringify(result.status)}, reason ${JSON.stringify(result.reason)}`
  if (result.meets !== true) return `meets is ${JSON.stringify(result.meets)}, but e10-verdict printed "MEETS: yes run=${RUN_ID}"`
  if (result.runId !== RUN_ID) return `runId is ${JSON.stringify(result.runId)}`
  if (result.verdict !== `${RUN}/verdict.md`) return `verdict is ${JSON.stringify(result.verdict)}`
  if (result.authoritative !== `${RUN}/verdict.json`) return `authoritative is ${JSON.stringify(result.authoritative)}`
  if (result.agents !== calls.length) return `agents is ${result.agents}, and the stub was called ${calls.length} times`
  return true
}

async function meetsFalse(script) {
  const { result } = await run({ ...HAPPY, 'e10-verdict': ran(`MEETS: no run=${RUN_ID}\nPASS 1, FAIL 2, UNKNOWN 0`) },
    ARGS, script)
  if (result.status !== 'done') return `status ${JSON.stringify(result.status)}, reason ${JSON.stringify(result.reason)}`
  if (result.meets !== false) return `meets is ${JSON.stringify(result.meets)}, but e10-verdict printed "MEETS: no"`
  return true
}

// F6: one repair round, and only when a probe came back unfaithful from the model itself.
async function repairRound(script) {
  const order = withGroup(HAPPY_ORDER, 'e8-check', REPAIR)
  const repaired = { ...HAPPY, ...REPAIR_ANSWERS, 'e8-check': checked(1, 1), 'e8-check-2': checked(0, 0) }
  const { result, calls } = await run(repaired, ARGS, script)
  if (calledOrder(calls) !== order.join(' ')) {
    return `e8-check reported 1 unfaithful, and the labels were called in this order: ${calledOrder(calls)}\n${wanted(order)}`
  }
  if (result.status !== 'done') return `status ${JSON.stringify(result.status)}, reason ${JSON.stringify(result.reason)}`
  // The round is written into the group between e8-check and e9-input and never repeated, so a second unfaithful
  // answer from e8-check-2 must not produce a third e8-repair: the same order is the whole proof.
  const stillUnfaithful = { ...HAPPY, ...REPAIR_ANSWERS, 'e8-check': checked(1, 1), 'e8-check-2': checked(1, 1) }
  const again = await run(stillUnfaithful, ARGS, script)
  if (calledOrder(again.calls) !== order.join(' ')) {
    return `e8-check-2 reported 1 unfaithful and the run repaired again: ${calledOrder(again.calls)}\n${wanted(order)}`
  }
  const none = await run(HAPPY, ARGS, script)
  const repairedTwice = none.calls.filter(c => c.label === 'e8-repair').length
  if (repairedTwice) return `e8-check reported 0 unfaithful and e8-repair ran ${repairedTwice} times`
  return true
}

async function skips(script) {
  const nothingToConfirm = await run({ ...HAPPY, 'e8-input': ran('0 to confirm') }, ARGS, script)
  if (nothingToConfirm.calls.some(c => c.label === 'e8-confirm')) {
    return 'e8-confirm ran, although e8-input printed "0 to confirm"'
  }
  if (!JUDGES.every(label => nothingToConfirm.calls.some(c => c.label === label))) {
    return 'a judge was skipped, although e9-input still printed "3 to judge"'
  }
  if (nothingToConfirm.result.status !== 'done') {
    return `with nothing to confirm the run came back ${JSON.stringify(nothingToConfirm.result)}`
  }
  const nothingToJudge = await run({ ...HAPPY, 'e9-input': ran('0 to judge') }, ARGS, script)
  const judges = nothingToJudge.calls.filter(c => c.label.startsWith('e9-judge')).map(c => c.label)
  if (judges.length) return `${judges.join(', ')} ran, although e9-input printed "0 to judge"`
  if (!nothingToJudge.calls.some(c => c.label === 'e8-confirm')) {
    return 'e8-confirm was skipped too, although e8-input still printed "2 to confirm"'
  }
  const order = calledOrder(nothingToJudge.calls)
  const wantedOrder = HAPPY_ORDER.filter(l => !JUDGES.includes(l)).join(' ')
  if (order !== wantedOrder) return `with nothing to judge the labels were called in this order: ${order}\n${wanted(HAPPY_ORDER.filter(l => !JUDGES.includes(l)))}`
  return true
}

// F7: the rerun happens once, on plant_found: false, and not at all with no second plant.
async function judgeRerun(script) {
  const order = withGroup(HAPPY_ORDER, 'e9-merge', RERUN)
  const missed = { ...HAPPY, ...RERUN_ANSWERS, 'e9-merge': ran('plant_found: false') }
  const { result, calls } = await run(missed, ARGS, script)
  if (calledOrder(calls) !== order.join(' ')) {
    return `e9-merge reported a missed plant, and the labels were called in this order: ${calledOrder(calls)}\n${wanted(order)}`
  }
  if (result.status !== 'done') return `status ${JSON.stringify(result.status)}, reason ${JSON.stringify(result.reason)}`
  const noPlant = { ...missed, 'e9-input-2': ran('no other plant') }
  const again = await run(noPlant, ARGS, script)
  const order2 = calledOrder(again.calls)
  if (again.calls.filter(c => ['e9-judge-1b', 'e9-judge-2b', 'e9-merge-2'].includes(c.label)).length) {
    return `e9-input-2 printed "no other plant" and the rerun still ran: ${order2}`
  }
  if (!again.calls.some(c => c.label === 'e9-input-2')) return 'e9-input-2 did not run at all'
  // "no other plant" stops the three steps after it, not the one that asked: e9-input-2 runs and then the run goes on.
  const noPlantOrder = withGroup(HAPPY_ORDER, 'e9-merge', ['e9-input-2'])
  if (order2 !== noPlantOrder.join(' ')) {
    return `with no other plant the labels were called in this order: ${order2}\n${wanted(noPlantOrder)}`
  }
  if (again.result.status !== 'done') return `with no other plant the run came back ${JSON.stringify(again.result)}`
  const found = await run(HAPPY, ARGS, script)
  if (found.calls.some(c => RERUN.includes(c.label))) {
    return `e9-merge found the plant and the rerun ran anyway: ${calledOrder(found.calls)}`
  }
  return true
}

async function stopOnRunnerFailure(script) {
  for (const label of RUNNERS) {
    const { result, calls } = await run({ ...EVERYTHING, [label]: broke() }, ARGS, script)
    const wrong = blockedAt(result, label)
    if (wrong) return `${label} exited non-zero and the run ${wrong}`
    const after = later(calls, label)
    if (after.length) return `${label} exited non-zero and ${after.join(', ')} still ran`
  }
  return true
}

// F17: a model step that reports it did not finish blocks the run, as a null result does.
async function stopOnUnfinishedModelStep(script) {
  for (const label of MODEL_STEPS) {
    const { result, calls } = await run({ ...EVERYTHING, [label]: NOT_DONE }, ARGS, script)
    const wrong = blockedAt(result, label)
    if (wrong) return `${label} returned done: false and the run ${wrong}`
    const after = later(calls, label)
    if (after.length) return `${label} returned done: false and ${after.join(', ')} still ran`
  }
  return true
}

// F17: check-output is what catches a model step that answered and wrote nothing usable.
async function stopOnCheckOutput(script) {
  for (const label of CHECKS) {
    const { result, calls } = await run({ ...EVERYTHING, [label]: broke('probes: not valid') }, ARGS, script)
    const wrong = blockedAt(result, label)
    if (wrong) return `${label} exited non-zero and the run ${wrong}`
    const after = later(calls, label)
    if (after.length) return `${label} exited non-zero and ${after.join(', ')} still ran`
  }
  return true
}

async function stopOnNullModelResult(script) {
  for (const label of MODEL_STEPS) {
    const { result, calls } = await run({ ...EVERYTHING, [label]: null }, ARGS, script)
    const wrong = blockedAt(result, label)
    if (wrong) return `${label} returned null and the run ${wrong}`
    const after = later(calls, label)
    if (after.length) return `${label} returned null and ${after.join(', ')} still ran`
  }
  return true
}

async function missingArguments(script) {
  for (const name of ['product', 'spec', 'runId']) {
    const args = { ...ARGS }
    delete args[name]
    const { result, calls } = await run(HAPPY, args, script)
    if (calls.length) return `args without ${name} still ran ${calls.length} agents`
    const reason = String(result.reason || '')
    if (result.status !== 'blocked') return `args without ${name} came back ${JSON.stringify(result)}`
    if (!/missing argument/i.test(reason) || !reason.includes(name)) return `args without ${name} says ${JSON.stringify(result.reason)}`
  }
  return true
}

// F12: a runId that reaches out of runs/ is refused before any agent runs.
async function badRunId(script) {
  const ids = ['../x', 'a/b', '..', 'a..b', '-lead', '.hidden', 'has space', 'x\\y']
  for (const runId of ids) {
    const { result, calls } = await run(HAPPY, { ...ARGS, runId }, script)
    if (result.status !== 'blocked') return `runId ${JSON.stringify(runId)} came back ${JSON.stringify(result)}`
    if (calls.length) return `runId ${JSON.stringify(runId)} still ran ${calls.length} agents`
    if (/missing argument/i.test(String(result.reason))) {
      return `runId ${JSON.stringify(runId)} was refused as a missing argument, not by the rule that keeps runs inside runs/`
    }
  }
  return true
}

async function neverMakesAVerdict(script) {
  const tails = [`wrote ${RUN}/verdict.json\nPASS 3, FAIL 0, UNKNOWN 0`, 'meets: yes\n', 'MEETS\n']
  for (const tail of tails) {
    const { result } = await run({ ...HAPPY, 'e10-verdict': ran(tail) }, ARGS, script)
    if (result.status === 'done') return `e10-verdict printed ${JSON.stringify(tail)} and the run came back done with meets ${JSON.stringify(result.meets)}`
    const wrong = blockedAt(result, 'e10-verdict')
    if (wrong) return `e10-verdict printed ${JSON.stringify(tail)} and the run ${wrong}`
  }
  return true
}

// F19: meets comes from one run's MEETS line and from no other run's.
async function meetsLineMustBeThisRun(script) {
  const tails = [`MEETS: yes run=20261013-somewhere-else`, 'MEETS: yes', 'MEETS: yes run=', 'MEETS: yes run=20261013-harnessx']
  for (const tail of tails) {
    const { result, calls } = await run({ ...HAPPY, 'e10-verdict': ran(tail) }, ARGS, script)
    if (result.status === 'done') {
      return `e10-verdict printed ${JSON.stringify(tail)} and the run came back done with meets ${JSON.stringify(result.meets)}`
    }
    const wrong = blockedAt(result, 'e10-verdict')
    if (wrong) return `e10-verdict printed ${JSON.stringify(tail)} and the run ${wrong}`
    if (!calls.some(c => c.label === 'e11-end')) return `e10-verdict printed ${JSON.stringify(tail)} and the run stopped without its end stamp`
  }
  return true
}

async function exactCommands(script) {
  const { calls } = await run(HAPPY, ARGS, script)
  for (const label of ['e0-start', 'e1-spec', 'e2-workspace', 'e3-check', 'e4-check', 'e5-view', 'e5-collect',
    'e5-check', 'e6-matrix', 'e8-input', 'e8-check', 'e9-input', 'e9-merge', 'e10-verdict']) {
    const command = CMDS[label].replace(/ --(step|attempt) \S+$/, '')
    if (!carries(promptOf(calls, label), command)) {
      return `the ${label} prompt does not carry its command.\n      wanted: ${CMDS[label]}\n      prompt:  ${promptOf(calls, label)}`
    }
  }
  for (const [label, step] of [['e3-check', 'classify'], ['e4-check', 'probes'], ['e5-check', 'mutants']]) {
    if (!hasFlag(promptOf(calls, label), '--step', step)) {
      return `the ${label} prompt does not say --step ${step}.\n      prompt:  ${promptOf(calls, label)}`
    }
  }
  if (!hasFlag(promptOf(calls, 'e9-input'), '--attempt', '1')) {
    return `the e9-input prompt does not ask for attempt 1.\n      prompt:  ${promptOf(calls, 'e9-input')}`
  }
  return true
}

// F9: the mutant writer works in its own folder, without the probes.
async function mutantViewCommand(script) {
  const { calls } = await run(HAPPY, ARGS, script)
  const mutants = promptOf(calls, 'e5-mutants')
  if (!carries(mutants, `codex exec -m gpt-6.1-sol`) || !mutants.includes('codex exec -m gpt-6.1-sol')) {
    return `the e5-mutants prompt does not call codex gpt-6.1-sol.\n      prompt:  ${mutants}`
  }
  if (!mutants.includes(`-C ${RUN}/mutant-view`)) {
    return `the e5-mutants prompt does not confine codex to the mutant view.\n      wanted: -C ${RUN}/mutant-view\n      prompt:  ${mutants}`
  }
  if (!mutants.includes('< /dev/null')) return `the e5-mutants prompt leaves codex reading stdin.\n      prompt:  ${mutants}`
  if (!mutants.includes('RUN=.')) {
    return `the e5-mutants prompt still names the run folder.\n      wanted: RUN=. (codex works in the view)\n      prompt:  ${mutants}`
  }
  return true
}

// F8: the optional exclude argument becomes one --exclude per glob, and the defaults stay.
async function excludeGlobs(script) {
  const { calls } = await run(HAPPY, ARGS_WITH_EXCLUDES, script)
  const prompt = promptOf(calls, 'e2-workspace')
  for (const glob of EXCLUDES) {
    // A glob is one shell argument: 'docs/*.md' quoted is right, an unquoted 'docs/*.md' would be expanded by the
    // shell into whatever files happen to match, and the runner would get a different command each day.
    if (!prompt.includes(`--exclude ${shellArgument(glob)}`)) {
      return `the e2-workspace prompt does not carry --exclude ${shellArgument(glob)}.\n      prompt:  ${prompt}`
    }
  }
  const plain = await run(HAPPY, ARGS, script)
  const withoutArgument = promptOf(plain.calls, 'e2-workspace')
  for (const glob of EXCLUDES) {
    if (withoutArgument.includes(glob)) {
      return `no exclude argument was given, and the e2-workspace prompt still names ${glob}.\n      prompt:  ${withoutArgument}`
    }
  }
  return true
}

// F2: call 1 is given the judge's own folder and is never told the run folder, so it cannot read plant_case.
async function judgeOneIsGivenTheJudgeFolder(script) {
  const { calls } = await run(HAPPY, ARGS, script)
  const first = promptOf(calls, 'e9-judge-1')
  if (!first.includes(`JUDGE_DIR=${JUDGE_DIR}`)) {
    return `the e9-judge-1 prompt does not carry JUDGE_DIR=${JUDGE_DIR}.\n      prompt:  ${first}`
  }
  if (!hasFlag(first, 'CALL', '1')) {
    return `the e9-judge-1 prompt does not say CALL=1.\n      prompt:  ${first}`
  }
  if (first.includes('RUN=')) {
    return `the e9-judge-1 prompt still hands the judge the run folder, where the plant's case id is readable.\n      prompt:  ${first}`
  }
  const second = promptOf(calls, 'e9-judge-2')
  if (!second.includes(`RUN=${RUN}`) || !second.includes(`PRODUCT_COPY=${RUN}/workspace/product`)) {
    return `the e9-judge-2 prompt does not carry RUN and PRODUCT_COPY.\n      prompt:  ${second}`
  }
  if (!hasFlag(second, 'CASE', '\\S+')) {
    return `the e9-judge-2 prompt does not name the plant case.\n      e9-input printed "plant G2-F2".\n      prompt:  ${second}`
  }
  return true
}

// F18: the run opens with a start stamp and closes with an end stamp carrying the agent count.
async function startAndEndStamps(script) {
  const { calls } = await run(HAPPY, ARGS, script)
  if (calls.length < 2) return `only ${calls.length} agents were called, so there is no end stamp to check`
  if (calls[0].label !== 'e0-start') return `the first agent was ${calls[0].label}, not e0-start`
  if (calls[calls.length - 1].label !== 'e11-end') return `the last agent was ${calls[calls.length - 1].label}, not e11-end`
  const start = promptOf(calls, 'e0-start')
  if (!carries(start, CMDS['e0-start'])) {
    return `the e0-start prompt does not carry its command.\n      wanted: ${CMDS['e0-start']}\n      prompt:  ${start}`
  }
  const end = promptOf(calls, 'e11-end')
  if (!carries(end, `python3 tools/evaluator/model_io.py stamp --run ${RUN} --event end`)) {
    return `the e11-end prompt does not carry its command.\n      wanted: ${CMDS['e0-start'].replace('start', 'end --agents <count>')}\n      prompt:  ${end}`
  }
  // DATA.md says "the count of agent() calls so far", read before or after the end step's own call; either is right.
  const agents = /--agents(?:[ =])(\d+)/.exec(end)
  if (!agents) return `the e11-end prompt carries no --agents count.\n      prompt:  ${end}`
  const count = Number(agents[1])
  if (count !== calls.length - 1 && count !== calls.length) {
    return `the e11-end stamp says ${count} agents, and the stub was called ${calls.length} times (${calls.length - 1} before the stamp)`
  }
  return true
}

async function modelsPerStep(script) {
  const { calls } = await run(EVERYTHING, ARGS, script)
  for (const call of calls) {
    const want = modelFor(call.label)
    if (call.model !== want) return `${call.label} runs on model ${JSON.stringify(call.model)}, DATA.md names ${want}`
  }
  return true
}

// The one rule broken here is the stop on a runner that exits non-zero (EV-C6.2): the script is given a copy in
// which it reads a field the runner's answer does not carry, so the exit is never what DATA.md says it is.
async function sabotageCase() {
  const brokenSource = source.replaceAll('exit_code', 'exit_code_')
  if (brokenSource === source) return 'the script does not read a runner exit_code, so there was nothing to break'
  let broken
  try {
    broken = build(brokenSource)
  } catch (error) {
    return `breaking the runner exit_code made the script unparseable: ${error.message}`
  }
  const outcome = await stopOnRunnerFailure(broken)
  if (outcome === true) return 'the runner exit_code is broken and the stop case still passes, so that case proves nothing'
  return true
}

const CASES = [
  ['happy path: the labels DATA.md puts on the way with nothing unfaithful and the plant found', happyPath],
  ['meets: false when e10-verdict prints MEETS: no', meetsFalse],
  ['F6: the repair round runs only when e8-check says unfaithful > 0, and runs once', repairRound],
  ['F7: the judge rerun runs only on plant_found: false, and not on "no other plant"', judgeRerun],
  ['e8-confirm and both judges are skipped when their input step says 0', skips],
  ['a runner that exits non-zero blocks there and no later label runs (EV-C6.2)', stopOnRunnerFailure],
  ['F17: a model step that returns done: false blocks there and no later label runs', stopOnUnfinishedModelStep],
  ['F17: a check-output exit non-zero blocks there and no later label runs', stopOnCheckOutput],
  ['a model step that returns null blocks there and no later label runs (EV-C6.2)', stopOnNullModelResult],
  ['a missing product, spec or runId blocks before any agent runs', missingArguments],
  ['F12: a runId that reaches out of runs/ blocks before any agent runs', badRunId],
  ['no MEETS line leaves the run blocked at e10-verdict; the workflow never guesses (EV-P1.3)', neverMakesAVerdict],
  ['F19: a MEETS line whose run= is not this runId blocks at e10-verdict', meetsLineMustBeThisRun],
  ['the runner prompts carry DATA.md commands with the arguments substituted', exactCommands],
  ['F8: each exclude glob becomes its own --exclude on e2-workspace', excludeGlobs],
  ['F9: codex runs with -C runs/<runId>/mutant-view and RUN=.', mutantViewCommand],
  ['F2: e9-judge-1 is given JUDGE_DIR only, never RUN=', judgeOneIsGivenTheJudgeFolder],
  ['F18: e0-start is first, e11-end is last, and the end stamp carries the agent count', startAndEndStamps],
  ['each step runs on the model DATA.md names (EV-C6.1)', modelsPerStep],
  ['sabotage: the runner stop rule broken in the source, and the stop case catches it', sabotageCase],
]

let failures = 0
for (const [name, fn] of CASES) {
  let outcome
  try {
    outcome = await fn()
  } catch (error) {
    outcome = `the harness could not run the case: ${error.message}`
  }
  if (outcome === true) console.log(`PASS ${name}`)
  else { failures++; console.log(`FAIL ${name}\n      ${outcome}`) }
}
console.log(failures ? `\n${failures} of ${CASES.length} cases FAILED` : `\nall ${CASES.length} cases passed`)
process.exit(failures ? 1 : 0)