# implement.result — memory-check v1

status: done

memory-check v1 is built in `memory_check/src/`: it checks every record of `SOURCE_OF_TRUTH_REQUIREMENTS.yaml` and
every Core requirement of `CACHES.md` against a project given on the command line, prints or writes a Markdown
report whose first line names its snapshot, prints a short warning with `--warn`, and exits 0/1/2.

## Files written

- `memory_check/package.json`, `memory_check/tsconfig.json` — bun, `bun test`, `tsgo --noEmit` (copied from `code_map/`)
- `memory_check/guidelines/SOURCE_OF_TRUTH_REQUIREMENTS.yaml`, `memory_check/guidelines/CACHES.md` — the tool's own
  verbatim copy of the two kit files (C1); the report prints their content hashes as the version
- `memory_check/src/guidelines.ts` — loads the 64 SoT records (`Bun.YAML.parse`) and the 11 CACHES Core requirements
  (the `**B1 — …**` headings and their *Fails if* lines)
- `memory_check/src/git.ts` — every git call, `GIT_OPTIONAL_LOCKS=0` (F3)
- `memory_check/src/locations.ts` — F1's locations (project root + `<home>/.claude/agent-memory/<name>/`)
- `memory_check/src/entry.ts` — the entry header/body fields the tool's own clauses compare
- `memory_check/src/indextool.ts` — runs `tools/memory_index.py --check` in the checked project and maps each of its
  messages to a requirement id (C3: no clause judged a second way)
- `memory_check/src/gitchecks.ts` — C5's snapshot (staged files; history since the first commit touching
  `project-memory/`, `--since` overrides, shallow clone) and the staged entries
- `memory_check/src/gitrequirements.ts` — the clauses the tool judges itself: W1.1a's prefix clause memory_index.py
  never sees, one entry per file (W6.1a), never deleted / `superseded_by` / retired reason (K4.1), claim, `source`,
  `depends_on`, `covers` (K4.3), and the git half of W1.1a and W1.1b (renames)
- `memory_check/src/cachechecks.ts` — C6 v1: B2.2 (`git check-ignore`) and Rd1.1 (the session-start scan)
- `memory_check/src/checks.ts` — every requirement's result: the five states, each with its evidence; the exit code
- `memory_check/src/report.ts`, `memory_check/src/warn.ts`, `memory_check/src/cli.ts` — R1, R2, R3
- `runs/20261017-memory-check/nodes/smoke-report.md`, `runs/20261017-memory-check/nodes/implement.progress.md`

Not written: tests. `bun test` reports "0 test files" — another engine writes them, per the brief and T1.

## Commands

```
cd memory_check && bun install && ./node_modules/.bin/tsgo --noEmit -p .
(no output)
tsgo exit 0
```

```
cd memory_check && bun src/cli.ts --project .. --out ../runs/20261017-memory-check/nodes/smoke-report.md; echo "exit $?"
/home/smoke01/dev/ancient-games/runs/20261017-memory-check/nodes/smoke-report.md
exit 0
```

The smoke report on this repo: 0 fail, 4 pass, 3 needs a reviewer, 70 not applicable, 0 could not run. The one fail is
`CACHES:B2` (clause B2.2): `git check-ignore -v project-memory/.cache` reports nothing in this repository.

Beyond the smoke run, six throwaway fixture projects under `/tmp/opencode/` were run by hand (evidence for this
result, not part of the deliverable): a clean project; one break per tool-checked clause (W1.1a prefix, W1.1b id form,
W1.2a, W1.3a, W4.1b, K4.1 deletion, K4.3 claim rewrite, W6.1a two entries in a file, K6.1a/K6.2 index mismatch,
CACHES:Rd1 a start hook that opens the cache); renames of prefix and of id; a project with no `AGENTS.md`; a shallow
clone. Read-only was checked with `git status --porcelain --ignored` plus md5sums of every file before and after a
run: no change.

## Requirements I could not meet, and why

- **T1 (known answers) — not implemented here.** The brief puts the tests with another engine; `memory_check/test/`
  and its fixtures are left for it.
- **C6 / R3, cache requirements and the exit code.** `CACHES.md` gives its Core requirements no level, so a failing
  one (here `CACHES:B2`) cannot gate the exit code under R3 ("exits 0 when no **MUST** fails or could not run"). The
  report prints the fail and states in its last section that no CACHES requirement gates the exit code. If the owner
  wants a failing B2.2 to exit 1, that is a change to R3 or to CACHES.md, not to this tool.
- **R2's session-start hook is not installed.** R2 leaves installing it to the owner (a harness config change,
  R12.3); `--warn` prints the warning, the report says the hook is not installed.
- **`CACHES:Rd1` can find a break but cannot certify absence** of a hook outside the repository. Its pass evidence
  names every file it scanned and says so in the evidence line, rather than claiming more.
- **Uncalibrated.** No real project has been named to calibrate against (design-decisions.md 15); only fixtures were
  run, and the report says so.

## CONTRADICTS

- **`USE_CASES.md` U2, minimum acceptance:** *"a fixture project with one planted break per checkable requirement
  gets exactly that requirement reported as failing, with the planted file named."* K6.1a and K6.2 cannot be separated:
  one comparison in `tools/memory_index.py --check` is the evidence for both, and C3 forbids checking either clause a
  second way, so a planted index mismatch fails both ids. `research-q/compare.md` § 7 records the same tension and
  names this pair (老子, point 12). Not fixed: both ids fail together, with the one command and its output as evidence.
- **`REQUIREMENTS.md` R2, "Fails if: a failing MUST is not in the warning":** read with R2's own clause that the hook
  "runs only the location, index and index-size checks", the hook's reduced run cannot see a history MUST (K4.1,
  K4.3) that the full report reports as failing, so such a MUST would be missing from the warning. `--warn` therefore
  prints every failing MUST from the full run, and the hook — the owner's to install — is not wired to a reduced run.