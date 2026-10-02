# Critic — four feature cases (2026-10-03)

Scope: judges A-unclear-requirements.md, B-migration.md, C-existing-system.md, D-new-system.md against the
"Lead-in by case" table in `docs/TASK_TYPES.md`. Numbers were checked by downloading the primary page with curl and
searching the raw text for the number (no summarizing fetch), except where the Source column says "search". n=0
throughout: nothing below has been tried in a real run.

## Numbers spot-checked

| Claim (file id) | Stated | Checked | Verdict | Source |
|---|---|---|---|---|
| B21 EquiBench best accuracy, hardest categories | 63.8% / 76.2% vs 50% random | abstract: "best accuracies are 63.8% and 76.2%, only modestly above the 50% random baseline" | confirmed | arxiv.org/abs/2502.12466 |
| B14 AlphaTrans | 96.40% syntactic, 27.03% runtime, 25.14% functional, 20.1 h / project | all four in abstract, same values | confirmed | arxiv.org/abs/2410.24117 |
| B10 Lost in Translation | 2.1–47.3%; GPT-4 8.1% on real projects, others 0% | abstract 2.1–47.3%; body: "success rates of 8.1% for GPT-4 and 0% for the rest" | confirmed | arxiv.org/html/2308.03109 |
| B12 same, feedback gain | +5.5% average | abstract: "improves ... by 5.5% on average" | confirmed | arxiv.org/abs/2308.03109 |
| B17 Airbnb | 75% in 4 h; 97% after 4 days; 50–100 retries; 1.5 y → 6 weeks | primary post (airbnb.tech, not the 403 Medium copy) has all four | confirmed — label can be raised to verified | airbnb.tech/infrastructure/accelerating-large-scale-test-migration-with-llms/ |
| B19 MigrationBench | 71.67% / 53.33% | body, same values, Claude-4.5-Sonnet | confirmed | arxiv.org/html/2505.09569 |
| C8 FeatBench | best 29.94%; regression pass 46.18% (Trae) / 29.94% (Agentless) | Table 4 "Average" row, RT% column: 46.18% and 29.94% | confirmed | arxiv.org/html/2509.22237 |
| C9 FeatBench failures | 73.6% regressive / 17.8% / 8.5%, 122 cases | body and Fig. 11 caption, same values | confirmed | arxiv.org/html/2509.22237 |
| C10 Doc2Feat-Bench | best 37.72%; GPT-4o 5.26%, Gemini-2.5-Pro 0%; single-file 53.5%/45.7%; RT 76.97%/62.06% | all values present, but GPT-4o 5.26% and Gemini 0% are **OpenHands only**; under Agentless the same models score 13.16% and 12.28% | confirmed values, condition omitted | arxiv.org/html/2507.18130 Table 4 |
| C11 SWE-Bench Pro | 43.6% public (Sonnet 4.5), 17.8% commercial (Opus 4.1) | Tables 1 and 2, same values | confirmed | arxiv.org/html/2509.16941v2 |
| C12 SWE-Bench Pro failures | Opus 4.1 35.9% / 24.2%; Sonnet 4 35.6% overflow, 17.0% endless reading | body, same values | confirmed | arxiv.org/html/2509.16941v2 |
| C13 | 7.8% of plausible patches incorrect; −4.5 points; 29.6% differ by PatchDiff | body, same values | confirmed | arxiv.org/html/2503.15223v1 |
| C14 AGENTS.md study | dev-written +2.4% (p=21%), cost +20–23%, CTXbench, `uv` 1.6× | **v3** text has all of these; the **cited v1** says "an increase of 4% on average" and names the benchmark AGENTbench. C14's note that a summarizer "got +4% wrong" is itself wrong: +4% is v1's number | confirmed against v3; citation points at the wrong version | arxiv.org/html/2602.11988 (v3) vs …v1 |
| C16 ContextCov | 88.3% vs 67.0% vs 50.3% | abstract and Table 2, same values. Caveat not in C16: compliance is scored by the same executable checks that ContextCov feeds back; a post-hoc LLM critic rated ContextCov and vanilla patches equally (30.1% vs 29.2%). Resolution 57.3% vs 53.0% supports "without hurting correctness" | confirmed | arxiv.org/html/2603.00822 |
| D6 ProgramBench | none resolves any task; best passes 95% of tests on 3% of tasks; monolithic single-file | abstract, same wording | confirmed | arxiv.org/abs/2605.03546 |
| D20 iterative security degradation | +37.6% critical vulnerabilities after 5 iterations; 400 samples, 40 rounds | abstract, same values | confirmed (abstract only; method not read by anyone) | arxiv.org/abs/2506.11022 |
| D19 Veracode | 45% of tests; Java >70% | vendor page headline 45%; Java 72% in press summaries | confirmed as reported (vendor headline, search) | veracode.com report page; search |
| D23 Lovable CVE | 170 of 1,645 apps (10.3%) | several secondary pages agree; Palmer's primary post did not render raw | consistent, unverifiable at primary | search; mattpalmer.io |
| A10 Ambig-SWE | up to 74% recovery; Sonnet 4 / 3.5 detection 89% / 84% | abstract 74%; body "89% and 84%, respectively" | confirmed | arxiv.org/html/2502.13069 |
| A11 Qwen 3 Coder | 100% FNR | body: "complete non-responsiveness to interaction prompts (100% FNR)" | confirmed | arxiv.org/html/2502.13069 |
| A12 Ask or Assume | 69.4% resolve | abstract 69.40% | confirmed | arxiv.org/abs/2603.26233 |
| A13 UnderSpecBench | 55.8–67.8% violate a boundary | abstract, same values | confirmed | arxiv.org/abs/2607.02294 |

