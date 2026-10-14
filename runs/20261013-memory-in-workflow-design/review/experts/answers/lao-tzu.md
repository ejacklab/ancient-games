I'll read that brief first.
# 老子 (Laozi) — the new §4 memory table: right direction, two defects, four cuts

## Answer

**Accept with changes.** It does what EJ asked — the four node fields now carry *when* and *how* for both designs — but two rows say something the designs do not say, and the block is one step short of the size it should be. Four cuts and one deletion, given below, and one call to change: `changelog.md` goes back only for the release note, which nothing now holds.

## How I decided

1. **The direction is right, and I will not reopen it.** All four experts took the pointer to SoT, and the change took it. Keeping the old three files beside the accepted design is the hoarding I named earlier, and my #1 is subtraction, `quoted`: 「損之又損，以至於無為。無為而無不為。」 The table is a map keyed to ids, not a duplicate document — that is the smallest form that can work.

2. **One call the COO made is a fact, not a choice: Linus's per-node contract is in.** The brief says it was left out. §4 L504–507 *is* a per-node memory contract in four rows — the shape of O6. I argued against that shape (`one sentence and not a section`), so I say so once and move on; the four changes below cut what it repeats, not the rows themselves.

3. **Change 1 — the Context row (L504) cites the wrong id and forbids what Rd2.1 permits.** Rd2.1 is about *session start* and names four files (`AGENTS.md`, `INDEX.md`, the `work/` listing, the task's `state.md`); "named by id or by the paths they cover" is Rd4.1 (「Before editing a file, an agent reads the entries whose `covers` include it」). And Rd2.1 ends: *"Only where none of these exists does the first instruction in `AGENTS.md` ask the agent to read them"* — SoT keeps a last-resort ask; the row says `never`. A method stricter than the design it cites is a second copy drifting. New text for the row:

   > `| **Context** — memory in | The entries the node needs, named by id or by the paths they cover (SoT Rd4.1), and how they reach it: in the brief, by an import, or by a start hook, wherever the engine allows — never as a sentence asking it to read them, which is this method's rule and stricter than SoT Rd2.1 (report E1, M1, M2). What it must not receive: a verifier gets no worker's reasoning, and no entry or journal that carries it. |`

   *"wherever the engine allows"* is not decoration. Report T5 and T8 say neither Codex nor opencode parses an `@` import, and S32 found no Codex hook setting. On two of the engines the brief is the only mechanism that exists.

4. **Change 2 — the Contract row (L505) stops a build node from building.** As written, a node implementing decision D checks D against the code, finds the code does not yet do D, and reports a mismatch instead of writing the code. That is my #6, `quoted`: 「為之於未有，治之於未亂。」 SoT's own Rd5.4 says that is not a mismatch. New text:

   > `| **Contract** — before acting | A node that acts on a decision or fact checks it against the code first; a mismatch is reported in the state file and to EJ, not settled (SoT Rd5). Two cases are not mismatches: a decision with no `done:` yet, and the node whose own task is to make the change (SoT Rd5.4). |`

5. **Change 3 — the Tools row (L507) drops the vector's own question.** CACHES gives full-text and vector two different questions and two different triggers (B1.1, B1.2), with the vector *proposed* and built after full-text. The row merges both into one question, so a node whose wording differs from the entry's — the only case the vector exists for — is told to use the files. New text:

   > `| **Tools** — the caches | A cache is never loaded at start (CACHES Rd1), and one is used only after its own trigger fires: B1.1 full-text, B1.2 vector — the vector is proposed, and only after full-text exists. Exact strings, "every entry covering X", "have we never…", header fields and "why" questions go to the files, never to a cache (CACHES § When to use which store): `INDEX.md`, grep, then read the entry. A cache answer names its entry, and the node reads that entry before acting on it (Rd2). |`

   The five "never a cache" items I would not cut. They are the denial half, and my #17 is that the use is in what is not there, `quoted`: 「故有之以為利，無之以為用。」 The empty half is sized by what the node needs.

6. **Change 4 — delete L515.** L509–511 and L515 say the same thing about Codex memory, four lines apart. One sentence must hold it. Delete `Not verified: Codex's memory and subagent features beyond `AGENTS.md`.` and end L511 with ` (report M14, T6; no run has broken such a rule, so the harm is not measured).` My #1 again: a fact in two places is two places to forget.

7. **Change 5 — the change missed its own method text.** `docs/TASK_TYPES.md` (and its mirror `skills/workflow-design/references/task-types.md`) still logs to a file this change deleted: L234 `the questions and answers are logged in `decisions.md``, L237 `a mainstream stack, its reason in `decisions.md``, L262 `loser gets one line in `decisions.md` saying why it lost`, L274 `(non-functional) and in `decisions.md``. The skill's step 2 sends every designer to that file. Replace all four with `a decision entry in `project-memory/entries/``, and give L262 the place SoT has for a rejected alternative — its **Why:** — since W1.3 has no "alternatives rejected" field:

   > `loser gets its reason in the decision entry's **Why:**.`

8. **The preamble leans on evidence the report marks as about something else.** L494–496 says "read only if the model decides to, which in measured runs it often does not (report E1, E2)". E1 is a docs *skill* never invoked; E2 is a code-graph *tool* with zero calls. The report's own thin-evidence note says so. The claim is sound on §1's own reading, so name the source that carries it. My #8, `quoted`: 「知不知上，不知知病。」 Replace `(report.md, E1, E2)` with `(report.md §1, my reading; E1 and E2 measured invoking a skill or a tool, not reading a file)`.

9. **Call (a), `changelog.md`: change, one line, and only for the release note.** Its real query — *what did run N change, and did it pass* — is answered by git and by W5.3's `done:`, so the file goes. Two things it carried have no home. The rejected alternative is fixed by change 5. The release note has nothing: SoT and CACHES do not mention it, and I looked for a generator and found none. The old paragraph was the only place that said where one comes from. Add after the table:

   > `A release note is for users, not for agents: it says what shipped, not why, so it is an output of the run and not memory. Nothing generates one today; when one is needed it is written from the decisions' `done:` lines (SoT W5.3) and the commits.`

   That is one sentence, not a file. If EJ's answer is that no release note is wanted, delete the sentence and the drop is complete.

10. **Call (b), keep-when-named: leave it out.** SoT W4.1 and K5.2 are EJ's accepted decisions and no answer came (Q15). My own condition from the earlier answer stands: if it is rejected, drop the half, and do not rewrite it into something larger. My fallback was孫子's denial plus the pointer, and the Context row's second sentence is the denial, so my fallback is now in place. The price I accept is stated below.

## What I need to know

1. Will SoT be built before the next run that needs project memory? `project-memory/` does not exist. If not, 范蠡's interim applies and §4's pointer leads to nothing: mark it *"until SoT is built"* and keep the changelog line for one line.
2. Does EJ want a release note at all, and who writes one today for a product that ships? That decides change 9.
3. Do EJ's designs run Codex, agy or opencode nodes, and does any of them have a hook or import that can carry a file? Report T5/T8 say no; S32 found none. This decides whether change 1's "wherever the engine allows" is a real mechanism.
4. Will EJ change SoT W4.1 or K5.2? Until yes, call (b) stands.
5. Which write time is "the run's end" that names what is kept — W5.1, W5.3 or W5.2? Still open (Q16), and I will not fill it.

## Costs and risks

- **Change 1** costs a clause, and the stricter rule is now the method's own rather than SoT's — a place where method and design may part company, which is why the difference is named in the row (*my reading*: a silent divergence is the thing to avoid, not a divergence).
- **Changes 1, 3 and 4** cut words, and my #1 warns that cutting can remove something still wanted. Each cut here removes a restatement, not a rule; if a designer later needs it, SoT and CACHES hold it (*my reading*).
- **Change 2** costs a sentence in every node's Contract and a designer who copies it blindly will add a clause that does nothing (*my reading*). The alternative — leaving the row as is — costs a build node that refuses to build, which is worse and silent.
- **The Tools row still costs a designer attention on a store with no files** (CACHES: "Neither cache is needed today"). I keep it because it is the denial half; the price is a paragraph of design effort for an unbuilt trigger, on every design.
- **Change 5** touches four lines in a method reference that also has a second copy under `skills/`. Both must change, or the method contradicts itself in one repo (`AGENTS.md` asks readers in words to check `CLAUDE.md`; two copies is the failure mode I have already seen here).
- **Leaving out keep-when-named** leaves nothing in the method that names what *leaves* the store. M15 stands, unmeasured. `changelog.md` is gone and with it the "any node proposes, the COO appends" pattern my rule leaned on — but that rule never reached SoT, so nothing was lost that was working.
- **A call I did not make**: nothing here changes whether agents use memory well. Report §5's own table says none of O6–O9 has been measured. `n=0` is already in the method changelog.

## How we would know I was right

1. `rg 'decisions\.md|changelog\.md|lessons\.md' docs/ skills/ .claude/ --glob '!runs/**' --glob '!site/**'` returns nothing live. Today it returns six, four of them in `docs/TASK_TYPES.md`.
2. The next design with a build node has the Rd5.4 exception in its Contract, or a run shows a build node that wrote a mismatch report for the decision it was told to implement.
3. §4 memory block line count does not rise again without an id in `report.md` or a run showing the harm. If a later diff adds a row, I was wrong about the size.
4. After the next SoT revision (its ids moved three times in two days: runbooks removed, Rd2.2 split, prefixes changed), §4 does **not** need a matching edit. If it does, the block is a second copy and I was right.
5. A designer following the changed §4 reaches the right memory in a matched test — a relevant prior decision, an entry contradicted by the code, a fresh-session handoff. Wrong if a needed entry is missed while the brief said nothing; that is my narrowing cost, and it is the one test that could overturn me.
6. I am wrong about call (b) if the first three runs that use project memory show entries accumulating that no reader ever asks for. That count does not exist today, which is why I say watch rather than write a sentence.
