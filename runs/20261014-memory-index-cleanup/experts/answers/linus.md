# Linus Torvalds — Missing facts and reversible choices

## Answer

*My reading:* Keep the two-check scope, but resolve the gaps in baseline preservation, engine readiness, verification and rollback before building. Keep experiments isolated and preserve their starting inputs so a mistaken choice can be reversed without disturbing another session’s work.

| Spot | Verdict |
|---|---|
| **Q1** | **EJ’s decision; technical evidence pending.** Test the chosen starting commit, including `d990dab` if used. Its reported test count does not establish compatibility with current master. An isolated integration branch preserves both histories; merging first increases coordination cost. |
| **Q2** | **EJ’s acceptance pending.** Freeze the wording before N1. Later changes invalidate affected tests and evidence, costing a rerun; preserving each spec version makes that change traceable. |
| **D1** | **Keep provisionally.** Form validation does not require calendar validation. Test a correctly shaped but impossible date as accepted; the price is intentionally accepting such dates. |
| **D2** | **Keep provisionally; coverage incomplete.** Every status includes `superseded`, but N1 names only active and retired cases. Include superseded coverage; the cost is additional cases, and the benefit is detecting a status-specific bypass. |
| **D3** | **Keep provisionally.** Test both specified prefixes and preserve acceptance of `=======`. Scanning every raw entry line would cover header and body without depending on successful header parsing; whether the current reader permits that is unknown. Literal examples starting with those prefixes will also be rejected. |
| **D4** | **Keep.** The backlog stays outside this change. The price is leaving known defects unresolved; recording them preserves a separate future choice. |
| **D5** | **Keep as optional evidence.** If the evaluator is absent, report the skip. If present, establish what it checks before relying on its result; availability alone does not establish usefulness. |
| **N1 — Character and parsing boundaries** | **Missing information; blocks precise tests.** Does “digits” mean ASCII `0–9`? Does validation examine the parsed id exactly, or a trimmed value? Test whole-value matching and line-prefix boundaries once those meanings are settled. Changing the interpretation later costs fixture and test revisions. |
| **N2 — Fixture migration and baseline** | **Missing evidence; blocks claiming baseline preservation.** Preserve the original fixtures and map each changed id to its assertions. Against unchanged code, migrated existing cases should retain their expected results. Green tests after rewriting inputs alone do not prove their original coverage survived. |
| **N3 — Current engine capability** | **Unknown until canaries run.** Installed binaries and earlier successful calls do not prove current access or writable execution. Use isolated canaries with the specified models and modes; stop dependent work on failure. Their cost is a small amount of time and usage. |
| **N4 — Strength of verification** | **Unknown until demonstrated.** Mutants must distinguish disabling each check from bypassing a mode, status or file region. A killed broad mutant does not prove those boundaries. The review plant’s relevance is also unspecified. Keep all sabotage in disposable copies; additional coverage costs test time. |
| **N5 — Reversal and change authority** | **Contradictory instructions; resolve before mutation.** The design both reserves commits for EJ and calls for frozen/checkpoint commits. It also edits spec files in the main tree. Agree on checkpoint authority and preserve existing changes before editing; otherwise rollback could disturb unrelated work. |
| **N6 — Repair bounds** | **Accounting incomplete.** N1 permits three calls, N2 five and N4 two: ten worker calls before separately accounting for N3 repairs and contradiction returns. The stated maximum of eight is unsupported. Clarify which limits repairs consume; otherwise the stopping rule and cost estimate can drift. |

## How I decided

1. **My #2 and #7:** Separate observed capability from promises. Earlier results support trying the same tools; current canaries and baseline runs establish whether this run can proceed.
2. **My #9 and #10:** Start with the data boundaries: the complete parsed id and every entry line. If both modes share validation, place the checks there; if they do not, demonstrate both paths. I have not inspected the implementation.
3. **My #1 and #3:** Preserve existing useful behavior. Fixture migration is necessary, but passing rewritten tests alone is insufficient evidence that unrelated behavior survived.
4. **My #5 and #12:** Preserve starting revisions and another session’s history. Discarding an isolated experiment is reversible; rewriting shared history or overwriting existing edits has wider consequences.
5. **My #13:** Keep the immediate need small. Calendar validation and unrelated backlog repairs add requirements that this brief does not authorize.
6. **My #18 and #19, both `attributed` in my list:** Explain costs and keep changes independently understandable. Deliberately failing tests are useful evidence snapshots; they should be identified as such rather than presented as green integration checkpoints.
7. **My reading — requirement check:** For the proposed checks, **source, one thing, unit, can it fail, weak words, basis and links pass provisionally on the supplied brief**. **Level fails:** the spec does not identify requirement levels. N1 separately raises a character-set ambiguity; N5 and N6 raise contradictory authority and incomplete attempt accounting.

## What I need to know

- **Q1/Q2:** Does EJ accept the starting-base choice and proposed wording, and what requirement level applies?
- **N1:** Are digits ASCII, and is the parsed id validated without further trimming?
- **N5:** Are private checkpoint commits authorized, and how will existing main-tree spec edits be preserved?
- **N6:** Do repair and contradiction calls consume existing attempt limits, or have separate limits?

Canary success, baseline preservation and mutant applicability are technical questions for the workers to establish with evidence.

## Costs and risks

- **My #5:** Isolation makes file changes reversible; it does not recover spent time, usage or trust.
- **My #3:** Stricter validation intentionally rejects previously accepted malformed entries. The brief reports no live deployment, which reduces migration exposure but does not prove the absence of other callers.
- **My #2 and #7:** The COO wrote the trace, gate and sabotage checks. Their results demonstrate the particular failures exercised; they do not establish complete correctness or independent verification.
- **My #18 (`attributed`):** The 45–90 minute estimate is *not measured* for this cleanup, and its call accounting needs correction.

## How we would know I was right

The selected starting revision passes its recorded baseline; migrated fixtures preserve existing assertions; unchanged code fails exactly the newly introduced acceptance cases; corrected code passes both modes and all statuses; boundary-specific mutants expose omitted validation paths; and the reviewer finds the relevant plant.

Reversibility is demonstrated when a failed experiment can be discarded while the original revisions, existing edits and other session’s history remain intact. These are proposed observations, not checks I have run.