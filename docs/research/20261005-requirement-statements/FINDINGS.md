# What makes a requirement statement good: findings

Brief: `runs/20261005-requirement-research/BRIEF.md`. Written 2026-10-05.

## Basis of this file (read this first)

**No network access in this session.** WebSearch and WebFetch were both requested and both refused by the
permission system. I did not try to get around that with `curl`. **No standard was read for this file.** Every claim
about a source below is **RECALLED** from training unless it is marked otherwise.

What *was* checked:

- **VERIFIED (local):** the five failure texts are quoted from `BRIEF.md`. Two of them also appear in the repository:
  the heading "The check only has to be non-empty" (`docs/research/20261004-sunzi/gate-review-minimax-m3.1-flash.md`)
  and "a friend's practice" (`docs/TASK_TYPES.md`, `docs/DISPATCHER_DESIGN.md`).
- **SECONDHAND:** an earlier run in this repository checked Kiro's vendor docs and recorded the EARS form
  "WHEN <condition> THE SYSTEM SHALL <behaviour>" (`docs/research/20261003-feature-cases/A-unclear-requirements.md`,
  row A20). That run also says it did **not** read the original EARS paper. So the paper is still unread.

How I handled citations: I name the document and, where I am confident, the section *title*. I give clause
**numbers** only for IEEE 830-1998 §4.3 and RFC 2119. Both are marked "number recalled". I give no clause numbers for
ISO/IEC/IEEE 29148 or the INCOSE Guide, because I am not sure of them, and the edition matters (29148 has 2011 and
2018 editions; the INCOSE Guide has several versions). Quotation marks around a recalled source mean "close to the
wording, not checked". Treat them as paraphrase until someone checks. Section 6 lists what to fetch to turn RECALLED
into VERIFIED.

### Sources used (all RECALLED)

| Key | Source |
|---|---|
| **IEEE 830** | IEEE Std 830-1998, *Recommended Practice for Software Requirements Specifications*. Superseded by 29148, but still widely cited. |
| **29148** | ISO/IEC/IEEE 29148 (*Systems and software engineering — Life cycle processes — Requirements engineering*), 2011 and 2018 editions. |
| **GtWR** | INCOSE Requirements Working Group, *Guide to Writing Requirements*. It has a set of numbered characteristics and a set of numbered rules. |
| **EARS** | Mavin, Wilkinson, Harwood & Novak, "Easy Approach to Requirements Syntax (EARS)", IEEE RE'09. Developed at Rolls-Royce. |
| **RFC 2119** | Bradner, *Key words for use in RFCs to Indicate Requirement Levels*, 1997 (BCP 14). Updated by **RFC 8174** (Leiba, 2017). |
| **Volere** | Robertson & Robertson, *Mastering the Requirements Process*. It defines the Volere requirement "shell" (template). |
| **Gotel & Finkelstein** | "An analysis of the requirements traceability problem", ICRE 1994. |
| **Berry et al.** | Berry, Kamsties & Krieger, *From Contract Drafting to Software Specification: Linguistic Sources of Ambiguity — A Handbook*, 2003. |
| **Femmer et al.** | Femmer, Méndez Fernández, Wagner & Eder, "Rapid quality assurance with Requirements Smells", *J. Systems and Software*, 2017. |
| **Zave & Jackson** | "Four dark corners of requirements engineering", *ACM TOSEM*, 1997. |
| **Gilb** | Tom Gilb, *Competitive Engineering*, 2005. Source of Planguage. |
| **NASA** | *NASA Systems Engineering Handbook*, SP-2016-6105 Rev 2. Its appendix on writing a good requirement is a checklist. |

---

## 1. The quality characteristics