Result: 22 claims checked. 20 confirmed as stated, 2 confirmed with a defect (C10 drops the scaffold condition;
C14 cites v1 but quotes v3). 0 wrong values. D23 unverifiable at its primary source; D19 rests on a vendor headline.

## Labels too strong

- **Abstract-only "verified"** (allowed by each file's own label rule, but the finding then rests on the authors'
  summary): A12–A16, A23, A25; B13, B14, B21–B24; D6, D7, D15, D20, D24. The ones a recommendation leans on hardest:
  - **D20** (37.6%) is the only support for D-R3's "security rescan after every fix round". Nobody read its method
    (what an "iteration" asks for, which scanner). One abstract, one paper.
  - **B21** (EquiBench) is synthetic pairs; B applies it to reviewers of real migrations (B's own gap says so). B-R9
    stands anyway on B25 and B23, but B21 is not evidence about review.
  - **A12** supports A-R6 ("stop on unclear"), but the paper's scaffold is a separate detection *agent*, not a clause
    in a brief. A-R6 is an inference from it, not an application of it.
- **Vendor or self-interested pages labelled plain "verified"** (A labels its vendor rows "no evidence of effect";
  C and D do not):
  - **D21** CodeRabbit (vendor selling AI review; authorship "assumed") — verified only that CodeRabbit said it.
  - **D19** Veracode — vendor report headline; method details read via press only.
  - **C22, D16, D17** Claude Code docs; **D14** Kiro docs — verified as "the tool advises X", not as "X works".
    D-R4 and C-R6 cite them as support; the non-vendor support there is C14/D15 and C16.
  - **D5** Thoughtworks Radar — verified that they claim it; an opinion, not evidence.
- **Secondary read as primary:** D1 cites Shank's essay in *97 Things*, not Cockburn (whose page 404'd). Fine for
  the definition, but it is a secondary source labelled verified.
- **Version mismatch:** C14 (see table). The researcher's note blames a summarizer for a number that is v1's own.
- **Too weak:** B17 can be raised to verified (primary now readable on airbnb.tech).
- **A-R3 overclaims the method:** it says a criterion that cannot be stated as an example "is already the blueprint
  template's rule". It is not. The method (§3.1 row 2) asks for "checkable acceptance criteria"; neither the method
  nor `docs/workflow-templates/blueprint.md` mentions examples. Requiring examples is a new rule.

## Overbuilt, and the minimal version

