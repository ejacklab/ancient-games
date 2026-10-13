# Brief, stage 3 — review one proposed algorithm for `INDEX.md`

You are one of three independent reviewers. You do not see the other reviews.

## What you review

`/home/smoke01/dev/ancient-games/runs/20261012-index-md-algorithm/proposals/claude.md` — a proposed algorithm for
generating `project-memory/INDEX.md`, with 3 supporting reasons, 6 must-not-dos and proposed design changes.

## What you check it against

- The design it serves: `/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md` (read in full; the
  relevant parts are K6, Rd1–Rd3, W1, W4, W6).
- The evidence it cites, the finding ids `C*`, `X*`, `O*`, in:
  - `/home/smoke01/dev/ancient-games/runs/20261012-index-md-algorithm/lit-review/claude.md`
  - `/home/smoke01/dev/ancient-games/runs/20261012-index-md-algorithm/lit-review/codex.md`
  - `/home/smoke01/dev/ancient-games/runs/20261012-index-md-algorithm/lit-review/opencode.md`

All of these are local files. You need no web access for this review.

## Your task

Find what is wrong or missing in the proposal. For each problem:
- **Where:** the step, reason, must-not or design change, by its number.
- **What:** one or two sentences.
- **Failure case:** concrete inputs or a concrete sequence of events, and the wrong result it produces.
- **Severity:** *breaks* (the algorithm gives a wrong index or a wrong pass/fail), *gap* (a case it does not cover),
  or *minor* (wording, clarity).

Look in particular for:
1. A sequence of git operations (branch, merge, rebase, cherry-pick, a clone without the hooks, `--no-verify`) that
   leaves a wrong `INDEX.md` committed while the check passes.
2. An entry file the parser reads wrongly: header format, quotes, a claim without `**Why:**`, unusual file names.
3. A citation that does not say what the proposal says it says. Open the cited finding id and compare.
4. A requirement in `SOURCE_OF_TRUTH.md` that the proposal breaks or quietly changes.
5. A part the proposal does not need: the owner's rule is that memory is simple, and a mechanism that is not needed
   is removed.

Do not write a competing algorithm. If a problem has an obvious fix, give it in one line.
If you find nothing wrong under a heading, say so. Do not invent problems to fill the list.
Read only; do not change any file in the repo.

## Output — one markdown report

```
# Review of proposals/claude.md (<your engine name>)

## Verdict
One of: ACCEPT, ACCEPT WITH FIXES, REJECT. One sentence why.

## Problems
| # | where | what | failure case | severity | fix (one line, if obvious) |

## Citations checked
| finding id | what the proposal says it shows | does it? (yes / partly / no) |

## What holds up
Short list.
```

The launcher tells you your engine name and where the report goes.
