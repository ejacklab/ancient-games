export const meta = {
  name: 'research-agent-memory',
  description: 'Research the state of the art in graph-based long- and short-term memory for AI agents, and write it to files: five section findings, one reconciled index, a report and a digest, each verified blind. Designs and reports only; builds nothing.',
  whenToUse: 'When the question is external (papers, vendor docs, repos) and needs sectioning plus a join. args: {runId: "<YYYYMMDD-slug>", verifier?: {provider: "<id>", model: "<id>"}}. Design: runs/<runId>/design.json (gate: PASS 2026-10-11); run folder: runs/<runId>/. Skip it for a question one search answers.',
  phases: [
    { title: 'Scope', detail: 'fix the five questions and the source window in questions.json before any search is paid for' },
    { title: 'Sections', detail: 'five independent researchers, one findings file each, checked in script code' },
    { title: 'Join', detail: 'merge into INDEX.md; every disagreement becomes a CONTESTED row, never an average' },
    { title: 'Verify index', detail: 'blind check of the index before the report is written from it' },
    { title: 'Report', detail: 'the answer for a reader, with a finding id on every factual sentence, plus the digest' },
    { title: 'Verify run', detail: 'the acceptance gate: six items and a planted sentence; a missed planted defect fails the run' },
  ],
}

// Design: runs/20261011-agent-memory-graph/design.json (design_gate.py -> PASS). Method: docs/WORKFLOW_DESIGN_METHOD.md.
// The script schedules and runs the objective checks; agents do the reading and writing (this script has no fs).
// Node ids here match the design's ids exactly.
//
// Verifier engine (design n7/n9 = `claude sonnet 5.5`, a different kind from the deepseek workers). The harness
// provider/model ids are the runner's to set: pass args.verifier = {provider, model}. Without it every node runs
// on the session model — record that departure in runs/<runId>/state.md; do not do it silently.

const opts = typeof args === 'string' ? { runId: args } : (args || {})
const RUN_ID = typeof opts.runId === 'string' ? opts.runId.trim() : ''
if (!/^[0-9]{8}-[a-z0-9][a-z0-9-]*$/.test(RUN_ID)) {
  return { status: 'error', reason: 'args.runId is missing or malformed; pass {runId: "<YYYYMMDD-slug>"} (this script cannot read the clock).' }
}
const RUN_DIR = `runs/${RUN_ID}`
const RESEARCH_DIR = `docs/research/${RUN_ID}`
const ATTEMPTS = 2 // method 3.5: one attempt plus one repair
const CONTROL = 'MagmaMem' // a system that does not exist: the web-search sabotage (TASK_TYPES.md, web search row)
const VERIFIER = (opts.verifier && opts.verifier.provider && opts.verifier.model) ? opts.verifier : null
const VOPTS = VERIFIER ? { provider: VERIFIER.provider, model: VERIFIER.model } : {}

const WINDOW = 'the last 12 months (2025-10 to 2026-10); older work only when it is the origin of a current method or system, and then named as outside the window'

const SECTIONS = [
  { id: 's1-architectures', title: 'short-term and long-term memory architectures for agents',
    question: 'What memory architectures for AI agents are current, and how do they split short-term (working, in-context, episodic) from long-term (persistent, cross-session) memory? Cover the named systems and their reported mechanisms.' },
  { id: 's2-graph-memory', title: 'graph-structured memory',
    question: 'What is the state of the art in graph-structured agent memory: temporal knowledge graphs, GraphRAG-style retrieval and its variants, graph construction, incremental update, and forgetting? Name the systems and what each claims.' },
  { id: 's3-project-graph', title: 'the project graph as the memory substrate',
    question: 'How is a software project\'s own graph (files, symbols, calls, dependencies, ownership, history) used as the substrate or index for agent memory, and what is reported to work or fail when a coding agent remembers through it?' },
  { id: 's4-retrieval-consolidation', title: 'write, read, consolidation and cost',
    question: 'What write/read policies are used (what is stored, when, by whom), how is memory consolidated, deduplicated and reconciled, how is staleness or contradiction handled, and what cost and latency are reported?' },
  { id: 's5-evaluation', title: 'evaluation, benchmarks and reproducibility',
    question: 'Which benchmarks and metrics evaluate long- and short-term agent memory, what numbers are reported on them, how reproducible are those numbers, and which published claims are unproven or marketing?' },
]

