# Linus Torvalds — Missing facts and reversible choices

## Answer

**My reading, through my #2, my #5 and my #9:** use the measured LanguageService result as a starting point, and keep implementation discovery, test wiring and presentation separable so a mistaken choice can be replaced without rebuilding the tool. Keep the following spots open; technical probes can reduce uncertainty, but acceptance and scope decisions belong to EJ.

| Spot | Verdict |
|---|---|
| **U1 — requirements acceptance** | **Decision remains open.** P3 already waits for EJ’s acceptance. Treat preparatory work as provisional, with no promise that its interface will survive acceptance. Reversibility: isolate draft interfaces and retain evidence that remains useful if requirements change. Price: some preparation may be discarded. **My #5, my #7.** |
| **U2 — Effect implementation lookup** | **One success establishes feasibility at that site, not its miss rate.** Compare stock lookup with source-established targets across the Effect patterns actually present in the selected modules. If stock lookup finds those implementations, omit the fallback for those cases; if it misses, add the demonstrated rules separately. Preserve the declaration, candidate implementations and discovery evidence rather than silently choosing one. Price: more probes and potentially two resolution mechanisms. **My #2, my #5, my #9.** |
| **U3 — tests with replacement layers** | **Implementation candidates do not establish which implementation a test reaches.** A replacement that supplies its own method should not count as reaching the production method unless another established path reaches it. Trace the layer wiring for each relevant test setup; mark wiring that cannot be settled. Reversibility: keep test-context selection separate from implementation discovery. Price: extra analysis and incomplete results for dynamic setup. **My #2, my #9.** |
| **U4 — entry flows** | **Decision remains open.** The proposed definition is implementable, but an internally called export used outside the module and a cycle with no uncalled function expose its consequences. Show those consequences to EJ before making the definition an acceptance rule. Reversibility: derive entry flows from the graph rather than making entry status part of the graph’s identity. Price: changing the definition changes which flows appear. **My #4, my #5, my #9.** |
| **U5 — siblings** | **The classification rule is underspecified.** Export compatibility, identical exported member names and common implementation concerns can produce different sibling groups. Present positive and negative examples from the proposed modules to EJ. Reversibility: retain per-file facts and make grouping replaceable. Price: grouping may need correction, and a grouping alone does not prove shared behaviour. **My #2, my #5, my #9.** |
| **U6 — finding code from words** | **A lexical ranking is a testable proposal; its adequacy is not measured.** Evaluate descriptions whose intended locations were fixed before ranking was tuned, including descriptions with several plausible matches. Keep ranking separate from symbol resolution and expose competing results. Price: noisy candidates; any acceptance threshold remains open. **My #2, my #5, my #18 — attributed.** |
| **U7 — answer-key blind spots** | **Open evidence risk.** Confirming quoted text does not establish that a key contains every relevant path or interprets wiring correctly. Corroborate consequential answers through the other methods already proposed in P1, and preserve disagreements. Reversibility: version keys and recompute scores when corrected. Price: independent checks take time; previous scores may change. **My #2, my #7.** |
| **U8 — Codex quota** | **Availability remains a runtime fact.** Today’s successful calls do not establish capacity for the remaining evaluator and test work. Keep those pieces resumable with their briefs and evidence intact. A quota failure should leave dependent work waiting rather than treating an unavailable check as passed. Price: delay; changing engines would also change the independence arrangement. **My #5, my #7.** |
| **N1 — source/test program boundary** | **New unknown; blocks P3 A3.** The successful probe loaded source only. The proposed combined source/test program has not established that package imports resolve to implementation source with the required compiler options. Probe that before committing to the host design. Reversibility: isolate project loading from graph construction. Price: configuration work and potentially greater memory use. **My #2, my #5.** |
| **N2 — references versus calls** | **New unknown; blocks P3 R2 and dependent chains.** The COO did not inspect the 19 references individually. A reference can identify a use without establishing a caller edge; passing a function as a value also requires more reasoning than locating its reference. Check enclosing functions and actual call sites, including Effect wrappers. Reversibility: retain reference evidence separately from derived call edges. Price: fewer claimed edges until established. **My #2, my #9.** |
| **N3 — evaluator coverage of R3** | **New check gap; blocks an R3 MET verdict.** Socket blocking tests network behaviour of the tool, while R3 also concerns git and outside engines. Establish which components own those routes and which checks cover them. Reversibility: retain separate results for checked and unchecked obligations. Price: a narrower verdict until the remaining obligations have evidence. **My #2, my #7.** |
| **N4 — measurement after tuning** | **New unknown; blocks claims of effectiveness beyond the tuning questions.** P5 improves the tool on the questions it reruns. Those results can describe improvement on those questions, but cannot establish performance on new ones. Keep original results and evaluate untouched questions separately if broader effectiveness is claimed. Price: additional questions and runs. **My #7, my #18 — attributed.** |

