# 孫子 (Sun Tzu) — how often the guard reports the time

## Answer
Take **(B)**: a one-line used/left figure after every tool call, plus the fuller block with the workers' progress at 50%, 80% and 100% and on every call once time is up. Make the line carry the *number*, not a nudge; hold (B) to the measured hook cost (C6), and fall back to (A) only if that measurement shows the line costs more than it returns.

## How I decided

1. **Reckon before I choose (my #1).** Both use cases go on the scale first — the agent knows how much of the limit is used, and it sees the workers' progress per small piece (C2, C3) — and then each option is weighed by what is measured. B is the only option with measured support: F2 (per-step tracker: 40.4% fewer search calls, 31.3% lower cost) and F6 (per-turn update: 32% vs 4% closure). A is "not addressed" by any source that compares it (research digest); C rests on a number nobody has measured. 「多算勝，少算不勝，而況於無算乎？」 — choosing C is 無算.
2. **Do not rest on the agent; rest on what you own (my #2).** 「無恃其不來，恃吾有以待之」 — F5 (prompt-stated budget 40% vs 100% with forcing) and F8 (prompt-only budget fails) are the same lesson: a budget stated once is resting on the agent to notice. The guard, run after every tool call, is the part we own.
3. **Seek it in the ground, not in the people (my #12).** 「求之於勢，不責於人」 — F6's own line is "LLMs struggle to internally track elapsed time". A design that makes the agent feel time is demanding it of the person; the running clock must live in the harness.
4. **Foreknowledge comes from people and must be paid for (my #11).** The workers' timestamped progress lines are the people "who know the situation"; the ~20-token line is the rank and salary I must not begrudge. F6 prices the refusal to pay: 4% against 32%.
5. **Move on advantage, act on gain (my #5).** 「非利不動，非得不用，非危不戰」 — C acts on a number nobody measured; A's gain is untested and arrives too late to act on; B's gain is the one measured. F1, F3 and F4 all chose per-step/per-call as well.
6. **Mix harm into benefit (my #6).** Benefit column: F2's 40.4% fewer calls and 31.3% lower cost, F6's 4%→32%. Harm column: ~20 tokens on every call, and F4's measured failure when a budget is made too tight — "decline to attempt the task at all, scope it down aggressively, or stop early". 「雜於利而務可信也，雜於害而患可解也」 — mixed with harm, the trouble is resolved by capping the line and measuring it (C6).
7. **Rank by 謀攻 (my #3).** Continuous shaping of conduct is 伐謀; informing only at the marks and then at the end is 攻城 — 「攻城之法，為不得已」. So B is the choice and A is the last resort, not C: C is neither measured nor a fallback the text ranks.
8. **Value victory, not duration (my #8).** 「兵聞拙速，未睹巧之久也」 — a fixed N is the skilled prolongation that has never been seen; the deadline does not move. F2's tracker is this design's food from the enemy: it returned about a third of the cost it was paid to watch.
9. **Clear orders first (my #16).** 「約束不明…將之罪也」 — B's rule is uniform and stated in one line (figure every call, block at the marks); C's N is set by nothing measured, which is unclear orders and breeds 亂.
10. **Bring it to the agent (my #9) and make it a number (my reading of F6/F7).** 「致人而不致於人」 — the guard pushes, the agent never asks (C2). F6's winner was a remaining-time figure; F7 records that the study's only other condition was a qualitative urgency note. So the line must show used/left, not "time is passing".

## What I need to know

- **The measured hook cost (C6):** the line's tokens per call against the calls or cost it prevents. If it is large relative to the run's context, my answer flips to (A). I answer conditionally on this measurement, because F2's and F6's savings are other models' measurements, not this run's.
- **Which model the run uses:** F2 is Gemini-2.5-Pro and F6 is GPT-5.1. If the run's model is neither, per-step support is analogy, and C6's measurement — not the studies — becomes the deciding evidence.
- **Whether the guard really can be forced after every call**, including after the deadline (C2). If it cannot, B silently degenerates to A; then choose A openly rather than claim B.

## Costs and risks

- (B) pays ~20 tokens on every tool call whether or not the agent is off pace — a fixed price for a variable benefit (my #1: the reckoning is only as good as its numbers; the harm column of my #6).
- A routine line can be ignored; the research's tested winner was the *figure*, and F7's alternative was only a qualitative note — a vague line is the failure mode of B (my reading of F6/F7).
- F4's warning — too tight a budget and the model declines or stops early — is the risk that the reminder itself becomes the thing that ends the work (my #6, harm).
- (A) as fallback is untested: the research says marks-only is "not addressed", so if we fall back it must be measured, and (A) is 不得已 (my #3).
- The deadline is irreversible: 「亡國不可以復存，死者不可以復生」 (my #5). An overrun cannot be undone, which is exactly why the warning must arrive on every call rather than at the end.

## How we would know I was right

- The run finishes and the report is written before the owner's deadline (C7), the guard's line appears after every tool call with the marks at 50/80/100% (C2), and the agent never has to ask for the time.
- C6's before/after measurement of the hook shows the per-call line paid for itself, measured as F2 measured it (fewer calls, lower cost). If the line's cost exceeds its return, that measurement falsifies (B) and makes the untested (A) the measured fallback.
- Observable result: no mid-run request for time and no overrun. A single run that overruns while the line was present falsifies the claim that per-call awareness is enough.
