# Round 1 — reader: claude

Snapshot read: `runs/20261013-caches-design-read/inputs/CACHES.md` (byte-identical to `docs/memory-system/CACHES.md`,
checked with `diff`). Line numbers below are the snapshot's.

### Verdict
REPAIR. Nothing is high-severity, but four lines that depend on this round's changes still disagree with them: the
Rd3.3 fallback, B1.1's agent-side run event against Rd4.1, the K3.2 rerun events for the full-text cache, and "all six
stay open". On top of that, two cost figures are cited to sources that do not contain them.

### Findings

**1. The Rules section still sends a missing embedding model to grep, which contradicts the changed Rd3.3** (medium)
- Location: `CACHES.md:148-149`, "Fall back when absent".
- Quoted: *"If the cache file or SQLite's FTS5 is missing, the tool answers with grep and says so in every answer
  (Rd3.2) (`S-F9`); the same for a missing embedding model (my reading, extending `S-F9`)."*
- Why it misleads: "the same" means grep. Rd3.3 was changed in this round (diff lines 401-403) and now says something
  else, but the rule that implementers read first was not updated.
- Source: `CACHES.md:442-443`, Rd3.3: *"A missing embedding model falls back to full-text if it is there, and to grep if
  not; the answer says so."*
- Fix: replace "the same for a missing embedding model" with "a missing embedding model falls back to full-text if it
  is there, else to grep (Rd3.3)".

**2. B1.1's agent-side run event depends on a journal note that Rd4 says is not written** (medium)
- Location: B1.1, "The comparison", `CACHES.md:327-329`.
- Quoted: *"It runs when EJ asks, or when an agent notes in its journal that `INDEX.md` plus grep made it read through
  many hits to reach an entry"*.
- Why it misleads: Rd4 is now the only rule about what agents note. It defines one kind of note, the miss, and excludes
  everything else. An agent that follows Rd4 never writes the "read through many hits" note, so in practice B1.1 runs
  only when EJ asks, while the text suggests a second route. Rd4's Fails-if does not check for this note either.
- Source: `CACHES.md:452-455`, Rd4.1: *"When an agent finds an entry that `INDEX.md`, grep and full-text all missed …
  it notes the miss in its `journal/` file … Every other question goes unrecorded"*.
- Fix: either add this second kind of note to Rd4.1 (what it holds, as for a miss), or say in B1.1 that until a
  full-text cache exists the comparison runs when EJ asks.

**3. K3.2 gives the full-text cache B1.2's rerun events, which say nothing about full-text** (medium)
- Location: K3.2, `CACHES.md:413-414`.
- Quoted: *"The comparison is rerun when an agent notes a miss, and when EJ asks … (*proposed*, the same as B1.2)."*
- Why it misleads: by definition, a noted miss is a question that full-text also missed. It is evidence for a vector
  index, not that full-text has stopped beating `INDEX.md` plus grep. B1.1's own event changed in this round and is no
  longer "the same as B1.2" (the earlier text had *"give B1.1 the same rerun wording"*, diff line 256). So for the
  full-text cache, K3 never fires on an event that bears on its own comparison.
- Source: `CACHES.md:333-335` (miss: *"`INDEX.md`, grep and full-text search all missed it"*), against
  `CACHES.md:327-329` (B1.1's own event).
- Fix: in K3.2, give each cache its own B1 event: B1.1's event for full-text and B1.2's for vector, plus EJ asking.

**4. "For memory entries all six stay open" is no longer true** (medium)
- Location: Part 1, "Still unresolved", `CACHES.md:111-117`.
- Quoted: *"… and what counts as a *fired* trigger. … For memory entries all six stay open."*
- Why it misleads: D6 asked what counts as a fired trigger. EJ settled it: every trigger is a comparison, the B1.1
  comparison for full-text (`CACHES.md:12-14`, *"the comparison for full-text"*; vision line 51-52). D5 asked whether
  `INDEX.md` carries `covers:` and status, and the sibling design now settles that (`SOURCE_OF_TRUTH.md` K6.1:
  *"one line per active entry, showing its id, kind and one-line claim"*, so no `covers`). D1, the order, is answered
  by the proposed hybrid-after-full-text rule (B1.2, `CACHES.md:343-345`).
- Source: `runs/20261012-caches-enhance/DECISION-RULES.md:157-160`, D6: *"opencode treats a size crossover (~37K
  entries) as a build condition … codex treats only a recorded miss count … claude requires a demonstrated baseline
  failure … unresolved"*.
