I'll read the brief first.
# 老子 (Laozi) — deliver the lesson with the edit's result, or hold the first edit?

## Answer

Hold once (Option B): deny the first call in a session that a lesson matches, with the lesson as the reason, and let the agent retry — and if the docs later confirm that `additionalContext` is added *before* the tool runs, take Option A instead, because it then buys the same effect with no retry.

## How I decided

1. **Start from the use case, then the cheapest stage.** The use case is an agent repeating a code or testing mistake. Option A serves it only if the lesson lands before the act that repeats the mistake. My #6: "act on a thing before it exists and put it in order before it is in disorder" — 為之於未有，治之於未亂。 Option A is 亂後 (the disorder is already in the file); option B is 未亂.

2. **My #8 — 不知知病 — decides this more than anything else.** "To know that you do not know is best… not-knowing knowing is a sickness" — 知不知上，不知知病。夫唯病病，是以不病。 The one premise that separates A from B is exactly where A is weak: the hooks reference says `additionalContext` is "String added to Claude's context alongside the tool result", and whether it arrives before the tool runs is "not found in docs". The fact is the reverse for B: the guard already denies Bash calls before they run with `permissionDecision: "deny"` and a reason the agent reads, then retries (Round 13's read-missing hold), and a deny writes no journal record ("nothing ran"). So B rests on something the run exercised; A rests on something the docs do not settle. Treat the unknown as unknown: build so the answer does not change whichever way it resolves — which is why the answer is conditional rather than a guess.

3. **My #11 — the disease is that knowing does not change the doing.** 弱之勝強，柔之勝剛，天下莫不知莫能行 — "everyone knows and none can practise." A adds the lesson to a context that already holds the agent's intention to write; the intent is the part that has not moved. The point of intervention is where the act is still undecided.

4. **My #2 and #3 set where the hold stops.** "No calamity is greater than not knowing what is enough" — 禍莫大於不知足 — and 知足不辱，知止不殆，可以長久。 Plus my #3: 持而盈之，不如其已；功遂身退，天之道。 A hold on every match is 持而盈之. So B's own clause — later matches of that lesson add nothing — is what keeps it inside 知足: one hold, then功成而弗居。夫唯弗居，是以不去。 My #2 does not say *how much* is enough (the list's Gaps say 知止 is unresolved: "stop where?"), so "once" is a decision I am making, not a number I derived.

5. **My #10, #19 and #5 fix who acts, and what the guard is for.** 不敢為天下先，故能成器長 — the guard does not stand in front; 善有果而已，不敢以取強 — the result, not compliance, is the point; my #19 (attributed): 以深爲根，以約爲紀 … 人皆求福，己獨曲全，曰：「苟免於咎。」 — restraint as the rule, and the aim is only to escape the fault. Under B the agent reads the lesson and writes the retry itself; my #5: 我無為而民自化 — the blockage is removed and the agent does the work.

6. **My #17 says why the empty space is the point, not a gap.** 故有之以為利，無之以為用。 The lesson is not the thing that works; the space it opens for the agent's own judgement is. A deny that hands the decision back and then gets out of the way has that shape; a deny that also judges is 執者失之 (my #4) and 國之利器不可以示人.

7. **My #1 caps how much is built, and settles the cap worry.** 損之又損，以至於無為 — build the smallest thing that works: no severity ranking, no lesson scoring, no second hold, no new journal type. 多則惑 (my #14) is the reason not to add them. On the 10,000-character cap: that figure is documented for `additionalContext`, and no cap is given for the deny reason — the deny path already carries a reason in this run, so B does not touch the number at all. 一件事不夠取天下: 取天下常以無事，及其有不��，不足以取天下 — once there is business, it stops working; the hook settings are the owner's (R12.3), so nothing can be tested live here and the recommendation must survive being untested.

8. **Re-read while deciding.** My #7 (民之從事，常於幾成而敗之。慎終如始) is the one that cuts both ways and I will not use it to decide: the failing moment is "close to finishing", and whether the first edit is that moment is not something I was given. My #12 (將欲歙之，必固張之) I do not use, because the list says the words do not say who stretches or what follows. My #16 (自知者明, 自勝者強) I use only in the test below: measure the run's own behaviour, not the doc's promise.

