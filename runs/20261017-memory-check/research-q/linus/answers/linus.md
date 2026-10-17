# Linus Torvalds — memory-check before implementation

## Answer

Build an evidence report that distinguishes what was checked, what failed, and what remains unknown. Before implementation, resolve the mismatch between checking current files and checking staged snapshots, and separate the session-start warning from checks that open caches or run rebuilds.

## How I decided

1. **My #9 and my #7: define the evidence before defining success.**

   **My reading:** a result needs its requirement id, inspected project, inspected snapshot, evidence, and limits. Passing a structural clause cannot certify a whole requirement that also needs judgement.

   I counted **20 records containing `tool` or `git`** in [the requirements YAML](/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH_REQUIREMENTS.yaml). That count comes from my extraction of the `id` and `check` fields; it establishes coverage, not that all 20 are automatically decidable.

   C1 currently assumes otherwise. Applying the requirement-check criteria to that routing statement:

   | Criterion | Result |
   |---|---|
   | Who decides | **FAIL:** mixed machine/reviewer results have no resolution rule. |
   | One thing | Pass: it specifies requirement checking. |
   | Unit | Pass: individual requirement records. |
   | Can it fail | Pass: omitting a named record is observable. |
   | Weak words | **FAIL:** checked does not distinguish an attempted check from a supported verdict. |
   | Level | Pass: coverage serves U2. |
   | Basis | **FAIL:** a git label does not establish that git contains sufficient evidence. |
   | Links | **FAIL:** mixed records conflict with the vision’s blanket treatment of reviewer judgement. |

   Sources: [C1](/home/smoke01/dev/ancient-games/memory_check/REQUIREMENTS.md:23), [the vision](/home/smoke01/dev/ancient-games/memory_check/VISION.md:16).

   **Recommendation:** show machine findings and unresolved reviewer clauses separately. Missing evidence produces an incomplete result, never a pass. **Price:** the report needs more states than R1 currently permits.

2. **My #2 and my #9: the source-of-truth checks divide by what their evidence can establish.**

   Every id below comes from the [source-of-truth YAML](/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH_REQUIREMENTS.yaml). The methods and limits are **my reading** of its failure conditions and the existing checker.

   | Requirement ids | What can actually be established |
   |---|---|
   | **W1.1a, W1.1b** | Files establish prefix/kind consistency, id form and duplicate ids. History is needed for prefix or id changes. Complete history still cannot establish how randomly an id was selected. |
   | **W1.2a, W4.1b, K6.3a** | File structure, allowed status values and the specified conflict-marker lines are mechanical checks. Delegate these to the existing checker for the snapshot it reads. |
   | **W1.3a** | The existing checker establishes whether an active entry has a claim and a `Why` line. Whether it contains two claims remains reviewer judgement. |
   | **K6.1a, K6.2** | Run the existing checker against the staging area or a named commit. A result applies to that snapshot. Checking every relevant historical commit requires an explicitly chosen history scope. |
   | **Rd3.1a** | The existing checker enforces its interim line and byte limits. Applying owner-recorded measured limits needs a defined input and support in the checker. |
   | **W4.2** | Compare successive entry versions for appended change-log records and altered earlier records. Establishing the actual writer and matching agent activity needs evidence beyond commit authorship. Written exceptions also matter. |
   | **K4.3** | Compare committed claims, `source`, `depends_on` and `covers` with their predecessors. Detect forbidden changes and missing change-log additions mechanically, within the inspected history. |
   | **K4.1** | Git reveals deleted tracked entries; files reveal missing replacement links. Whether a retirement explanation supplies a real reason needs a reviewer. |
   | **K5.1** | History reveals edits to earlier journal content versus append-only changes. It cannot establish where all raw notes were kept. Written exceptions need inspection. |
   | **W2.1b, W5.1, K1.1** | History establishes ordering once the relevant decision and code change have been identified. It cannot determine generally whether a code change embodies a new decision, changes governed behaviour, or omits a human correction. |
   | **W6.1a** | History can show content appended to an existing file. Recognising an additional semantic entry requires judgement; an ordinary permitted addition is not automatically a violation. |
   | **W6.1b** | Git can show multiple commits to a journal. It cannot identify distinct agent sessions without session evidence. |
   | **W6.2** | Recorded branches and merges can expose losses. An overwritten edit that never reached git may leave no evidence. No detected loss cannot certify compliance. |
   | **W6.3a** | Compare a merge with both parents for missing added log lines, links and covered paths. Contested supersession and whether it was reported require task records and reviewer judgement. |

   For SHOULD requirements, the YAML permits a written exception in task state or the commit message. A detected deviation alone therefore does not always establish failure. ([Exception semantics](/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH_REQUIREMENTS.yaml:31))

   **Price:** history checks need explicit bounds and missing-history reporting. Semantic checks remain reviewer work even where their `check` field includes git.

