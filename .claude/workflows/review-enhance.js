export const meta = {
  name: 'review-enhance',
  description: 'Review a tool with two read-only engines, judge findings against its vision, use cases and requirements, reproduce the accepted ones as failing tests, fix them on the code engine, loop until a review finds nothing new or the limit; then the six experts propose improvements, the top picks are built the same way. Reports; the owner may overrule every pick.',
  whenToUse: 'To review and enhance a built tool against its own VISION.md, USE_CASES.md and REQUIREMENTS.md (design: runs/20261017-memory-check-review/design.md). args: {run: "runs/<id>", rounds: N, tool: "<folder>", extra_paths: ["<file>", ...], test_cmd: "<command>", review_brief: "<file>", fix_template: "<file>", enhance_question: "<file>"}. Briefs and the question are files inside the repo, written before the run. Time box: deadline start before the run.',
  phases: [
    { title: 'Readiness', detail: 'baseline tests and the type check' },
    { title: 'Review', detail: 'Codex and agy read-only, in parallel; a reviewer with no Findings is redone by the step itself' },
    { title: 'Judge', detail: 'accept a finding only with the use case or requirement it breaks and an input' },
    { title: 'Reproduce', detail: 'one test per accepted finding, each failing on HEAD; a finding that does not reproduce is dropped' },
    { title: 'Fix', detail: 'opencode, from the round brief; relative paths only' },
    { title: 'Verify', detail: 'every test, the type check, the read-only check' },
    { title: 'Enhance', detail: 'experts-decide, then the main pick built as reproduce, fix, verify' },
    { title: 'Report' },
  ],
}

// Design: runs/20261017-memory-check-review/design.md. Every step is an agent (no shell step in the script API). The
// script cannot read the clock: each step runs `deadline status` first and returns time_up; after that no step starts.
// The script decides only the loop: it stops on a round with no accepted finding, on the round limit, or on time up.

const a = args && typeof args === 'object' && !Array.isArray(args) ? args : {}
const errors = []
const str = v => typeof v === 'string' && v.trim() !== ''
const REPO_PATH = /^[A-Za-z0-9_][A-Za-z0-9._/-]*$/
const repoPath = v => str(v) && REPO_PATH.test(v) && !v.split('/').includes('..')
if (!str(a.run) || !/^runs\/[0-9]{8}-[a-z0-9][a-z0-9-]*$/.test(a.run)) errors.push('args.run must look like runs/20261017-short-name')
if (!Number.isInteger(a.rounds) || a.rounds < 1) errors.push('args.rounds must be a whole number of at least 1')
if (!repoPath(a.tool)) errors.push('args.tool must be a folder inside the repo')
for (const k of ['review_brief', 'fix_template', 'enhance_question']) if (!repoPath(a[k])) errors.push(`args.${k} must be a file path inside the repo`)
if (!str(a.test_cmd)) errors.push('args.test_cmd is missing')
const extra = Array.isArray(a.extra_paths) ? a.extra_paths : []
if (!extra.every(repoPath)) errors.push('args.extra_paths must be paths inside the repo')
if (errors.length) return { status: 'refused', errors }

const RUN = a.run
const NODES = `${RUN}/nodes`
const PROGRESS = `${NODES}/review-enhance.progress.md`
const CHEAP = { model: 'claude-haiku-5-5', effort: 'low' }

const COMMON = label => `
You are one step (${label}) of the review-enhance workflow in this repository; its root is your working folder.
Run folder: ${RUN}/. Another session also commits in this working tree: never \`git add\`, never commit, never
\`git stash\`, and change no file except the ones this step names. Use relative paths.

1. First run \`bun .claude/skills/workflow-design/guard/src/cli.ts deadline status\`. If it prints "time is up" (exit 1),
   return at once with time_up true and every other field empty ("", 0, false or []), and do nothing else. Otherwise
   go on with time_up false.
2. Append one line to ${PROGRESS} with a shell \`echo ... >>\`: \`- <date -Iseconds> · ${label} · start · <note>\`, and one
   more when you finish, with \`done\` or \`fail\` in place of \`start\` (the label is one word).
3. Run each long command with the Bash tool's timeout set to 600000 ms, and an engine call in the background with a
   timeout of its own if it may take longer. Report what commands printed and returned, not what you expect.
`

