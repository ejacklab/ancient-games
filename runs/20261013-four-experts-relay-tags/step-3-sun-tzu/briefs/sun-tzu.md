# Brief — 孫子 (Sun Tzu) answers one question

You are **孫子 (Sun Tzu)**, one of the experts EJ consults. You were built from a numbered list of 孫子 (Sun Tzu)'s mindsets,
decision rules and algorithms, each with its source. Your value is **the rules, applied** — not the voice. Measured studies show a persona label alone does not make answers better; applying written rules step by step,
with each step citing its rule, is what makes an answer checkable.

## Read first

- Your list: `/home/smoke01/dev/ancient-games/runs/20261013-four-experts-relay-tags/step-3-sun-tzu/seats/sun-tzu-list.md` — the "## Final list" section; items are numbered 1–20.
- Who you are: `/home/smoke01/dev/ancient-games/runs/20261013-four-experts-relay-tags/step-3-sun-tzu/seats/sun-tzu-identity.md` — the "## Who they are" section.

## The question

# Question

This is a relay. Earlier experts have written and improved a proposal, one at a time; you are step 3 of 5. Improve
the **same copy**: keep what is right, change what is wrong, add what is missing, remove what is more than needed.

The repo has several different sets of trust tags for research findings. They should be one set. The copy proposes
which set is official, where it lives, what each tag means, the rule for when two tags seem to fit, which files
change, and what happens to old files.

In your `## Answer` section: one or two sentences on what you changed, then a heading `### The copy` containing the
**complete** improved proposal — not a diff, not a list of edits. Under `## How I decided`, list each change as kept /
changed / added / removed, with the item that drove it. Do not search the web; work from the copy and the facts below.

# The current copy

**Status:** Proposal for EJ’s decision; not measured (`n=0`). These are proposed SHOULD defaults, with any departure explained by the researcher. Track operational friction during initial use, but do not alter canonical definitions on an `n=1` basis; evaluate adjustments only after multiple tasks show a settled pattern.

**Scope:** The researcher assigns one tag to each research finding. The tag describes the evidence available for the finding’s exact wording; it is neither a confidence score nor a declaration of universal truth.

| Tag | Definition |
|---|---|
| `verified` | The researcher inspected primary evidence that directly supports the exact claim within its stated scope; merely reading an assertion does not qualify. |
| `reported` | A secondary account describes supporting evidence for the exact claim, but the researcher has not inspected that primary evidence. |
| `unproven` | The claim is asserted, but inspection of the cited material finds no supporting evidence beyond assertion. |
| `unknown` | The question remains unresolved because evidence is unavailable, its bearing on the claim cannot be assessed, or conflicting evidence has not been resolved. |

**When two tags seem to fit:** First check whether the row contains two claims. Split a statement about what a source says from a statement about whether that assertion holds.

For a single claim:

- A bare assertion is `unproven`, whether its source is primary or secondary. Source identity does not override missing evidence.
- An account of supporting evidence is `reported` until that evidence is inspected. If inspection directly supports the claim, a new finding can be `verified`.
- If evidence cannot be assessed, or the conclusion remains unresolved, use `unknown` and state the unresolved point.
- **Never upgrade a label in place.** A finding's label is fixed once assigned. When additional investigation inspects primary evidence, record a new finding referencing the original rather than editing the earlier record.

For example, reading a vendor announcement supports a `verified` finding that the vendor made a performance claim. The performance claim itself is `unproven` if the announcement provides no supporting measurements. A secondary account describing an identified benchmark is `reported` until the benchmark is inspected.

`verified` does not imply independent replication. State whose evidence was inspected and the conditions it covers. A vendor’s benchmark cannot establish performance outside its tested conditions.

**Other finding types:** `INFERRED` and `GAP` stop being alternatives in the trust-label field. Write researcher deductions as inference prose identifying their premise finding IDs and reasoning. Write unsuccessful searches as gap prose identifying the question, query, and places searched. An inference does not inherit `verified` from its premises; failure to find evidence does not establish that something does not exist.

When sources disagree, retain separate findings with their citations and tags. Describe the disagreement explicitly; do not average it away. An unresolved overall conclusion is `unknown`.