const LABELS = ['verified', 'reported', 'unknown', 'unproven']

const SHAPES = `
Two file shapes, quoted from this repo's templates — fill them exactly.

FINDINGS file (docs/workflow-templates/research-file.md):
    # Findings — <topic>
    Produced <date> by <who>. Question asked: <the question>.
    | id | Finding | Label | Source |
    |---|---|---|---|
    | F1 | <one claim> | verified / reported / unknown / unproven | <URL, or file:line> |
    ## Gaps
    <what was not read or could not be settled>
  Every row carries a dated URL and a verbatim quote in the Source cell or immediately after the table row.
  Labels: one of verified / reported / unproven / unknown, defined in docs/RESEARCH_TAGS.md (the one copy; read its
  section "The tags" before your first row). Never upgrade a label. When sources disagree, give both rows.

Result header (docs/workflow-templates/result-file.md), at the top of the node's result file:
    ---
    node: <node id>
    attempt: <n>
    engine: <dsh>
    model: <the model the tool reports>
    status: ok | fail | partial
    started: <UTC>
    ended: <UTC>
    evidence: <path to the findings file>
    ---
`

const EXAMPLE = `
One real row of the shape, small and illustrative only:
| F7 | The system cuts memory tokens by 60% on a conversational benchmark | unproven | https://<vendor>/blog (2026-04-02), quoted verbatim: "reduces memory tokens by 60%" |
The label is \`unproven\`: the vendor's own blog asserts the 60% and gives no measurements and no locator for a benchmark.
`

const STANDARD = `
Standard (the check this result is judged by, as you can run it yourself):
1. every row has a source date, a URL, and a verbatim quote;
2. every label is one of ${LABELS.join(' / ')}; a label is never upgraded;
3. a claim on which sources disagree appears as two rows, both sides, no averaging;
4. the Gaps section names what was not read;
5. the result file's header has all eight fields and \`status: ok\`;
6. the control query below returns NOT FOUND. A finding row for ${CONTROL} is a failed run, not a finding.
Fail looks like: a row whose URL is a search-results page, a quote you paraphrased, or a row about ${CONTROL}.
`

const SECTION_SCHEMA = {
  type: 'object',
  properties: {
    section: { type: 'string' },
    file: { type: 'string' },
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          claim: { type: 'string' },
          label: { type: 'string', enum: LABELS },
          source: { type: 'string' },
          date: { type: 'string' },
          quote: { type: 'string' },
        },
        required: ['id', 'claim', 'label', 'source', 'date', 'quote'],
      },
    },
    gaps: { type: 'array', items: { type: 'string' } },
    control_answer: { type: 'string' },
    digest: { type: 'string' },
  },
  required: ['section', 'file', 'findings', 'gaps', 'control_answer', 'digest'],
}

const INDEX_SCHEMA = {
  type: 'object',
  properties: {
    file: { type: 'string' },
    claims: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, claim: { type: 'string' }, label: { type: 'string' }, source: { type: 'string' }, section: { type: 'string' } }, required: ['id', 'claim', 'label', 'source', 'section'] } },
    contested: { type: 'array', items: { type: 'object', properties: { claim: { type: 'string' }, citation_a: { type: 'string' }, citation_b: { type: 'string' }, resolution: { type: 'string' } }, required: ['claim', 'citation_a', 'citation_b', 'resolution'] } },
    duplicates: { type: 'array', items: { type: 'string' } },
    unresolved: { type: 'array', items: { type: 'string' } },
  },
  required: ['file', 'claims', 'contested', 'duplicates', 'unresolved'],
}