| Rec | Why too heavy for one developer at n=0 | Minimal version that keeps the benefit |
|---|---|---|
| C-R1 seven-section impact map, every entry `file:line`, then `verify-extraction` on the map | Seven sections plus a verification pass on top of each run; no source shows an impact map helps agents on features (C's own gap) | Four items: focus/extension points, one-hop callers and shared state, 3–5 convention examples, "must not change". `verify-extraction` only for a behaviour claim a build node depends on |
| C-R4 characterization tests for every uncovered entry, with sabotage | Turns every C run into test-writing | Only for "must not change" entries with no test; if most of the area is untested, tell EJ (C's own inference) |
| C-R7 repo map / code graph for large repos | Measured on bug fixes only (C20, C21); speculative | Defer |
| C-R8 tester receives parts of the impact map | Couples tester to the COO's reading; not needed for blindness | Give the tester only "must not change" (g) |
| B (11 recs as a whole) | Eleven additions for a case EJ has not run once | Keep R1/R6 merged, R2, R5, R9, R10; others conditional or deferred (list below) |
| B-R6 separate known-difference ledger | Same artifact as B-R1's port/drop/change list | One list: B-R1 rows, with "change" rows carrying the updated golden and EJ's approval |
| B-R3 old-vs-old noise baseline | Needed only when outputs are nondeterministic | Conditional: only when an old-vs-old run differs |
| B-R7 four data-check levels | Right only when data migrates | Conditional on a data migration: schema + counts + row hash; read-comparison only for live data |
| B-R8 separate retry budget for mechanical translation | Conflicts with the 2-round cap (see contradictions); evidence is other companies' tooling | Keep "small pieces in dependency order, cheapest check first"; defer the extra budget |
| B-R11 shadow / dark launch | Not EJ's case (B's own inference) | Defer; offline replay of recorded inputs |
| D-R2 walking skeleton with CI, preview deploy, sabotage, line-by-line review | Preview deploys and CI are infrastructure for a team | Skeleton = lint + test runner + one end-to-end test through every part; sabotage (break a layer, e2e fails) is cheap, keep it; CI/preview optional |
| D-R3 four fitness functions plus security rescan every fix round | Duplication threshold rests on D22 (reported, correlational); rescan rests on D20 (abstract only); cost unknown (D's own gap) | One import/layer rule if there are layers; secret scan; an authorization test per data entry point only if there is auth. Rescan = the join check already reruns whatever scan exists; no extra node. Defer duplication |
| D-R4 Kiro's three steering files | `structure.md` is a repository overview, which C14/D15 found unhelpful | One short hand-written conventions file (commands, non-standard rules, pointers to ADRs) |
| A-R1 one-screen problem statement as a new step | Method 3.0 already states objective, in/out scope, why #1 (XY guard), why #6 (done) | Add only the new part: "stop / not now" is an allowed outcome, and EJ confirms the 3.0 restatement in case A |
| A-R4 separate COO consistency pass | A separate node for a scan the drafter can do | Fold into the COO's drafting: vague-word and contradiction scan feeds the capped batch |
| A-R5 walking skeleton per slice + A-R7 size limit | Changes how many times the pipeline runs per feature; inference | One sentence: if the capped batch cannot settle the feature, settle and build the thinnest slice first. Same rule covers spec bloat |

## Shared changes (apply to all cases)

Each appears in two or more files; adopt once, above the table, not per row.

1. **Every acceptance criterion carries at least one concrete example (input → expected).** A-R3 (A4, A6 verified);
   B's goldens are this; C/D criteria need it for the blind tester. New rule — see "Labels" on A-R3.
2. **"Stop on unclear" clause in every dev and tester brief:** return `UNCLEAR: <question> / <guess>` instead of
   guessing. A-R6 (A10, A11, A13 confirmed). Underspecification is not limited to case A.
3. **Conventions and invariants as executable checks; context file short and hand-written; no agent-written
   overview.** C-R6 and D-R4 (C14 verified in v3, C16 confirmed). Also covers B-R5.
4. **Tamper guard in the join check:** golden files and the tester's cases are read-only to the dev; the join fails
   if a case disappears or the count drops. B-R5 (B19, confirmed). Equally needed in C and D.
5. **Scope check in the COO checklist:** every file in the diff is planned or has a listed reason. C-R5 (C9
   confirmed, C23). Applies to B (B11, B15: added logic, noise edits) and A.
6. **Full-suite baseline, recorded per test id** whenever code exists (C-R3; C13 confirmed). B and D's end state
   need the same record. The checklist already says "the baseline still passes"; this fixes what "baseline" means.
7. **Settle per slice, not per product/feature.** A-R5 and D-R1 make the same move from different ends.
8. **Behavioural equivalence or regression is answered only by execution, never by an LLM read.** B-R9, C-R1's
   verify-extraction step, and C16's body (LLM reflection did worse than nothing).

## Contradictions and hand-offs

- **The table mixes two axes.** A is "are requirements clear?"; B/C/D are "what system exists?". A unclear feature on
  an existing system is A then C; on a new system A then D. B is "clear" by definition, so A never precedes B.
  The case name should be two answers, and A's lead-in runs first when it applies. None of the four files says this.
- **D ends as C** (D-R6). **B also ends as C:** once migrated, the next feature is on an existing system, and B's
  goldens become part of C's baseline. Not stated in B.
- **C can turn into B-like work:** C-R4's inference (untested area → characterization first) is B's method on a
  local scale. Name it, do not create a fifth case.
- **Retry limits conflict.** B-R8 wants a larger bounded retry budget for mechanical translation (B12, B17); D-R3
  keeps the 2-round cap and warns that fix loops degrade security (D20). Pick the 2-round cap (it is the method's
  current, documented rule); flag B-R8 for a decision after a real migration run.
- **"Walking skeleton" means two things.** A-R5: thinnest end-to-end slice of a feature. D-R2: architectural
  scaffolding through every part. Use different names in the table or EJ will get blended rules.
- **D-R4 contradicts itself:** it cites D15 (overviews do not help) and then recommends Kiro's `structure.md`.
- **Throwaway vs grow.** A-R3 deletes the prototype; D1 grows the skeleton. Consistent only if the table says which
  artifact is which; currently not.
- **A-R2 batches questions; A18 (Spec Kit clarify) asks one at a time.** A's own gap admits no evidence either way.
  The current row ("one batch") stands; no change.
- **C14 and D15 cite the same paper at different versions with different numbers.** Use v3 in both.

## Missing per case

- **A.** (1) An entry test for "clear": the INVEST Testable test (A4) — if every criterion can be written as an
  example, it is not case A. (2) What happens when dev and blind tester disagree because of an ambiguity (A's own
  "What goes wrong" 2): route it to EJ's next batch, not into the 2-round fix loop. No recommendation covers it.
  (3) Non-functional requirements (performance, security) are only touched via vague-adjective scans.
- **B.** (1) Rollback and backup before any data migration — irreversible, Rule 6; not mentioned. (2) Side effects
  of the old system (emails, files, external calls) in goldens: B24 mocks externals, but no recommendation records
  or stubs them. (3) Non-functional parity (latency, memory, error messages users see). (4) What happens when the
  old system goes away — goldens must be frozen before decommission.
- **C.** (1) Schema or data changes inside an existing system (C's data migration is B's material, not cross-
  referenced). (2) Cost of the full-suite baseline when the suite is slow; no budget rule. (3) Lint and type check
  as part of the baseline, not only tests. (4) A requirement found unclear during the scan → back to A.
- **D.** (1) Build-or-reuse check before scaffolding (an existing library or tool may make the system
  unnecessary) — the "kill" exit A-R1 adds is missing here. (2) Dependency pinning and checking that every package
  an agent adds exists and is the intended one. (3) Data-migration tooling from day one, since the next feature is
  case C and will change the schema. (4) Secrets handling (D23's failure was exposed keys as well as missing RLS).

## Recommended adoption list (keep / shrink / defer, per recommendation, with one-line reason)

Shared (adopt once): S1 examples in criteria — **keep** (A4, A6 verified). S2 stop-on-unclear clause — **keep**
(A10, A11, A13 confirmed). S3 executable conventions + short hand-written context file — **keep** (C14 v3, C16
confirmed). S4 tamper guard — **keep** (B19 confirmed). S5 scope check line in checklist — **keep** (C9 confirmed).
S6 full-suite per-test baseline — **keep** (C13 confirmed). S7 settle per slice — **shrink** to one sentence
(inference; A7, D11, D12 verified opinion only). S8 execution-only equivalence — **keep** (B25 n=1, B23, C16 body).
Two-axis case naming (A first, then B/C/D) — **keep** (no evidence needed; it removes a category error in the table).

| Rec | Verdict | Reason |
|---|---|---|
| A-R1 problem statement | shrink | 3.0 already has it; add only "not now" as a valid exit (A19 tool doc, A9 author claim) |
| A-R2 ≤5 questions, ranked, multiple-choice, answerable only, assumptions list | keep | A11, A15 (abstract) support the filter; cap matches row's "one batch" |
| A-R3 examples mandatory, prototype conditional | keep (as S1); prototype part shrink | Prototype evidence is A24 reported + A25 abstract; keep "accept the list, never the prototype" |
| A-R4 consistency pass | shrink | Fold into drafting; no separate node |
| A-R5 skeleton-first reorder | shrink | One-sentence slicing fallback (S7); inference, changes pipeline count |
| A-R6 stop-on-unclear | keep | = S2 |
| A-R7 size limit + Q→A log | shrink | Log Q→A in decisions.md; size limit replaced by S7 |
| B-R1 port/drop/change list (+ B-R6 merged) | keep | B3, B4 verified; one list, not two |
| B-R2 oracle = recorded old output, not description | keep | B25, B23, B24 |
| B-R3 noise baseline | shrink | Only when old-vs-old differs (B6, B7 verified) |
| B-R4 golden inputs aimed at measured bug classes | shrink | A checklist line for the tester (B11 verified); encoding/tz/rounding are inference |
| B-R5 tamper guard | keep | = S4 |
| B-R7 data checks | shrink | Conditional on data migration; schema + counts + row hash (B8, B9) |
| B-R8 small pieces in dependency order; extra retry budget | shrink | Keep ordering (B14, B15); defer the budget — conflicts with 2-round cap |
| B-R9 no LLM-only parity verdict | keep | = S8 |
| B-R10 readiness: must be able to record old outputs | keep | One line; follows from B-R2 |
| B-R11 shadow / dark launch | defer | Not EJ's single-developer case |
| C-R1 impact map | shrink | Four items, not seven; verify-extraction only on load-bearing claims |
| C-R2 depth: systematic in area, budget, prefer recall | keep | C12, C18 verified; one-hop is a guess, mark n=0 |
| C-R3 full-suite baseline per test id, run twice for flaky | keep | = S6 |
| C-R4 characterization tests for gaps | shrink | Only for "must not change" entries without tests |
| C-R5 scope check | keep | = S5 |
| C-R6 executable conventions | keep | = S3 |
| C-R7 repo map / code graph | defer | Bug-fix evidence only (C20, C21) |
| C-R8 tester gets impact-map parts | shrink | Only the "must not change" list |
| D-R1 two-tier blueprint rule | keep, as EJ's decision | Changes method §3.1 "all eight"; evidence is n=1 practitioner (D11, D12) and inference — EJ's call, not the critic's |
| D-R2 walking skeleton node | shrink | Lint + tests + one e2e + layer-break sabotage; no CI/preview requirement |
| D-R3 fitness functions + rescan | shrink | Secret scan, authz test if auth, one layer rule; duplication and per-round rescan deferred (D22 reported, D20 abstract only) |
| D-R4 conventions file | shrink | = S3; drop `structure.md` |
| D-R5 mainstream stack + ADR | keep | One line; D24 abstract, D4 verified |
| D-R6 D ends as C | keep | Also add "B ends as C" |
| D-R7 small per-slice specs | keep | D11, D12, D13 verified (opinion/n=1), matches Claude Code doc D17; costs nothing |

Decision this triggers for EJ: whether to restructure the table into two questions (requirements clear? then
which system) with eight shared lines above it, and whether to amend method §3.1's "new product → all eight
settled" (D-R1). Everything else is a shrink or a one-line add, n=0, and per house rules none becomes a rule
before two real runs.