## How I decided

1. **My #2 — start with demonstrated behaviour.** The COO’s probe established one implementation link, failure of stock call-hierarchy preparation at the tested locations, and source-program construction cost. It did not establish a repository-wide resolution rate, correctness of every reference, or test-layer selection. Those remain separate claims.

2. **My #9 — distinguish the relationships in the data.** A declaration, an implementation candidate, a call site and a test’s selected implementation answer different questions. U2, U3 and N2 become harder to correct if they are collapsed into one certain-looking edge. My proposed separation is an application of the rule, not a measured design result.

3. **My #5 — make replacement possible before choosing.** Project loading, implementation discovery, layer selection, entry classification, sibling grouping and ranking can change independently. Keeping their evidence intact makes correction possible without losing the observations that justified earlier choices.

4. **My #4 and my #7 — distinguish technical uncertainty from EJ’s decisions.** Workers should bring evidence about resolver behaviour and graph construction. EJ decides whether the resulting product definition is acceptable. U1, U4 and the policy parts of U5 and U6 should not be settled by an implementation accidentally becoming the specification.

5. **My #13 — test the immediate problem before expanding the machinery.** Start with the patterns present in the selected modules. If those demonstrate a need for the static Effect resolver, implement that need. I would not add another analyser merely because the research names one. The tradeoff is limited generality, explicitly reported.

6. **My #18 — attributed — measure the whole comparison.** The source-only build cost is useful evidence, but not the cost of a complete answer. P5 needs the specified tokens and time for both arms, including map construction. P6 also needs demonstrated tool use before attributing differences to the installed skill.

7. **My reading — requirement-quality check.** For the COO’s proposed sibling-classification rule: **source passes** because its author is named; **one thing passes** because it classifies files; **unit passes** because the objects are files; **basis passes when labelled an unmeasured proposal**; **links passes** because the spec explicitly connects it to A1. **Weak words fails** because export equivalence is undefined; **can it fail fails as an acceptance check** until agreed examples distinguish correct from incorrect grouping; **level remains open** because provisional grouping and an acceptance gate have different consequences. Those gaps go to EJ rather than receiving invented definitions.

## What I need to know

- **U1:** Does EJ accept the draft requirements, including their proposed additions?
- **U4:** Does EJ accept the proposed entry definition after seeing its treatment of cycles and externally used exports?
- **U5:** What makes two files siblings, and is automatic grouping a provisional aid or an acceptance condition?
- **U6:** What observable result would make description search acceptable? No ranking threshold has been supplied.
- **N3:** Which component is responsible for preventing protected maps from entering git or outside-engine prompts?

The remaining missing facts should come from probes: implementation misses, test wiring, project resolution, actual caller edges and runtime availability.

## Costs and risks

- **My #5:** Replaceable components still cost engineering effort. Deleting provisional code cannot recover time already spent.
- **My #7:** Preliminary work must remain visibly preliminary; passing a narrow check can otherwise create unwarranted confidence.
- **My #9:** Preserving uncertainty makes answers longer and sometimes less decisive, but avoids treating candidates as established paths.
- **My #18 — attributed:** Independent corroboration and untouched evaluation questions consume tokens and time. Their cost belongs in the reported comparison.
- **My #3:** A lower unclear-spot count in P6 is not automatically better. It could mean that the agent missed uncertainty. Assess the resulting design’s correctness.

## How we would know I was right

The proposed checks would establish observable results:

- Resolver probes distinguish source-established implementations, alternatives and unresolved targets across the selected patterns.
- A test with a complete mock replacement links to that mock; a test using the real layer links to production; uncertain wiring remains marked.
- Source/test loading reaches implementation source, and inspected references produce only justified caller edges.
- Changing entry, sibling or ranking policy preserves the underlying definitions and call evidence.
- Each R3 obligation receives supporting evidence or remains NOT CHECKED.
- P5 reports both arms’ complete cost and correctness, with tuning results distinguished from untouched-question results.
- P6 confirms tool use and checks design quality alongside counts.

**Not measured:** I have reviewed the supplied artifacts; I have not run these proposed probes. The COO ran the existing one-site probe, and the Claude researcher assembled the findings. Neither establishes the full tool’s correctness or effectiveness.