export const meta = {
  name: 'evaluate-requirements',
  description: 'Evaluate a product against its written requirements using probes, mutants, confirmation and planted judging checks.',
  phases: [
    { title: 'Workspace', detail: 'parse the spec and copy the product into a blind workspace' },
    { title: 'Probes', detail: 'classify cases, write probes and mutants, then run the matrix' },
    { title: 'Confirm', detail: 'confirm failing probes against quoted requirements and source' },
    { title: 'Judge', detail: 'judge a planted copy and recheck the plant case on the clean copy' },
    { title: 'Verdict', detail: 'run the verdict script and report its MEETS line' },
  ],
}

const options = args || {}
for (const name of ['product', 'spec', 'runId']) {
  if (typeof options[name] !== 'string' || !options[name].trim()) {
    return { status: 'blocked', reason: `missing argument ${name}` }
  }
}

const runId = options.runId
const run = `runs/${runId}`
let agentsUsed = 0
const runnerSchema = {
  type: 'object',
  properties: {
    exit_code: { type: 'integer' },
    stdout_tail: { type: 'string', description: 'The last 40 lines of stdout.' },
    stderr_tail: { type: 'string', description: 'The last 40 lines of stderr.' },
  },
  required: ['exit_code', 'stdout_tail', 'stderr_tail'],
}
const modelSchema = {
  type: 'object',
  properties: { done: { type: 'boolean' }, note: { type: 'string' } },
  required: ['done', 'note'],
}

function shellArgument(value) {
  return /^[A-Za-z0-9_./-]+$/.test(value) ? value : `'${value.replaceAll("'", "'\\''")}'`
}

async function runCommand(label, command, title) {
  agentsUsed++
  return await agent(`Run exactly this command from the repository root, with a Bash timeout of 600000 ms (some steps take minutes), then report: ${command}`, {
    label, phase: title, schema: runnerSchema, model: 'haiku', effort: 'low',
  })
}

async function runModel(label, brief, model, title, extra = '') {
  agentsUsed++
  return await agent(`Read ${brief} and do what it says. RUN=${run}${extra}`, {
    label, phase: title, schema: modelSchema, model, effort: 'high',
  })
}

function blocked(label, result) {
  return { status: 'blocked', step: label, reason: result?.stderr_tail || 'no result' }
}

const spec = options.spec
phase('Workspace')
let result = await runCommand('e1-spec', `python3 tools/evaluator/spec_parse.py --requirements ${shellArgument(`${spec}/REQUIREMENTS.md`)} --vision ${shellArgument(`${spec}/VISION.md`)} --out ${shellArgument(`${run}/requirements.json`)}`, 'Workspace')
if (!result || result.exit_code !== 0) return blocked('e1-spec', result)
result = await runCommand('e2-workspace', `python3 tools/evaluator/workspace.py --product ${shellArgument(options.product)} --spec ${shellArgument(spec)} --run ${shellArgument(run)}`, 'Workspace')
if (!result || result.exit_code !== 0) return blocked('e2-workspace', result)

phase('Probes')
result = await runModel('e3-classify', 'docs/evaluator/briefs/classify.md', 'haiku', 'Probes')
if (result === null || result === undefined) return blocked('e3-classify', result)
result = await runModel('e4-probes', 'docs/evaluator/briefs/probes.md', 'sonnet', 'Probes')
if (result === null || result === undefined) return blocked('e4-probes', result)
const mutantPrompt = `Read docs/evaluator/briefs/mutants.md with RUN=${run} and do what it says.`
const quotedMutantPrompt = `"${mutantPrompt.replace(/["\\$`]/g, '\\$&')}"`
result = await runCommand('e5-mutants', `codex exec -m gpt-6.1-sol -c model_reasoning_effort=high --sandbox workspace-write -C . ${quotedMutantPrompt} < /dev/null`, 'Probes')
if (!result || result.exit_code !== 0) return blocked('e5-mutants', result)
result = await runCommand('e6-matrix', `python3 tools/evaluator/probe_matrix.py --run ${shellArgument(run)}`, 'Probes')
if (!result || result.exit_code !== 0) return blocked('e6-matrix', result)

phase('Confirm')
result = await runCommand('e8-input', `python3 tools/evaluator/model_io.py confirm-input --run ${shellArgument(run)}`, 'Confirm')
if (!result || result.exit_code !== 0) return blocked('e8-input', result)
if (!/^0 to confirm\s*$/m.test(result.stdout_tail)) {
  result = await runModel('e8-confirm', 'docs/evaluator/briefs/confirm.md', 'sonnet', 'Confirm')
  if (result === null || result === undefined) return blocked('e8-confirm', result)
}
result = await runCommand('e8-check', `python3 tools/evaluator/model_io.py confirm-check --run ${shellArgument(run)}`, 'Confirm')
if (!result || result.exit_code !== 0) return blocked('e8-check', result)

phase('Judge')
result = await runCommand('e9-input', `python3 tools/evaluator/model_io.py judge-input --run ${shellArgument(run)}`, 'Judge')
if (!result || result.exit_code !== 0) return blocked('e9-input', result)
if (!/^0 to judge\s*$/m.test(result.stdout_tail)) {
  result = await runModel('e9-judge-1', 'docs/evaluator/briefs/judge.md', 'sonnet', 'Judge', ` CALL=1 PRODUCT_COPY=${run}/judge-copy`)
  if (result === null || result === undefined) return blocked('e9-judge-1', result)
  result = await runModel('e9-judge-2', 'docs/evaluator/briefs/judge.md', 'sonnet', 'Judge', ` CALL=2 PRODUCT_COPY=${run}/workspace/product\nJudge only plant_case from ${run}/judge-input.json; if it is null, write an empty cases list.`)
  if (result === null || result === undefined) return blocked('e9-judge-2', result)
}
result = await runCommand('e9-merge', `python3 tools/evaluator/model_io.py judged-merge --run ${shellArgument(run)}`, 'Judge')
if (!result || result.exit_code !== 0) return blocked('e9-merge', result)

phase('Verdict')
result = await runCommand('e10-verdict', `python3 tools/evaluator/verdict.py --run ${shellArgument(run)}`, 'Verdict')
if (!result || result.exit_code !== 0) return blocked('e10-verdict', result)
const meetsLine = /^MEETS: (yes|no)\s*$/m.exec(result.stdout_tail)
if (!meetsLine) return { status: 'blocked', step: 'e10-verdict', reason: 'no MEETS line' }
return { status: 'done', runId, meets: meetsLine[1] === 'yes', verdict: `${run}/verdict.md`, agents: agentsUsed }
