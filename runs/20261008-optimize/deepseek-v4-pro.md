# deepseek-v4-pro — optimize the workflow-design method

Verdict up front: **not lean.** The method (579 lines) has two long first-person
post-mortem narratives, one deleted-rule archaeology, several definitions stated twice,
and a summary section (§5) that re-states the operative sections. Ordered by value.

## The cuts/merges (highest value first)

1. **Cut the deleted-rule archaeology — 3.7 "Caps — deleted", lines 395–408.**
   ~14 lines explaining a rule that no longer exists. Keep only the two live sentences:
   "the pair survives in the spike rule" and "many roles is a design question, not a
   cap." The concurrency unit table (410–423) already states the operative distinction
   (sessions vs processes vs approaches) better than the deleted history does.

2. **Cut the "C was revisited" traversal story — 3.6, lines 356–370.**
   The operative rule is four lines: design and plan are two artifacts, the COO writes
   both, `dispatch.py validate PLAN --design DESIGN` compares asymmetrically (design's
   promises must survive; the plan may add, not lose), and omitting `--design` errors.
   Everything else — "decided as C — leave it", "C was revisited the same day", the
   two-checks-vanished anecdote, the italicised moral (369–370) — is narrative, not rule.

3. **Merge the two baseline definitions — 3.1:88–89 and 3.6:332–333.**
   The same concept ("the product's test command and its output") is defined twice in
   different words. Define once at 3.6 (where the three-part stop actually uses it) and
   make 3.1 point there; its only job there is "a git-status snapshot is not the baseline."

4. **Collapse §5 "Three qualities" (573–579) into a pointer list, or delete it.**
   It re-states 3.5/3.6/3.7: check-per-piece, blind verifier, check-can-fail, contradiction
   at joins, the three-part stop. As a final checklist it should be short bullets that
   cite the sections, not re-definitions. Half its cells duplicate §3 verbatim in spirit.

5. **De-duplicate "provisional assumption stands unless corrected" + "blueprint questions
   are not answered by silence" — stated in 3.0:68–71, 3.1:177–183, 3.3:231–236 and
   3.4:243–244.** Keep one canonical statement (3.3) and reference it; the 3.0 and 3.4
   restatements add nothing.

6. **Compress the git-status bug narrative — 3.1:85–91.**
   Keep the rule ("readiness checks the git *binary*; a plain directory must work; a
   `git status` snapshot is not the baseline"). Drop the "Before 2026-10-05 the runnable
   form ran `git status --short` unconditionally and a plain directory died at the first
   step of every run (register 9.2)" history — it is a register entry, not method.

7. **Move §4's project-memory detail (551–567) to an appendix.**
   The three append-only files (`decisions.md`, `changelog.md`, `lessons.md`) with their
   per-entry schemas are not needed to learn the method. The core state-file rule
   (528–533) stays; the memory-table section is "how we remember", a separate concern.

8. **Move the "One word, one job" glossary (11–20) to an appendix.**
   It is *not* duplicated — it appears once — but it is vocabulary, not method, and a
   first-time reader does not need it before §1. Glossary-at-the-end, not front matter.

9. **Trim 3.8's instance-level items to pointers.**
   The bundled-runtime preamble (434–438), item 5's failure catalog ("qwen headless exits
   0 …", 473–476) and item 11's runlog/harvest machinery (513–520) all already live in
   `docs/EXECUTOR_KINDS.md` / are implementation detail. 3.8 is the bloat centre — 12
   numbered items — and three of them are second copies of executor facts.

10. **SKILL.md is a second full copy of the method, not the "links" CLAUDE.md claims, and
    it has already drifted.** CLAUDE.md says "one copy of each"; SKILL.md re-states the
    whole method inline (219 lines). It contains rules the method doc lacks — "call the
    CLI first and the provider tool second" (2026-10-04) and the opencode engine split /
    `workload.py` — so the two sources of truth have already diverged. Either make it
    genuinely link-only or accept it as the canonical copy and delete the re-statements.

## Candidate duplicates I checked and cleared

- **"who fills it"** — not duplicated *within* the doc: it is applied consistently in two
  tables (blueprint "Whose decision", 132–141; memory "Written by, when", 556–560). The
  rule itself lives in CLAUDE.md, correctly. Leave it.
- **"one word one job"** — single occurrence (see item 8; a placement problem, not a copy).
- **the loop's five conditions** — stated once in the doc (3.5:281–292); the second copy is
  SKILL.md step 5, folded into item 10.
- **the three-part stop** — defined once (3.6:329–336); the repeats are §5 and SKILL, both
  covered by items 4 and 10.
- **five things a node carries / the state file / acceptance criteria** — all core and
  compact; do not cut. The heavy part around the state file is the memory table (item 7),
  not the state-file rule itself.

If forced to a single trim: **item 1** — the deleted-caps archaeology is the longest
stretch of text whose only subject is a rule that no longer exists.
