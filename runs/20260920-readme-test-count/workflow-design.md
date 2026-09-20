# Workflow design — 20260920-readme-test-count

A design, not a run. Sequential by default. Method: `docs/WORKFLOW_DESIGN_METHOD.md`.

Nothing below was executed against `README.md`, and no unclear spot is resolved here. Written on 2026-09-20 at HEAD
`edd0edc`. Read in this session: `state.md`, `algorithm.md`, `readiness.md`, the method, the design template,
`.claude/workflows/intake.js` (the checks this design must pass), `README.md:15-40`, `PROJECT_OVERVIEW.md:400-412`.
Run in this session: `command -v` for `bash grep sed git python3 sha256sum diff mktemp env tail` (all found);
`git status --short` (baseline plus `?? runs/`); `NO_COLOR` is unset. pytest was not run in this step.

`RUN` below stands for `runs/20260920-readme-test-count`. "The script" means the workflow script that schedules the
pieces and runs their checks; it is not an agent. The steps s1–s6 and the spots u1–u5 are those of `algorithm.md`.

## Questions for EJ (answer before running the designed workflow)

One batch. Before p1 starts, the script writes EJ's answers into `RUN/state.md`; a question left unanswered is
recorded there with its provisional assumption, marked "assumed".

| # | Question | Provisional assumption |
|---|---|---|
| 1 (u1) | Keep the `, 0 xfailed` suffix on README.md:33, or show only what pytest prints? | Keep it: change only the number (`# N passed, 0 xfailed`) |
| 2 (u4) | Is the fix limited to the count on README.md:33, leaving README.md:19-21, the dated counts under `docs/`, and any `NO_COLOR` note alone? | Yes: line 33 only; anything else found is reported, not changed |
| 3 (u5) | After the check passes, commit the README change or leave it uncommitted for you? | Leave it uncommitted; show the diff and the check output |

