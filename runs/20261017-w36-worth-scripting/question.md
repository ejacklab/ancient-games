# May a procedure a script could do stay a page because it runs rarely — and who decides?

## The question

Requirement W3.6 of the source-of-truth memory design now says when a procedure **cannot** be a script. It does not
say whether a procedure that **could** be a script may stay a `docs/` page because it is run rarely, or is not worth
building and keeping a script for. Answer, through your own rules:

1. May it stay a page? If yes, on what test — stated as a comparison an agent can make (for example, the cost of
   building and keeping the script against what it saves), **not as a number nobody has measured**.
2. Who decides: the agent writing the procedure, the project owner, or someone else — and at what moment?
3. What should W3.6 say, in one or two sentences added to its text below?

## Facts (each labelled with how it was checked)

- **W3.6 as it stands** (*read*: `docs/memory-system/SOURCE_OF_TRUTH_REQUIREMENTS.yaml`, record W3.6; level SHOULD;
  `check: reviewer`): *"No copy of the project's existing documents (requirements, architecture in `docs/`) or of its
  procedures: an entry links to them. A procedure lives in the repo as a script with an external check. A script that
  stops and waits for a person (an approval, a typed confirmation) is still a script. Where a step cannot be a command
  with a checkable result — an action a script cannot do or wait for, or a choice that depends on judging what was
  seen — it is a page in `docs/` that names that step and calls scripts for the rest. The agent writing the procedure
  decides by trying the script first; the project owner decides if it is contested. `AGENTS.md` names each script, one
  line each. A script is project work, not memory."* `fails_if` (same record): *"an entry copies a document or a
  procedure's steps, or a procedure page names no step a script cannot do, with no written reason."*
- **Levels** (*read*: the same YAML, key `levels`): SHOULD is a default; it may be skipped with a reason written in
  the task's `state.md`, and fails only when skipped without one.
- **Linus, 2026-10-16** (*read*: `runs/20261016-w36-procedure-script/experts/answers/linus.md:19`): *"A procedure can
  be scriptable yet not worth scripting: for example, a disposable task whose automation would require more
  construction and maintenance than its intended use warrants. That is a cost judgment, not technical impossibility."*
- **孫子, 2026-10-16** (*read*: `runs/20261016-w36-procedure-script/experts/answers/sun-tzu.md`, its Answer
  section): his test includes *"it will run again on ground that stays still"*, and the "should not" half is a value
  the project owner decides.
- **A skill used in this repo, `procedure-to-skill`** (*read*: the copy at
  `runs/20261017-w36-worth-scripting/sources/procedure-to-skill-SKILL.md:15`): *"The procedure is the memory. A prose
  description of a procedure is a summary of the memory, and summaries drift."* Its description (line 3) says it is
  *"NOT for a fact with no steps … or a procedure specific to one throwaway task."*
- **The owner's rule on thresholds** (*recall*: house memory "design guide: comparisons, not numbers"): a trigger is
  "measure X against Y"; never ask for, or invent, a threshold number up front.
- **The owner's decision of 2026-10-16** (*read*: `docs/memory-system/SOURCE_OF_TRUTH_RELEASE_NOTES.md`, entry
  2026-10-16): a script that waits for a person is still a script.
- The research for this question is added below by the workflow before you are asked.
