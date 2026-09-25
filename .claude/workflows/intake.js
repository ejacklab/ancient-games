export const meta = {
  name: 'intake',
  description: 'Take one incoming challenge through the workflow design method and produce a prompt file (small task) or a workflow design (bigger task). Designs only; executes nothing.',
  whenToUse: 'When a challenge arrives and it is not obvious whether it needs a workflow. args: {challenge: "<text>", runId: "<YYYYMMDD-slug>"}. Writes only under runs/<runId>/. Skip it when the problem, the fix and the check are one sentence each.',
  phases: [
    { title: 'Readiness', detail: 'create the state file; list tools, skills and information, and what is missing; check the product blueprint' },
    { title: 'Algorithm', detail: 'write the steps with their checks; list every unclear spot; judge risk' },
    { title: 'Design', detail: 'small task: a prompt file; bigger task: a sequential workflow design' },
    { title: 'Check', detail: 'fixed yes/no checks by the script, then one verifier that sees only the files' },
  ],
}

// Method: docs/WORKFLOW_DESIGN_METHOD.md. Sequential and state-file driven: every agent reads
// runs/<runId>/state.md, does one step, writes its output file and updates the state.
// The script has no file access. It schedules, decides the size, and runs the objective checks.
// Loops here close on fixed yes/no items, never on an open-ended "find a problem" review.

const opts = typeof args === 'string' ? { challenge: args } : (args || {})
const CHALLENGE = typeof opts.challenge === 'string' ? opts.challenge.trim() : ''
const RUN_ID = typeof opts.runId === 'string' ? opts.runId.trim() : ''
if (!CHALLENGE) return { status: 'error', reason: 'args.challenge is missing. Pass {challenge: "<text>", runId: "<YYYYMMDD-slug>"}.' }
if (!/^[0-9]{8}-[a-z0-9][a-z0-9-]*$/.test(RUN_ID)) return { status: 'error', reason: 'args.runId must look like 20260920-short-name (the script cannot read the clock).' }

const RUN_DIR = `runs/${RUN_ID}`
const MAX_ATTEMPTS = 2 // one attempt plus one repair
const MAX_STEPS_PER_PIECE = 3
let agentsUsed = 0

// Blueprint check (method 3.1). A task that changes a product needs a fixed target: the blueprint sections it depends
// on, settled by EJ, and acceptance criteria that end the run.
const SECTIONS = ['vision', 'requirements', 'domain model', 'business logic', 'architecture', 'data model', 'ui/ux', 'non-functional']
const NOT_A_PRODUCT_CHANGE = 'not a product change'
const TASK_KINDS = [NOT_A_PRODUCT_CHANGE, 'fix', 'feature', 'new product']
const MUST_NEED = { fix: ['requirements'], feature: ['vision', 'requirements'], 'new product': SECTIONS }

const COMMON = `
You are one step of the intake workflow in this repository. Method: docs/WORKFLOW_DESIGN_METHOD.md.
Templates: docs/workflow-templates/. Run folder: ${RUN_DIR}/ (state file: ${RUN_DIR}/state.md).

Rules for every step:
- Do only your own step. Design only: do NOT start solving the challenge itself.
- Create or change files only inside ${RUN_DIR}/. Change nothing else in the repository.
- Except for step 1, read ${RUN_DIR}/state.md first. When you finish, set your step's status in its step table and
  append one log line (get the date with \`date +%F\`). The state file holds progress and results, never reasoning.
- Evidence comes from running a command or reading a file in this session, not from recollection.

The challenge, verbatim:
"""
${CHALLENGE}
"""
`

const READY_SCHEMA = {
  type: 'object',
  properties: {
    state_file: { type: 'string' },
    readiness_file: { type: 'string' },
    tools_checked: { type: 'integer', description: 'how many tools you actually ran a command for' },
    missing: {
      type: 'array',
      description: 'tools, skills or information that are missing or unverified; empty if none',
      items: {
        type: 'object',
        properties: { item: { type: 'string' }, effect: { type: 'string', enum: ['organise piece', 'verify piece', 'research piece', 'export to a file', 'ask EJ'] } },
        required: ['item', 'effect'],
      },
    },
    blueprint: {
      type: 'object',
      properties: {
        task_kind: { type: 'string', enum: TASK_KINDS },
        reason: { type: 'string', description: 'one line: why the task is of this kind' },
        map: { type: 'string', description: "path to the product's docs/blueprint/README.md; empty if there is none" },
        sections: {
          type: 'array',
          description: 'one entry per section; empty for a task that is not a product change',
          items: {
            type: 'object',
            properties: {
              section: { type: 'string', enum: SECTIONS },
              needed: { type: 'boolean', description: 'does this task depend on the section' },
              status: { type: 'string', enum: ['settled', 'draft', 'incomplete', 'missing'], description: 'judged for this task: settled = accepted by EJ and covers the task; draft = covers it, not accepted; incomplete = does not cover it' },
              file: { type: 'string', description: 'where the section is; empty if missing' },
            },
            required: ['section', 'needed', 'status', 'file'],
          },
        },
      },
      required: ['task_kind', 'reason', 'map', 'sections'],
    },
  },
  required: ['state_file', 'readiness_file', 'tools_checked', 'missing', 'blueprint'],
}