The two main sources use nearly the same list. **29148 (2018 edition)** and **GtWR** both give these characteristics
for a single requirement: *necessary, appropriate, unambiguous, complete, singular, feasible, verifiable, correct,
conforming*. GtWR adds characteristics for a *set* of requirements: *complete, consistent, feasible, comprehensible,
able to be validated*. **IEEE 830** gives characteristics of a whole specification (SRS) in §4.3 (number recalled):
*correct, unambiguous, complete, consistent, ranked for importance and/or stability, verifiable, modifiable,
traceable*. The **29148 (2011 edition)** list, as I recall it, had *implementation-free*, *consistent* and
*traceable* where the 2018 edition has *appropriate*, *correct* and *conforming*. That edition difference is itself
RECALLED.

| Characteristic | Meaning | Source (RECALLED) | Failure it prevents |
|---|---|---|---|
| **Necessary** | Taking it out would leave a real need unmet. It is not there "just in case". | 29148; GtWR | Gold-plating. Rules that nobody asked for and that cost effort to obey. |
| **Appropriate** | Written at the right level of detail for whatever it applies to: it says *what*, and leaves *how* to the level below. | 29148 (2018); GtWR. In 29148 (2011) this was *implementation-free*. | Design written in as if it were a requirement, which closes off other solutions too early. |
| **Unambiguous** | It can be read only one way. IEEE 830 §4.3.2 (number recalled): every requirement has only one interpretation. It recommends a glossary for terms that could be read more than one way. | IEEE 830; 29148; GtWR | Two readers, two different rules. **Our failure 4.** |
| **Complete** | It needs no other information to be understood. Any condition, unit and tolerance is stated. | 29148; GtWR; IEEE 830 (at the level of the whole SRS) | The reader fills the gap with a guess. A number with no unit is the typical case. |
| **Singular** (also called *atomic*) | It states one requirement. It does not join two with "and", "or" or "/". | 29148; GtWR | Part of it passes and part fails, so it cannot be verified as one thing. **Our failure 1.** |
| **Feasible** | It can be achieved within the known constraints. | 29148; GtWR | Rules that are certain to be broken, which teaches readers to ignore rules. |
| **Verifiable** | Some finite, affordable process can show whether it has been met. Section 3 covers this in detail. | IEEE 830 §4.3.6 (number recalled); 29148; GtWR | Rules that cannot fail. **Our failure 3.** |
| **Correct** | It accurately states the need it was derived from. | 29148 (2018); GtWR; IEEE 830 §4.3.1 (number recalled) | A rule that is well formed but says something the source never said. **Our failure 2.** |
| **Conforming** | It follows the agreed template and style for the project. | 29148 (2018); GtWR | Each writer uses their own form, so reviews cannot be compared. |
| **Traceable** | Backward: its source can be identified. Forward: what depends on it can be identified. IEEE 830 §4.3.8 (number recalled) splits it this way. Backward traceability means each requirement explicitly refers to its source in earlier documents. | IEEE 830; 29148 (2011) as a characteristic. In 29148 (2018) and GtWR it became an *attribute* (trace to parent, trace to source). | A rule nobody can explain or defend. **Our failure 1.** |
| **Consistent** (a property of the set) | No two requirements conflict, and each term is used with one meaning throughout. | IEEE 830 §4.3.4 (number recalled); 29148; GtWR | One word meaning two things in two sections. **Our failure 4.** |
| **Ranked / stable** | Each requirement says how important it is and how likely it is to change. | IEEE 830 §4.3.5 (number recalled) | Firm and provisional rules carry the same weight. Related to **our failure 5.** |

---

## 2. The thirty-second checklist

Ask these of **one statement**, before writing it down. Any "no" stops you. Each item names the principle it comes
from.

1. **Source.** Who said this, and where? Can I point to the exact line? If not, it is my inference: label it as
   mine, or leave it out. *(Traceable: IEEE 830 backward traceability; Gotel & Finkelstein pre-RS traceability;
   Volere "Originator")*
2. **One thing.** Is there an "and", "or", "/" or a second number? Then it is two statements. Split it, and give
   each its own source. *(Singular; GtWR rule against combinators)*
