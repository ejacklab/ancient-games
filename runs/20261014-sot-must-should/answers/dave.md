# Dave: which source-of-truth requirements are MUST, SHOULD or guidance

## Answer
**MUST** covers three kinds of requirement, and only these:
- **Safety bounds:** credentials (W3.2, and the credentials item of Rd2.3), and memory never overriding standing instructions (Rd5.2).
- **EJ's one gate:** EJ's one exception to "no approval", where a reader reports a mismatch and does not settle it (Rd5.3).
- **Things the existing tool already enforces, or cannot work without:** the parts of W1, the `status` set, K6, Rd1 and Rd3.1 that the tool already checks.
- **Losses a reader cannot see:** K4.1, K4.3 and W6.3.

**SHOULD** covers everything a reviewer has to judge, because n=0 and nobody does that reviewing yet. **Guidance** covers definitions, explanations, and lines with no failure condition. One id gets two levels in many rows, and each such row says which part gets which.

| Id | Level | Reason (one line) |
|---|---|---|
| W1.1 | **Split.** MUST: one file per entry; the prefix matches `kind`; the id is unique and never changes. SHOULD: the `DD-MM-xxxxxx-YYYY` form | The tool already fails on a prefix that does not match the kind and on duplicate ids, and links break if an id changes. The date form is a method, and the tool only checks that the id is not empty. |
| W1.2 | **Split.** MUST: the `---` delimiters and the `id`/`kind`/`status` keys. SHOULD: the other keys | The tool parses only these and fails without them. No lint checks the rest yet. |
| W1.3 | **Split.** MUST: the `**Why:**` line. SHOULD: `**How to apply:**` and one claim per entry | The tool already fails an active entry with no `**Why:**`. The rest is checked by a reviewer, and there is no reviewer yet. |
| W2.1 | guidance | A definition. Nothing fails when it is not followed. |
| W2.2 | **Split.** Guidance: the definitions. SHOULD: "a hypothesis is a guess, labelled as one" | Labelling matters a great deal, but it is a judged check and no reviewer exists yet. It is the first candidate to promote. |
| W3.1 | SHOULD | A rule against duplication. Overriding it with a written reason does no harm. |
| W3.2 | MUST | A safety bound. The repo is public, and a committed secret cannot be taken back. |
| W3.3 | SHOULD | Bloat and privacy. The worst part (credentials) is already MUST under W3.2. |
| W3.4 | SHOULD | An honesty rule, but judged and with no gatekeeper today. It is the first candidate to promote. |
| W3.5 | SHOULD | A placement method. |
| W3.6 | SHOULD | A placement method. |
| W4.1 | **Split.** Guidance: "anyone may…, no owner". MUST: `status` is one of the three | A permission cannot fail. The tool already fails any other status. |
| W4.2 | SHOULD | Every commit's history already records the time and author, and the model in a trailer. Whether `changed:` adds anything has not been measured. |
| W4.3 | guidance | Says where history lives. Nothing to fail. |
| W5.1 | SHOULD | Timing is a method. Its check is partly judged. |
| W5.2 | guidance | No line in W5's "Fails if" covers it. |
| W5.3 | **Split.** SHOULD: adding `done:`. MUST: a mismatch is reported, not settled in `done:` | The second part is Rd5.3. |
| W6.1 | SHOULD | A method that serves the no-loss outcome in W6.3. |
| W6.2 | SHOULD | A method. It costs extra in a single-agent session. |
| W6.3 | MUST | A merge that drops one side loses data silently: no later check would show it. |
| K1.1 | SHOULD | Imposes an order of work, which is the method RFC 2119 §6 warns against. Rd5 catches drift when the entry is read. |
| K4.1 | MUST | Easy to check with a git query. A deleted entry disappears from what readers see. (Conflict with W3.2 below.) |
| K4.2 | guidance | The K4 "Fails if" has no condition about age. It describes the design (no expiry by age). |
| K4.3 | MUST | A rewritten claim looks like the original to a reader, and the W6.3 merge safety depends on it. (Conflict with W3.2 below.) |
| K5.1 | SHOULD | A method. |
| K5.2 | SHOULD | The design itself says a missed read "loses nothing: the next read covers it", so it is a default, not a gate. |
| K6.1 | MUST | `memory_index.py --check` enforces it today. |
| K6.2 | MUST | The same tool gate. The `docs/index-md/` pointer in it is guidance. |
| K6.3 | MUST | The tool's check catches a hand-merged `INDEX.md`. Conflict markers in an entry are judged. |
| Rd1.1 | **Split.** MUST: the `project-memory/entries/` and `project-memory/INDEX.md` paths. SHOULD: the rest of the layout | The tool hard-codes those two paths. |
| Rd1.2 | MUST | The core value: plain files, nothing that only a service holds. The tool already fails entries git does not track. |
| Rd2.1 | SHOULD | How the four files get loaded differs by tool, and the check is judged. This is the first thing to test. |
| Rd2.2 | guidance | Describes when later reads happen. Nothing fails on its own. |
| Rd2.3 | **Split.** MUST: credentials. SHOULD: the other five items | A safety bound for the first. The others manage how much context is loaded. |
| Rd3.1 | MUST | The tool's check mode already fails over the limit. The 200-line / 24 KB numbers are an example, not a measurement. |
| Rd4.1 | SHOULD | Judged, and it costs a read before every edit. |
| Rd4.2 | guidance | How to search. |
| Rd4.3 | guidance | How to answer "why" questions. |
| Rd4.4 | SHOULD | Repeats part of Rd2.3. |
| Rd4.5 | SHOULD | Naming whose memory it is, judged within a session. Nothing is persisted. |
| Rd5.1 | SHOULD | The only drift check left after K2 and K3 were removed, but it applies to every read and is judged. A promotion candidate. |
| Rd5.2 | MUST | A safety bound. Anyone may write memory (W4.1), so memory text could carry injected instructions. |
| Rd5.3 | MUST | EJ's one gate in a design with no approval step. |
| Rd5.4 | guidance | Sets the scope of Rd5.3. A definition. |
| Rd5.5 | guidance | Explains a limit. |
| Rd6.1 | SHOULD | A measure of whether the whole system works, observed after a handoff. It cannot stop a commit, so it cannot be a MUST under the given definition. |