- Fix: mark D6 settled by B1.1/B1.2, D5 settled by `SOURCE_OF_TRUTH.md` K6.1, and D1 answered as *proposed* by B1.2;
  say which stay open (D2, D3, D4).

**5. Two figures in "Costs" are cited to sources that do not contain them** (medium-low)
- Location: `CACHES.md:101-105`.
- Quoted: *"grep plus opening every hit, about 226K tokens per question (`S-F4`, `S-F13` — opencode's figure …)"* and
  *"an `INDEX.md` scan, under 0.01 s and minimal tokens (`SOURCE_OF_TRUTH.md`)"*.
- Why it misleads:
  - S-F13 measured no tokens. S-F4's 226K is a File-System Agent with `list_dir`, `grep` (paths only) and `read_doc`,
    making 80 LLM calls on a 1,144-document general corpus. It is not "grep plus opening every hit".
  - `SOURCE_OF_TRUTH.md` gives no `INDEX.md` timing (I searched it for "0.01" and found nothing). The run record
    lists the figure as opencode's and unresolved (D4).
- Source: `sqlite-fts.claude.md:107`, S-F13: *"Token cost to the agent is the real axis and this test does not measure
  it"*. `sqlite-fts.claude.md:55`, S-F4: *"`grep` (fixed string, up to 30 matching paths) and `read_doc` (first 8,000
  characters), 80 LLM calls per question"*. `DECISION-RULES.md:149-151`, D4: *"opencode: <0.01 s scan, minimal
  header-only tokens (`SOURCE_OF_TRUTH.md`). codex: time GAP and tokens GAP … unresolved"*.
- Fix: cite only S-F4 for 226K and describe it as "a grep-and-read agent on a 1,144-document corpus". Mark the
  `INDEX.md` figure "opencode's, unsourced (D4)" or drop it.

**6. "Example numbers by case" says it illustrates the B1/K3 comparisons, but its first subsection is the old `INDEX.md` size material** (low)
- Location: `CACHES.md:465-467` and the subsection at `CACHES.md:479-505`.
- Quoted: *"The triggers in B1 and K3 are comparisons. … This section shows **what those comparisons have come out at
  elsewhere**"*, followed by *"### The index read at session start (`INDEX.md`, `MEMORY.md`), by agent type"*.
- Why it misleads: no cache trigger compares start-file limits any more, because the `INDEX.md` size trigger was
  removed. The subsection stays because `SOURCE_OF_TRUTH.md` Rd3 cites it (*"(d: the size check; CACHES.md § Example
  numbers by case)"*). A reader of CACHES alone sees it as an example for a cache trigger.
- Fix: add one line under the subsection heading: "Serves `SOURCE_OF_TRUTH.md` Rd3.1 (`INDEX.md` size), not a cache
  trigger."

**7. Leftovers from the code graph and Part 2** (low)
- Location: `CACHES.md:54`, *"None of the three caches is needed today **for memory entries**."* The design now has two
  caches (title, `CACHES.md:24`).
- Location: `CACHES.md:549-550`, *"K2 (stale never answers) matters more here than any of the three stores."*
- Location: `CACHES.md:44-47`, *"adds measurements on this repo and a routing rule for code and docs. … Its conflict
  with the vision for code and docs is left to EJ."* The routing rule has moved out (`CACHES.md:134`), and the conflict
  was decided (`CACHES.md:60-61`, *"its proposals to widen the vision were not adopted"*).
