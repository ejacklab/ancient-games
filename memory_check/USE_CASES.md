# memory-check — use cases

Each use case has its purpose, what fails it, and its minimum acceptance. U1–U3 are the owner's request; U4–U6 are
*proposed* until the owner accepts them. A use case wins over a requirement that conflicts with it.

## U1 — See what memory a project has
- **Purpose:** the owner learns which memory exists: `AGENTS.md`, `project-memory/` (`INDEX.md`, `entries/`, `work/`,
  `journal/`), its caches under `project-memory/.cache/`, and the agent memory the guidelines place outside the repo.
- **Fails if:** a memory location the guidelines name exists and the report does not list it, or the report lists one
  that does not exist.
- **Minimum acceptance:** run on this repo and on a fixture project with every location present, the report lists each
  location and says present or absent, matching the files.

## U2 — Know what breaks the guidelines
- **Purpose:** each requirement a tool can check is checked, with its id, its level and the evidence.
- **Fails if:** a requirement whose check is `tool` or `git` is not checked, a result has no evidence (a file and line,
  or a command and its output), or a MUST that fails is shown as passing.
- **Minimum acceptance:** a fixture project with one planted break per checkable requirement gets exactly the
  requirements whose fails_if that break meets reported as failing (two ids that share one fails_if, such as K6.1a
  and K6.2, fail together), with the planted file named.

## U3 — Be warned at the start of a session
- **Purpose:** an agent starting work is told, in a few lines, what is missing or failing, without reading the report.
- **Fails if:** a failing MUST or a missing `AGENTS.md` is not in the warning, or the warning holds anything else.
- **Minimum acceptance:** the session-start hook prints one line per failing MUST and for a missing `AGENTS.md`, and
  nothing when there are none.

## U4 — Name what needs a reviewer (*proposed*)
- **Purpose:** the requirements a tool cannot judge are listed for a person, so the report does not look complete when
  it is not.
- **Fails if:** a requirement whose check is `reviewer` is reported as passing or failing by the tool.
- **Minimum acceptance:** the report has a section listing every reviewer-only requirement by id.

## U5 — Never change memory (*proposed*)
- **Purpose:** running the tool is always safe.
- **Fails if:** after a run, `git status --short` shows any change other than the report file.
- **Minimum acceptance:** a test runs the tool on a fixture and compares `git status` before and after.

## U6 — Work on any project (*proposed*)
- **Purpose:** the tool checks the project it is pointed at, not only this repo.
- **Fails if:** a project path given on the command line is ignored, or a missing path is reported as an empty memory.
- **Minimum acceptance:** run with `--project <path>` on a fixture outside this repo gives that fixture's report; a
  path that does not exist is an error, not an empty report.
