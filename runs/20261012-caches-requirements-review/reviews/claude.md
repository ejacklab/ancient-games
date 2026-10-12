# Review — memory caches core requirements (Claude reviewer, `claude-opus-5-5`, 2026-10-12)

Line numbers are from `runs/20261012-caches-requirements-review/inputs/CACHES.md`, which is byte-identical to the live
`docs/memory-system/CACHES.md` (checked with `diff -q`). Evidence ids were opened in their source files; where a claim
below is my inference it says *my reading*.

### Verdict

REPAIR. The Build / Keep / Read structure and most of the Read and Build-mechanics checks are sound. The two triggers
the whole layer depends on are not: B1.1 and the full-text 5W1H name different triggers, K3 now compares a rebuild's
cost in a unit (characters read) that cannot see it, and B1/K3 rest on a question record (Rd4) that cannot produce a
full-text miss before full-text exists and records no search terms to replay.

### Findings

**1. B1.1 against CACHES.md:209, :70–71, :193 and the vision. Two different triggers for full-text.** High.
- B1.1 (l.366–368): *"built only when, on the project's own recorded questions (Rd4), full-text reaches the right
  entry after reading less than `INDEX.md` plus grep does, with no more misses."*
- Full-text 5W1H, **When** (l.209): *"Built when the trigger fires: `INDEX.md` can no longer list every active entry."*
- Part 1 rule (l.70–71): FTS5 is for a question *"once `INDEX.md` can no longer list every active entry under its
  size limit **and** ranked results with snippets save opened files"*.
- Vision: *"Too many entries — full-text search. `INDEX.md` can no longer list every active entry under its size
  limit"* … *"The caches exist to keep finding the right entry cheap when that happens — and not before."*

