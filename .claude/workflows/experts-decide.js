export const meta = {
  name: 'experts-decide',
  description: 'Ask the six experts one question, each in its own subfolder; check each answer; rerun an expert with no usable answer once; compare them in compare.md. Returns the summary; decides nothing.',
  whenToUse: 'When a decision needs the six experts (skill six-experts) as a saved, clocked workflow. args: {run: "runs/<YYYYMMDD-slug>", question: "<question file inside the repo>", out: "<subfolder>", only?: ["linus", ...], insights?: "instruction,check", needsWeb?: true, approveOrChange?: true (the answer is APPROVE or CHANGE: the experts get the rules as a card and answer in the vote form), research?: "<a research question>"}. Writes under <run>/<out>/, <run>/nodes/<out>.progress.md and, with research, <run>/research/. The main agent reads the summary and decides.',
  phases: [
    { title: 'Research', detail: 'only with args.research: answer it from the web and add the findings to a copy of the question' },
    { title: 'Ask', detail: 'one step per expert, each its own --out subfolder; 老子 (opencode) alone, after the others' },
    { title: 'Check', detail: 'six_experts.py check per expert, that expert\'s lines only; one rerun for an expert with no usable answer' },
    { title: 'Compare', detail: 'read every answer and write <run>/<out>/compare.md' },
  ],
}

// Design: runs/20261017-workflows/design.md, section experts-decide. Skill: .claude/skills/six-experts/SKILL.md.
// Every step is an agent (the script has no shell and no clock). Every agent runs `deadline status` first and returns
// time_up when it prints "time is up"; then no further step starts. The script decides nothing (method 3.8 item 14).

const opts = args && typeof args === 'object' ? args : {}
const str = x => (typeof x === 'string' ? x.trim() : '')
const err = reason => ({ status: 'error', reason })

const IDS = ['linus', 'fan-li', 'sun-tzu', 'lao-tzu', 'dave', 'dario']
const ALONE = 'lao-tzu' // opencode cannot run twice at once, so 老子 runs on its own, after the others
const RUNNER = 'python3 .claude/skills/six-experts/scripts/six_experts.py'
const CLOCK_CMD = 'bun .claude/skills/workflow-design/guard/src/cli.ts deadline status'
const CMD_MODEL = { model: 'claude-haiku-5-5', effort: 'low' }

const RUN = str(opts.run)
const QUESTION = str(opts.question)
const OUT = str(opts.out)
if (!RUN) return err('args.run is missing. Pass {run: "runs/<YYYYMMDD-slug>", question: "<file>", out: "<subfolder>"}.')
if (!/^runs\/[0-9]{8}-[a-z0-9][a-z0-9-]*$/.test(RUN)) return err(`args.run must look like runs/20261017-short-name, got "${RUN}".`)
if (!QUESTION) return err('args.question is missing: the path of the question file, inside the repo.')
// The script cannot read files, so "inside the repo" is checked on the path: relative, no "..", shell-safe characters.
if (!/^[A-Za-z0-9._\/-]+$/.test(QUESTION) || QUESTION.startsWith('/') || QUESTION.split('/').includes('..'))
  return err(`args.question must be a relative path inside the repo (no leading "/", no "..", letters, digits, . _ - / only), got "${QUESTION}".`)
if (!OUT) return err('args.out is missing: the subfolder of the run for this question.')
if (!/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(OUT)) return err(`args.out must be one folder name (letters, digits, . _ -), got "${OUT}".`)
const ONLY = opts.only == null ? IDS : (Array.isArray(opts.only) ? opts.only : String(opts.only).split(',')).map(s => String(s).trim()).filter(Boolean)
const unknown = ONLY.filter(s => !IDS.includes(s))
if (unknown.length) return err(`unknown expert id(s): ${unknown.join(', ')}. Known: ${IDS.join(', ')}.`)
if (!ONLY.length) return err('args.only names no expert.')
const SIDS = IDS.filter(s => ONLY.includes(s))
const INSIGHTS = str(opts.insights)
if (INSIGHTS && !/^[a-z]+(,[a-z]+)*$/.test(INSIGHTS)) return err(`args.insights must be a comma list of category names, got "${INSIGHTS}".`)
const NEEDS_WEB = opts.needsWeb === true
// An approve-or-change question: the rules as a card and the vote form (run 20261017-experts-speed-trial).
const APPROVE = opts.approveOrChange === true
const RESEARCH = str(opts.research)

