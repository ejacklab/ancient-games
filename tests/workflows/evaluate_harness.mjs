// Offline harness for .claude/workflows/evaluate-requirements.js. No agents run and no tokens are spent: `agent` is a
// stub that answers by label, and every runner's answer is a canned {exit_code, stdout_tail, stderr_tail}. It checks
// the label order and the two skips of DATA.md's table, the exact commands, the two stops (EV-C6.2), the model each
// step runs on (EV-C6.1) and that the workflow never makes a verdict (EV-P1.3). The last case runs a deliberately
// broken copy of the script, so the checks above are shown to be able to fail.
// Run from the repository root:  node tests/workflows/evaluate_harness.mjs

import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const here = dirname(fileURLToPath(import.meta.url))
const SCRIPT = join(here, '../../.claude/workflows/evaluate-requirements.js')

const RUN_ID = '20261013-harness'
const ARGS = { product: 'products/calc', spec: 'spec/calc', runId: RUN_ID }
const RUN = `runs/${RUN_ID}`
const clone = x => (x === null ? null : JSON.parse(JSON.stringify(x)))

// DATA.md's table, in order: 14 labels, 9 of them runners and 5 of them model steps.
const ORDER = ['e1-spec', 'e2-workspace', 'e3-classify', 'e4-probes', 'e5-mutants', 'e6-matrix', 'e8-input',
  'e8-confirm', 'e8-check', 'e9-input', 'e9-judge-1', 'e9-judge-2', 'e9-merge', 'e10-verdict']
const RUNNERS = ['e1-spec', 'e2-workspace', 'e5-mutants', 'e6-matrix', 'e8-input', 'e8-check', 'e9-input',
  'e9-merge', 'e10-verdict']
const MODEL_STEPS = ['e3-classify', 'e4-probes', 'e8-confirm', 'e9-judge-1', 'e9-judge-2']
const SKIPPABLE = ['e8-confirm', 'e9-judge-1', 'e9-judge-2']
const JUDGES = ['e9-judge-1', 'e9-judge-2']
const MODEL_OF = { 'e3-classify': 'haiku', 'e4-probes': 'sonnet', 'e8-confirm': 'sonnet', 'e9-judge-1': 'sonnet',
  'e9-judge-2': 'sonnet' }
const modelFor = label => (MODEL_OF[label] || 'haiku') // every runner is a haiku at low effort

const CMDS = {
  'e1-spec': `python3 tools/evaluator/spec_parse.py --requirements ${ARGS.spec}/REQUIREMENTS.md --vision ${ARGS.spec}/VISION.md --out ${RUN}/requirements.json`,
  'e2-workspace': `python3 tools/evaluator/workspace.py --product ${ARGS.product} --spec ${ARGS.spec} --run ${RUN}`,
  'e5-mutants': `codex exec -m gpt-6.1-sol -c model_reasoning_effort=high --sandbox workspace-write -C . "Read docs/evaluator/briefs/mutants.md with RUN=${RUN} and do what it says." < /dev/null`,
  'e6-matrix': `python3 tools/evaluator/probe_matrix.py --run ${RUN}`,
  'e8-input': `python3 tools/evaluator/model_io.py confirm-input --run ${RUN}`,
  'e8-check': `python3 tools/evaluator/model_io.py confirm-check --run ${RUN}`,
  'e9-input': `python3 tools/evaluator/model_io.py judge-input --run ${RUN}`,
  'e9-merge': `python3 tools/evaluator/model_io.py judged-merge --run ${RUN}`,
  'e10-verdict': `python3 tools/evaluator/verdict.py --run ${RUN}`,
}

const ran = (stdout = '') => ({ exit_code: 0, stdout_tail: stdout, stderr_tail: '' })
const broke = (stderr = 'the command failed') => ({ exit_code: 1, stdout_tail: '', stderr_tail: stderr })
const WROTE = { done: true, note: 'written' }

const HAPPY = {
  'e1-spec': ran(), 'e2-workspace': ran(), 'e3-classify': WROTE, 'e4-probes': WROTE, 'e5-mutants': ran(),
  'e6-matrix': ran(), 'e8-input': ran('2 to confirm'), 'e8-confirm': WROTE, 'e8-check': ran('2 checked, 0 voided'),
  'e9-input': ran('3 to judge'), 'e9-judge-1': WROTE, 'e9-judge-2': WROTE, 'e9-merge': ran('plant_found: true'),
  'e10-verdict': ran(`wrote ${RUN}/verdict.json\nMEETS: yes\nPASS 3, FAIL 0, UNKNOWN 0`),
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
  if (unasked.length) throw new Error(`the workflow called ${unasked.join(', ')}, which this harness has no answer for`)
  return { result, calls }
}

const promptOf = (calls, label) => (calls.find(c => c.label === label) || { prompt: '' }).prompt
const later = (calls, label) => calls.slice(ORDER.indexOf(label) + 1).map(c => c.label)

// A prompt carries the command when the whole command is there and nothing runs straight on from it, so that
// "--run runs/<runId>" does not pass for "--run runs/<runId>/matrix".
const carries = (prompt, cmd) => {
  const at = prompt.indexOf(cmd)
  if (at < 0) return false
  const before = at === 0 ? '' : prompt[at - 1]
  const after = prompt[at + cmd.length] || ''
  return !/[A-Za-z0-9_/]/.test(before) && !/[A-Za-z0-9_/]/.test(after)
}

