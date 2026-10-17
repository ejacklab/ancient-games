# 范蠡 (Fan Li): may a scriptable procedure stay a page, and who decides

## Answer
Yes, but only until the procedure is used again, and only if the page gives each step as an exact command with the result to expect. Being run rarely is not a reason on its own. The next agent who follows that page decides, during that run. It either scripts the procedure or writes in the task's `state.md` why building and keeping a script would cost more work than following the page and fixing whatever had gone stale in it on that run. The project owner decides only if that is contested, as W3.6 already says.

Text to add to W3.6, after "…calls scripts for the rest.":
> A procedure a script could do may stay a page of exact commands, each with its expected result, until an agent follows it again. That agent scripts it on that run, or writes in the task's `state.md` why building and keeping the script costs more work than following the page and fixing what had gone stale in it on that run.

The matching `fails_if` clause would be: *"a page for a procedure a script could do is followed again with neither a script nor that written comparison."*

## How I decided
1. **Two conditions must both hold** (my #1, `quoted`: 「天時不作，弗為人客；人事不起，弗為之始。」 "When Heaven's time has not arisen, do not be the guest [the attacker]; when human affairs have not arisen, do not be the one who begins." Also 「夫人事必將與天地相參，然後乃可以成功。」 "Human affairs must be joined with Heaven and Earth as a three; only then can success be achieved.")
   - *My reading:* W3.6 as it stands tests only one condition: whether each step can be a command with a checkable result. That is the readiness of the work itself.
   - It does not test the other condition: whether the time for that procedure has come, meaning whether it is used again.
   - A script needs both. When one is there and the other is not, my #1 says wait. Here, waiting means the procedure stays a page.
2. **Do not force it, and do not plan early.**
   - My #3, `quoted`: 「時不至，不可彊生；事不究，不可彊成。」 "When the time has not come, growth cannot be forced; when the matter has not run its course, completion cannot be forced." Also 「待其來者而正之」 "wait for what comes and set it right."
   - My #7, `quoted`: 「王若蚤圖之，其事又將未可知也。」 "If you plan for it early, the matter will again be unknowable."
   - The research says the same. Abstracting too early can pick the wrong abstraction (A6, which is about code, so this is an analogy). And "Only by performing these processes repeatedly can we understand what is really needed and what should be automated" (A7, from a secondary summary).
   - *My reading:* "wait for what comes" also removes the need to forecast. The test is not "will it run often?", which is a guess no one has measured (A9 found no measured break-even point). The test is "has it come round again?", which can be observed.
3. **Rarity does not decide either way** (*my reading* of research D).
   - Both forms decay when they are not run. Rarely-run scripts break as things change around them (B10, B11). Rarely-run pages go out of date, and the person following them is out of practice (C16, C18, C19).
   - So "it runs rarely" argues neither for nor against a script. What differs is when the decay is found.
   - The repeat run is the moment a page's decay shows itself, so that is where I put the test.
4. **When the time comes, take it on that run** (my #4, `quoted`: 「得時無怠，時不再來，天予不取，反為之災。」 "Having got the time, do not slacken; the time does not come again; what Heaven gives and you do not take turns into disaster.")
   - *My reading:* the repeat run is the cheapest moment to script. The agent is doing the steps anyway, written instructions are already close to pseudocode (A3), and whatever has gone stale is in front of it.
   - If that run passes without a script, the next run faces a page that has drifted further and an operator who is even less in practice (C16, C18).
5. **The comparison is made on that run.** On one side: the work of turning the page's commands into a script with checks. On the other: the work of following the page by hand plus fixing what had gone stale in it.
   - Both sides are seen during the run, not guessed (*my reading*). This follows the owner's "measure X against Y" rule.
   - Every source that weighs scripting uses this shape: cost against benefit (A1, A5).
   - If the page needed fixing on the run, its cost of keeping is no longer a guess.
6. **A page that waits must be prepared** (my #18, `quoted`: 「審備則可以戰乎？」 "If the preparations are examined, can we then fight?")
   - *My reading:* a page allowed to wait must be exact commands, each with its expected result. Then the agent on the repeat run can check it, and can script it without working the steps out again.
   - This matches A7 (add exact commands), A3 (written instructions are pseudocode) and A8 (the do-nothing script as a middle form).
   - A prose page has no preparations to examine.
7. **Who decides: each part goes to whoever is better at it** (my #14, `quoted`: 「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也。」 "Inside the four borders, the people's affairs: I am not as good as 種. Outside the four borders, dealing with enemy states, matters decided on the spot: 種 is not as good as I.") *My reading* of how that splits here:
   - **The agent doing the repeat run** makes the on-the-spot call, script or keep, because it sees both costs.
   - **The agent who writes the page** decides only "page for now". That needs no comparison, because the time has not come (my #3).
   - **The owner** keeps two things: a contested call, and any value no run can show, such as "this must work the first time it is needed". W3.6 already sends only contested cases to the owner, and the SHOULD level already lets a reason written in `state.md` stand. So the owner is not asked about every page.

## What I need to know
- **Does the project have procedures that must work the first time they are needed** (recovery, rollback, failover)?
  - If yes, "may wait until it comes round again" is wrong for them, because their first real run is the emergency. B10 calls failover "infrequently executed automation", "difficult to test". Such procedures need either a script exercised on a schedule (B15, reported) or a page that is drilled (C16). Which one is the owner's call.
  - If the project has none, the answer stands as given.
- **Does a run record in its `state.md` which procedure page it followed?**
  - If yes, the reviewer can check the added text (W3.6 is `check: reviewer`).
  - If no, only the agent doing the run knows. The added text would then also need to require that log line.

## Costs and risks
- **Waiting** (my #3, #7): between the first run and the next, the page can go stale with nothing to signal it (C16 is verified; the "silent" part is only reported, C17). The repeat run pays that price. For a procedure that is needed rarely and urgently, this may be the whole cost; see the first question above.
- **Taking the time** (my #4): if the agent on the repeat run writes "costs more" too easily, the page lives on and becomes the drifting summary that `procedure-to-skill` warns against: *"summaries drift"*. The only guard is the reviewer reading the written comparison.
- **The preparation** (my #18): a page of exact commands with expected results costs more to write than a prose note. The writing agent pays this up front, possibly for a procedure that never runs again.
- **The two conditions** (my #1): an agent can label a step as "judgement" to avoid scripting it. W3.6's reviewer check already covers this; my addition adds no new guard against it.
- **Who decides** (my #14): different agents may judge similar pages differently. Only contests that reach the owner make the calls consistent.
- **A script still costs upkeep** (research A2, B10, B11): a script that is then rarely run breaks too. My addition does not require scheduled runs of the script. That would be a separate rule, if the owner wants it.

## How we would know I was right
- **Check every repeat run.** For each procedure page, find each later run that followed it (from the `state.md` logs). A page followed again with neither a script nor the written comparison fails the added text. That count should be zero.
- **Measure whether kept pages were the right call.** Take the pages kept with a written comparison and look at their *next* run: did they need a fix, or was a step missed (C20; C21 is reported)?
  - If kept pages need fixes about as often as they did on the repeat run where they were kept, the comparisons were written too easily, and my #4 should weigh more.
  - If they run clean, the comparison held.
- **Measure what scripting too early wasted.** Before and after the change, measure the effort spent on scripts for procedures that never ran a second time. If the change works, that effort falls and pages that were followed again still end up scripted.
- **Plant a stale command.** Give an agent an existing page containing one stale command, and a task that follows it. Pass: the agent scripts it, or writes a comparison that names the fix it made. Fail: it follows the page silently.
