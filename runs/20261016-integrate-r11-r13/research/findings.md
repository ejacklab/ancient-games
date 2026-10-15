# Findings: requirement-quality and use-case sources behind R13 and the requirement-check skill

Produced 2026-10-16 by the researcher (Claude Opus 5.5, subagent); saved by the main agent because the harness refused
the subagent's own Write ("Subagents should return findings as text, not write report files"). All pages fetched
2026-10-16. Text below is the researcher's report, unchanged.

Status: open. 6 rows verified (what a page says), 13 reported, 4 unproven, 0 unknown. Not one row rests on the
standard, on GtWR or on Cockburn's own text. The quotes passed through WebFetch's summarising model, not raw page text.

**About the quotes.** Every page was read through WebFetch, which runs the page through a small summarising model
first. Text in quotation marks is what that tool returned as quoted from the page. The researcher did not see raw page
text. Where the tool paraphrased, no quote is given and the item goes to Gaps.

## 1. ISO/IEC/IEEE 29148

| id | Finding | Label | Source |
|---|---|---|---|
| F1 | A 2024 paper's Table I, captioned "Characteristics of high-quality software requirements (ISO 29148)", lists nine: appropriate, complete, conforming, correct, feasible, necessary, singular, unambiguous, verifiable. | verified | https://arxiv.org/html/2408.10886v1 (2024-08-20), Lubos et al., quoted: Necessary "The requirement defines an essential aspect of the system and is irremovable without causing a deficiency."; Singular "The requirement defines only one aspect of the system."; Unambiguous "The requirement is clearly stated, understandable, and allows only one interpretation."; Verifiable "The requirement is formulated in a way that its fulfillment can be proven or, in the best case, measured."; Appropriate "The level of abstraction is adequate, excludes unnecessary constraints, and avoids implementation details."; Complete "All information needed to understand the requirement is included in the description."; Conforming "The representation of the requirement follows an approved standard template."; Correct "The need is accurately represented in the requirement."; Feasible "The requirement is realizable within the given system constraints considering an acceptable risk." |
| F2 | ISO/IEC/IEEE 29148:2018 names those nine as the characteristics of an individual requirement. | reported | Same paper. Its reference entry: "ISO/IEC/IEEE 29148:2018(E), pp. 1–104, 2018". The standard was not read. |
| F3 | The paper says 29148 also has set characteristics, but does not list them. | verified | Same paper, §V-C, quoted: "specifies characteristics for sets or requirements, encapsulating the quality aspects of a consistent solution that meets stakeholder expectations" |
| F4 | A 2016 blog gives 29148's individual list as Necessary, Implementation Free, Unambiguous, Consistent, Complete, Singular, Feasible, Traceable, Verifiable, and its set list as Complete, Consistent, Affordable, Bounded. | reported | https://www.formalmind.com/?p=999 (2016-07-27), "How to Model Textual Requirements", quoted: "It contains quality criteria for individual requirements, as well as criteria for sets of requirements." No edition is named. |
| F5 | A 2026 vendor page gives 29148 set characteristics: complete, consistent, feasible. | reported | https://www.modernrequirements.com/?p=32595 (2026-07-16), quoted: Consistent "Make sure that none of the requirements contradict each other and that the terminologies are consistent."; Complete "The requirement set should cover everything that the solution needs."; Feasible "It should be possible to implement the requirements set within the project's real budget, schedule, and technical limits" |
| F6 | The same page defines "necessary" by a removal test. | reported | Same page, quoted: "If removing any requirement wouldn't leave a gap in what the system must do, it is not necessary." |

**F2 and F4 disagree.** F2 has appropriate, correct and conforming; F4 has implementation free, consistent and
traceable in their place. *Inference from the dates:* F4 is probably the 2011 edition. Neither row settles this from
the standard.

## 2. INCOSE GtWR

