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

## F-785afc27 — a command of mine ended with exit 1, and the record cannot say which

Whys:
1. Why was it logged? At 16:01:46 UTC a Bash call of this session ended in PostToolUseFailure with exit 1; the guard labelled it "rm call" (evidence: command word rm, 3,741 bytes of stderr, the size of a bun test report).
2. Why can I not name the call? None of my commands at that minute starts with `rm`; the record keeps only one command word, the exit code and lengths — no tool-use id, no segment — so it cannot be matched back to the call.
3. Why does the record keep so little? Round 4 (D2) chose "the command word" to keep command text out of the journal, and nothing else that identifies the call was added.
4. Why is that a problem now? R12.3 asks for six whys down to a changeable source; with no way to find the call, the whys stop at the record itself.
Source: tool (the guard's D2 record)
Root cause: a command-error record holds too little to find the call it describes, and its command word may not be the failing segment's.
Options:
1. [tool] Add the hook payload's `tool_use_id` to every guard-written record, so a failure can be matched to its call in the transcript without storing any command text. evidence: the PostToolUseFailure payload carries `tool_use_id` (runs/20261015-ts-hybrid/research/hook-points.md, line 99).
2. [check] Label a command error by the segment that failed when the exit can be tied to one (the last segment of a plain chain), and say "compound command" otherwise. evidence: this record's "rm call" for a call that, by its stderr size, was a bun test run.