- Location: `CACHES.md:291-294`, item 4, *"No single store answers 'which tests should I run' … That is why the full
  suite runs before committing."* This is test-selection guidance for code, which is Part 2's subject, not evidence
  about memory caches.
- Fix: "both caches" at :54; "either cache" at :550; at :44-47, "its routing rule moved to `docs/code-graph/`; the
  vision conflict was decided (EJ kept memory entries only)"; trim item 4's last sentence, or point it to
  `docs/code-graph/CODE_GRAPH.md`.

**8. B1.2 measures "loses nothing" on "the B1.1 question set", but Rd4.2 builds a new set for each comparison** (low)
- Location: `CACHES.md:337-339`.
- Quoted: *"every question in the B1.1 question set that full-text answers is still answered"*.
- Why it misleads: Rd4.2 (`CACHES.md:456-457`) says *"The question set for a comparison is built when the comparison
  runs"*. "The B1.1 question set" could mean B1.1's original set, which may by then point at superseded entries, or a
  fresh one. K3.1 says "a question set built then".
- Fix: "every question in a question set built for this comparison (Rd4.2) that full-text answers".

**9. B1.1's new `INDEX.md` arm has no defined way to give a "top 5"** (low)
- Location: `CACHES.md:320-323`.
- Quoted: *"A route answers a question when the right entry is in its top 5 results … The benchmark had no `INDEX.md`
  arm; this comparison adds one."*
- Why it misleads: grep and an `INDEX.md` scan are unranked. In the benchmark, rg's "top 5" was the order in which it
  printed files (`bench/results.md:26-28`), and there is no precedent for `INDEX.md`. *"Measured as the code-and-docs
  benchmark was"* reads as if the whole procedure already exists. It is also unclear whether `INDEX.md` plus grep is one
  route or two arms.
- Fix: say whether `INDEX.md` plus grep is one route, and that its result order (what counts as its first 5) is
  recorded with the run. This adds no number.

**10. Cursor's 12.5% gain is tied to "1,000 or more files", but that file count belongs to a different figure** (low)
- Location: `CACHES.md:531`, *"Code, 1,000 or more files | +12.5% accuracy with vector search (Cursor)"*.
- Source: `vector.claude.md:90-93`, V-F6: *"Achieving on average 12.5% higher accuracy …"*; *"agent code retention
  increases by 0.3% … This effect increases to 2.6% on large codebases with 1,000 files or more"*.
- Fix: "Code (Cursor's own benchmark) | +12.5% average accuracy; code retention +2.6% at 1,000+ files".

**11. Vector why 5 cites code studies as evidence on "memory-style text"** (low)
- Location: `CACHES.md:212-213`, *"On memory-style text, the positive results found combine vectors with keyword search
  (`V-F6`, `V-F7`; `V-F10` is unproven)"*.
- Source: V-F6 is Cursor on code (*"code (not decisions/lessons)"*, `vector.claude.md:95`). V-F7 is a 2024 chunk-RAG
  test whose *"Datasets include codebases"* (`vector.claude.md:102`). Only the unproven V-F10 is agent memory.
- Fix: "The positive results found (code and chunk-RAG, `V-F6`, `V-F7`; on agent memory only the unproven `V-F10`)
  combine vectors with keyword search."

**12. Small mismatches with the changed B1.2 and B4** (low)
- `CACHES.md:152`, *"the same set as `INDEX.md`"*, against B4.1 (`CACHES.md:374`), *"The headers are the reference,
  not `INDEX.md`"*. Fix: "every entry whose header says `status: active` (B4)".
- `CACHES.md:209-210`, vector why 4, defines a miss without B1.2's clause *"the asker's words share no term with it"*
  (`CACHES.md:333`; V-F13 has it, `vector.claude.md:165-166`). Fix: cite B1.2's definition instead of restating it.
