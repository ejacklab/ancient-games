export const meta = {
  name: 'enhance-ancient-games',
  description: 'Plan one Ancient Games enhancement as a recorded per-segment planning decision, run it as a dependency graph with verify/repair loops, and report for owner approval',
  whenToUse: 'To design (default) or prototype an enhancement from 20260919-state.md. args: {goal, mode: "design"|"prototype", maxSegments, maxAttempts, stateFile}. Nothing is merged; prototypes stay in worktrees.',
  phases: [
    { title: 'Plan', detail: 'recheck the state file against the code, write the planning decision record, critic reviews it' },
    { title: 'Execute', detail: 'segments start as soon as their dependencies are verified' },
    { title: 'Verify', detail: 'independent refuters per segment; problems feed the repair attempt' },
    { title: 'Report', detail: 'completeness check and a report for the owner' },
  ],
}

// This workflow applies the policy that 20260919-state.md says Ancient Games lacks.
// Each decision is recorded per task segment instead of as one run-wide switch:
//   task structure    -> `depends_on`; the script starts a segment once its dependencies are verified
//   routing authority -> the script schedules; the planner only proposes. No peer handoff.
//   feedback cycle    -> `max_attempts` with `acceptance` as the stop condition
//   communication     -> every agent is an explicit invocation and control returns here;
//                        shared state is only the verified output of `depends_on` segments;
//                        verifiers never see the worker's method or each other (READ_SCOPE.deny).

const opts = typeof args === 'string' ? { goal: args } : (args || {})
const MODE = opts.mode === 'prototype' ? 'prototype' : 'design'
const MAX_SEGMENTS = opts.maxSegments || 3
const MAX_ATTEMPTS = opts.maxAttempts || 2
const MAX_PLAN_ROUNDS = 3
const STATE_FILE = opts.stateFile || '20260919-state.md'
const GOAL = opts.goal || [
  'Design the pre-execution planning decision proposed in the state file: a recorded, testable decision',
  'per task segment covering task structure (dependencies, parallel branches, checkpoints), routing',
  'authority, feedback cycle (loop bounds and stop condition) and communication (which state is shared',
  'and by whom, which handoffs are permitted, who holds control after each call). Include a check that',
  'forbids worker-to-worker sharing or handoff wherever claims must be independent sources.',
].join(' ')

const CONTEXT = `
Repository: Ancient Games, a standard-library Python framework that governs agent work (stages Gate, Guard,
Corroborate, Filter, Prove; a hybrid tool loop; a JSONL journal). Start from PROJECT_OVERVIEW.md. SPEC.md and
DECISIONS.md are the contract. ${STATE_FILE} is untracked, so it exists only in the main checkout, not in a worktree.

House rules:
- Never edit SPEC.md, DECISIONS.md, or registry stakes and ownership. Never write approval events or clear an owner
  or checkpoint gate. Where the work needs one of these, stop and list it as a question for the owner (EJ).
- Do not pre-empt an open owner decision. Build so that either answer still works, or list the question.
- No rule changes from a single run. Mark n=1 observations "not to be built on".
- Evidence comes from running a command or reading the code, never from recollection. Report skipped, failing or
  unrun checks as such.
- A code change counts as verified only after a sabotage check: a one-line mutation of the change makes a test fail,
  and the mutation is then reverted.
- Run the suite and commit as separate steps. Test command: env -u NO_COLOR python3 -m pytest -q
- Never modify or commit to the main checkout. ${MODE === 'design'
    ? 'This is a design run: change no files at all and return text only.'
    : 'Code changes happen only inside the worktree assigned to the segment, committed on its branch.'}
`

