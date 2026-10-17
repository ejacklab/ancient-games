# Insight — run 20261017-insight-placement

## Brief fact 1 — I told the experts the guard sees every Write and Edit before it runs; it does not

Found by: Linus (`place-q/linus/answers/linus.md`); confirmed by `src/install.ts:28` (`["PreToolUse", "Bash"]`),
`src/hooks.ts` (the PreToolUse handler returns for any tool but Bash) and `~/.claude/settings.json` (PreToolUse matcher
`Bash`).

Whys:
1. Why was the fact wrong? I wrote "sees the path of every Write, Edit and MultiEdit call before it runs (PreToolUse)";
   only PostToolUse covers file writes, after the call.
2. Why did I write it? I merged two facts from memory — the PostToolUse matcher `Bash|Write|Edit|MultiEdit`, set today,
   and the PreToolUse lint — into one, without opening `install.ts`.
3. Why not open it? The question was written under a 20-minute clock, and I marked the facts "verified 2026-10-17"
   as a block, though I had verified only some of them in this call.
Source: instruction — the brief template lets a facts block carry one "verified" label for all its lines.
Root cause: a fact recalled, not checked, and labelled verified with the checked ones.
Options:
1. [rule] Each fact in an expert question carries its own label and the command or file:line that checked it; a fact
   with neither is marked *recall*. evidence: the facts that had a file path in this question were right.
2. [tool] experts-decide's Check step also checks each fact the question labels verified against the file it names,
   and lists any with no source. evidence: Linus caught it by reading two files.

## Timer crash — `deadline wait` failed when the deadline was ended before it woke

Found by: the background timer's exit 1 and its one line, "harness-guard: an internal error was caught; the guard is
failing open". Cause by reading `src/cli.ts:224-232`, not reproduced.

Whys:
1. Why did the timer fail? After its sleep, `deadline wait` reads `deadlineStatus(...)!.line`; the result was null.
2. Why null? I ran `deadline end` when the experts finished early, and `sessionDeadline` skips ended deadlines.
3. Why does wait not handle that? It was written for a deadline that runs to its end; `end` came later (Round 10) and
   no test runs `end` while a `wait` sleeps.
Source: check — `deadline wait` assumes its deadline is still open when it wakes.
Root cause: the non-null assertion after the sleep; the deadline can be ended in between.
Options:
1. [tool] After the sleep, if the deadline was ended, print "<id> ended before its deadline" and exit 0; with a test
   that ends a deadline while wait sleeps. evidence: this run's sequence (end at 13:48, the timer woke at 13:58).
2. [rule] When a run ends early, stop its background timer before `deadline end`. evidence: the same sequence.
