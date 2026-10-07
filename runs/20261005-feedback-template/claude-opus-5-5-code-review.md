# code review — feedback template (claude-opus-5-5, blind)

## Six whys

1. **Why does a code review report back?** So the person receiving it can decide whether to act on it without
   doing the review again.
2. **Why can't they decide from the findings alone?** A finding only counts as one when it's measured against
   something. Without the basis, "3 findings" and "0 findings" tell the reader nothing.
3. **Why does the basis matter most?** A review against the wrong basis, or with no basis, produces the same empty
   result as a clean review. Only the basis tells "clean" apart from "never checked".
4. **Why the method, and why that method?** The same basis reviewed different ways finds different defects:
   reading the diff, running the tests, and tracing the spec each miss different things. The method tells the reader
   which defects might still be there. The why tells them whether the reviewer *chose* that method or just fell into it.
5. **Why file:line?** It turns each finding into a check that takes one step: open that line and look.
6. **Why the report's location?** The person fixing the code needs the detail behind each finding. But that is
   what `evidence:` is for, so see the Report section below.

## Judgments

**Basis: agree that it comes first, but the placeholder mixes two things.** "spec / requirements" is what the code
was reviewed *against*. "diff" is *what* was reviewed. These are two separate facts.
→ **Open for the author:** when you said "review based on what" (twice), did you mean the standard, the target,
or both? If both, I'd write it as one line: `<target> against <standard>`. Either way, the standard must be named
specifically (path or ID), not "the spec".

**Method + Why: keep them as two fields.** The author asked two separate questions. If they are merged, the line
can be filled with the how alone ("read the diff"), and the missing why goes unnoticed. With two fields, an empty
`Why` shows. The task type fixes the method ("fixed checklist"), so `Method` should name *which* checklist. `Why`
earns its place when the reviewer departed from the checklist or added to it. "Default checklist" is an honest
answer there.

**Report: redundant. Drop it from the Summary.** If the full report is the evidence, the path ends up in two places,
and those two can disagree. The `evidence:` line already answers "where the report put at" (by default under
`runs/<run-id>/`). Keep a separate field only if the report and the evidence are *different* files. That's the
author's call.

**Findings: two changes.**
- **An empty field must fail.** "None" has to be written out explicitly. Otherwise a blank looks the same as a
  clean review.
- *(My suggestion; the author did not ask for this.)* Each finding names the checklist item or spec clause it
  breaks: `file:line — <basis item> — <what's wrong>`. This ties Findings to Basis, so the checker can verify it.

**Leave these out:**
- "Did it find the planted defect?" The reviewer is blind and cannot know which defect was planted. The checker
  writes that, in the verdict.
- Effort: code review is not a loop type.

## Proposed

```
## Summary
- Basis:    <what was reviewed> against <named standard — spec/requirements/checklist, by path or ID>
- Method:   <how it was reviewed — which checklist; what was run vs. only read>
- Why:      <why this method for this basis; "default checklist" if unchanged>
- Findings: <file:line — basis item — what's wrong>, one per line; or "none"
```
(Report → the pass-back `evidence:` line.)

## For the human
1. "Based on what": the standard, the target, or both?
2. Is the full report the same file as the evidence? If yes, drop Report. If no, keep it.
3. Do you want the basis-item link in each finding (my suggestion)?
