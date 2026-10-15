# Linus Torvalds — Source-of-truth memory review

## Answer

**My reading:** keep the two-file design and the clause records, but fix the contradictions and incomplete checks before calling it finished. **Whether an agent will follow it is not measured**; a valid YAML file does not establish that.

## How I decided

1. **Separate a readable specification from demonstrated behaviour — my #2, my #7 and my #18.**

   The COO’s build script establishes structural properties: loading, consistent keys, unique record ids, coverage and resolving links. It does not establish semantic agreement, correct enforcement or successful agent handoffs.

   Keep the YAML’s grouping and one level per clause. Make `how_to_read` explain that:
   
   - A parent id such as W1.2 identifies its clause records; it does not supply another requirement text or level.
   - The leaf record’s `level` determines its obligation.
   - A group’s `basis` applies to its records.
   - `fails_if` must agree with `text`; passing a narrower check does not establish compliance with everything in the text.
   - A disagreement between the prose and YAML is reported to the project owner rather than silently resolved by the reader.

   The current instruction that `text` governs does not clearly distinguish a clause’s text, its parent requirement and the prose. **Cost:** a little more reading guidance and continued maintenance of agreement between the files.

2. **Fix the data model where it permits contradictory interpretations — my #9 and my #10.**

   | Location | My reading of the problem | Recommendation |
   |---|---|---|
   | W1.2a / W1.2b | The MUST record requires every field on one `key: value` line; the SHOULD record puts multiple values on indented lines. | Keep delimiters in W1.2a. Put field layout entirely in W1.2b. |
   | W1.1a / W2.1a | One permits an observation to become a fact through supersession; the other excludes facts discovered afterwards. | Define when discovered knowledge becomes a governing fact. Do not make agents guess from timing alone. |
   | K4.3 / prose | The prose’s list of permitted changes omits `done:`, which the YAML permits. | Include `done:` in that prose sentence. |
   | W6.3a | Immutability of claims does not prevent conflicts in mutable `status` or `done:` fields. Keeping both values cannot resolve a field requiring one value. | Preserve both histories and links; report incompatible status or completion information for resolution. |
   | Rd4.1 / Rd4.4 | Reading all covering entries can include superseded entries, whose reading is restricted. The matching meaning of `covers` is unspecified. | Say active entries govern edits; historical entries are reached through links. Specify how coverage matches a path. |
   | Rd5.1 / Rd5.4 | An authorised change can temporarily contradict the code. Rd5.4 exempts it from Rd5.3, but Rd5.1’s failure condition still catches acting on it. | Distinguish checking existing behaviour from implementing an authorised new requirement. Carry that distinction into Rd5.1. |
   | K5.2 | Recovery after an abrupt cutoff depends on notes having been written and surviving it. | Limit the recovery claim to persisted journal content. |
   | `checks.secret scanner` | It describes an available check, although no scanner exists. | Mark it unimplemented; identify reviewer judgement as the current check. |

   Add one complete entry example, including its filename. It would also remove the ambiguity between prefixes written as `D-` and the filename template containing `<prefix>-`.

   **Cost:** these changes need coordinated edits across records and prose. Defining coverage also commits implementations to one matching convention. None requires a new memory service or background agent.

