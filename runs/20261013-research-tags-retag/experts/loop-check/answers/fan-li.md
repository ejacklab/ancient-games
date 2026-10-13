# 范蠡 (Fan Li) — Bounding loop attempts and prompt closure

## Answer
Both loops are bounded at two attempts before exiting to EJ and close promptly on the first passing check, but R5 requires a tighter schema check to prevent premature closure on malformed data.
- **R4:** loop-ready as written — attempts are bounded at 2 before exit to EJ and it closes immediately upon script pass; concrete failure missed: a degenerate run tagging all 143 rows with the identical label (e.g., all `unproven`).
- **R5:** strengthen the check (enforce mutual exclusivity among `tag`/`split`/`stuck`, require valid tags inside split parts, and require exactly two tags and a non-empty `why` string for stuck) — concrete failure missed: a line with untagged split parts or `{"why": ""}` passing schema and falsely closing the loop.

## How I decided

1. **Attempt bounds must stop when the count is exhausted. My #10 and my #3.**  
   Those of old who moved troops well 「無過天極，究數而止」 (`quoted` — "did not pass Heaven's limit, and stopped when the count was exhausted"). A loop must not drift into indefinite iteration. An attempt limit of 2 fixes the count (究數而止). Furthermore, 「時不至，不可彊生；事不究，不可彊成」 (`quoted` — "when the time has not come, growth cannot be forced; when the matter has not run its course, completion cannot be forced"). If the low-effort flash model cannot deliver a schema-valid classification in two tries, forcing further attempts under unchanged conditions cannot force completion.

2. **The exit to EJ preserves the council plan. My #5 and my #14.**  
   A plan made at court should not be lost in execution: 「夫謀之廊廟，失之中原，其可乎？…贏縮轉化，後將悔之。天節固然，唯謀不遷」 (`quoted` — "to plan it in the temple hall and lose it on the central plain — can that be right? … Advance and retreat change into each other; later you would regret it. Heaven's rhythm is like that; only the plan does not move"). The plan requires both passes to run under identical conditions for fair comparison. Escalating one pass to a higher tier on failure would break parity and discard the court's design. Exiting to EJ respects who decides what: 「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也」 (`quoted` — "inside the four borders, the people's affairs: I am not as good as 種. Outside the four borders, dealing with enemy states, matters decided on the spot: 種 is not as good as I"). Autonomous loop execution handles mechanical classification; changing tiers or revising definitions belongs to EJ.

3. **Closure must be prompt the moment the check passes. My #4 and my #6.**  
   When the condition is met, close without delay: 「臣聞從時者，猶救火、追亡人也，蹶而趨之，唯恐弗及」 (`quoted` — "one who follows the time is like one fighting a fire or chasing a runaway — run and hurry, fearing only not to get there") and 「得時無怠，時不再來，天予不取，反為之災」 (`quoted` — "having got the time, do not slacken; the time does not come again; what Heaven gives and you do not take turns into disaster"). The moment the verification script returns exit code 0, the loop must terminate immediately. No lingering, no secondary guessing, and no manual prompting: 「今事已濟矣」 (`quoted` — "now the task is done") — the step concludes and hands off to R6.

4. **R4 preparations are examined. My #18 and my reading.**  
   Asked if examining preparations permits action, the answer was 「審備則可以戰乎？」王曰：「巧」 (`quoted` — "'if the preparations are examined, can we then fight?' The king: 'Skilful'"). For R4, the deliverable is simple (`{"id", "tag"}`), checked for 143 unique IDs against the four old tags. The bound (2 attempts) and exit (to EJ) are real. **My reading:** the script would miss a degenerate collapse where the engine outputs 143 syntactically valid rows assigning every row the same label. That is an engine failure rather than a loop-boundary defect, so R4 is loop-ready as written.

5. **R5 preparations require tighter defense against false closure. My #18 and my #4.**  
   R5 introduces compound structures (`split` and `stuck`). If the check only verifies key presence, a malformed output (such as `{"id": "R001", "stuck": ["verified", "reported"], "why": ""}` or split parts lacking valid tag assignments) would pass the check. Closing promptly on a flawed pass violates my #4: 「得時不成，天有還形」 (`quoted` — "if you get the time and do not complete it, Heaven has a way of turning it back"). The check must verify that keys are mutually exclusive, that each split part contains a valid tag from the four, and that `why` is a non-empty string.

## What I need to know

- Does `dsh headless` enforce a strict wall-clock timeout per attempt so an unresponsive call aborts and counts against the attempt limit rather than hanging? (If not, attempts are bounded in count but unbounded in time.)
- Does the R5 schema check script already validate that `split` parts contain valid tags from the four and that `why` is non-empty, or does it only test top-level keys? (If it already validates nested fields, R5 is loop-ready as written.)

## Costs and risks

- **My #10:** Bounding attempts strictly at 2 risks aborting to EJ on trivial syntax slips that a third attempt might fix, trading automated completion for strict bounding.
- **My #4:** Closing promptly as soon as the script passes risks accepting semantic misclassifications if the verification script tests only structural shape.
- **My #5:** Refusing automated tier escalation halts the workflow if both attempts fail, costing EJ's time to triage.
- **My #18:** Strengthening R5's schema check requires additional fixture validation and script preparation before the run can launch.

## How we would know I was right

- If an attempt fails twice on schema errors, the loop terminates after exactly two attempts without hanging and exits to EJ.
- If an attempt succeeds on attempt 1, the loop terminates immediately and proceeds to R6 without delay or second attempts.
- A test fixture containing a `stuck` row with an empty reason (`"why": ""`) or a `split` row with an invalid part tag fails the strengthened R5 check before the run begins.