- `CACHES.md:224`, vector 5W1H **When**, *"when the B1.2 comparison favours hybrid"*. "Favours" is looser than B1.2's
  "finds one, loses nothing", and EJ's decision (B1.0) is missing, though the full-text row has it (`CACHES.md:186`).
  Fix: "when the B1.2 comparison passes and EJ decides (B1.0)".
- `CACHES.md:89`, the vector row's fallback, *"`INDEX.md`, grep, then read"*. Under the proposed order, full-text
  exists before vector, so full-text belongs in the fallback (as Rd3.3 now says).

**13. Rd4.1 names one journal, but the sibling design has two** (low)
- Location: `CACHES.md:453`, *"notes the miss in its `journal/` file"*.
- Source: `SOURCE_OF_TRUTH.md:128-129`: a task's journal is `work/<task-id>/journal/`, and `journal/` is the
  project's, *"for work not tied to a task"*.
- Why it matters: B1.2 runs *"on the misses noted in agents' journals"*. A runner reading only
  `project-memory/journal/` would miss every miss noted during task work.
- Fix: "in its journal (the task's `work/<task-id>/journal/`, or the project `journal/`, `SOURCE_OF_TRUTH.md` K5.1);
  a comparison reads both".

**14. The vector How row points to an option whose source re-embeds only changed files** (low)
- Location: `CACHES.md:227`, *"The smallest options in `V-F18`/`V-F19`: a static Model2Vec model with numpy (option
  A …)"*.
- Source: `vector.claude.md:292-293`, Option A: *"Rebuild = re-embed the files whose hash changed (INFERRED design
  detail)"*. That is the incremental path B3.1 forbids (*"reuses any row or vector from the previous index"*,
  `CACHES.md:368`).
- Fix: add "with a full re-embed on every rebuild (B3), not the option's per-hash update".

**15. Two Part 1 "none" rows rely on `INDEX.md` for fields it does not carry** (low)
- Location: `CACHES.md:92`, *"exhaustive scan of `INDEX.md` and entry headers"* (covers path X), and `CACHES.md:94`,
  *"`INDEX.md` scan or a script over frontmatter"* (status, `supersedes`, `depends_on`).
- Source: `SOURCE_OF_TRUTH.md` K6.1: *"one line per active entry, showing its id, kind and one-line claim"*. There is no
  `covers`, `supersedes` or `depends_on`.
- Fix: for both rows, make the route "a scan of entry headers (`INDEX.md` lists only id, kind and claim)".

### Unresolved table
- **The BM-9 speed bound and the `git ls-files` overhead:** no longer relevant to any requirement. B1.1 and B1.2 compare
  characters and misses, not time, and K3's time-cost part was dropped. The disclosure codex asked for is still absent
  from BM-9 (`CACHES.md:273-276`), so as an evidence-wording item it is still open. Either add the half-sentence or drop
  the row.
- **Corpus snapshot stability:** still open. Nothing in the design closes it. The run log still has the builder's
  warning, *"the numbers must be re-run on a stable snapshot"* (`runs/20261012-caches-routing/state.md:48`). B1.1 now
  says *"Measured as the code-and-docs benchmark was"*, so the method matters again.
- **The audit's lower-severity findings:** still open. The text does not address them. They bear only on the
  code-and-docs evidence, unless B1.1 reuses that harness.
- **Discovery versus exhaustive routes in the "none" rules:** settled by the current Part 1 rule and table. Discovery
  (free text, find by meaning) goes to a cache once its trigger fires (`CACHES.md:81-84, 88-89`). Completeness and
  absence stay files-only (`CACHES.md:92-93`). That is codex's position, which agy adopted, and it keeps A's rows.

