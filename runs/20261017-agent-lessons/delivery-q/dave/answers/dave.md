# Dave — deliver a lesson with the result, or hold the first edit?

## Answer
Option B, hold once, with two additions. The deny reason should say the call was not judged wrong and can be retried unchanged if the lesson does not apply. The guard should also write a delivery record that keeps both the denied input and the retried input, because a deny writes nothing to the journal today. The choice stays provisional until a small three-arm test (no lesson, A, B) has run, if the rules allow that test (see below).

## How I decided
1. **What would change my mind, named first (my #1).** I would switch to A if either of these is seen. First, the agent's first edit follows a lesson as often under A as under B. Second, under B most retries are identical to the denied call, or they change a correct call into a wrong one. Then the hold costs a retry and buys nothing.
2. **The data we already have (my #5).**
   - The hook reads `tool_input` from the payload (`guard/src/hooks.ts:107`). So the edit is already written when PreToolUse fires. Under A, the content of the first edit is fixed no matter when `additionalContext` is shown. The gap in the docs about timing does not change this. *My reading, resting on that code fact.* A can only affect the next step, never the first edit.
   - Deny and retry has been measured once. In `runs/20261015-long-session/results.md:26-27`, arm C (hooks only) held 3/3. Each run hit one deny, learned from the hooks' messages, and ran about 25% slower than rules-only (median 102 s against 83 s). That was n=3, one task, one model (haiku), and the slowdown also includes Stop blocks, not just denies.
   - Not measured: whether an agent acts on `additionalContext` after a call, and whether a lesson delivered after the first edit leads to a fix-up edit.
   - Not measured either: a deny on Write or Edit. Today `handlePreToolUse` returns quiet for anything but Bash (`hooks.ts:106`). Our only deny data is for Bash.
3. **How nature solves it (my #6).** An ant senses the trail at the fork, before it picks a branch. The information is at the place and in time for the choice.
4. **Does the analogy fit (my #7)?** What is the same: the information has to be there when the choice is made, and here the choice is made when the model writes the tool input. What differs: sensing a trail costs the ant nothing, while B's fork costs a denied call. The key condition holds for B and fails for A on the first call, so I keep the analogy.
5. **Insight `runs/20261016-four-experts-what-counts-as-change/insight.md#F-cc665076`.** The read-missing hold denied a command that was correct. A lesson hold goes further: by design it denies every first matching call, whether right or wrong. This changed my answer from plain B to B with a reason that says the call was not judged wrong. It also means a correct call that the agent changed after a hold must be counted as a cost.
6. **Report what failed (my #9).** The facts say a deny writes no journal record. If B leaves no trace, nobody can see a lesson that changed nothing, so its failure goes unreported. The plan's "once per session" rule already has to store which lessons each session got. *My reading:* that store can be the record (session, lesson id, tool, path, time, denied input, retried input).
7. **A small experiment beats a long argument (my #2, #3, #4, #8).**
   - The test costs less than this debate. `runs/20261015-long-session/design.md:17,20` already ran headless `claude -p --setting-sources project` with hooks loaded through `--settings` from the run folder.
   - The arms: no lesson (the control, my #4), A, and B. Use one lesson whose effect shows in the first edit, and one path only (my #8).
   - The prediction, written before any result (my #3): A's first edit follows the lesson no more often than the control's. B's retried edit follows it more often than either. B costs one extra call per lesson. Stop at n=3 per arm or at the end of the time box, whichever comes first.
   - Long-session runs took a median of 82–102 s each, so nine runs fit well inside 3 hours. *My reading.*
8. **Bash.** The logic is the same. One further point is *recall* only (the memory note `engine-calls-need-dev-null`): a bare `codex exec` hangs until timeout. Under A, that lesson would arrive after the hang. It is recall, so it does not decide alone.
9. **How sure I am (my #10).** For lessons themselves this is n=0. Deny and retry has n=3 on Bash only. This is a hint that points to B, not a law.

*Proposed change to the pattern:* when a decision can be settled by a headless test inside the time box, run the test before asking the experts. That changes the order "experts, then decide" into "test if cheap, then experts on what the test did not settle". (my #2)

## What I need to know
- Does R12.3 cover a temporary `--settings` file in the run folder used only for a headless test, the way long-session did? R12.3 needs the owner's yes before a fix is applied to a harness's config. *My reading:* a temporary test file is not the owner's config. If the test is allowed, run it before B is final. If not, B stays provisional and untested, and the live delivery records become the test.
- What are the lessons mostly about? If they are about the content of the call (how to write a test, where to put a plant), B is right. If they are mostly about what to do after the result (how to read the output), A is enough.
- How large are the first calls that lessons will match? A hold throws away the whole denied input. If most matches are large new-file Writes, B's price grows, and delivering the lesson at the agent's Read of the file becomes worth a test. That would mean registering Read too, which changes the plan.

## Costs and risks
- **B costs one denied call per lesson per session**, plus the output spent writing the denied input (my #8: measure it on one path before spreading).
- **B can make an agent "fix" a call that was right**, because a deny reads like an error (insight F-cc665076; count these under my #9). The plain reason is meant to reduce this, but that is *not measured*.
- **Deny on Write or Edit has never been run in this project** (`hooks.ts:106` handles Bash only), so B's behaviour there is unmeasured (my #10).
- **B's effect cannot be seen without the delivery record**, since a deny writes no journal record (my #9). The record is extra code and storage.
- **The risk of A** is that the first edit can never benefit (my #5, the code fact). Any fix is a second edit that may not happen, and that is *not measured*.
- **The test** costs about nine headless runs of the time box (my #2), and it may be ruled out by R12.3.

## How we would know I was right
- **In the test (my #3, #4):** B's retried first edit follows the planted lesson more often than both A's first edit and the control's. Under A, the first edit should look no better than the control.
- **In live use, from the delivery records:** for each lesson, compare the denied input with the retried input. B is right if the retries change in the lesson's direction. B is wrong if most retries are identical to the denied call (the lesson changed nothing, so the hold was only friction and A is enough), or if retries turn correct calls into wrong ones.

**Choice:** B, hold once, with a reason saying the call was not judged wrong and a record of the denied and retried inputs; provisional until A, B and a no-lesson control are compared.