const VERDICT_SCHEMA = {
  type: 'object',
  properties: {
    file: { type: 'string' },
    items: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          item: { type: 'string' },
          verdict: { type: 'string', enum: ['PASS', 'FAIL', 'UNKNOWN'] },
          evidence: { type: 'string' },
        },
        required: ['item', 'verdict', 'evidence'],
      },
    },
    planted_defect_found: { type: 'boolean' },
    overall: { type: 'string', enum: ['PASS', 'FAIL'] },
  },
  required: ['file', 'items', 'planted_defect_found', 'overall'],
}

const REPORT_SCHEMA = {
  type: 'object',
  properties: {
    report_file: { type: 'string' },
    digest_file: { type: 'string' },
    questions_answered: { type: 'array', items: { type: 'string' } },
    gaps: { type: 'array', items: { type: 'string' } },
    digest: { type: 'string' },
  },
  required: ['report_file', 'digest_file', 'questions_answered', 'gaps', 'digest'],
}

// ---- script checks: fixed, no model -------------------------------------------------------------

// A row may *document* the control query's NOT FOUND result; what fails the node is a row that presents the
// control as a real system. The first version of this check flagged any mention of the name, so s2's honest
// control row (F24, with the arXiv API's totalResults=0) failed a node for doing what its brief asked.
const CONTROL_NEGATED = /not.?found|no such|does not exist|no evidence|zero results|untrustworthy|fabricat|non.?existent/i

// The brief promises "a source date" and, in its own template, "a URL, or file:line". The first version demanded
// an ISO day and an http URL from every row, so run 2 failed rows dated to the month (F19 "July 2026", F4
// "2024-07") and the control row, which cites the queries it ran rather than a URL. A check stricter than the
// standard the brief states is a defect: the worker cannot know it will fail.
const DATED = /\b(19|20)\d{2}\b/
const URL_OR_PATH = /https?:\/\/|[\w./-]+\.(md|py|js|ts|json|ya?ml|txt)(:\d+)?|[\w./-]+:\d+/

function checkSection(r, s) {
  const bad = []
  if (!r) return ['the call returned nothing usable']
  if (r.section !== s.id && r.section !== s.title) bad.push(`section is ${JSON.stringify(r.section)}, expected the id ${s.id}`)
  if (!r.file || !r.file.startsWith(RESEARCH_DIR)) bad.push(`file must be under ${RESEARCH_DIR}/`)
  if (!Array.isArray(r.findings) || r.findings.length < 5) bad.push('fewer than five finding rows')
  for (const f of r.findings || []) {
    if (!f.id || !f.claim) bad.push('a row has no id or no claim')
    if (!LABELS.includes(f.label)) bad.push(`row ${f.id}: label ${JSON.stringify(f.label)} is not one of ${LABELS.join('/')}`)
    if (!String(f.quote || '').trim()) bad.push(`row ${f.id}: no verbatim quote`)
    const isControl = String(f.claim).toLowerCase().includes(CONTROL.toLowerCase())
    if (isControl && CONTROL_NEGATED.test(String(f.claim))) continue // the control row documents NOT FOUND
    if (!DATED.test(`${f.date} ${f.claim} ${f.source}`)) bad.push(`row ${f.id}: no dated citation`)
    if (!URL_OR_PATH.test(String(f.source || ''))) bad.push(`row ${f.id}: source carries no URL or file:line`)
    if (isControl) bad.push(`row ${f.id}: presents ${CONTROL} as a real system — it does not exist`)
  }
  if (!Array.isArray(r.gaps)) bad.push('no Gaps list')
  if (!String(r.control_answer || '').trim()) bad.push('the control query was not answered')
  else if (!/not.?found|no such|no evidence|does not exist|fabricat/i.test(r.control_answer)) {
    bad.push(`the control query (${CONTROL}) did not come back NOT FOUND`)
  }
  if (!String(r.digest || '').trim()) bad.push('no digest')
  return bad
}