const ALGO_SCHEMA = {
  type: 'object',
  properties: {
    algorithm_file: { type: 'string' },
    steps: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string', description: 's1, s2, ...' },
          action: { type: 'string', description: 'one action with a result that can be checked' },
          clear: { type: 'boolean', description: 'false if you cannot write this step clearly yet' },
          check: { type: 'string', description: 'how we know the step is done; empty if you cannot name one' },
          check_kind: { type: 'string', enum: ['script', 'judged', 'ej', 'none'] },
        },
        required: ['id', 'action', 'clear', 'check', 'check_kind'],
      },
    },
    unclear_spots: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string', description: 'u1, u2, ...' },
          what: { type: 'string' },
          kind: { type: 'string', enum: ['information', 'decision', 'unknown'] },
          blocks: { type: 'array', items: { type: 'string' }, description: 'step ids that cannot start until this is resolved' },
          depends_on: { type: 'array', items: { type: 'string' }, description: 'spot ids whose answer could remove or change this one' },
          blueprint_section: { type: 'string', enum: ['', ...SECTIONS], description: 'the blueprint section this spot is about; empty if none' },
          question: { type: 'string', description: 'for kind decision: the question for EJ' },
          assumption: { type: 'string', description: 'for kind decision: the provisional assumption if EJ does not answer' },
        },
        required: ['id', 'what', 'kind', 'blueprint_section', 'blocks', 'depends_on'],
      },
    },
    risk: { type: 'string', enum: ['low', 'high'], description: 'high if a mistake would be noticed late, cannot be undone, or touches many things' },
    risk_reason: { type: 'string' },
  },
  required: ['algorithm_file', 'steps', 'unclear_spots', 'risk', 'risk_reason'],
}

const PROMPT_SCHEMA = {
  type: 'object',
  properties: {
    output_file: { type: 'string' },
    task: { type: 'string' },
    steps: { type: 'array', items: { type: 'string' } },
    check: { type: 'string' },
    check_kind: { type: 'string', enum: ['script', 'judged', 'ej'] },
    independent_check: { type: 'string', description: 'empty unless the task is risky' },
    acceptance_criteria: { type: 'array', items: { type: 'string' }, description: 'for a product change: the criteria in scope (R1.1, ...); the check is these passing' },
    questions_for_ej: {
      type: 'array',
      description: 'one entry per decision spot; empty if there are none',
      items: {
        type: 'object',
        properties: {
          spot: { type: 'string' }, question: { type: 'string' }, assumption: { type: 'string' },
          must_answer: { type: 'boolean', description: 'true for a blueprint question: nothing that builds runs until EJ answers it' },
        },
        required: ['spot', 'question', 'assumption', 'must_answer'],
      },
    },
  },
  required: ['output_file', 'task', 'steps', 'check', 'check_kind', 'independent_check', 'acceptance_criteria', 'questions_for_ej'],
}

const DESIGN_SCHEMA = {
  type: 'object',
  properties: {
    output_file: { type: 'string' },
    pieces: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string', description: 'p1, p2, ...' },
          name: { type: 'string' },
          steps: { type: 'array', items: { type: 'string' } },
          over_three_reason: { type: 'string', description: 'empty unless the piece has more than 3 steps' },
          pattern: { type: 'string', enum: ['step', 'loop', 'explore'] },
          resolves_spot: { type: 'string', description: 'unclear spot id this piece resolves, else empty' },
          builds: { type: 'boolean', description: "true if the piece changes the product's code, schema, UI or configuration" },
          blueprint_sections: { type: 'array', items: { type: 'string', enum: SECTIONS }, description: 'the blueprint sections the piece depends on' },
          acceptance_criteria: { type: 'array', items: { type: 'string' }, description: 'for a piece that builds: the criteria it covers; its stop is these passing' },
          check: { type: 'string' },
          check_kind: { type: 'string', enum: ['script', 'judged', 'ej'] },
          attempt_limit: { type: 'integer', description: '1 for pattern step' },
          feedback: { type: 'string', description: 'what goes back to the agent on failure; empty for pattern step' },
          exit_on_limit: { type: 'string', description: 'where the piece goes when the limit is hit; empty for pattern step' },
          needs: { type: 'array', items: { type: 'string' }, description: 'piece ids whose result this piece needs' },
          intent: { type: 'string', description: 'contract: one sentence, why this piece exists' },
          stop: { type: 'string', description: 'contract: the observable condition that ends the piece' },
          returns: { type: 'string', description: 'contract: what comes back and in what shape' },
          files_touched: { type: 'array', items: { type: 'string' }, description: 'contract: paths the piece may create or edit' },
          must_not_change: { type: 'string', description: 'contract: what is off limits' },
          evidence: { type: 'string', description: 'the proof that comes back with the result: command and output, or file:line' },
          evidence_file: { type: 'string', description: 'the file the proof is saved in' },
          state_reads: { type: 'string', description: 'what it takes from the state file before it starts' },
          state_writes: { type: 'string', description: 'what it records in the state file when it finishes' },
          brief_given: { type: 'string', description: 'context: exactly what the agent is given' },
          brief_withheld: { type: 'string', description: 'context: what it must not see' },
        },
        required: ['id', 'name', 'steps', 'over_three_reason', 'pattern', 'resolves_spot', 'builds', 'blueprint_sections', 'acceptance_criteria', 'check', 'check_kind', 'attempt_limit', 'feedback', 'exit_on_limit', 'needs', 'intent', 'stop', 'returns', 'files_touched', 'must_not_change', 'evidence', 'evidence_file', 'state_reads', 'state_writes', 'brief_given', 'brief_withheld'],
      },
    },
    order: { type: 'array', items: { type: 'string' }, description: 'every piece id once, in the sequential order they run' },
    joins: { type: 'array', items: { type: 'string' } },
    parallel_candidates: {
      type: 'array',
      description: 'optional, decided last; only groups for which all five points hold',
      items: {
        type: 'object',
        properties: {
          pieces: { type: 'array', items: { type: 'string' } },
          no_result_needed: { type: 'boolean' },
          no_shared_resources: { type: 'boolean' },
          no_method_change: { type: 'boolean' },
          own_checks: { type: 'boolean' },
          worth_the_join: { type: 'boolean' },
        },
        required: ['pieces', 'no_result_needed', 'no_shared_resources', 'no_method_change', 'own_checks', 'worth_the_join'],
      },
    },
    questions_for_ej: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          spot: { type: 'string', description: 'unclear spot id, or empty' }, question: { type: 'string' }, assumption: { type: 'string' },
          must_answer: { type: 'boolean', description: 'true for a blueprint question: nothing that builds runs until EJ answers it' },
        },
        required: ['spot', 'question', 'assumption', 'must_answer'],
      },
    },
    acceptance_criteria: { type: 'array', items: { type: 'string' }, description: 'for a product change: every criterion in scope (R1.1, ...); the success criteria and the only stop target' },
    agent_count: { type: 'integer' },
    cost_estimate: { type: 'string' },
    success_criteria: { type: 'string' },
  },
  required: ['output_file', 'pieces', 'order', 'joins', 'parallel_candidates', 'questions_for_ej', 'acceptance_criteria', 'agent_count', 'cost_estimate', 'success_criteria'],
}

