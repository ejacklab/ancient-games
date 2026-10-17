# Question — two choices that wait for the owner; give your advice and pick

The owner decides both; your answer is advice. For each, give your pick, the reason, and what would change it.

## Q1. A question that trials cannot answer goes to the owner at once?
Today the method lets a design try a piece up to three times before an unclear spot goes to the owner. Three experts
proposed (run 20261017-memory-check, research-q, item 16): "a question that trials cannot answer goes to EJ at once,
not after three failed trials." Examples of such questions: which location a requirement names, whether a real
project exists, a threshold only the owner can set. Since 2026-10-17, in a time-boxed run the experts advise and the
main agent decides provisionally (method 3.8 item 14), and the owner accepts or declines at the end.
Options: (a) adopt — a question no trial can answer is sent to the owner at once (in a time-boxed run: decided
provisionally at once and listed for the owner); (b) keep the three-trial rule.

## Q2. Is Claude Code's own memory "agent memory" for memory-check?
memory-check (`memory_check/REQUIREMENTS.md` F1) looks for agent memory at `<home>/.claude/agent-memory/<name>/`, the
place the source-of-truth design names. Claude Code itself keeps its memory at
`~/.claude/projects/<project path with / as ->/memory/` (one `MEMORY.md` index plus one file per fact, with
frontmatter). That folder exists for this repository and holds about 50 files. memory-check does not list it.
Options: (a) F1 also lists it, reported present or absent only (not checked against the guidelines' entry format,
which it does not follow); (b) F1 also lists it and checks it as agent memory; (c) leave F1 as it is: it is the
harness's memory, not the project's.
