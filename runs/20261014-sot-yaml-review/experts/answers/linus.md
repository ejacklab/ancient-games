# Linus Torvalds — YAML requirements agents can follow

## Answer

My reading: this draft preserves the words, but reliable agent compliance is **not measured**, and several checks contradict or incompletely describe their requirements. Keep EJ’s Markdown/YAML split; use individually levelled clauses, checks beside those clauses, explicit links, and decision authority attached to each unresolved choice.

## How I decided

1. **Keep the useful structure — my #9 and my #13.**

   Keep the Write / Keep / Read groups, requirement identifiers, level definitions, and separation of requirements from explanation and history. These serve the current reader without requiring a future requirements engine.

   Preserve existing identifiers when splitting requirements: subordinate clause identifiers can retain the connection to W1.1, for example. The price is more records and migration review; losing the connections would make existing references harder to follow.

   My reading: the COO’s round-trip check establishes textual preservation. It does not establish completeness, consistency, or agent compliance.

2. **A — split the operative text into clauses with one level each — my #9 and my #10.**

   The current representation makes an agent reconcile two descriptions: the full paragraph and the summary under `level`. Those descriptions can diverge. W1.1’s level summary, for example, explicitly requires unique identifiers, while its paragraph describes decentralized identifier generation without stating uniqueness as directly.

   Prefer the same record shape throughout: identifier, one scalar level, operative text, and applicable check. Split independently governed actions; keep a condition and its exception together. Put explanatory material in Markdown or a clearly separate explanation field.

   Fold Rd2’s `items` into the relevant clauses too. A restriction should carry its level directly, rather than inheriting it through a separate list and a summary referring to the remaining items by count.

   **Price:** splitting can accidentally alter meaning or lose exceptions. Review each resulting clause against the original; text equality alone will no longer suffice.

3. **B — place failure conditions beside each normative clause — my #9 and my #17, applied by analogy.**

   A group check currently merges different levels and different checks. W1’s check treats missing sections as failure although some sections are SHOULD defaults. W4’s check similarly combines a SHOULD change-log practice with MUST status restrictions.

   An agent needs to distinguish a MUST violation from a SHOULD departure accompanied by a written reason. Guidance needs no pass/fail test.

   Retain a shared group check only where it genuinely tests several requirements together, and identify those requirements explicitly. Do not copy the same check into several records.

   **Price:** additional check maintenance. The benefit is that failure can be attributed to the exact obligation and handled at its stated level.

4. **C — add explicit links with their purpose — my #9.**

   A bare reference cannot distinguish an exception from a dependency or an explanation. Rd5.4 supplies exceptions to Rd5.3; that relationship affects behavior and should be visible when an agent reads Rd5.3.

   Prefer a link target plus its relationship, with the operative condition still understandable locally. Resolve external document references to actual paths and sections. Preserve short references in prose where they help readability.

   **Price:** structured links require maintenance. A resolving link proves that its target exists; it does not prove that the asserted relationship is correct.

5. **D — identify who decides each open choice — my #4 and my #6.**

   Add `who_decides` where a requirement leaves a choice open, identifying the choice as well as the decider. A generic field naming EJ on every requirement would hide the problem.

   Rd5.3 already names EJ as the mismatch decider. Other choices remain unresolved: who judges whether a journal observation merits an entry, who determines the applicable start-file limits, and who performs the judged checks?

   Keep decision authority distinct from execution and review. An agent may write the report while EJ decides the disposition.

   **Price:** assigning authority requires actual decisions. Leave unresolved authority visible until EJ settles it; do not invent owners or approval stages.