const VERIFY_ITEMS = [
  ['V1', 'The output file exists at the stated path and has the headings of its template in docs/workflow-templates/.'],
  ['V2', 'The output file says the same as the structured data below: same steps or pieces, same checks, same order, same questions.'],
  ['V3', 'Every check of kind "script" names a command or file that exists here (use `command -v`, `ls`, or a dry run; run nothing that changes anything).'],
  ['V4', 'state.md is complete: the challenge verbatim, the baseline, the Blueprint section, every finished step marked done with its output file, the size decision, the unclear spots and the questions for EJ matching the data below, one log line per finished step.'],
  ['V5', 'Every file named in a brief or in "what you need" exists.'],
  ['V6', '`git status --short` now differs from the baseline recorded in state.md only by paths under runs/.'],
  ['V7', 'readiness.md has a Blueprint section that matches the blueprint data below, and its kind of task fits the challenge (a challenge that changes code, schema, UI or configuration is not "not a product change"). For a product change: every section marked settled says so in its file, and every acceptance criterion named in the data is either written in the requirements or non-functional section, or named as a criterion that a blueprint piece in the design is to propose.'],
]

const VERIFY_SCHEMA = {
  type: 'object',
  properties: {
    check_file: { type: 'string' },
    items: {
      type: 'array',
      items: {
        type: 'object',
        properties: { id: { type: 'string' }, pass: { type: 'boolean' }, note: { type: 'string', description: 'what you ran or read; required when pass is false' } },
        required: ['id', 'pass', 'note'],
      },
    },
  },
  required: ['check_file', 'items'],
}

// ---- objective checks (plain code: free, repeatable, cannot be argued with) ----

const has = v => typeof v === 'string' && v.trim().length > 0
const dupes = ids => ids.filter((id, i) => ids.indexOf(id) !== i)

function hasCycle(ids, edgesOf) {
  const mark = {}
  const visit = id => {
    if (mark[id] === 'done') return false
    if (mark[id] === 'open') return true
    mark[id] = 'open'
    const hit = (edgesOf(id) || []).some(visit)
    mark[id] = 'done'
    return hit
  }
  return ids.some(visit)
}

const isChange = bp => !!bp && bp.task_kind !== NOT_A_PRODUCT_CHANGE
const mentions = (text, id) => typeof text === 'string' && new RegExp(`(^|[^A-Za-z0-9.])${id.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}($|[^0-9])`).test(text)
const neededSections = bp => ((bp && bp.sections) || []).filter(x => x.needed)
const unsettledSections = bp => neededSections(bp).filter(x => x.status !== 'settled')

function checkBlueprint(bp) {
  const f = []
  if (!bp) return ['blueprint: readiness did not report the blueprint check']
  const secs = bp.sections || []
  for (const d of new Set(dupes(secs.map(x => x.section)))) f.push(`blueprint: section ${d} is listed twice`)
  if (!has(bp.reason)) f.push('blueprint: no reason is given for the kind of task')
  if (!isChange(bp)) {
    if (secs.some(x => x.needed)) f.push('blueprint: a task that is not a product change needs no sections')
    return f
  }
  for (const m of MUST_NEED[bp.task_kind] || []) {
    if (!secs.some(x => x.section === m && x.needed)) f.push(`blueprint: a ${bp.task_kind} needs the ${m} section`)
  }
  for (const x of secs) if (x.status !== 'missing' && !has(x.file)) f.push(`blueprint: section ${x.section} is ${x.status} but names no file`)
  return f
}

