### Verdict

REPAIR — my reading: the two-cache design is supportable, but conflicting triggers, an undefined cost comparison, and incomplete failure checks prevent acceptance.

### Findings

All findings below are my reading. `CACHES.md` line numbers refer to the supplied snapshot.

1. **K3.1 — high — Rebuild cost has no comparable unit.**  
   **Evidence:** K3.1 says “a query’s cost includes any rebuild it triggered”; B1.1 measures “the characters read to the first right entry.” The K3 examples instead report rebuilds in seconds (`CACHES.md:568–579`). The previously accepted R8.2 compared rebuild time with reading time; the supplied diff removes that comparison.  
   **Breaking case:** a cache saves characters but takes minutes to rebuild. The text cannot determine whether it still pays. Its failure check becomes usable only after someone supplies an unstated cost rule.  
   **Proposed fix:** ask EJ which cost comparison governs retention, keeping unlike units separate unless he chooses a conversion. Define the measurement scope and the failure check without inventing a threshold.

2. **B1.1 — high — The full-text comparison lacks a complete scoring rule.**  
   **Evidence:** “after reading less … with no more misses” (`CACHES.md:366–370`) specifies characters but leaves the aggregation, result cutoff, and treatment of misses unresolved. The cited benchmark says its character mean is “over the answers that named one” and “A miss is left out” (`bench/results.md:28`).  
   **Breaking case:** full-text loses an expensive question that grep answers, gains a cheap question grep misses, and reports fewer characters with the same miss count. Different question sets can make that look like a saving.  
   **Proposed fix:** have EJ settle whether the comparison is per question or aggregate, which result cutoff defines a miss, and how unmatched successes are handled. Specify how the `INDEX.md` read contributes to the baseline cost.

3. **B1.1 / CACHES.md:70, 79, 209 — high — Two different full-text triggers remain operative.**  
   **Evidence:** B1.1 says full-text is built when its measured comparison wins. The routing table says “conditional on the size trigger,” and the 5W1H says “Built when … `INDEX.md` can no longer list every active entry.” The vision also names that size problem, but its success test uses B1.1’s comparison (`caches-vision.md:29–35, 47–49`).  
   **Breaking case:** the comparison passes while every active entry still fits in `INDEX.md`. B1.1 permits building; the 5W1H does not.  
   **Proposed fix:** ask EJ whether exceeding the index limit is a prerequisite or an example of when the comparison might win. Apply that answer consistently to the vision, routing table, five whys, and B1.1.

4. **B1.1 / CACHES.md:193–195 — high — The size-trigger explanation conflicts with the sibling design.**  
   **Evidence:** the caches text says that when the complete index no longer fits, “ranked search is what replaces it.” `SOURCE_OF_TRUTH.md` K6.1 still requires “one line per active entry,” while Rd3.1 requires that file to fit the strictest start-file limit.  
   **Breaking case:** the complete active-entry list exceeds that limit. Installing full-text does not make the same complete `INDEX.md` fit, and Rd1 prohibits loading the cache at session start.  
   **Proposed fix:** leave the overflow behavior as an explicit owner decision and coordinate it with the sibling design. Do not imply that a search cache alone resolves the index’s incompatible obligations.

5. **Rd4 — medium — Its failure check does not enforce recording every question.**  
   **Evidence:** Rd4.1 requires “The questions agents ask … are recorded”; Rd4.2 requires recording “as it happens”; Rd4.3 specifies location, separate session files, and git. The check only fails when there are “no recorded questions” or a record lacks a field (`CACHES.md:478–491`).  
   **Breaking case:** an agent records one complete question after the session and omits every other question. The stated check passes despite violating Rd4.1 and Rd4.2.  
   **Proposed fix:** give completeness, timing, storage, and field validity their own checks. Treat blank or placeholder required values as invalid, while preserving the explicitly allowed “not found” answer.

6. **B1 / K3 — medium — The checks omit comparison and notification obligations.**  
   **Evidence:** B1 requires reruns when a miss is recorded and notification when a comparison passes; K3.2 requires reruns, and K3.3 requires telling EJ when the cache fails. Their checks inspect whether a cache exists without the necessary comparison or decision (`CACHES.md:372–393, 440–446`).  
   **Breaking case:** a recorded miss never triggers a rerun, or a passing trial is never reported to EJ. With no production cache installed, B1’s check does not fail.  
   **Proposed fix:** add checks for the specified rerun events and notifications. Clarify K3.1’s “keeps passing” against K3’s explicit allowance for EJ to retain a failed cache.

7. **B4.1 — medium — Agreement with `INDEX.md` is insufficient to establish active membership.**  
   **Evidence:** B4.1 requires “the same set of entries as `INDEX.md`.” V-F22’s inference instead depends on filtering the entry’s `status` field (`vector.claude.md:254–257`). The sibling design itself recognizes an out-of-step index as a failure in K6.  
   **Breaking case:** an entry becomes retired while `INDEX.md` still lists it as active. Copying that list either includes an inactive entry or conflicts with the “Only active entries” requirement.  
   **Proposed fix:** establish the active set from current entry headers and validate the generated index against it. Specify what a query does when those sets disagree.

8. **B3.1 — medium — “Fails if” does not check that rebuilding is complete.**  
   **Evidence:** B3.1 requires regeneration of “the whole index from the files,” but its check only asks whether “the rebuild has an update or incremental mode” (`CACHES.md:405–408`).  
   **Breaking case:** a command called `rebuild`, with no update option, silently reuses existing rows or vectors. The check passes without proving a full rebuild.  
   **Proposed fix:** check regeneration from the complete current source set as well as the absence of incremental paths, including paths outside the rebuild command.