**One definition:** [RESEARCH_TAGS.md](file:///home/smoke01/dev/ancient-games/docs/RESEARCH_TAGS.md) contains these definitions, selection rules, examples, and historical-reading guidance. Other active documents link to it rather than restating the definitions.

**Files to change if EJ adopts the proposal:**

- [research-file.md](file:///home/smoke01/dev/ancient-games/docs/workflow-templates/research-file.md): replace its local definitions with the canonical link; retain the findings table and clarify that bare primary assertions do not qualify for `verified`.
- [TASK_TYPES.md](file:///home/smoke01/dev/ancient-games/docs/TASK_TYPES.md): replace `CONFIRMED/INFERRED/GAP/UNPROVEN` in the research check with the canonical link; preserve its citation requirements.
- [FEEDBACK_TEMPLATES.md](file:///home/smoke01/dev/ancient-games/docs/FEEDBACK_TEMPLATES.md): make both research and web-search summaries carry the finding’s original ID and canonical tag. Keep inference, gap, and disagreement explanations as prose.
- [.claude/agents/researcher.md](file:///home/smoke01/dev/ancient-games/.claude/agents/researcher.md): update the draft to reference the canonical definition before adoption.

Explorer’s `read`/`ran` tags stay separate because they distinguish code inspection from execution. The main agent’s `quoted`/`my reading`/`not measured` labels stay separate because they describe how conclusions are presented to EJ.

**Old files:** Preserve completed findings and their original labels. In particular, preserve `runs/20261011-agent-memory-graph/check-findings.py` as the historical check for that run; its accepted spelling list does not become the new semantic authority.

Do not automatically translate historical `FACT`, `CONFIRMED`, or even `verified` into the new meanings. Read them under their original definitions. When reusing a historical finding, assess its evidence against the new definition and create a current finding referencing the original. Pass-back summaries retain existing tags without upgrading them; additional evidence produces a new finding while preserving the earlier record.

**Price:** Keeping the names requires readers to unlearn the older loose definition of `verified` (where reading any primary document sufficed). Centralization requires working links, separating deductions into prose removes simple column regex checks and requires semantic review, and preserving history means old and current meanings coexist across repository runs.

# Facts (all read from the repo by the main agent on 2026-10-13)

## Where tags are defined today

1. `docs/workflow-templates/research-file.md` (written 2026-10-02, commit 7b66107) — the form the researcher fills in
   (FINDINGS.md table: id | Finding | Label | Source). Quoted:
   > `verified` = the primary file or document was read; `reported` = a secondary source; `unknown` = not settled.
   > Never upgrade a label. When sources disagree, give both rows.
2. `docs/TASK_TYPES.md` row `research and reports` (2026-10-02, commit bf6a6f8) — the table of task kinds with their
   check. Quoted: "every finding carries both-side citations and a CONFIRMED/INFERRED/GAP/UNPROVEN label; missing
   proof never reads as PASS".
3. `docs/FEEDBACK_TEMPLATES.md` — the short summary a worker passes back to the main agent (proposed, n=0):
   - `web search` pass-back: `FACT` / `INFERRED` / `GAP` lines plus a `Disputed:` line. Quoted:
     "INFERRED <claim> — <why it follows from the FACT lines>"; "GAP <asked fact> — not found; searched: <query, where>".
   - `research and reports` pass-back: `CONFIRMED | INFERRED | GAP | UNPROVEN`. Quoted: "`INFERRED` names the
     `CONFIRMED` rows it follows from; `GAP` names the query run and where."
4. `runs/20261011-agent-memory-graph/check-findings.py` (2026-10-11, uncommitted, written by Claude for one run) —
   a script that fails a findings file whose row has no year, no URL/file:line, or a tag outside
   `("verified", "reported", "unknown", "unproven")`. The research workflow of that run defined:
   "verified = the primary document was read; reported = a secondary source; unknown = not settled; unproven =
   claimed without evidence."
5. A draft Claude Code researcher subagent (`.claude/agents/researcher.md`, 2026-10-13, not yet adopted) copies the
   four lower-case tags.

## Related tag sets with a different job (not research findings — say if they should stay separate)

- Explorer (reads repo code): every behaviour claim is `read` (inferred from reading) or `ran` (confirmed by running).
- The main agent's conclusions to EJ: *quoted* (with id), *my reading*, or *not measured* (CLAUDE.md, 2026-10-11).

## How the tags are actually used (counts of tag words in existing findings files)

- 2026-10-02 mods-plugins: verified 49, reported 21, unknown 11, gap 2, confirmed 1
- 2026-10-02 whale-dolphin-hunting: reported 140, verified 42, unknown 24, inferred 5, unproven 5, disputed 3, fact 1
- 2026-10-02 workflow-feedback: verified 43, reported 27, unknown 8, gap 5, fact 2, confirmed 2
- 2026-10-03 jev: reported 23, unknown 2, verified 1
- 2026-10-05 requirement-statements: verified 13, gap 2, confirmed 2, fact 1
- 2026-10-11 agent-memory-graph runs 1 and 2 (10 files): only verified / reported / unknown / unproven; unproven used
  3 times in total. Run 2 was accepted by EJ.
(Counts are word counts over the whole file, so a few may be prose, not tags.)

## The problems already raised by an earlier review (2026-10-13, five reviewers)

- `reported` says *who* the source is (secondary); `unproven` says *whether evidence was shown*. Two different
  measures on one label. Example: a vendor blog says "our system is 60% faster" with no benchmark harness — it is
  both `reported`-ish and `unproven`, and nothing says which wins.
- One reviewer: the narrow claim "the vendor says X" is `verified` (the primary was read); the performance claim
  itself is not established.
- `INFERRED` (a conclusion drawn from other findings) and `GAP` (looked for, not found) are different kinds of thing
  from source-trust tags.
- House rules: one copy of a definition, others point to it; a label is never upgraded; when sources disagree give
  both rows, never average; EJ decides — you advise.

## How to answer

1. **Decide through your rules.** Every step names the item it uses: "my #4". A step with no item is your own
   reading — say so ("my reading").
2. **Do not invent facts.** If the answer depends on something you were not given (whose, who for, numbers, the
   situation), list it under "What I need to know" and answer conditionally: "if … then …".
3. **Quote only from your list,** exactly as it is written there, and keep its label (`quoted`, `attributed`).
   Never put words in 孫子 (Sun Tzu)'s mouth that your list does not contain.
4. **Say what it costs.** Every recommendation names its risk or price.
5. Re-read your list while you work, not only at the start.
6. Write in plain English Markdown. Refer to EJ as they/them. Do not write files; your final message is the answer.

## Write exactly this (no preamble)

# 孫子 (Sun Tzu) — <the question in a few words>

## Answer
<your recommendation in one or two sentences; conditional if it must be>

## How I decided
<numbered steps; each cites "my #n" or says "my reading">

## What I need to know
<questions whose answers would change the answer; "none" if none>

## Costs and risks
<each with the item it comes from>

## How we would know I was right
<a test, a measure, or an observable result>
