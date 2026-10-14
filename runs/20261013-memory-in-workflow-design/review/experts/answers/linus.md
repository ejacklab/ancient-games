# Linus Torvalds — review of the §4 memory change

## Answer
**Accept with changes.** The approach is right. It handles memory inside each node's existing fields and points to the two accepted designs. Two parts are wrong as written:
- It breaks two live products that still keep the three files: SEZA and `site/ancients`.
- Its Context row says one thing that SOURCE_OF_TRUTH (SoT) forbids and one thing SoT does not say.

I propose six changes, with exact text below. On the two calls: keep both. Call (a) needs a transition line, and the release-note question goes to EJ.

## How I decided

1. **My #1 and #3: does this break what used to work for a user?** It does, and I checked the files.
   - `/home/smoke01/dev/seza/docs/blueprint/` holds `decisions.md` (53 lines), `changelog.md` (199) and `lessons.md` (15). SEZA's changelog header says "Generated release notes, when needed, come from the `release note:` lines here."
   - `site/ancients/docs/blueprint/` holds all three files. Its `README.md` lists them, and `01-vision.md`, `08-non-functional.md` and `tests/test_mobile.py:481` cite "decisions.md D1".
   - Neither product has a `project-memory/` folder (`ls` says it does not exist).
   - The change now sends a designer working on either product to a folder that does not exist, and the template no longer mentions the files they use. My #1, `quoted`: "If the kernel used to work for you, the rule is that it continues to work for you."
   - This is a breakage in how a user works, not just a doc mismatch (my #3). The fix is a transition line (change 1), not a migration.

2. **My #10: one wording for both schemes, so the old files stop being a special case.** `docs/TASK_TYPES.md` lines 234, 237, 262 and 274 still send decisions to `decisions.md`, and so does its copy at `skills/workflow-design/references/task-types.md`. The skill's step 2 reads that file. The change missed them.
   - If those lines say "the product's decision record (method §4)", they are right both for a product that still has `decisions.md` and for one with `project-memory/entries/` (change 6).

3. **My #9: check each cited id against the data it claims to follow.** I read each id in `docs/memory-system/SOURCE_OF_TRUTH.md` and `CACHES.md`.
   - **Context row, "by a start hook … (SoT Rd2.1)": wrong.**
     - Rd2.1 allows a start hook only for the four session-start reads.
     - Entry bodies are "on demand (Rd4)" under Rd2.2.
     - Rd2's Fails-if reads: "a start hook or instruction loads any memory file outside Rd2.1".
     - So a hook that delivers entries breaks the accepted design.
   - **Context row, "never as a sentence asking it to read them (SoT Rd2.1)": overstated.** Rd2.1 keeps exactly that as its fallback: "Only where none of these exists does the first instruction in `AGENTS.md` ask the agent to read them."
     - In this repo a brief is itself delivered by asking: "read <file> and do what it says".
     - So "in the brief" only works if the entry's text is inside the brief, not just a pointer to it.
   - **Contract row: misses two parts of SoT.**
     - It leaves out Rd4.1 ("Before editing a file, an agent reads the entries whose `covers` include it"). That is the main reading time for a node that builds.
     - It leaves out the Rd5.4 exceptions. Without them, a node building under a decision that has no `done:` yet would report its own unfinished work as a mismatch.
   - **State row: citations wrong or incomplete.**
     - "Raw notes to the task's `journal/`" is K5.1, not K5.2.
     - "Lessons, observations and hypotheses at the end of the task" is W5.2.
     - K5.2 also requires the journal read to be logged in `state.md`, and that log line is K5.2's own Fails-if check. The row leaves it out.
     - W5.3's `done:` applies only to "a decision to build something", never to a standing rule.
   - **State row, "its check fails if a required one is missing":** this is in neither design. It is the method's own rule (my earlier proposal) and should be labelled as such.
   - **Tools row: correct.**
     - CACHES Rd1, B1 and the routing table ("When to use which store") are cited correctly. The exact-string, completeness, absence, header and "why" rows match the table.
     - "A cache answer names its entry" is CACHES Rd2.1. "Reads that entry before acting" is SoT Rd5.1. Citing Rd2.1 and Rd5.1 is more exact than "Rd2".
     - "What do we know about X" is the full-text row. The vector row covers a question worded differently from the entry. A small wording fix (change 5).
   - **W5.1, K6.2 and CACHES Rd1 are right.**

4. **My #11: anything odd must be explained in the record.** The METHOD_CHANGELOG line does not say that two products still use the removed files. Change 1 adds that sentence.

5. **My #4 and #6: does the method decide something only EJ decides?** Leaving out 老子's "keep only when named" rule is right. It would change SoT W4.1 (no owners, no approval) and K5.2 (the writer chooses what to keep), and EJ accepted both. The method cannot override the design it points to.

6. **My reading: my own per-node contract.** It was not left out. My earlier answer proposed specifying memory "in its existing Context, Contract and State fields", plus required outputs and checks. The four rows and the sentence "the node's return lists the entries it wrote" are that proposal. A separate block would be a second copy. Keep it as it is.

7. **My #13 and #8: call (a), `changelog.md`.**
   - In the target state, its question ("what did run N change, and did it pass?") is answered by W5.3's `done:` (time, result, tests, a pointer to `runs/`) and by git. W3.1 bars commit-log content from memory. So the drop is right for products on `project-memory/`.
   - Products that have not moved keep both schemes for now (my #8, "can't we just do both?"), and the comparison settles itself.
   - Release notes lose their only stated source. SEZA uses `release note:` lines today. That goes to EJ, below. I am not filling it in myself.

8. **My #19: one logical change per patch.** The working tree also has unrelated edits: `docs/code-graph/CODE_GRAPH.md` (+141), `docs/TASK_TYPES_LEDGER.md` and `runs/20261012-index-md-build/state.md`. Commit this change on its own.

### The changes, exact text

**Change 1. Method §4, a new paragraph straight after the paragraph that ends "(3.6; the skill's 'Every node carries five things'):", before the table:**
> **Until a product has `project-memory/`.** A product that already keeps `docs/blueprint/decisions.md`, `changelog.md` and `lessons.md` (SEZA and `site/ancients` on 2026-10-13) keeps writing them under the rules this section had before 2026-10-13 (`docs/METHOD_CHANGELOG.md`), until EJ moves it to `project-memory/`. The table below still applies, read against those files. Nothing in this change moves or deletes them.

Add the same sentence to the end of the METHOD_CHANGELOG entry. Under "## Project memory — not in the blueprint" in both `blueprint.md` templates, add:
> A product that already has `decisions.md`, `changelog.md` and `lessons.md` here keeps them until EJ moves it (method §4).

**Change 2. Context row:**
> The entries the node needs, named by id or by the paths they cover, and how they reach it: their text inside the brief, or by an import, so the node does not have to choose to read them. A start hook carries only the four session-start reads (SoT Rd2.1); entry bodies are never loaded by a hook (SoT Rd2.2 and Rd2's Fails-if). A sentence asking the node to read an entry is the fallback, used only where neither the brief nor an import can carry it, and the design says so (SoT Rd2.1). What it must not receive: a verifier gets no worker's reasoning, and no entry or journal that carries it.

Make the same change to the skill's Context row: "delivered as text in the brief or by an import; a sentence asking for them only as the stated fallback (method §4)".

**Change 3. Contract row:**
> Before editing a file, the node reads the entries whose `covers` include it (SoT Rd4.1). Before acting on a decision or fact, it checks it against the code; a mismatch is reported in the state file and to EJ, not settled (SoT Rd5.1, Rd5.3). Two cases are not mismatches: a decision with no `done:` yet whose code is still being built, and the node whose own task is that change (SoT Rd5.4).

**Change 4. State row:**
> What the node writes, and when: a decision or fact before the code it governs, and a human correction at once (W5.1); `done:` on a decision to build something when its work is complete (W5.3); raw notes to the task's `journal/` (K5.1), read at the end of the task and before a handoff, turned into lessons, observations and hypotheses, with that read logged in `state.md` (W5.2, K5.2); `INDEX.md` regenerated in the same commit as any entry (K6.2). The node's return lists the entries it wrote, and its check fails if a required one is missing (this method's rule, not the design's; n=0).

**Change 5. Tools row.** Replace "A node uses full-text search or the vector index only for a free-text 'what do we know about X' question" with:
> A node uses full-text search for a free-text "what do we know about X" question, and the vector index when its wording may differ from the entry's, and only when that cache exists

Replace the final "(Rd2)" with "(CACHES Rd2.1; SoT Rd5.1)".

**Change 6. `docs/TASK_TYPES.md` and its copy `skills/workflow-design/references/task-types.md`, lines 234, 237, 262 and 274:**
- Lines 234, 237 and 274: replace `` `decisions.md` `` with `the product's decision record (method §4)`.
- Line 262: replace "loser gets one line in `decisions.md` saying why it lost" with "loser is named, with why it lost, in the product's decision record (method §4)".

## What I need to know

1. **Does a brief that carries an entry's text count as "an instruction [that] loads any memory file outside Rd2.1" under SoT Rd2's Fails-if?** Only EJ can rule on SoT.
   - If **no**: change 2 stands.
   - If **yes**: the Context row must name entries by id, the node reads them on demand under Rd4.1, and "load, don't ask" covers only the four Rd2.1 reads. In that case the main finding the change rests on (E1: a skill "never invoked" in 56% of cases) protects less than the change hopes.
2. **Release notes for a product on `project-memory/`: does EJ still want them, and from what?**
   - If yes, the method needs one sentence naming the source, written by EJ, not by me.
   - If no, say plainly that release notes are no longer produced.
   - SEZA keeps its `release note:` lines under change 1 either way.
3. **When does SEZA or `site/ancients` move to `project-memory/`?** If never, change 1 is permanent and the method carries two schemes. Then the old rules should be restored to §4 in full, not just pointed to in the changelog.

## Costs and risks

- **Change 1 (my #1, #8):** two memory schemes live side by side until EJ moves each product. A designer must check which one a product uses. The price is one sentence and some reader confusion. The alternative is two live products whose method no longer describes their files.
- **Change 2 (my #9):** dropping start hooks for entries removes the one delivery route that needs nothing from the brief author. Inlining entry text makes briefs longer, so it costs tokens on every node that needs memory. Not measured.
- **Change 3 (my #9):** Rd4.1 adds a read before every edit to a covered file. That is SoT's cost, already accepted, now made visible here.
- **Change 4 (my #9):** the `state.md` log line is one more thing a node must write, and one more way its check can fail.
- **Change 6 (my #10):** "the product's decision record" is less exact than a file name. A new reader has to open §4 to learn which file it means.
- **Keeping both calls (my #4, #5):** easy to reverse, since each is one paragraph. The risk: if EJ later wants 老子's rule, SoT changes first, then this table.
- **Accepting at all (my #2, #7):** this is n=0. Nothing yet shows that nodes designed this way use memory better. My acceptance means the change is coherent and faithful once the six changes are made. It does not mean the change works.

## How we would know I was right

- **Static checks, runnable now:**
  - `grep -n 'decisions.md' docs/TASK_TYPES.md skills/workflow-design/references/task-types.md` returns nothing.
  - Every SoT or CACHES id cited in the §4 table appears in a sentence of the cited design that says what the row says (a reader check, row by row).
  - No row mentions a start hook carrying anything beyond the four Rd2.1 reads.
- **Regression check:** the next workflow designed for SEZA or `site/ancients` writes its decisions to that product's `decisions.md`, and nobody asks "where do decisions go now?".
- **The test I proposed before, still not run:**
  - Take matched tasks in a product with `project-memory/`, with the engine, model and memory settings held fixed.
  - Include a fresh-session handoff, a prior decision that applies, and an entry that the current code contradicts.
  - Compare the method before and after this change.
  - The change has earned its place if the "after" nodes:
    - take up the correct next step after the handoff;
    - follow the decision;
    - report the contradiction under Rd5.3, holding the three items;
    - log the journal read;
    - return the entries they wrote;
    - and do all this at a token and time cost EJ accepts.
  - Complete-looking node contracts alone would not show that.