B1.1 drops the `INDEX.md` overflow condition. By B1.1 alone, full-text can pass while `INDEX.md` still fits (on the
code-and-docs benchmark full-text already printed about a sixth of grep's characters at 490 files, BM-6), which is the
"before" the vision rules out. *My reading:* the vision makes overflow the condition and the comparison the proof.
**Fix:** either make B1.1 "INDEX.md has reached its size limit (SoT Rd3.1) **and** the comparison passes", or change
l.209, l.70–71 and five-whys 4 (l.193) to the comparison. This is EJ's choice; do not keep both.

**2. K3.1 — the cost of a rebuild is added in a unit that cannot count it; R8.2's meaning changed under "was R8.2".**
High.
- K3.1 (l.440–441): *"its B1 comparison is rerun on the recorded questions (Rd4), and a query's cost includes any
  rebuild it triggered (K2)"*. B1's measure is *"the characters read to the first right entry"* (l.368).
- A rebuild prints nothing into the agent's context, so in characters it costs zero: the clause cannot change the
  outcome. The accepted R8.2 compared time with time (diff l.209–210: *"its time is compared with the reading time the
  cache saved"*); K3 says "was R8.2" but now compares something else.
- The example section for K3 is still in seconds (l.568–579: *"K3: rebuild cost"* … *"So K3 starts to bite with
  corpus size and with a slow embedding model"*), which only makes sense under the old R8.2.
- The per-query staleness check of K2.1 (hashing every entry file before each answer) is a cost no requirement counts.

**Fix:** say what unit K3 compares. If it is characters read (B1), drop "includes any rebuild" and retitle the example
table; if rebuild time matters, K3 needs a second comparison in time, and that is EJ's call (not a number).

**3. Rd4.1 / B1.1 — a "miss" cannot be recorded before full-text exists, so B1.1's rerun event never fires.** High.
- Rd4.1 (l.478–480) and B1.2 (l.379–380) define a miss as: *"an entry existed, `INDEX.md`, grep and full-text search
  all missed it, and it was found another way"*.
- B1.1's rerun (l.373–374): *"It is rerun when an agent records a miss, and when EJ asks"*.
- Before the full-text cache exists no agent can try full-text, so no record can meet the definition. *My reading:* B1.1
  then reruns only when EJ asks, and nothing tells EJ that the corpus has grown. B1.1 also uses "misses" (*"with no more
  misses"*, l.368) to mean "a route did not reach the right entry", a second meaning of the same word.

**Fix:** give B1.1 its own rerun event that can happen before full-text exists (for example, `INDEX.md` reaching its
SoT Rd3.1 limit, which the build already checks), and rename B1.1's "misses" to something like "unanswered questions".

**4. B1.1 "measured as the code-and-docs benchmark was" — the benchmark cannot be replayed from the Rd4.4 record.**
Medium-high.
- `runs/20261012-caches-routing/bench/results.md` l.6: *"a route may read: question, terms, symbol, file"*; the
  `README.md` there: rg and FTS run on the pre-written `terms`, rg is ranked (*"distinct terms matched, then match
  count per file"*) and capped (*"at most 10 paths per answer … rg output capped at 40 lines"*).
- Rd4.4 (l.486–488) records *"the question as asked; the routes tried … the entry that answered it"* — no search terms
  or query string per route.
- The benchmark has no `INDEX.md` route at all; B1.1's baseline is *"`INDEX.md` plus grep"*.

So "measured as BM-1 to BM-9" names a harness whose inputs Rd4 does not record and whose baseline is a ranked, capped
rg, not `INDEX.md` plus grep. **Fix:** add the terms or query each route ran to Rd4.4, and state in B1.1 how the
`INDEX.md` step and the grep step are run in the replay (and who picks the terms). Cite only BM-1 to BM-6; BM-7 to
BM-9 are test impact and speed.

**5. B1.1 / B1.2 — "reaches", "less", "no more than" have no aggregate, and the "right entry" is self-graded.** Medium.
- B1.2 defines **Finds** as *"in the top 5 results"* (l.381); B1.1, whose measure B1.2 borrows (*"the same measure as
  B1.1"*, l.383), defines no cut-off for "reaches the right entry".
- *"reading less"* (B1.1) and *"no more than full-text's"* (B1.2) do not say per question, mean, or total. The
  benchmark's mean leaves misses out (`results.md`: *"A miss is left out, never scored 0"*; CACHES l.298: *"each
  route's mean is over a different set of questions"*), so "less on the mean" can be won by answering fewer questions.
- Ground truth is Rd4.4's *"the entry that answered it"*, written by the agent that asked. The benchmark's answers were
  re-checked by five other agents (l.288–289); nothing here is.

**Fix:** state per-question or aggregate, over which question set (questions both routes answered), use one
"reaches/finds" definition for B1.1 and B1.2, and say who confirms the answering entry.

**6. B1.2 — "vector index" in the requirement and Fails-if, "hybrid index" in the comparison.** Medium.
- B1.2 (l.376): *"the vector index finds an entry that full-text missed"*; Fails-if (l.390): *"a vector index exists …
  with no recorded comparison in which it found at least one missed entry"*.
- Same block (l.388–389): *"the comparison runs on the hybrid index"*; 5W1H **When** (l.247): *"when the B1.2
  comparison favours hybrid"*; five whys 4 (l.234): *"the hybrid index finds entries full-text did not"*.

A checker cannot tell whether vector-alone or hybrid results decide. **Fix:** write the requirement and its Fails-if
in terms of "the vector route as it will be served (hybrid while that proposal stands)".

**7. Source labels — "*proposed*" on wording EJ is quoted as ordering written.** Medium.
- The section defines *proposed* as *"wording EJ has not decided"* (l.354). Yet: Rd2.1 is *proposed* with *"EJ … 'write
  fixes 1–4 into CACHES.md'"* (l.459–460); the B1.1 rerun is *proposed* with *"EJ … 'give B1.1 the same rerun
  wording'"* (l.374–375); K3.1–K3.3 are all *proposed* under a heading with *"EJ … 'yes please write'"* (l.438–439).
- Rd4 is labelled *"proposed; new"* although its core is in the vision (*"Two tests, both on the project's own
  recorded questions"*; *"Vector search, run on the recorded misses"*) and in M4 (RECOMMENDATION l.33: *"only when the
  project's own queries justify it"*). Rd4.1 is (v) + M4; only Rd4.2–Rd4.4 are proposals.
- K1.1 cites S-F9 for a content hash, but S-F9 is the mtime design K1.1 rejects (`sqlite-fts.claude.md` l.80:
  *"`query` compares the index build time with the newest source mtime"*). The hash comes from S-F11 (*"SHA-256 on
  files and chunks"*) and S-F15.
- Rd1 cites M18, which says *"Never auto-load the whole memory tree, the full session history, or a whole-graph
  dump"* — not caches at start. The (v) label carries Rd1; M18 does not.
- B2 and Rd3 cite M6 without noting that M6 is **CONTESTED** in its source (RECOMMENDATION l.35: *"opencode: use
  `state.sqlite` as the structured state store, queried at session start"*). The vision settles it for EJ; the citation
  should say so.

**Fix:** split "EJ asked for it to be written" from "EJ decided the wording", or drop *proposed* where EJ's quote is the
decision; correct K1.1's citation to S-F11/S-F15; add M4 to Rd4.1.

**8. B1.1 trial index in `runs/<run-id>/` — not said to be scratch, and not SoT's evidence location.** Low-medium.
- B1.1/B1.2 (l.372, l.384): *"runs on a trial index built in `runs/<run-id>/`"*; K3.2: result written to
  `runs/<run-id>/`.
- `runs/` is committed in this repo (`git ls-files runs` lists 1,269 files); a trial index is several MB (BM-9:
  full-text 9.5 MB, vector 10.2 MB for 490 files). Here `.gitignore` has `*.sqlite`, so a SQLite trial index would not
  be committed; a vector index stored in another format (the 5W1H's option A is numpy) is not covered, and a project
  adopting the design need not have that ignore line. Nothing in the requirements says the trial index is scratch.
- SoT (l.107) puts task evidence in *"`work/<task-id>/    state.md (the handoff), evidence/`"*; `runs/<run-id>/` is
  this repo's convention, not part of the memory layout a project gets.

**Fix:** say the trial index is scratch (deleted or gitignored) and only the comparison result is kept, and pick one
home for the result — SoT's `work/<task-id>/evidence/` or a path SoT lists.

**9. Rd3.3 — a missing embedding model falls back to grep, discarding a working full-text index.** Medium.
- Rd3.3 (l.469): *"A missing embedding model does the same"*, i.e. Rd3.2's *"falls back to grep"*.
- With hybrid, the full-text half still works. **Fix:** "falls back to full-text alone and says so; to grep only if
  full-text is also unavailable".

**10. Rd4 — Fails-if fails on day one and passes with one record; "the questions agents ask of the memory" is
undefined.** Medium.
- Fails-if (l.490): *"`project-memory/` has entries and B1 or K3 has no recorded questions to run on"*. It fails as
  soon as the first entry is written, before any question is asked, and one recorded question satisfies it for ever.
  It cannot detect an agent that does not record (Rd4.1 *"The questions … are recorded"*).
- "A question of the memory" is not defined: every grep over `entries/`? every `INDEX.md` read at session start? the
  Rd4.1 (SoT) read of covering entries before an edit? Rd4.2 *"as it happens"* is a weak word.
- Rd4 sits under **Read — an agent queries it** but it is a write of a new committed source, and it applies when no
  cache exists.

**Fix:** define a recorded question (which reads count), make the Fails-if judged against a session ("a session
searched `entries/` and wrote no record"), and move Rd4 to Keep or a fourth group, or say why it is under Read.

**11. Rd4.3 — `questions/` is required here but is not in the accepted SoT layout.** Medium (acknowledged in the text).
- Rd4.3 (l.482): *"The record lives in `project-memory/questions/`"*; l.489: *"`SOURCE_OF_TRUTH.md` § Where it is put
  does not list `questions/`; adding it waits for EJ."*
- SoT Rd1.1 (l.245–247) lists the contents of `project-memory/` without it, and SoT is accepted. Until EJ decides, a
  project that follows SoT fails CACHES Rd4. The vision calls the caches *"two optional indexes"*; Rd4 makes the
  caches design add a permanent, committed source to memory. *My reading:* that belongs in SoT, with CACHES citing it.

**12. B2.1 / B2.2 — the Fails-if can fire for reasons that are not the cache holding knowledge.** Low-medium.
- B2.1 *"the same query returns the same entries"*: a GPU embedding run is not bit-reproducible in general, and a tie
  in BM25 or RRF can reorder results, so "same entries" can break with nothing wrong. Say whether order counts.
- B2.2 *"a rebuild leaves `git status --short` clean"* fails whenever the tree was dirty before the rebuild. Say
  "unchanged by the rebuild".

**13. B4 — compares against `INDEX.md`, whose generator is still open; `status` is redundant.** Low.
- B4.1 (l.411): *"The index holds the same set of entries as `INDEX.md`"*. SoT l.84: *"which tool generates `INDEX.md`
  and what runs it (K6)"* is open, and SoT K6's Fails-if is exactly "out of step". A stale `INDEX.md` makes B4 pass on a
  stale set. Compare against the entry headers with `status: active` (the rule `INDEX.md` uses) instead.
- If only active entries are indexed, every row's `status` is `active`; "a row without `covers`" needs a rule for
  entries that cover no code (a fact about an outside constraint, a lesson).

**14. Rd3 — five events in one requirement.** Low.
- Rd3.1 (memory readable with no cache — a layout property), Rd3.2/3.3 (missing pieces), Rd3.4 (wrong path), Rd3.5
  (failed rebuild — not absence; it is K2's stale case) share one Fails-if with five conditions. Split Rd3.1 out (it is
  B2/SoT Rd1.2 territory) and move Rd3.5 next to K2.

**15. K3 Fails-if — has no time grain; cannot fail if nobody reruns.** Low-medium.
- l.446: *"a cache stays in `project-memory/.cache/` after a rerun it failed, with no decision by EJ to keep it."* It is
  true in the window between a failed rerun and EJ reading the result, every time. Reruns happen only on a recorded miss
  or EJ's request (K3.2), so a cache that stops paying because questions or the corpus changed, with no miss, is never
  rerun. Say "until EJ decides, the cache is marked failed" and add a rerun event that does not depend on a miss.

**16. Code-graph leftovers around the requirements.** Low.
- Title l.12 *"Memory Caches: SQLite Full-Text, Vector, Code Graph"*; l.154 and l.160 *"the rules for all three
  caches"* — and B4, K1, K2 cite *"(d: Rules for all three caches)"*; l.42 *"None of the three caches"*; Part 1 rule
  l.73–75 and table rows l.91 (*"Is the graph I am about to query current?"*) and l.81; the whole **Code graph**
  section l.252–279. The status note (l.9–10) says the code graph was taken out of *the requirements and the example
  numbers*; the requirements are clean, but they cite a section heading that still says three. Rename the rules
  section to "both caches" and either move the code-graph section to `docs/code-graph/` or mark it out of scope.

**17. The settled vision now cites ids of unaccepted requirements.** Low.
- Vision l.48–51: *"(B1.1)"*, *"(B1.2)"*, *"B5.1"*; CACHES l.7: *"Changed 2026-10-12, not yet accepted"*. B5's (v)
  label rests on a vision line that was edited to match B5.1 (vision l.18–19: *"now excepts the vector embedding step,
  as B5.1 does"*). EJ approved the edit, so the label holds, but the vision and requirements now cite each other.
  Keep the vision's tests in words and drop the ids, so renumbering the requirements cannot break the vision.

### Gaps

- **A zero-hit or failed query against a present cache.** S-F16 measured both: unquoted `D-0012` raises *"no such
  column: 0012"*, and a plausible tokenizer change returned *"0 rows, silently"*. Rd3 covers only absence. Needed: a
  query error falls back to grep and says so, and a zero result is reported as "not found by the cache", never as
  absence (the routing table already says *"no hit is not proof"*, l.84).
- **Who confirms the right entry in a comparison.** B1 and K3 decide builds and drops on Rd4.4's self-reported answer.
  Needed: who checks it, or the comparison's result carries "self-graded" (the house rule on naming who wrote a check).
- **The search input to replay.** Rd4.4 has no field for the terms or query each route ran; without it the B1
  comparison cannot be rerun the way the benchmark was (finding 4).
- **Which recorded questions count.** All time, or since the last comparison? A question whose answering entry was
  later superseded is not in the index (B4) and would count against full-text.
- **A full-text rerun event before full-text exists** (finding 3), tied to something observable such as the SoT Rd3.1
  size check.
- **Where EJ's build, keep and drop decisions are recorded.** B1, B1.2 and K3 Fails-ifs test for *"no decision by EJ"*
  but no requirement says where a checker finds one (an entry? the comparison's run folder?).
- **The embedding model is pinned and available offline.** B2.1 depends on rebuilding *"with the same embedding
  model"*; K2.1 rebuilds when the model id changes; nothing requires the model to stay obtainable or local.
- **Vector cannot outlive full-text.** Under the hybrid proposal, dropping full-text (K3.3) must also drop or disable
  the vector index; nothing says so.
- **Concurrent rebuilds.** K2.1 rebuilds before answering; two agents in one worktree can trigger it together.
  Needed: the temporary-file-and-rename build does not let one rebuild overwrite another's half-written file.
- **Enforcement of recording.** SoT Rd2.1 needs a hook because *"agents skip optional reads"*; Rd4.2 is an optional
  write with no hook or instruction named.

### What holds

- **B1.0** — EJ decides after a passed comparison; matches the 5W1H **Who** rows (l.207, l.245) and the vision's "EJ,
  who sets the triggers".
- **B1 group Fails-if** — checkable: a cache file with no recorded comparison or decision fails it (once the decision's
  location is named).
- **B3** — full rebuild only; the Fails-if (an update or incremental mode exists) can be checked by reading the tool;
  G-F5 drift says what is claimed (code-graph node l.191, *"4.3% of distinct edges were wrong"*).
- **B5** — no model call except embedding; checkable by rebuilding without credentials or network; matches the
  vision as edited.
- **K1.2** — embedding-model id recorded; V-F24 says *"A model change invalidates every vector"*.
- **K2** — stale never answers; the Fails-if (add, change or delete an entry, then query) is concrete and covers the
  deletion case mtime misses; consistent with the Rules (l.168–170) and the full-text 5W1H **How** (l.212).
- **Rd1** — never read at session start; consistent with SoT Rd2.2 (*"Never at session start: `journal/`, `.cache/`"*).
- **Rd2** — results name their entry file; M19's quote is verbatim (RECOMMENDATION l.48).
- **Rd3.2** — the change from S-F9's *"print one warning"* to "every answer says so" is labelled *proposed* and the
  Rules text (l.171–172) was updated to match.
- **Rd3.4** — wrong path never read as an empty index; G-F5 failure mode 5 says exactly this (code-graph node l.220).
- **B4's evidence** — V-F22 is cited as *my reading* and the node marks it INFERRED; the label is right.
- **B1.2's miss definition** matches V-F13 (*"misses that were later answered by a different route"*), and V-F13's
  note that the threshold *"would be EJ's, not a finding"* is respected by B1.0.

### Not checked

- The other two reviews (not opened, to stay independent).
- EJ's quotes in the requirements (*"label hybrid as proposed"*, *"give B1.1 the same rerun wording"*, *"write fixes
  1–4 into CACHES.md"*, *"yes please write"*, *"let rewrite using these 3 categories first"*): grep over `runs/` and
  `docs/` finds them only in `CACHES.md` itself, so they rest on the session thread, which I cannot see.
- `docs/code-graph/` (out of scope), the `W-*`, `OC`, `SZ`, `CX` sources of the example-numbers section, and the
  `s3-F*` research index.
- The vector node beyond F3, F11–F13, F21–F24; the code-graph node beyond F5, F18 and failure mode 5; RECOMMENDATION
  beyond rows M4, M6, M18, M19.
- The benchmark code beyond `results.md`, the route description in `bench/README.md` and the `terms` handling in
  `bench/query.py`; I did not rerun it.
- The source-of-truth vision file and the SoT parts of the diff, except where CACHES cites them.
- No requirement was exercised against running code: no cache exists, so every "can it fail" case above is a reading
  of the text, not a test.