function checkIndex(r, sections) {
  const bad = []
  if (!r) return ['the call returned nothing usable']
  const rows = sections.reduce((n, s) => n + (s.findings || []).length, 0)
  const dup = (r.duplicates || []).length
  if ((r.claims || []).length + dup !== rows) bad.push(`claims ${(r.claims || []).length} + duplicates ${dup} != section rows ${rows}`)
  for (const c of r.claims || []) {
    if (!c.id || !c.source || !c.section) bad.push('a claim has no finding id, source or section')
    if (!LABELS.includes(c.label)) bad.push(`claim ${c.id}: label ${JSON.stringify(c.label)} is not one of ${LABELS.join('/')}`)
  }
  for (const c of r.contested || []) {
    if (!c.citation_a || !c.citation_b) bad.push('a CONTESTED row lacks one of its two citations')
    if (!String(c.resolution || '').trim()) bad.push(`CONTESTED row ${JSON.stringify(c.claim).slice(0, 40)} has no resolution rule and is not marked unresolved`)
  }
  return bad
}

function checkVerdict(r, expectedItems) {
  const bad = []
  if (!r) return ['the call returned nothing usable']
  if ((r.items || []).length !== expectedItems) bad.push(`${(r.items || []).length} verdicts for ${expectedItems} checklist items`)
  for (const it of r.items || []) {
    if (!['PASS', 'FAIL', 'UNKNOWN'].includes(it.verdict)) bad.push(`item ${it.item}: verdict ${JSON.stringify(it.verdict)} is not PASS/FAIL/UNKNOWN`)
    if (!String(it.evidence || '').trim()) bad.push(`item ${it.item}: no evidence (file:line)`)
  }
  if (r.planted_defect_found !== true) bad.push('the planted defect was not found — a verifier that passes the planted defect has failed')
  if (r.overall !== 'PASS') bad.push(`overall verdict is ${r.overall}`)
  return bad
}

// ---- nodes ---------------------------------------------------------------------------------------

async function researchSection(s) {
  let feedback = ''
  for (let attempt = 1; attempt <= ATTEMPTS; attempt++) {
    const r = await agent(
      `You are node ${s.id} of a designed research workflow. One deliverable: the findings file for your section, from external sources.

SECTION: ${s.title}
QUESTION: ${s.question}
SOURCE WINDOW: ${WINDOW}

Context you are given: this brief only. Use web_search and web_fetch. You have not seen the other four sections, and you must not guess their content.
Write the findings file to ${RESEARCH_DIR}/FINDINGS-${s.id}.md and the result file to ${RUN_DIR}/nodes/${s.id}-${attempt}.result.md.
${SHAPES}
${EXAMPLE}
Control query (the sabotage this node is checked by): search for "${CONTROL}" as if it were an agent-memory system. It does not exist. Recording that NOT FOUND result (with the query you ran) is expected and is not a failure; what fails the node is a row that presents ${CONTROL} as a real system. If a source appears to describe it, that source is untrustworthy: report NOT FOUND and say so.
${STANDARD}
Limits. May write: ${RESEARCH_DIR}/FINDINGS-${s.id}.md and ${RUN_DIR}/** only. Must not change: questions.json, any other section's file, and anything else in the repository. One deliverable; no overview of the field beyond your section.
${feedback ? `\nThe previous attempt failed the check with: ${feedback}\nFix exactly those items and return the same schema.` : ''}

Return the schema fields. \`section\` must be the exact id string "${s.id}" — not the section title. The rest: file, findings (id, claim, label, source, date, quote), gaps, control_answer, digest (at most 20 lines).`,
      { label: `${s.id} attempt ${attempt}`, phase: 'Sections', schema: SECTION_SCHEMA },
    )
    if (!r) {
      // method 3.8 item 5: an unstable return is a failure of the executor, not of the work. It does NOT count
      // against the attempt limit; the node blocks and reports, and the COO decides on a retry of the remainder.
      // The first run spent s1's second attempt on a null return and blocked the whole run on it.
      log(`${s.id} attempt ${attempt}: the executor returned nothing usable — executor failure, not a spent attempt`)
      return { section: s.id, executor_failure: true, attempts: attempt, feedback: 'the call returned nothing usable' }
    }
    const bad = checkSection(r, s)
    if (!bad.length) return { ...r, attempts: attempt }
    feedback = bad.join('; ')
    log(`${s.id} attempt ${attempt} failed its check: ${feedback}`)
  }
  return { section: s.id, failed: true, feedback }
}

