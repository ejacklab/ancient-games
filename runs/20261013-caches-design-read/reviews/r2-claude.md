# Round 2 — reader: claude

I read all four round-1 reports, and reopened the snapshot `inputs/CACHES.md` and the sources each point depends on.
Line numbers are the snapshot's. All positions below are *my reading* of the quoted lines, unless a line is marked
otherwise.

### Points I now support

**Points I missed in round 1 that hold:**

- **agy 4, `CACHES.md:93`. Proving absence cites V-F20, which is about negation, not absence.** It holds. Source:
  `vector.claude.md:233`, *"F20 (CONFIRMED) Negation is a documented weakness of bi-encoders"*, against `:259`,
  *"F23 (CONFIRMED) Top-k cannot enumerate or prove absence … 'cannot enumerate a complete set, establish an
  absence'"*. Low. Fix: cite V-F23 (and V-F1).
- **codex 5, `CACHES.md:549-550`. "K2 (stale never answers) matters more here."** It holds. K2.1 (`:395`) compares
  the index's recorded hash with the entry files. SEZA's failure was outdated *content* in a hand-kept index, which a
  faithful hash check passes. CX `codex.md:341`: *"a faster search index would still return outdated information
  unless memory maintenance and source checking addressed it."* Only the second SEZA item, the missing graph, is a
  cache matter, and it is Rd3, not K2. Medium. Merge this with the "three stores" fix on the same line.
- **codex 6, `CACHES.md:518`. "On tokens read, full-text wins much earlier: on SEZA-sized memory…"** It holds. The
  only SEZA measurement says the opposite at memory-folder size and gives no verdict. `seza.md:337`: *"So at 55
  entries full-text did not read less than the index plus grep … n=5, no verdict."* `seza.md:349` adds that the
  reading path was not measured. The "my reading" label does not save a sentence that its own row's source
  contradicts. Medium.
- **codex 7, `CACHES.md:526`. W-18 is labelled "instead of retrieving".** It holds. `web.md:110` compares *"oracle
  (only the right sessions) against S (everything)"*, which is not a retrieval route. Low to medium. (For `:535`, see
  Points I reject.)
- **codex 10, `CACHES.md:484, 487`. "Instructions plus index under 32 KiB / 64 KiB."** It holds, low. CX's own
  caveat, `codex.md:444`: *"Codex's instruction cap and DSH's instruction-loader byte budget apply if an index is
  placed in that instruction chain. An ordinary subsequent file read … is not thereby governed by the same loader
  cap."* The Example column drops the "if".
- **codex 12 and opencode 4, `CACHES.md:240-242, 273-276`. Measured here carries neither the snapshot warning nor
  the rg overhead.** It holds, low. `build.opencode.stdout.md:68`: *"these numbers are a snapshot of a corpus in
  motion. Re-run before the tables are used."* `audit-0.json:93-95`: *"rg's measured seconds include a `git ls-files`
  subprocess … rg's seconds are about 16% high."* B1.1 (`:317-318`) now adopts "the code-and-docs benchmark" as its
  method, so the caveats belong beside the numbers, not only in the Unresolved table.
- **codex 15, `CACHES.md:145-147`. The hash procedure is cited to S-F9.** It holds, low. `sqlite-fts.claude.md:80`,
  S-F9: *"compares the index build time with the newest source mtime"*. `:89`, S-F11: *"Change detection: SHA-256 on
  files and chunks."* K1.1 and K2.1 already split the two citations this way.
- **codex 17, `CACHES.md:561-562`. "All evidence is on other corpora: source code, chat memory, enterprise
  documents."** It holds, low. The list leaves out SEZA's markdown memory (`seza.md:245`, *"five questions taken from
  SEZA memory entries or docs"*), which the document itself uses at `:515` and `:538-540`. The gap is real but
  narrower: nothing has been measured on this design's `entries/`.
