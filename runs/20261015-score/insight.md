# Insight — run 20261015-score (the main agent's session)

## F-1e90a8e1 — a pipe hid a failed merge

Whys:
1. Why did the chain continue? `git merge … 2>&1 | tail -1 && …` — the pipeline's exit is tail's (0), so `&&` went on.
2. Why did the merge fail? An untracked copy of `runs/20261015-score/mutants.txt` in the main checkout would have been overwritten.
3. Why was there an untracked copy? The main agent writes run evidence in the main checkout and copies it into the worktree to commit, leaving the original behind.
4. Why was the pipe there? Habit: trimming long git output with `| tail` — the same "exit 0 is not success" trap the guard exists to catch, in the main agent's own commands.
Source: instruction (the main agent's command habit; no rule forbids piping a command whose exit matters)
Root cause: a command whose success gates the next step was piped, so its failure was invisible to `&&`.
Options:
1. [rule] Never pipe a command whose exit gates the next step; print its exit (`; echo "exit $?"`) or use `set -o pipefail`. evidence: this record; runs/20261015-score/merge-hidden.txt.
2. [check] A guard trap: `git merge|git push|git commit … | tail|head` followed by `&&` — the pipe hides the exit. evidence: the same shape here; E2's corpus can count how often it occurs.
3. [tool] Keep run evidence only in the worktree during a build and copy it to the main checkout after the merge, so no untracked twin can block it. evidence: the identical mutants.txt (cmp) that blocked the merge.