Question 2 depends on u3, which only p1 can settle. It is asked in advance in its conditional form ("any `NO_COLOR`
note"); join J1 compares the answer with p1's result.

## Pieces, in the order they run

One block per piece. A piece has at most 3 steps unless a reason is given. Order: p1 → p2 → p3 → p4.

Where the algorithm's steps went: s3 → p2; s1, s2, s4 → p3; s5 → the check of p3's loop, and rerun independently as
p4 step 1; s6 → p4. Every script check below is spelled as commands that exist today. The one file they call,
`RUN/check_readme_count.sh`, does not exist at design time: p2 creates it.

### p1 — Reproduce the NO_COLOR result

- **Steps:**
  1. Run `NO_COLOR=1 python3 -m pytest -q -p no:cacheprovider` from the repo root; keep the exit code, the summary line and any line starting `FAILED`.
  2. Run `env -u NO_COLOR python3 -m pytest -q -p no:cacheprovider`; keep the exit code and the summary line.
  3. Write both results and the HEAD hash to `RUN/p1-nocolor.md`; write to the p1 row of `RUN/state.md` the two summary lines and `u3: confirmed` (the `NO_COLOR=1` run shows a failed figure) or `u3: not confirmed`.
- **Pattern:** step
- **Resolves unclear spot:** u3
- **Check:** Run by the script, not the worker: rerun both commands; the count part of each fresh summary line (the text before ` in `) equals the one recorded in `state.md`; `u3: confirmed` is recorded if and only if the `NO_COLOR=1` line contains `failed`; `git status --short` equals the baseline plus `?? runs/`. — kind: script
- **Attempt limit:** 1
- **Feedback on failure:** — (pattern step)
- **Exit when the limit is hit:** — (pattern step)
- **Needs the result of:** none
- **Files touched:** `RUN/p1-nocolor.md`, `RUN/state.md`
- **Brief — given:** The two commands of steps 1 and 2, word for word; `PROJECT_OVERVIEW.md` lines 402-410 (the recorded claim `378 passed, 1 failed` against `379 passed`, older than this run and not reproduced since); `RUN/state.md`; the rule: change no file outside `RUN/`, fix nothing, report what the commands print.
- **Brief — withheld:** The README task itself (line 33, the wording question, the edit): this agent only measures. `RUN/algorithm.md`, `RUN/readiness.md` and this design are not given.
- **Tools and skills:** Bash, python3, pytest 9.0.2, git. No skill.

### p2 — Build the count check and show it can fail

- **Steps:**
  1. Write `RUN/check_readme_count.sh` to the specification in this piece's brief.
  2. Run `bash RUN/check_readme_count.sh README.md` against the unedited README and save the output and the exit code to `RUN/p2-notes.md` (algorithm step s3).
- **Pattern:** loop
- **Resolves unclear spot:** none
- **Check:** Run by the script, not the worker, with N taken from `python3 -m pytest --collect-only -q | tail -1`: (1) `bash RUN/check_readme_count.sh README.md` exits non-zero and prints `README: 68` and `pytest: N`; (2) on a `mktemp` copy of README.md made with `sed '33s/68 passed/N passed/'` it exits 0; (3) on a copy carrying N+1 it exits non-zero; (4) `grep -c -w N RUN/check_readme_count.sh` prints 0 (no literal count in the script); (5) `git status --short` equals the baseline plus `?? runs/`. When all five pass, the script records `sha256sum RUN/check_readme_count.sh` in `state.md`. — kind: script
- **Attempt limit:** 3
- **Feedback on failure:** The exact command that failed, its exit code and its full output, saved as `RUN/p2-attempt-<n>.txt` and pasted into the next attempt's prompt.
- **Exit when the limit is hit:** Back to the unclear list as a new spot ("the count cannot be checked by a script as specified") and to EJ; p3 and p4 do not start.
- **Needs the result of:** none
- **Files touched:** `RUN/check_readme_count.sh`, `RUN/p2-notes.md`, `RUN/state.md`
- **Brief — given:** The specification: `bash RUN/check_readme_count.sh [readme path, default README.md]`, run from the repo root, (a) reads the number from the single line that contains both `python3 -m pytest -q` and `# <n> passed`, and fails if there is not exactly one such line; (b) runs `env -u NO_COLOR python3 -m pytest -q -p no:cacheprovider` and requires exit code 0 and a last line matching `^[0-9]+ passed in ` with no failed, skipped, xfailed or error figure; (c) prints `README: <n>` and `pytest: <N>`, exits 0 if they are equal and 1 otherwise; (d) changes no file. Also given: the current text of `README.md` line 33 (`python3 -m pytest -q          # 68 passed, 0 xfailed`); `pyproject.toml` (`testpaths = ["tests"]`); `RUN/state.md`; the rule: create files only inside `RUN/`, do not edit `README.md`.
- **Brief — withheld:** The number recorded by earlier sessions (379): the script must measure, never contain a count. `RUN/readiness.md` and `RUN/algorithm.md` are not given. The scope commands (`git diff --numstat`, `git status --short` against the baseline) are kept out of this script and stay with the workflow script, so that the count check can be tried on a scratch copy.
- **Tools and skills:** Bash, python3, pytest, grep, sed. No skill.

### p3 — Measure the count and edit README.md line 33

- **Steps:**
  1. Locate the count: `grep -n "68 passed" README.md` must give line 33 only, and `grep -n -i "passed\|xfail" README.md` no other line that carries a count (s1).
  2. Take the count in this same session: `env -u NO_COLOR python3 -m pytest -q -p no:cacheprovider` must exit 0 with a summary `N passed in …` and no failed, skipped, xfailed or error figure; `python3 -m pytest --collect-only -q` must report the same N; record N and the HEAD hash (s2, resolves u2).
  3. Replace only the comment on `README.md` line 33 so that the line reads `python3 -m pytest -q          # N passed, 0 xfailed` (the wording recorded in `state.md` for question 1), and write N, HEAD and the command outputs to `RUN/p3-notes.md` (s4).
- **Pattern:** loop
- **Resolves unclear spot:** u2
- **Check:** Run by the script, not the worker (these are the commands of algorithm step s5): (1) `sha256sum RUN/check_readme_count.sh` equals the value recorded in `state.md`; (2) `bash RUN/check_readme_count.sh README.md` exits 0; (3) `grep -c "68 passed" README.md` prints 0 and `sed -n '33p' README.md` equals the line expected under question 1, with the N that (2) printed; (4) `python3 -m pytest --collect-only -q | tail -1` reports the same N; (5) `git diff --numstat` is exactly `1	1	README.md`, `git status --short` equals the baseline plus ` M README.md` and `?? runs/`, and `git status --short tests/ ancient_games/ pyproject.toml` shows only `?? tests/workflows/`. — kind: script
- **Attempt limit:** 3
- **Feedback on failure:** The command that failed, its exit code and its full output (including the `README: <n>` and `pytest: <N>` lines) plus `git diff README.md`, saved as `RUN/p3-attempt-<n>.txt` and pasted into the next attempt's prompt.
- **Exit when the limit is hit:** `README.md` is left as the last attempt made it and is not reverted automatically; the script shows EJ `git diff README.md` and the attempt files; u2 goes back to the unclear list; p4 does not start.
- **Needs the result of:** p1, p2
- **Files touched:** `README.md`, `RUN/p3-notes.md`, `RUN/state.md`
- **Brief — given:** `RUN/state.md` (EJ's answers or the assumed answers to questions 1 and 2, p1's u3 result, the outcome of join J1); `README.md`; the commands of steps 1 and 2, word for word; the target line with N as its only blank; the rules: outside `RUN/` change only line 33 of `README.md`; a number from any earlier session is not evidence, N comes from this agent's own run; if pytest shows any failed, skipped, xfailed or error figure, stop and report instead of editing.
- **Brief — withheld:** The text of `RUN/check_readme_count.sh` and its recorded sha256: the worker has no reason to open the script and must not edit it. `RUN/p2-notes.md`. README.md:19-21 and the dated counts under `docs/` are out of scope and are not pointed at. Not withheld, because `state.md` carries it: the earlier figure 379.
- **Tools and skills:** Bash, python3, pytest, grep, Edit. No skill.

Why s1, s2 and s4 are one piece: u2 says the number must be taken in the session that edits. Splitting them would
pass a number from one agent to the next, which is the staleness the spot is about; it would not change the route.

### p4 — Final check, what-is-missing pass and hand-over

- **Steps:**
  1. Rerun the five commands of p3's check fresh and save their full output and exit codes to `RUN/final-check.txt` (s5, rerun by an agent that did not make the edit).
  2. What-is-missing pass: compare `RUN/state.md`, this design's success criteria and `git diff README.md`; list every check that was skipped, not run or failed, and the things found but left alone under question 2 (README.md:19-21, the dated counts under `docs/`, p1's u3 result).
  3. Write `RUN/handover.md` with the diff, the final check output, the u3 result and the list from step 2; show it to EJ; leave `README.md` uncommitted (question 3's assumption) (s6).
- **Pattern:** step
- **Resolves unclear spot:** none
- **Check:** Gate, by the script, before EJ is asked: `RUN/final-check.txt` shows exit 0 for every command and `RUN/handover.md` exists. Then EJ reads `RUN/handover.md` and accepts or rejects the diff. — kind: EJ
- **Attempt limit:** 1
- **Feedback on failure:** — (pattern step)
- **Exit when the limit is hit:** — (pattern step)
- **Needs the result of:** p1, p2, p3
- **Files touched:** `RUN/final-check.txt`, `RUN/handover.md`, `RUN/state.md`
- **Brief — given:** `RUN/state.md`; this design (`RUN/workflow-design.md`: the success criteria and the commands of p3's check); `README.md` and `git diff README.md`; `RUN/check_readme_count.sh` to run, not to edit (created by p2); `RUN/readiness.md` for the list of out-of-scope places (its Information table); the rule: change no file outside `RUN/`, make no commit.
- **Brief — withheld:** `RUN/p3-notes.md`, `RUN/p3-attempt-<n>.txt` and `RUN/p2-notes.md`: the workers' notes and reasoning. This agent judges the result from the files and the commands only.
- **Tools and skills:** Bash, python3, pytest, git. No skill.

## Joins

- **J1 — after p1, before p3: u3's result against the answer to question 2 (u4).** Done by the script from
  `state.md`. Question 2 answered or assumed "line 33 only": u3's result is reported in the hand-over and changes
  nothing; p3's expected diff stays `1	1	README.md`. EJ widened the scope (README.md:19-21, the `docs/` counts or
  a `NO_COLOR` note): p3's check no longer fits, so the run stops, u4 goes back to the unclear list and only p3 and
  p4 are planned again. EJ asked for a `NO_COLOR` note and p1 recorded `u3: not confirmed`: a contradiction, so the
  run stops and EJ is told; nothing is averaged.
- **J2 — inside the checks of p3 and p4: four sources of the number.** The number on README.md line 33, the N that
  `check_readme_count.sh` measures, the `--collect-only` count and the N the worker recorded must be equal. Any
  disagreement fails the attempt and goes back as feedback; no source is preferred over a fresh measurement.
- **J3 — question 1 against the measurement.** If any pytest run in p3 or p4 reports an xfailed, skipped, failed or
  error figure, `, 0 xfailed` and README.md:26 ("No test is xfailed") may no longer be true: the run stops and goes
  to EJ instead of writing a line that averages the two.

## Parallel candidates (optional — decided last)

Only pieces for which all five hold. Otherwise they stay sequential.

| Pieces | Neither needs the other's result | No shared files or resources | One would not change how the other is done | Each has its own check | Time saved is worth the join |
|---|---|---|---|---|---|

None. The one pair looked at was p1 + p2, which do not need each other's result. It fails point 2: both write
`RUN/state.md` (one writer at a time) and both run pytest in the same working tree. It fails point 5: the saving is
about one short agent in a run of four. p3 needs p1 and p2; p4 needs p3.

## Predictability

- Agents in total: 4, one per piece when every check passes first time. Bounds: at most 8 (p1 1, p2 up to 3, p3 up
  to 3, p4 1); concurrency 1; the script schedules and runs every script check; a failed check on a pattern-step
  piece (p1, p4) stops the run and goes to EJ.
- Cost estimate: about 120k to 250k tokens for 4 agents, up to about 500k if every attempt limit is used. Basis: a
  guess of 30k to 60k tokens per agent (each reads at most five short files and runs at most three commands); it is
  not measured, because no run of this method has reported token use yet. Suite time, measured: one full pytest run
  takes about 7.5 s wall clock (`readiness.md`), and the happy path has about 15 full runs (workers and checks
  together), so about 2 minutes. For scale: method §2 fits this task (problem, fix and check are one sentence each),
  and by hand it is one pytest run and one edited line; the workflow is being run to try the method.
- Success criteria, written before the run: (1) `README.md` line 33 reads exactly `python3 -m pytest -q          # N passed, 0 xfailed`, or EJ's wording for question 1, where N is the passed count of `env -u NO_COLOR python3 -m pytest -q -p no:cacheprovider` run fresh by the final check, with no failed, skipped, xfailed or error figure and the same N from `--collect-only`. (2) `grep -c "68 passed" README.md` prints 0. (3) `git diff --numstat` is exactly `1	1	README.md`, and `git status --short` equals the baseline in `state.md` plus ` M README.md` and `?? runs/`. (4) `check_readme_count.sh` was shown to fail on the unedited README, and its sha256 is unchanged at the final check. (5) u3 has a recorded result, confirmed or not confirmed. (6) `handover.md` lists every skipped, unrun or failed check; EJ accepted the diff; nothing is committed unless EJ answered question 3 otherwise. Stop conditions: an attempt limit is hit; a join finds a contradiction; pytest reports anything other than `N passed`.

## Debuggability

- Agent labels: `p1-nocolor`, `p2-check#<n>`, `p3-edit#<n>`, `p4-handover`.
- Every step's input and output file: input is the piece's brief, saved by the script as `RUN/<piece>-brief.md`
  before the agent starts; outputs are `RUN/p1-nocolor.md`, `RUN/check_readme_count.sh` and `RUN/p2-notes.md`,
  `RUN/p3-notes.md` and the `README.md` diff, `RUN/final-check.txt` and `RUN/handover.md`. Feedback is kept per
  attempt in `RUN/p2-attempt-<n>.txt` and `RUN/p3-attempt-<n>.txt`.
- State in one place: the script adds a section "Execution" to `RUN/state.md` with one row per piece (status,
  result, output file), EJ's answers, p1's u3 result and the sha256 of the check script. Results only, no reasoning.
- Resume point after a failure: the first piece whose row is not `done`. Every piece can be rerun alone: p1 and p2
  do not touch `README.md`; p3 starts by reading the current line 33; p4 only reads and reruns.

## Quality control

- Which checks are scripts, which are judged, which are EJ's: p1, p2 and p3 are script checks, run by the workflow
  script and never by the worker; p4's gate is a script and its acceptance is EJ's. No check is judged by an agent.
- How each script check is shown to be able to fail (sabotage check): p2's check is the proof for the count check,
  in both directions: it must fail on the unedited README (68 against N), pass on a scratch copy carrying N, and
  fail again on a scratch copy carrying N+1; a script that contains the count is refused. p3's check is then known
  to be able to fail, and the recorded sha256 shows that the worker did not edit it. p1's check reruns the commands
  itself, so a made-up summary line fails the comparison. The scope commands of p3 fail today by construction:
  before the edit `git diff --numstat` is empty, not `1	1	README.md`.
- A verifier that does not see the worker's reasoning: p4 is a separate agent and is not given any worker's notes
  or attempt files.
- The final "what is missing" pass: p4 step 2, looking at `state.md`, the success criteria above and the diff. It
  reports skipped, unrun and failed checks, and what was found but not changed under question 2.

## Assumptions and conflicts surfaced

- `algorithm.md` says the check script is "to be written in intake step 5". Intake step 5 (`verifyPrompt` in
  `.claude/workflows/intake.js`) writes `check.md`, a verification of this design; it writes no script. Chosen: p2
  of the designed workflow writes the script. The sentence in `algorithm.md` is flagged for correction, not edited
  here.
- `algorithm.md` gives the check script the scope comparison (d) as well. Chosen: the script holds only the count
  comparison, so that it can be proved on a scratch copy; the scope commands stay in the workflow script (p3's
  check, item 5).
- "s2 to s5 belong to one session" is read as: no number crosses from one agent to another. s1, s2 and s4 are one
  agent (p3); every check measures N again instead of trusting a recorded one.
- The design assumes the working tree and HEAD (`edd0edc`) are not changed by anyone else during the run. If they
  are, the checks still measure fresh, but the baseline comparison of `git status --short` will fail and say so.
