# Dave — final levels for the 22 split source-of-truth ids

## Answer
Use MUST in only two cases. The first is where a tool already stops the commit, so the document cannot say "may override" for something the tool refuses. The second is where a failure loses data silently and for good. Everything else is SHOULD for now, starting with the judged checks that no reviewer covers, and moves up to MUST only after a measured trial. Definitions and how-to text are guidance. Four ids changed from round 1: W6.1, W6.3, K6.1 and K6.3.

| Id | Final level (or clause → level) | Changed from round 1? | Reason (one line) |
|---|---|---|---|
| W1.1 | Split. MUST: "Each entry is one file", the prefix "matches the entry's `kind`", "An entry's kind, and so its prefix, never changes", ids unique, "An id never changes". SHOULD: the `DD-MM-xxxxxx-YYYY` form | No | The tool already fails a prefix that does not match the kind and a duplicate id, and a changed id breaks every link to it. The id form is a method, and the tool does not check it yet. |
| W1.3 | Split. MUST: the `**Why:**` line. SHOULD: `**How to apply:**`, and "There is one claim per entry" | No | The tool fails an active entry with no `**Why:**`, and git cannot restore a lost reason. Two claims in one entry are awkward but lose nothing, because K4.1 keeps the old body and two new entries can supersede it. |
| W2.1 | guidance | No | A definition. Nothing fails. The "written before the code" order sits in K1.1. |
| W2.2 | Split. guidance: the definitions. SHOULD: "a hypothesis is a guess, labelled as one" | No | This is the first SHOULD to promote. Rd5.5 says a wrong outside-world fact is the one error no later check finds. It stays SHOULD because the check is judged and no reviewer exists. |
| W3.3 | SHOULD (depends on how "sensitive data" in W3.2 is read; see below) | No | The safety bound is W3.2's "sensitive data", which is already MUST. Transcripts and private state are a volume and placement default. |
| W3.4 | SHOULD | No | A false "verified" can be put right: Rd5.1 checks against the code before anyone acts, and a new entry corrects it. Judged, with no reviewer. Second in line to promote. |
| W3.5 | SHOULD (the user-memory clause depends on W3.2; see below) | No | A placement method. The privacy part belongs to W3.2. |
| W4.1 | Split. guidance: "Anyone… may create or change any entry… There is no owner and no approval". MUST: "`status` is only `active`, `superseded` or `retired`" | No | A permission cannot fail. The tool fails any other status. The Rd5.3 exception has its own row. |
| W4.2 | SHOULD (both clauses) | No | git keeps who and when, and `git log -p` can restore an edited earlier line, so nothing is lost for good. Whether `changed:` adds anything over git has not been measured. |
| W5.1 | SHOULD | No | Timing is a method. The state of unfinished work is backed up by the per-session journal (K5.1), and K5.2 says a session cut off "loses nothing". |
| W5.3 | Split. SHOULD: adding `done:`. MUST: "it is reported, not settled in `done:`" | No | The second clause is Rd5.3's gate, pointed to from here. |
| W6.1 | Split. MUST: "Each new entry gets its own file. Agents never append to one shared file" (for entries). SHOULD: "each journal… has one file per agent session" | **Yes** (was SHOULD) | My round 1 contradicted itself: W1.1 had "one file per entry" as MUST. An entry appended inside another entry's file never gets its own id in `INDEX.md`, so no session start sees it. That loss is silent. A journal clash shows up as a merge conflict (W6.2). |
| W6.3 | Split. MUST: "keeps both sides: … both links. Nobody chooses between two claims." SHOULD: keeping both `changed:` lines. Pointers: the report sentence → Rd5.3's level; the `INDEX.md` sentence → K6.3's level | **Yes** (was MUST) | A dropped link leaves an entry that readers cannot reach (Rd4.4 reads a superseded entry only by following a link), and nothing shows it. A dropped `changed:` line can be recovered from git, the same as in W4.2. |
| K1.1 | SHOULD | No | It sets an order of work, the kind of method RFC 2119 §6 warns against, and Rd5 catches the mismatch when the entry is read. |
| K4.2 | guidance | No | No "Fails if" mentions age. An entry retired for age keeps its body, and K4.3 allows its status to change again. |
| K6.1 | Split. MUST: `INDEX.md` equals what the tool builds, "one line per active entry". SHOULD: "never edited by hand" | **Yes** (was MUST) | Linus and Sun Tzu moved me: the check tests the result, not the method. A hand edit that matches the build passes the check and harms nothing. |
| K6.3 | Split. MUST: no conflict-marker line committed in an entry or `INDEX.md`. SHOULD: "never merged by hand" / regenerate | **Yes** (was MUST) | Same reason as K6.1 for the method part. A committed `<<<<<<<` line can be read as the claim, and one grep can check for it. |
| Rd2.1 | SHOULD | No | Loading differs by engine and the check is judged. Rd4.1 is a second guard before any file is edited. This is the first thing to test. |
| Rd2.3 | Split. MUST: "credentials". SHOULD: the other five items | No | Credentials are a safety bound. The rest is a context budget. |
| Rd3.1 | MUST for "the K6 check also fails when it does not fit". guidance: the 24 KB / 200-line example | No | The tool's `--check` fails over the limit (I read the code). The numbers are labelled an example, not a measurement. |
| Rd4.2 | guidance | No | How to search. A third way of searching loses nothing. |
| Rd4.5 | SHOULD | No | Attribution inside one session. Nothing is persisted. |