3. **My #7 and my #13: cache inspection cannot certify cache behaviour.**

   These are the eleven groups in [CACHES.md’s Core requirements](/home/smoke01/dev/ancient-games/docs/memory-system/CACHES.md:320). Classification below is **my reading**.

   | Cache requirement | Files or git can establish | Additional evidence needed |
   |---|---|---|
   | **B1** | Presence of comparison records and EJ’s recorded decision. | Whether the comparison used correct answers and supports its claimed outcome. There is no specified machine-readable record format. |
   | **B2** | Git ignore status, including whether cache files are already tracked. | Delete/rebuild/query equivalence and rebuild side effects require an isolated execution. |
   | **B3** | A visible incremental mode is evidence of failure. | Absence of every incremental path, including row reuse, requires implementation review and execution evidence. |
   | **B4** | With a known schema, compare stored entry paths and `covers` fields with active entry headers. | A cache reader/schema contract; none is specified by these requirements. |
   | **B5** | Documentation or code may expose model calls. | An isolated rebuild with controlled model/network access. Missing credentials alone do not prove no call was attempted. |
   | **K1** | With a known schema, inspect recorded hashes and embedding-model id. | A contract locating those values and identifying current model settings. |
   | **K2** | Compare recorded hashes with current sources and compare the two indexes’ build provenance. | Query, rebuild, failure and concurrency trials establish freshness handling, exclusion and replacement behaviour. |
   | **K3** | Inspect rerun results and the subsequent keep/drop decision. | Establishing that the comparison is valid and identifying the applicable latest decision need review. Age alone is no failure. |
   | **Rd1** | A direct cache read in a known startup hook is evidence of failure. | Indirect reads require tracing or review; a static search cannot prove their absence. |
   | **Rd2** | Inspect recorded search results for entry paths. | Exercise the actual search command; database rows alone do not establish what it prints. |
   | **Rd3** | Inspect whether source files remain available without caches. | Exercise absent-cache, absent-FTS, absent-model, wrong-path and failed-rebuild cases. |

   **Recommendation:** the read-only report inspects supported formats and reports behavioural evidence or its absence. Rebuild and query trials belong in disposable fixtures, not the inspected project. **Price:** some cache requirements remain unverified until a cache implementation supplies an interface and test evidence.

