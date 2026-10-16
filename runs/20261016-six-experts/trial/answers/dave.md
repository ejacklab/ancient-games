# Dave — what a pre-flight check should verify in a brief or question file

## Answer
Verify only the file's shape, never its meaning. Check for four things: one fresh result destination the post-check can test, every template part filled with no placeholder left, limits that parse and read-paths that exist, and, only after a replay shows no false fails, the one spec-shape pattern that misled two coders. Anything that needs a reader (clarity, paraphrase, truth) stays outside the check.

## How I decided
1. **Start from what is already measured** (my #5). The loaded insights are the only measured faults of this kind. The spec category has 8 ids. A script could see 2 by shape (`runs/20261016-integrate-r11-r13/insight.md#F-4cbb2f4b`, `#F-05a1b440`). It could see 3 only by a weak guess (`#F-b7c8635f`, `#F-2cdebf3b`, `#F-d0736dc7`, a JSON contract written as prose). It cannot see 3 at all (`#F-90389583`, `#F-d8a49e5a`, and `runs/20261016-time-monitor/insight.md#F-84636a96`, which the post-answer check already catches). So most brief faults need a reader, and a pass from this check means "well-formed", not "right". The insights also contain no count of briefs with these shapes that were fine, so false-fail rates are unknown.

2. **Item 1: one fresh result destination** (my #5, #10).
   - *Looks for:* under "Write the result to", exactly one path inside `runs/<id>/`, whose folder exists and whose file does not exist yet.
   - *How a script tells:* read the section and stat the path.
   - *Prevents:* the engine exits 0 and writes nothing, so a missing or stale file goes unnoticed. This is `runs/20261015-ts-hybrid/e4/runs/A2/insight.md#F-c5874495`, `runs/20261015-ts-hybrid/e4/runs/A3/insight.md#F-79db2403` and `runs/20261015-ts-hybrid/e4/runs/B2/insight.md#F-6184fa1e`. Those runs hit one planted shim in a sandbox (B2's why 3 calls it deliberate), so they are one condition seen several times, not several independent failures. `runs/20261015-ts-hybrid/e4/runs/B1/insight.md#F-5c0f9976` has an unconfirmed cause.
   - *What it changed:* a pre-flight cannot catch a silent engine, only fix the target the post-check will test (see step 9). The stale-file clause is my reading.
   - *Engine-conditional:* `runs/20261016-integrate-r11-r13/insight.md#F-c60edad6` shows the harness refusing a subagent's report file. For a Claude subagent, the item should require a named return shape instead of a path (n=1).

3. **Item 2: every template part present and not blank** (my reading).
   - *Looks for:* the headings of `docs/workflow-templates/node-brief.md`, read from that file so the script cannot drift from it, each with text under it. "Pieces and progress" must name a progress path.
   - *How a script tells:* heading match plus non-empty body.
   - *Prevents:* a worker with no standard, no example or no timestamped progress line. `#F-4cbb2f4b` option 3 shows a missing example row doing damage. The runner already does this on the answer side (`answer_ok` fails on missing sections), but nothing does it on the question side.

4. **Item 3: no surviving placeholder; limits parse** (my reading).
   - *Looks for:* any `<…>` string that is in the template and still verbatim in the brief, and timers in Limits that are positive numbers with units.
   - *How a script tells:* set difference against the template text, then a number parse.
   - *Prevents:* the engine being told to write to a literal `runs/<id>/nodes/<node>-<attempt>.result.md`.
   - *Adjacent evidence:* `runs/20261016-time-monitor/insight.md#F-a03fa5b3`, a time typed from recall that was a year off and was caught only by a sign check.

5. **Item 4: paths it tells the engine to read exist** (my #2).
   - No loaded insight shows a dead path in a brief, so this has no failure behind it. A stat call costs less than arguing about it, so I keep it.

6. **Item 5: the spec-shape pattern** (my #10).
   - *Looks for:* in a brief item that defines output text, a backticked literal followed by a parenthesis or instruction in the same item, or a new record shape with no example line.
   - *How a script tells:* regex.
   - *Prevents:* the coder copying `(12) …` into names, or ending output with "(ids not printed)". See `#F-4cbb2f4b` and `#F-05a1b440`. That is n=2, one author, one run: "n=1 is a hint, not a law" (`EJ's rule`), and n=2 here is the same hint. The regex also matches ordinary prose, so it ships off until the replay (step 11).

7. **Deliberately not verified** (my #5, #9). Each of these needs a reader, a test or a different check:
   - Ambiguity such as "first paragraph" (`#F-05a1b440`). A second engine's reading caught it, which is an AI call and outside this check.
   - Paraphrase against its source (`#F-d8a49e5a`).
   - JSON field types (`#F-b7c8635f`, `#F-2cdebf3b`). The fix is a writing rule: a table, never prose.
   - Runtime side effects (`#F-90389583`). That needs a test in an empty HOME.
   - Chinese quote variants (`#F-84636a96`). `check_one` already compares exactly after the answer, and the brief already carries the "character by character" sentence.
   - Engine command shape (`runs/20261016-time-monitor/insight.md#F-173e0190`). That is a test run when the runner changes, not a per-call check.
   - Engine quota and PATH (`runs/20261015-ts-hybrid/e4/runs2/B2/insight.md#F-acd8b58b`). That is a property of the engine, not the file, and the runner already has `codex_left`.

8. **Proposed change to the pattern:** a twin check after the engine ends (my reading).
   - It checks that the result file exists, is non-empty and has the template's headings. It also checks that every `planned` progress line has a `done` or `fail` line with an ISO time.
   - *What it changes:* "done" and "timestamped" are confirmed by a script reading files, not by the worker's own report. This makes EJ's "small pieces, timestamped" rule checkable.

9. **Nature step** (my #6, #7).
   - *Mechanism borrowed:* immune selection. Test a new receptor against "self" before it is armed (here, run a new item on known-good briefs), and expand only what matched a real threat (here, add items only from a logged fault).
   - *Same:* the same author repeats the same faults, and false fails are the cost, like autoimmunity.
   - *Different:* pathogens evolve, and our faults come from one author's habits.
   - I keep only the "test against self before arming" part, because it does not need an evolving enemy. I drop the rest of the analogy.

10. **What would change my mind** (my #1). If, over the run's time, faults that reach the engine after a pass outnumber the faults the check caught, the check is aimed at the wrong faults and the effort belongs to a second reader instead.

11. **Test before shipping** (my #2, #3, #4, #8). Run items 1–5 on one path first (worker briefs), on known-good briefs plus the uncorrected H4/H5 text. The prediction is written under "How we would know".

12. **Insight categories.** `spec` was right. `tool` was half right: 6 of its 12 rows (`#F-c5874495`, `#F-79db2403`, `#F-5c0f9976`, `#F-d9b6b41b`, `#F-6184fa1e`, `runs/20261015-ts-hybrid/e4/runs2/B3/insight.md#F-431b04f6`) bear on item 1. `own-work`, which was not named, held two rows that changed the answer (`#F-c60edad6`, `#F-a03fa5b3`). No insight applies from `#F-785afc27`, `#F-99ea442b`, `#F-682702da` and `#F-86553997`: they concern guard records, hooks, export and types.

## What I need to know
1. Is there a machine-readable list of what a worker must not see, such as planted controls? A project memory note says planted controls must never be named in a file a worker reads, but I only know that from the memory list, so it is recall. If yes, add a no-leak item first, since a leak voids a run and a grep is free. If no, nothing changes.
2. Is there a template for question files, like `node-brief.md` for worker briefs? If yes, items 2 and 3 read their headings and placeholders from it. If no, question files get items 3 and 4 only, and item 1 is the runner's own job, because the runner names the answer file.
3. How does each engine hand its result back, as a file or as text? `docs/EXECUTOR_KINDS.md` should say, and I have not read it. If a Claude subagent must return text, item 1 becomes "return shape named" for that engine.
4. Can the specs before their "Corrections" (H4 and H5 in `integrate-r11-r13`) be recovered from git history? If yes, the replay for item 5 is a real control. If no, item 5 rests on four corrected lines and stays off.

## Costs and risks
- **False fails are paid on every call** (my #4, #8). Item 5's pattern matches normal prose. The price is a blocked good brief, and the mitigation is that it ships off until the replay.
- **A pass can read as "right"** (my #10, step 1). Six of the eight loaded spec ids are invisible to a script. Mitigation: the pass line says "shape ok; meaning not checked".
- **Item 1 rests on one planted shim** (my #10). The real frequency of silent engine failure is unmeasured. The item is cheap, so I keep it.
- **Item 3 fails a brief that quotes the template**, such as a brief about briefs, so it needs an escape (my reading).
- **Each item is code plus a test, and items are added only after a logged fault** (my #6). Coverage grows slower than guessing would, which is the intended trade.
- **I have no timing for the check** (my #5). It should take milliseconds, but I have no measurement and the first runs must record it.

## How we would know I was right
- **Prediction, written first** (my #3):
  - Items 1–4 fail 0 known-good briefs.
  - Item 5 fails the uncorrected H4/H5 lines, and passes H3 and the corrected lines.
  - The stop date is the end of the time EJ sets for the run; I do not invent one.
- **Metrics per item** (my #4): true catches (the main agent fixed the brief and the next call worked), false fails (the main agent judged the brief fine), and misses (a brief fault logged in the insights after a pass). The control is the current way, no pre-flight. Its baseline is the faults already logged, 8 spec ids plus 6 silent-output rows, compared per run before and after.
- **Decision rule:** an item whose false fails exceed its true catches by the stop date is cut. An item that never fired is reviewed, not cut, because zero fires may mean the fault is gone.
- **Reporting** (my #9): log every fail and every pass with the item that fired, and report null results at the same weight as catches. With few runs, any result is a hint (my #10).
