# Linus Torvalds — What does 80% coverage mean?

## Answer

**My reading:** EJ’s process holds up as a way to discover and prioritize tests; its percentage becomes misleading when an AI controls what counts as a case. Keep EJ’s 80% target, but count distinct, reviewed behaviors tied to the requirement, reuse old tests only where their assertions still apply, and treat permission to omit a case as a separate decision from its estimated rarity.

## How I decided

1. **My #9 — define the data before calculating the percentage.**  
   My application: each case should identify the situation, the action, and the observable result that would show the requirement met or broken. AI can suggest cases from the requirement, existing workflows, past failures, boundaries, invalid inputs, and interactions with affected behavior. That produces candidates; it does not establish completeness.

   **Concrete break:** an AI generates many valid-input examples for an import requirement but misses interruption halfway through writing. Testing every generated example would still miss partial data loss.

   **Price:** someone must review the cases against the requirement and affected workflows. Another AI list can expose omissions, but agreement between lists does not prove completeness.

2. **My #9 and my #10 — count behavior, rather than variations in wording.**  
   My proposal: count distinct reviewed cases, with multiple inputs grouped when they exercise the same behavior and failure mechanism. Keep separate cases where a boundary, state, or interaction could change the result.

   Use:

   `coverage = distinct reviewed cases exercised by applicable passing tests / all distinct reviewed cases`

   Keep deferred cases in the denominator. Show failing and untested cases separately. A test that ran and failed establishes a detected defect, not evidence that the requirement is met.

   **Concrete break:** eight passing cases out of ten gives 80%. Adding ninety passing variations of those same eight behaviors gives 98%, while the same two behaviors remain untested.

   **Price:** deciding whether cases are equivalent takes judgment. The grouping can itself hide a meaningful difference, so its rationale needs review. This percentage describes the reviewed list; it does not establish 80% of possible behavior or usage.

3. **My #1 and my #3 — preserve working user behavior when reusing old cases.**  
   Checking old cases is a strong part of EJ’s process. My application: map each old test’s actual assertions to the current requirement, check that its setup still applies, and rerun it against the changed implementation. A test’s name or historical pass is insufficient.

   **Concrete break:** an existing save test checks that the operation returns success. A new requirement concerns reopening the saved content. The old test does not establish that result.

   Also check affected old workflows beyond the new requirement. A seldom-used workflow can still be something users depend on.

   **Price:** maintaining old tests costs time. My #3 also warns against equating every changed test result with user breakage: investigate the effect before preserving an obsolete assertion.

4. **My #5 — rarity alone does not justify omission.**  
   My application: consider what happens if the case fails and whether the damage can be undone. An unsupported frequency estimate is not evidence.

   **Concrete break:** a rare interruption permanently corrupts saved work, while a common display glitch disappears on refresh. Calling the first case rare does not establish that skipping it is acceptable.

   The main agent’s added clause protects cases marked basic, but it leaves two holes: the labels can be wrong, and a rare case can have unacceptable consequences. I would propose documenting the consequence, evidence, and reason for each omission, with acceptance by whoever EJ authorizes to accept that consequence.

   **Price:** this requires more judgment than two labels. It does not require testing every imaginable edge case.

5. **My #4, my #6, and my #14 — delegate technical classification without silently delegating acceptance of harm.**  
   My answer to the open question: **the plan writer proposes classifications and reasons; a reviewer who understands the affected behavior challenges them.** That reviewer should examine the case inventory and claimed coverage as well as proposed omissions. Reviewing only the rare list cannot catch a missing case or an incorrectly claimed test.

   If EJ delegates acceptance of omissions, the designated owner can decide within that authority. Otherwise, the consequential omissions come to EJ with the technical evidence.

   **Concrete break:** the writer omits a failure mode entirely. EJ reviews every listed rare case and never sees it.

   **Price:** review adds effort, and independence does not guarantee domain knowledge. Having EJ label every case instead risks making them the technical bottleneck.

6. **My reading — the draft is still incomplete under the requirement check.**  
   Applied to R11.1:

   - **Who decides — FAIL:** classification and omission authority remain open.
   - **One thing — pass:** it describes an eval plan and its contents.
   - **Unit — FAIL:** listed cases are named, but their grain and equivalence are undefined.
   - **Can it fail — pass for the written checks:** seven covered cases out of ten misses the target; an uncovered basic case contradicts the added clause. Neither establishes that the list is adequate.
   - **Weak words — FAIL:** basic and rare lack operational meanings.
   - **Level — pass only with the supplied context:** 80% remains a target. The added omission clause remains a proposal, not EJ’s adopted rule.
   - **Basis — incomplete:** 80% is explicitly EJ’s unmeasured target, n=0; when to reassess it is open.
   - **Links — pass:** no unsupported relationship to another rule is asserted.

7. **My #13 and my #2 — try the smallest useful comparison before adopting a method.**  
   My proposal is to compare the current process and the revised approach on the same requirement and implementation, using the checks below.

   **Price:** preparing the comparison takes work. It may show that the added review costs more than it contributes. No improvement has been measured yet.

## What I need to know

- Who can decide that two cases count as one, and who understands the affected user workflows well enough to review that decision?
- What makes a case basic or rare, what evidence supports rarity, and whose authority covers accepting the consequence of leaving it untested?
- Does EJ want 80% counted over the reviewed distinct cases described above, and when should that unmeasured target be reassessed?

## Costs and risks

- **My #9 and my #10:** grouping cases reduces padding but can conceal meaningful differences.
- **My #1 and my #3:** regression coverage needs maintenance; retaining an old assertion without checking its user relevance can preserve the wrong behavior.
- **My #4, my #6, and my #14:** delegation reduces EJ’s workload but depends on competence and explicit authority.
- **My #5:** testing rare failures can cost more than their expected benefit; omitting them can create damage that cannot be reversed.
- **My #13 and my #18 (`attributed`):** the proposed review may be too expensive. Compare its observed benefit with its preparation, execution, and review effort.

## How we would know I was right

**My application of my #2, my #7, and my #18 (`attributed`):**

Have a reviewer other than the plan writer prepare faults tied to the requirement: a broken basic behavior, a broken existing workflow, and a rare failure with a stated consequence. Compare what each process detects, what it explicitly defers, and the effort each consumes.

Before trusting any check, show it failing on a planted wrong input. An empty inventory, zero denominator, or missing expected result should produce an incomplete result, never successful coverage.

Also add duplicate case descriptions without changing behavior or tests. The revised coverage figure should stay unchanged. Add a genuinely distinct untested behavior: it should change the denominator and appear as uncovered.

The proposal earns support if it detects a relevant failure the current process misses, or makes the same failures visible with less effort. These are **checks I propose**, not independent evidence already obtained; passing them would not prove completeness or validate 80% as the right target.