4. **My #1, my #3 and my #7: fix the promises that would produce false reassurance.**

   **My reading:** these are the material problems in the four product documents.

   - **Current files versus staging.** `memory_index.py --check` reads staged objects; `--check <rev>` reads a commit. It can exit successfully when that snapshot contains no memory, including an unborn repository. Meanwhile, discovery can find unstaged memory. A successful subprocess exit cannot become a claim that current memory passes. ([Checker modes](/home/smoke01/dev/ancient-games/tools/memory_index.py:1), [early returns](/home/smoke01/dev/ancient-games/tools/memory_index.py:481))  
     **Recommendation:** identify the snapshot on every result and expose unchecked working-tree differences. If current-file certification is required, extend the existing checker rather than duplicating it. **Price:** that extension is additional scope.

   - **Reuse does not imply complete coverage.** The existing checker ignores names outside its recognised entry-name pattern and treats some inactive-entry content defects as warnings. W1.1a has broader MUST failure conditions. It also holds the interim size limits as constants. ([Path selection](/home/smoke01/dev/ancient-games/tools/memory_index.py:306), [content checks](/home/smoke01/dev/ancient-games/tools/memory_index.py:148), [limits](/home/smoke01/dev/ancient-games/tools/memory_index.py:30))  
     **Recommendation:** expose these gaps; do not translate one exit code into passes for every delegated id. **Price:** either limited coverage or changes to the shared checker.

   - **The hook and full cache audit conflict.** Cache Rd1 fails a startup hook that opens any cache file. Full B4/K1 inspection would do exactly that. ([Cache Rd1](/home/smoke01/dev/ancient-games/docs/memory-system/CACHES.md:442))  
     **Recommendation:** the startup path inspects permitted files and location metadata; full cache-content checks run on demand. **Price:** startup cannot claim a fresh, complete cache audit.

   - **U3 and R2 disagree about missing locations.** U3’s minimum acceptance includes every missing location; R2 includes missing required locations. This matters because caches are explicitly optional. The accepted use case currently wins; the conflict needs an owner decision. ([U3](/home/smoke01/dev/ancient-games/memory_check/USE_CASES.md:22), [R2](/home/smoke01/dev/ancient-games/memory_check/REQUIREMENTS.md:49))

   - **C4 invents an absence policy the guidelines do not fully settle.** Caches are explicitly optional. The guidelines do not similarly identify the whole project-memory system as optional. Nor does the YAML make absence of `AGENTS.md` a tool-checkable MUST. ([C4](/home/smoke01/dev/ancient-games/memory_check/REQUIREMENTS.md:37), [layout requirement](/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH_REQUIREMENTS.yaml:630))  
     **Recommendation:** report absence as an observed fact; leave its unresolved severity open. **Price:** fewer automatic verdicts until applicability is agreed.

   - **C1 conflates guidance with reviewer work.** The YAML defines `none` as guidance with nothing to pass or fail. W3.2 explicitly falls back to a reviewer because no secret scanner exists. Mixed `tool; reviewer` records need clause-level treatment. CACHES core requirements lack the YAML’s `check` field and consistent RFC levels. ([C1](/home/smoke01/dev/ancient-games/memory_check/REQUIREMENTS.md:23), [source definitions](/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH_REQUIREMENTS.yaml:34))  
     **Recommendation:** preserve guidance, mixed checks and unspecified cache levels without manufacturing verdicts or MUST severity. **Price:** unresolved rows cannot enter the failing-MUST warning automatically.

   - **F1 cannot fulfil U1’s entire discovery promise as written.** The guidelines name an agent-memory path, but only say user memory lives in the home folder. They supply no user-memory path or way to associate every named agent with a project. F1 also omits task-level `state.md`, `evidence/` and `journal/` locations. ([U1](/home/smoke01/dev/ancient-games/memory_check/USE_CASES.md:6), [F1](/home/smoke01/dev/ancient-games/memory_check/REQUIREMENTS.md:9), [scopes](/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md:17), [layout](/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md:109))  
     **Recommendation:** distinguish known paths, discovered instances and unspecified locations; do not search the whole home directory. **Price:** external-memory inventory requires supplied scope.

   - **R1 and R3 cannot represent operational uncertainty.** An unreadable file, missing Python interpreter, failed git command or shallow history is neither compliance nor a usage mistake. A silent exit 0 would mislead the owner. ([R1–R3](/home/smoke01/dev/ancient-games/memory_check/REQUIREMENTS.md:44))  
     **Recommendation:** add an incomplete-check result and an explicit operational-error exit policy. **Price:** the owner must settle that policy.

   - **The vision’s stale-memory promise exceeds structural checks.** A fresh index or matching cache hash does not establish that an entry still agrees with code or the outside world. Those are reviewer checks, and entries do not expire by age. ([Vision](/home/smoke01/dev/ancient-games/memory_check/VISION.md:10), [K4.2](/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH_REQUIREMENTS.yaml:508))  
     **Recommendation:** distinguish stale derived data from an outdated assertion. **Price:** semantic freshness remains unresolved by the tool.

   U4–U6 and the requirement groups remain proposed; this advice does not accept them for EJ. Their purpose links also need recording before acceptance. ([Document status](/home/smoke01/dev/ancient-games/memory_check/USE_CASES.md:3))