### What holds
- **Header and diff:** the changes recorded at `CACHES.md:7-22` match the diff. The question log, Rd4.3–Rd4.6,
  `questions/`, the K3 cost table, "K3: cheap", B4's `status` and the code-graph section are all gone from the text.
- **Replacing the question log with noted misses plus a per-comparison set (Rd4):** sound in itself. The miss
  definition in B1.2 now carries V-F13's "share no term" clause, and Rd4.2 records who wrote and who checked the set,
  as the benchmark did.
- **K3 without its cost part:** consistent. No time-versus-tokens unit is left, and nothing else cites the dropped
  table.
- **B4 without `status`:** consistent with both 5W1H tables (`CACHES.md:185, 223`). The headers as reference agree with
  `SOURCE_OF_TRUTH.md` K6.1.
- **The full-text trigger as the B1.1 comparison:** consistent in the rule (`:81-83`), the table (`:88`), why 4
  (`:170-172`), the 5W1H When (`:186`) and the vision's "Too many entries".
- **The answer first:** sound apart from "three caches" (finding 7).
- **SQLite full-text index, five whys and 5W1H:** the S-F1, S-F2, S-F4, S-F5, S-F13, S-F16 and S-F17 citations match
  the node.
- **Vector index, whys 1–3 and the 5W1H Where/How:** the V-F3, V-F4, V-F8, V-F11, V-F12, V-F18, V-F19, V-F20, V-F21
  and V-F24 citations match the node.
- **Rules:** "Full rebuild, never patched" (G-F5 drift 4.3%, G-F5c) and "Rebuild before answering when stale" (S-F9
  quote) match the code-graph and SQLite nodes. Failure mode 5 is quoted correctly.
- **Measured here:** every BM-1 to BM-6 cell matches `bench/results.md`. BM-7's 0.78/0.59/0.04 and the C01/C02 0.33/0.8
  match `nodes/runtime-recall.json`. BM-9's 529 tests in 31–33 s and the gold "37 correct, 3 incomplete" match the run's
  `state.md`. Determinism 180/180 matches.
- **Core requirements:** the B1.0, B2, B3, B5, K1, K2 and Rd1–Rd3 citations hold. S-F11 is the hash. CP6's quote is
  exact. M6 is CONTESTED as stated. M19's quote is exact.
- **Example numbers:** the W-22 tier figures (77.4/74.7, 70.1/69.9, 50.5/30.7, 7 tiers) match `nodes/web.md:132-141`,
  and V-F4's 51.4/68.8 matches. SEZA B1.2 "not met" is consistent with Rd4 (no noted misses).
- **What this changes elsewhere:** correct now that `questions/` is gone. `SOURCE_OF_TRUTH.md` § Where it is put lists
  `.cache/` only.
- **Not known:** all four lines hold. V-F quotes were checked against saved copies (`vector.claude.md:9-11`), and the
  planted name was in `state.md` (`sqlite-fts.claude.md:27`).
- **The vision:** consistent with the requirements as changed (B1.0, B1.1, B1.2, B5.1, K2, Rd1), apart from what
  findings 1–4 touch on the CACHES side.

### Not checked
- The sources behind `W-*` (except W-22's table), `OC`, `SZ` and `CX` in `runs/20261012-caches-numbers/nodes/`, so the
  start-load table, the SEZA byte counts and the Instant Grep claim are unverified. For V-F6 I checked only the Cursor
  row.
- `s3-F*` ids (s3-F29, s3-F34) and `docs/KNOWLEDGE_GRAPH_DESIGN.md` §1. I saw the latter only through G-F21's quote.
- `audit-0.json`'s lower-severity findings, and whether node 3 ran on a stable snapshot. I read the run log's account,
  not the audit.
- `docs/code-graph/CODE_GRAPH.md`, beyond confirming it holds Part 2.
- The round-2 merge reviews, beyond the `git ls-files` lines.
- M5, M13, M17, M18 and M21 beyond their one-line rows in `RECOMMENDATION.md`.
- No code was run.
