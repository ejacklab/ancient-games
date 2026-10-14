# 孫子 (Sun Tzu) — which memory requirements are MUST

## Answer

Assign MUST only where failure is silent and unrecoverable: an entry's identity (W1.1), a secret (W3.2), another agent's private state (W3.3), a claim dropped in a merge (W6.3), the record governing the code (K1.1), deletion or rewriting a claim (K4.1, K4.3), the index out of step or carrying conflict markers (K6.2, K6.3), an entry a clone cannot read (Rd1.2), an index that does not fit once the check tests it (Rd3.1), and the check-before-acting family (Rd4.1, Rd5.1–Rd5.3, Rd6.1). Everything that is format, timing, path or search method is SHOULD, and every definition or limitation is guidance — 16 MUST, 23 SHOULD, 7 guidance.

| Id | Level | Reason (one line) |
|---|---|---|
| W1.1 | MUST | The id and prefix are the entry's identity; a duplicate or a renamed prefix/id silently orphans or overwrites an entry, and no link repairs that. |
| W1.2 | SHOULD | The header format is schema; a malformed header is caught and fixed by a reader or lint and the content is not lost, so the shape stays a default. |
| W1.3 | SHOULD | The body sections and the one-claim shape are a default; the immutability they serve is gated by K4.3, and "two claims" is a judged check. |
| W2.1 | guidance | Definitions of decision and fact; the "written before the code" clause is an order rule whose gate lives in K1.1. |
| W2.2 | SHOULD | Which kind a claim is, and labelling a guess a hypothesis, is a default; the five-value enum is enforced through W1.1's prefix match. |
| W3.1 | SHOULD | Not restating code, tests or commit log is a redundancy default; a link takes the place of a copy and nothing is lost. |
| W3.2 | MUST | A leaked credential is unrecoverable and is the clearest safety bound; the secret scanner named in the fails-if is its gate. |
| W3.3 | MUST for another agent's private state; SHOULD for raw transcripts | Copying another agent's private state is a privacy bound; raw transcripts are a volume and provenance default. |
| W3.4 | SHOULD | Calling implemented work "verified" is a truthfulness default, judged by a reader; it costs trust, not the record. |
| W3.5 | SHOULD | Keeping user, agent and project memory apart is a scope default; a mistake can be retired and linked. |
| W3.6 | SHOULD | Linking to docs and keeping procedures as scripts or pages is method; where a procedure lives is a project choice. |
| W4.1 | guidance for no owners or approval; SHOULD for `status` being one of the three | "No owner, no approval" removes a gate and is a design choice, not a gate; an unknown `status` is a schema default a reviewer catches. |
| W4.2 | SHOULD | The `changed:` line is the in-file audit trail, but git already carries who and when, so it is a default rather than the only record. |
| W4.3 | guidance | Relying on git history for non-entry files explains how those files are versioned. |
| W5.1 | SHOULD | When to write is timing; the order that binds is K1.1, and a late entry can still be written and dated. |
| W5.2 | SHOULD | End-of-task lessons, observations and hypotheses are a default; they can be deferred without breaking a guarantee. |
| W5.3 | SHOULD | `done:` is a completion default judged by a reviewer; the test-results clause is the part that carries trust. |
| W6.1 | SHOULD | One file per entry and per session is a collision default; a shared append is a risk, not a lost claim. |
| W6.2 | SHOULD | The branch or worktree is the method for W6.3's outcome; the outcome, not the mechanism, is the bound. |
| W6.3 | MUST | A merge must keep both sides; choosing between two claims deletes one, which is the loss K4.3 forbids. |
| K1.1 | MUST | Changing the code before the entry turns the record into a description of the code and loses the reason, which git cannot restore. |
| K4.1 | MUST | Deletion is the one loss nothing else can repair; the entry must be retired and linked instead. |
| K4.2 | guidance | "Age never expires an entry" explains why there is no TTL; the prohibition on deletion is already K4.1's gate. |
| K4.3 | MUST | Rewriting a claim destroys the audit trail and hides what was believed; a new claim must supersede the old. |
| K5.1 | SHOULD | The journal layout and one-file-per-session rule is a default; the safe terminal harvest is K5.2's job. |
| K5.2 | SHOULD | A missed read can be covered by the next read because the journal persists; only the terminal read approaches a gate. |
| K6.1 | SHOULD | The index being generated with one line per active entry is method; the gate that keeps it true is K6.2. |
| K6.2 | MUST | A stale `INDEX.md` silently misleads the next session, and this is the one requirement with a working tool behind it (`--check`). |
| K6.3 | MUST for no committed conflict markers; SHOULD for regenerating rather than hand-merging | A committed `<<<<<<<` line is silent corruption a reader may act on; regenerating the index is method. |
| Rd1.1 | SHOULD | The folder layout is a tooling default; a moved path breaks tooling visibly, not silently. |
| Rd1.2 | MUST | An entry living only in a database, cache or one agent's store is lost to a fresh clone, and no other rule recovers that. |
| Rd2.1 | SHOULD | Reading the four files at session start is a strong default, but a small task may override it with a written reason. |
| Rd2.2 | SHOULD | The later read times (journals, cache, bodies on demand) are defaults about when, not bounds. |
| Rd2.3 | SHOULD | What a session loads is a context-budget default; the security items it names are already MUST under W3.2 and W3.3. |
| Rd3.1 | MUST if the K6 check tests the size limit; SHOULD otherwise | An index over the strictest limit is silently truncated or dropped, so it must stop the commit once the tool tests it. |
| Rd4.1 | MUST | Editing a covered file without reading its covering decisions is how a rule is broken unknowingly; the `covers` link is the check. |
| Rd4.2 | SHOULD | How to search — grep, or the cache once its trigger fires — is method. |
| Rd4.3 | guidance | Which artifact answers a "why" (the decision entry, or git blame) is advice on where to look. |
| Rd4.4 | SHOULD | Reading superseded or retired entries only by link is a default that keeps the active set clean. |
| Rd4.5 | SHOULD | Naming whose memory you used is a labelling default that stops agent memory being read as project memory. |
| Rd5.1 | MUST | Acting on memory without checking it against the code it points to is the drift the whole design exists to prevent. |
| Rd5.2 | MUST | Memory must never override standing instructions; precedence is a safety bound. |
| Rd5.3 | MUST | A reader who settles a mismatch takes EJ's decision; report-and-wait is the control bound. |
| Rd5.4 | guidance | Naming two cases that are not mismatches explains the scope of Rd5.3. |
| Rd5.5 | guidance | What Rd5.3 cannot catch — a wrong outside-world fact — is a limitation, not a rule. |
| Rd6.1 | MUST | This is the acceptance gate: a handoff that makes the next session ask what `state.md` or a decision already answers has failed. |