| id | Finding | Label | Source |
|---|---|---|---|
| F7 | A review of GtWR v3.1 says the guide has 14 characteristics, C1–C14, with C1 "Required" and C11 "consistent". | reported | https://www.se-trends.de/en/review-incose-guide-for-writing-requirements/ (2022-09-29, updated 2025-09-23), Michael Jastram, quoted: "14 characteristics"; "C1 (Required)"; "C11 (consistent)" |
| F8 | The same review names attributes A2 Trace to Parent, A3 Trace to Source and A15 Unique identifier. | reported | Same page |
| F9 | The same review names three rules: R5, R13 and R36. | reported | Same page, quoted: R5 "Use definite article "the" vs "a""; R13 "Use correct spelling"; R36 "Use terms & units of measure consistently" |
| F10 | A vendor checker numbers its checks after "a set of INCOSE rules" and gives R7 as the vague-terms rule. | verified (that the page says so) | https://www.altium.com/documentation/altium-365/requirements-systems-portal/valiassistant/quality-assessment?version=5 (updated 2025-02-04), quoted, R7: "Avoid the use of vague terms such as "some", "any", "allowable"" |
| F11 | GtWR's R7 is the vague-terms rule. | unproven | F10's page names no guide title or version. |
| F12 | The same page gives R18 as the single-thought rule. | verified (the page says so); unproven as a GtWR fact | quoted: "Write a single sentence that contains a single thought" |
| F13 | The same page gives R6 as the units rule and R31 as the solution-free rule. | verified (the page says so); unproven as a GtWR fact | quoted: R6 "All numbers should have units of measure explicitly stated."; R31 "Focus on the problem "what" rather than the solution "how"." |

## 3. Use cases

| id | Finding | Label | Source |
|---|---|---|---|
| F14 | Cockburn's fully dressed template: Title, Primary Actor, Goal in Context, Scope, Level, Stakeholders and Interests, Precondition, Minimal Guarantees, Success Guarantees, Trigger, Main Success Scenario, Extensions, Technology & Data Variations List. | reported | https://en.wikipedia.org/wiki/Use_case, citing "(Cockburn, 2001, p. 120)" |
| F15 | The title names the primary actor's goal. | reported | Same page, quoted: "an active-verb goal phrase that names the goal of the primary actor" |
| F16 | A minimal guarantee is what the system promises the stakeholders, in particular when the primary actor's goal cannot be achieved. | reported | https://kantara.atlassian.net/wiki/spaces/IDPVUseCases/pages/1441797 (2018-11-25), which says its guidance is from Cockburn's *Writing Effective Use Cases*. Quoted: "Minimal guarantees are what the system promises to the stakeholders" … "in particular when the primary actor's goal cannot be achieved." |
| F17 | A success guarantee is what the system promises at the end of the main success scenario. | reported | Same page, quoted: "Success guarantees are what the system promises to the stakeholders at the conclusion of the main success scenario." |
| F18 | Stakeholders and Interests, Main Success Scenario and Extensions fields. | reported | Same page |
| F19 | Use-Case 2.0 adds "slices". | reported | Wikipedia, citing Jacobson, Spence & Bittner, *Use Case 2.0*, 2011 |
| F20 | Use cases suit non-interaction requirements poorly. | unproven | Wikipedia, Limitations, uncited |