- **codex 4, Rd4.1 with K3.1 (`:411`). Noted misses outlive their target entries.** It holds as a gap, but low, not
  medium. B4.1 (`:371`) indexes active entries only, so a miss whose target was later superseded can be found by
  neither route. Under B1.2's test (*"finds an entry that full-text missed, and loses nothing"*, `:330-331`) that
  miss counts for neither side. It can make the cache look as if it stopped paying only when every noted miss is
  stale. A one-line rule (judge a miss against its target, or the target's active successor) closes it.
- **codex 1, K2.3 (`:402`). "The full-text and vector indexes are rebuilt by one command, in one step."** The point
  holds: the sentence is unconditional while B1.2 (`:343-344`) builds vector only after full-text. Fix: "when both
  exist". Severity: see Points I reject.
- **opencode 8, Rd3.4 (`:446`). "(G-F5, failure mode 5)".** It holds, low. The provenance note (`:28-29`) says the
  node uses F5 twice. Failure mode 5 is in the drift study (`code-graph.opencode.stdout.md:186` drift study, `:218`
  failure mode 5; Serena is `:158`). The Rules bullet (`:150`) already says `G-F5 drift`.
- **opencode 10, `CACHES.md:233`. "results in `bench/results.md`, ids `BM-*` below".** It holds, low. `results.md`
  has no `BM-` ids. Its sections are Build, Determinism check, and Category A–E (checked with grep). BM-7 comes from
  `nodes/runtime-recall.json` and BM-9's suite timing from `state.md`, so the ids are this document's own labels over
  several files. Say so once.
- **opencode 11, `CACHES.md:97` (M17) and `:438` (M6). CONTESTED ids cited bare.** It holds, low.
  `RECOMMENDATION.md:46`: M17 *"CONTESTED (opencode: …)"*, and `:55`: *"M17 is CONTESTED, not MAJORITY"*. B2
  (`:352-353`) discloses M6's status. The other two places do not.
- **opencode 13, `CACHES.md:98`. "A map of the whole repo … M18, G-F18".** It holds, low. G-F18 is the in-repo tool's
  stdout-only determinism (`code-graph.opencode.stdout.md:181`), not a repo map. The run record's row
  (`DECISION-RULES.md`, "Give me a map of the whole repo") cites *"M18, G-F12, G-F7b, s3-F24"*.

**Points other readers raised that match my own, and still hold:**

- **agy 1 and codex 3 (my 1):** `:148-149` against Rd3.3 `:442`.
- **codex 2 and opencode 3 (my 2):** B1.1's journal note against Rd4.1's *"Every other question goes unrecorded"*.
- **agy 5 and opencode 2 (my 3):** K3.2 gives full-text B1.2's events.
- **codex 11 and opencode 12 (my 4):** "all six stay open" at `:117`.
- **codex 13 and opencode 5 (my 5, second half):** the `INDEX.md` 0.01 s figure cited to `SOURCE_OF_TRUTH.md`. D4
  (`DECISION-RULES.md`) records it as opencode's and unresolved.
- **agy 6 (my 6):** the start-load subsection under a "comparisons" introduction.
- **agy 2, agy 3, codex 16 and opencode 1, opencode 7 (my 7):** "three caches" `:54`, "three stores" `:550`, and the
  header note at `:44-47`.
- **codex 8 (my 10):** Cursor's 12.5% and the 1,000-file condition.
- **codex 9 (my 11):** V-F6 and V-F7 cited as memory-style evidence.
- **codex 14 and opencode 6 (my 12, first item):** "the same set as `INDEX.md`" `:152`, against B4.1 `:373`.

### Points I reject

- **codex 1, the severity "high" for K2.3.** No reader can build a vector index from this line. B1.2 (`:343-344`,
  *"it is built only after B1.1 has fired"*) and B5.1's example (`:381`, *"the full-text path still works"*) both say
  otherwise, and K2.3's own *"If either fails"* presupposes two indexes. It is a wording gap: low.
- **agy 1, the severity "high" for `:148-149`.** The finding holds, but medium is better supported. The Rules line
  is labelled *"my reading"*, while Rd3.3 is the requirement and carries the Fails-if (`:448-449`), so the
  requirement governs a conflict. The fix is the same at either severity.
- **codex 7, the `:535` half.** *"It is keyword retrieval that wins"* does not rest on W-19. It rests on the W-22 and
  V-F4 rows of the same table (`:529-530`). `web.md:142`: *"Dense was the lowest at every size"*. `web.md:151`:
  *"BM25 68.8 / vector 51.4"*. The sentence is labelled my reading, and its keyword half is sourced. Only W-18's row
  label (above) misleads. A tidy fix splits the sentence by source, but it is not a defect.
- **opencode 9, `:143` and `:366`. `G-F5 drift` needs the vision's "a study of a code-graph tool" label.** Not
  misleading. The provenance note (`:26-28`) says that `G-F*` ids come from the code-graph node. The cited line itself
  says *"4.3% of edges wrong"* (`:142-143`), and edges are graph language. Repeating the vision's parenthetical would
  be a second copy.
- **opencode, Unresolved row 3: the vector-deduplication finding "explains the very top-5 measure B1.1 and B1.2
  adopt".** The audit says otherwise. `audit-0.json:52`: *"vec returns 9.28 paths on average (… the minimum is 7) …
  The hit@5 tables do not change."* With at least 7 paths returned, top 5 is never short. codex's reading of that
  finding is right. (opencode's broader claim, that some low findings bear on the text, still holds. See the
  Unresolved table.)
- **opencode 2's framing**, that a miss is "the circular event the change to B1.1 just removed". K3 applies only to a
  built cache, so for full-text a miss is definable. The defect is relevance, not circularity: a miss says nothing
  about full-text against grep. The fix is the same.

### My own points: held or withdrawn

1. `:148-149` against Rd3.3: **held**, medium.
2. B1.1's journal note against Rd4.1: **held**, medium. codex and opencode found it independently.
3. K3.2 gives full-text the wrong rerun events: **held**, medium. agy and opencode found it independently.
4. "All six stay open": **held**. D6 is settled by B1. D5 is settled by `SOURCE_OF_TRUTH.md` K6.1 (*"id, kind and
   one-line claim"*). D1 is answered as *proposed* by B1.2. D2, D3 and D4 stay open.
5. Costs at `:101-105`: **held**, with the first half lowered to low. The line already discloses *"opencode's figure,
   and D3 records …; S-F4 measures other corpora"*. What remains is that S-F13 measured no tokens
   (`sqlite-fts.claude.md:107`) and that S-F4's set-up is a grep-and-read agent, not "grep plus opening every hit". The
   `INDEX.md` 0.01 s half stays medium-low: all three readers agree.
6. The Example numbers introduction against the start-load subsection: **held**, low.
7. Leftovers: **held** for `:54`, `:550` and `:44-47`. **Withdrawn** for `:291-294`, test selection. That section is
   kept as code-and-docs evidence by decision (`:60-61`, `:135-136`), and the sentence reads that evidence correctly.
8. "The B1.1 question set" in B1.2 against Rd4.2: **held**, low.
9. The `INDEX.md` arm has no defined top 5: **held**, low.
10. Cursor's +12.5% at 1,000+ files: **held**, low (codex agrees).
11. Vector why 5 cites code and chunk-RAG studies as memory-style evidence: **held**, low (codex agrees).
12. Small mismatches: `:152` **held** (codex and opencode agree). Vector why 4's miss definition: **withdrawn**; its
    first sentence, *"because their words differ from the entry's"* (`:208`), carries the meaning, and the paragraph
    ends at B1.2. `:224`, "favours", without B1.0: **held**, low. `:89`, the vector row's fallback without full-text:
    **held**, low.
13. Rd4.1 names one `journal/`, while SOURCE_OF_TRUTH K5.1 has two: **held**, low.
14. The vector How row points to option A, whose rebuild is per-hash (`vector.claude.md:292-293`): **held**, low.
15. `INDEX.md` in two "none" rows: **withdrawn for `:92`**, whose route already includes *"and entry headers"*.
    **Held for `:94`**: *"`INDEX.md` scan or a script"* offers `INDEX.md` as an alternative for `supersedes` and
    `depends_on`, which K6.1's line does not carry.

### Unresolved table

- **The BM-9 speed bound and the `git ls-files` overhead: settled as a dispute.** The only open part is a disclosure.
  The audit decides the dispute: `audit-0.json:95`, *"rg's seconds are about 16% high. fts … is faster either way, so
  the speed winner does not change."* Removing the overhead lowers grep's time, so the 15 ms bound holds (codex's
  position). opencode's "undercuts BM-9" is not supported. agy is also right that no requirement now uses time (B1.1
  compares characters and misses, and K3's cost part is gone). What remains is the half-sentence disclosure (codex
  12, opencode 4). Once it is added, the row can go.
