# 孫子 (Sun Tzu) — hold the first edit once, or deliver with the result?

## Answer

Hold the first edit (Option B): when a lesson first matches a state-changing call in a session, deny the call with the whole lesson as the reason, let the agent read it and retry, and do not hold that lesson again; keep `additionalContext` for matched read-only calls. The count turns on an asymmetry — if holding is wrong the price is one wasted retry, while if delivering with the result is wrong the price is the first edit the lesson existed to prevent.

**Choice: B — hold the first edit, once per lesson per session; deliver with the result only where nothing can be written.**

## How I decided

1. **My #1 — reckon before committing.** I laid both options against EJ's two aims, the way the seven comparisons are laid out: does it prevent the wrong first edit (A: no, at the earliest its effect is the next step; B: yes, the call does not run); what noise does it add (A: none; B: one blocked call and one retry per lesson per session); what does being wrong cost (A: the wrong edit, plus whatever is built on it before anyone sees it; B: one retry, nothing run, no journal record). More wins and fewer does not: 「多算勝，少算不勝，而況於無算乎？」 (my #1, quoted). The chain 「地生度，度生量，量生數，數生稱，稱生勝。」 (my #1, quoted) is the order I used: the ground is what the hook can actually be relied on to do, then the quantity of prevention each option buys, then the weighing.

2. **My #2 — never rest the plan on the other side's expected behaviour.** Deliver-with-the-result depends on a sentence the docs do not contain: whether `additionalContext` is shown before the tool runs. Hold-once depends on the deny path, which the docs do describe, which the guard already uses for Bash, and which the agent already reads and retries from. 「無恃其不來，恃吾有以待之；無恃其不攻，恃吾有所不可攻也。」 (my #2, quoted). Make the call unable to run before the lesson, then let it run: 「勝兵先勝而後求戰，敗兵先戰而後求勝。」 (my #2, quoted).

3. **My reading, not measured — A's earliest effect is after the call.** "String added to Claude's context alongside the tool result" reads to me as reaching the model with the result of a call it has already committed to for that turn; the brief's own parenthetical says the lesson reaches it "before its next step, maybe after the first edit." So A is learn-after-the-edit, B is learn-before-the-retry. Both deliver a lesson only once per session; the difference is only *where* that single exposure falls. This is the step a fact could overturn: if an owner-permitted probe shows the model can revise the call before it executes, A becomes cheaper and this decision should be re-run.

4. **My #12 — change the condition, not the person.** A asks the agent to read an appended note in time; B makes the edit impossible until the note is read. 「故善戰者，求之於勢，不責於人，故能擇人而任勢。」 (my #12, quoted). A hold is only as good as its reason, so #16 supplies both halves: the discipline that stops the call, 「令之以文，齊之以武，是謂必取。」 (my #16, quoted), and an order that is clear — because 「約束不明，申令不熟，將之罪也；既已明而不如法者，吏士之罪也。」 (my #16, attributed). A truncated or vague reason would put the fault on the guard, not the agent.

5. **My #6 — write the harm column before the benefit.** Harm of B: one round trip; the first match may be a harmless call; the agent may retry the identical call just to get past the block; a long lesson may hit a length cap. These are constraints on the design, not reasons to prefer A: hold only state-changing calls, keep the reason to the lesson itself, and count how often the retry differs. The delivery should have no constant form either (my reading of #10 — 「兵無成勢，無恒形」, quoted): hold writes, attach on reads. 「是故智者之慮，必雜於利害」 (my #6, quoted). B's downside is bounded and known; A's downside is the outcome itself — with both uncertain, take the bounded error.

6. **My #5 — spend the reversible move.** A deny runs nothing and writes no journal record; a wrong edit must be found and undone, and in a three-hour run with no question to EJ it may be built on for several steps first. 「合於利而動，不合於利而止。」 (my #5, quoted): where the lesson cannot change the call, the hold is not called for. #5's irreversibility argument is the reason to gate before rather than repair after — 「亡國不可以復存，死者不可以復生。」 (my #5, quoted), scaled down: the edit that lands is the irreversible step, the deny is not. #3 says the same in cost: 「全國為上，破國次之」 (my #3, quoted) — an edit kept whole is cheaper than one broken and mended.