## How I decided
1. **I checked the data first (my #5).** In `tools/memory_index.py`, `--check` fails on errors and on an over-limit `INDEX.md`, while write mode only warns. That matches the COO's facts. Two more things I verified: `.githooks/pre-commit` runs the check, but it is opt-in per clone, and `git config core.hooksPath` is unset in this clone. Its own comment says it is "a convenience, not the guarantee". The test suite also runs the check. `project-memory/` does not exist in this repo, so the n=0 in the brief holds.
2. **One rule for every id (my reading, kept consistent because of my #9).**
   - (a) If a tool already stops the commit, the level is MUST, because calling it SHOULD would mislead. If EJ thinks the rule is only a method, the fix is to make the tool warn instead, not to relabel it.
   - (b) If a failure loses data silently and for good, the level is MUST even when the check is judged.
   - (c) Anything else is SHOULD. Judged checks with no reviewer start here and move up after a trial.
   - (d) Definitions and how-to text are guidance.
3. **Reversibility decides between MUST and SHOULD (my #8).** If a change can be undone, try it small and correct it later. If it cannot, it needs a gate. That is why W4.2, W5.1, K1.1 and W3.4 stay SHOULD (git, the journal or Rd5 can recover or catch them), and the links in W6.3 and the entry file in W6.1 are MUST.
4. **I report my own round-1 contradiction (my #9).** I had W1.1 "one file per entry" as MUST and W6.1 "each new entry gets its own file" as SHOULD. Those are the same rule. W6.1's entry clause is now MUST.
5. **The others moved me on K6.1 and K6.3 (my #4).** Comparing the method against the result: the check compares the built output, so only the result earns MUST. A hand edit is the "current way", and when its output is identical it fails nothing.
6. **I held my position against the irreversibility arguments for W3.3 and W3.5 (Lao Tzu, 范蠡), conditionally (my #1).** The privacy loss they describe is real. But it is the "sensitive data" that W3.2 already makes MUST, and keeping one copy of the bound is cleaner. What would change my mind is listed below.
7. **The judged checks stay SHOULD, in a ranked order to promote (my #2, my #8).** W2.2's hypothesis label first, because of Rd5.5. Then W3.4, then Rd2.1. Each one is a cheap test that settles more than another round of argument.
8. **How sure I am (my #10).** Every level here is my reading at n=0. No workflow has used this memory. The only measured inputs are what the tool checks and how the hook is set up (item 1).
9. **Nature analogies (my #6, my #7).** I found no living-system mechanism whose key condition fits a question about levels, so I did not use one.

## What I need to know
- **How EJ reads "sensitive data" in W3.2.** If it covers a person's preferences and context (user memory can hold such things, for example personal investing context), then W3.3 and W3.5 are covered and stay SHOULD. If it means credentials only, then the user-memory clause of W3.5 and the private-state clause of W3.3 go up to MUST. A leak into a cloned or public repo cannot be removed under K4.1, and git history keeps it anyway.
- **How EJ settles W3.2 against K4.1/K4.3.** If an entry holding sensitive data may be rewritten or deleted, the W3.3/W3.5 slip can be recovered and SHOULD holds more firmly. If it may not, see the point above.
- **How EJ settles K4.3 against W6.3.** My MUST on "both links" assumes a merge may add links. If K4.3's list of what an entry may gain after its first commit excludes `depends_on` and `supersedes`, the MUST narrows to `superseded_by` only.
- **Whether the pre-commit hook will be switched on in every clone that uses this memory.** If not, the "tool stops the commit" MUSTs (W1.1, W1.3, W4.1, K6.1, Rd3.1) are enforced only by the test run, after the commit. They are still MUST, but they are gated later than they read.
- **A stop date for the promotion trial below (my #3).** That is EJ's to set.

## Costs and risks
- **A MUST nobody checks (my #10).** Of my MUSTs, the W6.1 entry clause, W6.3's links and K6.3's markers in entries are judged today. Until a lint or reviewer exists they stop nothing, and the level overstates the guard.
- **SHOULD on silent errors (my #8).** A guess recorded as a fact (W2.2) can sit in memory, unseen, until a trial or a reviewer exists. That is the price of not gating a judged check with no judge.
- **Tying levels to the tool (my #5).** If the tool changes (the `R-` prefix branch, the id-form fix), some levels follow it. Every tool change then needs a check of these rows.
- **Splitting by clause (my #9).** It makes rows longer to read and adds pointer clauses (W5.3, W6.3) that depend on another row's level.

## How we would know I was right
- **A promotion trial (my #2, #3, #4).** Seed a test project with entries that each break one judged SHOULD: a guess recorded as a fact (W2.2), work called "verified" that is only implemented (W3.4), a `changed:` line edited (W4.2). Run a working session on it, and run a control session with the same work and no planted errors. Write the prediction down before running: if I am right, the reader catches the W2.2 plant less often than the W3.4 plant (Rd5.1 helps with W3.4 but not with W2.2). A SHOULD that slips through and causes a wrong action is the one to promote.
- **Rd2.1 per engine.** For each engine (Claude Code, Codex, agy, Qwen, opencode), check whether the four files reach a fresh session before its first action, with no automatic loading as the control. If they arrive automatically everywhere, the judged part of Rd2.1 can be dropped and the SHOULD stays a default. If some engine skips them and then acts against a recorded decision, Rd2.1 moves up.
- **W4.2 against git.** On the first entries written, compare the `changed:` lines with `git log`. If they never add anything git lacks, W4.2 could be dropped. If they do, keep it as SHOULD.
- **K6.3 markers.** A grep for lines starting `<<<<<<<` or `>>>>>>>` over `entries/` and `INDEX.md`, run on every commit, would turn the marker MUST from judged into checked. The fix being designed for the tool is where that belongs.
- **Wrong signs.** A W6.1 or W6.3 MUST that never fires in the first real merges, while a SHOULD caused a lost or misread entry, would mean I put the bar in the wrong place. I would report that with the same weight (my #9).