3. **Check the requirements themselves — my reading, using the eight house criteria.**

   These are findings about particular records, not a claim that every record passes or fails together.

   | Criterion | Result |
   |---|---|
   | Who decides | **FAIL:** W3.6 and Rd3.1a explicitly remain unassigned. Review responsibility is also unresolved. |
   | One thing | **FAIL:** W3.6 combines entry duplication, procedure placement and script listing. W5.1 combines several writing events with different evidence. |
   | Unit | **PASS:** sentence and file counts name their units. **FAIL:** Rd3.1a lacks the configured limits and their units needed for comparison. |
   | Can it fail | **PASS:** many records name concrete violations. **FAIL:** several conditions miss obligations in their own text; examples follow below. |
   | Weak words | **FAIL:** procedure scriptability and the boundary of sensitive data leave judgement unspecified. |
   | Level | **PASS:** leaf records declare levels and SHOULD exceptions. **FAIL in presentation:** absolute prose can conceal those exceptions. |
   | Basis | **PASS for traceability:** the records identify vision or design sections. Agent compliance and YAML superiority remain **not measured**. |
   | Links | **PASS for resolution**, according to the COO’s script. **FAIL for completeness of the relationship:** Rd5.4’s authorised-change exception needs agreement with Rd5.1 as well as Rd5.3. |

   Other incomplete failure conditions matter. W5.1 omits the unfinished-work handoff obligation; W3.6 omits procedure placement and script listing; W5.3a omits the evidence pointer and exclusion of `done:` from standing rules; Rd5.1 catches contradictory action but not skipping the check; Rd5.3 does not cover every required notification or action on the blocked part; Rd6.1 catches redundant questions but not choosing the wrong next step without asking.

   **Recommendation:** make these conditions cover their texts, or explicitly describe them as partial detection. **Cost:** reviewers must examine behaviour and evidence, rather than merely search for a log line.

4. **Review each COO addition on its merits — my #9, my #11 and my #18.**

   | Addition | Verdict and reason | Cost or risk |
   |---|---|---|
   | W5.2 `fails_if` | **Change.** Connect it to K5.2’s agent judgement about what deserves an entry. It currently suggests everything learned must be promoted. | Judgement remains necessary; relevant knowledge can be overlooked. |
   | W6.1a `fails_if` | **Keep.** It identifies multiple entries in one entry file. Clarify that the shared-file prohibition concerns new entries, since journals and change logs are appended to. | One file per entry increases file count. |
   | K5.1 `fails_if` | **Change.** Distinguish altering existing journal content from appending new content. Include absence of the required journal when applicable. | Checking append-only behaviour requires history inspection. |
   | Rd1.1 `fails_if` | **Change.** Explicitly allow an absent `.cache/`; its optional status must survive the failure wording. | Minor extra wording. |
   | Rd5.2 `fails_if` | **Keep.** It corresponds to the prohibition on memory overriding standing instructions. | A reviewer needs both the instructions and evidence of the action. |
   | SHOULD exception wording | **Keep.** It implements the declared level. Explain where the written reason is recorded; task `state.md` is a sensible recommendation for task work. | Exceptions become paperwork and can conceal weak reasoning. |
   | W1.2 split | **Change.** Keep mandatory header delimiters, but move the single-line layout sentence out of the MUST clause. | Existing entries may need checking against the clarified format. |
   | W1.1b uniqueness | **Keep.** Independent writers still need unique ids. Define collision recovery, because committed ids are also immutable. | Collision detection currently has no stated repair path. |
   | Rd5.3 naming Rd5.4 | **Keep.** Necessary to avoid reporting normal implementation as drift. Align Rd5.1 too. | An overly broad exception could excuse unrelated contradictions. |
   | Rd2.3b linked-history exception | **Keep.** Historical links need to remain usable. | Following a link must not exempt the content from other applicable prohibitions. |
   | Owner on W4.1c, W5.3b, W6.3a and Rd5.3 | **Keep.** Those concern contested project meaning or a result differing from the decision. | Resolution can wait on the owner. |
   | Reading agent on K5.2 | **Keep.** The reader has the context for selecting useful knowledge. | Selection is fallible and should be reviewable. |
   | Project workflow on K1.1 | **Change.** Refer to the workflow’s actual decision rule or designated role for code-first exceptions. | Requires project-specific configuration. |
   | `unassigned` on W3.6 and Rd3.1a | **Change before adoption**, using the assignments below. | Somebody must accept those responsibilities. |

   For the header keys: **keep** `what`, `levels`, `roles` and `basis`; **change** `how_to_read` and `checks` as above. **Change** `retired_ids` to describe reserved group ids without historical explanation, consistent with EJ’s decision to move formation history out of the agent-facing design. The cost is a small schema/documentation change.

