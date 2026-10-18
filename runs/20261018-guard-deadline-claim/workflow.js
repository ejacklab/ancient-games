export const meta = {
  name: 'guard-deadline-claim',
  description: 'Research, fix, test and evaluate the guard defect: a session claims another run\'s deadline (design.md)',
  whenToUse: 'Run 20261018-guard-deadline-claim. args: {rounds: N (repair rounds, default 2)}. Start the run\'s deadline first with the full-path deadline start --run runs/20261018-guard-deadline-claim.',
  phases: [
    { title: 'Research', detail: 'repo starts table and harness payload facts, in parallel' },
    { title: 'Experts', detail: 'six experts on the fix options (experts-decide)' },
    { title: 'Spec', detail: 'the main agent writes SPEC Round 21 from the compare (outside this script)' },
    { title: 'Tests', detail: 'Claude, red first, the incident replayed' },
    { title: 'Code', detail: 'opencode; Codex if opencode stays busy' },
    { title: 'Verify', detail: 'Sonnet: suite, tsgo, test hashes' },
    { title: 'Review', detail: 'Codex read-only, a Claude judge reproduces each finding; repair rounds' },
    { title: 'Evaluate', detail: 'replay, rate before/after, planted repeat' },
  ],
}

// Design: runs/20261018-guard-deadline-claim/design.md. The script stops after the experts (phase 1) when
// args.phase is not 2: the main agent writes SPEC Round 21 from their compare, then reruns with {phase: 2}.

const RUN = 'runs/20261018-guard-deadline-claim'
const NODES = `${RUN}/nodes`
const G = '.claude/skills/workflow-design/guard'
const ROUNDS = Number.isInteger(args && args.rounds) && args.rounds > 0 ? args.rounds : 2
const PHASE2 = args && args.phase === 2
const COMMON = name => `You are step ${name} of a workflow. First run: cd "$(git rev-parse --show-toplevel)" — the repository root is your working folder; use paths relative to it.
Then run: bun ${G}/src/cli.ts deadline status --run ${RUN} — if it prints "time is up" (exit 1), do nothing else and return time_up true with every other field empty. Any other harness-guard "time is up" line is about another deadline: ignore it.
Another session also commits here: change only the files this step names; never commit, git add or stash.
Use the Bash tool's timeout 600000 ms for long commands. Report what commands printed, not what you expect.
Append \`- <date -Iseconds> · ${name} · start|done · <note>\` to ${NODES}/${name}.progress.md as you start and end.
`
const T = { time_up: { type: 'boolean' } }
const S = props => ({ type: 'object', properties: { ...T, ...props }, required: ['time_up', ...Object.keys(props)] })
const str = { type: 'string' }
const list = { type: 'array', items: str }
const up = r => !r || r.time_up === true

if (!PHASE2) {
  phase('Research')
  const [repo, harness] = await parallel([
    () => agent(`${COMMON('research-repo')}
Step: read ${RUN}/facts.md and ${RUN}/design.md §1. Find every path in ${G}/src that writes \`session\` into a deadline
file. Then every \`deadline start\` call in this machine's Claude Code transcripts (~/.claude/projects/*/*.jsonl, and
subagent transcripts under them): its session, its time, its command form (full path, \`bun src/cli.ts\`, \`bun $VAR\`,
other), the id it printed, and the session that file carries now in .harness-guard/deadlines/ (or "gone"). Write
${RUN}/research/starts.md (Write tool): one row per start, then the counts — claimed by its own session, by another, by
none. Read only otherwise.`, { label: 'research-repo', phase: 'Research', schema: S({ starts: { type: 'number' }, own: { type: 'number' }, other: { type: 'number' }, none: { type: 'number' }, claim_paths: list, file: str }) }),
    () => agent(`${COMMON('research-harness')}
Step: answer three questions about Claude Code hooks, each with a doc page (code.claude.com docs, or the claude-code-guide
agent's cited answer) or a probe: (1) does a PostToolUse payload for Bash carry the command's stdout (tool_response),
and in what field; (2) does a Bash command's environment hold the session id (which variable); (3) what session_id do
the hooks of a subagent and of a workflow agent report — the parent's or their own. For a probe: a scratch settings
file is NOT allowed (harness config needs the owner's yes); read the payloads the guard already journals in
.harness-guard/journal.jsonl and the guard's own hook-payload tests instead. Write ${RUN}/research/harness.md (Write
tool): each answer, its source, or "not established".`, { label: 'research-harness', phase: 'Research', schema: S({ stdout_field: str, session_env: str, subagent_session: str, file: str }) }),
  ])
  if (up(repo) || up(harness)) return { stopped: 'time_up or research missing', repo, harness }

  phase('Experts')
  const experts = await workflow({ scriptPath: '.claude/workflows/experts-decide.js' }, {
    run: RUN, question: `${RUN}/fix-question.md`, out: 'fix-q',
  })
  return { phase: 1, repo, harness, experts, next: 'the main agent writes SPEC Round 21 from fix-q/compare.md and the briefs, then reruns with {phase: 2}' }
}

phase('Tests')
const tests = await agent(`${COMMON('tests')}
Step: write tests for SPEC Round 21 (the last section of ${G}/SPEC.md). You write tests only; another engine writes the
code. Read first and assert the way they do: ${G}/test/round10*.test.ts, ${G}/test/round20-deadline.test.ts. File:
${G}/test/round21.test.ts (Write tool). Cases: the incident replayed from ${RUN}/facts.md (D-593045da started by session
B with \`bun $G deadline start\`, then session A starts its own 27 s later: A must not own B's deadline); the three
command forms of facts.md; a start whose claim was missed; a workflow agent's call (its session as
${RUN}/research/harness.md says); and every Fails-if line of Round 21. Red run:
cd ${G} && bun src/cli.ts expect-fail --run "bun test test/round21.test.ts" --out ../../../../${NODES}/r21-tests.red.txt
Then sha256sum ${G}/test/round21.test.ts > ${NODES}/r21-test-hashes.txt. Every other guard test still passes.`,
  { label: 'tests', phase: 'Tests', schema: S({ red: list, not_red: list, problem: str }) })
