# Linus Torvalds — What pre-flight should verify

## Answer

My reading, applying my #13 and #2: start with readable input, accessible dependencies, and unfilled template fields; add checks for launch contradictions only where the runner exposes explicit values. The ranking is provisional, **n=0**: the supplied files establish what can be checked, but do not measure which checks save the most failed calls.

## How I decided

1. **Identify the actual handoff — my #9 and #11.**

   In `six_experts.py:205–207`, the runner already rejects an empty question. It then generates expert briefs and dispatches a path through `prompt_for`. The worker template supplies a different contract: task, context, template, example, standard, progress, limits, and result destination.

   My reading: validate the **finished file handed to the engine**, using the contract for that kind of file. Requiring worker headings in an expert question would reject legitimate work.

2. **Check these in this provisional order — my #13, #9 and #11; the specific predicates are my reading.**

   | Priority | What it looks for | How the script tells | Failure prevented | Price or limit |
   |---|---|---|---|---|
   | 1 | A readable, nonempty handoff file | Resolve against the launch working directory; open a regular file; decode using the runner’s encoding; reject whitespace-only content | Starting an engine with an absent, unreadable, or empty task | One file read; does not prove the engine has the same access |
   | 2 | Required inputs that exist and satisfy known engine access restrictions | Check explicitly declared input files, including persona lists and result templates; resolve paths using launch context; apply configured engine boundaries | Paying for a worker that cannot read a prerequisite | Filesystem reads and engine-specific configuration; host readability alone cannot establish sandbox access |
   | 3 | Missing contract fields and unfinished substitutions | Select the known brief profile; inspect its required sections outside fenced examples; reject empty bodies and exact unresolved template markers | Dispatching a brief with no task, judgment standard, or usable return instructions | Maintaining profiles; populated nonsense still passes |
   | 4 | Explicit contradictions between the brief’s declared contract and the launch configuration | Compare typed declarations with runner values: required capabilities, output channel, permitted write paths, time and attempt allowances | Asking a read-only launch to write a result, or assigning work with no remaining allowance | Requires structured declarations; prose cannot support a reliable general contradiction detector |

   For priority 2, check **required inputs**, not every path-looking string. Output files may not exist yet; examples may contain illustrative paths.

   For priority 3, preserve the difference between returning a final message and writing a result file. This brief itself requires a final message.

3. **Make failures explainable — my #17 and #5.**

   My reading: each failure should identify the file, field or line, failed predicate, and observed value. The check returns failure without changing the brief; the main agent repairs and retries it.

   **Proposed change to the pattern:** where dependencies and launch requirements are currently only prose, have the main agent supply explicit declarations alongside the brief. This enables priorities 2 and 4 without guessing. Its price is additional authoring and the possibility that declarations drift from the prose; introduce only declarations needed by a demonstrated failure.

4. **Deliberately leave these outside pre-flight — my #3, #6 and #13.**

   My reading: do not claim to verify factual truth, task feasibility, sufficient research, complete reasoning, freedom from contradictory prose, or whether a proposed solution serves the vision. These require evidence or judgment.

   If an accepted use-case index exists, a script can check whether a cited ID exists. It cannot establish that the task actually serves that use case.

   Do not impose arbitrary word counts, mandatory examples on every question, universal Markdown style, or guessed context limits. Do not fetch URLs, execute acceptance commands, or start engines during this file check. Those add latency and belong to separate checks when justified.

   The price is deliberate incompleteness: a structurally valid brief can still be a bad brief.

5. **Check the proposed requirements themselves — my #7; this evaluation is my reading using requirement-check.**

   - **Who decides — pass:** the main agent selects the profile and provisionally chooses additions; the script applies declared predicates.
   - **One thing — pass:** each predicate concerns one dispatch condition.
   - **Unit — pass:** paths, fields, seconds, and attempts remain distinct.
   - **Can it fail — pass:** missing files, blank required sections, unresolved markers, and explicit capability mismatches provide counterexamples.
   - **Weak words — FAIL/open:** required dependency syntax and exact profile definitions remain unspecified.
   - **Level — FAIL/open:** which proposed method checks deserve dispatch-blocking status remains undecided.
   - **Basis — FAIL for proven value:** the ranking has no measured savings yet.
   - **Links — pass conditionally:** validate declared IDs against an existing index; do not invent relationships.

## What I need to know

- Which recorded failed calls would these predicates have prevented?
- Which brief profiles and dependency declarations already exist? If none exist, begin with file readability and exact template substitutions.
- What overhead or false rejection would make the main agent remove a check? Leave that acceptance value open until the run supplies a decision.

These are inputs for the main agent’s provisional trials; they need not interrupt EJ before the pattern’s escalation point.

## Costs and risks

- **My #1 and #3:** rejecting a previously successful brief can break EJ’s workflow. Replay successful briefs before making a new predicate blocking.
- **My #5:** keep each predicate independently removable. Configuration and profile maintenance are continuing costs.
- **My #7:** passing establishes only the predicates checked. It does not certify a sound task.
- **My #18, attributed:** include authoring, repair, and false-rejection costs when measuring savings.

## How we would know I was right

My #2 and #18, attributed: test the implementation against recorded successful briefs, recorded failed handoffs, and deliberately damaged copies with specific expected failures.

Name who wrote each fixture and who judged its expected outcome. Synthetic fixtures demonstrate predicate behavior; they do not independently demonstrate usefulness.

Within EJ’s trial budget, record per predicate:

- Check duration in milliseconds.
- Rejections confirmed useful and rejections overturned.
- Authoring and repair time.
- Subsequent engine failures the check missed.
- Engine time and spend demonstrably avoided.

My reading: a predicate earns its place when observed avoided failures outweigh its checking, authoring, and repair costs under the run’s chosen acceptance criterion. A rising rejection count alone proves nothing.