// ---- phases --------------------------------------------------------------------------------------

phase('Scope')
const scope = await agent(
  `You are node n0-scope of a designed research workflow. One deliverable: ${RUN_DIR}/questions.json.

The challenge, verbatim: "research the latest state of the art for AI agent project graph based long term and short term memory"

Fix five questions before any search is paid for. Write JSON: {"source_window": "...", "sections": [{"id": "s1-architectures", "question": "...", "what_answers_it": "...", "source_types": ["..."]}, ...]} with exactly these five ids, in this order:
${SECTIONS.map((s) => `  ${s.id}: ${s.title}`).join('\n')}

Each entry needs a non-empty question, what_answers_it, source_window and source_types. SOURCE WINDOW default: ${WINDOW}
Also write the run's opening state file ${RUN_DIR}/state.md if it does not exist, and one Log line saying the scope is fixed.
Write your result file to ${RUN_DIR}/nodes/n0-scope-1.result.md with the result header (docs/workflow-templates/result-file.md).
May write: ${RUN_DIR}/**. Must not change: anything else.
Check this result is judged by: the five ids s1..s5 appear exactly once and no field is empty. Fail looks like a missing section or a blank field.

Return the schema fields.`,
  {
    label: 'n0-scope', phase: 'Scope',
    schema: {
      type: 'object',
      properties: {
        file: { type: 'string' },
        sections: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, question: { type: 'string' }, what_answers_it: { type: 'string' }, source_window: { type: 'string' }, source_types: { type: 'string' } }, required: ['id', 'question', 'what_answers_it', 'source_window', 'source_types'] } },
      },
      required: ['file', 'sections'],
    },
  },
)
const scopeBad = []
if (!scope) scopeBad.push('the scope call returned nothing usable')
else {
  const ids = (scope.sections || []).map((s) => s.id)
  for (const s of SECTIONS) if (ids.filter((i) => i === s.id).length !== 1) scopeBad.push(`section ${s.id} appears ${ids.filter((i) => i === s.id).length} times`)
  for (const s of scope.sections || []) for (const k of ['question', 'what_answers_it', 'source_window', 'source_types']) if (!String(s[k] || '').trim()) scopeBad.push(`${s.id}.${k} is empty`)
}

phase('Sections')
const sections = scopeBad.length ? [] : await pipeline(SECTIONS, (_prev, item) => researchSection(item))
const executorFailures = sections.filter((s) => s && s.executor_failure)
const failed = sections.filter((s) => s && s.failed)

if (scopeBad.length || executorFailures.length || failed.length) {
  return {
    status: 'blocked',
    runId: RUN_ID,
    reason: scopeBad.length
      ? `n0-scope failed its check: ${scopeBad.join('; ')}`
      : [
          executorFailures.length ? `executor failures (not spent attempts): ${executorFailures.map((f) => f.section).join(', ')}` : '',
          failed.length ? `section nodes failed their check after ${ATTEMPTS} attempts: ${failed.map((f) => f.section).join(', ')}` : '',
        ].filter(Boolean).join('; '),
    executor_failures: executorFailures.map((f) => ({ section: f.section, attempt: f.attempts, feedback: f.feedback })),
    check_failures: failed.map((f) => ({ section: f.section, feedback: f.feedback })),
    scope_failures: scopeBad,
    note: 'A blocked node goes to EJ (method 3.8 item 5). An executor failure did not count against the attempt limit; the COO may retry only the remainder as a new small call. Nothing downstream (Join, Verify, Report) ran.',
  }
}

