I'll read the brief first.
# 老子 (Laozi) — what a pre-flight check on a brief or question file should verify

## Answer

One script, run after the brief is written and before the engine starts, should verify the **hand-over itself** and nothing else: that every path it names exists and resolves inside the run, that no attempt overwrites an earlier result, that the parts which decide pass/fail are filled with a runnable command instead of the template's `<...>` text, that exactly one result path is named, and that the brief carries the `UNCLEAR:` escape — and it should never judge whether the brief is a good brief or whether the worker's answer is right. Its own list must be **subtracted as it is used**: 損之又損，以至於無為 (`quoted`, my #1) — a check that has caught nothing over two runs is deleted before the next run.

## How I decided

**0. The spine: the list is subtracted, not added.** My #1 is the only item in my list whose kind is *algorithm*: 為學日益，為道日損。損之又損，以至於無為。無為而無不為。 (`quoted`). A pre-flight check that grows by habit ends少則得，多則惑 (`quoted`, my #14). So I ask first what can be left out, and I write the surviving checks in the order of the damage each prevents, not in the order of how easy they are to write. The order below is *my reading* — I have no run yet that shows which failure costs most, and by the pattern's own rule a point from memory alone does not decide, so step 7 is the measurement that may reorder them.

**1. Every path the brief names resolves, and it resolves inside the run.** *Looks for:* each path token in `## Context`, `## Template`, `## Standard`, `## Limits`, `## Write the result to` — the brief template (`docs/workflow-templates/node-brief.md`) puts paths in all five. *How a script tells:* regex the backticked path-like tokens, resolve each against the repo root, `is_file()` or `is_dir()`; the result path's parent directory must already exist; every path must be under the run directory. *Failure prevented:* the whole engine call is spent discovering that the file it was told to read is not there, and returns an answer about nothing. This is the cheapest possible moment to find it — 為之於未有，治之於未亂 (`quoted`, my #6): the thing that is still at rest, 其安易持，其未兆易謀 (`quoted`, my #6). **First in the order because its cost is a whole call and its check is a `stat` per path.**

**2. The attempt in the brief matches the file it would write, and no earlier result is overwritten.** *Looks for:* the `<attempt>` in the H1 title, the attempt in `runs/<id>/nodes/<node>-<attempt>.result.md`, and the attempt allowed by `attempts left:` in `## Limits`; and that the target file does not already hold a different attempt's result. *How:* pull the three numbers, compare; `exists()` on the target with a title mismatch → fail. *Failure prevented:* attempt 2's brief silently writes over attempt 1's result, and the evidence of the first failure is gone, so the loop cannot learn from it. This is my #7 in the harness's own body: 民之從事，常於幾成而敗之。慎終如始，則無敗事 (`quoted`) — people fail when the work is nearly done, and in a run the thing that is nearly done is the last hop of every node.

**3. No part that decides pass/fail still holds the template's placeholder text.** *Looks for:* an unedited `<...>` placeholder, or the literal template wording, in `## Task`, `## Standard`, `## Limits`, `## Write the result to` — `node-brief.md` says outright, "A part that cannot be filled is an unclear spot, not a blank", and ships eight of them. *How:* for each heading, take the body and fail if it matches `<[^>]{4,}>` or is the template's own sentence verbatim. *Failure prevented:* a `## Standard` with the placeholder still in it is a heading with the shape of a standard and none of the use —三十輻共一轂，當其無，有車之用 (`quoted`, my #17): the use of a part is in what fills it, 故有之以為利，無之以為用 (`quoted`). `dispatch.py:38,145-151` already refuses a brief missing `## Template`, `## Example` or `## Standard`, so this item must **not** repeat that; it is about the *bodies*, and about the four parts dispatch.py does not look at.

**4. The command in `## Standard` is one the worker can actually run, and it is the one the harness will run.** *Looks for:* at least one runnable command line in `## Standard`; and, where a node manifest exists, the check name or script path in the brief equal to the one the dispatcher will use. *How:* regex a command line; stat the script/binary token; compare with the plan's check field. *Failure prevented:* the node is judged by a command nobody ran, so pass/fail is undefined, the run's ledger has nothing to check back against, and the COO re-judges the result by hand — which is the rewrite the brief exists to prevent. My #5 gives the reason it must be runnable and not merely described: 我無為而民自化 (`quoted`) — the Standard is what lets the worker act without supervision.

**5. Exactly one result path, and it is named in the template's own field.** *Looks for:* one path in `## Write the result to`. *How:* count matches. *Failure prevented:* two deliverables get two partial results and a hand-off nobody planned. This is method 3.8's "one task per brief", and it is my #1 applied to the brief itself: the second deliverable has not yet been lost.

**6. The stop-on-unclear escape is present.** *Looks for:* the literal `UNCLEAR:` escape that every dev and verifier brief is to carry (`docs/TASK_TYPES.md:219`). *How:* substring. *Failure prevented:* a gap in the brief is filled by a guess, the guess enters the ledger as a fact, and nothing downstream can see it. My #8 is the whole argument for this item: 知不知上，不知知病。夫唯病病，是以不病 (`quoted`) — naming the gap is the cure and pretending not to have one is the sickness; only by treating the sickness as a sickness is one not sick. My list records that the witnesses differ on the second clause (silk A 不知不知 against WB and silk B 不知知), so the brief should ask for the gap *named* and not prescribe which form the words take.

**7. The order and the list are to be measured, not assumed.** *Looks for:* per-check failure counts in the run's state. *How:* one counter per check id. *Failure prevented:* a check nobody ever removes becomes a cost on every call for ever. The algorithm is again my #1 — the check list is subtracted until what is left is enough.

### What it should deliberately not verify

- **That the brief is good.** Whether the Standard is the *right* standard, whether the Context is sufficient, whether the task is well chosen — a script does not know what is enough for a task it has never seen. 禍莫大於不知足 (`quoted`, my #2). Pretending otherwise is不知知 (`quoted`, my #8): the sickness.
- **That the worker's answer is right.** That is the Standard's job, run after the call; `six_experts.py:151-156` already checks the answer's shape and `:365-389` already checks cited items and Chinese against the seat list. My #5: the check does not act; the worker does the work.
- **Length, tone, or prose.** A length check passes a longer brief whether or not it is better; 多則惑 (`quoted`, my #14).
- **The substance of the linked files.** That they exist is the hand-over; what they say is the payload — 故有之以為利，無之以為用 (`quoted`, my #17). Checking content is a check on a different object.
- **Timers and ceilings.** `dispatch.py` and the guard already own them.
- **Anything that writes.** The check fails a file, never fixes it: 為者敗之，執者失之 (`quoted`, my #4) — one who acts on it spoils it.

### Proposed changes to the pattern

- **Proposed change 1 — check the edge, not only the result.** *What it changes:* the pattern gives each *piece* its own check and counts outcomes. This adds the **hand-over** as a piece in its own right, checked before the call and given its own line in the Steps table and progress file. *Why:* with it, a broken brief is seen in under a second instead of after an engine timeout, and the ledger counts hand-overs as well as results.
- **Proposed change 2 — the list of checks is itself subtracted.** *What it changes:* every check carries its catch-count in the run's state, and a check with zero catches across two runs is deleted before the next run; deleting it must not change any verdict. *Why:* it is my #1 applied to the harness's own instruments, and it is the only way the check avoids becoming a ritual.
- **Proposed change 3 — an unclear brief is found by the check, not by a failed trial.** *What it changes:* the pattern sends a question to EJ after three failed trials; a cheap pre-flight check can find the same defect first, at the cost of a `stat` instead of three engine calls. 功遂身退，天之道 (`quoted`, my #3) — once the check has done its part, it withdraws and does not follow the work.

## What I need to know

1. **Where the check lives and who calls it.** If it is a new `preflight_check.py` that only the main agent may remember to run, it will not run; if it is added to `dispatch.py validate`, its three-part check becomes its neighbour and the two must not drift. This changes the recommendation's shape, not its content.
2. **How many briefs one run dispatches.** If a run hands thirty briefs to workers, thirty checks pay for themselves at a different threshold than one question file for six expert seats.
3. **Whether a path the worker is expected to create is exempt.** `node-brief.md` names temp-then-rename for results; if any path is meant to exist only after the worker writes it, a bare existence check fails it for the wrong reason. *If* such paths are common, *then* they need an explicit exemption marker; *if* they are rare, *then* no exemption.
4. **Whether question files get the same script or their own mode.** The question file's requirements are different (it must be non-empty after stripping, and it must carry the facts the answer needs and the shape); my reading is one script with two modes, but I have not seen a question file fail.
5. **What EJ counts as an unclear spot**, so the `UNCLEAR:` check is not a style demand in disguise.
6. **Whether EJ wants the check to hold the whole dispatch or only fail the file.** I have assumed the latter, as the brief for this question states.

## Costs and risks

- **Every check runs on every engine call.** The cost is a `stat` and a regex per path, small against a call — but the list grows by habit, and 禍莫大於不知足 (`quoted`, my #2). Removal rule, step 7.
- **False failures are the real price.** A check that fails a good brief costs a main-agent round-trip and teaches EJ to bypass it, after which the check is worse than nothing — 持而盈之，不如其已 (`quoted`, my #3).
- **Structural checks bend the writer toward the shape.** Once a field must be filled, it gets filled to satisfy the check rather than to do the task; that is the reversal of my #12 (將欲弱之，必固強之 `quoted`) read as an application, and I mark it *my reading*, since the words say nothing about briefs.
- **Duplicating `dispatch.py`.** Its `BRIEF_PARTS` check already exists; adding a second place that must agree is upkeep with no return.
- **A green check read as a green result.** This is the failure I would call most likely, and it is exactly 不知知病 (`quoted`, my #8).
- **The restraint has to be written in, not hoped for.** 以深爲根，以約爲紀 (`quoted`, my #19, `attributed`) — restraint is the rule, not a mood.

## How we would know I was right

- **A sabotage run, and its inverse.** Feed the check three broken briefs — one deleted path, one surviving `<placeholder>`, one attempt mismatch — and confirm those three fail *and nothing else*. Then run it over the last five real briefs unmodified: five passes, or the check has false positives and my order is wrong.
- **Two runs, with and without, counting only what the check predicts.** Before each engine call record: (a) calls that returned nothing usable, (b) calls that named a path that was not there, (c) hand-offs to a re-dispatch, (d) time to first word of the result. My prediction: (b) goes to zero and (a) and (c) fall, at a check cost under a tenth of the shortest engine call. One run proves nothing here — n=1 is recall.
- **The removal test.** Delete every check with zero catches and confirm no verdict changes. If the run is unchanged, those checks were 損 without 益 (`quoted`, my #1) and are gone.
- **The observable that would refute me outright:** a failure mode the check cannot see — a brief that is complete, runnable and correct, and an answer that is still wrong. If that is what actually happens, the check was aimed at the wrong stage.
