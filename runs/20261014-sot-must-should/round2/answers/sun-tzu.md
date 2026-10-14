# 孫子 (Sun Tzu) — which of the 22 are MUST and which are SHOULD

## Answer

Fourteen of the 22 carry MUST at the clause where failure is silent and nothing later repairs it, or where `tools/memory_index.py` already stops the commit; the rest are SHOULD defaults or guidance, with the method clauses split out from the bound. Where I write MUST and no checker exists today (W1.3's one-claim rule, K1.1's no-code-without-entry, K6.3's conflict markers, W3.5), I am stating the rule's weight and marking the gate as a build item — not claiming work stops today.

| Id | Final level (or clause → level) | Changed from round 1? | Reason (one line) |
|---|---|---|---|
| W1.1 | MUST for one file per entry, prefix matches `kind`, unique id, and "kind and id never change"; SHOULD for the `DD-MM-xxxxxx-YYYY` form | Yes (was flat MUST) | Identity and uniqueness are gated by the tool, and a changed id or prefix silently orphans links; the date form is method (my #2, #8). |
| W1.3 | MUST for the `**Why:**` line and for one claim per entry; SHOULD for `**How to apply:**`, section order and sentence count | Yes (was flat SHOULD) | The tool already fails an active entry with no `**Why:**`; two claims cannot be superseded one at a time under K4.3, a permanent entanglement (my #2, #6). |
| W2.1 | guidance for the definitions; SHOULD for "they are written before the code" | Refined | Definitions explain terms; the timing is an order whose own gate is K1.1 (my #8; my reading). |
| W2.2 | guidance for the three definitions; MUST for `kind` being one of the five; SHOULD for "a hypothesis is a guess, labelled as one" | Yes (was flat SHOULD) | The five-value enum is enforced by the tool's kind/prefix check; guess-labelling is judged and no reviewer is assigned (my #2, #17). |
| W3.3 | MUST for nothing from another agent's private state; SHOULD for no raw transcripts | No | Private state, once in a shared repo, leaves its owner for good; transcripts are a volume and provenance default (my #2, #8). |
| W3.4 | SHOULD | No | An honesty default, judged; a new entry can correct it, so the loss is not silent (my #2, #6). |
| W3.5 | MUST for no user memory and no agent memory in the project; SHOULD for "both live in the home folder" | Yes (was flat SHOULD) | Once cloned, private memory is out for good — the same confidentiality bound as W3.3; the location is the method (my #2). |
| W4.1 | guidance for "anyone may…, no owner, no approval"; MUST for `status` being one of the three | Yes (status was SHOULD) | A permission cannot fail; the tool already fails any status outside the three (my #2, #16). |
| W4.2 | SHOULD | No | `changed:` repeats what git holds, and an edited earlier line is recoverable from git history — a default, not a gate (my #1, #6). |
| W5.1 | SHOULD | No | Timing is method, and K5.2's journal read covers a session cut off before it; the binding order is K1.1 (my #8, #17). |
| W5.3 | SHOULD for adding `done:`; MUST for "a mismatch is reported, not settled in `done:`" | Yes (was flat SHOULD) | `done:` points at evidence `runs/` and commits already hold; silently settling a mismatch removes the divergence from EJ (my #2, #6, #13). |
| W6.1 | SHOULD | No | File-per-entry is the means; the no-loss outcome it serves is gated by W6.3 (my reading). |
| W6.3 | MUST for "keeps both sides; nobody chooses between two claims"; SHOULD for regenerating `INDEX.md`; the "both links" clause depends on the K4.3/W6.3 conflict | No (MUST kept) | A merge that drops a side loses a claim with no trace; regeneration is method (my #2, #6). |
| K1.1 | MUST for "no commit changes governed behaviour with no entry in the same or an earlier commit"; SHOULD for "change the entry first, then the code" | Yes (was flat MUST) | Code without its entry loses the reason git cannot restore; the clause's own "work that has to go the other way" is a stated override, so the ordering is a default (my #1, #13; RFC 2119 §6). |
| K4.2 | guidance | No | It explains why there is no TTL; any deletion already fails K4.1 (my reading). |
| K6.1 | MUST for "one line per active entry, showing id, kind and claim"; SHOULD for "generated, never edited by hand" | Yes (was flat SHOULD) | The tool's `--check` fails an `INDEX.md` that differs from the build or lists a superseded entry as active; generation is the method (my #2, #8). |
| K6.3 | MUST for no committed conflict-marker line; SHOULD for regenerate rather than hand-merge | No (MUST kept) | A committed `<<<<<<<` is corrupt text a reader may act on; regeneration is method (my #2, #6). |
| Rd2.1 | MUST for receiving governing instructions (`AGENTS.md`) and task state (`state.md`) before starting work; SHOULD for the four-file recipe and tool-loading mechanisms | Yes (was flat SHOULD) | Acting before the governing instructions arrive is acting on unknown constraints; the recipe differs by tool and a small task may override it (my #1, #16, #17). |
| Rd2.3 | MUST for credentials; SHOULD for the other five items | Yes (credentials was folded into SHOULD) | Credentials are a safety bound (W3.2); the rest manage context volume (my #2, #8). |
| Rd3.1 | MUST; the 24 KB / 200-line example is guidance | Yes (was conditional on the check) | `memory_index.py` fails an `INDEX.md` over its size limit, and an over-limit index is silently truncated or dropped at session start (my #1, #2). |
| Rd4.2 | guidance for "grep, or the cache" | Yes (was SHOULD) | Nothing fails when a third search method is used; the operative default is to search before relying (Rd4.1/Rd5.1) (my #8). |
| Rd4.5 | guidance for "may read another agent's memory"; SHOULD for "says whose it is — the agent name and the tool" | Yes (was flat SHOULD) | A permission cannot fail; attribution is a labelling default a reader can correct (my #2, #6). |

## How I decided

1. I start from **my #2** (make yourself unbeatable first; you cannot make the enemy beatable). A rule earns MUST when its failure is inside your own hands and silent — nothing later repairs it. A failure a later reader can see and correct is a SHOULD default or an explanation.
2. **My #6** (mix harm into benefit before committing) gave the second test: for each id I asked what is lost on violation, and whether git, a new entry or a reader can get it back. Credentials, private state, a dropped merge side, a deleted claim, a lost reason: not recoverable → MUST. A wrong label, a repeated audit line, a hand-edit that a check would catch: recoverable → SHOULD or guidance.
3. **My #16** (orders clear first, then enforced; an order that cannot be enforced is the general's fault) gave the third test: where `tools/memory_index.py` already fails on the condition — duplicate or empty id, prefix/kind mismatch, missing `**Why:**`, status outside the three, `INDEX.md` differing from the build or over its size limit — the rule has a gate today → MUST. This moved W2.2's enum, W4.1's `status`, K6.1's content and Rd3.1.
4. **My #1 and #17** (reckon before battle; learn by probing and signs) put the readiness rules in the MUST class: governing instructions and task state in hand before work starts (Rd2.1), and a record that carries its reason (W1.3, K1.1). Acting before the reckoning is the waste my #1 names.
5. **My #13** (not every road is taken, not every command accepted) decides the ids that name their own override: K1.1's "work that has to go the other way", W5.1's timing. A rule that writes its own release valve is a default by its own words — that is what SHOULD is — so K1.1's literal ordering dropped from MUST to SHOULD.
6. **My #8** (value victory, not duration; do not buy a gate whose cost exceeds the harm) plus RFC 2119 §6, quoted in the brief, keeps method off MUST: the id form, `**How to apply:**`, the home-folder location, the four-file recipe, the search tool. Where the outcome is gated elsewhere (W6.1 → W6.3, Rd4.2 → Rd4.1/Rd5.1), the mechanism is SHOULD or guidance, not a second gate.
7. **My #14** (choose the action by the ratio of forces) applied to the judged MUSTs: I still call a safety bound MUST and mark the missing check as a build item, because the level says what work must respect. I do not promote a recoverable wrong label to MUST just because it is disliked (W3.4, Rd4.5).
8. On the two conflicts EJ holds: (a) W3.2 against K4.1/K4.3 raises the stakes on every "never loaded" clause (W3.3, W3.5, Rd2.3), because the cheap moment to stop a credential or private state is before it is committed, not after; (b) my W6.3 "both links" clause is MUST only if K4.3 is read to permit a link to be added after the first commit — if not, that clause must go to EJ. I do not settle either.

## What I need to know

1. Will a reviewer be assigned to the judged checks, or is a machine check being built? My MUSTs without a check today — W1.3's one-claim rule, K1.1's no-entry case, K6.3's conflict markers, W3.5, W5.3's settled mismatch — hold only by the writer's discipline until then.
2. How are the two conflicts EJ holds to be settled — may a credential be expunged from an entry by rewriting it (raises W3.2/W3.5), and does K4.3 permit a link to be added after an entry's first commit (decides my W6.3 "both links" level)?
3. Is the memory system in force, or still a draft (n=0)? If no entry has been written, these levels bind nothing yet and the missing scanner and reviewer are not yet live risks.

## Costs and risks

- A MUST with no checker buys nothing today and can read as enforced when it is not; the price is false confidence in the wall (my #2).
- The twin error — lowering a bound to SHOULD because the check is missing — invites the exact harm the bound exists to stop (my #6).
- Splitting fifteen ids by clause multiplies the lines a reviewer must carry; the price is upkeep, weighed against speed (my #8).
- Keeping W3.4, W4.2, W5.1 and W6.1 at SHOULD means each override needs a written reason; if writers do not write it, the defaults become unobservable and this round's work cannot be measured (my #16, #17).
- Marking K6.3's markers and K1.1's missing entry MUST while no check sees them is relying on the enemy not attacking — the one thing my #2 forbids (my #2).

## How we would know I was right

Run `tools/memory_index.py --check` on a branch where each MUST condition is violated in turn and confirm the commit fails for the ones I marked enforced (W1.1 id/prefix, W1.3 `**Why:**`, W2.2 enum, W4.1 `status`, K6.1 content, Rd3.1 size). For the judged MUSTs, have the first reviewer over the first 20 entries count how many of W1.3's two-claim, K1.1, K6.3-marker and W3.5 cases are caught; if none is ever caught, those MUSTs are paper gates and each should be checked or lowered. That is my #17 (read the signs) turned on the rules themselves.