## How I decided

1. **my #1** (「不可不察也」, `quoted`) — before assigning a level I listed what each id actually protects: an entry's identity, a secret, a claim, the index, a session's reads. A level is a statement about harm, not about how important the topic feels.
2. **my #2** (「先為不可勝，以待敵之可勝」, `quoted`) — the ids that remove a failure rather than promise to detect it are the unbeatable position: never delete (K4.1), never rewrite a claim (K4.3), never drop a merge side (W6.3), never leak (W3.2, W3.3). They earn MUST.
3. **my #6** (「必雜於利害」, `quoted`) — for every MUST candidate I wrote the harm first: is the loss silent at the time and unrecoverable after? Yes → MUST; detectable or repairable → SHOULD. That is the line I used throughout.
4. **my reading**, from RFC 2119 §6 and the requirement-check skill ("a safety bound earns MUST. A method does not.") — format, timing, path and search method stay SHOULD; definitions and limitations are guidance.
5. **my #8** (「兵聞拙速，未睹巧之久也」, `quoted`; 費留) and **my #16** (「約束不明，申令不熟，將之罪也」, `quoted`) — a MUST no check can fire is a cost with no victory. Today only `tools/memory_index.py` exists, so K6.2 is the one id with a real gate behind it and W3.2's scanner is the second named gate; I did not raise ids merely because they matter.
6. **my #5** (「非利不動」, `quoted`) — I resisted MUSTs whose only effect is to impose a way of working. K1.1 is MUST because it decides whether the record or the code governs; W5.1 is SHOULD because it only sets the moment.
7. **my #13** (「途有所不由…君命有所不受」, `quoted`) and **my #14** (「十則圍之」, `quoted`) — where one id bound several cases I split it and named the part carrying the bound: W3.3, W4.1, K6.3. The branch rule W6.2 is the method for W6.3's outcome, so the outcome is MUST and the method is SHOULD.
8. **my #17** (「策之而知得失之計」, `quoted`) and **my #11** (「必取於人」, `quoted`) — the check-before-acting family (Rd4.1, Rd5.1–Rd5.3) is MUST because it is the only thing keeping stale memory from being acted on; a reader or git is enough of a check when the harm is a rule broken unknowingly.
9. **my #3** (「全國為上，破國為次」, `quoted`) — on the read side, Rd1.2 is MUST because it keeps the record whole across machines and agents; the rest of Rd1 and Rd2 arranges the read, so SHOULD.
10. **my #5 again** (finish it; 費留) — I ended by counting 16 MUST (one conditional), 23 SHOULD, 7 guidance, and required each MUST to name the loss it prevents rather than the value it expresses.