function checkAlgorithm(a, bp) {
  const f = []
  const steps = a.steps || [], spots = a.unclear_spots || []
  if (!steps.length) f.push('algorithm: there are no steps')
  const stepIds = steps.map(s => s.id), spotIds = spots.map(s => s.id)
  for (const d of new Set(dupes(stepIds))) f.push(`step id ${d} is used twice`)
  for (const d of new Set(dupes(spotIds))) f.push(`spot id ${d} is used twice`)
  for (const s of steps) {
    const unclear = !s.clear || !has(s.check) || s.check_kind === 'none'
    const covered = spots.some(p => (p.blocks || []).includes(s.id))
    if (unclear && !covered) f.push(`step ${s.id}: it is not clear or names no check, but no unclear spot blocks it`)
  }
  for (const p of spots) {
    if (!(p.blocks || []).length) f.push(`spot ${p.id}: it blocks no step`)
    for (const b of p.blocks || []) if (!stepIds.includes(b)) f.push(`spot ${p.id}: blocks unknown step ${b}`)
    for (const d of p.depends_on || []) if (d === p.id || !spotIds.includes(d)) f.push(`spot ${p.id}: depends on unknown spot ${d}`)
    if (p.kind === 'decision' && !(has(p.question) && has(p.assumption))) f.push(`spot ${p.id}: a decision needs a question for EJ and a provisional assumption`)
  }
  if (hasCycle(spotIds, id => (spots.find(p => p.id === id) || {}).depends_on)) f.push('unclear spots: depends_on contains a cycle')
  if (a.risk === 'high' && !has(a.risk_reason)) f.push('risk is high but no reason is given')
  // A draft section is a question for EJ; an incomplete or missing one is information a blueprint piece must produce.
  const unsettled = unsettledSections(bp)
  for (const x of unsettled) {
    const kind = x.status === 'draft' ? 'decision' : 'information'
    if (!spots.some(p => p.blueprint_section === x.section && p.kind === kind)) f.push(`blueprint section ${x.section} is ${x.status}: it needs an unclear spot of kind ${kind}`)
  }
  for (const p of spots) {
    if (has(p.blueprint_section) && !unsettled.some(x => x.section === p.blueprint_section)) f.push(`spot ${p.id}: ${p.blueprint_section} is not a needed, unsettled blueprint section`)
  }
  return f
}

function checkPrompt(p, algo, bp) {
  const f = []
  if (!has(p.output_file) || !p.output_file.includes(RUN_DIR)) f.push(`prompt: output_file must be inside ${RUN_DIR}/`)
  if (!has(p.task)) f.push('prompt: the task is empty')
  const n = (p.steps || []).length
  if (n < 1 || n > MAX_STEPS_PER_PIECE) f.push(`prompt: it has ${n} steps; a prompt file has 1 to ${MAX_STEPS_PER_PIECE}`)
  if (!has(p.check)) f.push('prompt: it names no check')
  if (algo.risk === 'high' && !has(p.independent_check)) f.push('prompt: the task is risky but there is no independent check')
  const criteria = p.acceptance_criteria || []
  if (isChange(bp) && !criteria.length) f.push('prompt: a product change must name the acceptance criteria in scope')
  if (!isChange(bp) && criteria.length) f.push('prompt: the task is not a product change, so it has no acceptance criteria')
  for (const c of criteria) if (!mentions(p.check, c)) f.push(`prompt: the check does not name criterion ${c}`)
  for (const s of algo.unclear_spots || []) {
    const q = (p.questions_for_ej || []).find(q => q.spot === s.id && has(q.question) && has(q.assumption))
    if (!q) f.push(`spot ${s.id}: a decision must appear in the questions for EJ with an assumption`)
    else if (has(s.blueprint_section) && !q.must_answer) f.push(`spot ${s.id}: a blueprint question must be marked must_answer`)
  }
  return f
}

