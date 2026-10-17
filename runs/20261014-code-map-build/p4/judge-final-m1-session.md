# P4 re-judge — final map (builds/probe-final-session.json) against the M1 key (Claude opus subagent)

Totals, 61 claims: **held 30, limited 23, missed 3, wrong 1, n/a 4.** On the A5 tool they were held 26, limited 8,
missed 21, wrong 2, n/a 4.

- **Limited (23):** places that now carry a limit, either at the line or through the scope limit ("callers written in
  these folders were not searched") or "no sibling rule given (A1)".
- **Missed (3):**
  - an interface member;
  - a constant;
  - `yield* SessionStep.make`, which is not a call, while `make` is not a definition.
- **Wrong (1), M1.6e.** model-request.ts:405 resolves to one target only: the fallback stub in
  `input.tools ?? {...stub}`. The main target, the registry's `execute`, is missing. The link should be ambiguous, or
  carry a limit.
- **Side finding.** Calls into `@opencode/ai`, a workspace package in this repository, are still labelled
  "implemented outside the repository". The judge reads this as a wrong reason text that no key claim depends on.
- **Ten random links:** 10 of 10 correct. Most are easy library calls.