const SEGMENT = {
  type: 'object',
  properties: {
    id: { type: 'string', description: 'short kebab-case id' },
    goal: { type: 'string' },
    role: { type: 'string', enum: ['researcher', 'designer', 'coder', 'tester'] },
    depends_on: { type: 'array', items: { type: 'string' }, description: 'ids whose verified output this segment needs; empty means it can start at once' },
    inputs_from_deps: { type: 'string', description: 'what this segment reads from those outputs; "none" if no dependencies' },
    max_attempts: { type: 'integer', description: '1 when no feedback cycle is justified, otherwise the loop bound' },
    independent_sources_required: { type: 'boolean', description: 'true when the result will be relied on as corroborated; it then gets two verifiers who cannot see each other' },
    files: { type: 'array', items: { type: 'string' }, description: 'paths the segment reads or, in a prototype run, changes' },
    verify_cmd: { type: 'string', description: 'command whose result decides acceptance; empty for pure design' },
    acceptance: { type: 'string', description: 'observable condition that ends the loop' },
    rationale: { type: 'string', description: 'why this structure, this loop bound and these shared inputs' },
  },
  required: ['id', 'goal', 'role', 'depends_on', 'inputs_from_deps', 'max_attempts', 'independent_sources_required', 'acceptance', 'rationale'],
}

const PLAN_SCHEMA = {
  type: 'object',
  properties: {
    state_claims: {
      type: 'array',
      description: `claims in ${STATE_FILE} that the goal relies on, rechecked against the current code`,
      items: {
        type: 'object',
        properties: { claim: { type: 'string' }, still_true: { type: 'boolean' }, evidence: { type: 'string', description: 'file:line or command output' } },
        required: ['claim', 'still_true', 'evidence'],
      },
    },
    baseline: { type: 'string', description: 'pass/fail/skip counts from running the test command now' },
    owner_questions: { type: 'array', items: { type: 'string' }, description: 'open owner decisions this work touches and must not pre-empt' },
    segments: { type: 'array', items: SEGMENT },
  },
  required: ['state_claims', 'baseline', 'owner_questions', 'segments'],
}

const CRITIC_SCHEMA = {
  type: 'object',
  properties: { approved: { type: 'boolean' }, problems: { type: 'array', items: { type: 'string' } } },
  required: ['approved', 'problems'],
}

// Mirrors the project's return template: Method, Findings, Verdict, Not established, Follow-on.
const WORK_SCHEMA = {
  type: 'object',
  properties: {
    method: { type: 'string' },
    findings: { type: 'string', description: 'the deliverable itself: the design text, the research answer, or a summary of the diff' },
    claims: {
      type: 'array',
      items: {
        type: 'object',
        properties: { id: { type: 'string' }, statement: { type: 'string' }, evidence: { type: 'string', description: 'file:line, command and output, or "none"' } },
        required: ['id', 'statement', 'evidence'],
      },
    },
    not_established: { type: 'array', items: { type: 'string' } },
    follow_on: { type: 'array', items: { type: 'string' } },
    worktree_path: { type: 'string', description: 'absolute path from `git rev-parse --show-toplevel` if files were changed, else empty' },
    branch: { type: 'string', description: 'branch holding the committed change, else empty' },
    test_result: { type: 'string', description: 'command and pass/fail/skip counts, or "not run" with the reason' },
  },
  required: ['method', 'findings', 'claims', 'not_established', 'follow_on', 'test_result'],
}

const VERDICT_SCHEMA = {
  type: 'object',
  properties: {
    pass: { type: 'boolean' },
    problems: { type: 'array', items: { type: 'string' }, description: 'each one specific enough to act on; empty only when pass is true' },
    checks_run: {
      type: 'array',
      items: { type: 'object', properties: { check: { type: 'string' }, result: { type: 'string' } }, required: ['check', 'result'] },
    },
    sabotage: { type: 'string', description: 'the mutation made and whether a test failed, or "not applicable" for text-only work' },
  },
  required: ['pass', 'problems', 'checks_run', 'sabotage'],
}

// The first framing always runs; the second is added when independent sources are required.
const FRAMINGS = [
  {
    key: 'evidence',
    brief: 'Refute by evidence. Re-derive every claim yourself: open the cited code, rerun the cited commands, run the verify command. For a code change, do the sabotage check inside the worktree and revert it. A claim you cannot reproduce is a problem.',
  },
  {
    key: 'contract',
    brief: 'Refute by contract. Check the work against SPEC.md, DECISIONS.md, the house rules and the listed owner questions. Look for a rule change smuggled in, an owner decision pre-empted, scope beyond the segment goal, or a design that lets workers share state or hand off where sources must stay independent.',
  },
]