6. **Fix behavioral ambiguities before claiming a better layout — my #17; the findings below are my reading.**

   - **Exceptions disappear in checks.** Rd2’s group check appears to reject loading superseded entries even when following a link is permitted. Rd5’s check does not repeat the exclusions in Rd5.4. Make each check respect its requirement’s exceptions.
   - **Reading scope differs.** Rd4.1 requires reading covering entries; its failure condition mentions covering decisions. Define whether inactive entries are excluded, particularly given Rd4.4.
   - **Retirement assumes a replacement.** K4.1 and its check require a replacement link for retired entries. What happens when an entry is withdrawn without replacement?
   - **Change instructions conflict on a literal reading.** K1.1 directs changing an entry before code, while K4.3 prohibits rewriting committed claims. State the supersession operation explicitly where that is intended.
   - **Gate scope is unclear.** The general MUST definition stops work, while Rd5.3 permits unaffected work to continue. Define what work a failed gate blocks.
   - **A required check is absent today.** Rd3 requires the K6 check to reject an oversized index; the supplied facts say current automation does not implement that check. Distinguish required behavior from implemented behavior.
   - **Index overflow has no stated response.** Keeping every active entry in the index and fitting a finite start-file limit eventually requires a decision if memory grows sufficiently. The draft supplies no recovery behavior.
   - **Timing evidence is weaker than the timing rule.** W5 and K1 commit checks can establish that entry and code coexist in a commit; they cannot establish which was written first inside that commit.
   - **Private state and readable agent memory need a boundary.** W3.3 and Rd4.5 need an explicit distinction so an agent does not interpret permission to read agent memory as permission to inspect private state.

   **Price:** these are product decisions, not mechanical formatting repairs. Resolving them takes discussion and may change existing checks.

7. **Apply the eight requirement checks — my reading, using the requirement-check skill.**

   This is a draft-level assessment, not certification of every clause.

   | Criterion | Assessment |
   |---|---|
   | Who decides | **FAIL:** several judgments and limit choices lack a decider. |
   | One thing | **FAIL:** some records combine independently governed events. |
   | Unit | **FAIL for Rd3:** the operative limit needs its actual measurement units; example KB and line counts do not define it. |
   | Can it fail | **FAIL in places:** concrete failures exist, but checks omit obligations or reject permitted exceptions. |
   | Weak words | **FAIL in places:** journal selection and applicable limits remain open without assigned resolution. |
   | Level | **FAIL in places:** clause summaries and group checks do not consistently preserve MUST/SHOULD distinctions. |
   | Basis | **PASS for traceability:** labels and paths exist. That does not establish measured effectiveness. |
   | Links | **FAIL for complete relationships:** targets are often named, but behavioral relationships and their justification need review. |

   The price of completing this assessment clause by clause is reviewer time. Adding fields without resolving these failures would merely encode the ambiguity.

## What I need to know

- Who judges journal selection, semantic compliance, and SHOULD departures? If agents decide these themselves, say so; if a reviewer decides, name that role.
- Who selects the participating agents and their applicable limits, and what should happen when the index exceeds them?
- May an entry be retired without replacement, and precisely which activity stops when a MUST fails?
- Does reliable following mean fewer missed requirements, fewer incorrect actions, less clarification, or some combination? EJ needs to choose the acceptance criterion before the comparison is judged.

## Costs and risks

- **More explicit records mean more maintenance** — my #9 and my #17. Keep fields tied to an actual reading or checking need.
- **A split can change semantics despite preserving vocabulary** — my #1, applied by analogy. Preserve identifiers and review exceptions during migration.
- **A larger format may consume more context** — my #18, which the list labels `attributed`. YAML’s token cost and compliance benefit remain unmeasured here.
- **Additional authority fields can create a bottleneck** — my #4 and my #14. Assign only the choices that require a decision; retain EJ’s stated mismatch authority.
- **This recommendation may be wrong** — my #7. Keep the layout revision reversible under my #5.

## How we would know I was right

**My #2, my #3, and my #18 (`attributed`): test agent behavior on equivalent tasks.**

Compare the current draft with the revised layout across the intended engines, using repeated fresh sessions and the same task inputs. Include an ordinary entry, a justified SHOULD departure, a supersession, retirement without replacement, a permitted historical read, a mismatch, and an oversized index.

Record missed obligations, false stops, missed exceptions, clarification requests, and token use. Have the evaluator and acceptance criterion chosen beforehand, with authorship of the checks disclosed.

The proposed layout earns its place if agents meet that criterion more consistently at an acceptable cost. Parsing successfully or passing the COO’s text-preservation check cannot establish that result.