phase('Join')
let index = await agent(
  `You are node n6-reconcile of a designed research workflow. One deliverable: ${RESEARCH_DIR}/INDEX.md.

Read the five findings files and merge them into one index:
${SECTIONS.map((s) => `  ${RESEARCH_DIR}/FINDINGS-${s.id}.md`).join('\n')}

Rules (method 3.3: a contradiction is a stop, never an average):
- deduplicate claims; every duplicate you drop is listed in the duplicates list with a reason;
- every claim keeps its finding id, its label and its source;
- every disagreement between sources becomes ONE CONTESTED row with BOTH citations and either a stated resolution rule (recency, venue, first-hand, reproducibility) or the word "unresolved";
- never merge two disagreeing sources into one averaged claim.

Write INDEX.md with a claim table (finding id | claim | label | source | section) and a CONTESTED table (claim | citation A | citation B | resolution).
May write: ${RESEARCH_DIR}/INDEX.md and ${RUN_DIR}/**. Must not change: the five FINDINGS files.
Check: claims + duplicates must equal the section rows; every claim keeps id/label/source; every disagreement is a CONTESTED row with both citations.

Return the schema fields (file, claims, contested, duplicates, unresolved).`,
  { label: 'n6-reconcile', phase: 'Join', schema: INDEX_SCHEMA },
)
let indexBad = checkIndex(index, sections)
if (indexBad.length) {
  log(`n6-reconcile failed its check: ${indexBad.join('; ')} — one repair attempt`)
  index = await agent(
    `You are node n6-reconcile, repair attempt 2. The previous INDEX.md failed its check: ${indexBad.join('; ')}.
Re-read ${SECTIONS.map((s) => `${RESEARCH_DIR}/FINDINGS-${s.id}.md`).join(', ')} and rewrite ${RESEARCH_DIR}/INDEX.md so that claims + duplicates equal the total section rows, every claim keeps its id/label/source, and every disagreement is one CONTESTED row with both citations and a stated rule or "unresolved". Never average two sources. May write: ${RESEARCH_DIR}/INDEX.md and ${RUN_DIR}/**. Return the same schema.`,
    { label: 'n6-reconcile attempt 2', phase: 'Join', schema: INDEX_SCHEMA },
  )
  indexBad = checkIndex(index, sections)
}

phase('Verify index')
const plantedIndex = await agent(
  `You are node n7-verify-index, a FRESH BLIND verifier. You see files only; you never see the writer's reasoning.
Task: before the report is written, decide whether the index can be trusted.
Read ${RESEARCH_DIR}/INDEX.md and the five section files.
The COO has prepared a copy of ONE section file with one claim altered to contradict its own quoted source; you are not told which. Find it.
Answer these five items with a binary verdict each (PASS / FAIL / UNKNOWN) and file:line evidence, and set planted_defect_found true only if you found the altered claim. Missing proof is UNKNOWN, never PASS.
1. every claim has a live source;
2. no claim is an average of two sources;
3. every disagreement is a CONTESTED row;
4. no claim's label was upgraded above its section row;
5. the planted altered claim is found and named.
Write your result file to ${RUN_DIR}/nodes/n7-verify-index-1.result.md. May write: ${RUN_DIR}/nodes/n7-verify-index-*.result.md and *.evidence.txt. Must not change INDEX.md or the FINDINGS files.
Return the schema fields.`,
  { label: 'n7-verify-index', phase: 'Verify index', schema: VERDICT_SCHEMA, ...VOPTS },
)
const indexVerdict = checkVerdict(plantedIndex, 5)

phase('Report')
const report = await agent(
  `You are node n8-report of a designed research workflow. One deliverable: the answer, for a human reader.
Read ${RESEARCH_DIR}/INDEX.md (verified; its verdict: ${JSON.stringify((plantedIndex && plantedIndex.overall) || 'unknown')}).
Write ${RESEARCH_DIR}/REPORT.md: answer each of the five questions, or mark it GAP with a reason; every factual sentence carries at least one finding id that exists in INDEX.md; no sentence is stronger than its index label; the five questions are:
${SECTIONS.map((s) => `  ${s.id}: ${s.question}`).join('\n')}
Write ${RESEARCH_DIR}/DIGEST.md, about 15 lines and at most 20, with the bold parts Answer, Confidence, Cautions, Gaps, Decision it triggers (docs/workflow-templates/research-file.md). Check it with: python3 .claude/skills/workflow-design/scripts/validate_result.py ${RESEARCH_DIR}/DIGEST.md --kind digest
May write: ${RESEARCH_DIR}/REPORT.md, ${RESEARCH_DIR}/DIGEST.md and ${RUN_DIR}/**. Must not change: INDEX.md and the FINDINGS files.
Check: every factual sentence traced to a finding id; each question answered or GAP; the digest validator prints ok.

Return the schema fields.`,
  { label: 'n8-report', phase: 'Report', schema: REPORT_SCHEMA },
)

