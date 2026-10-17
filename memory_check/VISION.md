# memory-check — vision

A TypeScript tool that looks at a project, finds which memory it has, checks that memory against the two memory
guidelines — `docs/memory-system/SOURCE_OF_TRUTH.md` (with `SOURCE_OF_TRUTH_REQUIREMENTS.yaml`) and
`docs/memory-system/CACHES.md` — and tells the user what is there, what is missing and what is wrong: a full report on
demand, and warnings at the start of a session.

## Who it is for

- **The project owner**, who wants to know, without reading the guidelines, whether a project's memory follows them.
- **Every agent starting a session**, which must not start work on memory that is missing, stale or broken without
  being told.

## What it checks

Only what the two guidelines require: each check is one requirement's `fails_if` (or **Fails if**) line, cited by its
id. A requirement whose check is a reviewer's judgement is listed as needing a reviewer, never passed or failed by the
tool. The tool adds no rule of its own.

## What it will never do

- Change any memory, entry, index or cache: it only reads, and writes only its own report.
- Say a requirement passes without the evidence that shows it.
- Load what the guidelines say is never loaded (another agent's transcripts, credentials, the whole memory tree at
  once).
- Replace `tools/memory_index.py`: where that tool checks a requirement, this one runs it and reports its result.