- **Corpus snapshot stability: still open.** All four readers agree. The run log records one later run on the
  repaired harness (`state.md`: *"node 3 run once on the repaired harness … determinism 180/180"*). `results.md` shows
  4,021 chunks, against the builder's 4,016→4,017, so it was a different run. Nothing records that the corpus held
  still during it. Determinism (180/180) shows that the harness is repeatable, not that the snapshot was stable. B1.1
  borrows this method, so the warning should be carried.
- **The audit's lower-severity findings: still open, but narrow.** Nine are low (`audit-0.json`). One is *"No problem
  found"*. The deduplication finding changes no hit@5 (codex right). Graph's two-question row is already disclosed
  (`:260`). Two touch numbers in the text: rg's seconds (BM-9) and the hybrid block (`audit-0.json`: *"Small effect
  on hybrid's output_chars and chars_to_first_gold"*, which bears on BM-1–BM-6's hybrid column). So opencode's "some
  bear on the text" holds through those two. A recorded disposition per finding would close the row.
- **Discovery versus exhaustive routes in the "none" rules: settled**, by the rule at `:81-84` and the table. The
  free-text and find-by-meaning rows go to a cache once its trigger fires (`:88-89`). Completeness and absence stay
  files-only (`:92-93`). That is codex's position, so opencode's "rows unchanged" is true, but the rule above them
  settles the dispute. codex's remaining worry, that the "why" row (`:95`) hides a discovery step, does not hold. The
  row answers from *"the entry's **Why:**"*, so it starts from a found entry, and finding one is row `:88`. My `:94`
  point (held above) is a route-correctness item, not this dispute.
