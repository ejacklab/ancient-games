# Dave — review of the eleven harness-health requirements

## Answer
Keep the list, but stop treating config as health. On this project's own record, the config check catches 0 of 7 failures. A fast check on each dispatch's *result* (did the file appear, is it non-empty, is it in the right shape, did it finish in the time expected) would catch most or all of the 7 on paper (my reading, not measured). R11.2 plus two new items (N1, N2) should therefore carry the weight, and R1–R10 should be split into the part readiness can prove and the part that only a run can show. If a cheap replay of the 7 failures (see the last section) shows the output check doing no better than the config check, this answer is wrong.

## How I decided

1. **What would change my mind (my #1).** I would change it if planting the 7 recorded failure outputs showed that a result check catches no more of them than the config check does. Until that replay runs, everything below is a prediction.

2. **Start from the data we already have (my #5).** Two things are already measured. First, what `harness_health.py` reads: config only, and it says so ("configured is not enforced"). Second, the backtest: 0 of 7 recorded failures flagged. What the data shows: all 7 are behaviour at dispatch, and most exited 0. What it does not show: it is the main agent's reading on paper, not a run. Also, 7 is a small n, so this is a hint, not a law (my #10).

3. **Compare against a control (my #4).** The control is "no harness-health check at all". It also catches 0 of 7. So on the recorded failures, the built check adds nothing over doing nothing. That is a null result and has to be reported as one (my #9). It does not mean the check is useless: R6 and R8 do fail on this machine today (no deny rule, sandbox off, bypass prompt skipped). It means those flags are not what has hurt this project.

4. **Verdict on each requirement** (all ten came from an outside source with an unknown author, so their basis is n=0 here, my #10):

| Req | Verdict | Readiness check that can fail | What readiness cannot prove |
|---|---|---|---|
| R1 Context | **Split.** R1a: each engine the design will use has the instruction file *that engine* reads. R1b: context budget. | R1a: for each planned engine, its instruction file exists and is readable. Planted failure: dispatch to Codex with only `CLAUDE.md` present must fail. | R1b. "Short" and "budget" are weak words with no comparison. It can only be measured after a run, by comparing tokens per node against earlier runs. |
| R2 Tools | **Change.** It is a design standard for tools the project builds, not a harness state. | None at readiness. "Covered by a script" proves the script exists, not that it works. | Whether interfaces are unambiguous. That is a judge in R11's sense, not a readiness line. |
| R3 Planning | **Keep; move to step 2.** | At step 2: every step names its check, and a step without one is flagged as an unclear spot. Planted failure: a step with no check must be flagged. | Not a readiness item. Readiness comes before the plan exists. |
| R4 State/memory | **Change.** "Memory directories exist" is the wrong measure. | The run's state file exists and its Steps table parses. Planted failure: a malformed table must fail. | Whether a fresh context can actually resume. Testing that means starting a new session from the state file only, which costs quota and needs EJ's go-ahead (house rule). |
| R5 Independent verification | **Merge with R11** (surfacing the conflict, not averaging it). R5 says "separate evaluator agent"; R11.1 says "any judge". R5 becomes the readiness *list of judges*. | The test command is *run* (no model quota) and must exit. Planted failure: a deliberately broken test must make it fail. Linters and eval tools are each run once. | Whether the judges catch real errors. That is R11.1's job, after step 2. |
| R6 Guardrails | **Split.** R6a: config (sandbox, deny rules, least privilege). R6b: prompt-injection defence. | R6a is checkable and fails today on this machine, so it has been shown failing on real input. Label it `reported`, because configured is not enforced. agy, qwen, dsh and opencode stay `unknown` until their formats are verified. | R6b, and enforcement in general. Possible **MUST** candidate (it is a safety bound). That is EJ's call. |
| R7 Recovery/retries | **Change; move to the design step.** | Every dispatch loop in the design has a retry cap and a stop condition. Planted failure: an uncapped loop must fail. | Idempotence and rollback. Trap 6 (agy transient 502) belongs here: one verified login does not prove the next one. |
| R8 Human gates | **Split.** R8a: config (bypass prompt, `approval_policy`). R8b: the design names which nodes need EJ's approval. | R8a, like R6a, fails today and is `reported`. R8b at step 2: an irreversible action with no approval point must fail. | Possible **MUST** candidate (safety bound). EJ's call. |
| R9 Observability | **Change.** | For each planned engine: a known log location exists and has an entry newer than the last dispatch. Planted failure: an empty log folder must fail. | Tokens and cost per action. Claude's transcripts carry usage; for the other engines it is not given to me (see what I need to know). |
| R10 Feedback loop | **Change.** "Hooks present" is a stand-in. Make it: each recorded harness failure has a check that catches its signature, shown failing on a planted repeat. | Count recorded failures that have a check. Today that is **0 of 7** (memory notes are `reported`, not checks), so this check fails now, which is what we want from it. | "Review as models improve". Retiring scaffolding needs a with/without control run (my #4), which costs quota. |
| R11.1 | **Keep, with one addition:** a judge counts only once it has been shown failing on a planted wrong input (house rule). | Readiness lists the judges. The percentage is counted after step 2, as the main agent proposed. That is the right fix for where R11 sits: readiness cannot count prompts that do not exist yet. "Exists before the prompt is sent" can be checked by comparing the judge's commit time with the dispatch time. | The 80% is n=0 (my #3, my #10). Before using it, count past designs in `runs/` (no quota, my #5) and write down what share of prompts already had a judge. Otherwise we cannot tell whether 80% binds anything. |
| R11.2 | **Keep.** It is the item most likely to have caught the 7. | Readiness checks that each judge has a first check written, and that the expected duration is in the design. | Whether the first check really runs faster than the prompt. That is measured at run time, comparing check time against prompt time. |

5. **Why R11.2 matters most (my #4, my reading on paper).** A fast first check on the result could catch each of the seven:
   - Output missing or empty with exit 0 catches 3 (opencode reject), 4 (agy soft-deny) and 7 (refused heredoc writes).
   - Answer not in the return shape catches 5 (plan instead of answer).
   - Ran longer than the expected duration catches 1 (codex hang). This works because R11.2 makes the expected duration be written down.
   - Error text or non-zero exit catches 2 (database locked) and 6 (502).

   That gives roughly 7 of 7 for a result check against 0 of 7 for the config check. **Not measured.** It is my reading of one-line descriptions.

6. **How nature solves it (my #6), and whether the analogy fits (my #7).** Immune memory.
   - **Same:** each failure that was met before leaves a specific detector for its signature (exit 0 + empty output, stdin hang, plan instead of answer). That is R10 done properly. There is also a fast generic layer (innate) and a slow specific layer (adaptive), which matches R11.2's first signal followed by the full verdict.
   - **Different:**
     - Immunity detects *on contact with the threat*, not ahead of time. That fits checks on the result, and it does not fit readiness, which runs before any contact.
     - In immunity the fast layer also *feeds* the slow one rather than only gating it.
   - **Conclusion:** keep the analogy for "a detector per recorded failure, checked on the result". Drop it as an argument for doing more at readiness, because the key condition (meeting the threat) is missing there.

7. **Small and reversible first (my #8).** agy accounts for 3 of the 7 failures. Try the result check on the agy path alone first, measure it, then spread it.

8. **Q1: count over prompts or over criteria? (my #1, my #5, then conditional).**
   - Whether this matters can be measured: count both ways on past designs. If every prompt has exactly one criterion, Q1 makes no difference.
   - If they differ: counting over prompts lets a prompt with three criteria and one judge count as "judged", which inflates the share.
   - **If** EJ wants to keep counting over prompts (their own words: "insight the prompt results"), **then** a prompt should count only when *every* one of its criteria has a judge. That makes the two ways of counting equally strict. This is proposed, not decided; it is EJ's choice.

9. **Q2: does a design-standard document count as a judge? (house rule "every check must be able to fail", my #4).** A document alone cannot fail, so counting it would inflate R11.1 and nothing would stop it.
   - **If** EJ wants design standards in (their words list them), **then** count the standard *together with what applies it* (a script, a linter, or an evaluator that reads the standard and returns pass or fail), and only after that pair has been shown failing on a planted violation.
   - EJ decides.

10. **What the list misses.** Each of these is a question for EJ, not a decision:
    - **N1. Exit 0 is not success.** Every dispatch's result goes through a fast output check (expected file exists, non-empty, in the return shape) before anything reads it.
      - *Catches:* failures 3, 4, 5 and 7.
      - *Overlap:* close to R11.2, but R11.2 is about judging the *answer*, and N1 is about whether the harness produced *any* answer.
    - **N2. A trap lint on dispatch commands,** read from a per-engine data file of known traps (not hardcoded, so it works in other projects).
      - *Catches before sending:* failure 1 (`codex exec` without `</dev/null`), 2 (parallel opencode starts), 3 (opencode inputs outside the repo), 5 (agy in plan mode) and 7 (heredoc writes in a worktree brief).
      - *Planted failure:* a `codex exec` line without the redirect must fail the lint.
      - *When it runs:* after step 2. Readiness can only check that the trap file loads.
    - **N3. A wall-clock limit per dispatch,** taken from the expected duration R11.2 already asks for.
      - *Catches:* failure 1 (hang until timeout).
      - Could fold into R7.
    - **N4. Engine versions recorded at readiness** (`--version`: verified, no quota).
      - *Catches:* a trap entry that has gone stale after an upgrade, and new behaviour that an old pass hides. This is the measurable part of R10's "review as models improve".
    - **N5. The health check is scored against the failure log every time it changes** (the backtest, re-run).
      - *Catches:* a check that grows in size but catches nothing. Today's 0 of 7 would be reported, not hidden (my #9).
    - **N6. No secret in the report.** Scan the health output for key-like strings.
      - *Planted failure:* a fake key in a config must not appear in the output.
      - *Catches:* breaking the "never print a secret" house rule, which today rests on trust alone.

## What I need to know
- Whether agy, qwen, dsh and opencode write tokens and cost anywhere locally. If they do not, R9's cost part is `unknown` for four of six engines.
- Whether a deny rule or sandbox can be tested to *fail* without a model call. If yes, R6a moves from `reported` to `verified`. If no, it stays `reported`, or needs a canary and EJ's go-ahead.
- How many prompts in past designs carried more than one criterion. This decides whether Q1 matters at all.
- Whether EJ wants R6 and R8 as MUST (a safety bound) or as SHOULD.
- Whether the seven failures are the full record or only the ones written down. If there are unrecorded ones, the 7 is a lower bound and both backtests are optimistic.

## Costs and risks
- **N1 and R11.2 (from my #4):** they add a check step to every dispatch. That is small, but it is code that must itself be shown failing once. They also find a failure only *after* it costs quota. They cut the damage, not the spend.
- **N2 (from my #6 and #7):** the trap lint only knows yesterday's traps. A new trap passes until it is recorded. The trap file needs an owner, or it goes stale.
- **Splitting R1, R6 and R8 (my reading):** the list grows from 11 to about 14 lines, and each new line needs a planted failure.
- **Moving R3, R7, R8b and R11.1's count to step 2 (my reading):** readiness proves less on its own. It is honest, but the readiness report will look emptier.
- **Counting past designs for the 80% and for Q1 (my #3, my #5):** an hour or so of work. It may show that 80% binds nothing or binds everything, which forces EJ to reopen the number.
- **Everything above (my #10):** it rests on 7 cases read on paper by the main agent and by me. Neither of us is an independent judge of a check we reasoned about.

## How we would know I was right
- **Prediction, written before the result (my #3).** Replay the 7 recorded failures as planted outputs and commands: an empty file, a plan instead of an answer, a missing file, a `codex exec` line without `</dev/null`, two parallel opencode starts, an error with exit 0, and a run past its expected duration. This costs no model quota (my #2).
  - I predict N1 + R11.2 + N2 together flag **at least 6 of the 7**.
  - I predict the current `harness_health.py` flags **0 of the 7** (the control, my #4).
  - Stop date: before R11.2 moves from proposed to accepted.
- **I am wrong if** the result check flags about as few as the config check (my #1). That result gets reported with the same weight as a win (my #9).
- **Forward test (my #8).** On the agy path first, over the next runs, compare two counts:
  - harness failures the result check caught at dispatch;
  - harness failures found later by a human.

  If the human keeps finding ones the check missed, the check is not doing its job.