## What I need to know

- Does `tools/memory_index.py` test the Rd3.1 size limit and K6.3's conflict markers, or only build and compare? If not, Rd3.1 and K6.3's marker clause are SHOULD until it does.
- Is a secret scanner actually configured for W3.2, or is "a secret scanner" in the fails-if aspirational? The bound still stands; the gate would have to be built.
- Will a lint over `entries/` exist, and when? W1.1's identity bound and W1.2's shape rest on review until it does.
- Is this project one writer or many? W6.3 is MUST as written for many agents; for a single serial writer I would move it, and W6.2, to SHOULD.
- Who measures the "strictest start-file limit" in Rd3.1, and from which agents? The number is a measurement, not a fixed value.
- Does "the commit, task or handoff does not go ahead" have a real stopping point in this repo (a hook or CI), or is every MUST enforced by a person reading? That answer moves several ids between MUST and SHOULD.

## Costs and risks

- Every MUST is a stopping condition, and with n=0 and almost no tooling most of mine are enforced by a reader's judgment; a MUST that cannot fire teaches readers to ignore the word and dilutes K6.2, the one gate that can fire (**my #8**, **my #16**).
- Marking W4.1 (no owners, no approval) guidance means nothing stops a bad change at the door; the price is placed on git review and Rd5.3 (**my #13**).
- K4.1 as MUST makes a wrong or embarrassing entry permanent; the price is that retire-and-link must be cheap or people will work around it (**my #3**).
- W3.2 as MUST without a scanner is a promise with no gate; the cheap fix is building the scanner before the entry lint (**my #2**).
- The splits (W3.3, W4.1, K6.3) buy precision but lengthen the rule and invite misreading (**my #13**).
- If I have over-MUSTed, the word loses force (RFC 2119 §6); if under-MUSTed, a reader cannot tell which failures matter. My line — silent and unrecoverable — puts 16 of 46 at MUST, and that ratio is my reading, not a measured one (**my #5**).
- W3.4 and W5.3's test-results clause are the two SHOULDs nearest MUST; leaving them SHOULD means a false "verified", or a `done:` with no test result, is overridable (**my #6**).

## How we would know I was right

- Give the 46 ids and these three definitions to two independent readers; if they agree with my MUST set and my guidance set, the line is visible to a reader. Disagreement on a named id is the finding (**my #1**, **my #17**).
- Run one real task through the memory system (n=1) and count how many of my 16 MUSTs actually stopped a commit, task or handoff when they should have, and how many fired when they should not have. A MUST that never fires where it should is misleveled (**my #14**).
- Break the system on purpose — delete an entry, commit a credential, leave a conflict marker, hand-edit `INDEX.md`, change code under an unwritten decision — and record which gate catches each. The ones that catch are MUST; the ones that do not are SHOULD until tooled (**my #17**).
- Read the next fresh session's first question. If it asks something `state.md` or a decision already answers, Rd6.1's gate failed and the design's claim is not yet true (**my #2**).
- Re-measure after the first tool lands: if the entry lint and the size check change which ids can fire, the MUST set should be revisited (**my #11**).
