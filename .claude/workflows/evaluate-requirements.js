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
if (!/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(runId) || runId.includes('..')) {
  return { status: 'blocked', reason: 'invalid runId' }
}
if (options.exclude !== undefined && (!Array.isArray(options.exclude) || options.exclude.some(glob => typeof glob !== 'string'))) {
  return { status: 'blocked', reason: 'exclude must be a list of globs' }
}
const run = `runs/${runId}`
const probeEnvironment = `HOME="$PWD"/${shellArgument(`${run}/probe-scratch`)} TMPDIR="$PWD"/${shellArgument(`${run}/probe-scratch`)}`
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
  const result = await agent(`Run exactly this command from the repository root, with a Bash timeout of 600000 ms (some steps take minutes), then report: ${command}`, {
    label, phase: title, schema: runnerSchema, model: 'haiku', effort: 'low',
  })
  if (!result || result.exit_code !== 0) throw blocked(label, result)
  return result
}

async function runModel(label, brief, model, title, context = `RUN=${run}`) {
  agentsUsed++
  const result = await agent(`Read ${brief} and do what it says. ${context}`, {
    label, phase: title, schema: modelSchema, model, effort: 'high',
  })
  if (!result || result.done !== true) throw blocked(label, result)
  return result
}

function blocked(label, result) {
  return { status: 'blocked', step: label, reason: result?.stderr_tail || result?.note || 'no result' }
}

async function confirmProbes(suffix = '') {
  const input = await runCommand(`e8-input${suffix}`, `python3 tools/evaluator/model_io.py confirm-input --run ${shellArgument(run)}`, 'Confirm')
  if (!/^0 to confirm\s*$/m.test(input.stdout_tail)) {
    await runModel(`e8-confirm${suffix}`, 'docs/evaluator/briefs/confirm.md', 'sonnet', 'Confirm')
  }
  return await runCommand(`e8-check${suffix}`, `python3 tools/evaluator/model_io.py confirm-check --run ${shellArgument(run)}`, 'Confirm')
}

async function judgeCases(input, retry = false) {
  if (!/^0 to judge\s*$/m.test(input.stdout_tail)) {
    const plant = /^plant (\S+)\s*$/m.exec(input.stdout_tail)?.[1]
    const judgeDir = `/tmp/evaluator-judge-${runId}`
    await runModel(retry ? 'e9-judge-1b' : 'e9-judge-1', 'docs/evaluator/briefs/judge.md', 'sonnet', 'Judge',
      `CALL=1 JUDGE_DIR=${judgeDir}\nFor this call, read ${judgeDir}/judge-input.json, judge ${judgeDir}/product/, and write ${judgeDir}/judge-1.json. These paths override the brief's paths. Judge every listed case.`)
    await runModel(retry ? 'e9-judge-2b' : 'e9-judge-2', 'docs/evaluator/briefs/judge.md', 'sonnet', 'Judge',
      `CALL=2 RUN=${run} PRODUCT_COPY=${run}/workspace/product CASE=${plant || 'none'}\n${plant ? `Judge only ${plant} on the clean product.` : 'There is no plant case; write an empty cases list.'}`)
  }
  return await runCommand(retry ? 'e9-merge-2' : 'e9-merge', `python3 tools/evaluator/model_io.py judged-merge --run ${shellArgument(run)}`, 'Judge')
}