## How I decided
1. **What the levels rest on (my #5).** Only one tool exists, `tools/memory_index.py`. I read it, and it already fails on:
   - a header that does not start with `---` on line 1;
   - an empty id, or duplicate ids;
   - a `status` outside the three;
   - an active entry's `kind`/prefix mismatch, or a missing `**Why:**`;
   - an entry git does not track;
   - an `INDEX.md` that differs from what it builds, or is over 200 lines / 24,000 bytes.

   It does **not** check the id's date form, `**How to apply:**`, the other header keys, or conflict markers. There is no secret scanner: `tools/` holds only `memory_index.py` and `export_skills.py`, there are no git hooks or `.github/`, and gitleaks, trufflehog and detect-secrets are not installed. So "MUST, the tool already enforces it" is a fact for some rows and unbuilt for others, and I split rows on that line.
2. **A finding (my #9).** W1.1 says *"There is no runbook prefix"*, but the tool still has `"R": "runbook"` in `PREFIX_KIND` and `R` in `ENTRY_NAME`. The W1.1 MUST is enforced today with six prefixes, not five, so the tool needs fixing (one line).
3. **The MUST test (my reading, from the brief's quotes).** RFC 2119 §6: *"they MUST only be used where it is actually required"*. The skill says a safety bound earns MUST and a method does not. That gives MUST for:
   - the two safety items (W3.2 and Rd2.3 credentials, Rd5.2);
   - EJ's explicit gate (Rd5.3);
   - what the tool needs in order to work. This is RFC's own reason, interoperation (my reading).
4. **Can it fail? (my reading of the brief's levels).** A line with no failure condition is guidance: W5.2, K4.2, Rd2.2 and the definitions. I used the "Fails if" lines to decide.
5. **A judged MUST with no judge (my #8, my #10).** W4.1 rules out an approval gate, and the brief says judged checks are done "by a reviewer reading", but no workflow has that reviewer yet and n=0. A gate nobody runs is a MUST in name only. So W3.4, the hypothesis label in W2.2, Rd5.1 and Rd2.1 start as SHOULD and are the first to promote. This is small and reversible: promoting later costs one edit.
6. **Exception for losses nobody sees (my reading).** K4.1, K4.3 and W6.3 stay MUST even though no lint exists. A missed check there leaves no trace for a reader, and K4.1 and K4.3 can each be checked with one git query.
7. **A conflict found while checking (my #1).** W3.2, K4.1 and K4.3 cannot all be MUST without an exception. If a credential is committed inside an entry's claim, removing it breaks K4.3 (claim rewritten), and history removal breaks K4.1. My pick: W3.2 wins, because it is a safety bound. Fixing the wording is EJ's call, so it is listed below.
8. **Nature check (my #6, my #7).** Immune memory gives a close parallel to K4.3: a new variant gets a new memory cell, and the old one is not rewritten. Ant trails give a parallel to W1.1 and W6.1: deposits made without coordination. Both analogies break on decay (pheromones evaporate, and immune memory wanes), which K4.2 rules out. Neither says anything about MUST versus SHOULD, which is a question of who governs, so I dropped the analogy for the levels (my #7).
9. **Control (my #4).** The current way is "no levels", where everything weighs the same. The fair comparison is that against this table, measured on the same run (below), not this table judged on its own.

## What I need to know
- **A secret scanner.** W3.2 says "a secret scanner finds a credential", but none exists. If EJ adds one, W3.2 is a working gate. If not, it is a MUST checked only by a reviewer, which step 5 says is weak.
- **W3.2 versus K4.1/K4.3** (step 7). Does EJ want a written exception, such as "except to remove a credential (W3.2)"? That changes the wording, so it is EJ's decision, not mine.
- **Will a reviewer step exist** in the workflows that use this memory? If yes, W3.4, the W2.2 hypothesis label and Rd5.1 move to MUST. If no, they stay SHOULD.
- **The stop date for the trial below (my #3).** I was not given one and will not invent it.
- **W4.2.** Is the `changed:` line's model ID meant to be exact (for example `claude-opus-5-5`)? The repo's trailers carry "Claude Opus 5.5", a name rather than an ID. If git's trailer is enough, W4.2 could become guidance.

## Costs and risks
- **About 21 of 47 ids carry some MUST part (my #10).** Most of those MUSTs are already enforced by the tool, so they add no new work. The rest (K4.1, K4.3, W6.3, Rd1.2, Rd5.2, Rd5.3, W3.2) need a check that does not exist yet. Until it does, they are promises.
- **Risk of making honesty SHOULD (my #8).** A false "verified" (W3.4), or a guess filed as a fact (W2.2), could be followed by a fresh session without asking (Rd6.1). I accept that risk only while n=0.
- **Rd3.1 numbers (my #10).** The tool's own comment calls 200 lines / 24 KB "the design's example, not a measurement". The gate is real but its threshold is n=0, so it may block wrongly or let through too much.
- **W1.1's MUST currently lets `R-` through (my #9).** Until the tool is fixed, the gate is looser than the requirement.
- **Splitting rows has a cost (my reading).** Fourteen rows carry two levels, so whoever records the levels must do it per clause, not per id.
- **Every level here is a prediction (my #10).** No run has used this memory.

## How we would know I was right
- **Prediction (my #3):** on the first real task that uses `project-memory/`, ending with a fresh-session handoff (Rd6.1):
  - every MUST that fires will be a real defect, not a gate blocking legitimate work;
  - every SHOULD override will have a written reason, and none will have caused harm that a gate would have stopped.
- **Metric:** for each rule broken, record its level, whether a gate would have stopped it, and whether the break did harm.
- **What changes my mind (my #1):**
  - Promote a SHOULD to MUST if a break of it did harm a gate would have caught. The order I would watch is W3.4, then the W2.2 label, then Rd5.1, then Rd2.1.
  - Demote a MUST if it blocked legitimate work twice, or had to be overridden at all.
- **Control (my #4):** for the same run, mark which breaks the "no levels" baseline would also have caught (that is, the tool's existing checks). If this table catches nothing more, the levels added nothing, and I will report that just as plainly (my #9).
- **Stop date:** not set. It goes to EJ.
- **Cheapest first test (my #2):** fix the `R-` prefix in `memory_index.py` and add a git query for K4.1 (deleted entries). Both cost less than debating whether they should be MUST.