function planProblems(plan) {
  const problems = []
  const segs = plan.segments || []
  if (!segs.length) problems.push('The plan has no segments.')
  if (segs.length > MAX_SEGMENTS) problems.push(`The plan has ${segs.length} segments; the limit for this run is ${MAX_SEGMENTS}. Merge or drop segments.`)
  const ids = new Set()
  for (const s of segs) {
    if (ids.has(s.id)) problems.push(`Segment id "${s.id}" is used twice.`)
    ids.add(s.id)
  }
  for (const s of segs) {
    for (const d of s.depends_on) if (!ids.has(d)) problems.push(`Segment "${s.id}" depends on unknown segment "${d}".`)
    if (MODE === 'design' && (s.role === 'coder' || s.role === 'tester')) problems.push(`Segment "${s.id}" has role ${s.role}, but this is a design run; use researcher or designer.`)
    if (s.role === 'coder' && !s.verify_cmd) problems.push(`Coder segment "${s.id}" has no verify_cmd.`)
  }
  const mark = {}
  const cyclic = id => {
    if (mark[id] === 'done') return false
    if (mark[id] === 'open') return true
    mark[id] = 'open'
    const seg = segs.find(s => s.id === id)
    const hit = (seg ? seg.depends_on : []).some(cyclic)
    mark[id] = 'done'
    return hit
  }
  if (segs.some(s => cyclic(s.id))) problems.push('depends_on contains a cycle.')
  return problems
}

const planPrompt = problems => `${CONTEXT}
You are planning one enhancement. You do not carry it out.

Goal: ${GOAL}

1. Read ${STATE_FILE} and PROJECT_OVERVIEW.md. For each claim in the state file that the goal relies on, recheck it
   against the current code and record whether it still holds, with file:line evidence.
2. Run the test command once and record the counts as the baseline.
3. List the open owner decisions this work touches (PROJECT_OVERVIEW.md F1, DECISIONS.md, the ablation documents).
4. Split the goal into at most ${MAX_SEGMENTS} segments. For each segment decide separately, and explain in
   \`rationale\`:
   - structure: which segments need another segment's verified output (\`depends_on\`). Segments with no dependency
     between them run in parallel, so do not invent dependencies and do not let two segments change the same file.
   - feedback cycle: \`max_attempts\` is 1 unless a later attempt would really use verification feedback; then bound
     it (at most ${MAX_ATTEMPTS}) and state the stop condition in \`acceptance\`.
   - communication: a segment sees only the verified output of its \`depends_on\` segments. Say what it reads from
     them. Set \`independent_sources_required\` when the result will be relied on as corroborated.
   ${MODE === 'design'
    ? 'This is a design run: roles are researcher and designer only, and no segment changes a file.'
    : 'This is a prototype run: a coder segment works in its own worktree and needs a verify_cmd. A coder segment that depends on another coder segment merges that branch first.'}
${problems.length ? `\nYour previous plan was rejected. Fix these problems:\n- ${problems.join('\n- ')}` : ''}`

const criticPrompt = plan => `${CONTEXT}
Review this plan before any work starts. Try to reject it. Do not carry it out.

Goal: ${GOAL}

Plan:
${JSON.stringify(plan, null, 2)}

Reject if any of these holds, and name the segment: a rechecked state claim is marked true without evidence you can
find; a segment would change the contract, stakes, ownership or an approval; an open owner decision is pre-empted
or missing from owner_questions; two parallel segments touch the same file; a dependency is missing or invented;
\`acceptance\` is not observable; a loop has no stop condition; a result that will be relied on as corroborated is
not marked independent_sources_required; the segments together do not cover the goal, or go beyond it.`

