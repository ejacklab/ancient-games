# Brief 1a — a question set for measuring caches (run 20261012-caches-routing)

You are writing a test set. Do not answer anything else, and do not change any file.

The repo is `/home/smoke01/dev/ancient-games`: Python code (`ancient_games/`, `code_graph/`, `tools/`, `skills/`), pytest
tests (`tests/`, `code_graph/tests/`) and memory-like markdown (`docs/`, `runs/`, `DECISIONS.md`, `SPEC.md`,
`PROJECT_OVERVIEW.md`). Ignore `runs/20261012-caches-routing/` and `runs/20261012-memory-caches/`.

We will measure how fast and how cheaply in tokens an agent can find answers with grep, with a full-text index, with a
vector index and with a code graph. For that we need **40 questions an agent really asks while developing and testing
this repo**, each with a checked gold answer.

## Categories (exact counts)

- **A: exact identifier (8).** Where is a named function, class, constant or CLI flag defined?
- **B: concept in other words (8).** The question does not use the code's own words. Example: "where does the code
  decide that an action needs a human's approval?" Check that the key words of the question do not occur literally
  in the gold file, or occur only rarely.
- **C: structure and test impact (10).**
  - at least 4 of "which tests exercise function X" (gold = test functions or test files that call X directly or
    through a fixture)
  - at least 3 of "if I change file F, which test files should I run"
  - at least 3 of "what calls function X" (gold = caller functions or files)
- **D: decision or reason in the docs (8).** Why something was decided or rejected, or what EJ decided about X. Gold =
  the markdown file(s) that state it.
- **E: how to run or configure (6).** For example, how to run the tests, or where a model or engine is configured.

## For each question, give

- `id`: e.g. A01.
- `category`.
- `question`: natural language, as an agent would ask it.
- `terms`: 1–4 words an agent would grep for first. These must be guessable from the question alone, not from the
  answer.
- `symbol` and `file`: the identifier or file the asker already knows, if any; otherwise null.
- `gold`: a list of repo-relative paths. For test files use the path; for a function use `path::name`. Keep it
  small, with only the places that truly answer the question. For C questions list every answer, because
  completeness matters there.
- `gold_check`: the exact command you ran (`rg ...`, `grep ...`, `sed -n ...`) and a one-line excerpt of what it showed
  proving the gold.
- `literal_overlap`: true if the `terms` occur literally in a gold file, false if not.

## Rules

- Every gold answer must be checked by a command you ran in this session. Never guess.
- If you cannot check a question, drop it and write another.
- Do not create or edit files. Print the result to stdout.

## Output

First a JSON array between the lines `BEGIN_QUERIES` and `END_QUERIES`, then a short list of anything you were unsure
about.