try {
  const spec = options.spec
  phase('Workspace')
  await runCommand('e0-start', `python3 tools/evaluator/model_io.py stamp --run ${shellArgument(run)} --event start`, 'Workspace')
  await runCommand('e1-spec', `python3 tools/evaluator/spec_parse.py --requirements ${shellArgument(`${spec}/REQUIREMENTS.md`)} --vision ${shellArgument(`${spec}/VISION.md`)} --out ${shellArgument(`${run}/requirements.json`)}`, 'Workspace')
  const excludes = (options.exclude || []).map(glob => ` --exclude ${shellArgument(glob)}`).join('')
  await runCommand('e2-workspace', `python3 tools/evaluator/workspace.py --product ${shellArgument(options.product)} --spec ${shellArgument(spec)} --run ${shellArgument(run)}${excludes}`, 'Workspace')

  phase('Probes')
  await runModel('e3-classify', 'docs/evaluator/briefs/classify.md', 'haiku', 'Probes')
  await runCommand('e3-check', `python3 tools/evaluator/model_io.py check-output --run ${shellArgument(run)} --step classify`, 'Probes')
  await runModel('e4-probes', 'docs/evaluator/briefs/probes.md', 'sonnet', 'Probes')
  await runCommand('e4-check', `python3 tools/evaluator/model_io.py check-output --run ${shellArgument(run)} --step probes`, 'Probes')
  await runCommand('e5-view', `python3 tools/evaluator/model_io.py mutant-view --run ${shellArgument(run)}`, 'Probes')
  // The runner's PWD supplies the repository brief while Codex works inside its view.
  await runCommand('e5-mutants', `codex exec -m gpt-6.1-sol -c model_reasoning_effort=high --sandbox workspace-write -C ${shellArgument(`${run}/mutant-view`)} "Read $PWD/docs/evaluator/briefs/mutants.md with RUN=. and do what it says." < /dev/null`, 'Probes')
  await runCommand('e5-collect', `python3 tools/evaluator/model_io.py mutant-view --run ${shellArgument(run)} --collect`, 'Probes')
  await runCommand('e5-check', `python3 tools/evaluator/model_io.py check-output --run ${shellArgument(run)} --step mutants`, 'Probes')
  await runCommand('e6-matrix', `${probeEnvironment} python3 tools/evaluator/probe_matrix.py --run ${shellArgument(run)}`, 'Probes')

  phase('Confirm')
  const checked = await confirmProbes()
  const unfaithful = /^\d+ checked, \d+ voided, (\d+) unfaithful\s*$/m.exec(checked.stdout_tail)
  if (unfaithful && Number(unfaithful[1]) > 0) {
    await runModel('e8-repair', 'docs/evaluator/briefs/probes-repair.md', 'sonnet', 'Confirm',
      `RUN=${run}\nRewrite only probes listed in ${run}/repair.json, using their requirement sentence and the confirm answer's reason. This is the single repair round.`)
    await runCommand('e6-matrix-2', `${probeEnvironment} python3 tools/evaluator/probe_matrix.py --run ${shellArgument(run)}`, 'Probes')
    await confirmProbes('-2')
  }

  phase('Judge')
  const input = await runCommand('e9-input', `python3 tools/evaluator/model_io.py judge-input --run ${shellArgument(run)} --attempt 1`, 'Judge')
  const merged = await judgeCases(input)
  if (/^plant_found: false\s*$/m.test(merged.stdout_tail)) {
    const secondInput = await runCommand('e9-input-2', `python3 tools/evaluator/model_io.py judge-input --run ${shellArgument(run)} --attempt 2`, 'Judge')
    if (!/^no other plant\s*$/m.test(secondInput.stdout_tail)) await judgeCases(secondInput, true)
  }

  phase('Verdict')
  const verdict = await runCommand('e10-verdict', `python3 tools/evaluator/verdict.py --run ${shellArgument(run)}`, 'Verdict')
  const meetsLine = /^MEETS: (yes|no) run=(\S+)[ \t]*$/m.exec(verdict.stdout_tail)
  await runCommand('e11-end', `python3 tools/evaluator/model_io.py stamp --run ${shellArgument(run)} --event end --agents ${agentsUsed}`, 'Verdict')
  if (!meetsLine || meetsLine[2] !== runId) {
    return { status: 'blocked', step: 'e10-verdict', reason: 'no MEETS line for this run' }
  }
  return { status: 'done', runId, meets: meetsLine[1] === 'yes', authoritative: `${run}/verdict.json`,
    verdict: `${run}/verdict.md`, agents: agentsUsed }
} catch (failure) {
  if (failure?.status === 'blocked') return failure
  throw failure
}