**Mapping to R13.2** (*the researcher's reading*, from F14–F18): purpose ↔ the goal (F15) plus Stakeholders and
Interests (F18); minimum acceptance ↔ the **success guarantee** (F17); the minimal guarantee is **rejected** as the
match — F16 makes it what must hold even when the goal fails, a floor for a failed run, not a pass bar; fails-if has
no single field (nearest: breaking the minimal guarantee, and the failure conditions under Extensions). R13.2 has no
field for what must still hold when a use case fails.

## 4. Conflicting qualities

| id | Finding | Label | Source |
|---|---|---|---|
| F21 | A quality-attribute scenario is a quality-specific requirement in six parts; its response measure makes it testable. | verified (page text) | https://people.ece.ubc.ca/matei/EECE417/BASS/ch04lev1sec3.html (undated), quoted: "A quality attribute scenario is a quality-attribute-specific requirement. It consists of six parts."; "When the response occurs, it should be measurable in some fashion so that the requirement can be tested." |
| F22 | An ATAM course slide defines tradeoff and sensitivity points. | verified (the slide says so) | https://people.computing.clemson.edu/~johnmc/courses/cpsc875/ATAM_files/v3_slide0011.htm, quoted: "Tradeoff point – a decision point at which some attributes are enhanced and some are degraded" |
| F23 | ATAM (SEI) defines these points as in F22. | unproven | The slide names no author or report. |

No source read says what 29148 or GtWR prescribe for qualities that pull against each other.

## 5. Traceability of purpose

| id | Finding | Label | Source |
|---|---|---|---|
| F24 | SEBoK's example requirement table has a Rationale column; traceability ties requirements to their needs. | verified | https://sebokwiki.org/wiki/System_Requirements_Definition (v2.14), quoted: "Reqt ID, Requirement Title, Requirement, Rationale, and Category"; "Traceability helps ensure the requirements trace to their needs, and that they are correct and complete." |
| F25 | Budgeted quantities create requirements that depend on each other. | verified | Same page |
| F26 | 29148 moved "traceable" out of the individual characteristics (2011-era list has it, 2018 does not); GtWR treats tracing as attributes. | reported | F4, F2, F8 |

*The researcher's reading:* R13.5 is trace-to-parent (F8), with the use case or vision line as the parent; "necessary"
(F1, F6) is the test that the trace is real.

## Proposed (all *proposed*; for EJ — nothing written to the skill's rules)

- **P1.** Read "minimum acceptance" as the success guarantee. Rests on F17.
- **P2.** Ask EJ whether a use case also needs a minimal guarantee (what still holds when the goal fails), as a question, not a fourth field. Rests on F16.
- **P3.** The purpose check asks for the primary actor's goal and the stakeholders' interests. Rests on F14, F15, F18.
- **P4.** R13.5 removal test: delete the requirement; if no use case or vision line is left with a gap, it fails "necessary". Rests on F1, F2, F6.
- **P5.** Write purpose as a trace field beside the requirement, not inside its sentence. Rests on F24, F8.
- **P6.** R13.4: state each side's target as a response measure. Rests on F21.
- **P7.** R13.7: the record names a "tradeoff point" and both qualities. Rests on F22; ATAM attribution unproven (F23).
- **P8.** Check the requirement set for consistency, not only single requirements. Rests on F4, F5.
- **P9.** Add "some", "any" and "allowable" to the weak words. Rests on F10; F11 unproven.

## What the Limits text can now say

- A 2024 paper (Lubos et al., arXiv 2408.10886, Table I, "Characteristics of high-quality software requirements (ISO 29148)") lists nine characteristics it attributes to ISO/IEC/IEEE 29148:2018: appropriate, complete, conforming, correct, feasible, necessary, singular, unambiguous, verifiable. (F1 verified; the attribution is F2, reported.)
- Those nine names match the list recalled in the skill one for one. (*reading*; not checked against the standard.)
- A 2016 blog gives a different 29148 list — implementation free, consistent, traceable in place of appropriate, correct, conforming — probably the 2011 edition. (F4 reported.)
- The standard and the INCOSE GtWR were still not read: INCOSE and ANSI/BSI URLs returned HTTP 403 on 2026-10-16.
- No GtWR rule number is verified.

## Gaps

- **29148: not read** (ANSI/BSI preview 403; IEC preview returned the store home page; an archives.gov .docx was saved but not readable with the researcher's tools). Whether F1's definitions are the standard's words is unsettled. The full set-characteristics list was not found.
- **GtWR: not read** (403 on incose.org PDFs and a Jama page). The full C and R lists were not found. Altium's R8, R9, R19, R20, R26, R32, R34, R35 came back paraphrased only.
- **Cockburn's own words: not found**; **Use-Case 2.0 PDF: not found**; ISO 25010 not searched; CMU/SEI-2000-TR-004 not read.
- Calls: 10 searches and 21 fetches, about 6 over the brief's budget.
