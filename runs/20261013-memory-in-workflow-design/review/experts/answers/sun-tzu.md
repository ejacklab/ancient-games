# 孫子 (Sun Tzu) — is the memory change to §4 fit to issue?

## Answer

**Accept with changes.** The shape is right — it sets the position (memory *delivered* to the node, never asked of it) and keeps one whole copy by pointing to the two accepted designs instead of repeating them. It is not yet fit as written: it points to a store that does not exist, one citation claims more than the requirement it cites, and four live lines still send decisions to the file this change removed.

If `project-memory/` will be built before the next design that needs project memory, changes 2–4 are enough. If not, change 1 is required too.

**The changes.**

**1. The ground is missing (required if the store stays unbuilt).** Insert after the §4 intro paragraph, before the table:

> **Not built yet.** `project-memory/` does not exist today; `SOURCE_OF_TRUTH.md` is accepted, not built. Until it exists, the files this section named before the change — `docs/blueprint/decisions.md`, `changelog.md` and `lessons.md` — stay in use, marked *until SoT is built*; a decision, run record or lesson is written there, and the table below applies only where a store and its `INDEX.md` are present.

(That is 范蠡's interim, report §5 O7, which 老子 also falls back to. It is not a new mechanism.)

**2. Wrong citation, §4 Context row (method line 504).** Replace:

> ...never as a sentence asking it to read them (SoT Rd2.1).

with:

> ...never as a sentence asking it to read them (the method's rule, O1/O7/O8; SoT Rd2.1 names the import, the tool's own loading and the start hook, and keeps the words-only instruction as its fallback where none of those can reach the node).

**3. Four dangling pointers.** In `docs/TASK_TYPES.md`, replace every `` `decisions.md` `` (lines 234, 237, 262, 274) with:

> a decision entry in `project-memory/entries/` (method §4)

Then regenerate the bundle with `tools/export_skills.py` — `skills/README.md:4` says the `skills/` copy is generated, "do not edit by hand."

**4. The skill points at two of the four memory slots.** In the "Every node carries five things" table, either (a) append to **Contract**: *"; a decision or fact it acts on is checked against the code, test or commit it points to before acting, and a mismatch is reported, not settled (method §4)"*, and to **Tools**: *"; a cache is never loaded at start and is used only for a free-text search, and only where it is built (method §4)"* — or (b) remove the restated rule from the Context and State rows and let step 8's "How nodes use project memory and its caches: method §4" carry it. Do not do both; one whole copy, not two.

**5. Three small fidelity fixes (same file, §4 table).**
- **Tools row:** replace "full-text search or the vector index" with *"full-text search, or the hybrid vector search where it is built (CACHES B1.2, *proposed*)"*. CACHES makes the vector index conditional and hybrid-only; the row currently makes it an equal.
- **State row:** replace "(K5.2)" with "(K5.1; K5.2)" — the journal write is K5.1's, the end-of-task conversion is K5.2's.
- **Contract row:** replace "checks it against the code first" with *"checks it against the code, test or commit it points to (Rd5.1)"*.

**The two calls: keep both.** (a) Keep the `changelog.md` drop *in the target state*: its query — "what did run N change, and did it pass?" — is the commit log, `runs/<run-id>/` and the task's `state.md`, and SoT W3.1 bars commit-log content from memory. But name that home (change 1 does it while the store is unbuilt), and put the release-note question to EJ (below). (b) Keep 老子's "kept only when named" out: it changes SoT W4.1 and K5.2, which EJ accepted and only EJ changes. Keep Linus's separate per-node contract out: the four rows already give the per-node slot, and a second copy of SoT's rules is a second, broken copy.

## How I decided

1. **my #1 (Reckon before battle).** I laid the change out against EJ's words — project memory *and* caches, right time *and* right way — and counted. In the table: delivery (Context), pre-action check (Contract), write timing (State), cache routing (Tools). Not in it: whose memory each node needs, and where a run's change record lives. "More wins, fewer does not, how much less none at all?" (*quoted*). I did not judge the writing, only what is on the page.

2. **my #12 (Seek it in 勢, not in people).** The change's core is the right lever: the designer sets the position — the brief, the import, the hook — and does not ask the agent to remember. That is what the report's E1/E2 (*reported*) support, and it is the change I argued for. 「故善戰者，求之於勢，不責於人」 — "the skilled fighter seeks it in 勢 and does not demand it of people" (*quoted*).

3. **my #3 (Whole over broken).** Pointing at SoT and CACHES instead of copying their rules keeps one whole copy; refusing Linus's per-node copy is right for the same reason. The denial clause I proposed earlier was kept — "a verifier gets no worker's reasoning, and no entry or journal that carries it" — which is more than I expected and is correct.

4. **my #4 (Know the ground).** Here it fails. I checked: `ls project-memory` returns "No such file or directory," and `docs/memory-system/` holds the accepted design, not a built store. The change removed the only rules that worked and put a pointer in their place. 「知敵之可擊，知吾卒之可以擊，而不知地形之不可以戰，勝之半也」 — "knowing the enemy can be attacked and our troops can attack, but not that the ground does not permit battle, is half a victory" (*quoted*). This is change 1.

5. **my #11 (Foreknowledge from people, labelled).** A cited id must be the requirement the sentence rests on. "(SoT Rd2.1)" is not: Rd2.1 names the import, the tool's own loading and the start hook, and it keeps the words-only instruction as its fallback. "Never as a sentence asking it to read them" is the run's own option O1/O7/O8. The same count found `docs/TASK_TYPES.md:234,237,262,274` still logging decisions in `decisions.md`, a file this change removed. Changes 2 and 3.

6. **my #16 (Orders clear first, then enforced).** The State row's "its check fails if a required one is missing" is the right shape — a check that can fail. But it is the method's own addition, not SoT's, and mixing a per-node write with the end-of-task conversion in one cell is an unclear order. K5.1 and K5.2 are different requirements. Changes 4 and 5.

7. **my #13 and my #1 (Not every road; count first).** On call (a): I keep the drop, because the run record is not memory (SoT W3.1) — but only a stored run record answers it, and removal without a named home is how a listed query goes missing. On call (b): 老子's gate changes an accepted requirement EJ has not decided; my #1 says do not commit to a course not reckoned. Linus's contract is a duplicate of what SoT already holds. Both stay out.

8. **my #5 and my #6 (Move only on advantage; mix harm into benefit).** I recommend only lines with a named defect, and no new mechanism. The caches half is otherwise faithful: the row's "exact strings, 'every entry covering X', 'have we never…', header fields and 'why'" maps the CACHES routing table row for row. The one fidelity slip is the vector index, fixed in change 5. The costs are below.

## What I need to know

1. **Will `project-memory/` be built before the next design that needs project memory?** If yes, change 1 is not needed and the pointer stands. If no, change 1 is the difference between a method with working rules and one that points at nothing.
2. **Where do release notes come from now?** The old §4 generated them from `changelog.md`'s `release note:` lines; the new text names no home. If EJ still wants them, name the file; if not, say so plainly.
3. **Whose memory does each node need — task, project, agent or user?** The Context row says "the entries the node needs" as if there were one store; SoT covers task and project, and agent and user memory live in the home folder. The answer changes whether the row is complete. (This is my earlier Q14, still open in the report.)
4. **Is `docs/TASK_TYPES.md` in this change or a later one?** If later, change 3 waits, and the four dangling pointers stay until then.
5. **Does EJ accept CACHES B1.2 (the vector index, hybrid-only), or does it stay *proposed*?** If it stays proposed, change 5's vector clause becomes "drop the vector index from the row."

## Costs and risks

- **Change 1 is a second home for a time.** When SoT is built, someone must delete the interim or the repo has two places a decision can live (*my #3*, *my #6*).
- **The delivery rule costs brief preparation on every node** and buys nothing while the store is empty (O7's own cost, *quoted* in the report).
- **Change 3 touches the file `design_gate.py` parses** (`design_gate.py:6`), so the default pattern must be re-checked after the edit; a wrong edit changes what the gate accepts (*my #16*; my reading of the script).
- **Change 4 adds two rows of upkeep**; the alternative costs a designer who reads only the skill table missing the caches (*my #6*).
- **Leaving 老子's gate out** leaves the store with no limit from within: if nothing ever leaves, it grows (M15, his reading, *not measured*). That is EJ's call, not a defect of this change (*my #1*).
- **The denial clause and the pre-action check cost brief tokens** and can omit an entry a node needed; both are already accepted (*my #6*).
- **The pointer depends on a design that is not built** (report F1, *verified*: `project-memory/` is absent). No edit to the method can make the store exist.

## How we would know I was right

My test, run on the next three workflow designs (the count 范蠡 and 老子 both proposed):
1. Every node that needs memory names the entry or its `covers` path, and its delivery is a brief, an import or a hook — never a sentence asking it to read. Right = zero ask-only briefs. Wrong = one ask-only brief, or a needed entry missing while the brief said nothing (*my #2*, *my #4*, *my #11*).
2. `grep -rn 'decisions.md' docs/TASK_TYPES.md` returns nothing after change 3.
3. A fresh session with only a clone and a task id names the next step from `state.md` and follows a recorded decision without asking EJ again (SoT Rd6.1).
4. Count the new memory sentences in §4 and the skill over two runs. If none of changes 1–5 fixes a defect those runs show, delete them (*my #5*, *my #6*; 老子's "no new sentence without a harm it fixes," *quoted* in the report).

I was wrong if a design follows the new §4, a node acts on a decision that was never delivered to it, and no check in that design catches it.