function checkDesign(d, algo, bp) {
  const f = []
  const pieces = d.pieces || [], ids = pieces.map(p => p.id)
  const byId = Object.fromEntries(pieces.map(p => [p.id, p]))
  if (!has(d.output_file) || !d.output_file.includes(RUN_DIR)) f.push(`design: output_file must be inside ${RUN_DIR}/`)
  if (!pieces.length) f.push('design: there are no pieces')
  for (const x of new Set(dupes(ids))) f.push(`piece id ${x} is used twice`)
  for (const p of pieces) {
    const n = (p.steps || []).length
    if (n < 1) f.push(`piece ${p.id}: it has no steps`)
    if (n > MAX_STEPS_PER_PIECE && !has(p.over_three_reason)) f.push(`piece ${p.id}: ${n} steps and no reason for more than ${MAX_STEPS_PER_PIECE}`)
    if (!has(p.check)) f.push(`piece ${p.id}: it names no check`)
    if (p.pattern !== 'step') {
      if (!(p.attempt_limit >= 1)) f.push(`piece ${p.id}: a ${p.pattern} needs an attempt limit`)
      if (!has(p.feedback)) f.push(`piece ${p.id}: a ${p.pattern} needs the feedback that goes back on failure`)
      if (!has(p.exit_on_limit)) f.push(`piece ${p.id}: a ${p.pattern} needs an exit for when the limit is hit`)
    }
    for (const x of p.needs || []) if (x === p.id || !ids.includes(x)) f.push(`piece ${p.id}: needs unknown piece ${x}`)
    if (!has(p.brief_given)) f.push(`piece ${p.id}: the context (what the agent is given) is empty`)
    if (!has(p.intent)) f.push(`piece ${p.id}: the contract has no intent`)
    if (!has(p.stop)) f.push(`piece ${p.id}: the contract has no stop condition`)
    if (!has(p.returns)) f.push(`piece ${p.id}: the contract does not say what the piece returns`)
    if (!has(p.must_not_change)) f.push(`piece ${p.id}: the contract does not say what must not change`)
    if (!has(p.evidence)) f.push(`piece ${p.id}: it names no evidence that comes back with the result`)
    if (!has(p.evidence_file)) f.push(`piece ${p.id}: it does not say where the evidence is saved`)
    if (!has(p.state_reads)) f.push(`piece ${p.id}: it does not say what it reads from the state file`)
    if (!has(p.state_writes)) f.push(`piece ${p.id}: it does not say what it writes to the state file`)
  }
  if (hasCycle(ids, id => (byId[id] || {}).needs)) f.push('pieces: needs contains a cycle')

  const order = d.order || []
  if (order.length !== ids.length || ids.some(id => !order.includes(id))) f.push('order: it must list every piece exactly once')
  for (const p of pieces) for (const x of p.needs || []) {
    if (order.includes(p.id) && order.includes(x) && order.indexOf(x) > order.indexOf(p.id)) f.push(`order: ${p.id} runs before ${x}, whose result it needs`)
  }

  const questions = d.questions_for_ej || []
  for (const s of algo.unclear_spots || []) {
    if (s.kind === 'decision') {
      const q = questions.find(q => q.spot === s.id && has(q.question) && has(q.assumption))
      if (!q) f.push(`spot ${s.id}: a decision must appear in the questions for EJ with an assumption`)
      else if (has(s.blueprint_section) && !q.must_answer) f.push(`spot ${s.id}: a blueprint question must be marked must_answer`)
    } else if (!pieces.some(p => p.resolves_spot === s.id)) f.push(`spot ${s.id}: no piece resolves it`)
  }

  const reach = (from, to, seen = new Set()) => {
    if (seen.has(from)) return false
    seen.add(from)
    return ((byId[from] || {}).needs || []).some(x => x === to || reach(x, to, seen))
  }

  // Blueprint: a piece that builds stops at its acceptance criteria and waits for the sections it depends on.
  const change = isChange(bp)
  const inScope = d.acceptance_criteria || []
  const needed = neededSections(bp)
  const spots = algo.unclear_spots || []
  if (change && !inScope.length) f.push('design: a product change must list the acceptance criteria in scope')
  if (!change && inScope.length) f.push('design: the task is not a product change, so it has no acceptance criteria')
  for (const c of inScope) if (!mentions(d.success_criteria, c)) f.push(`design: the success criteria do not name criterion ${c}`)
  for (const p of pieces) {
    const spot = spots.find(s => s.id === p.resolves_spot)
    if (spot && has(spot.blueprint_section) && spot.kind === 'information' && p.check_kind !== 'ej') f.push(`piece ${p.id}: it drafts the ${spot.blueprint_section} section, which is settled only when EJ accepts it, so its check must be EJ's`)
    if (!p.builds) continue
    if (!change) { f.push(`piece ${p.id}: it builds, but readiness says the task is not a product change`); continue }
    if (!(p.acceptance_criteria || []).length) f.push(`piece ${p.id}: it builds but names no acceptance criteria`)
    for (const c of p.acceptance_criteria || []) {
      if (!inScope.includes(c)) f.push(`piece ${p.id}: criterion ${c} is not in the design's acceptance criteria`)
      // The stop is the criteria, not an open-ended review; a judged check is a checklist of the same criteria.
      if (!mentions(p.stop, c)) f.push(`piece ${p.id}: its stop condition does not name criterion ${c}`)
      if (p.check_kind === 'judged' && !mentions(p.check, c)) f.push(`piece ${p.id}: a judged check must be a checklist of its criteria, and it does not name ${c}`)
    }
    if (!(p.blueprint_sections || []).length) f.push(`piece ${p.id}: it builds but names no blueprint section it depends on`)
    for (const sec of p.blueprint_sections || []) {
      const x = needed.find(y => y.section === sec)
      if (!x) { f.push(`piece ${p.id}: it depends on the ${sec} section, which readiness did not mark as needed`); continue }
      if (x.status !== 'missing' && x.status !== 'incomplete') continue
      const drafter = pieces.find(q => spots.some(s => s.id === q.resolves_spot && s.blueprint_section === sec))
      if (!drafter || !reach(p.id, drafter.id)) f.push(`piece ${p.id}: it builds on the ${x.status} ${sec} section but does not need the piece that drafts it`)
    }
  }
  if (change) {
    for (const c of inScope) if (!pieces.some(p => p.builds && (p.acceptance_criteria || []).includes(c))) f.push(`criterion ${c}: no piece that builds covers it`)
  }
  for (const c of d.parallel_candidates || []) {
    const name = (c.pieces || []).join('+')
    if ((c.pieces || []).length < 2) f.push(`parallel candidate ${name}: it needs at least two pieces`)
    for (const x of c.pieces || []) if (!ids.includes(x)) f.push(`parallel candidate ${name}: unknown piece ${x}`)
    if (!(c.no_result_needed && c.no_shared_resources && c.no_method_change && c.own_checks && c.worth_the_join)) f.push(`parallel candidate ${name}: not all five points hold, so it stays sequential`)
    for (const a of c.pieces || []) for (const b of c.pieces || []) {
      if (a >= b || !byId[a] || !byId[b]) continue
      if (reach(a, b) || reach(b, a)) f.push(`parallel candidate ${name}: ${a} and ${b} are linked by needs`)
      const shared = (byId[a].files_touched || []).filter(x => (byId[b].files_touched || []).includes(x))
      if (shared.length) f.push(`parallel candidate ${name}: ${a} and ${b} both touch ${shared.join(', ')}`)
    }
  }

  if (!(d.agent_count >= 1)) f.push('predictability: the agent count is missing')
  if (!has(d.cost_estimate)) f.push('predictability: the cost estimate is missing')
  if (!has(d.success_criteria)) f.push('predictability: the success criteria are missing')
  return f
}

