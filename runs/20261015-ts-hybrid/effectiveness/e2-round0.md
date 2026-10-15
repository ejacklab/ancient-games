# E2 round 0 — past commands through M1 as first built (commit after m1-code-1)

Corpus: this project's Claude Code transcripts, 65 sessions, 3,677 Bash commands (raw commands kept in local scratch
`/tmp/hg-corpus/`, not here). Labels by the main agent, by reading each flagged command (*my reading*, one labeller).

| Measure | Count |
|---|---|
| Engine-like by the crude pattern | 284 |
| Recognised by `recognizeEngineCall` | 273 |
| Crude hit, not recognised | 12 — 2 real `dispatch.py run` calls (not in `engines.yaml`: the dispatcher checks its own results), 10 not calls (Python heredocs editing files, `echo`, `cat` of logs that mention a CLI) |
| Recognised with an output file found | 197 |
| Lint denies | 37 |
| — `trap:codex-stdin` | 20: **6 real** (codex exec with no stdin redirect, 2 of them backgrounded), **14 false** (`codex exec --help`, `pgrep -f "codex exec"`, `grep` patterns, `echo` text) |
| — `trap:opencode-outside-repo` | 17: **0 real**, **17 false** (heredoc text and `grep` patterns that mention `opencode run`; absolute paths belonging to other commands on the same line, e.g. `runlog.py --runs-root /…`) |

**Against the prediction:** false denies > 0 — held, and far larger than "a few": 31 of 37 denies were false.
Hold-out (N5): 6 earlier real occurrences of the codex-stdin trap caught — held (≥ 1).

**Cause (my reading):** the lint matches the whole Bash string. It does not split a line into simple commands, does
not drop heredoc bodies, does not know that `--help` starts no session, and takes path tokens from every command on the
line. Fix proposed as M1 round 2 (shell-aware segments), before M5 builds on the lint.
