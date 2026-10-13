# Summary — readers on item 8, runbooks

COO (Claude `claude-opus-5-5`), 2026-10-13. Three reports: `reviews/claude.md`, `reviews/codex.md`,
`reviews/opencode.md`. **agy produced nothing**: its headless mode auto-denied the `read_file` permission
(`reviews/agy.stderr.txt`). In stage 3 of the INDEX.md run it read local files without this error.

## All three recommend the same thing

**Drop the runbook kind.** A procedure lives in the repo as a script, or as a page in `docs/` where it can't be a
script. An entry links to it and never repeats its steps. What was learned while running it is a lesson. **The vision
doesn't change**: it never had runbooks, so dropping them brings the design into line with it.

**Scope:** project. A one-off step inside one task stays in that task's `state.md`.

**Their reasons (quoted):**
1. The vision lists only *"decisions and facts … lessons, observations and hypotheses"*. W2 cites the vision as its
   source, yet adds a kind the vision never had. Dropping it makes the citation true.
2. `procedure-to-skill`: *"The procedure is the memory. A prose description of a procedure is a summary of the memory,
   and summaries drift."* A runbook entry is either a pointer to a script, or prose steps that drift.
3. W3.1 already forbids repeating the code, and W3.6 already says to link to documents rather than copy them. A
   procedure is one more thing to link to. No new rule is needed.

**The edits** (six places): the "What it is for" bullet, the When-to-write row, the layout's `R-`, W1.1, W2.2 and W5.2.
W2's existing check then fails `kind: runbook` on its own. Two more places, found by opencode: `docs/index-md/`
REQUIREMENTS B2.4 and DESIGN step 5 say "the six kinds", which becomes five.

## Risks they named

- **The skill's default home is the home folder** (`~/skills/<name>/`), where a fresh clone can't find it (claude).
  Mitigation: the design says a project's procedure lives in the repo.
- **A procedure with judgement in it,** which can't be a script and is run once, could be lost with its task (opencode).
  Mitigation: a page in `docs/`, linked from an entry.
- **A manual step dropped when the commands become a script,** such as "pick the right backup" (codex). Mitigation:
  manual steps stay with the procedure, and the skill's verify script checks the real result.

## Open, small

1. A procedure that can't be a script: a page in `docs/` (claude and opencode's default) or somewhere else?
2. Should `AGENTS.md` name the project's scripts, one line each (claude's default)? This repo's `CLAUDE.md` already
   does it for tests.
3. Should the vision get one guard line, *"It never holds a procedure"* (opencode, optional)? Without it the change is
   design-only.
