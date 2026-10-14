# Linus Torvalds — MUST versus SHOULD in project memory

## Answer

**My reading:** reserve MUST for identity, safety, data integrity and explicit decision authority; use SHOULD for recording, presentation and retrieval methods. These are recommended levels, not a claim that every gate is enforced today.

| Id | Final level (or clause → level) | Changed from round 1? | Reason (one line) |
|---|---|---|---|
| W1.1 | **MUST:** “It matches the entry's `kind`”; “An entry's kind, and so its prefix, never changes”; “An id never changes, so the file keeps its name”; duplicate ids fail. **SHOULD:** remaining filename and id-generation prescriptions. | No; clarified. | Protect reference identity; the particular date and randomness scheme is method, with collision risk if overridden (my #9, #12). |
| W1.3 | **SHOULD** | No. | Atomic claims aid independent replacement, but sentence counts and headings prescribe a method; overriding them risks ambiguous entries (my #17, #19). |
| W2.1 | **guidance:** definitions. **SHOULD:** “they are written before the code.” | Yes. | Definitions do not establish a new gate; entry-first timing belongs with W5.1/K1.1 and risks retrospectively invented reasons (my #11; my reading). |
| W2.2 | **guidance:** definitions. **SHOULD:** “labelled as one.” | Yes: labelling MUST → SHOULD. | Labelling uncertainty matters, but this judged convention has no assigned gatekeeper; omission risks guesses becoming authority (my #7; my reading). |
| W3.3 | “No raw transcripts” → **SHOULD**; “nothing from another agent's private state” → **MUST**. | No. | Transcript format is method; publishing private state can cause disclosure that retirement cannot undo (my #5; my reading). |
| W3.4 | **SHOULD** | Yes: MUST → SHOULD. | Evidence discipline is essential, but the supplied rule lacks an assigned verification gate; false labels risk downstream reliance (my #2, #7). |
| W3.5 | **SHOULD** | No. | Scope and home-folder placement are conventions; actual sensitive content remains subject to W3.2 regardless of location (my #13; my reading). |
| W4.1 | **guidance:** permission, no owner, no approval. “`status` is only `active`, `superseded` or `retired`” → **MUST**; reader exception → **MUST**, as Rd5.3. | No. | Unknown status breaks lifecycle interpretation; reader authority is explicitly limited, at the price of waiting on contradicted work (my #9; my reading). |
| W4.2 | **SHOULD**, including “Earlier lines are never edited.” | Yes: earlier-line MUST → SHOULD. | Editing an in-file log misleads current readers, but git retains its previous content; it does not itself destroy published history (my #11, #12). |
| W5.1 | **SHOULD** | No. | Timing prescriptions are methods; late recording risks losing corrections or unfinished state, especially at an abrupt cutoff (my #11, #13). |
| W5.3 | “it is reported, not settled in `done:`” → **MUST**, as Rd5.3; remainder → **SHOULD**. | Yes: separate evidence MUST removed. | Completion bookkeeping needs evidence discipline, but no reviewer is assigned; settling a mismatch would cross EJ’s explicit authority boundary (my #2, #11; my reading). |
| W6.1 | **SHOULD** | No. | Separate files are a concurrency method; an alternative must account for the risk of overwritten or inseparable records (my #9, #13). |
| W6.3 | **MUST:** claim preservation, keeping both sides, and reporting competing supersessions. “A conflict in `INDEX.md` is resolved by regenerating it (K6.3).” → **SHOULD**. | No; conflicts remain open. | Losing a branch’s contribution defeats the no-loss contract; preservation may block a merge until EJ resolves the link conflict (my #12; my reading). |
| K1.1 | **SHOULD** | No. | Entry-first is an order of work; an explained alternative can preserve intent, but creates a temporary mismatch readers must handle (my #11, #13, #19). |
| K4.2 | **SHOULD** | No. | Age alone is weak evidence of invalidity, but forbidding every age-based retirement policy is method; exceptions risk retiring valid knowledge (my #2, #13). |
| K6.1 | “one line per active entry, showing its id, kind and one-line claim” → **MUST**; generation and no hand editing → **SHOULD**. | No. | Index content must match its source; the check cannot distinguish identical bytes produced manually or mechanically (my #3, #9). |
| K6.3 | “with no conflict markers left in them” → **MUST**; merge order and regeneration procedure → **SHOULD**. | Yes: marker exclusion made explicit. | Unresolved merge text is invalid committed input; regeneration is the preferred repair, with manual repair carrying greater error risk (my #9, #19; my reading). |
| Rd2.1 | **SHOULD** | Yes: startup MUST removed. | Four-file loading is a method; standing instructions retain their authority independently, while skipped task state risks duplicated or incorrect work (my #13; my reading). |
| Rd2.3 | “credentials” → **MUST**; “another agent's transcripts” → **MUST** where they expose private state, otherwise **SHOULD**; other exclusions → **SHOULD**. | No; privacy scope clarified. | Disclosure is a safety boundary; bulk-loading categories are imperfect proxies for an actual capacity limit (my #5, #18; my reading). |
| Rd3.1 | Actual strictest loader limit and the check rejecting an oversized index → **MUST**; example figures → **guidance**. | Yes: size rejection in K6 MUST. | The supplied check already rejects oversize output; the capacity bound matters, but its numerical applicability still needs evidence (my #2, #18). |
| Rd4.2 | **guidance** | Yes: SHOULD → guidance. | Grep and cache search are suggested mechanisms; another mechanism needs no special dispensation, but may miss relevant entries (my #9, #13). |
| Rd4.5 | “An agent may read another agent's memory” and example → **guidance**; attribution and treating it as that agent’s memory → **SHOULD**. | Yes: attribution MUST → SHOULD. | Attribution prevents authority confusion, but the specified session check has no assigned reviewer; misattribution remains a serious risk (my #11; my reading). |

## How I decided

1. **My #2 and my #7 — distinguish recommendations from demonstrated enforcement.** My #2, `quoted`: “Talk is cheap. Show me the code.” The COO’s supplied facts establish particular tool rejections and missing checks; they do not establish that workflows invoke those checks or that this memory improves real handoffs. No workflow has used it yet.

2. **My #9 and my #3 — protect the data contract and assess the result.** Duplicate identity, uninterpretable status, an inaccurate index and unresolved conflict markers undermine the stored data. Conversely, a manually produced index can equal the generated one exactly. Rejecting incorrect content does not prove that every production method deserves MUST.

3. **My #5 and my #12 — distinguish disclosure or lost contributions from recoverable edits.** Private-state disclosure cannot reliably be undone by retiring an entry. Dropping a merge contribution violates the preservation contract. Editing a `changed:` line leaves its earlier version in git; my round-1 argument treated these different cases too similarly. Applying the kernel-history rules to memory is **my reading**, not a statement from Linus about this system.

4. **My #11, my #13 and my #17 — preserve useful defaults without turning each method into a gate.** Reasons, uncertainty labels, completion evidence, atomic claims and startup reads remain valuable. The absence of an assigned judged checker, combined with n=0, does not establish a separate blocking necessity for every convention. It also does not weaken an actual confidentiality bound.

5. **My reading — retain EJ’s explicit authority boundary.** The mismatch clauses in W4.1, W5.3 and W6.3 inherit the supplied Rd5.3 instruction. That establishes who may settle the disagreement. It does not make all surrounding bookkeeping mandatory.

6. **My #18 — separate capacity from example numbers.** This item is `attributed`, not established as Linus’s own words. A loader ceiling is a concrete compatibility bound; the supplied 24 KB and 200 lines are examples, not measurements of this project’s current agents. Requiring the size check to reject oversized output specifies its result rather than its implementation.

7. **My reading — requirement-check results for this assessment:**

   | Criterion | Result |
   |---|---|
   | source | **PASS:** recommendations are labelled my reading; requirements and COO facts are supplied in the brief. |
   | one thing | **FAIL for bundled ids:** definitions, permissions, methods and bounds sometimes share one id; the table separates their levels. |
   | unit | **PASS:** the supplied counts identify characters, lines or bytes. |
   | can it fail | **PASS for identifiable bad inputs; FAIL for operational completeness:** judged gates lack an assigned checker and stopping point. |
   | weak words | **FAIL:** “immediately” lacks a precise deadline; illustrative capacity figures cannot fill a missing measured bound. |
   | level | **Resolved as recommendations above:** their deployment is not established. |
   | basis | **PASS for explicit n=0 disclosure; FAIL for claiming measured effectiveness or confirmed loader limits.** |
   | links | **FAIL for the two supplied conflicts:** confidentiality versus immutability, and permitted additions versus preserving both links. |

8. **My #7 — change the recommendation when the evidence changes.** A missing checker alone does not demote a safety rule. Conversely, an existing tool rejection alone does not turn a formatting preference into a justified MUST. W1.3 is an immediate example: the current tool rejects a missing `**Why:**` even though I recommend SHOULD; that mismatch needs explicit resolution before such an override can work.

## What I need to know

- **EJ:** how should W3.2 interact with K4.1/K4.3 when a committed claim contains a credential? If redaction is permitted, preservation needs that exception; otherwise the affected action cannot satisfy both requirements.
- **EJ:** which links may an entry gain under K4.3? If both merge-added links are permitted, W6.3 preserves them; otherwise that merge remains unresolved rather than silently dropping one.
- Who checks each judged MUST, what evidence do they inspect, and which commit, task or handoff do they stop? Until answered, these are recommended obligations with incomplete enforcement.
- What are the confirmed start-file limits for the agents actually used here, and do the configured index limits match them? If confirmed, Rd3.1 has a concrete gate; otherwise its numerical bound remains open.
- What deadline does “immediately” mean for a human correction? Until specified, W5.1 remains a timing default without a precise immediate-write test.

## Costs and risks

- **Identity and index gates — my #9, my #18:** malformed entries and oversized indexes block commits. That costs repair time and may require changing index presentation as memory grows.
- **Privacy and preservation gates — my #5, my #12:** retaining both sides can delay merges; disclosure may require exceptional repair whose authority EJ has not yet specified.
- **Recording defaults — my #11, my #13:** fewer gates reduce procedural burden, but late notes, misleading labels and omitted completion records can damage the next session’s decisions.
- **Search and loading defaults — my #9, my #13:** flexibility permits better retrieval methods, but also permits missed constraints or excessive context.
- **Current tool disagreement — my #2, my #7:** a written SHOULD override does not make the existing parser accept it. The recommendation and implementation must be reconciled explicitly.

## How we would know I was right

**My reading, using my #2, my #3 and my #18:** validate the distinction with concrete bad inputs and real handoffs.

- Duplicate ids, invalid statuses, stale index content and indexes over a confirmed loader limit stop the affected commit.
- A merge either retains both contributions or reports the unresolved conflict.
- A manually repaired index identical to generated output passes the content check.
- A fresh session continues the recorded task and respects its decisions despite an explained method override.
- Privacy and authority violations stop at their assigned boundary.

These are proposed checks, not tests I ran. A checker I design would establish only the conditions it tests; real handoffs are still needed to assess missed constraints, repeated questions and recovery failures.