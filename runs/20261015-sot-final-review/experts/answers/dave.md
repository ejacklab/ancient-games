# Dave: review of the finished source-of-truth memory design

## Answer
An agent will follow most of it. It will stumble in four places: the prose says "never" where the YAML says SHOULD, `levels.MUST` says "the work it governs stops" with no unit named, retiring an entry can't be done without a replacement link (and the tool itself advises retiring), and the tool already hard-codes the INDEX.md limit that the YAML calls "unassigned". My recommendations: fix those four, name a default reviewer by role, assign both open `who_decides`, and run one small seeded-violation test before anyone claims agents follow it. That test would replace the YAML-versus-Markdown test EJ skipped, which is still **not measured**.

## How I decided

**Data I had before judging (my #5).** I read `docs/memory-system/SOURCE_OF_TRUTH_REQUIREMENTS.yaml` and `tools/memory_index.py`.
- **Levels:** 64 records: 25 MUST, 28 SHOULD, 11 guidance.
- **Checks:** 31 records have `check: reviewer` and nothing else. 11 of those are MUSTs: W3.3a, W3.5a, W4.1c, W5.3b, Rd1.2, Rd2.3a, Rd4.1, Rd5.1, Rd5.2, Rd5.3 and Rd6.1.
- **The tool:** it hard-codes `MAX_LINES = 200` and `MAX_BYTES = 24_000`. Its own comment calls these "the design's example, not a measurement". When over the limit, `--check` returns 1, while write mode only warns and returns 0. Its message says "retire or merge entries until it fits".
- **What these checks were:** these are counts I ran myself (this is my reading of the files, and I wrote the count). They show the layout. They do not show what an agent does.

**Q1: Will an agent follow it?**
1. **Prose and YAML disagree on level (my reading).** Under "What will not be put in" and "Never loaded, at any point", the prose lists flat absolutes. In the YAML, W3.1, W3.3b, W3.4 and Rd2.3b are SHOULD, and K6.1b ("never edited by hand") is SHOULD too. `how_to_read` says which wins between a clause and its requirement, but not which wins between the prose and the YAML. An agent that reads only the prose (the likely case, since the prose is what gets loaded) treats them as gates. An agent that reads the YAML skips them with a reason. Fix: one line in both files saying "the YAML's level governs; the prose explains".
2. **"Text governs" points at nothing (my reading).** Parent requirements such as W1.1 have no record and no text of their own. The rule "when a clause and its requirement seem to differ, text governs" has no second text to compare against.
3. **K4.3's text and its `fails_if` differ (my reading).** The text says that after the first commit an entry "only gains" four things. So `covers`, `source` and `depends_on` can never be corrected, for example after a file rename. But `fails_if` only catches a changed claim. An agent following the text supersedes an entry just to fix a path. One following `fails_if` edits the `covers` line. W6.3a ("keeps both sides… both links") assumes links get added after the commit, which K4.3's text forbids for every link except `superseded_by`.
4. **W6.3b and K6.3b name different checks (my reading).** W6.3b's `fails_if` is "as K6.3b", but its check is `tool`, while K6.3b's check is `reviewer`. The tool cannot see whether a merge was done by hand. It only sees whether the result matches.
5. **A check that does not exist (my #5).** `checks.secret scanner` is listed, and W3.2 (MUST) relies on it, but the Facts say no scanner exists. An agent will assume it is protected.
6. **Paths that a new project won't have (my reading).** `basis.v` and Rd3/Rd4.2 point to `vision-statements/…` and `CACHES.md`. Both exist in this repo under `docs/memory-system/`, but the design is "for any project". An agent installing it elsewhere follows dead links.
7. **Rd6.1 is a test, not an act (my reading).** Rd6.1 is a MUST with a reviewer check, but it tests the design, not an act the agent can do or refrain from. Under `levels.MUST` ("the work it governs stops"), nothing an agent does can satisfy it. See Q5c.
8. **Small issues (my reading).**
   - W1.2b: "a field is missing" could mean that every key must be present even when empty (`superseded_by` on an active entry). One sentence would settle it.
   - The prose's "When to write" table has a typo: "When the work a decision to build something is complete".
9. **How sure I am (my #10).** Items 1 to 8 are what I found reading the files. Whether an agent actually trips on them is **not measured**: n=0.

**Q2: The COO's wording (my #5 and #10: keep what the data supports, change what can't fail as written).**
10. **Keep:**
    - W1.2 split: the tool really does fail an entry with no `---`.
    - W1.1b's "no two entries share an id": the tool checks for duplicate ids.
    - W6.1a's `fails_if`: git can show it.
    - Rd5.3 naming Rd5.4's two cases, and Rd2.3b passing a superseded entry reached by a link: both match Rd4.4.
    - `who_decides` on W4.1c, W5.3b, W6.3a, Rd5.3 (project owner) and K5.2 (agent doing the read): these match the `roles` key.
    - Header keys `what`, `how_to_read`, `levels`, `roles`, `retired_ids`.
11. **Change:**
    - **K5.1's `fails_if`:** "a journal file is edited after it is written" contradicts "appended to". An append is an edit in a git diff. Say instead: "a line already written is changed or removed".
    - **The SHOULD ending "with no written reason":** keep it, but none of the 28 SHOULDs says *where* the reason is written, so no checker can find it. Name the place. A proposed default (my reading, for EJ to confirm): the task's `state.md` or the commit message.
    - **K1.1's `who_decides`, "the project's workflow":** a workflow is a document and cannot decide. Change it to "the project owner, through the project's workflow", or ask EJ.
    - **`checks.secret scanner`:** add "none exists yet; until one does, W3.2 rests on the reviewer".
    - **`basis`:** make the paths relative to the design folder.
    - **`levels.MUST`:** see Q5c.
12. **Can't fail as written:**
    - **W5.2:** "what it learned unwritten" can only be judged by someone who knows what was learned. Keep it as SHOULD, but say the check is the K5.2 journal-read log line, which can be seen.
    - **Rd5.2:** it can only be checked from a transcript. Keep it, and label its check "only on audit".

**Q3: Who reviews the judged checks?**
13. **Two kinds of reviewer check (my #5).** The 31 reviewer-only records split by what a reviewer can actually see:
    - **About the files:** entry content, layout and `state.md` reports (W1.x, W3.x, W5.x, Rd1.x, Rd5.3). A reviewer reading the diff can see these.
    - **About session behaviour:** what a session loaded or read before acting (Rd2.1, Rd2.2, Rd2.3a/b, Rd4.1, Rd4.4, Rd5.1, Rd5.2, Rd6.1). No diff shows these.
14. **Recommendation, labelled proposed (my #4: the control is today's state, where nobody is named, so nothing is checked).** The design should say:
    - **Default:** "whoever merges the change reviews the file-visible checks; the project owner may name someone else".
    - **Session-behaviour checks:** "checked only by auditing a sample of session transcripts, which the project owner orders; otherwise unchecked". Saying "unchecked" plainly is better than implying coverage (my #9).

**Q4: The two open `who_decides`.**
15. **W3.6, whether a procedure can be a script.** Assign it to the agent writing the procedure, with the project owner deciding if it is contested. This follows K5.2's pattern ("the agent doing the read"). It is a judgment made in the moment, while writing.
16. **Rd3.1a, which agents work on the project.** This should not stay unassigned. The data shows the choice has already been made silently: the tool enforces 200 lines and 24,000 bytes, while Rd3.1b calls those numbers "an example, not a limit" (my #5).
    - A MUST with a tool check needs a number someone owns. Which engines a project uses is the project owner's choice. Assign it to the project owner, and record the agent list where the tool can read it, for example `AGENTS.md`.
    - Until then, Rd3.1a should say the tool uses Rd3.1b's example as a placeholder. That is honest about what runs today.

**Q5: The three behaviour questions.**
17. **(a) Retiring with nothing replacing it.** Today it is impossible: K4.1 is a MUST with "no link" in its `fails_if`, and the prose says the same. Yet the tool tells agents to "retire or merge entries until it fits". So the tool directs agents into a K4.1 failure (my #5).
    - It also leaves `retired` and `superseded` with no difference between them.
    - Recommendation: `superseded` needs `superseded_by`; `retired` needs a `changed:` line that gives the reason instead.
    - A nature check (my #6, #7): epigenetic silencing keeps a gene without deleting it and needs no replacement. But the key condition differs: a cell does not need to tell a reader *why*, and an agent does. So I drop the analogy. The mechanism I keep is "kept, marked, with a reason".
18. **(b) Is the supersession step clear enough?** No (my reading). "Change the entry first" (K1.1 and Rd5.4) reads like an edit. The actual steps are spread over K4.3, K4.1, W1.1a and K6.2:
    1. Write a new entry with `supersedes`.
    2. On the old entry, add a `changed:` line, `status: superseded` and `superseded_by`.
    3. Regenerate `INDEX.md` in the same commit.

    Put those steps in K1.1's text, or link K1.1 to K4.3, and say "change" means "supersede" for a claim.
19. **(c) What stops when a MUST fails?** The YAML's "the work it governs stops" doesn't name a unit, while Rd5.3 says carry on with the rest. Proposed, for EJ (my reading): what stops is the thing named in that record's `fails_if`, the entry, commit, load or action. The whole task stops only when the rest of the task depends on it.
    - This matches the one mechanism that exists today: the tool rejects a *commit*, not a task (my #5).
    - Rd6.1 needs its own note, because there is no agent work for it to stop.

## What I need to know
- **Which file an installing agent loads:** the prose, the YAML, or both? If only the prose, Q1 step 1 is the most important finding. If the YAML, Q1 steps 3 and 4 matter more.
- **Whether `retired` and `superseded` should mean different things.** If EJ wants them the same, drop `retired` instead of loosening K4.1.
- **Whether the design ships `CACHES.md` and the vision file with it.** If it does, Q1 step 6 is only a path fix.
- **Whether EJ accepts "unchecked unless audited" for the session-behaviour MUSTs.** If not, they need a mechanism such as a start hook log, which costs build work.

## Costs and risks
- **"YAML governs" line (Q1 step 1):** agents may stop reading the prose's reasons. The price is one line in each file. (my reading)
- **Loosening K4.1 for `retired` (step 17):** agents could retire still-true entries to save space, which edges toward expiry without a reader's check (K4.2). Mitigation: the reason line is visible in `INDEX.md` diffs and to the reviewer. (my #9: say the risk)
- **Writer decides W3.6 (step 15):** projects will be inconsistent, so some procedures stay as prose. This is the price of not routing every case to the owner.
- **Owner decides Rd3.1a (step 16):** one more decision for the project owner, plus a place the tool must read, which is a code change to `memory_index.py`.
- **Merger-reviews default (step 14):** the merger is often the same agent that wrote the change, so the check is not independent. This should be stated, not hidden. (my #10)
- **Narrow MUST unit (step 19):** a task can finish while one part sits blocked. It needs the blocked part recorded in `state.md`, or it gets lost.
- **Test below (my #2):** about one afternoon of agent runs. Cheaper than another expert round.

## How we would know I was right
- **Test (my #2, #3, #4, #8).** Before running it, write down: metric = share of planted violations an agent avoids or reports; stop = after one seeded project; prediction = misses cluster on Q1 steps 1, 3 and 17.
  - **Setup:** a small seeded project with about 10 planted cases, among them: a retirement for size, a mismatch between an entry and the code, a SHOULD skipped with no reason, a path fix in `covers`, and a conflict in `INDEX.md`.
  - **Arms:** (A) the prose alone, the control; (B) prose plus YAML; (C) prose plus YAML with the four fixes above. Same agent and model, one run each.
- **What would change my mind (my #1):** if A and B both handle the planted cases at about the same rate as C, these fixes are not needed. Report that null result with the same weight (my #9).
- **Size of the evidence:** a single run per arm is a hint, not a law (my #10). Repeat it before writing any rule from it.
- **Separate observable checks:** after the K4.1 change, the tool's "retire… until it fits" advice no longer produces a K4.1 failure. After the Rd3.1a assignment, the limit the tool reads can be traced to a named decision, not a hard-coded example.