if (up(tests)) return { tests }

const code = (tag, extra) => agent(`${COMMON('code-' + tag)}
Step: have an engine write the code from ${RUN}/briefs/r21-code.md${extra ? ` plus, at its end, "## Still failing": ${extra} (write ${RUN}/briefs/r21-code-${tag}.md with the Write tool: the brief with that section added)` : ''}.
Wait until no opencode runs (\`ps -eo args | grep -c "[o]pencode run"\` prints 0; sleep 60 between checks, up to 30 minutes), then in the background (run_in_background) and wait:
  timeout 2400 opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent build --variant high "Read ${RUN}/briefs/r21-code${extra ? '-' + tag : ''}.md and do what it says. Use relative paths only." </dev/null > ${NODES}/r21-code-${tag}.opencode.log 2>&1
If opencode is still busy after 30 minutes, run Codex instead, the same way:
  timeout 2400 codex exec -m gpt-6.1-sol -c model_reasoning_effort=high -s workspace-write "Read ${RUN}/briefs/r21-code${extra ? '-' + tag : ''}.md and do what it says." </dev/null > ${NODES}/r21-code-${tag}.codex.log 2>&1
Record which engine ran and its exit; read ${NODES}/r21-code.result.md (status, else "none").`,
  { label: 'code-' + tag, phase: 'Code', schema: S({ engine: str, exit: { type: 'number' }, status: str, problem: str }) })
const verify = tag => agent(`${COMMON('verify-' + tag)}
Step: verify. cd ${G} && bun test; cd ${G} && ./node_modules/.bin/tsgo --noEmit -p .; sha256sum -c ${NODES}/r21-test-hashes.txt
(the coder may not edit tests); git diff --stat -- ${G}/src shows only the files ${RUN}/briefs/r21-code.md names. pass only when all hold.`,
  { label: 'verify-' + tag, phase: 'Verify', schema: S({ pass: { type: 'boolean' }, failing: list, summary: str }), model: 'claude-sonnet-5-5' })
const review = n => agent(`${COMMON('review-' + n)}
Step: run Codex read-only on ${RUN}/briefs/review.md in the background and wait:
  timeout 1500 codex exec -m gpt-6.1-sol -c model_reasoning_effort=high -s read-only --skip-git-repo-check -o ${NODES}/review-${n}.md "Read ${RUN}/briefs/review.md and do what it says." </dev/null > ${NODES}/review-${n}.log 2>&1
Then judge each finding in ${NODES}/review-${n}.md: read the code at its file:line and the SPEC line it quotes; reproduce
with a read-only probe in a scratch dir (removed after). reproduced: the findings shown in today's code, each as
"<n>: <summary> — input: <input>"; dropped: each with its reason. Write ${NODES}/review-${n}-judge.md (Write tool).`,
  { label: 'review-' + n, phase: 'Review', schema: S({ reproduced: list, dropped: list }) })

phase('Code')
let c = await code('a')
phase('Verify')
let v = !up(c) ? await verify('a') : null
if (v && !v.pass && !up(v)) { c = await code('a2', v.failing.join('; ')); v = !up(c) ? await verify('a2') : null }
const rounds = []
for (let n = 1; n <= ROUNDS && v && v.pass; n++) {
  phase('Review')
  const r = await review(n)
  rounds.push(r)
  if (up(r) || !r.reproduced.length) break
  const t2 = await agent(`${COMMON('tests-r' + n)}
Step: add one red-first test per reproduced review finding to ${G}/test/round21.test.ts (Write or Edit tool), the way
the file already does: ${r.reproduced.join(' | ')}. Red run: cd ${G} && bun src/cli.ts expect-fail --run "bun test test/round21.test.ts" --out ../../../../${NODES}/r21-r${n}.red.txt
Then sha256sum ${G}/test/round21.test.ts > ${NODES}/r21-test-hashes.txt.`, { label: 'tests-r' + n, phase: 'Review', schema: S({ red: list, problem: str }) })
  if (up(t2)) break
  c = await code('r' + n, r.reproduced.join(' | '))
  v = !up(c) ? await verify('r' + n) : null
}

phase('Evaluate')
const evaluation = v && v.pass ? await agent(`${COMMON('evaluate')}
Step: evaluate the fix; you wrote none of it. Write each measure's command and output under ${RUN}/evaluate/ (Write tool).
1. Replay: copy .harness-guard/deadlines/ to a scratch folder as it was before the incident (D-593045da and D-17979aae
   unclaimed, from ${RUN}/facts.md), and feed the old claim (git show HEAD~:${G}/src/hooks.ts and deadline.ts in a
   scratch worktree at the commit before the fix) and the new one the two real start calls of facts.md as hook
   payloads, in their real order. Old: session 1159cce6 owns D-593045da. New: it does not; 16098663 owns its own.
2. Rate: re-score ${RUN}/research/starts.md under the new rule: starts claimed by another session or by none, before
   against after.
3. Planted repeat: in a scratch worktree, put the old claim line back into the new code; bun test test/round21.test.ts
   must fail. Remove the worktree after.`, { label: 'evaluate', phase: 'Evaluate', schema: S({ replay: str, rate_before: str, rate_after: str, plant_caught: { type: 'boolean' }, problem: str }) }) : null

return { tests, code: c, verify: v, rounds, evaluation }
