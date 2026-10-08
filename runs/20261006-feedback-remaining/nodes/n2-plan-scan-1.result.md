---
node: n2-plan-scan
attempt: 1
engine: opencode
model: minimax-coding-plan/MiniMax-M3.1-Flash-Preview
status: ok
started: 2026-10-08T01:00:09.750Z
ended: 2026-10-08T01:01:21.007Z
evidence: none
---

## multi step planning
- Objective (worker): <the challenge restated — what is true when the plan is done, in scope, out of scope; copied from the challenge text, not re-derived from the method>
- Nodes (worker): <one line per node — id, its category, its engine, its check, the deliverable it owns, the nodes it `needs`, and loop or no-loop; plus where the machine-readable design lives (`design.json` / `plan.md` / inline below)>
- Coverage (worker): <which acceptance-criterion ids (`R1.1`, …) and which checks the nodes cover, and which criteria or checks are NOT covered>
- Method (worker): <default or challenger; if challenger, the claimed margin (≥20%) with the basis it rests on and the proof that coverage is equal. Default: "default, unchanged", with why if a default row was adapted>
- Unclear (worker): <each decision spot still open, with the reading used to proceed — `spot — read A, chose A because …`; or "none">

## repo scanning
- Scope (worker): <the area scanned and how it was sectioned — one row per section, the budget, the commit explored (`git rev-parse --short HEAD`), and what was deliberately left unscanned>
- Coverage (worker): <the coverage manifest — which files, nodes and edges of the graph were read, which were NOT, the counts against the graph's `stats`, and the claims resting on `unresolved_calls` (`dynamic` / `attribute` / `name`), which are `read`, never facts>
- Findings (worker): <one line each — claim, `file:line`, a verbatim quote (≥8 chars, pipes escaped as `\|`), and `read | ran` with the command and where its output is saved; findings, not issues: no severity, no fix>
- Source (worker): <the code graph — `python3 code_graph/code_graph.py <root>`, its schema and root, `stats` (files / modules / functions / edges) and every entry in `errors`>
- Unclear (worker): <each spot the scan reached and could not settle, with `file:line` — two readings of a name, a dynamic call, a module whose purpose is not in the code; or "none">

## Whys

**multi step planning / Objective (kept)**
1. Why restate at all? The checklist layer's first item asks whether the category fits the challenge's *intent*, and intent lives only in the restatement (method 3.0 writes it before any tool call).
2. Why in scope and out of scope on the same field? A plan that never says what it excludes cannot be checked for creep; the gate's `touched_paths` is compared against that line.
3. Why does the worker write it? The planner is the only one who read the challenge. Copying the challenge text rather than re-deriving it is deliberate: a mismatch between the two then shows.
4. Why first? Everything below it is judged against it — the join and the checklist reviewer read the objective when a node returns.

**multi step planning / Nodes (kept)**
1. Why one line per node? The script gate parses `design.json` node by node — structure, category-vs-facts, label agreement (G8). The plan's shape is machine-checked only if it is listed.
2. Why the category and engine on the line? G8 demands the design's categories equal the categories its nodes carry, and the engine is what the dispatcher will actually call; both mismatches surface on this line.
3. Why the check? "Why would we believe it is done" (method 3.0) — a node with no check cannot be judged at all.
4. Why the dependencies? The graph's edges decide what runs in parallel, and method 3.7's five independence conditions are judged from these lines, not from prose around them.
5. Why say loop or no-loop per node? `Effort` is filled only by loop types, and the worker learns from the brief whether it is one.
6. Can it fail? Yes — a node with no check, a category its own facts contradict, or a dependency on a node that does not exist.

**multi step planning / Coverage (kept)**
1. Why is coverage here? Coverage is a gate and never an axis (rule 3). A challenger's claim only counts at *equal* coverage, so "equal" has to be written down to be compared.
2. Why criterion ids? The gate and the verifier both address criteria by id (`R1.1`); two coverage sets can only be diffed if the sets are named.
3. Why the not-covered half? A list of covered criteria alone reads as complete when it is not. The gap is the half the second reviewer hunts for.
4. Why the worker's field? Only the planner knows which criterion it hung on which node; the checker re-derives nothing, so it can compare but not reconstruct.
5. How does it fail? A criterion with no node, a check that can fire on nothing, or a coverage set larger than the design's own.

**multi step planning / Method (kept)**
1. Why the default-or-challenger claim? The ledger row (rule 5) cannot be written without it, and a bespoke design that never says so is invisible as a challenger.
2. Why the 20% threshold? It is the bar set above "ask three times, get three different answers" — variance, not signal. Under it the default stands.
3. Why the basis? A margin with no basis is an assertion; the 2026-10-02 lesson is that the claim must be on paper *before* the run, with coverage equal.
4. Why reuse the name `Method`? `code review` (11) settled it as "what it did, and why any deviation from the default" — one field, one writer, no second `Why` to repeat the same reason.
5. Why not the actual cost? Cost comes back after the run and lands in the ledger's *Actual cost* column, written by the harvest, not by the designer.

**multi step planning / Unclear (kept)**
1. Why keep it? The type's sabotage is "an unresolved spot → the gate fails", and the worker is the only one who knows which spots it carried on past by assumption.
2. Why the reading beside the spot? A spot with no reading stops the run; a spot with a stated assumption can be overridden in one line. Both are one row.
3. Why is that not a human decision? The worker writes the *spot and the reading it used*, not the decision. The decision goes to `decisions.md` or EJ (method 3.0).
4. Why not folded into `Nodes`? A spot is not a node; buried in a node's line, a provisional assumption reads as a settled fact — the exact failure the gate exists to catch.

