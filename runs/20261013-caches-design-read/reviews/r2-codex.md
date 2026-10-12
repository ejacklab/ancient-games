### Points I now support

Reader: **codex**. Positions below are **my reading** after checking all four round-1 reports against the sources. `CACHES.md` means the [review snapshot](/home/smoke01/dev/ancient-games/runs/20261013-caches-design-read/inputs/CACHES.md). This is a documentary review; I did not rerun measurements or change files.

1. **The main changes hold, subject to the dependent wording findings below — agree with all four readers.** Dropping the full question log, generating question sets when comparisons run, removing K3’s rebuild-cost clause, removing stored `status`, and moving the operational code-graph sections follow the recorded decisions. Deciding lines: `CACHES.md:20–22`, “only misses are noted”; `:411–412`, “the rebuild-cost part was dropped”; `:372–374`, “no row stores `status`” and “The headers are the reference”; `:134–136`, Part 2 moved while its evidence remains.

2. **Missing-model fallback contradicts Rd3.3 — agree with claude F1, codex F3 and agy F1.** At `CACHES.md:148–149`, “the same for a missing embedding model” inherits the preceding grep fallback. The deciding requirement at `:442–443` says: “falls back to full-text if it is there, and to grep if not.” Claude F12’s observation about the vector fallback row at `:89` also holds: that row omits available full-text. These summaries need the accepted fallback order.

3. **Rd4 excludes the journal note B1.1 needs — agree with claude F2, codex F2 and opencode F3.** B1.1 at `CACHES.md:327–328` runs when an agent notes that the baseline “made it read through many hits to reach an entry.” Rd4.1 at `:454` then says, “Every other question goes unrecorded.” A successful but expensive search need not satisfy B1.2’s miss definition. The contradiction concerns which exceptional searches get noted; it does not justify restoring a log of every search.

4. **Historical misses need a stated interpretation against the current active corpus — hold codex F4.** K3.1 at `CACHES.md:411` uses “the noted misses”; B4.1 at `:371` indexes active entries “and nothing else.” Rd4.2 at `:456–457` creates fresh questions from entries existing then, but does not explain what happens to a historical miss whose target has since become superseded. **Cannot tell** which treatment is intended. The missing interpretation should remain open rather than treating deliberate exclusion as a retrieval failure.

5. **“The B1.1 question set” is ambiguous after the change to fresh sets — agree with claude F8.** `CACHES.md:337` names that set, while Rd4.2 at `:456` says, “The question set for a comparison is built when the comparison runs.” K3.1 at `:411` likewise says “a question set built then.” **Cannot tell** whether B1.2 means the earlier B1.1 artifact or a current baseline set. Claude caught this ambiguity that I missed.

6. **The added baseline’s top-five procedure is unspecified — agree with the central point of claude F9.** `CACHES.md:320` makes success depend on “top 5 results,” and `:323` says, “The benchmark had no `INDEX.md` arm; this comparison adds one.” The text does not explain how the combined `INDEX.md` plus grep route produces its ordered candidates. That limits reproducibility. I reject Claude’s description of the benchmark grep ordering separately below.

7. **`INDEX.md` alone cannot answer every structured-header question — agree with part of claude F15.** At `CACHES.md:94`, “`INDEX.md` scan or a script over frontmatter” presents alternatives for questions involving `supersedes` and `depends_on`. The deciding sibling-design line, `SOURCE_OF_TRUTH.md:276–277`, lists only “id, kind and one-line claim.” The frontmatter route holds; the standalone index alternative is insufficient for those links. Claude caught this distinction that I missed.

8. **The index timing is unsupported by its citation — agree with claude F5, codex F13 and opencode F5.** `CACHES.md:104–105` gives “under 0.01 s and minimal tokens” against `SOURCE_OF_TRUTH.md`. The research run explicitly preserves the disagreement: `DECISION-RULES.md:150–151` attributes that figure to opencode, while codex reports “time GAP and tokens GAP.” It should not appear as an established measurement from the sibling design.

