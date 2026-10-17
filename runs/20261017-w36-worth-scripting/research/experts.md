# Research: when scripting a procedure pays off, and what happens to rarely-run scripts and pages

Question: when does scripting an operational procedure pay off compared with a written step-by-step page; what do
practitioners and studies say about build-and-keep cost against how often it runs; what happens over time to
rarely-run scripts and to rarely-run written procedures?

Researched 2026-10-17 by the research step of experts-decide (Claude, web search and fetch). How to read the labels:
**verified** means the page was opened with a fetch tool and it says this (the fetch tool returns an extract, so
quotes are as that extract gave them). **reported** means a search result or a secondary source says it and the page
itself could not be opened or did not show it.

## A. Cost of building and keeping a script against how often the procedure runs

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

## B. What happens to rarely-run scripts

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

## C. What happens to rarely-run written procedures (pages, runbooks) and to the people using them

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

## D. Reading across the sources (my reading, not a source's claim)

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
