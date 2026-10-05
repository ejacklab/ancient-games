# Research: what makes a good requirement statement

## Why we need it

We have been writing rules for a workflow-design method, and today we found a repeating failure. Real examples from
this repository, all caught by a person, not by us:

1. **A rule with no source.** *"At most 5 subagent roles per run and at most 3 running at once."* Nobody could say
   where the numbers came from. Tracing them found a **different** rule's numbers — "run at most 3 in parallel",
   "up to 5 in a round" — which are about *candidate approaches for one question*, not about roles or concurrency.
   The sentence would not parse because it counted two different things with one word.
2. **An invented structure.** A person said one thing: *"we don't ask a subagent to give a HUGE prompt that runs
   like 10 hours to Codex; since an LLM can estimate the workload, better to divide into like 6 or more pieces."*
   An agent paired it with a separate 8-hour ceiling, declared them "the design-time half" and "the runtime half" of
   one rule, and wrote the pairing into three documents. He replied: *"I never said got a run time half… maybe this
   is why got so many problems."*
3. **A rule that cannot fail.** *"The check string only has to be non-empty."* A node could put `TBD` in its check
   field and pass every gate. Same for an engine field holding an em dash, and a ledger whose column headers were
   never read while the parser matched columns by **position**.
4. **A count and a time wearing the same words.** *"A limit on attempts"* meant a retry **count**; the reader took it
   for a **time** bound, which was a different rule in another section.
5. **Numbers with no basis.** The method itself says of one rule: *"a friend's practice plus reasoning, not
   measured"* — and it is marked `n=0`.

## What to research

**What makes a requirement statement good, testable and durable** — from the established literature, not from your
own invention. Name the sources you use. The relevant bodies of work include (verify these, do not trust this list):
requirements-engineering quality criteria (IEEE 830 / ISO/IEC/IEEE 29148), the INCOSE *Guide to Writing
Requirements*, EARS (*Easy Approach to Requirements Syntax*), RFC 2119's requirement keywords, and any
well-documented work on ambiguity in natural-language requirements.

Answer, concretely:

- What are the named **quality characteristics** of a good requirement (atomic, unambiguous, verifiable, traceable,
  necessary, complete, singular…)? Define each, and say **which failure it prevents**.
- **Who to attribute, how, and why.** Is "the source must be recorded with a requirement" actually a documented
  practice, and under what name? What do the standards say about *rationale* and about requirements that are
  **unverifiable** — do they belong in a requirements document at all?
- **Verifiability.** What does it mean for a requirement to be verifiable, and what do the sources say about
  requirements that cannot be verified by test, analysis, inspection or demonstration?
- **Ambiguity.** What is documented about weak words, compound requirements ("and"/"or"), units without a quantity,
  and passive voice? Give the named anti-patterns.
- **Requirement vs design vs guidance.** Is there a documented distinction between *what must be true* and *how to
  achieve it*? Which of our five failures above are violations of which principle?
- **Structure.** What do the sources say about a canonical form (condition / subject / action / object / constraint)
  and about stating a basis or rationale beside a requirement?

## The deliverable

`docs/research/20261005-requirement-statements/FINDINGS.md`, with:

1. **The quality characteristics**, each defined, each with its source, each with the failure it prevents.
2. **A short checklist** — the questions to ask of one statement before writing it down. Aim for something a person
   can apply in thirty seconds. This is the artefact we will actually use.
3. **The anti-patterns**, named, with sources.
4. **An application to our five failures**: for each, say which principle it violated and what the statement should
   have said instead. Quote our text exactly as given above.
5. **The limit of the sources**: anything you could not verify, and anything where the standards disagree.

## Rules

- **Cite a source for every claim**: the document, and the clause or section where you can. If you are working from
  memory without the source in front of you, say so and mark it **RECALLED** — do not invent a clause number. We
  have been burned by confident unattributed claims all day, and a wrong citation is worse than an admitted gap.
- Prefer fewer, verified points to many recalled ones.
- Do not edit anything outside `runs/20261005-requirement-research/` and
  `docs/research/20261005-requirement-statements/`.
- You may not be able to run commands or reach the network. If so, say that plainly at the top of the file and mark
  every point RECALLED rather than pretending to have checked. **A file that admits its basis is worth more to us
  than one that looks authoritative.**

## Reply with

Only: where you wrote it, which sources you actually verified versus recalled, and the single checklist question you
think we most often skip.
