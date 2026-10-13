# Question

This is a relay. You write the **first copy** of a proposal. Four other experts will each improve the same copy
after you, one at a time.

The repo has several different sets of trust tags for research findings. They should be one set. Which set (or
which new set) should be the single official one, where should it live, and what should each tag mean?

In your `## Answer` section: one or two sentences, then a heading `### The copy` containing the complete proposal —
the tag names, a one-line definition each, the rule for when two tags seem to fit, where the definition lives, which
files change to point at it, and what happens to old files. Write the copy so the next expert can improve it without
reading anything else of yours. Do not search the web; work from the facts below.

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
