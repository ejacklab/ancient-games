# 范蠡 (Fan Li): deliver a lesson with the edit's result, or hold the first edit?

## Answer
Choose **B, hold once**, on two conditions. First, the guard records "this lesson was shown in this session" before it returns the deny. Second, the deny reason says the call is not forbidden: send it again, changed if the lesson applies. If the owner's live trial at the end shows that PreToolUse `additionalContext` reaches the agent *before* the tool runs, switch to A. A would then deliver the lesson at the same moment without the retry.

## How I decided
1. **The lesson matters only before the first edit.** My #4: 「得時無怠，時不再來，天予不取，反為之災。」 (`quoted`). A lesson's moment is the edit it is about. Under A the lesson may arrive "alongside the tool result" (hooks.md). The docs do not say whether it is shown before the tool runs ("not found in docs"). If it comes after, the first edit already holds the mistake the lesson exists to prevent. That moment does not come again, and the agent needs a second edit to undo it. This goes against the owner's aim of fewer repeated mistakes.
2. **Choose the channel whose readiness has been checked.** My #18: 「審備則可以戰乎？」 (`quoted`). The deny path has been checked. The guard already denies Bash calls before they run, with a reason the agent reads and then retries (`guard/src/hooks.ts:106-128`, Round 13). A's timing has not been checked, and it cannot be checked in this run: the hook settings are the owner's to change (R12.3).
3. **Keep the aim; the mechanism may change.** My #5: 「天節固然，唯謀不遷。」 (`quoted`). The plan's own delivery test says "check the lesson's text arrives before the call" (plan file §5). The plan also foresaw this case: "If it cannot, section 3's first bullet changes" (§6 piece 1). B keeps the aim and changes only the mechanism, as the plan allowed. A keeps the mechanism but risks the aim.
4. **Use force as little as possible.** My #13: 「兵者，凶器也；爭者，事之末也。」 and my #11: 「用力甚少」 (both `quoted`). A deny is the guard's strongest tool. So each lesson holds a call once, and only for a lesson that matched. It never holds a second time, and never holds for a lesson already shown.
5. **Stop when the count runs out.** My #10: 「無過天極，究數而止。」 (`quoted`). After a lesson has been shown once, later matches of it add nothing. This is also the guard against noise.
6. **Holding on a match alone is weak evidence.** My #9: 「天地未形，而先為之征，其事是以不成」 (`quoted`). A path match is a sign that the mistake may come, not the mistake itself. My #12: 「又觀其民之饑飽勞逸以參之」 (`quoted`): check a second way before acting. So the hold should fire only on the plan's full match: `agents` and `kinds`, plus `paths` where given (plan §3). For Bash the match is by command word, which is coarser. My reading: a hold that turns out to be needless costs one retry per lesson per session, while a lesson that arrives late costs a mistake in a file or a command that already ran. That is why I keep B for Bash too, and treat false holds as noise to measure.
7. **Wait at the call, not before it.** My #3: 「待其來者而正之」 (`quoted`). This supports delivering at the matching call (both A and B), not at session start. It does not choose between A and B; steps 1–3 do that.
8. *Proposed change to the pattern* (my reading): when a fact a decision rests on is "not found in docs" and cannot be tested in the run, the provisional choice goes to the option that does not depend on that fact. The untested fact goes into the end-of-run report as a named trial only the owner can run. This would add a "trials for the owner" list to the end-of-run report, so the owner's accept or decline comes with the test that would settle it.

## What I need to know
- **Can "once per session" be keyed reliably?** I recall (*recall*, not verified) that the hook payload carries a `session_id`. If it does not, or if it changes between the deny and the retry, B loops. Then B must not ship until that is solved.
- **Where may the guard store the "shown" marks?** A deny writes no journal record ("nothing ran", `hooks.ts:106-128`), so the marks need their own store, written before the deny returns.
- **Do PreToolUse hooks fire for subagents, under the same session?** (*recall*.) If they do, subagents get held too, which the plan's "main agent" scope (§3) did not intend. In that case, limit the hold to the main agent if the payload allows it.
- **Is there a cap on `permissionDecisionReason`?** Not given. Only `additionalContext`'s 10,000-character cap is known (hooks-guide). This matters only when several lessons match one call.

## Costs and risks
- **One extra turn per lesson per session.** A held `Write` re-sends the whole file, which costs tokens; an `Edit` retry is cheap. (#4: this is the price of arriving on time.)
- **Loop risk.** If the shown-mark is not written before the deny returns, every retry is held again and the agent is stuck. (#10)
- **Read as a ban.** An agent may abandon the edit or route around it, for example by writing through Bash. The reason must say "not forbidden; send it again". (#13)
- **False holds on Bash.** Command-word matching is coarse and will hold calls the lesson does not fit. (#9, #12)
- **It changes what the owner approves.** Plan §6 piece 4 says "(no deny, context only)", and piece 5 asks the owner's word to add `Write|Edit|MultiEdit` to the matcher. Under B that hook can hold writes, and the owner should approve piece 5 knowing that. (#5)
- **If A were chosen instead:** the first edit may carry the mistake, and the plan's §5 test ("arrives before the call") could not be shown to pass. (#4, #18)

## How we would know I was right
- **Now, offline** (no live test needed): tests on `handlePreToolUse` with `Write` and `Edit` payloads, each shown failing on the old code first. (a) The first matching call in a session gets a deny whose reason holds the lesson text. (b) The same lesson on a second call in the same session gets no deny. (c) A control path gets no lesson. (d) The shown-mark exists on disk after the deny.
- **At the owner's live trial** (R12.3): the plan's planted-repeat test (§5). For three filed lessons, replay the call that failed; for each I would check:
  - the lesson's text reached the agent before the tool ran;
  - the retried call was changed where the lesson applies;
  - the control got nothing.
- **Signs B was the wrong choice:**
  - The same trial shows `additionalContext` is shown before the tool runs. A would then meet §5 without the retry, so B's price was paid for nothing; switch to A.
  - Agents abandon or route around edits after a lesson hold. Compare edits completed after a hold against edits begun.
  - A lesson is held more than once in a session.
  - Most holds were for lessons that did not apply to the edit. Compare holds against lessons that applied, as in plan §3's noise check. If so, tighten the match before giving up on the hold.

**Choice:** B, hold once per lesson per session, with the shown-mark written first and a "not forbidden, send it again" reason; switch to A if the owner's live trial shows `additionalContext` arrives before the tool runs.
