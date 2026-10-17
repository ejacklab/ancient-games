# Insight — run 20261017-experts-speed-trial

## F-e548ca60, F-e4eac99c — red runs while writing the tests first; one was 21 red, not the 8 planned

Found by: the guard (R12.2-test-failed). F-e4eac99c is the planned red run: 8 new-behaviour tests red on the old code,
the 29 others green. F-e548ca60 is the run before it: 21 red, mostly existing tests.

Whys:
1. Why 21 red, not 8? `run_seats` passed `card=` and `vote=` into the Namespace, but its signature had no such
   parameters, so every test calling it hit a NameError.
2. Why was the signature missing them? The signature edit and the Namespace edit were sent together. The signature edit
   came back held by a harness-guard lesson ("read it, then send the call again"), but the Namespace edit applied.
3. Why did the run go ahead? I ran pytest in the same batch, before the held edit was sent again.
4. Why was that possible? The lesson hold drops a call without failing the batch, and my instruction for batched edits
   assumes every edit in a batch applies.
Source: instruction — batching dependent edits with a test run assumes none of them can be held.
Root cause: dependent edits and the test run sent in one batch while any edit may come back held by a lesson.
Options:
1. [rule] Send an edit that another edit depends on alone, and run tests only after every edit has come back
   applied. evidence: this run's held signature edit and the 21-red run right after it.
2. [tool] The lesson hold could name the other calls in the same batch that it did not hold, so a split batch is
   visible. evidence: the hook output showed only the lesson text, not that the second edit had gone through.

## F-1ed514ad, F-1c81bc00 — a size limit in a test was a number I made up

Found by: the guard (R12.2-test-failed); the test asserted that a card brief is smaller than a quarter of the list and
identity files, and the brief was 15,435 bytes against a limit of 14,486.

Whys:
1. Why red? The card at first held each rule's whole Rule paragraph, and the brief came out at 26% of the two files.
2. Why was 25% the limit? I chose it while writing the test; neither EJ nor the report gave a size.
3. Why choose one? I wanted a test that "the card is small" and reached for a ratio instead of the card's structure.
4. Why is that the wrong kind of test? CLAUDE.md says never to fill a gap with my own value; the substance is
   "no quotes, no sources, one line per rule", which can be tested without a number.
Source: instruction — I wrote a test threshold that no one gave, against the never-fill-a-gap rule.
Root cause: a test assertion on a ratio I invented instead of on the card's required structure.
Options:
1. [rule] A test asserts what was asked (structure, presence, absence); a size or ratio goes in a test only when the
   owner gave it. Measured sizes go in the report. evidence: the test now asserts no Their words/Source lines and one
   line per rule; sizes are in report.md.
2. [check] The criteria file names each number the tests rest on and who gave it. evidence: criteria.yaml C1 had no
   number, and the test added one.

## great: runs/20261017-experts-speed-trial/compare-numbers.txt

Comparison: round 3 rerun with --card --vote against the 2026-10-13 run, same four experts and the same question:
slowest engine 94.0 s → 48.1 s, sum of engine seconds 324.0 → 162.3, Codex tokens 45,671 → 12,202, answers
2.4–8.6 KB → 0.5–2.3 KB, all four APPROVE both times. n=1 per engine, on a different day, with the lessons section
and the "How we work" section in the brief that the old run did not have.
Cause: the experts read a 10–12 KB brief instead of a ~2 KB brief plus 55–78 KB of list and identity files, and
wrote three short sections instead of five long ones (my reading: both of fixes 1 and 2 count; the run does not
separate them).
Options:
1. [rule] Use --card --vote for approve-or-change questions. evidence: compare-numbers.txt.
2. [check] Run one rerun with --card alone and one with --vote alone to separate the two effects before making
   either a default. evidence: this run applied both at once.
