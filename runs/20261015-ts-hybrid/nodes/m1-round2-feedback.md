This is a **repair round** caused by a measurement, not by your tests being wrong. The COO replayed 3,677 past Bash
commands from this project through M1 as first built: 37 denies, **31 false**. The lint read the whole Bash string, so
it fired on `codex exec --help`, on `pgrep -f "codex exec"`, on `grep` patterns and `echo` text naming an engine, on
heredoc bodies that mention `opencode run`, and on absolute paths belonging to another command on the same line
(e.g. `python3 …/runlog.py --runs-root /abs/runs exec … -- opencode run "…"`). Six denies were real: `codex exec`
with no stdin redirect, two inside a backgrounded `( … ) &` group.

SPEC.md's M1 section now has a **Segments** part (read it in full) and new Fails-if lines; `data/*.yaml` regexes are
now anchored to the command word (`^(?:\S*/)?codex…`). Also still missing from the first tests: a **proposed result
trap** must produce no finding in `checkResult` (SPEC: "each approved **result** trap").

For the test writer: keep every existing test that still matches SPEC.md; change only tests the new SPEC contradicts
(say which, and why, in the result); add tests for every new Fails-if line and for `segments()` (heredoc removal,
quotes, `2>&1` not a separator, background of a `( … ) &` group, wrapper stripping incl. `runlog.py … --`, `--help`).
Use planted command strings shaped like the false denies above — never real paths from this machine.