9. **The 226K figure describes a particular agent experiment, not opening every grep hit — agree with claude F5.** `CACHES.md:102` says “grep plus opening every hit.” The deciding source, `sqlite-fts.claude.md:55`, describes `list_dir`, grep returning up to 30 paths, `read_doc` returning limited text, and 80 model calls per question. At `:107`, S-F13 explicitly says its test does not measure token cost. The figure itself is reported in S-F4; the procedure and the extra S-F13 attribution are wrong. Claude caught this qualification that I missed.

10. **K2 does not establish that indexed statements remain true — hold codex F5.** `CACHES.md:549–550` connects SEZA’s outdated memory to “K2 (stale never answers).” K2.1 at `:395–398` compares the index with entry files. An unchanged file containing an outdated claim can pass that check. The deciding research line, `caches-numbers/nodes/codex.md:341`, says maintenance and source checking are needed. The missing projection supports a fallback concern; it does not establish that K2 would repair outdated source content.

11. **The SEZA example does not establish an early full-text win — hold codex F6.** `CACHES.md:518–520` says “full-text wins much earlier.” The SEZA researcher’s deciding line, `nodes/seza.md:337`, says “n=5, no verdict” and records full-text misses. At `:349–350`, the researcher says the paired reading path was not measured. Large grep output motivates the B1.1 comparison; it does not establish its winner.

12. **The history-loading examples support weaker conclusions than the design states — hold codex F7.** `CACHES.md:526` describes loading history “instead of retrieving,” but `caches-numbers/nodes/web.md:110` identifies the comparator as an oracle containing only the right sessions. At `:111–120`, W-19 reports RAG against vanilla long context without establishing that keyword retrieval produced the result. **Cannot tell** the actual W-19 retriever from this extract. The design’s `:535` conclusion, “it is keyword retrieval that wins,” is unsupported by these two reported comparisons.

13. **Cursor’s file-count condition is attached to the wrong result — agree with claude F10 and codex F8.** `CACHES.md:531` associates “1,000 or more files” with the 12.5% accuracy gain. `vector.claude.md:91–93` reports average question-answering accuracy separately; the 1,000-file condition qualifies code retention. The figures should remain separate.

14. **The hybrid evidence is overstated as evidence on memory-style text — agree with claude F11 and codex F9.** `CACHES.md:212` says “On memory-style text.” The cited V-F6 explicitly concerns “code (not decisions/lessons)” at `vector.claude.md:95`; V-F7 is a chunk-RAG experiment at `:102–103`. These findings can inform the proposed policy without establishing its benefit on the intended memory corpus.

15. **The loader-cap examples omit their applicability condition — hold codex F10.** `CACHES.md:484` and `:487` say “instructions plus index” under the respective caps. The deciding source, `caches-numbers/nodes/codex.md:444`, says those budgets apply **if the index is placed in that instruction chain**; a subsequent file read is governed differently. I hold the qualification issue, not a claim that the quoted loader budgets are themselves wrong.

16. **“For memory entries all six stay open” overstates the current disagreement — agree with claude F4, codex F11 and opencode F12.** At `CACHES.md:117`, historical disagreements are presented as current open questions. B1.1 at `:323` settles comparison rather than a fixed size; B1.2 at `:343–345` states the proposed full-text-before-hybrid policy. `SOURCE_OF_TRUTH.md:276–277` settles the index’s listed fields. D6 is settled, D5’s layout question is settled, and D1’s routing policy is answered while actual need remains unmeasured. D2–D4 retain measurement gaps.