const PROGRESS = `${RUN}/nodes/${OUT}.progress.md`
const dirOf = sid => `${RUN}/${OUT}/${sid}`
// With research, the experts are asked from a copy of the question with the findings added.
const QFILE = RESEARCH ? `${RUN}/research/${OUT}.question.md` : QUESTION

const COMMON = `You are one step of the experts-decide workflow in this repository (its root is your working folder).
Another session also commits here: change only the files this step names, never commit, never git add or stash.

First run: ${CLOCK_CMD}
If it prints "time is up" (exit 1), do nothing else: return time_up true and every other field empty, 0 or false.
Exit 2 (no deadline recorded) or exit 0: go on.

Write files with the Write tool, never with a heredoc.`
const progressLine = piece => `Append one line to ${PROGRESS} as you start and one as you end, with:
  echo "- $(date -Iseconds) · ${piece} · start · " >> ${PROGRESS}
  echo "- $(date -Iseconds) · ${piece} · done · <short note>" >> ${PROGRESS}   (fail instead of done when it failed)`

const obj = (properties, extra = {}) => ({ type: 'object', properties, required: Object.keys(properties), ...extra })
const S = { type: 'string' }, B = { type: 'boolean' }, N = { type: 'integer' }, LIST = { type: 'array', items: { type: 'string' } }
const RESEARCH_SCHEMA = obj({ time_up: B, file: S, digest: S })
const ASK_SCHEMA = obj({ time_up: B, sid: S, exit: N, ok: B, answer_bytes: N, problem: S })
const CHECK_SCHEMA = obj({ time_up: B, sid: S, pass: B, failures: LIST })
const COMPARE_SCHEMA = obj({
  time_up: B, file: S, agree: LIST, disagree: LIST, dissent: LIST,
  questions: { type: 'array', items: obj({ question: S, options: LIST }) },
})

let stopped = false
const agentsRun = []
async function step(label, prompt, o) {
  if (stopped) return null
  agentsRun.push(label)
  const r = await agent(prompt, { label, ...o })
  if (r && r.time_up) stopped = true
  return r
}

const askPrompt = (sid, again) => `${COMMON}

Your step: ${again ? 'ask once more' : 'ask'} the expert "${sid}". Run exactly this command with the Bash tool, timeout 590000 ms:

${RUNNER} run --question-file ${QFILE} --out ${dirOf(sid)} --only ${sid}${sid === 'dave' && INSIGHTS ? ` --insights ${INSIGHTS}` : ''}${NEEDS_WEB ? ' --needs-web' : ''}${APPROVE ? ' --card --vote' : ''} --progress ${PROGRESS} --timeout 540 </dev/null

The runner writes its own progress lines; do not add any. Do not change the command, do not answer the question yourself.
When it ends, read ${dirOf(sid)}/status.json (the "${sid}" entry) and count the bytes of ${dirOf(sid)}/answers/${sid}.md
(wc -c; 0 when it does not exist). Return sid "${sid}", the command's exit code, ok and problem from that entry
(ok false and the reason in problem when the entry is missing, for example after a Bash timeout), and answer_bytes.`

const checkPrompt = sid => `${COMMON}

Your step: check the expert "${sid}". ${progressLine(`check-${sid}`)}
Run: ${RUNNER} check ${dirOf(sid)} </dev/null
The folder holds this expert only, so the output also lists the other experts as "no answer file", and the summary
line says FAIL; ignore every line that is not about ${sid}. Return sid "${sid}", failures = each "FAIL ${sid}: ..." line
verbatim without the leading "FAIL ", and pass = true when there is none.`

// A usable answer: the runner said ok, and check found the file and every section.
const usable = (sid, ask, check) => !!(ask && ask.ok && check && !(check.failures || []).some(f =>
  f.startsWith(`${sid}: no answer file`) || f.startsWith(`${sid}: missing section`)))