5. **Put review with someone who knows the work — my #4, my #6 and my #14.**

   Recommend that the project owner designate a reviewer role when adopting the design, recorded in the project’s standing instructions or workflow. **My proposed fallback is the project owner until they delegate**, rather than leaving `reviewer` silently unassigned.

   The reviewer may be a person or agent. Review happens at the event the record governs: before acting, during a merge, at completion or at handoff. It does not require approval for every ordinary entry edit.

   Record who reviewed and what evidence supports the judgement. If the author also reviewed, label it as self-review; it supplies no independent corroboration.

   **Cost:** review consumes attention, and the owner fallback can become a bottleneck. Delegation reduces that cost without giving ordinary reviewers authority to settle contested project decisions.

6. **Assign the two open decisions at the appropriate level — my #4, my #6 and my #14.**

   **W3.6:** recommend the person or agent implementing or maintaining the procedure decides whether it can be a script, with a written reason when choosing documentation. The project owner settles a dispute. This is a technical implementation choice, not a reason to route every procedure through the owner.

   **Rd3.1a:** recommend the project owner decides which agent tools the project supports. Whoever maintains the loading configuration establishes their applicable limits; the checker enforces the configured constraints. Where limits use different units, each applicable constraint must hold—there is no meaningful minimum between bytes, lines and tokens.

   Do not substitute the example numbers for an unset configuration. An unset limit cannot establish compliance.

   **Cost:** procedure writers must explain their judgement, and supported-tool changes require configuration maintenance. The actual tools and limits remain unknown here.

7. **Make lifecycle behaviour explicit — my #5, my #9 and my #10.**

   **Retirement without replacement:** currently it fails K4.1. I recommend allowing it: use `superseded` when another entry replaces the claim; use `retired` when the claim ceases to govern and has no replacement. Preserve the body and record the retirement reason. Require `superseded_by` for supersession, not retirement. **Cost:** retirement needs review so it does not become a convenient way to discard inconvenient requirements.

   **Memory before code:** the supersession rule exists, but K1.1 should name it directly. Create the successor, link it to the predecessor, mark the predecessor superseded, regenerate the index, then change the governed code. Mere addition of a `changed:` line must not satisfy the prerequisite. Also decide whether “first” means editing order or separate commits: the current checks permit both changes in one commit. **Cost:** supersession creates additional records; requiring separate commits would add another workflow constraint.

   **Failed MUST:** stop the operation governed by that record and work depending on it. Continue independent work when that boundary is established. Rd5.3 already provides this behaviour for a contradicted claim. A malformed entry or failed index check blocks the affected memory commit; a local mismatch need not stop an unrelated task.

   The agent identifies the affected work and its dependencies; the designated reviewer resolves an uncertain boundary. If independence cannot be established, the dependent work remains stopped. **Cost:** this requires dependency judgement and may delay work whose independence is unclear.

## What I need to know

- Will EJ adopt the reviewer assignment and owner fallback, or should a different role be responsible?
- Should retirement without replacement be permitted, and does memory-first ordering require separate commits?
- Which tools must adopting projects support, what are their applicable loading limits, and how should `covers` match paths?
- When may discovered knowledge become a governing fact, and who defines the project’s sensitive-data boundary?

These choices remain recommendations or open values; I have not treated them as decided.

## Costs and risks

- **My #9 and my #18:** correcting both files and their checks costs maintenance time; superficial agreement can still hide semantic disagreement.
- **My #4 and my #14:** named review makes responsibility clear but consumes attention; making the owner review everything would create a bottleneck.
- **My #5:** preserved history permits reconsideration, while retirement and SHOULD exceptions can weaken useful rules if poorly justified.
- **My #2 and my #7:** these are specification findings. They do not demonstrate that agents reliably perform the required actions.

## How we would know I was right

Observe the next real adoption and handoff against concrete cases: an indented header field, append-only journal update, authorised supersession, unrelated mismatch, conflicting `done:` values, retirement without replacement, and an index beyond the configured limit.

The agent should produce the specified outcome, identify the applicable records, and stop exactly the affected work. A fresh session should then name the next step and follow the active decisions without repeating answered questions.

These are checks I propose, **not checks I ran**. They would expose failures in actual use; they would not establish YAML superiority over Markdown, which EJ chose not to measure.