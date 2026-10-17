status: done

## Findings

These findings are my reading of the code. I wrote the in-memory probes; they confirm individual code paths, not independent end-to-end behaviour.

1. **[P1] Unrecognised checker failures become passes — [indextool.ts:139](/home/smoke01/dev/ancient-games/memory_check/src/indextool.ts:139).** An entry containing invalid UTF-8 makes `memory_index.py` exit 1, but its diagnostic maps to no requirement. A Python startup error with stderr is also treated as a completed check. Both probes produced passing MUSTs and exit 0. **Fix:** propagate execution errors and unmapped failures as “could not run” for affected checks.

2. **[P1] Checks skipped by early returns receive passes — [checks.ts:225](/home/smoke01/dev/ancient-games/memory_check/src/checks.ts:225).** After entry validation fails, Python never compares or measures the index, yet K6.1a, K6.2 and Rd3.1a pass. An oversized, mismatching index also gets Rd3.1a pass: the `mismatch` recogniser expects `INDEX.md`, while Python prints `project-memory/INDEX.md`. **Fix:** track which checks completed, correct the recogniser, and report skipped checks as “could not run.”

3. **[P1] Working-tree presence overrides the declared staged snapshot — [checks.ts:90](/home/smoke01/dev/ancient-games/memory_check/src/checks.ts:90).** Stage broken memory, then remove its working-tree directory without staging that removal: every project-memory requirement becomes “not applicable,” discarding the staged checker’s failures. Cache and instruction checks also read working-tree state. **Fix:** use staged presence and bytes for staged verdicts; explicitly label any filesystem-only observations.

4. **[P1] Staged deletions and renames escape history checks — [gitchecks.ts:128](/home/smoke01/dev/ancient-games/memory_check/src/gitchecks.ts:128).** The checks inspect committed `git log` output only. Stage an entry deletion and a matching empty index: K4.1 passes. Stage a prefix/id rename with matching content and index: the rename clauses pass. **Fix:** inspect the staged diff alongside committed history.

5. **[P1] K4.3 checks endpoints instead of every change — [gitrequirements.ts:143](/home/smoke01/dev/ancient-games/memory_check/src/gitrequirements.ts:143).** Commit a changed claim, then restore its original text: K4.3 passes despite the forbidden historical rewrite. Likewise, an earlier unrelated `changed:` addition can excuse a later unlogged `covers` edit because only total counts are compared. **Fix:** check each transition and its accompanying log addition.

6. **[P1] `--since` silently excludes existing entries from K4.3 — [gitchecks.ts:182](/home/smoke01/dev/ancient-games/memory_check/src/gitchecks.ts:182).** Create an entry before the selected range, then change its claim inside that range. The creation search finds nothing, so K4.3 reports pass after comparing zero entries. **Fix:** obtain the baseline before the range and inspect changes within it.

7. **[P1] A merge can discard an entire entry undetected — [gitrequirements.ts:218](/home/smoke01/dev/ancient-games/memory_check/src/gitrequirements.ts:218).** Add an entry on one branch, then merge using an `ours` result that omits it. The merge check excludes missing paths, delegating them to K4.1; the ordinary log scan does not request merge-parent deletion diffs. **Fix:** compare missing paths against every merge parent and report deleted entries.

8. **[P1] K4.1 passes a mixed git/reviewer requirement — [checks.ts:240](/home/smoke01/dev/ancient-games/memory_check/src/checks.ts:240).** With no mechanical break, K4.1 returns pass, contrary to C2. A retired entry retaining only its original “created” log item also passes as having a retirement reason. **Fix:** retain mechanical failures, but otherwise return “needs a reviewer.”

9. **[P2] Quoted statuses bypass K4.1 — [gitrequirements.ts:122](/home/smoke01/dev/ancient-games/memory_check/src/gitrequirements.ts:122).** `status: "superseded"` without a replacement link passes; the unquoted equivalent fails. Python accepts and unquotes that value. **Fix:** normalise header scalar values consistently before comparing them.

10. **[P1] Rd1’s keyword scan produces unsupported verdicts — [cachechecks.ts:74](/home/smoke01/dev/ancient-games/memory_check/src/cachechecks.ts:74).** “On demand, open project-memory/.cache/index.sqlite” fails despite permitting an allowed read. “At session start, do not read entries; open project-memory/.cache/index.sqlite” passes because any negation exempts the whole line. A startup instruction invoking a cache-reading script also passes. **Fix:** limit decisive verdicts to established startup behaviour and send unresolved instructions or indirect calls to a reviewer.

11. **[P1] Warnings expose entry text — [warn.ts:26](/home/smoke01/dev/ancient-games/memory_check/src/warn.ts:26).** A K4.3 claim-change warning includes both the original and replacement claims. Truncating the evidence does not satisfy R2’s “never entry text.” **Fix:** render warnings from ids, diagnostic categories and filenames, without reusing evidence prose.

12. **[P1] Git failures become empty successful results — [git.ts:28](/home/smoke01/dev/ancient-games/memory_check/src/git.ts:28).** Injecting Git exit 128 produced “zero renames,” “deleted none” and a clean K4.3 outcome. The command’s actual failure disappears. **Fix:** preserve Git errors and propagate “could not run” rather than substituting empty output.

13. **[P2] A configured Bun cache permits writes outside `--out` — [cli.ts:16](/home/smoke01/dev/ancient-games/memory_check/src/cli.ts:16).** Cache suppression runs only when `BUN_RUNTIME_TRANSPILER_CACHE_PATH` is unset. With it set to a writable cache directory, imported modules can create transpiler-cache files, violating F3. **Fix:** relaunch with caching disabled whenever its effective value is not already disabled.

14. **[P2] Markdown examples count as additional entries — [entry.ts:39](/home/smoke01/dev/ancient-games/memory_check/src/entry.ts:39).** A single valid entry containing a fenced YAML example with two `---` lines fails W6.1a as having another header block. **Fix:** distinguish document content from entry headers; ambiguous content needs review.

Checked and found nothing:

- **F2:** project selection and git-root usage validation.
- **C1/R1 coverage:** bundled guideline copies, version hashes, ids and levels.
- **C4/C6:** absent-cache handling, including B2.2. The current specification contains no contradiction here.
- **R3 calculation:** the final verdict-to-exit-code mapping itself; incorrect input verdicts are covered above.
- **R2 filtering:** warning selection includes failing MUSTs and missing `AGENTS.md`; the content defect is finding 11.

Type checking passed. No files were changed. The acceptance suite was not run because it creates fixture files, conflicting with this review’s read-only instruction.