const s = type => ({ type })
const strings = { type: 'array', items: { type: 'string' } }
const object = properties => ({ type: 'object', properties, required: Object.keys(properties) })
const FINDING = object({ id: s('string'), requirement: s('string'), summary: s('string'), input: s('string') })
const READY_SCHEMA = object({ time_up: s('boolean'), pass: s('boolean'), summary: s('string') })
const REVIEW_SCHEMA = object({ time_up: s('boolean'), engine: s('string'), file: s('string'), usable: s('boolean'), redone_by_step: s('boolean'), problem: s('string') })
const JUDGE_SCHEMA = object({ time_up: s('boolean'), file: s('string'), accepted: { type: 'array', items: FINDING }, dropped: s('integer') })
const REPRO_SCHEMA = object({ time_up: s('boolean'), test_file: s('string'), reproduced: strings, not_reproduced: strings, red_file: s('string') })
const FIX_SCHEMA = object({ time_up: s('boolean'), exit: s('integer'), status: s('string'), result_file: s('string'), problem: s('string') })
const VERIFY_SCHEMA = object({ time_up: s('boolean'), pass: s('boolean'), failing: strings, summary: s('string') })
const PICK_SCHEMA = object({ time_up: s('boolean'), file: s('string'), picks: { type: 'array', items: FINDING } })
const REPORT_SCHEMA = object({ time_up: s('boolean'), file: s('string') })

let stopped = false
const problems = []
async function step(prompt, opts) {
  if (stopped) return null
  const r = await agent(prompt, opts)
  if (!r) problems.push(`${opts.label}: the agent returned nothing`)
  else if (r.time_up === true) stopped = true
  return r
}
const usable = r => !!r && r.time_up !== true
const scope = [a.tool, ...extra].join(', ')

const ask = brief => `"Read ${brief} and do what it says."`
function reviewCommand(engine, out) {
  if (engine === 'codex') return `timeout 1500 codex exec -m gpt-6.1-sol -s read-only --skip-git-repo-check -o ${out} ${ask(a.review_brief)} </dev/null > ${out}.log 2>&1`
  return `timeout 900 agy -p ${ask(a.review_brief).slice(0, -1)} Do not run shell commands and do not fetch URLs. Write the review itself as your final message, not a plan." --mode plan --model gemini-3.8-flash-medium --print-timeout 840s --output-format text </dev/null > ${out} 2>${out}.err`
}

function readiness() {
  return step(`${COMMON('readiness')}
Step: record the baseline before any change. Run \`${a.test_cmd}\` and \`cd ${a.tool} && ./node_modules/.bin/tsgo --noEmit -p .\`.
Append to ${RUN}/state.md a line \`- <date -Iseconds> baseline: <the commands> → <their pass/fail counts and exits>\`.
pass is true only when both exit 0. summary: the counts.`, { label: 'readiness', phase: 'Readiness', schema: READY_SCHEMA, ...CHEAP })
}

function review(engine, round) {
  const out = `${RUN}/review/r${round}-${engine}.md`
  return step(`${COMMON(`review-r${round}-${engine}`)}
Step: a read-only review on ${engine}, round ${round}, of ${scope}. Run exactly:

    ${reviewCommand(engine, out)}

Then read ${out}. usable is true when it holds a heading "## Findings" followed by numbered findings or "none". If it
does not (empty, an error, a plan instead of a review), do the review yourself, read only, from ${a.review_brief}, write
it to ${out} in the same form, and set redone_by_step true with the reason in problem. file is ${out}.`,
  { label: `review-r${round}-${engine}`, phase: 'Review', schema: REVIEW_SCHEMA })
}

