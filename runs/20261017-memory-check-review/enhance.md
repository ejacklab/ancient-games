# Enhance picks — memory-check, after round 1

Step: pick (review-enhance). Sources I read: `enhance-q/compare.md` and the six answers under `enhance-q/*/answers/`.
The main pick is applied (R12.3); the owner may overrule any pick.

Labels: *quoted* (an answer's own words), *my reading*, *not measured* (nobody in this step ran it).

## The ground these picks stand on

- The judge never finished. `findings.md` does not exist, and `nodes/review-enhance.progress.md` has
  `judge-r1 · start` (23:11:34) and no done or fail line for it. I checked both at 23:24. So every expert worked
  from the two raw reviews that no judge has looked at, `review/r1-codex.md` (12 findings) and `review/r1-agy.md`
  (5). No fix has landed. All six experts say this.
- What that means for the picks (*my reading*): each pick is a general rule plus the test that proves it. The single
  findings it covers are still the fix loop's job if the judge is run again and accepts them. If the fix loop runs
  first, a pick gets smaller (Dave: *quoted* "improvement 1 shrinks to the floor rule plus one fault test per read
  path"). It does not go away.
- The cited code lines in E-1 and E-2 I read myself (`command.ts:105-122`, `checks.ts:105-120`, `:205-215` and the
  early returns at `:212-282`, `cachechecks.ts:60-72`). I ran none of them. The only behaviour anyone measured is
  孫子's fixture run and Linus's in-memory probe. Both were run by the experts themselves, and the comparer did not
  repeat either.

## Picks

### E-1 (main pick): a check that could not read its input never reads as clean

- **What:** a "not applicable" or "pass" result needs a read that worked. If the read that would have found memory
  (or a break) failed or was not done, the result is "could not run", and the reason is the error text. One
  table-driven fault test proves it, with one row per input the tools read.
- **Use case / vision line:** U2 Fails if: *quoted* "a result has no evidence (a file and line, or a command and its
  output), or a MUST that fails is shown as passing". U3 Fails if: *quoted* "a MUST that fails or could not run …
  is not in the warning". `VISION.md:23`: *quoted* "Say a requirement passes without the evidence that shows it."
- **Who agrees:** five of six. It is the top pick of 老子, Dave and Dario, it is 孫子's #2, and 范蠡's #1 and #2 rest
  on the same cases. Linus does not mention it. The fault-test form is 孫子 #2, 老子 #1 and Dario #2, and Dave asks
  for four fault fixtures built one at a time.
- **The case that shows the need** (raw findings, not judged; the code lines are *my reading*):
  - `checks.ts:111`: `projectMemory` is `stagedMemoryPaths(...).length > 0`. A failed `git ls-files` only adds a note
    (`:116`), so the list comes back empty. Then `checks.ts:212` makes every SoT record "not applicable", and the
    run exits 0. This is `r1-codex.md:7`.
  - `cachechecks.ts:66-71`: an unreadable session-start file is recorded as "(unreadable)" and skipped with
    `continue`, so Rd1 can pass. This is `r1-codex.md:25`.
  - `tools/memory_index.py:483-485`: with an unborn HEAD it exits 0 before it reads the staging area
    (`r1-codex.md:19` = `r1-agy.md:192`). Dario adds *quoted* "`checks.ts:262` uses it only for clauses in
    `AFTER_ENTRIES`", so *quoted* "a staged `status: bogus` entry in a repo with no commits probably passes W4.1b"
    (*not measured*).
  - `tools/memory_index.py:354`: only 40-character object ids are accepted, so a SHA-256 repository looks as if it has
    no memory (`r1-codex.md:21`).
- **Why it comes first:** the previous round fixed this class one case at a time (commit 24e0fba, which Dario cites),
  and this round's reviewers found four more. 老子: *quoted* "that one shape is seven of the fourteen distinct defects
  this round found". The previous round's could-not-run warning cannot catch these cases, because they never become
  "could not run" in the first place (Dave).
- **Where it goes:** the guard sits on the TypeScript side (`checks.ts`, Dario's shape). If memory-check's own staged
  read found entries and `memory_index.py` reports `noMemory` or `unbornHead`, every clause the tool checks is
  "could not run". Built this way, E-1 needs no change to `memory_index.py`. Fixing the Python instances themselves
  (the unborn HEAD, the 64-character ids) is the fix loop's job. On whether those fixes may touch `memory_index.py`,
  two lines conflict, flagged here and not settled by me: the run request says *quoted* "memory_index.py in scope",
  and so does `design.md:7` Q2, but `REQUIREMENTS.md:43` C3 says *quoted* "never changes `memory_index.py`".
- **Check first (Dario's open fact, *not measured*):** confirm that memory-check's staged-entry read uses the same
  `[DFLOH]-*.md` filter as `memory_index.py`. If it does not, the guard raises false could-not-run results.
- **Known cost:** a rule that is too wide makes the session-start hook noisy (老子, Dave, Dario). 孫子 answers that
  a false "could not run" is visible and exits 1, so it fails safe. The control row below is what bounds the noise.
- **How to check it is done:**
  1. One test table, one row per input: the git index (`git ls-files` fails), an unborn HEAD with a staged entry
     (`status: bogus`), a `git init --object-format=sha256` repo with staged entries, an unreadable
     `.claude/settings.json`, and the `memory_index.py` run failing. Each row is shown red on the current HEAD (a MUST
     that is `pass` or "not applicable", exit 0). After the change, each row gives "could not run" with the error
     text, exit 1, and one `--warn` line.
  2. The early returns and exemptions on the rerouted path, listed before the test is written, each get one row fed a
     could-not-read case: the `OUTSIDE_PROJECT_MEMORY` exemption (`checks.ts:57`, W3.5a, W3.5b, Rd1.1) at the
     "not applicable" return (`checks.ts:212`), the `AFTER_ENTRIES` set (`checks.ts:64`) at `:262`, and the final
     `pass` (`checks.ts:282`). (Agent lesson test-exemptions-on-reroute.)
  3. Control: a repo that never had `project-memory/` still gives "not applicable" and exits 0. The baseline stays
     the same (bun 74 pass, pytest 465 pass, tsgo exit 0), and so does this repo's own report.
  4. A mutation that turns a read failure back into `pass` makes the table red again.
  5. The table is written by an engine other than the one that writes the fix (Dario: `crossed-build-check`), so
     the check is independent.
  6. A row that is already green on HEAD means that finding was not real. Drop the row and report it (Dave).

### E-2: `--out` must never overwrite memory

- **What:** if the `--out` path resolves to a memory location (anything F1 lists, aliases such as symlinks and `..`
  included), it is a usage error: exit 2, the file's bytes unchanged. A normal report path still writes.
- **Use case / vision line:** `VISION.md:22`: *quoted* "Change any memory, entry, index or cache: it only reads, and
  writes only its own report." F3 (`REQUIREMENTS.md:20`) says the same. U5 Fails if, still *proposed*: *quoted*
  "after a run, `git status --short` shows any change other than the report file."
- **Who agrees:** two of six, Linus #1 and 孫子 #1, and both ran a probe. No expert argues against it.
- **The case that shows the need:**
  - 孫子 *quoted*: "I ran the tool on a throwaway git fixture with `--out project-memory/INDEX.md`; the index's sha256
    changed and `git status --short` showed `M project-memory/INDEX.md`."
  - Linus *quoted*: "My in-memory probe intercepted an attempted overwrite and returned exit 0".
  - I read `command.ts:117-118`: `writeFileSync(path.resolve(options.out), ...)`. There is no check of where the path
    points. I did not run it.
  - The existing read-only test (`acceptance.test.ts:46`) writes to a separate `report.md`, so it cannot see this
    collision (Linus).
- **Why it is picked, with only two votes:** it is the tool's one irreversible action, and the only case in any
  answer that someone has measured. 孫子: *quoted* "A wrong verdict can be corrected; memory overwritten before it is
  committed cannot." It also needs nothing from the owner. The other two-vote proposals each wait on an owner's
  answer (see below).
- **How to check it is done:** a fixture with `project-memory/INDEX.md`, one entry and `AGENTS.md`. Run `--out` at
  each, then through a symlink to each and through a `..` path. Every run must give exit 2, the same bytes and an empty
  `git status --short`, and each must be shown red on the current HEAD first. `--out report.md` still writes the
  report and exits as before. Like E-1, the test is written by an engine other than the fixer.

## Not picked

| Proposal | From | Why not |
|---|---|---|
| Calibrate on a real multi-branch repo with `project-memory/` (U6, `VISION.md:10`) | 范蠡 #1; Dario #3 and Dave make it conditional | It waits on the owner to name a project. Dave and Dario each globbed `~/dev/*/project-memory/INDEX.md` and found nothing. 范蠡's fallback is a synthesized fixture, which Dario rejects: *quoted* "A fixture written to match the tool is not evidence." It stays open for EJ, as `runs/20261017-memory-check/report.md` already has it. |
| One judge per clause at the `memory_index.py` seam, a 9-row table (U2, C3, `VISION.md:26`) | 老子 #2; 范蠡 #2 is close | Two votes, but it cannot be built before the owner answers two things. One is the C3 vs Q2 conflict (老子: *quoted* "cannot be built before Q2 is answered"). The other is whether a `(warning)` from `memory_index.py` breaks SoT:W1.1a. Its case, `indextool.ts:126`, which drops warnings so a retired entry with the wrong kind passes W1.1a, is `r1-codex.md:17` and can be taken by the fix loop. |
| Full deletion of `project-memory/` still fails K4.1 (U2) | Dave #2 | One vote. The case is a raw finding (`r1-codex.md:9`) that the judge and the fix loop can take. Its fix changes C4 under the use-case-wins rule, and that change has to be flagged when it is made. |
| Carry file paths as data into warnings (U3, U2) | Linus #2 | One vote, and Linus's own probe shows the case: a bare Python file name disappears, and a path with spaces or Chinese characters is cut short. Dario: *quoted* "It is small and is the fix loop's to take." It is raw finding `r1-codex` #12 = `r1-agy` #5. |
| Take the self-asserted pass out of F2 and F3 (`VISION.md:23`, C2) | 老子 #3 | One vote, and it needs the owner's word on whether a test's name counts as F3's evidence (老子's own question 1). |
| Agent-memory location: stop listing regular files, maybe add `~/.claude/projects/*/memory/` (U1, F1) | 范蠡 #3 | One vote. The regular-file part is raw finding `r1-codex.md:27`, which the fix loop can take. Which location F1 names is the owner's call (Dario agrees). |
| Drop the static "session-start hook is not installed" line (`report.ts:101`) | 孫子 #3 | It names no use case or vision line, so the step's filter drops it. The case is real: `report.ts:101` still prints the line, while `runs/20261017-memory-check/settings-diff.md:38` and commit `7f1f67a` record the hook as applied. It is small enough for the fix loop or the owner to take. |
| Workflow changes: enhance only after `verify-r*` exits 0 (范蠡); rerun an empty judge once, then stop (Dave); reproduce before judging (老子) | 范蠡, Dave, 老子 | These change the workflow, not memory-check, so they are outside this step. Three different changes, none shared. All three come from the same failure: Enhance ran with no `findings.md` because `review-enhance.js:182` (`if (!usable(j)) break`) records no problem. That is for the owner. |

## What this file does not establish

The step's filter (a use case or vision line, plus a case) and the vote counts are my reading of the six answers and
`compare.md`. `compare.md` and its `check.txt` script were written by Claude; they confirm each answer's shape and
that its citations resolve, not that any code claim is true. No pick here has been shown red on HEAD yet. That is
the first step of each pick's check.