17. **The benchmark limitations need to accompany its interpretation — agree with codex F12 and the disclosure part of opencode F4.** The opencode builder warned at `build.opencode.stdout.md:68` that the corpus moved during its run. The run recorder at `state.md:59` records a later repaired-harness run, so “no rerun” would be wrong. Neither that record nor `CACHES.md:241–242`’s determinism statement establishes a frozen snapshot. The Claude audit at `audit-0.json:93–94` also identifies timing overhead. These caveats already appear in the unresolved table, but their relation to the adjacent benchmark conclusions should be explicit. This does not invalidate the recorded maximum.

18. **The current-scope leftovers hold — agree with claude F7, codex F16, opencode F1/F7 and agy F2/F3.** `CACHES.md:54` and `:550` count three current caches/stores, against the vision’s `:27`, “two optional indexes.” The provenance note at `CACHES.md:45–47` still describes a present routing rule and an undecided vision conflict, against `:134–136` and `:60–61`. Claude also correctly identifies the prescriptive tail at `:294`, “the full suite runs before committing,” as code-work guidance. The retained benchmark observations themselves remain permitted evidence.

19. **The summary’s hash citation remains incomplete — hold codex F15.** `CACHES.md:145–147` gives a content-hash procedure with S-F9 alone. `sqlite-fts.claude.md:80` describes newest-mtime checking; `:89` supplies SHA-256. K2.1 already distinguishes these sources at `CACHES.md:397–398`. The summary should preserve that distinction.

20. **The “Not known” corpus list omits the supplied file-memory example — hold codex F17, narrowly.** `CACHES.md:561–562` lists source code, chat memory and enterprise documents. `caches-numbers/nodes/seza.md:245–248` explicitly measures a Claude memory folder and a wider collection including memory and decision records. The remaining gap is still measurement on **this design’s active-entry corpus**; SEZA does not close it. My finding concerns the incomplete evidence description.

21. **The absence row cites the wrong finding — agree with agy F4.** `CACHES.md:93` cites V-F20. `vector.claude.md:233–238` concerns linguistic negation; `:259–260`, V-F23, explicitly says top-k cannot enumerate or prove absence. Agy caught this citation error that I missed.

22. **G-F18 does not support the repo-map row — agree with opencode F13.** `CACHES.md:98` cites it for “A map of the whole repo.” At `code-graph.opencode.stdout.md:181`, F18 describes the implementation, output and determinism of the in-repo graph tool. M18 supports avoiding a whole-graph startup dump, but that does not make G-F18 evidence for the proposed map route. Opencode caught this citation mismatch that I missed.

### Points I reject

1. **My codex F1: K2.3 unconditionally requires an unapproved vector index — disagree; withdraw.** I read the joint-rebuild sentence too strongly. `CACHES.md:140` scopes the rules to “whichever cache is built”; B1.0 at `:312–313` says a passed comparison alone builds nothing, and B1.2 separately gates vector construction. K2.3 at `:402–404` addresses coordinated rebuilding of the pair. Its wording could be more explicit about installations with one cache, but it does not establish the high-severity contradiction I claimed.

2. **Claude F3, opencode F2 and agy F5: K3.2’s miss event cannot serve full-text — disagree.** K3.1 begins at `CACHES.md:410` with “A built cache.” Full-text therefore exists when its continued value is checked, and a miss involving full-text can occur in a full-text-only installation. K3.1 says to rerun the cache’s own **comparison**; it does not require the same scheduling event as initial construction. K3.2 explicitly chooses misses and EJ asking at `:413–414`. A miss does not itself demonstrate a full-text benefit or loss, but it can trigger a fresh comparison. The claimed circularity and the mandatory remedy of matching B1.1’s event are not supported.

3. **My codex F14, claude F12 and opencode F6: “the same set as `INDEX.md`” makes the generated file authoritative — disagree.** `CACHES.md:152` first says “Index only active entries.” B4.1 at `:373–374` explicitly says, “The headers are the reference, not `INDEX.md`.” Equality with a correctly generated index is compatible with that rule. The summary does not instruct the builder to use `INDEX.md` as its membership source.