function checkVerdict(v) {
  const f = []
  for (const [id] of VERIFY_ITEMS) {
    const item = (v.items || []).find(i => i.id === id)
    if (!item) f.push(`${id}: the verifier did not report it`)
    else if (!item.pass) f.push(`${id}: ${item.note || 'failed, no note'}`)
  }
  return f
}

// ---- prompts ----

const feedbackBlock = failed => failed.length
  ? `\nYour previous attempt failed these checks. Fix exactly these, in the file and in your returned data:\n- ${failed.join('\n- ')}\n`
  : ''

const readyPrompt = failed => `${COMMON}
STEP 1 — intake, readiness and the blueprint check.${failed.length ? `
This is a repair attempt: ${RUN_DIR}/state.md and readiness.md already exist. Keep the baseline and the log lines in
state.md as they are; fix only the failed items listed at the end, in readiness.md, state.md and your returned data.` : ''}
1. BEFORE creating anything, run \`git status --short\` and keep the output.
2. Create ${RUN_DIR}/state.md from docs/workflow-templates/state.md: the run id, the challenge verbatim, the baseline
   output from 1.
3. Create ${RUN_DIR}/readiness.md from docs/workflow-templates/readiness.md. Tools: run a command for each one the
   challenge will need. Skills: list the ones that apply. Information: where it is, what structure it is in, whether
   you verified it against its source, and which agents and tools can read it.
4. Blueprint check (method 3.1; layout docs/workflow-templates/blueprint.md). Decide the kind of task:
   "${NOT_A_PRODUCT_CHANGE}" (research, a question, an analysis, an edit to documentation only), "fix" (restores
   behaviour the requirements already describe), "feature" (adds or changes behaviour) or "new product". For a product
   change, find the product's blueprint map (docs/blueprint/README.md in its repository) and, for each of the eight
   sections (${SECTIONS.join(', ')}), whether this task depends on it and its status FOR THIS TASK: settled (the file
   says EJ accepted it, and it covers what the task needs), draft (covers the task, but not accepted), incomplete
   (exists, accepted or not, but does not cover the task — e.g. no requirement for this feature yet), or missing. A fix needs at least the requirements; a feature at least the vision and the requirements; a new
   product all eight. Read the files; do not assume. Fill in the Blueprint section of readiness.md and of state.md.
5. Mark step 1 done in state.md and add the log line.
${feedbackBlock(failed)}`

const algoPrompt = failed => `${COMMON}
STEP 2 — write the algorithm and list ALL the unclear spots. Read ${RUN_DIR}/readiness.md as well.
- Write the steps that would solve the challenge. A step is one action with a result that can be checked. Give each
  step its check and the kind of check (script is best; judged = a fixed checklist judged by a separate agent; ej =
  EJ's own judgment). If you cannot write a step clearly, or cannot name its check, set clear=false or check_kind=none.
- Every step that is not clear must be blocked by an unclear spot. List every spot BEFORE thinking about how to
  resolve any: what is unclear, its kind (information / decision / unknown), which steps it blocks, and which other
  spot it depends on. A decision needs the question for EJ and a provisional assumption.
- Items marked missing in readiness.md are unclear spots of kind information unless they are decisions.
- Blueprint (readiness.md, Blueprint section): every NEEDED section that is not settled is an unclear spot with its
  blueprint_section set to exactly one of: ${SECTIONS.join(', ')}. A draft section is kind decision: the question is
  "accept this section as written?" and the draft is the provisional assumption. An incomplete or missing section is
  kind information: a blueprint piece will draft the missing part. Such a spot blocks every step that builds on the
  section. Leave blueprint_section empty for every other spot.
- Judge risk separately from size: high if a mistake would be noticed late, cannot be undone, or touches many things.
- Do not resolve anything. Do not split into pieces yet.
Write ${RUN_DIR}/algorithm.md (steps table, unclear-spots table, risk), copy the unclear spots and the questions for
EJ into state.md, mark step 2 done, add the log line.
${feedbackBlock(failed)}`

