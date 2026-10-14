# INDEX.md generator — backlog

> Findings from building and testing the generator that fall **outside** the accepted criteria, so they did not
> become work in the run that found them (method 3.6). Each line names the date, the run, and where it came from. EJ
> decides what, if anything, becomes a requirement. Location agreed by EJ on 2026-10-12 (Q3 of run
> `20261012-index-md-build`).

## From run 20261012-index-md-build (2026-10-13)

Sources:
- `n4` is the blind review, `runs/20261012-index-md-build/nodes/n4-1.result.md`.
- `n2` is the coder's "Choices not in the spec", `nodes/n2-2.result.md`.

### Needs a ruling from EJ (the spec says two things)

1. **"Every run prints the size" vs. an early exit** (n4 F4; n2 choice 3).
   - B4.2 and DESIGN step 7 say the size line is printed on every run.
   - DESIGN step 5 exits on any error before step 7 measures anything. The script follows step 5, so there is no size
     line when entries are invalid, and none on "nothing to index", "nothing to check" or a bad rev.
   - Decide: does "every run" mean every run that renders an index?

### Silent passes (*not measured*; found by reading)

2. **SHA-256 repositories** (n4 O1). `is_object_id` accepts only 40-hex ids. In a SHA-256 repo every listing is
   dropped, and `--check` prints "nothing to check" and exits 0, so a wrong `INDEX.md` would pass.
3. **The real-repo test checks nothing yet** (n4 O4). `--check HEAD` on this repo passes as "nothing to check" until
   `project-memory/` exists. It starts guarding only when the first entry is committed.

### Hardening

4. **A rev that starts with `-`** is passed to git as an option (n4 O2). Guard it with `--end-of-options`.
5. **A blank id**: `id: " "` gives the id `" "`, which is non-empty and renders `- [ ](…)` (n4 O5). *Closed
   2026-10-14 by B2.3's id form (run `20261014-memory-index-cleanup`): a blank id is not in the form.* Also, a
   duplicate-id error names only the later file.
6. **The unit tests import the tool in-process**, which may write `tools/__pycache__/` in the real repo (n4 O3).

### Naming (house standard; outside the criteria)

7. `gather` sorts, flags duplicates and prints. `parse_entry` also validates. `is_utf8` tests whether a string can be
   encoded. One name, one job (n4 F6).

### Choices the coder made where the spec is silent (kept; listed so EJ can see them)

8. Write mode uses two `git ls-files` calls (`--cached`, then `--others`), not step 1's single call, so that untracked
   files can be told apart.
9. Problems go to stderr and status to stdout. Warnings end in `(warning)`.
10. An unborn `HEAD` passes `--check` in both modes. A revision without `--check` is a usage error (exit 2).
11. A file name that is not valid UTF-8 is reported as a problem.

## From run 20261014-memory-index-cleanup (2026-10-14)

Sources: `n4` is the blind review, `runs/20261014-memory-index-cleanup/nodes/n4-1.result.md`; `n3` is the mutant run.

1. **No acceptance test has a marker late in a long entry** (n4 F2). Every marker test puts it within the first ten
   lines, so a scan cut short would pass the acceptance file.
2. **No acceptance test shows that every marker line is reported** (n3 N14). The unit test does; the acceptance
   tests check only that the file is named.
3. **The acceptance tests do not show which problem caused the exit 1** (n4 F8): they assert `<file>: ` only, as the
   file's older tests do.
4. **Spaces inside quotes**: `id: ' 14-10-a1b2c3-2026 '` fails the form, because B2.1 strips spaces and then one pair
   of quotes, not the spaces inside them (n4 O1). The result is an error either way; EJ to say what B2.1 means.
5. **`check_content`'s docstring** says every entry needs an id and a known status, but those checks live in
   `parse_entry` (n4 O3; older text).