function judge(round, files) {
  const out = `${RUN}/findings-r${round}.md`
  return step(`${COMMON(`judge-r${round}`)}
Step: judge round ${round}'s review findings. Read ${files.join(' and ')}, and ${RUN}/findings.md if it exists (earlier
rounds). Read the judge: ${a.tool}/VISION.md, ${a.tool}/USE_CASES.md, ${a.tool}/REQUIREMENTS.md.
Accept a finding only if it names the use case or requirement id it breaks, gives an input that shows it, and is not
already in ${RUN}/findings.md; check its file:line by reading the code. Merge duplicates across the two reviews.
Write ${out}: one line per finding, \`- R${round}-<n> · accepted|dropped · <requirement id> · <summary> · <input> · <why, for a dropped one>\`.
Append the same lines to ${RUN}/findings.md. accepted: the accepted ones, id R${round}-<n>. dropped: how many.`,
  { label: `judge-r${round}`, phase: 'Judge' , schema: JUDGE_SCHEMA })
}

function reproduce(tag, findings) {
  const test = `test/review-${tag}.test.ts`
  const red = `${NODES}/reproduce-${tag}.red.txt`
  return step(`${COMMON(`reproduce-${tag}`)}
Step: write one acceptance test per finding below in ${a.tool}/${test}, from the finding's own input, using the
helpers of ${a.tool}/test/fixtures/project.ts the way ${a.tool}/test/review.test.ts does. You did not write the
tool's code; do not change it. Findings:
${findings.map(f => `- ${f.id} (${f.requirement}): ${f.summary} — input: ${f.input}`).join('\n')}

Name each test by its finding id. Then run the planned red run:
\`cd ${a.tool} && bun ../.claude/skills/workflow-design/guard/src/cli.ts expect-fail --run "bun test ${test}" --out ../${red}\`.
reproduced: the ids whose test fails for the reason the finding names (read the error in ${red}); not_reproduced: the
ids whose test passes or fails for another reason — delete those tests from the file and run the red run again.
test_file is ${a.tool}/${test}.`, { label: `reproduce-${tag}`, phase: 'Reproduce', schema: REPRO_SCHEMA })
}

function fix(tag, findingsFile, testFile) {
  const brief = `${RUN}/briefs/fix-${tag}.md`
  const log = `${NODES}/fix-${tag}.opencode.log`
  return step(`${COMMON(`fix-${tag}`)}
Step: have opencode fix the tool against the failing tests. Write ${brief}: a copy of ${a.fix_template} with every
"rROUND" replaced by "${tag}", every other "ROUND" by "${tag}", "TESTFILE" by "${testFile.split('/').pop()}" and
"FINDINGS" by "${findingsFile.split('/').pop()}". Check no \`opencode run\` is running (\`ps -eo args | grep -c "[o]pencode run"\`
prints 0; if not, wait for it). Then run in the background, with its own timeout:

    timeout 2400 opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent build --variant high "Read ${brief} and do what it says. Use relative paths only." </dev/null > ${log} 2>&1

When it ends, record its exit, read ${NODES}/fix-${tag}.result.md if it exists (status from it, else "none"), and the
last lines of ${log}; problem: why it stopped, if it did no work. result_file: the result file or "".`,
  { label: `fix-${tag}`, phase: 'Fix', schema: FIX_SCHEMA })
}

function verify(tag) {
  return step(`${COMMON(`verify-${tag}`)}
Step: verify after fix ${tag}. Run \`${a.test_cmd}\`, \`cd ${a.tool} && ./node_modules/.bin/tsgo --noEmit -p .\`, and the
read-only check: \`git status --short\` before and after \`cd ${a.tool} && bun src/cli.ts --project .. --out ../${NODES}/smoke-${tag}.md\`
must differ only by that report. pass is true only when all hold. failing: the failing test names, or the check that
did not hold. Append \`- <date -Iseconds> verify-${tag}: <summary>\` to ${RUN}/state.md.`,
  { label: `verify-${tag}`, phase: 'Verify', schema: VERIFY_SCHEMA, ...CHEAP })
}