9. **B2.1–B2.2 — medium — Verification preconditions are missing.**  
   **Evidence:** B2.1 promises identical entries after rebuilding with the same embedding model; B2.2 requires `git status --short` to be “clean.” K1.1 explicitly accommodates “edits not yet committed” (`CACHES.md:398–403, 424–426`).  
   **Breaking case:** rebuilding changes nothing tracked, but an existing uncommitted entry edit makes the check fail. Separately, unchanged model identity alone does not fix source contents or ranking configuration.  
   **Proposed fix:** hold the source snapshot and retrieval configuration constant for the repeatability check. Check that rebuilding introduces no tracked changes relative to the initial worktree state.

10. **K1.1 / K2.1 / B1.2 — medium — Some citations support an adaptation, not the stated mechanism.**  
    **Evidence:** K1.1 and K2.1 cite S-F9 for content-hash checking; S-F9 describes comparing build time with “the newest source mtime,” while S-F11 describes SHA-256. B1.2 cites V-F13 for its miss definition, but V-F13 explicitly says “the adaptation is INFERRED” (`vector.claude.md:151–168`).  
    **Breaking case:** a reader opens S-F9 expecting the cited hash mechanism and finds a different mechanism.  
    **Proposed fix:** retain the correct `(d)` and *proposed* labels, but distinguish the borrowed behavior from this design’s adaptation. Cite S-F11 for the hash precedent and mark the V-F13 miss definition as the researcher’s inference.

11. **CACHES.md:73–75, 160, 252–279 — medium — Code-graph instructions remain inside the operative design.**  
    **Evidence:** the core scope says “the code graph is its own project” (`CACHES.md:350–351`), yet Part 1 still routes memory questions to it, the rules cover “all three caches,” and its 5W1H still specifies `project-memory/.cache/code-graph.json`. The vision says there are “two optional indexes” (`caches-vision.md:21`).  
    **Breaking case:** an implementer follows the remaining 5W1H and installs a third cache in the memory project.  
    **Proposed fix:** replace operative graph instructions with a link to its project and update the title and cache count. Graph research may remain as clearly identified evidence for a shared failure class.

12. **B2.2 / B4.1 / K2.1 / Rd3.2 — low — Individual clauses combine independently failing obligations.**  
    **Evidence:** B2.2 combines git exclusion with rebuild cleanliness; B4.1 combines membership with metadata; K2.1 combines freshness comparison with atomic publication; Rd3.2 combines fallback routing with disclosure.  
    **Breaking case:** fallback works but its answer omits the disclosure. That is a different failure from fallback not working.  
    **Proposed fix:** split these clauses into separately identifiable obligations and checks. Preserve their existing sources and proposal status.

### Gaps

- **Stable source and index generations.** K2 needs an observable rule for source changes during hashing, rebuilding, or querying. Temporary-file rename prevents a partially written file from becoming visible; it does not prove that the published index represents one consistent source snapshot.
- **Consistent full-text and vector publication.** The vector 5W1H promises rebuilding both “in the same step, so the two cannot disagree,” but no requirement checks that a hybrid answer uses matching source generations. Failure between publishing the two stores needs defined behavior.
- **Active-entry filtering on fallback.** B4 constrains index membership, while Rd3 merely says to use grep. Ordinary grep over `entries/` can return superseded or retired entries, contrary to the sibling’s read restrictions; fallback needs the corresponding filtering behavior.
- **Safe interpretation of agent questions.** S-F16 reports that unquoted `D-0012` raises an FTS error. The design selects a tokenizer but gives no requirement for translating arbitrary question text into valid search input or handling malformed queries.
- **Replayable comparison evidence.** Rd4 records a question and an answering entry but does not establish the corpus revision, reproducible baseline searches, or how the expected answer is validated when entries later change. B1 and K3 need those facts to make their comparisons reviewable.

### What holds

- **B1.0:** the EJ decision gate is explicit and checkable; installing a cache after a passing comparison without his decision fails.
- **B1.2, retrieval condition:** a recorded missed entry recovered in the proposed top five provides a concrete success; losing a previously answered question provides a failure.
- **B2, derived-only intent:** deleting a cache must preserve memory; the vision and M4/M6 support that boundary.
- **B4, metadata condition:** a row missing `status` or `covers` concretely fails; V-F22 supports the labelled inference.
- **B5:** a full-text rebuild that calls a model fails; the updated vision directly supports the embedding exception.
- **K1.2:** missing embedding-model identity concretely fails; V-F24 supports invalidation on a model change.
- **K2, freshness outcome:** returning a deleted entry from the old index concretely fails.
- **Rd1:** a startup hook opening `project-memory/.cache/index.sqlite` concretely fails; the vision and sibling agree.
- **Rd2:** a result without its entry-file path concretely fails; M19 supports opening the primary source before acting.
- **Rd3:** a mistyped path that creates an empty database, or a failed rebuild that serves stale results, concretely fails; G-F5 and the labelled extensions support the behavior.
- **Rd4, provenance intent:** preserving question records outside the disposable cache and assigning their recording to the asking agent are coherent proposals.

### Not checked

- I checked the supplied design, vision, complete diff, sibling design, and relevant cited findings. I did not open other reviewers’ reviews.
- I did not verify original external publications, saved web copies, benchmark scripts, raw measurements, or the additional W/OC/SZ/CX sources behind the example tables.
- This is my manual requirements review; I ran no implementation tests. The benchmark questions were written by Codex and its harness by opencode, as the design discloses; those measurements do not establish performance on a real memory-entry corpus.
- Embedded EJ quotations were assessed as documentary attribution, without verification against the original conversation. No files were changed.
