# Report — run 20261016-integrate-r11-r13

**Done.** R11 and R12 are now part of harness validation: `harness_health.py` reports R1–R9, R11 and R12 (R10 is
replaced by R12). It reads the guard's state through the guard's own `--json` commands (hooks per harness, success
and failure counts, open failures) and has one line for each sub-requirement no script checks. R13's one copy now
lives in the requirement-check skill (`references/use-cases-and-requirements.md`), and the skill's description and a
new section cover it. Every live pointer moved, and `docs/HARNESS_REQUIREMENTS.md` holds R11–R12. Score 10/10 criteria
(`criteria.yaml`).

## The path against its parent (R12.7)

Parent `runs/20261015-score/success-path.yaml`; one change: an independent review of the whole diff before merge. The
aim measure was **failures (parent 1, lower is better): this run recorded 15**, so the child is **not better** and does
not become a parent. Why not (*my reading*): the change was to add a step whose job is to find failures, and 4 of the
15 records are the reviewer's findings. The measure counts the finding against the run, not the defects it kept out of
master. So "failures" was the wrong measure for this change. A measure that would read it is *defects found after
merge*, which is not measured yet. Of the other 11 records, 6 have causes I can change (three are my spec's wording,
one is my command habit, one is my paraphrase, one is the export script), 2 are the Codex sandbox, 1 is the harness
refusing a subagent's file, 1 is bun's cache, and 1 is a false failure from the guard's own late-criteria check.

## Raised to EJ (R12.3: the agent proposes, EJ chooses)

`insight.md` holds 15 failure ids in 11 sections, each with 2–3 fix options. The ones that need your choice:
1. **F-8392b4ce — the guard's late-criteria check is wrong in long sessions:** it counts the whole session as one task.
   Options: mark the boundary at the request's prompt, or at the last scored criteria file.
2. **F-c60edad6 — the harness now refuses a subagent's report file**, but `.claude/agents/researcher.md` and method
   3.8 item 9 tell the researcher to write one. Options: the researcher returns text and the main agent saves it; or
   look for a setting; or run research on Codex `--search`.
3. **F-969500fa (and F-1e90a8e1 before it) — test results hidden by the command's shape**, the second time in two days.
   Options: the guard reads "N failed" from the output whatever the exit code; or a rule that a test run is its own call.
4. **F-76013d09 / F-0a1f3ca1 — Codex's sandbox loses pipe output** (its log asks for the system bubblewrap). Option:
   install bubblewrap; this is advice for your machine, I have not changed anything.

## From the research (proposed, none applied)

`research/findings.md`: 29148's nine characteristics are confirmed at second hand (a 2024 paper); GtWR and Cockburn's
own text were not readable. Proposals P1–P9, for your decision. The one that changes R13 itself: **P1/P2 — R13.2's
"minimum acceptance" reads as Cockburn's *success guarantee*;** his *minimal guarantee* (what must still hold when the
goal fails) has no field in R13.2. Should a use case also state it?

## Not done / not established
- Pushed: no. Master is ahead of origin by the earlier 2 commits plus this merge.
- The review was one pass by one engine; it checked the claims named in its brief, not everything.
- The mutants were planted by me: they show the tests catch the faults I thought of.