9. **Proposed change to the pattern.** *When a mechanism cannot be tested live in a time-boxed run (R12.3), decide by which premise the run has already exercised, and write that premise into the state entry.* This changes the pattern's "research and data, not recall" from a rule about research into a rule about *unprovable-in-session* decisions: EJ's accept/decline at the end then decides a named premise rather than a taste. The line for this decision reads, in my words: B rests on the Bash deny path observed in Round 13; A rests on `additionalContext` timing, undocumented.

## What I need to know

1. **Has `permissionDecision: "deny"` ever fired on Write/Edit/MultiEdit in the guard?** The fact names Bash. If it has not, B is untested on exactly the tools it targets, and the conditional is: if a deny on Write has not run, use B and treat the first session's holds as the test, or (if EJ wants a proven path first) hold only on a matching Bash call.
2. **Does the once-per-session set get written before the deny, or after?** If it is written only on a delivered context, the retry re-matches the same lesson and is denied again — a loop. This is the one thing that can make B worse than A.
3. **How many lessons typically match in one session?** If nearly every lesson matches on the first edit, "once" is not a limit and B's friction is per-session large.
4. **Is one extra blocked call per lesson per session acceptable inside "less noise"?** Or does EJ's noise aim count friction as loudly as context?
5. **Whether the agent's retries after a Bash deny completed the work.** Round 13 establishes the retry happened, not that the session finished cleanly after it.

## Costs and risks

- **B can teach routing, not the lesson.** The agent changes the path, the file name or the command word until nothing matches. This is the largest risk of B, and it is measurable (my #14: 物或惡之，故有道者不處 — "things may loathe them, so one who has the Way does not dwell in them").
- **B costs latency on false positives.** A hold on an edit the lesson does not concern forces a re-issue of a call the agent was going to make anyway. Mitigation without new machinery: keep the reason to the matched lesson and the path, one line, so the retry is immediate.
- **B is friction on every session that matches, even when the agent already knew** (my #11's own words: everyone knows, no one can practise).
- **A's cost is that it cannot be measured.** Its arrival point is undocumented, so the guard cannot report whether a lesson came before or after the act; and matches inject into context against a 10,000-character cap, with no count of matches given. If it lands after the act it can only subtract from later work (my #1) — it prevents the *second* repeat, not the first.
- **Both options cost one thing I will not build around:** a lesson's usefulness is judged by the agent's next act, not by delivery, so neither option buys anything that an unread reason cannot also buy (my #13: 善有果而已).
- **Nothing is tested live here** (R12.3), so whichever is chosen ships unverified; my #18 (attributed) fits the situation: 且君子得其時則駕，不得其時則蓬累而行 — when the time is not right, go, do not force. And the choice is provisional for that reason, not provisional on my confidence.

## How we would know I was right

- **The effect test.** Count, per session, (a) holds at a first match, (b) retries where the written act differs from the held act. (b) is the lesson working; (a) with no (b) is pure friction and A — or C — wins.
- **The loop test.** Any session where the same lesson id denies the same call twice is a falsifier for B as specified: the once-per-session marking does not precede the deny. Target: zero.
- **The routing test.** Count sessions where, after a hold, the agent changed the path or command word rather than the act. Any rise over sessions means B is producing avoidance; my #9: 以其不爭，故天下莫能與之爭 — a guard that contends with the agent is not holding a line, it is starting one.
- **The error-rate test that tests the real aim.** Count repeats of the same code or testing mistake within a session. B predicts a fall against A's baseline; no fall means the delivery timing, not the mechanism, was doing the work — and my #16's 自勝者強 is to measure this run's own acts.
- **The falsifier for my own premise.** If the hooks reference is later confirmed to add `additionalContext` before the tool runs, A delivers the same ordering with no retry and no friction, and my choice was wrong on a named, checkable premise rather than on judgement.

**Choice: Option B — hold the first match once per lesson per session with the lesson as the deny reason; switch to Option A if the docs confirm `additionalContext` arrives before the tool runs.**