5. **My #19, an attributed rule in my list: build independently reviewable pieces.**

   **My reading:** these pieces each have a fixture-sized outcome:

   | Piece | Fixture and observable result |
   |---|---|
   | Requirement catalogue | Every source id appears once; semicolon-separated checks remain separate; guidance and unspecified levels survive unchanged. |
   | Project and location discovery | Distinct project and fake-home fixtures prove correct targeting, presence/absence reporting and errors for inaccessible or nonexistent targets. |
   | Existing-checker adapter | Handwritten entry/index fixtures exercise staged, committed, unstaged, untracked and unborn states; results name the actual snapshot. |
   | Git checks | Tiny histories plant a claim rewrite, deletion, log edit, rename and merge omission; incomplete histories remain explicitly incomplete. |
   | Cache inspection | Handwritten cache rows and metadata exercise active-entry membership, missing provenance, changed sources and model mismatch, where a supported schema exists. |
   | Reporting and warnings | Hand-authored result records produce exact Markdown, warning lines and exit behaviour without involving filesystem discovery. |
   | Startup integration | A fake harness invocation proves project targeting and permitted reads; installation remains subject to EJ approving the concrete settings diff. |

   **Price:** a cache schema and startup harness cannot be guessed. Those pieces remain conditional until their interfaces are known.

6. **My #2, my #7 and my #18, with #18 attributed in my list: tests need a separately established answer.**

   **My reading:** U2’s demand for exactly one failing requirement per planted break is unsafe. Requirements overlap: the same incorrect index can violate both K6.1a and K6.2. A malformed entry can prevent an index comparison from completing. ([U2](/home/smoke01/dev/ancient-games/memory_check/USE_CASES.md:15))

   Recommend fixtures with a **handwritten expected set of findings and unresolved checks**, rather than an expected single id. The worker writes each expectation from the source requirement; a second reader checks it before seeing implementation output. This follows the question-set authorship distinction already present in cache B1.3. ([B1.3](/home/smoke01/dev/ancient-games/docs/memory-system/CACHES.md:363))

   Do not generate expected indexes with the production renderer. Handwrite tiny expected indexes. For delegated checks, separately test adapter attribution and independently specified checker behaviour; agreement with the subprocess alone proves delegation, not correctness.

   Git-status comparison also cannot prove read-only operation: ignored cache changes are invisible. Compare fixture contents, paths and symlink targets before and after, including fake-home and ignored files, alongside git status. ([U5](/home/smoke01/dev/ancient-games/memory_check/USE_CASES.md:35), [F3](/home/smoke01/dev/ancient-games/memory_check/REQUIREMENTS.md:18))

   **Price:** independently reviewed expectations cost time. They reduce shared mistakes but do not prove that the guidelines themselves are correct. I performed a static review here; I did not run implementation tests.

## What I need to know

- Does the default report certify **current files, staged content, or a named commit**? If current files, the existing checker needs an agreed read-only path for that scope.
- Does startup warn about **every missing named location**, as U3 says, or only required locations, as R2 says? Which source establishes that the whole project-memory system may be absent?
- What target harness and external-memory scope apply? Without them, hook installation and complete external discovery remain conditional.
- May incomplete checks receive an explicit result and operational-error exit status? Without that, R1/R3 cannot faithfully describe unavailable evidence.

These are unresolved inputs for the main agent’s provisional decision process, not a request to interrupt the run.

## Costs and risks

- **My #7:** honest reporting will contain unresolved results. Treating them as passes would give a cleaner but misleading report.
- **My #13:** defer unsupported cache interfaces and behavioural certification; the first release will cover less.
- **My #5:** preserve read-only inspection and reviewable hook installation. Running real rebuilds would introduce changes that the tool promises to avoid.
- **My #18, attributed:** history inspection and independent fixture review add cost. No performance or accuracy improvement has been measured here.

## How we would know I was right

A reviewer can trace every verdict to its source clause and inspected evidence. Planted violations produce the independently specified findings; unavailable evidence never produces a pass. Startup opens no cache files, and fixture contents remain unchanged except for an explicitly requested report.

Recommended plan:

1. Resolve snapshot scope, absence policy, warning scope and incomplete-check behaviour.
2. Catalogue every source requirement with its evidence needs and unresolved clauses.
3. Build project discovery using repository and fake-home fixtures.
4. Wrap the existing index checker and expose its coverage gaps.
5. Add mechanically supported history checks with explicit history bounds.
6. Add cache inspection only for defined formats; verify behaviour in disposable fixtures.
7. Test reports, warnings, exits and unchanged fixture contents against reviewed expectations.
8. Present the concrete hook settings diff for EJ’s approval after the checks pass.