const workPrompt = (seg, plan, deps, feedback, worktree) => `${CONTEXT}
You are the ${seg.role} for segment "${seg.id}".

Goal of this segment: ${seg.goal}
Acceptance: ${seg.acceptance}
${seg.verify_cmd ? `Verify command: ${seg.verify_cmd}` : ''}
Files in scope: ${(seg.files || []).join(', ') || 'decide from the goal'}
Test baseline before this run: ${plan.baseline}
Owner questions you must not pre-empt:
${plan.owner_questions.map(q => `- ${q}`).join('\n') || '- none listed'}

Verified output of the segments you depend on (${seg.inputs_from_deps}):
${deps.length ? JSON.stringify(deps.map(d => ({ id: d.id, findings: d.work.findings, claims: d.work.claims, branch: d.work.branch || '' })), null, 2) : 'none'}
${worktree
    ? `\nThis is a repair attempt. Work only inside the existing worktree ${worktree.path} (branch ${worktree.branch}); do not create another.`
    : seg.role === 'coder' ? '\nYou are in a fresh worktree. Merge the branches listed above first if there are any. Commit your change on this worktree\'s branch and report its path and branch.' : ''}
${feedback.length ? `\nThe verifiers rejected the previous attempt. Address each problem:\n- ${feedback.join('\n- ')}` : ''}

Return the deliverable in \`findings\`. Give every factual statement you rely on as a claim with evidence you
produced in this session. Put anything you could not establish in \`not_established\`.`

// Verifiers get the deliverable and the claims. They do not get the worker's method,
// the other verifier's verdict, or any sibling segment's output.
const verifyPrompt = (seg, plan, work, worktree, framing) => `${CONTEXT}
You are verifying segment "${seg.id}". Your job is to refute it. If you are unsure, it does not pass.
Change nothing outside a sabotage check, and revert that.

${framing.brief}

Goal of the segment: ${seg.goal}
Acceptance: ${seg.acceptance}
${seg.verify_cmd ? `Verify command: ${seg.verify_cmd}` : ''}
Test baseline before this run: ${plan.baseline}
Owner questions that must not be pre-empted:
${plan.owner_questions.map(q => `- ${q}`).join('\n') || '- none listed'}
${worktree ? `The change is in worktree ${worktree.path} on branch ${worktree.branch}. Inspect and run it there.` : 'No files were changed; the deliverable is the text below.'}

Deliverable:
${work.findings}

Claims:
${JSON.stringify(work.claims, null, 2)}

Reported test result: ${work.test_result}`

async function runOne(seg, plan, deps) {
  const bound = Math.max(1, Math.min(seg.max_attempts || 1, MAX_ATTEMPTS))
  const framings = seg.independent_sources_required ? FRAMINGS : FRAMINGS.slice(0, 1)
  let feedback = [], work = null, verdicts = [], worktree = null
  for (let attempt = 1; attempt <= bound; attempt++) {
    const isolate = MODE === 'prototype' && seg.role === 'coder' && !worktree
    work = await agent(workPrompt(seg, plan, deps, feedback, worktree), {
      label: `${seg.role}:${seg.id}#${attempt}`, phase: 'Execute', schema: WORK_SCHEMA,
      ...(isolate ? { isolation: 'worktree' } : {}),
    })
    if (!work) return { id: seg.id, status: 'error', attempts: attempt, work: null, verdicts: [], reason: 'The worker returned nothing.' }
    if (work.worktree_path) worktree = { path: work.worktree_path, branch: work.branch || '' }
    verdicts = await parallel(framings.map(f => () =>
      agent(verifyPrompt(seg, plan, work, worktree, f), { label: `verify-${f.key}:${seg.id}#${attempt}`, phase: 'Verify', schema: VERDICT_SCHEMA })))
    const missing = verdicts.filter(v => !v).length
    if (!missing && verdicts.every(v => v.pass)) return { id: seg.id, status: 'verified', attempts: attempt, work, verdicts }
    feedback = verdicts.filter(Boolean).flatMap(v => v.problems)
    if (missing) feedback.push(`${missing} verifier(s) returned nothing, so the attempt counts as unverified.`)
    log(`${seg.id}: attempt ${attempt}/${bound} not verified (${feedback.length} problem(s))`)
  }
  return { id: seg.id, status: 'unverified', attempts: bound, work, verdicts: verdicts.filter(Boolean), reason: feedback.join(' | ') }
}