4. **Claude F15’s completeness-row objection — disagree with that part.** `CACHES.md:92` requires an exhaustive scan of “`INDEX.md` **and entry headers**.” The headers supply fields absent from the index. This route does not depend on the index carrying `covers`. The separate `:94` alternative remains a supported finding above.

5. **Claude F9’s account of the benchmark grep order — disagree.** The benchmark documentation, `bench/README.md:75`, says it ranks by “distinct terms matched, then match count per file.” `bench/results.md:26–28` defines scoring and output, not ordinary filesystem print order. Claude’s conclusion that the added index arm needs a defined procedure holds; this description of the existing benchmark does not.

6. **Opencode F10: BM citations are unresolvable because the source lacks BM IDs — disagree.** `CACHES.md:233` explicitly says “ids `BM-*` below,” and `:257–276` assigns those labels to the reported categories and measurements. They are local labels with an identifiable mapping. They are not claimed to be headings already present in `results.md`.

7. **Opencode F8: Rd3.4’s G-F5 reference is substantively ambiguous — disagree.** `CACHES.md:446` includes “failure mode 5,” which resolves to `code-graph.opencode.stdout.md:218–220`, the mistyped-path finding. Adding “drift” would improve consistency with the naming note at `CACHES.md:28–29`; the present qualified reference still identifies the evidence.

8. **Opencode F9: retaining the drift citation without another graph-study label is misleading — disagree as a finding requiring repair.** `CACHES.md:27–29` identifies the code-graph source and defines `G-F5 drift`; `:142–143` describes wrong **edges**. The snapshot vision at `:45–47` explicitly labels the graph study as analogous evidence. None of these lines presents a measured memory-cache drift rate.

9. **Opencode F11: a bare contested ID necessarily misrepresents consensus — disagree.** `CACHES.md:352–353` already discloses M6’s contested status. The citations at `:97` and `:438` do not assert unanimity. `RECOMMENDATION.md:35` and `:46` preserve the disagreements. A contested recommendation can inform an owner-accepted design; repeating its voting status at every use is not necessary to make these statements true.

10. **Claude F13: Rd4.1 excludes task journals — disagree with the asserted restriction.** `CACHES.md:453` says “its `journal/` file,” while B1.2 at `:330` refers to “agents’ journals.” `SOURCE_OF_TRUTH.md:266–268` defines both task and project journals. **Cannot tell** the eventual comparison runner’s discovery procedure, but the text does not explicitly restrict notes to the project-root journal or establish that task misses will be omitted.

11. **Claude F14: naming Model2Vec option A imports its incremental rebuild procedure — disagree.** `CACHES.md:227` names model/runtime options from V-F18/V-F19; it does not adopt the source’s whole option-A storage and update design. B3.1 at `:366–368` expressly forbids incremental updates and reuse of previous vectors. The source’s incremental suggestion at `vector.claude.md:292–293` does not override that accepted requirement.

12. **Claude F12’s remaining vector-summary objections — disagree as requirement contradictions.** The fifth-why narrative at `CACHES.md:208–211` describes wording mismatch and cites V-F13; B1.2 at `:333–334` supplies the exact no-shared-term definition. The vector “When” row at `:224` explicitly references B1.2, and the “Who” row at `:222` says EJ decides. “Favours hybrid” could be made more precise, but the table as a whole does not replace B1.2’s test or remove EJ’s decision.

13. **Claude and agy: discovery versus exhaustive routing is already settled — disagree.** `CACHES.md:88–89` permits discovery through caches, but `:94–95` still assigns “none” to entire structured-header and “why” question classes; `:84` says, “Everything else is the files.” Those lines do not distinguish discovering a candidate from verifying its content or enumerating all matches. The explicit completeness and absence rows settle those two cases, not the disputed boundary for every other row.

