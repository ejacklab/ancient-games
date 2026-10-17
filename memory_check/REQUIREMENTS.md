# memory-check — requirements

Grouped by what the tool does: it **finds** the memory, **checks** it against the guidelines, and **reports**. The
three groups are *proposed*. Levels follow RFC 2119: MUST is a gate, SHOULD a default that may be skipped with a written
reason. Each requirement names who decides any choice it leaves open, and the case that fails it.

## Find

**F1 (MUST) The locations.** The tool looks for every memory location the guidelines name: under the project root
`AGENTS.md`, `CLAUDE.md`, `project-memory/INDEX.md`, `project-memory/entries/`, `project-memory/work/`,
`project-memory/journal/`, `project-memory/.cache/`; and the agent memory the design places in the home folder
(`<home>/.claude/agent-memory/<name>/`, where `<home>` is `--home`, else the user's home). `AGENTS.md` is required;
the rest are reported present or absent. Who decides: the guidelines. Fails if: a named location exists and is not
found, one is reported that does not exist, or a missing `AGENTS.md` is not a failure.

**F2 (MUST) The project.** The project is `--project <path>`, else the current folder, and must be the root of a git
repository; the root is printed. Who decides: the user. Fails if: a given path is ignored, or a path that is not a git
root is checked instead of being a usage error.

**F3 (MUST) Read only.** The tool reads files and git (with `GIT_OPTIONAL_LOCKS=0`), and writes nothing but its own
report. Who decides: none. Fails if: a run changes, creates or deletes any file, ignored files included, other than the
report.

## Check

**C1 (MUST) From the requirements.** The checks are the guidelines' own requirements, by id, prefixed by guideline:
every record of `SOURCE_OF_TRUTH_REQUIREMENTS.yaml` (`SoT:<id>`) and every requirement of `CACHES.md`'s Core
requirements (`CACHES:<id>`). A record whose `check` names `tool` or `git` is checked where the tool can decide it;
where it cannot (the change it needs is not visible to git, or a reason "written" elsewhere would excuse it), and for a
`reviewer` check, the result is "needs a reviewer". A record whose check is `none` (a definition, a permission: its
`fails_if` is "nothing") is "not applicable". Which copy of the guidelines: the tool's own, with its
version printed. Who decides: the guidelines' `check` field. Fails if: a decidable `tool` or `git` record is not
checked, or a record the tool cannot decide gets a pass or a fail.

**C2 (MUST) Results and evidence.** Each requirement's result is one of: pass, fail, needs a reviewer, not applicable
(its memory is absent), or could not run (with the reason). A record checked by the tool and by a reviewer fails when
the tool finds a break, else needs a reviewer. Every pass and fail carries its evidence: the file and line, or the
command and its output. Who decides: none. Fails if: a result has no evidence, or a record gets a state outside the
five.

**C3 (MUST) The existing tool.** The index and entry-format checks are `tools/memory_index.py --check`, run and parsed
(its output pinned by tests); the tool adds only the format clauses `memory_index.py` does not check, and never
changes `memory_index.py`. Who decides: none. Fails if: the tool reports a pass that `memory_index.py --check` fails,
or checks a clause `memory_index.py` already checks a second way.

**C4 (MUST) Absent memory.** With no `project-memory/`, its requirements are "not applicable", with the absent location
as the reason; with no `project-memory/.cache/`, every cache requirement is, B2.2 included. Who decides: the guidelines. Fails if: an absent optional
location makes a requirement fail.

**C5 (MUST) The snapshot and history.** The report names what it checked in its first line: the staged state (the
view `memory_index.py --check` reads) for files, and for history the commits since the first one that touches
`project-memory/` (`--since` overrides), the range printed. A shallow clone makes history checks "could not run". Who
decides: the user (`--since`). Fails if: the report does not name its snapshot or its range.

**C6 (MUST) Caches, first version.** Of `CACHES.md`'s requirements, B2.2 (the cache folder is ignored by git) and Rd1
(no start hook or instruction opens a cache file) are checked when the cache folder exists; the others are "needs a
reviewer" then. With no cache folder, C4 applies. Who decides: the owner, for adding more. Fails if: B2.2 or Rd1 is not checked, or another
cache requirement gets a pass or a fail.

## Report

**R1 (MUST) The report.** One Markdown report per run: the snapshot (C5), the locations (F1), a line giving how many
files under `project-memory/` are changed but not staged (and so not checked), then per requirement its id, level,
result and evidence, MUSTs first, a list of what needs a reviewer, and last a section `## Not applicable` holding
every "not applicable" result. Where it is written: `--out`, else
printed. Fails if: a requirement of C1 is missing from the report, or the report's results differ from the checks'.

**R2 (MUST) The warning.** A short warning: one line per MUST that fails or could not run, and a missing
`AGENTS.md`, with ids and file names, never entry text; nothing else; empty when there are none. It is printed by `--warn` and given at the start of
a session by a hook running `--warn`, which never opens a cache file. (U3 wins over a narrower hook: one line per
failing MUST needs every check to run.) Who decides:
the owner, for installing the hook (a harness config change, R12.3). Fails if: a failing MUST is not in the warning,
the warning holds anything else, or the hook opens a cache file.

**R3 (MUST) Exit code.** The command exits 0 when no MUST fails or could not run, 1 when one does, 2 on a usage error.
Who decides: none. Fails if: a failing MUST exits 0.

## Tests

**T1 (MUST) Known answers.** Fixtures and their expected results are written before the check runs, by hand (an
expected `INDEX.md` as literal bytes) or by an engine that did not write the check, never computed by the check. Who
decides: none. Fails if: an expected answer is produced by the code under test.
