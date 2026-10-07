# Code review — feedback template (deepseek-v4-pro)

## Verdict

Agree with the skeleton; two edits: **split `Method`/`Why`** and **drop `Report`**. Keep `Basis` first, keep `Findings` with `file:line`. No `Effort` field (code review is maker–checker, not a loop type) and no verdict field (the pass/fail is the verifier's, not the worker's — the worker writes before the human looks).

## The six whys (method 3.0), in order

1. **Why does EJ want this?** A verifier reads the worker's return and must be able to answer, in one pass: "was this review against the spec/requirements/diff, and did it find the planted defect?" Free text cannot be scanned for that; a fixed shape can. → *the objective*. **Changes the design: yes** — it is the reason every field exists and why `Basis` matters most.
2. **Why now?** Types are being walked one at a time (10 decided, 11–16 pending); code review is the current one. → *priority*. **Changes the design: no** — noted, not acted on.
3. **Why this shape of solution?** The alternative is free text; the author already mapped five questions to five fields, which is the shape. The category is `code review` — maker–checker, fresh blind session; check "fixed checklist; findings with file:line"; sabotage "plant a known defect → the reviewer must find it". → *category + default pattern*. **Changes the design: yes** — the check pins `Findings`' unit (`file:line`), and the sabotage makes `Basis` the anchor: a finding is only a finding against a named thing.
4. **Why would it fail?** Three ways: (a) `Basis` soft-pedaled → findings unanchored ("reviewed against nothing") — the author's own "matters most"; (b) `Method`+`Why` merged → the worker answers "how" and drops "why", so the verifier cannot tell whether the method *could* have caught the defect class (a read-only pass cannot find a runtime-only defect); (c) `Report` kept → the same path written twice, by the same writer, and it drifts. → *risk tier / review depth*. **Changes the design: yes** — it is the direct argument for all three edits.
5. **Why does it stop where it stops?** In scope: the worker's own summary fields. Out of scope: the human's verdict (a different writer, a different artifact), the pass-back header (already the contract's, script-validated), and the checklist definition (belongs to the design, not the return). → *in/out of scope*. **Changes the design: yes** — it is why there is no verdict field and why `Report` leaves.
6. **Why would we believe it is done?** When every field names its writer (all: the worker), `Basis` names the thing reviewed against, and every finding carries `file:line` — checked by the fixed checklist, and the planted defect proves the check can fail. → *stop condition + check kind*. **Changes the design: yes** — it confirms the check stays external; the summary reports, it does not grade.

## Rulings on the two questions

**`Method` + `Why`: two fields, not one.** The author asked two questions ("how the code is reviewed", "why use that review way"). "How it was reviewed, and why that way" is two statements wearing one field; a merged field lets the worker answer the first clause and silently drop the second — and the second is the clause the verifier needs to judge whether the review could have caught the planted defect (read vs ran is exactly the "why that way"). `Why` is already a first-class field in the shared vocabulary, so this costs nothing. Keep it one clause — a justification of the method, not a second review.

**`Report`: drop it.** The pass-back header already carries the `evidence` path, it is script-validated, and the COO reads the header together with the summary (method 3.8.4). For code review the full report *is* the findings file, so `Report` and the evidence path are the same pointer written twice by the same writer — a drift hazard carrying no new information. If there is no separate full report (the summary is the report), the field is empty. Redundant either way.

## The template

```
## Summary
- Basis:    <what it reviewed against — the spec / requirements / diff>
- Method:   <how it was reviewed>
- Why:      <why that way — one clause>
- Findings: <what was found — each with file:line>
```

All four written by the worker. "How" and "why" in practice: `Method` says read and/or ran (and what was run); `Why` says why that mix — e.g. *"ran the tests because a read-only pass cannot catch the planted runtime defect."* No `Effort` (maker–checker is a single blind pass, not a loop), no `Report` (the pass-back `evidence:` line is the path), no verdict (the human's).