const results = {}
async function expert(sid) {
  const r = (results[sid] = { sid, dir: dirOf(sid), ask: null, check: null, rerun: null, recheck: null })
  r.ask = await step(`ask ${sid}`, askPrompt(sid, false), { phase: 'Ask', schema: ASK_SCHEMA, ...CMD_MODEL })
  if (stopped) return r
  r.check = await step(`check ${sid}`, checkPrompt(sid), { phase: 'Check', schema: CHECK_SCHEMA, ...CMD_MODEL })
  if (stopped || usable(sid, r.ask, r.check)) return r
  r.rerun = await step(`rerun ${sid}`, askPrompt(sid, true), { phase: 'Ask', schema: ASK_SCHEMA, ...CMD_MODEL })
  if (stopped) return r
  r.recheck = await step(`recheck ${sid}`, checkPrompt(sid), { phase: 'Check', schema: CHECK_SCHEMA, ...CMD_MODEL })
  return r
}

const summary = () => SIDS.map(sid => {
  const r = results[sid]
  if (!r) return { sid, started: false }
  const ask = r.rerun || r.ask, check = r.recheck || r.check
  return { sid, dir: r.dir, rerun: !!r.rerun, usable: usable(sid, ask, check), exit: ask ? ask.exit : null,
    problem: ask ? ask.problem : 'not asked', check_pass: check ? check.pass : null, failures: (check && check.failures) || [] }
})
const finish = extra => ({ run: RUN, out: OUT, question_file: QFILE, agents: agentsRun, experts: summary(), ...extra })
const stop = extra => finish({ status: 'stopped', stopped: 'time is up', ...extra })

let research = null
if (RESEARCH) {
  phase('Research')
  research = await step('research', `${COMMON}

Your step: research, before the experts are asked. ${progressLine('research')}
Answer this research question from the web: "${RESEARCH}"
Write the findings to ${RUN}/research/${OUT}.md, each one labelled verified (you opened the source and it says so,
with its URL) or reported (a source says it and you could not confirm it). Then write ${QFILE}: the text of
${QUESTION} copied verbatim, followed by a section "## Research findings" with the findings and their labels.
Return file "${RUN}/research/${OUT}.md" and a digest of the findings in at most five lines.`, { phase: 'Research', schema: RESEARCH_SCHEMA })
  if (stopped) return stop({ research })
}

phase('Ask')
await parallel(SIDS.filter(s => s !== ALONE).map(s => () => expert(s)))
if (stopped) return stop({ research })
if (SIDS.includes(ALONE)) await expert(ALONE)
if (stopped) return stop({ research })

phase('Compare')
const lines = summary().map(e => `- ${e.sid}: answer ${e.dir}/answers/${e.sid}.md, status ${e.dir}/status.json; ` +
  `${e.usable ? 'usable' : 'NO USABLE ANSWER'}${e.rerun ? ' (after one rerun)' : ''}; check ${e.check_pass ? 'pass' : 'fail'}` +
  `${e.failures.length ? ': ' + e.failures.join(' | ') : ''}`).join('\n')
const compare = await step('compare', `${COMMON}

Your step: compare the experts' answers. ${progressLine('compare')}
The question: ${QFILE}. The experts, their files and their check results:
${lines}

Read .claude/skills/six-experts/SKILL.md section "3. Compare" and every usable answer, then write ${RUN}/${OUT}/compare.md
in that shape: the table, where they agree, where they disagree (side by side, quoted, never averaged), what each added
that the others did not, what they need to know (the questions merged, each with its options), and the check (the
results above; engines and any fallback from each status.json; the check script was written by Claude and does not
establish that a rule was applied correctly). Label each line quoted, my reading, or not measured. An expert with no
usable answer is listed as such, never filled in. Do not pick a winner and do not decide: the main agent decides.
Return file "${RUN}/${OUT}/compare.md"; agree, disagree and dissent (who stands alone, and on what) as short lines;
questions, each with its options.`, { phase: 'Compare', schema: COMPARE_SCHEMA })
if (stopped) return stop({ research, compare })

return finish({ status: 'done', research, compare })