const smallPrompt = (algo, bp, failed) => `${COMMON}
STEP 4 — this is a SMALL task (${algo.steps.length} steps, ${algo.unclear_spots.length} decision(s) with a default answer, nothing else unclear, risk ${algo.risk}). Write the prompt file.
Record in state.md: size decision "small — steps: ${algo.steps.length}, unclear spots: ${algo.unclear_spots.length} (decisions only), risk: ${algo.risk}", and mark step 3 done.
Create ${RUN_DIR}/prompt.md from docs/workflow-templates/prompt-file.md using ${RUN_DIR}/algorithm.md: every decision
as a question for EJ at the top with its provisional assumption, the task, the steps (at most ${MAX_STEPS_PER_PIECE},
written on the provisional assumptions), exactly what is needed, the check${algo.risk === 'high' ? ', and an independent check because the task is risky' : ''}.
A question about a blueprint section is must_answer: no step that builds runs until EJ answers it; say so in the file.
${isChange(bp) ? `This is a product change: name the acceptance criteria in scope (R1.1, ...). The check names each of them and how
it is checked, plus: what passed before still passes, and nothing off limits changed. A failure of any of these is a
failure, not a backlog item. Anything else found (a new wish, an improvement, a gap no criterion covers) goes to the
product's docs/blueprint/backlog.md.` : 'This task is not a product change: acceptance_criteria is an empty list.'}
Mark step 4 done and add the log line.
${feedbackBlock(failed)}`

const designPrompt = (algo, bp, failed) => `${COMMON}
STEP 4 — this task needs a WORKFLOW DESIGN (${algo.steps.length} steps, ${algo.unclear_spots.length} unclear spots, risk ${algo.risk}).
Record in state.md: size decision "design — steps: ${algo.steps.length}, unclear spots: ${algo.unclear_spots.length}, risk: ${algo.risk}", and mark step 3 done.
Create ${RUN_DIR}/workflow-design.md from docs/workflow-templates/workflow-design.md, using ${RUN_DIR}/algorithm.md
and ${RUN_DIR}/readiness.md. Follow docs/WORKFLOW_DESIGN_METHOD.md sections 3.4 to 3.7:
- Group the steps into right-sized pieces: at most ${MAX_STEPS_PER_PIECE} steps each unless you give a reason; split only
  if each part keeps its own check and splitting changes how the work is done.
- Every unclear spot of kind information or unknown gets a piece that resolves it (research = pattern step or loop;
  unknown = pattern explore, bounded). Every decision goes to the questions for EJ with its provisional assumption.
- Clear pieces with a script check are loops: attempt limit, the feedback that goes back, the exit when the limit is hit.
- Put the pieces in ONE sequential order in which every piece comes after the pieces it needs. Sequential is the default.
- Only after that, list parallel candidates, and only where all five points hold. An empty list is a good answer.
- Every piece carries five things (method section 3.6). Tools. Context: exactly what its agent is given and what is
  withheld. Contract: the intent, the observable stop condition, what it returns and in what shape, what it may change
  and what it must not. Evidence: the proof that comes back with the result (a command and its output, or file:line)
  and the file it is saved in; a verifier reads the evidence, never the worker's reasoning. State: what the piece
  reads from the state file and what it writes back. Borrow names from ancient_games/schema.py where they fit.
- A piece that needs another piece gets that piece's returns and evidence as part of its context.
- Blueprint (readiness.md, Blueprint section; method 3.1 and 3.6). ${isChange(bp) ? `This is a product change.
  Mark every piece that changes the product's code, schema, UI or configuration as builds=true. A piece that builds
  names the blueprint sections it depends on and the acceptance criteria it covers (R1.1, ...). Its stop condition
  names each of those criteria and has three parts: they pass; what passed before still passes (existing tests,
  criteria of settled requirements); its must-not-change holds. A failure of any part is a failed attempt. A judged
  check is a checklist of those criteria, never an open-ended review. List every criterion in scope at the top level
  and name each in the success criteria; every one of them is covered by a piece that builds. An incomplete or
  missing section gets a blueprint piece that drafts the missing part into the product's docs/blueprint/ from the
  sections above it; its check is EJ's (check_kind ej), because only EJ settles a section; every piece that builds on
  that section needs it. If that piece is to write the requirements, list the criteria you expect it to propose. A
  draft section is a question for EJ with must_answer=true. Anything else found (a new wish, an improvement, a gap no
  criterion covers) goes to the product's docs/blueprint/backlog.md, never into new pieces or attempts of this run.` : 'This task is not a product change: no piece builds, and acceptance_criteria is an empty list.'}
