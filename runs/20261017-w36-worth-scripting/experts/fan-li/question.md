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

## Research findings

Question: when does scripting an operational procedure pay off compared with a written step-by-step page; what do
practitioners and studies say about build-and-keep cost against how often it runs; what happens over time to
rarely-run scripts and to rarely-run written procedures?

Researched 2026-10-17 by the research step of experts-decide (Claude, web search and fetch). How to read the labels:
**verified** means the page was opened with a fetch tool and it says this (the fetch tool returns an extract, so
quotes are as that extract gave them). **reported** means a search result or a secondary source says it and the page
itself could not be opened or did not show it.

### A. Cost of building and keeping a script against how often the procedure runs

1. **verified** — Google SRE workbook, "Eliminating Toil" (https://sre.google/workbook/eliminating-toil/): "Before
   beginning toil reduction projects, it's important to analyze cost versus benefit". It adds that projects that look
   "unprofitable" from a simplistic comparison of hours saved versus hours invested may still be worth doing for
   indirect benefits (fewer human-error outages, morale, skills). It gives no break-even number.
2. **verified** — same workbook page: "Repair automation is not fire and forget"; "Automation can have a very long
   lifetime, so make sure to plan for project continuity as people leave and join the team." Keeping a script is an
   ongoing cost, not a one-time one.
3. **verified** — same workbook page recommends partial automation: "consider a partially automated approach as an
   interim step toward full automation", and says written remediation instructions "are essentially pseudocode to
   someone with software development skills!" It also notes the pull to do a migration by hand "because it's a
   one-time effort."
4. **verified** — Google SRE book, "Eliminating Toil" (https://sre.google/sre-book/eliminating-toil/): toil is
   "manual, repetitive, automatable, tactical, devoid of enduring value, and that scales linearly as a service grows";
   the hands-on time a human spends running a script "is still toil time"; the target is toil "below 50% of each SRE's
   time." Repetition is part of the definition: work that does not repeat is not toil by this definition.
5. **verified** — xkcd 1205 "Is It Worth the Time?" (https://xkcd.com/1205/): a table of how long one may spend making
   a routine task faster before it costs more than it saves, over five years, by how often the task runs (50/day to
   yearly) and the time shaved per run. The comparison is build time against (runs × time saved per run); it leaves
   out maintenance cost and error reduction.
6. **verified** — Rule of three (https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming)), attributed to
   Don Roberts and popularised in Fowler's *Refactoring* (1999): "when similar code is used three times, it should be
   extracted into a new procedure"; at two copies it is unclear whether it is worth it, and abstracting too early can
   pick the wrong abstraction. Note: it is about duplicated code, not operational procedures; applying it to "run a
   procedure the third time, then script it" is an analogy, not what the source says.
7. **verified** (secondary summary) — Limoncelli, "Manual Work is a Bug", ACM Queue 2018, as summarised by bssw.io
   (https://bssw.io/items/manual-work-is-a-bug): "Document the process as you do the steps manually the first time",
   then add exact commands, then "Develop an expanding set of scripts/code to automate parts of the process as it is
   executed repeatedly", then a stand-alone tool. Processes worth it are those "likely to be repeated enough to justify
   automating them to some degree"; "Only by performing these processes repeatedly can we understand what is really
   needed and what should be automated." The ACM Queue article itself returned HTTP 403 and was not read.
8. **verified** — Dan Slimmon, "Do-nothing scripting" (https://blog.danslimmon.com/2019/07/15/do-nothing-scripting-the-key-to-gradual-automation/):
   "A do-nothing script is a script that encodes the instructions of a slog, encapsulating each step in a function";
   it performs no step itself, and "doesn't save your team any manual effort" on its own, but "lowers the activation
   energy for automating tasks" and makes it "much less likely that you'll lose your place and skip a step." Automating
   "sometimes feels like an all-or-nothing proposition."
9. **not found** — No study or practitioner source found gives a measured frequency at which an operational script
   pays off against a page. The sources found give a comparison (cost against benefit, xkcd's table) or a heuristic
   (rule of three, "repeated enough"), not a measured threshold.

### B. What happens to rarely-run scripts

10. **verified** — Google SRE book, "The Evolution of Automation at Google"
    (https://sre.google/sre-book/automation-at-google/): rarely-run automation is "often particularly fragile because of
    the extended feedback cycle"; cluster failover is "one classic example of infrequently executed automation", crucial
    "but only executed at infrequent intervals and therefore difficult to test."
11. **verified** — same chapter: "Automation code, like unit test code, dies when the maintaining team isn't obsessive
    about keeping the code in sync with the codebase it covers"; "The world changes around the code". Early ad hoc
    turnup shell scripts were "brittle" and "became a cholesterol of technical debt."
12. **verified** — same chapter, a failure of an automation script: the empty set "was used as a special value,
    interpreted to mean 'everything'", and the automation sent almost all machines to Diskerase. Scripts can fail loud
    and wide, not only silently.
13. **verified** — same chapter, on the benefit of running often: "If automation runs regularly and successfully
    enough, the result is a reduced mean time to repair (MTTR)". The chapter does not state a general rule that more
    frequent runs make automation more reliable.
14. **verified** — Martin Fowler, "Frequency Reduces Difficulty" (https://martinfowler.com/bliki/FrequencyReducesDifficulty.html):
    "if it hurts, do it more often"; pain grows with the time between integrations; reasons given are chunking,
    feedback and practice ("we improve as we do it more often"). About integration and deployment, applied here by
    analogy.
15. **reported** — search results (Xebia, Sonar on "bit rot"; a Linux kernel mailing-list thread saying gdb helper
    scripts "are peculiarly sensitive to getting damaged by routine kernel development") describe scripts left unrun
    breaking as their environment changes; the common advice is to run them on a schedule or in CI. Pages not opened.

### C. What happens to rarely-run written procedures (pages, runbooks) and to the people using them

16. **verified** — Gremlin, "Ensuring runbooks are up to date" (https://www.gremlin.com/blog/ensuring-runbooks-are-up-to-date):
    runbook documentation, "if it is not already outdated, it will be"; "The biggest reason that documentation doesn't
    get updated is that time was never scheduled to update it." Advice: regular tests of runbooks, game days, chaos
    experiments to "validate whether the guidance in our runbooks is valid", quarterly (or monthly) reviews. A vendor
    source.
17. **reported** — vendor and practitioner posts (OpsPilot, Tallyfy, found by search, not opened): runbooks drift
    silently after system changes; review cadence is slower than change; writing a runbook earns credit, updating it
    does not. The figures they quote (for example "60% faster" attributed to Atlassian, DORA percentages) have no
    primary source found.
18. **verified** (secondary notes) — Bainbridge, "Ironies of Automation" (1983), as noted by Fred Hebert
    (https://ferd.ca/notes/paper-ironies-of-automation.html): "cognitive and manual skills, both of which erode over
    time when not used"; recall becomes "more deliberate, less automatic, and slower"; she recommends operators
    "frequently run some steps manually just to remain familiar", or simulators. The paper itself was not opened.
19. **verified** — Google SRE book automation chapter, same point in operations: "The fluidity of their reactions has
    been lost due to lack of practice", and manual fallbacks may vanish: "those manual actions are not always
    performable because the functionality to permit them no longer exists."
20. **verified** — UK HSE, maintenance error (https://www.hse.gov.uk/humanfactors/topics/error.htm): lists "omission of
    a task step" among common maintenance failures and advises "Develop up-to-date procedures for safety-critical
    maintenance tasks." It says nothing on infrequent tasks.
21. **reported** — Hobbs, ISASI 2004 paper and a maintenance error guide (search results; PDF could not be read):
    omissions are the largest single category of maintenance errors, often memory lapses near the end of a sequence;
    mistakes are likely when someone is "feeling their way through an unfamiliar task". About unfamiliarity, not
    measured frequency.
22. **reported** — Aghajani et al., "Software Documentation Issues Unveiled", ICSE 2019: the review at
    neverworkintheory.org (opened) quotes "the creation and the maintenance of documentation is often neglected,
    negatively impacting its quality and usefulness"; an "outdated documentation" category and its frequency were not
    confirmed from what was opened.

### D. Reading across the sources (my reading, not a source's claim)

- Every source that weighs scripting does it as a comparison — build plus keep cost against runs times the effort
  and error it removes — and none gives a measured break-even frequency for an operational procedure.
- Both forms decay when not run: a rarely-run script breaks as the world changes around it (B10, B11, B15), and a
  rarely-run page goes out of date and the person following it is out of practice (C16, C18, C19). The difference the
  sources point at is how the decay shows: a script that is run (or tested on a schedule) fails at a known step, while
  a page drifts with nothing to signal it until it is followed (C16, C17; the "silent" claim is reported, not
  measured).
- The remedy both camps name is the same: exercise it — scheduled runs or CI for scripts, game days and runbook tests
  for pages (B13, B14, C16, C18).
- Middle forms exist: a page with exact commands, then partial scripts (A7), a do-nothing script (A8), partial
  automation as an interim step (A3).