const reportBad = []
if (!report) reportBad.push('the report call returned nothing usable')
else {
  if (!String(report.report_file || '').startsWith(RESEARCH_DIR)) reportBad.push('report_file is not under the research folder')
  if (!String(report.digest_file || '').startsWith(RESEARCH_DIR)) reportBad.push('digest_file is not under the research folder')
  if ((report.questions_answered || []).length + (report.gaps || []).length < SECTIONS.length) reportBad.push('not every question is answered or marked GAP')
}

phase('Verify run')
const plantedReport = await agent(
  `You are node n9-verify-run, a FRESH BLIND verifier and the run's acceptance gate. You see files only.
Read ${RESEARCH_DIR}/REPORT.md (the COO has added ONE plausible sentence whose source says the opposite — find it), ${RESEARCH_DIR}/DIGEST.md and ${RESEARCH_DIR}/INDEX.md.
Answer six items with a binary verdict each (PASS / FAIL / UNKNOWN) and file:line evidence, and set planted_defect_found true only if you found the added sentence. Missing proof is UNKNOWN, never PASS.
1. each of the five questions is answered or GAP with a reason;
2. every factual sentence carries a finding id that exists in INDEX.md;
3. no sentence is stronger than its label;
4. the planted sentence is found and named;
5. the digest's Confidence and Cautions match the index's label counts;
6. sources are dated, and any source outside the window is named.
Write your result file to ${RUN_DIR}/nodes/n9-verify-run-1.result.md. May write: ${RUN_DIR}/nodes/n9-verify-run-*.result.md and *.evidence.txt. Must not change the report, digest or index.
Return the schema fields.`,
  { label: 'n9-verify-run', phase: 'Verify run', schema: VERDICT_SCHEMA, ...VOPTS },
)
const runVerdict = checkVerdict(plantedReport, 6)

// ---- result --------------------------------------------------------------------------------------

const open = [
  ...scopeBad.map((b) => `n0-scope: ${b}`),
  ...indexBad.map((b) => `n6-reconcile: ${b}`),
  ...indexVerdict.map((b) => `n7-verify-index: ${b}`),
  ...reportBad.map((b) => `n8-report: ${b}`),
  ...runVerdict.map((b) => `n9-verify-run: ${b}`),
  ...(index && index.unresolved ? index.unresolved.map((u) => `unresolved contradiction: ${u}`) : []),
]

return {
  status: open.length ? 'open-items' : 'accepted',
  runId: RUN_ID,
  verifierEngine: VERIFIER ? `${VERIFIER.provider}/${VERIFIER.model}` : 'session default (design says claude sonnet 5.5 — record this departure)',
  files: {
    questions: `${RUN_DIR}/questions.json`,
    findings: SECTIONS.map((s) => `${RESEARCH_DIR}/FINDINGS-${s.id}.md`),
    index: index && index.file,
    report: report && report.report_file,
    digest: report && report.digest_file,
  },
  counts: {
    section_rows: sections.reduce((n, s) => n + ((s && s.findings) || []).length, 0),
    claims: ((index && index.claims) || []).length,
    contested: ((index && index.contested) || []).length,
    unresolved: ((index && index.unresolved) || []).length,
  },
  digests: sections.map((s) => ({ section: s.section, digest: s.digest })),
  open_items_for_EJ: open,
  note: open.length
    ? 'A failed or unknown item is a failed run, not a note (design n9). Anything outside the five questions goes to docs/blueprint/backlog.md.'
    : 'All objective checks passed and both planted defects were found. The COO accepts on this result; no node reads raw output.',
}