- Fill in predictability (agent count, cost estimate and its basis, success criteria), debuggability and quality control.
Return the same design as structured data. Mark step 4 done and add the log line.
${feedbackBlock(failed)}`

const verifyPrompt = (kind, data, bp, jsFailed) => `${COMMON}
STEP 5 — verify. You did not see how the ${kind} was made; judge only the files in ${RUN_DIR}/ and the data below.
Report every item below with pass true or false. Pass means you checked it yourself in this session by reading or
running something; if you are unsure it is false. Say in the note what you ran or read. Do not add items of your own.
${VERIFY_ITEMS.map(([id, text]) => `- ${id}: ${text}`).join('\n')}
${jsFailed.length ? `\nThe script's own checks already failed on these; record them in check.md as failed:\n- ${jsFailed.join('\n- ')}\n` : ''}
Write ${RUN_DIR}/check.md with one line per item. In state.md set step 5 to done if every item passed and the
script's checks passed, otherwise to blocked with the failed item ids, and add the log line.

Structured data:
${JSON.stringify(data, null, 2)}

Blueprint data from readiness (for V7):
${JSON.stringify(bp, null, 2)}`

// ---- run ----

const run = async (prompt, o) => { agentsUsed++; return agent(prompt, o) }
const fail = (step, reason, extra) => ({ status: 'error', step, reason, run_dir: RUN_DIR, agents_used: agentsUsed, ...extra })

phase('Readiness')
let ready = null, failed = []
for (let n = 1; n <= MAX_ATTEMPTS; n++) {
  ready = await run(readyPrompt(failed), { label: `1-readiness#${n}`, phase: 'Readiness', schema: READY_SCHEMA })
  if (!ready) return fail(1, 'The readiness agent returned nothing.')
  failed = checkBlueprint(ready.blueprint)
  if (!failed.length) break
  log(`Readiness attempt ${n}/${MAX_ATTEMPTS}: ${failed.length} blueprint check(s) failed`)
}
if (failed.length) return { status: 'unverified', step: 1, run_dir: RUN_DIR, failed_items: failed, agents_used: agentsUsed }
const bp = ready.blueprint
if (ready.missing.length) log(`Readiness: ${ready.missing.length} item(s) missing or unverified`)
const notSettled = unsettledSections(bp)
log(`Blueprint: ${bp.task_kind}${notSettled.length ? `; not settled: ${notSettled.map(x => `${x.section} (${x.status})`).join(', ')}` : ''}`)

phase('Algorithm')
let algo = null
failed = []
for (let n = 1; n <= MAX_ATTEMPTS; n++) {
  algo = await run(algoPrompt(failed), { label: `2-algorithm#${n}`, phase: 'Algorithm', schema: ALGO_SCHEMA })
  if (!algo) return fail(2, 'The algorithm agent returned nothing.')
  failed = checkAlgorithm(algo, bp)
  if (!failed.length) break
  log(`Algorithm attempt ${n}/${MAX_ATTEMPTS}: ${failed.length} check(s) failed`)
}
if (failed.length) return { status: 'unverified', step: 2, run_dir: RUN_DIR, failed_items: failed, agents_used: agentsUsed }

// Size decision: the script decides, from the counts.
// A decision with a provisional assumption does not make a task big: it goes to the top of the prompt file.
const blocking = algo.unclear_spots.filter(s => s.kind !== 'decision')
const small = algo.steps.length <= MAX_STEPS_PER_PIECE && blocking.length === 0
const kind = small ? 'prompt file' : 'workflow design'
log(`Size: ${algo.steps.length} step(s), ${algo.unclear_spots.length} unclear spot(s) of which ${blocking.length} not a decision, risk ${algo.risk} -> ${kind}`)

let out = null
failed = []
for (let n = 1; n <= MAX_ATTEMPTS; n++) {
  out = await run(small ? smallPrompt(algo, bp, failed) : designPrompt(algo, bp, failed),
    { label: `4-${small ? 'prompt' : 'design'}#${n}`, phase: 'Design', schema: small ? PROMPT_SCHEMA : DESIGN_SCHEMA })
  if (!out) return fail(4, `The ${kind} agent returned nothing.`)
  const jsFailed = small ? checkPrompt(out, algo, bp) : checkDesign(out, algo, bp)
  // Skip the verifier while a repair attempt remains and the free checks already failed.
  if (jsFailed.length && n < MAX_ATTEMPTS) {
    failed = jsFailed
    log(`${kind} attempt ${n}/${MAX_ATTEMPTS}: ${failed.length} script check(s) failed`)
    continue
  }
  const verdict = await run(verifyPrompt(kind, out, bp, jsFailed), { label: `5-verify#${n}`, phase: 'Check', schema: VERIFY_SCHEMA })
  failed = jsFailed.concat(verdict ? checkVerdict(verdict) : ['The verifier returned nothing, so the attempt is unverified.'])
  if (!failed.length) break
  log(`${kind} attempt ${n}/${MAX_ATTEMPTS}: ${failed.length} check(s) failed`)
}

return {
  status: failed.length ? 'unverified' : 'verified',
  size: small ? 'small' : 'design',
  run_dir: RUN_DIR,
  output_file: out.output_file,
  steps: algo.steps.length,
  unclear_spots: algo.unclear_spots.map(s => ({ id: s.id, kind: s.kind, what: s.what })),
  questions_for_ej: out.questions_for_ej,
  missing_at_readiness: ready.missing,
  blueprint: { task_kind: bp.task_kind, not_settled: notSettled.map(x => ({ section: x.section, status: x.status })) },
  acceptance_criteria: out.acceptance_criteria,
  risk: algo.risk,
  failed_items: failed,
  agents_used: agentsUsed,
}