**multi step planning / removed: Effort, Source, Gate result**
1. Why no `Effort`? The settled rule puts it on loop types only, unit `tokens + rounds`. `plan + gate` is one node plus a gate, not a loop; a re-plan is a new node, not another round.
2. Why no `Source` and no code-graph tool? A plan's source is the challenge and the context, not code. Where an existing system must be read, that read is its own deliverable and its own label (`repo scanning`); rule 1 forbids a passenger label, and a planner that silently scanned is a plan whose evidence nobody checked.
3. Why no gate result, `Accepted` or `Agreement`? Whether the design passed the checklist, and whether EJ accepts it, are the reviewer's and the human's. The worker writes before anyone has looked, so a field someone else fills later breaks the one-writer rule.

**repo scanning / Scope (kept)**
1. Why name the area? Case C's scan is "inside the affected area, under a budget, never a repo-wide overview". The boundary is what makes the manifest mean anything: without it, "complete" has no denominator.
2. Why the sectioning? The default pattern is parallel sectioning with a read-only fan-out. The manifest is checkable only if the sections are listed, so a section that silently never ran appears as a missing row.
3. Why the commit? Explorer findings cite `git rev-parse --short HEAD`; without it a `file:line` claim cannot be dated and a stale read cannot be spotted later.
4. Why the worker's field? Only the sectioning worker knows which section was its own, and the join needs per-section rows to reconcile.

**repo scanning / Coverage (kept)**
1. Why is this field non-optional? It is the row's check — "coverage manifest". The field is that check's input, so a scan that skips it has no check at all.
2. Why the not-read half? A fan-out drops whatever looks uninteresting. Writing the drop out is the only way the gap is visible to the join; silence reads as a clean scan.
3. Why reconcile against `stats` and `unresolved_calls`? `unresolved_calls` (`dynamic` / `attribute` / `name`) is where the tool itself could not see through. A claim resting on one of those is a `read`, not a fact, and the manifest's numbers must not contradict the graph's.
4. Why kind per claim (`read | ran`)? Only `ran` may feed a node that builds (explorer file, method 3.8 item 10). The scan is read-only, so every claim it returns is `read` by construction — writing it says so instead of implying.
5. Why is this not the graph's `coverage` key? That number is test reach (`tested` / `total`). It stays inside `Source` with the rest of the graph; this field's subject is the scan's own reading.
6. How does it fail? A section with no rows, a file counted in `stats.files` that no section claims, or a claim citing a node id the graph does not contain.

**repo scanning / Findings (kept)**
1. Why a findings list and not an issue report? Labelling rule 3: research delivers a findings list; review delivers a verdict against a standard. A scan that grades quality is mislabelled `code review`.
2. Why `file:line` plus a quote on every line? The row's check is "findings with paths" and its sabotage is a planted marker file. A pathless finding cannot be checked, and `quote_check.py` confirms the quote is at the cited line.
3. Why no severity and no fix? A severity is a judgment against a standard (review's job) and a fix is code generation — separate deliverables, separately labelled (rule 1).
4. Why one line each? The scan is a fan-out and the join diffs rows; a paragraph cannot be compared across sections or checked by `quote_check.py`.
5. How does it fail? The planted marker reported without a path, or a path that does not resolve.

**repo scanning / Source (kept)**
1. Why name the graph at all? The settled rule: a type whose source is code carries the code-graph tool, and `Source` names the graph. The scan's deliverable *is* a code graph, so the graph is its source and its artifact.
2. Why the worker's? The `root`, `stats` and `errors` are what that scan actually ran; a figure supplied from outside would be a claim nobody checked against a file.
3. Why the counts, not just the path? `files` / `modules` / `functions` / `edges` are the denominator `Coverage` is reconciled against. A graph named without counts gives the manifest nothing to be checked against.
4. Why every entry in `errors`? `code_graph.py` records a parse failure and carries on, so a hole in the scan is real and silent unless the error rides with the graph.
5. Why no separate "the graph was written to" field? Naming it twice lets two names disagree — the one-writer rule. `Source` is the single place the graph is named, and its deliverable lines are the rows above.

**repo scanning / Unclear (kept)**
1. Why keep it? A read-only section can end on a spot with two honest readings: a name bound twice, a `dynamic` call, a module whose purpose is nowhere in the code.
2. Why does the scan not settle it? Settling means deciding what the code means, which is a follow-up node's or EJ's call. The scan's job is to report the spot with `file:line` and stop there.
3. Why not inside `Findings`? A finding is a claim about the code; an unclear spot is a question about it. Mixed together, a question reads as an answer — and `read | ran` cannot be honestly marked for it.
4. Why no `Verdict`, `Complete` or `Accurate`? Only a reader who has seen the manifest can say the scan was sufficient, and that reader is the human or the verifier. This field is the question being asked, not the answer.

**repo scanning / removed: Effort**
1. Why no `Effort`? Loop types only. A read-only fan-out has no loop — a re-scan is a new node, not another round.
2. Why not count the sections as rounds? Rounds measure thrash inside a loop. N sections run in parallel is the design's shape, and it is already written in `Scope`.

UNCLEAR: is `Coverage` written per section and reconciled at the join, or written once by the join over the sections' returns — and does `Findings` merge into one list there, or stay per-section? / best guess: per section, in `Scope`'s rows, with the join reconciling them (`scan → report`: "coverage manifest complete; contradictions = stop"), because a coverage manifest that only exists after the join cannot fail its own gate at the section that dropped the work.
