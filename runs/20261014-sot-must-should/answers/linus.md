# Linus Torvalds — Levels for source-of-truth memory

## Answer

**My reading:** Reserve MUST for preserving identity, evidence, confidentiality, authority boundaries and a usable handoff; make the prescribed writing, storage and reading methods SHOULD, and explanations guidance. Several ids combine these levels, so they cannot honestly receive one level as written; the table identifies their parts without changing their wording.

| Id | Level | Reason (one line) |
|---|---|---|
| W1.1 | Mixed: MUST / SHOULD | MUST keep identity and kind stable and unambiguous; SHOULD use the prescribed filename and random-id scheme—the former protects references, the latter is method (my #9, #12). |
| W1.2 | SHOULD | Header syntax and field layout are a serialization method; deviations cost parser compatibility and need a recorded reason (my #9, #13). |
| W1.3 | SHOULD | One claim and the prescribed sections aid review, but their sentence count and spelling are editorial methods (my #11, #17). |
| W2.1 | Mixed: guidance / MUST / SHOULD | Definitions are guidance; respecting governing constraints is MUST; recording them before code is SHOULD sequencing (my #3, #11). |
| W2.2 | Mixed: guidance / MUST | Kind definitions explain the vocabulary; labelling a guess as a hypothesis is MUST to prevent uncertainty becoming asserted truth (my #2, #7). |
| W3.1 | SHOULD | Avoiding code-derived content reduces duplication, but a justified summary need not stop work (my #13, #17). |
| W3.2 | MUST | Committing credentials or sensitive data can cause harm that reverting the commit cannot undo (my #5; my reading of confidentiality). |
| W3.3 | Mixed: SHOULD / MUST | Avoiding raw transcripts is a content method; excluding another agent’s private state protects a confidentiality boundary (my #5; my reading). |
| W3.4 | MUST | Calling implementation verified gives subsequent workers evidence they do not have (my #2). |
| W3.5 | SHOULD | Separating project, user and agent memory is a useful storage convention; the home-folder location is method (my #9, #13). |
| W3.6 | SHOULD | Links, scripts and procedure listings reduce competing copies, but prescribe how knowledge is maintained (my #11, #13). |
| W4.1 | Mixed: guidance / MUST | Open writing and no ownership or approval describe EJ’s standing permission model; valid lifecycle states and the reader exception are MUST boundaries (my #9, #14; my reading). |
| W4.2 | Mixed: SHOULD / MUST | SHOULD add the per-change record; MUST leave earlier records intact, so an audit trail cannot silently change meaning (my #11, #12). |
| W4.3 | guidance | This explains where history comes from rather than introducing another action gate (my #12). |
| W5.1 | SHOULD | Immediate recording and entry-before-code are timing methods; their exceptions risk forgotten corrections or incomplete handoffs (my #11, #13). |
| W5.2 | SHOULD | Task-end recording is a batching default, with the cost of losing useful knowledge if postponed (my #11, #13). |
| W5.3 | Mixed: SHOULD / MUST | Completion bookkeeping is SHOULD; truthful evidence and reporting a divergent result without settling it are MUST (my #2, #11). |
| W6.1 | SHOULD | Separate entry and session files reduce contention, but prescribe a particular concurrency method (my #9, #13). |
| W6.2 | SHOULD | Branches and worktrees are an isolation method; the essential protection is against lost edits (my #12, #13). |
| W6.3 | Mixed: MUST / SHOULD | MUST preserve both sides and report competing replacements; regenerating the index is SHOULD merge procedure (my #9, #12). |
| K1.1 | SHOULD | Entry-first ordering is workflow method; a deliberate transition can temporarily put entry and implementation out of step (my #13, #19). |
| K4.1 | MUST, with an unresolved conflict | Preserving bodies and replacement links protects historical references; absolute retention conflicts with removing accidentally stored sensitive content (my #5, #12). |
| K4.2 | SHOULD | Age is a poor substitute for checking applicability, but forbidding every age-based retirement policy is method (my #2, #13). |
| K4.3 | Mixed: MUST / SHOULD | MUST keep the committed claim immutable; the exhaustive list of permitted metadata changes is SHOULD and conflicts with W6.3’s added links (my #9, #12). |
| K5.1 | SHOULD | Journals, their paths and their append-only format are a chosen capture method, with storage and maintenance costs (my #11, #13). |
| K5.2 | SHOULD | Reading, promoting and logging journal material is a handoff method; successful continuation is the outcome gate (my #3, #11). |
| K6.1 | Mixed: MUST / SHOULD | MUST accurately represent active entries; generating rather than editing the index is SHOULD implementation method (my #9, #13). |
| K6.2 | SHOULD | Regeneration frequency, tooling and commit scheduling prescribe how to achieve the index consistency required by K6.1 (my #13, #19). |
| K6.3 | SHOULD | Regeneration is the preferred merge repair; a correct result matters more than how it was produced (my #3, #13). |
| Rd1.1 | SHOULD | The directory tree and instruction-import arrangement are layout methods, with compatibility costs if overridden (my #9, #13). |
| Rd1.2 | MUST | Clone-alone readability is the promised interface for another session; private or service-only entries break it (my #1, #3). |
| Rd2.1 | Mixed: MUST / SHOULD | MUST receive governing instructions and task state before acting; the four-file startup recipe and loading mechanisms are SHOULD methods (my #3, #13; my reading). |
| Rd2.2 | SHOULD | Deferring material until its useful reading time is a context-management default (my #13). |
| Rd2.3 | Mixed: MUST / SHOULD | Credentials and private transcripts require MUST exclusion; bulk-loading and link-only history restrictions are SHOULD context methods (my #5, #13; my reading). |
| Rd3.1 | Mixed: MUST / SHOULD / guidance | A measured loader limit is MUST; coupling its check to K6 is SHOULD; illustrative sizes are guidance (my #2, #18). |
| Rd4.1 | SHOULD | Reading covering entries before editing is the default discovery method; exceptions risk missing governing decisions (my #11, #13). |
| Rd4.2 | SHOULD | Text search and a triggered cache prescribe retrieval mechanisms, whose benefit needs measurement (my #9, #18). |
| Rd4.3 | guidance | This is navigation advice about where explanations can be found (my #11, #12). |
| Rd4.4 | SHOULD | Following links is a useful history-reading default, but direct historical investigation need not stop work (my #12, #13). |
| Rd4.5 | Mixed: guidance / MUST | Permission and the example are guidance; attribution and keeping agent memory distinct from project authority are MUST (my #11; my reading). |
| Rd5.1 | SHOULD | Comparing memory with referenced repository evidence is a checking method with real reading cost and incomplete coverage (my #2, #18). |
| Rd5.2 | MUST | Stored text cannot acquire authority over standing instructions merely because it was retrieved (my #9; my reading of the authority boundary). |
| Rd5.3 | Mixed: MUST / SHOULD | MUST stop reliance on the contradicted part and leave settlement to EJ; report location, format and continuing other work are SHOULD methods (my #4, #11, #14; my reading). |
| Rd5.4 | guidance | These are scope explanations for the mismatch rule, preventing expected implementation work from becoming a false alarm (my #3, #19). |
| Rd5.5 | guidance | This states the check’s limits and EJ’s position; it adds no independent gate (my #2, #7). |
| Rd6.1 | MUST | A usable fresh-session continuation is the design’s promised outcome; failure means the handoff is incomplete (my #3, #11). |

## How I decided

1. **Start with the user’s outcome — my #3.** The distinction is whether a violation breaks EJ’s workflow or breaches a safety boundary. A different filename convention, search tool or recording schedule does not establish that by itself. Applying this kernel rule to memory is **my reading**, not a quoted Linus position on this design.

2. **Protect references and shared history — my #9 and my #12.** Stable identities, immutable claims, honest evidence and preserved merge contributions let another reader understand what happened. Formatting and generation mechanisms serve those protections; they do not automatically inherit MUST.

3. **Keep irreversible harm behind gates — my #5.** Confidentiality failures deserve MUST because deleting a leaked credential afterwards does not recover confidentiality. Extending that rule to private agent state is **my reading**.

4. **Avoid making EJ the routine throttle — my #4 and my #14.** W4.1’s open writing model stands. Rd5.3 is a narrow exception for settling an identified contradiction, and blocks reliance on the contradicted part; it does not introduce approval for every write.

5. **Treat untried methods as defaults — my #13 and my #18.** This design has n=0. Journals, startup loading and index regeneration may work well, but no supplied measurement establishes their effectiveness or cost. My #18 is labelled **attributed** in the list: it is kernel documentation, not established as Linus’s own words.

6. **Check the requirements before declaring them complete — my reading, using requirement-check.** Source **PASS**: the brief identifies the design and EJ’s confirmations. One thing **FAIL** for the mixed rows. Unit **FAIL** operationally for Rd3.1 until actual loader limits are known. Can it fail **PASS** for the stated judged and mechanical checks, although those checks are not all implemented. Weak words **FAIL** where scope remains open, particularly sensitive data and journal material worth keeping. Level **FAIL** for ids that need more than one level. Basis **PASS** as an explicitly untried design, not measured effectiveness. Links **FAIL** where K4.3’s permitted edits do not accommodate W6.3’s added links.

7. **Distinguish a recommendation from an implemented gate — my #2 and my #7.** The supplied facts establish only that `tools/memory_index.py` exists. They do not establish an entry lint, comprehensive startup enforcement or a successful handoff. These levels are advice for EJ; enforcement and effectiveness remain **not measured**.

## What I need to know

- Which participating agents and measured start-file limits determine Rd3.1? If exceeding a limit prevents complete loading, that boundary is MUST; the example cannot supply it.
- Does K4.3 permit adding the links W6.3 requires? If yes, its metadata list is incomplete; if no, the merge instructions conflict.
- What does EJ include in sensitive data, and what happens if it is already committed? If removal requires changing or deleting an entry, W3.2 and absolute K4 retention need an explicit resolution.

## Costs and risks

- **My #5 and my #12:** Preservation gates protect history but retain obsolete material and can obstruct removal of sensitive content; that conflict remains open.
- **My #11 and my #13:** SHOULD methods allow justified exceptions, but cost consistency and require someone to read the recorded reasons.
- **My #4 and my #14:** Human mismatch settlement costs EJ attention and can delay the affected work; keeping its scope narrow limits that price.
- **My #2 and my #18:** Checking applicability and proving handoff usability costs reading and experimentation. No productivity gain has been measured.
- **My #7:** Overly broad MUST labels can stop useful work on formatting failures; overly weak labels can let a misleading record reach the next session.

## How we would know I was right

**My #2 and my #3:** Observe a real handoff to a fresh session using only a clone and task id. It should identify the next step, retrieve the governing decisions, distinguish hypotheses from established evidence, and continue without asking questions already answered in memory.

Try violations of the proposed gates: a duplicate identity, rewritten committed claim, falsely verified result, lost merge contribution, credential, stale active-entry index and known decision/code contradiction. Each should prevent the affected commit, reliance or handoff.

Try justified method exceptions separately. If a different retrieval or recording method preserves the required outcomes, a method-level failure should not block it.

**My #18; my reading:** Record loading completeness, repeated questions, missed decisions, lost edits and time spent maintaining memory. These are proposed observations, not supplied thresholds. Any checks I devise would be my checks: passing them would show that those cases were handled, not independently prove the whole design works.