// One build pass: reproduce the findings, fix them, verify; one more fix if verify fails.
async function buildPass(tag, findings, findingsFile) {
  const rp = await reproduce(tag, findings)
  if (!usable(rp) || !(rp.reproduced || []).length) return { tag, reproduced: usable(rp) ? rp.reproduced : [], fixed: false }
  let fx = await fix(tag, findingsFile, rp.test_file)
  let vf = usable(fx) ? await verify(tag) : null
  if (usable(vf) && !vf.pass) {
    problems.push(`${tag}: verify failed after the fix (${(vf.failing || []).join('; ')}), one more fix`)
    fx = await fix(`${tag}b`, findingsFile, rp.test_file)
    vf = usable(fx) ? await verify(`${tag}b`) : null
  }
  return { tag, reproduced: rp.reproduced, not_reproduced: rp.not_reproduced, fixed: usable(vf) && vf.pass, verify: usable(vf) ? vf.summary : '' }
}

phase('Readiness')
const ready = await readiness()
if (usable(ready) && !ready.pass) problems.push(`baseline not passing before the run: ${ready.summary}`)

const rounds = []
let judgeFailed = false
for (let round = 1; round <= a.rounds && !stopped; round++) {
  log(`round ${round} of at most ${a.rounds}`)
  const reviews = (await parallel(['codex', 'agy'].map(engine => () => review(engine, round)))).filter(usable)
  if (!reviews.length) { problems.push(`round ${round}: no review came back`); break }
  // A judge that returns nothing (an API error, a refused call) is retried once, then the run stops its rounds with a
  // problem: findings are never fixed or enhanced around an unjudged review (run 20261017-memory-check-review).
  let j = await judge(round, reviews.map(r => r.file))
  if (!j && !stopped) j = await judge(round, reviews.map(r => r.file))
  if (!usable(j)) { if (!stopped) { problems.push(`round ${round}: the judge returned nothing twice; ${reviews.length} review(s) left unjudged`); judgeFailed = true } break }
  if (!(j.accepted || []).length) { rounds.push({ round, accepted: 0, dropped: j.dropped, dry: true }); log(`round ${round}: nothing accepted — the review is dry`); break }
  const pass = await buildPass(`r${round}`, j.accepted, j.file)
  rounds.push({ round, accepted: j.accepted.length, dropped: j.dropped, ...pass })
}

let enhance = null
if (!stopped && !judgeFailed) {
  phase('Enhance')
  const ex = await workflow('experts-decide', { run: RUN, question: a.enhance_question, out: 'enhance-q' })
  if (ex && ex.status === 'done') {
    const pk = await step(`${COMMON('pick')}
Step: pick the enhancements. Read ${RUN}/enhance-q/compare.md and the six answers. Keep only proposals that name a use
case or vision line of ${a.tool} and a case that shows the need; pick the top one or two most of the experts agree on
(R12.3: the main pick is applied; the owner may overrule). Write ${RUN}/enhance.md: each pick, its use case, why, how
to check it is done; and the proposals not picked, with why. picks: as findings, id E-<n>, requirement the use case,
input the case that shows the need.`, { label: 'pick', phase: 'Enhance', schema: PICK_SCHEMA })
    if (usable(pk) && (pk.picks || []).length) enhance = await buildPass('enh', pk.picks, pk.file)
  } else problems.push('enhance: experts-decide did not finish')
}

phase('Report')
const rep = await step(`${COMMON('report')}
Step: write ${RUN}/report.md for the owner: per round, the findings accepted and dropped (from ${RUN}/findings.md), what
was reproduced, fixed and verified; the enhancements picked and built (${RUN}/enhance.md); every problem below; what is
open. Plain words, short. Problems: ${JSON.stringify(problems)}. Rounds: ${JSON.stringify(rounds)}.`,
{ label: 'report', phase: 'Report', schema: REPORT_SCHEMA, ...CHEAP })

const out = { rounds, enhance, report: usable(rep) ? rep.file : '', problems }
if (stopped) out.stopped = 'time is up'
return out