// --- the cases ----------------------------------------------------------------------------------------------------------

async function happyPath(script) {
  const { result, calls } = await run(HAPPY, ARGS, script)
  const order = calls.map(c => c.label).join(' ')
  if (order !== ORDER.join(' ')) return `the labels were called in this order: ${order}`
  if (result.status !== 'done') return `status ${JSON.stringify(result.status)}, reason ${JSON.stringify(result.reason)}`
  if (result.meets !== true) return `meets is ${JSON.stringify(result.meets)}, but e10-verdict printed "MEETS: yes"`
  if (result.agents !== calls.length) return `agents is ${result.agents}, and the stub was called ${calls.length} times`
  if (result.runId !== RUN_ID) return `runId is ${JSON.stringify(result.runId)}`
  if (result.verdict !== `${RUN}/verdict.md`) return `verdict is ${JSON.stringify(result.verdict)}`
  return true
}

async function meetsFalse(script) {
  const { result } = await run({ ...HAPPY, 'e10-verdict': ran('MEETS: no\nPASS 1, FAIL 2, UNKNOWN 0') }, ARGS, script)
  if (result.status !== 'done') return `status ${JSON.stringify(result.status)}, reason ${JSON.stringify(result.reason)}`
  if (result.meets !== false) return `meets is ${JSON.stringify(result.meets)}, but e10-verdict printed "MEETS: no"`
  return true
}

async function skips(script) {
  const nothingToConfirm = await run({ ...HAPPY, 'e8-input': ran('0 to confirm') }, ARGS, script)
  if (nothingToConfirm.calls.some(c => c.label === 'e8-confirm'))
    return 'e8-confirm ran, although e8-input printed "0 to confirm"'
  if (!JUDGES.every(label => nothingToConfirm.calls.some(c => c.label === label)))
    return 'a judge was skipped, although e9-input still printed "3 to judge"'
  if (nothingToConfirm.result.status !== 'done')
    return `with nothing to confirm the run came back ${JSON.stringify(nothingToConfirm.result)}`
  const nothingToJudge = await run({ ...HAPPY, 'e9-input': ran('0 to judge') }, ARGS, script)
  const judges = nothingToJudge.calls.filter(c => c.label.startsWith('e9-judge')).map(c => c.label)
  if (judges.length) return `${judges.join(', ')} ran, although e9-input printed "0 to judge"`
  if (!nothingToJudge.calls.some(c => c.label === 'e8-confirm'))
    return 'e8-confirm was skipped too, although e8-input still printed "2 to confirm"'
  const order = nothingToJudge.calls.map(c => c.label).join(' ')
  const wanted = ORDER.filter(l => !JUDGES.includes(l)).join(' ')
  if (order !== wanted) return `with nothing to judge the labels were called in this order: ${order}\n      DATA.md skips only ${SKIPPABLE.join(', ')}, so it should be: ${wanted}`
  return true
}

async function stopOnRunnerFailure(script) {
  for (const label of RUNNERS) {
    const { result, calls } = await run({ ...HAPPY, [label]: broke() }, ARGS, script)
    const wrong = blockedAt(result, label)
    if (wrong) return `${label} exited non-zero and the run ${wrong}`
    const after = later(calls, label)
    if (after.length) return `${label} exited non-zero and ${after.join(', ')} still ran`
  }
  return true
}

async function stopOnNullModelResult(script) {
  for (const label of MODEL_STEPS) {
    const { result, calls } = await run({ ...HAPPY, [label]: null }, ARGS, script)
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

async function exactCommands(script) {
  const { calls } = await run(HAPPY, ARGS, script)
  for (const label of ['e1-spec', 'e2-workspace', 'e6-matrix', 'e10-verdict']) {
    if (!carries(promptOf(calls, label), CMDS[label]))
      return `the ${label} prompt does not carry its command.\n      wanted: ${CMDS[label]}\n      prompt:  ${promptOf(calls, label)}`
  }
  const mutants = promptOf(calls, 'e5-mutants')
  if (!mutants.includes('codex exec -m gpt-6.1-sol'))
    return `the e5-mutants prompt does not call codex gpt-6.1-sol.\n      wanted: ${CMDS['e5-mutants']}\n      prompt:  ${mutants}`
  if (!mutants.includes('< /dev/null'))
    return `the e5-mutants prompt leaves codex reading stdin.\n      wanted: ${CMDS['e5-mutants']}\n      prompt:  ${mutants}`
  return true
}

async function modelsPerStep(script) {
  const { calls } = await run(HAPPY, ARGS, script)
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
  ['happy path: the 14 labels in DATA.md order, done, meets read from e10-verdict', happyPath],
  ['meets: false when e10-verdict prints MEETS: no', meetsFalse],
  ['e8-confirm and both judges are skipped when their input step says 0', skips],
  ['a runner that exits non-zero blocks there and no later label runs (EV-C6.2)', stopOnRunnerFailure],
  ['a model step that returns null blocks there and no later label runs (EV-C6.2)', stopOnNullModelResult],
  ['a missing product, spec or runId blocks before any agent runs', missingArguments],
  ['no MEETS line leaves the run blocked at e10-verdict; the workflow never guesses (EV-P1.3)', neverMakesAVerdict],
  ['the runner prompts carry DATA.md commands with the arguments substituted', exactCommands],
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