3. **Unit.** Does every number say what it counts and in what unit? Attempts or hours? Roles, or agents running at
   the same time? *(Complete; GtWR rule on units; Gilb's "Scale")*
4. **Can it fail?** Name one concrete input that would make the check fail. `TBD`, `—` or an empty value must be
   among the failing inputs. If you cannot name one, the statement cannot be verified. *(Verifiable; Volere "fit
   criterion")*
5. **Weak words.** Does it contain *like, about, appropriate, as needed, if possible, fast, enough, etc., TBD,
   only has to*? Replace each with a value, or mark the value as open. *(Unambiguous; 29148's language criteria;
   GtWR rules on vague terms and escape clauses)*
6. **Level.** Is it MUST (a gate), SHOULD (a default that may be overridden with a reason), or guidance? Does it
   say *what* must be true, or *how* to do it? *(RFC 2119; Appropriate / solution-free; Zave & Jackson)*
7. **Basis.** Why this value? Measured, quoted from a source, or a guess? If it is a guess, mark it TBR or n=0 and
   say when it will be looked at again. *(Rationale attribute: 29148, GtWR, Volere; NASA TBD/TBR practice)*
8. **Links.** Does it claim a relation to another rule ("half of", "pairs with", "the same as")? Did the source say
   that? A link is a claim too, and it needs its own source. *(Traceability. Applying it to links between
   requirements is my inference; see section 5.)*

---

## 3. Verifiability, rationale and unverifiable requirements

**What verifiable means.** IEEE 830 §4.3.6 (number and wording recalled) says a requirement is verifiable only if
there is some finite, cost-effective process by which a person or a machine can check that the product meets it. It
says an ambiguous requirement is, in general, not verifiable. Its examples of unverifiable requirements are close to
"works well", "good human interface" and "shall usually happen". Its instruction for a requirement that no method
can check is to **remove or revise** it. 29148 and the systems-engineering literature (NASA, INCOSE) name four
verification methods: **inspection, analysis, demonstration, test**. A requirement should be written so that at
least one of the four applies. (RECALLED)

**What to do with what cannot be verified.** The sources agree that it should not stand as a requirement. They
differ on what to do with it instead:

- IEEE 830: remove it or revise it until it can be checked. (RECALLED)
- 29148 (2011 edition, as I recall it): "shall" is for binding requirements, "should" for goals and preferences,
  "will" for statements of fact or purpose, and "may" for permissions. So an aim that cannot be checked can be kept,
  but as a goal and not as a gate. (RECALLED)
- Gilb's Planguage turns a vague quality into a number. It names a **Scale** (what is measured, in what unit) and a
  **Meter** (how it is measured), then gives target levels (for example *Must* and *Plan*). (RECALLED)
- Volere attaches a **fit criterion** to every requirement: a measurable test of whether it has been met. A
  requirement without one is not finished. (RECALLED)

**Where the source and the rationale go.**

- **Source.** Recording where a requirement came from is documented practice under several names. IEEE 830 calls it
  *backward traceability*: each requirement explicitly refers to its source. Gotel & Finkelstein (1994) call it
  *pre-requirements-specification (pre-RS) traceability*: being able to follow a requirement back to where it
  started, including who stated it. Their paper argued that most traceability problems come from missing pre-RS
  traceability. Volere has an **Originator** field. GtWR lists **trace to source** and **trace to parent** among
  its attributes. (All RECALLED)
- **Rationale.** Rationale is a named attribute in 29148's list of requirement attributes and in GtWR. It is also a
  field in Volere's requirement shell. The NASA handbook says to document rationale and gives reasons: the reason
  for the requirement, the assumptions behind it, and how it relates to other requirements. GtWR has a rule against
  **purpose phrases** ("in order to", "so that") *inside* the requirement text. The rationale goes in its own field,
  next to the requirement, not mixed into it. (All RECALLED)

**Provisional values.** NASA and aerospace practice use **TBD** ("to be determined": the value is not known) and
**TBR** ("to be reviewed" or "to be resolved": there is a value, but it is not confirmed). Each open item is
tracked until it is closed. (RECALLED; I have not confirmed which document defines these terms formally.)

---

## 4. The anti-patterns

Each row names the pattern, the source that names it, and an example from this repository's failures.

| Anti-pattern | Named in (RECALLED) | What it is | Example from our failures |
|---|---|---|---|
| **Vague terms** | GtWR rule; 29148 "subjective language" and "ambiguous adverbs and adjectives"; Femmer's requirements smells | *user friendly, fast, significant, like, about, minimal* | "like 6 or more pieces" (#2) |
| **Escape clauses / loopholes** | GtWR rule; 29148 "loopholes"; Femmer | *if possible, as appropriate, as applicable, where practical* | — |
| **Open-ended clauses** | GtWR rule; 29148 "open-ended, non-verifiable terms"; Femmer | *including but not limited to, etc., and so on* | — |
| **Combinators** | GtWR rule (singularity) | "and", "or", "and/or", "/" joining two requirements in one sentence | "at most 5 … and at most 3 …" (#1) |
| **Coordination ambiguity** | Berry et al.; Chantree et al. (RE'06, "nocuous ambiguity") | It is unclear how far "and"/"or" reaches. "Old men and women" can be read two ways. | — |
| **Quantifier scope / the "dangerous all"** | Berry et al.; GtWR rule (prefer "each" to "all") | "all", "every", "only" read as covering the group as a whole or each member | — |
| **Absolutes** | GtWR rule; 29148 "terms implying totality" | *always, never, 100%* without a stated tolerance | — |
| **Passive voice** | GtWR rule (active voice, with a clear subject); Berry et al. | "Shall be verified" — by whom? The responsible party disappears. | "has a check" — but who runs it? (#3) |
| **Missing unit / tolerance** | GtWR rules (units of measure, range of values); Gilb's Scale | A number with no unit, or no range | "a limit on attempts" (#4) |
| **Vague pronouns / incomplete references** | 29148; Femmer | *it, this, that, the above*; "see the other section" | — |
| **Negative statements** | 29148; Femmer | "shall not" where a positive form exists | — |
| **Solution in the requirement** | GtWR rule (solution-free); 29148 (2011) *implementation-free*; IEEE 830 section on embedding design in the SRS | Saying *how* where *what* was asked for | Partly #2; see section 5 |
| **Purpose phrases** | GtWR rule | "… in order to …" inside the requirement text | — |
| **Indefinite time** | GtWR rule | *eventually, as soon as possible* | — |

**Requirement, design and guidance are different things.**

- IEEE 830 has a section on embedding design in the SRS. As I recall it, it says the SRS should say what functions
  are performed, on what data, with what results, and should not normally contain design. (RECALLED)
- RFC 2119 §6 (number recalled) says the key words must be used sparingly. They are for cases that are actually
  required for interoperation, or to limit behaviour that could cause harm. They are **not** for imposing a
  particular method on implementers when that method is not required. (RECALLED; RFC 2119 is free to read and
  short, so this should be checked first)
- RFC 2119's levels: MUST / SHALL / REQUIRED is absolute. SHOULD / RECOMMENDED may be ignored in particular cases,
  but only after the consequences are understood and weighed. MAY / OPTIONAL is truly optional. RFC 8174 adds that
  the words carry this meaning only when written in capitals. (RECALLED)
- Zave & Jackson separate two kinds of statement. **Requirements** are *optative*: they describe what we want to
  be true. **Domain knowledge** is *indicative*: it describes what is already true of the world. If you mix the two,
  you end up writing a guess about the world as if it were a demand. (RECALLED)

**Canonical form.**

- 29148 gives a requirement construct: **[Condition] [Subject] [Action] [Object] [Constraint]**. My recollection of
  its example is close to: "When signal x is received, the system shall set the signal-x-received bit within 2
  seconds." It gives a second form, [Condition] [Action or Constraint] [Value]. (RECALLED)
- EARS gives five patterns:
  - *Ubiquitous*: "The <system> shall <response>"
  - *Event-driven*: "WHEN <trigger> …"
  - *State-driven*: "WHILE <state> …"
  - *Unwanted behaviour*: "IF <trigger> THEN …"
  - *Optional feature*: "WHERE <feature is included> …"

  Patterns can be combined. (Pattern names RECALLED; the WHEN…SHALL form was checked SECONDHAND through Kiro's
  docs, row A20.)
- None of these forms has a field for the source or the rationale. In every source I recall, those are
  **attributes beside** the statement, not words inside it.

---

## 5. Applying this to our five failures

**1.** *"At most 5 subagent roles per run and at most 3 running at once."*

- **Violated:** traceable (no source); singular (two limits in one sentence); complete (does "3" count roles or
  agents?); correct (the numbers came from a different rule, about *candidate approaches for one question*).
- **Should have said:** nothing new. The traced source was the original rule, so the honest statement is that rule
  restated with its source attached: *"For one question, at most 3 candidate approaches run in parallel, and at most
  5 in a round. Source: <the rule it came from>."* If a separate limit on roles or concurrency is wanted, it is a
  new requirement. It needs its own source and a TBR basis, as two statements:
  *"R-a: A run shall define at most N subagent roles. Source: … Basis: TBR."* and *"R-b: At most M subagents shall
  run at the same time. Source: … Basis: TBR."*

**2.** *"we don't ask a subagent to give a HUGE prompt that runs like 10 hours to Codex; since an LLM can estimate the
workload, better to divide into like 6 or more pieces."* — paired with an 8-hour ceiling as "the design-time half" and
"the runtime half."

- **Violated:** correct and traceable. The pairing was an invented link between two requirements, and no source
  said it. The quoted sentence also uses vague terms ("like 10 hours", "like 6") and is guidance ("better to"), not
  a gate.
- **Should have said:** two statements, each with its own source, and no claimed relation between them:
  - *"S1 (EJ, 2026-10-05, quoted above): When work is estimated at many hours of engine time, the designer SHOULD
    divide it into smaller pieces before handing it to an engine; EJ's example is ~10 hours → 6 or more pieces.
    Level: guidance."*
  - *"S2 (<its own source>): <the 8-hour ceiling, stated on its own>."*
- **Note:** the claim that a link between requirements needs its own source is **my inference** from the principle
  of traceability. I do not recall a standard that states it in those words.

**3.** *"The check string only has to be non-empty."* — and the engine field holding an em dash, and the ledger matched
by column position.

- **Violated:** verifiable. The check verifies something else: that a string exists, not that a working check
  exists. It has no fit criterion that `TBD` would fail.
- **Should have said:**
  - *"Each node's check SHALL name a command, or a fixed checklist, that can return fail. The gate SHALL reject an
    empty value, a placeholder (`TBD`, `—`, `n/a`), or a check that cannot be run. Verification: feed the gate
    `TBD` and `—` and confirm both are rejected."*
  - For the ledger: *"The parser SHALL read the header row and match columns by name. A missing or renamed header
    SHALL be an error."*
- **Related technique:** testing whether a check can fail by making a deliberate bad change is documented as
  **mutation testing** (DeMillo, Lipton & Sayward, 1978; RECALLED). A check that catches no mutant tells you nothing.

**4.** *"A limit on attempts"* (meant as a retry count; read as a time bound).

- **Violated:** unambiguous (lexical ambiguity, Berry et al.); complete (no unit); consistent (one term, two
  meanings, in two sections).
- **Should have said:** *"A repair loop SHALL stop after at most N attempts (unit: one attempt = one run of the
  repair step). Source: …"* The time ceiling is a separate statement that uses the word "time", never "attempts".
  Both terms go in a glossary (IEEE 830 recommends one for this; RECALLED).

**5.** *"a friend's practice plus reasoning, not measured"*, marked `n=0`.

- **Violated:** this is the **least** wrong of the five. It already records a source and a basis, which is what the
  rationale attribute asks for. What is missing is a **status**: it is not marked TBR, and nothing says when it will
  be reviewed. IEEE 830's "ranked for stability" asks for this kind of marking.
- **Should have said:** the same words, plus *"Level: SHOULD (default, may be overridden with a reason). Status: TBR
  — review when the ledger has <k> rows."* It should not be a MUST gate while it is n=0.

**Summary.** #1 and #2 are failures of **traceability and correctness**: something was written that no source
supports. #3 is a failure of **verifiability**. #4 is a failure of **unambiguity, completeness and consistency** (a
missing unit and a term that means two things). #5 is a missing **status mark** on a rationale that is otherwise
honest.

---

## 6. The limits of this file

**Nothing here was verified against a primary source.** Network tools were refused in this session. To turn RECALLED
into VERIFIED, start with the sources that are free to read:

| Check | Where (from memory; confirm the address) | Expected access |
|---|---|---|
| RFC 2119 §6, and RFC 8174 | rfc-editor.org | free |
| NASA SE Handbook, the appendix on writing good requirements, and TBD/TBR | nasa.gov (SP-2016-6105 Rev 2) | free |
| INCOSE GtWR summary sheet (lists of characteristics and rules) | incose.org | the summary sheet was free; the full guide may require membership |
| EARS original paper | IEEE Xplore (RE'09); also Alistair Mavin's own site | paywalled / free |
| IEEE 830 §4.3 wording | IEEE (withdrawn standard; copies are in circulation) | paywalled |
| ISO/IEC/IEEE 29148 lists of characteristics, attributes and language criteria | ISO / IEEE | paywalled |
| Femmer et al. 2017 | arXiv preprint (from memory) | free |

**Where the standards disagree (as I recall them):**

- **MUST versus SHALL.** RFC 2119 makes MUST, SHALL and REQUIRED synonyms. 29148, as I recall it, uses "shall" for
  requirements and advises against "must". US plain-language guidance prefers "must" to "shall". Pick one word per
  document and define it.
- **Traceable: characteristic or attribute.** IEEE 830 and 29148 (2011) treat it as a quality characteristic. 29148
  (2018) and GtWR treat it as an attribute (trace to source, trace to parent). Either way it is required. They
  disagree only on where it is listed.
- **Implementation-free versus appropriate.** 29148 (2011) said implementation-free. The 2018 edition softened this
  to "appropriate to the level". So a design constraint is allowed when it is stated at the right level.
- **Unverifiable aims.** IEEE 830 says remove or revise them. 29148 lets you keep them as goals ("should"). Gilb
  says quantify them. These do not contradict each other, but they lead to different documents.

**What I could not settle:**

- Which items in 29148 belong to the 2011 edition and which to the 2018 edition.
- The exact numbering of GtWR's rules and characteristics, and the current version of the guide.
- Whether GtWR's attribute list includes "trace to source" under that exact name.
- Which document formally defines TBD and TBR.

**What is my own inference, not from any source:** the claim in failure 2 that a link between two requirements needs
its own source, and the choice of which checklist question we skip most often.


---

# Verification pass — 2026-10-05, later the same day

The agent above had no network. This pass had one, and fetched the two sources it named as free and worth checking
first. **Everything else in this file is still RECALLED.**

## VERIFIED — RFC 2119 §6

Fetched from `https://www.rfc-editor.org/rfc/rfc2119.txt`. The section is titled **"Guidance in the use of these
Imperatives"**, and its text matters more to us than the keyword list:

> "Imperatives of the type defined in this memo must be used with care and **sparingly**. In particular, they MUST
> only be used where it is actually required for interoperation or to limit behavior which has potential for causing
> harm (e.g., limiting retransmisssions) For example, **they must not be used to try to impose a particular method
> on implementors where the method is not required for interoperability.**"

**Why this lands on us:** nearly every rule in `WORKFLOW_DESIGN_METHOD.md` is a *method* — how to size pieces, when
to split, what to write in a node. By §6's own words, a MUST-level imperative is the wrong level for those. They are
defaults and guidance, not requirements.

## VERIFIED — RFC 8174

Fetched from `https://www.rfc-editor.org/rfc/rfc8174.txt`. It updates RFC 2119 and settles the capitalisation
question:

> "The words have the meanings specified herein **only when they are in all capitals**. … When these words are not
> capitalized, they have their normal English meanings and are not affected by this document."

And it is explicit that the keywords are not what makes text normative:

> "These words can be used as defined here, but using them is not required. Specifically, **normative text does not
> require the use of these key words.** … a lot of normative text does not use them and is still normative."

**Why this lands on us:** our documents write *must*, *never* and *always* in lowercase prose, with no template and
no marker. So by BCP 14 **none of it carries a defined requirement meaning, and nothing tells the reader which
sentences are rules and which are explanation.** That is a mechanical cause of the complaint that started this
research: *"many rules here… don't know who write one, make things sounds weird later."* It is not only attribution —
**a reader cannot even see which lines are rules.**

## NOT VERIFIED — the characteristics lists

The quality-characteristics table in section 1 rests on **29148**, the **INCOSE GtWR** and **IEEE 830 §4.3**. All
three failed to reach from this session:

| source | what happened |
|---|---|
| INCOSE GtWR (both PDFs) | HTTP **403** — blocked at the CDN |
| a thesis quoting the GtWR table | HTTP **403** |
| a university reader listing the characteristics | PDF only, and the fetcher refuses `application/pdf` |
| IEEE 830 / 29148 | paywalled |

So the characteristic **names** (necessary, appropriate, unambiguous, complete, singular, feasible, verifiable,
correct, conforming) and their sources remain **RECALLED**. The two verified points above do not depend on them.

---

# The checklist applied to three of our own rules

The test of a checklist is whether it catches real text. It was run on: our deleted caps rule, the ceiling, and the
guideline EJ gave on 2026-10-05.

## 1. The deleted caps rule — *"At most 5 subagent roles per run and at most 3 running at once."*

| question | verdict |
|---|---|
| **Source** — who said it, where? | **FAIL.** The method's own note said *"a friend's practice plus reasoning, not measured"*. |
| **One thing** | **FAIL.** Two statements joined by "and": a count of roles, and a count of concurrent processes. |
| **Unit** | **FAIL.** "5 roles" counts distinct `role` values; "3 running at once" counts processes alive. One sentence, two units, and the word "subagent" used for both. |
| Can it fail? | pass — `check_plan` refused it. |
| Weak words | pass. |
| Level | **FAIL.** A method preference written as a MUST-level cap. |

Four failures out of six. **The checklist would have stopped this rule before it was written** — which is worth more
than the four days it took to find by other means.

## 2. The ceiling — *"No single call runs longer than the ceiling: 8 hours."*

Source (EJ, dated) ✓ · one statement ✓ · unit (hours) ✓ · can it fail (a 40-hour plan is refused; pinned by test) ✓ ·
no weak words ✓ · level (a genuine MUST — a safety bound, not a method) ✓ · basis (`n=0`, marked) ✓ · no links ✓.

**Passes all eight.** It is the shape the checklist asks for, and it was written today by accident rather than by
method — which is the point of having the checklist.

## 3. EJ's guideline — *"a piece whose work is hours long is not a piece: split it into six or more logical pieces"*

| question | verdict |
|---|---|
| Source | **pass** — quoted, attributed, dated. |
| One thing | pass (one test, one prescription). |
| **Unit** | **FAIL.** "Hours long" has no threshold. Eight, or one? The ceiling next door says 8 — but this rule does not say it. |
| **Weak words** | **FAIL.** "**logical** pieces" is exactly a weak word: no test distinguishes a logical split from an illogical one. |
| Can it fail? | **FAIL as written.** Nothing can check "six logical pieces", so no input makes it fail. |
| Level · basis · links | pass — guidance, `n=0`, no claims about other rules. |

**Three failures.** The guideline is *right* and it is not yet *checkable*. Per question 5 the remedy is to replace
each weak term with a value or **mark the value open** — and inventing either number would repeat the failure this
whole file is about. **So the two are recorded as open, for EJ:**

1. **Hours-long** — what is the threshold? (1 hour? 8, matching the ceiling? something else?)
2. **Logical** — what test makes a split logical? (one deliverable each? one check each? no two pieces sharing a
   file? the existing 3.2 rule says a hand-off must have its own check, a different kind, or fit the context.)