7. **My #8 — value the win, not the duration.** B costs one turn per lesson per session; the win is fewer repeated code and testing mistakes, which is the aim. #8 warns against prolongation that buys nothing (「兵聞拙速，未睹巧之久也」, my #8, quoted) and gives the standard: 「故兵貴勝，不貴久。」 (my #8, quoted). One gate is not a long war — but if turns rise while mistakes do not fall, the gate has become the prolongation and should go.

8. **My #4 and #17 — when the ground is unknown, choose the option that does not need it.** Knowing the hook mechanism but not whether the string lands before the call is half a victory: 「不知地形之不可以戰，勝之半也」 (my #4, quoted). #17 would have me probe — 「策之而知得失之計」 (my #17, quoted) — but R12.3 leaves hook settings to EJ and EJ is not asked inside the three hours, so there is no probe now. B is safe under either ground; A is safe under only one. That decides it.

## What I need to know

- **Is there a cap on the deny reason, and what is it?** If the whole lesson cannot fit, B as written fails; the fix would be a design change (a pointer plus one guaranteed read), not a shorter lesson.
- **Does the model see `additionalContext` before it commits the call, or only with the result?** One owner-permitted probe answers it; it could overturn steps 3 and 8. The quotes came via a docs agent and are "close but not byte-checked".
- **Can the guard reliably tell a state-changing Bash command from a read-only one?** If not, hold on Write/Edit/MultiEdit only and attach for Bash.
- **If several lessons match one call, does the hold deny once with all of them, or once per lesson?** Once per lesson would put several blocked calls in a row — the noise EJ wants removed, not the mistake.
- **Does a denied edit leave the agent's intended content intact so the retry is the same edit?** If the agent must rebuild it, the round trip is longer than one call.

## Costs and risks

- **A round trip on every first match (my #2).** If the lesson would not have changed that call, the cost buys nothing; bound it to state-changing calls and watch the retry-differs rate.
- **An unclear order is the guard's fault (my #16, attributed).** A truncated or vague deny reason teaches the wrong thing and punishes a rule that was never delivered; the reason must be the lesson, or the hold must not fire.
- **Over-correction (my #15).** 「愛民，可煩也」 (quoted): a guard too eager to teach harries the agent, and every deny spends attention. Once per lesson per session is the cap, and the reason carries no lecture beyond the lesson.
- **Stalling instead of retrying (my reading, not measured).** The agent may read a deny as "blocked, ask EJ" — and in this run EJ is not asked until the time ends. The reason must end with the retry path, as the guard's Bash denials already do.
- **A is not free (my #6).** Delivering with the result spends no turn, but it risks the mistake and then the repair; the bounded error is the one to prefer while the timing fact is unverified.

## How we would know I was right

Compare the same lessons, context-only against hold-once, on EJ's two aims — and set the threshold with EJ rather than inventing one. Measure: repeated code and testing mistakes per 100 edits of the kinds the lessons cover; turns and denied calls per session (the noise price); the share of holds whose retried call differs from the denied one (near zero means the hold is friction, not teaching); and same-lesson recurrence later in the session (once per session may be too thin).

**Wrong if** mistakes do not fall while turns and denials rise; retries are identical in most holds; the same mistake recurs later as often as before; or a probe shows context reaches the model before it commits the call, in which case A would have given the same prevention more cheaply.

**Right if** repeated mistakes fall with turns roughly flat, and the retried call differs in most holds.

**Proposed change to the pattern:** have each hold write one journal line — lesson id, matched path or command word, and whether the retry differed — so the hold's price and effect are visible while the run is happening, as the pattern's timestamped progress lines require, not only in a post-run comparison. The line records the decision to hold, not a tool action, so "nothing ran" still holds.