14. **Opencode: vector deduplication changes the adopted top-five results — disagree with that implication.** The Claude audit’s deciding line, `audit-0.json:52`, says, “The hit@5 tables do not change.” It reports fewer than ten returned paths, not an altered measured top-five hit rate. Other low-severity findings can affect character output: `:100–101` explicitly reports that effect for hybrid blocks. Neither statement settles the whole audit.

15. **Agy: the lower-severity findings were never addressed by code changes — cannot tell; reject that categorical claim.** `state.md:56–59` records repair of the five high findings and a later run, with re-audit stopped. That does not establish the disposition of every low finding. The design can accurately say that their closure is unverified; absence of re-audit is not proof that no repair occurred.

### My own points: held or withdrawn

- **F1 — Withdrawn:** K2.3 does not establish mandatory construction of an unapproved vector index.
- **F2 — Held:** Rd4’s blanket exclusion conflicts with B1.1’s exceptional journal note.
- **F3 — Held:** the missing-model summary has the wrong fallback order.
- **F4 — Held:** treatment of historical misses against current active entries remains unspecified.
- **F5 — Held:** cache-to-file freshness does not establish source-content truth.
- **F6 — Held:** SEZA’s broad grep output does not establish a B1.1 win.
- **F7 — Held:** oracle context selection and unspecified RAG do not establish the stated keyword-retrieval conclusion.
- **F8 — Held:** Cursor’s file-count condition belongs to retention, not average accuracy.
- **F9 — Held:** the cited hybrid studies do not establish the stated memory-text result.
- **F10 — Held:** loader-cap examples need the instruction-chain condition.
- **F11 — Held:** “all six stay open” fails to distinguish settled policy from unmeasured benefits.
- **F12 — Held, narrowed:** carry the unclosed snapshot caveat with the interpretation; do not claim the rerun never happened or the recorded determinism result is false.
- **F13 — Held:** the index timing is not measured by its cited design.
- **F14 — Withdrawn:** equality with `INDEX.md` does not make it the membership authority.
- **F15 — Held:** S-F9 does not supply the summary’s hash procedure.
- **F16 — Held:** current three-cache counts and the undecided scope-conflict wording are leftovers.
- **F17 — Held, narrowed:** the corpus list omits SEZA file memory; the gap on the designed active-entry corpus remains real.

### Unresolved table

| Row | My position after discussion | Deciding evidence and limits |
|---|---|---|
| **BM-9 speed bound and `git ls-files` overhead** | **Settled for the recorded maximum; disclosure remains open.** Agree with the narrower bound position. Reject the claim that removing positive overhead invalidates that maximum. | The Claude audit at `audit-0.json:93–94` says grep timing includes extra work and that the speed winner does not change. `CACHES.md:273` reports the observed maximum. This establishes neither a general latency guarantee nor an unbiased comparative timing. With K3’s cost clause removed, timing is not an adoption gate. |
| **Corpus snapshot stability** | **Still open; cannot tell whether the later run closed it.** | The opencode builder warns at `build.opencode.stdout.md:68`; the run recorder documents the later repaired-harness run at `state.md:59`. Matching rebuild answers establishes recorded determinism, not by itself a frozen corpus. “No rerun happened” is unsupported. |
| **Audit’s lower-severity findings** | **Still open in part.** Agree that some concern presentation or character measurements; reject treating every listed item as an outstanding defect. | The Claude audit at `audit-0.json:107–109` records “No problem found” and “None needed.” At `:52`, vector deduplication leaves hit@5 unchanged; at `:101`, hybrid block choice affects character measurements. `CACHES.md:241–242` discloses that repair was not re-audited. The remaining implementation dispositions are unverified. |
| **Discovery versus exhaustive memory routes** | **Still open. Hold my round-1 position.** | `CACHES.md:92–93` correctly requires exhaustive routes for completeness and absence. The blanket “none” rows at `:94–95` still do not distinguish candidate discovery from authoritative reading or exhaustive enumeration. Claude’s and agy’s “settled” reading is less well supported than the unresolved reading shared by codex and opencode. |
