# Question — how should the guard know which deadline a session started?

The guard keeps a time limit per run as a file in `.harness-guard/deadlines/` (`{id, start, minutes, run, session}`).
`deadline start` writes it with `session: null`; the PostToolUse hook of the Bash call that ran `deadline start`
then claims every file with `session: null` for its own session. Only a call whose text matches
`/\/src\/cli\.ts\s+deadline\s+start\b/` claims.

What happened (`runs/20261018-guard-deadline-claim/facts.md`): session B started its deadline with
`G=…/src/cli.ts; bun $G deadline start …`, which the pattern misses, so the file stayed unclaimed. Session A started
its own 27 s later and claimed both. After A's own deadline ended, A and every agent of its workflows were told
"time is up" by B's deadline.

Read the research first: `runs/20261018-guard-deadline-claim/research/starts.md` (every start on this machine, and
how often it was claimed by its own session, another or none) and `runs/20261018-guard-deadline-claim/research/harness.md`
(what a hook payload carries, whether Bash sees the session id, what session a subagent's hooks report).

Options:
- (a) **Claim by the id the call printed.** The PostToolUse hook reads the start call's output for
  `D-xxxxxxxx: N min` and claims that one id only, whatever the command's text.
- (b) **The session is written at start.** The CLI writes `session` itself, from an id the harness gives the command
  (only if the research finds one).
- (c) **Claim only a deadline started during the call.** Its `start` lies between the call's start and end.

Questions:
1. Which option, or what else? Why, and what would change your pick?
2. What should happen to deadline files already claimed by the wrong session?
3. What one test would show the fix holds when two sessions start deadlines seconds apart?
