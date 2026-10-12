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
5. **A blank id**: `id: " "` gives the id `" "`, which is non-empty and renders `- [ ](…)` (n4 O5). Also, a
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
