# Algorithm — 20260920-readme-test-count

Step 2 of the intake workflow (method §3.2, §3.3). A design only: nothing here was executed against README.md, and
no unclear spot below has been resolved.

Read in this session on 2026-09-20 at HEAD `edd0edc`: `state.md`, `readiness.md`, `docs/WORKFLOW_DESIGN_METHOD.md`,
the four templates, `README.md:15-40`, `PROJECT_OVERVIEW.md:400-412`. Commands run: `grep -n "68 passed" README.md`
→ line 33 only; `git status --short` → the baseline plus `?? runs/`; `NO_COLOR` is unset in this session. pytest was
not run in this step; the 379 figure is step 1's.

## Assumptions

- "The real current test count" means the summary line printed by the command the README itself shows
  (`python3 -m pytest -q`), taken on the working tree of the session that makes the edit.
- The challenge asks for a literal number in the README. A number will go stale again with the next added test
  (68 → 379 went unnoticed since `61d4cc9`, 2026-09-07). A guard against that is not asked for and is not in the
  steps (CLAUDE.md Rule 2).
- The executing agent may change `README.md` and nothing else outside the run folder.

## Steps

`N` is the number of passed tests measured in s2. "The check script" is one script, to be written in intake step 5,
that (a) reads the number from the README line, (b) runs the suite, (c) compares the two, (d) compares
`git diff --numstat` and `git status --short` with the baseline. The worker of s4 must not be able to edit it.

| Id | Action | Check | Check kind | Clear? | Blocked by |
|---|---|---|---|---|---|
| s1 | Locate every place `README.md` states the pytest result count | `grep -c "68 passed" README.md` prints `1` and `grep -n` gives line 33; `grep -n -i "passed\|xfail" README.md` gives no other line with a count | script | yes | — |
| s2 | Take the count in the editing session: run `env -u NO_COLOR python3 -m pytest -q -p no:cacheprovider` and record the summary line and the HEAD hash | Exit code 0; the summary line matches `^N passed in` with no `failed`, `skipped`, `xfailed` or `error` figure; `python3 -m pytest --collect-only -q` reports the same `N`; `git status --short tests/ ancient_games/ pyproject.toml` shows only `?? tests/workflows/` (no uncommitted test changes are being counted) | script | yes | — |
| s3 | Show the check can fail: run the check script against the unedited README | It exits non-zero and its output names both numbers (`68` in README, `N` from pytest) | script | yes | — |
| s4 | Replace the comment on `README.md:33` with the agreed wording carrying `N` | `grep -c "68 passed" README.md` prints `0`; line 33 equals the expected string exactly | script | **no** — the exact replacement text cannot be written until the wording (u1) and the number (u2) are fixed | u1, u2 |
| s5 | Run the check script after the edit | Exit 0: README number = fresh pytest `N`; `git diff --numstat` is exactly `1	1	README.md`; `git status --short` = baseline + ` M README.md` + `?? runs/` | script | yes (its expected scope changes if u4 widens it) | u3, u4 |
| s6 | Hand over: show EJ `git diff README.md` and the s5 output; leave the change uncommitted | EJ accepts the diff | ej | **no** — whether the step ends with a commit is not decided, and the action and its check differ by the answer | u5 |

Order: s1 → s2 → s3 → s4 → s5 → s6. Nothing repeats. s2's result is valid only for the session and tree it was
taken in, so s2 to s5 belong to one session.

## Unclear spots

Listed before any is resolved. None is resolved here.

| Id | What is unclear | Kind | Blocks steps | Depends on spot |
|---|---|---|---|---|
| u1 | The exact replacement wording. pytest prints `N passed in …s` and prints no xfailed figure when there are none, so `, 0 xfailed` is README wording, not pytest output. Keep the suffix or drop it? | decision | s4 | — |
| u2 | The number itself. It is a command result, not stored knowledge: 379 is dated 2026-09-20 / `edd0edc` / `NO_COLOR` unset (readiness.md "Missing or unverified", verify piece). It must be retaken in the session that edits | information | s4 | — |
| u3 | Whether a plain `python3 -m pytest -q` (the command the README shows) still gives `378 passed, 1 failed` when `NO_COLOR` is set. Recorded in `PROJECT_OVERVIEW.md:402-410`; not reproduced in step 1 or here | information | s5 — its expected scope is set by u4, and u4 part (c) cannot be put to EJ as a fact until this is known. s2 does not wait for it: it unsets `NO_COLOR` | — |
| u4 | Scope beyond line 33: (a) `README.md:19-21` describes the suite as "eight trace test cases … nine lints" and was not checked against a suite of 379 tests; (b) eight files under `docs/` carry dated counts (282 … 370) tied to named commits; (c) if u3 is confirmed, a reader with `NO_COLOR` set will not see the number the README shows. The challenge names only the count in README.md | decision | s5 (its "only README.md, one line" expectation) | u3 (part c disappears if u3 is not confirmed) |
| u5 | Whether the run ends with a commit. The challenge does not ask for one; the house rule keeps "run the suite" and "commit" as separate steps; CLAUDE.md Rule 6 says show the diff and get approval | decision | s6 | — |

## Questions for EJ (one batch)

| # | Spot | Question | Provisional assumption if unanswered |
|---|---|---|---|
| 1 | u1 | Keep the `, 0 xfailed` suffix on README.md:33, or show only what pytest prints? | Keep it: change only the number (`# N passed, 0 xfailed`). It is the smallest change, and it is true as of step 1's run and README.md:26 ("No test is xfailed") |
| 2 | u4 | Is the fix limited to the count on README.md:33, leaving README.md:19-21, the dated counts under `docs/`, and any `NO_COLOR` note alone? | Yes: line 33 only. Anything else found is reported, not changed |
| 3 | u5 | After the check passes, commit the README change or leave it uncommitted for you? | Leave it uncommitted; show the diff and the check output |

## Risk

**Low.** Judged separately from size:

- Noticed late? Not with the s5 script: a wrong number fails the comparison at once. (Without a check it would be
  noticed late — README.md was last changed on 2026-09-07 (`61d4cc9`, per readiness.md) and the wrong number has
  stood unnoticed since some point after that.)
- Can it be undone? Yes: one tracked line, `git checkout README.md` or a revert.
- How much does it touch? One comment on one line of one documentation file. No code, no test, no running system,
  no shared state.

What the low rating does not cover: the number going stale again after this run, which the challenge does not ask
to prevent.

## Not decided here

Size (step 3), the form of the output (step 4), the check script itself and its sabotage proof (step 5).