phase('Plan')
let plan = null, problems = []
for (let round = 1; round <= MAX_PLAN_ROUNDS; round++) {
  plan = await agent(planPrompt(problems), { label: `plan#${round}`, phase: 'Plan', schema: PLAN_SCHEMA })
  if (!plan) return { status: 'plan_failed', mode: MODE, goal: GOAL, reason: 'The planner returned nothing.' }
  problems = planProblems(plan)
  if (!problems.length) {
    const review = await agent(criticPrompt(plan), { label: `plan-critic#${round}`, phase: 'Plan', schema: CRITIC_SCHEMA })
    if (!review) problems = ['The plan critic returned nothing, so the plan is unreviewed.']
    else if (!review.approved) problems = review.problems.length ? review.problems : ['The critic rejected the plan without naming a problem.']
  }
  if (!problems.length) break
  log(`Plan round ${round}/${MAX_PLAN_ROUNDS} rejected: ${problems.length} problem(s)`)
}
if (problems.length) return { status: 'plan_rejected', mode: MODE, goal: GOAL, plan, problems }

const stale = plan.state_claims.filter(c => !c.still_true)
if (stale.length) log(`${stale.length} state-file claim(s) no longer hold: ${stale.map(c => c.claim).join('; ')}`)
log(`Plan accepted: ${plan.segments.map(s => `${s.id}${s.depends_on.length ? `<-${s.depends_on.join('+')}` : ''}`).join(', ')}`)

// No barrier between waves: each segment waits only on its own dependencies.
const byId = Object.fromEntries(plan.segments.map(s => [s.id, s]))
const started = {}
const runSegment = seg => {
  if (!started[seg.id]) started[seg.id] = (async () => {
    const deps = await Promise.all(seg.depends_on.map(d => runSegment(byId[d])))
    const open = deps.filter(d => d.status !== 'verified').map(d => d.id)
    if (open.length) return { id: seg.id, status: 'blocked', attempts: 0, work: null, verdicts: [], reason: `Not started: ${open.join(', ')} not verified.` }
    try {
      return await runOne(seg, plan, deps)
    } catch (e) {
      return { id: seg.id, status: 'error', attempts: 0, work: null, verdicts: [], reason: String(e && e.message || e) }
    }
  })()
  return started[seg.id]
}
const results = await Promise.all(plan.segments.map(runSegment))
log(results.map(r => `${r.id}: ${r.status}`).join(', '))

phase('Report')
const report = await agent(`${CONTEXT}
Write the report for the owner (EJ) in Markdown. Change no files. Use only what is below; do not add findings of
your own, and do not describe an unverified or blocked segment as done.

Sections, in this order:
1. Outcome: one paragraph, leading with how many segments were verified out of how many.
2. Planning decision record: a table of the segments with dependencies, loop bound, shared inputs, number of
   verifiers and the rationale. State that it is a single run and not to be built on as a rule.
3. Results per segment: the deliverable, the claims with evidence, and what each verifier checked.
4. Not established, and state-file claims that no longer hold.
5. Questions for the owner.
6. What is missing: acceptance conditions nobody checked, claims without evidence, checks reported as not run.
7. ${MODE === 'prototype' ? 'Worktrees and branches to review. Nothing has been merged.' : 'Proposed next step. No files were changed.'}

Goal: ${GOAL}
Mode: ${MODE}
Plan: ${JSON.stringify(plan, null, 2)}
Results: ${JSON.stringify(results, null, 2)}`, { label: 'report', phase: 'Report' })

const verified = results.filter(r => r.status === 'verified').length
return {
  status: verified === results.length ? 'all_verified' : 'partly_verified',
  mode: MODE,
  goal: GOAL,
  verified: `${verified}/${results.length}`,
  plan,
  results,
  report,
}
