I'll read all three files and compare them.
## 1. Correct?

No false claim, no invented name. Every heading is the source's heading verbatim (method 3.0–3.8), the twelve 3.8 items match method 3.8's 1–12, and the five loop-ready conditions, five node-carries, five parallel conditions, the3-step prompt-file rule, the ≥20% challenger rule, "Git is not required" and the n=1/n=0 footer all check out.

Four defects, all loss by omission or mis-drawing, none of substance:

- **The flow mis-draws the method's one gate.** Method §2 and `WORKFLOW_DESIGN_DIAGRAM.md:18-20` put "is it tiny?" *immediately after 3.0, before 3.1*. The page draws 3.0→3.1→…→3.8 as one unbroken chain and parks the tiny box after the whole chain (workflow-design-algorithm.html:100) — while that box's own text says "after 3.0". A newcomer reads it as: do all nine, then maybe don't. The chain also omits 3.4's second prompt-file exit (`S4 → yes → prompt file`, diagram line 38), so the map shows only one exit from the method and the map shows none at3.4.
- **The blueprint check is compressed to a consequence.** 3.1 keeps "a building piece waits for settled sections; silence doesn't count" but drops the operating parts: the four statuses and what each does (settled → nothing, draft → decision question, incomplete/missing → a blueprint piece at the front) and which sections a kind of task needs (method 3.1:148-183). So 3.6's stop — "the acceptance criteria it covers pass" — uses a term the page never defines, with no hint that ids are `R1.1` / `N1.1` from the blueprint's requirements section. A newcomer cannot execute3.6's stop condition.
- **Dropped, in scope:** the six-whys "unanswerable ⇒" column (method 3.0:55-62 — an unanswerable why-4 means assume the higher tier, why-6 means the piece is not loop-ready); `others` (no TASK_TYPES row → full method from first principles, 3.2:204, 3.4:265); "if its check is judged, it is a fixed checklist of those three parts" (3.6:334); 3.6's whole picture — loops inside the nodes, exploration only inside the unknown-spot nodes (:370); and §4's three product memory files `decisions.md` / `changelog.md` / `lessons.md`, which a run that builds must write — "State and memory" covers only the state file.

## 2. Simple and direct?

The prose is genuinely good: "a label is not a node" and "a loop only closes when its check is objective" survive translation intact, and the glossary earns its place. Four things confuse a newcomer:

- **"fixed bounds on attempts, pieces and concurrency"** (Predictability card) — method §5's wording, but the method *deleted* its concurrency caps on 2026-10-05 (3.7:387-400). A newcomer will hunt for a number that no longer exists, and 3.7's five parallel conditions sit right beside the deleted rule with no note that there is no cap.
- **"Anything else found goes to `backlog.md`"** sits immediately after the numbered 1-2-3 stop. "Else" must mean "any other finding", but against a list it reads as "any of the three failing".
- **"Git is not required"** reads as *don't check git*; the source still checks the git binary when present and keeps a pre-run `git status --short` (3.1:85-91).
- **3.2's merge rule** ("pieces that share an engine and have no independent check merge into one node") drops the three things that buy a hand-off — own check, different kind, context room — so the merge looks absolute rather than the default it is.

Unresolved jargon after the glossary: COO, tier, loop-ready, pass-back, and four near-synonyms (piece / node / gate / edge / joining node) used as if distinct.

## 3. One concrete improvement

Branch the flow at 3.0 — `3.0 → {tiny? → prompt file | no → 3.1 … 3.4 → {small? → prompt file | no → 3.5 …}}` — and move the tiny box into the chain, so the page's map matches §2 and 3.4's second exit.
