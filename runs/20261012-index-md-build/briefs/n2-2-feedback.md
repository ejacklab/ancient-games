## Feedback from attempt 1 (the COO's verdict: failed attempt; your code is restored in the worktree)

Your gate run was green, but two of your "Choices not in the spec" break the spec. The acceptance file has been
repaired and re-frozen, so it now checks both.

1. **Choice 1 is reversed.** An untracked entry file is an error in write mode **whatever its status**. B1.2: *"An
   untracked entry file is an error that names the file and tells the writer to `git add` it."* The test that made you
   downgrade it to a warning for inactive entries had a defect (its write-mode case never staged the entry). That is
   fixed, and a new test checks an untracked retired entry exits 1.
2. **Choice 9 is reversed.** `--check <rev>` with a rev that names no commit must exit 1 with a message that names the
   rev. C1.2: *"It passes (exit 0) only when the entries are valid, the bytes are equal, and the size is within the
   limits. Otherwise it exits 1."* The only pass-through cases are C1.3's: no `project-memory/` in the snapshot, or an
   **unborn** `HEAD` (a repo with no commits yet). Tell these apart, for example: `HEAD` that fails `git rev-parse
   --verify -q` while `git symbolic-ref -q HEAD` succeeds is unborn.
3. **Citation.** Cite the CACHES.md agy row by name (*"CACHES.md, limits table, agy row"*), not by a line number. The
   line differs between the committed and the working copy.

Keep everything else as it was. Choice 5 (a tracked entry deleted in the working tree keeps its line) is outside the
criteria and is recorded for EJ. Do not change it in this attempt.
