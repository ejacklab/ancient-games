# Five decisions to finish the source-of-truth memory design

A time-boxed run (6 hours, owner EJ away until the end): the main agent applies your **majority** on each point,
provisionally; EJ accepts or overrules at the end. Answer **each of D1–D5** with one choice, a short reason from your
rules or the research, and the words to write if it changes the design. Never invent a number: a limit is a measured
or documented value with its source (the owner's rule, *recall*: house memory "comparisons, not numbers").

## Facts (each labelled)

- **The limits rule** (*read*: `docs/memory-system/SOURCE_OF_TRUTH_REQUIREMENTS.yaml`, record Rd3.1a, MUST, `check:
  tool`): *"`INDEX.md` fits the strictest start-file limit among the agents whose session start loads it. … The
  project owner records those agents and each one's limit, with its unit and its basis (measured, documented, or an
  example), in one file the tool reads; this requirement does not repeat the numbers. A documented figure is not a
  measurement of the installed engine. Until the tool reads that file, it holds the example in Rd3.1b."*
- **The tool** (*read*: `tools/memory_index.py:17-36`): Python, standard library only (`argparse`, `difflib`, `os`,
  `re`, `subprocess`, `sys`, `tempfile`, `urllib.parse`, `dataclasses`, `pathlib`); `MAX_LINES = 200`,
  `MAX_BYTES = 24_000`. It is run in write mode and with `--check` (also by `.githooks/pre-commit`).
- **The tool's spec** (*read*: `docs/index-md/REQUIREMENTS.md` B4.1): the two constants' values "come from measuring
  the readers' load paths. Until then they hold the design's example".
- **The last round** (*read*: `runs/20261017-sot-item11/experts/compare.md`): the file's place split (the design's
  folder 2, `project-memory/` 3, the owner 1); format YAML 4, JSON 2 (JSON because the tool is standard library only;
  no YAML voter said how the tool would parse it); when the example stops: no majority; both sides changing one path:
  no majority; measure later 4 of 6, agy first 3 of 6.
- **Documented limits** (*read*: `runs/20261017-sot-item11/research/experts.md`): Claude Code `MEMORY.md` 200 lines or
  25 KB; Codex `AGENTS.md` 32 KiB combined; agy 24,000 bytes per rule file plus a 20,000-token budget (12,000
  characters only from a third-party page); Qwen 200 lines or 25,000 UTF-16 code units; dsh 65,536 bytes; Gemini CLI
  and opencode none stated. Nothing measured.
- **The merge rule** (*read*: the YAML, record W6.3a): a `covers` path one side removed or replaced, and the other left
  alone, stays removed; nothing says what happens when **both** sides change the same path.
- **W3.2** (*read*: the YAML, record W3.2, MUST): *"No credentials or sensitive data."* `check: secret scanner;
  reviewer`. The YAML's `checks` key: *"a scanner over entries/ finds it. None exists yet; until one does, the reviewer
  is the check."* (*ran*: `which gitleaks trufflehog detect-secrets` found none installed.) The project owner reviews
  judged checks.

## The decisions

- **D1. The limits file: where, and what format?** Options include `project-memory/` (the project's own, beside
  `INDEX.md`) or the design's folder; JSON (parsed by the standard library) or a simple line format; or YAML (needs a
  parser the tool does not have). Name the path and the format, and the fields of one row.
- **D2. When does the interim example stop applying?** For example: as soon as the file exists; row by row; or only
  when every agent that loads `INDEX.md` has a row. What does the tool do if the file is missing, or an agent has no
  row?
- **D3. Both sides of a merge change the same `covers` path differently.** Keep both new paths; report it in
  `state.md` for the project owner; keep the path that exists in the repository; or another rule.
- **D4. The secret scanner for W3.2.** (a) build a small standard-library check into `tools/memory_index.py` (which
  patterns: say what is detected); (b) adopt an outside scanner (which, and who installs it); or (c) accept the
  reviewer as the only check and change `check:` to say so.
- **D5. Measure agy's start-file limit now, later, or never** — and if now, how (for example sentinel files at known
  offsets, with a control file under any limit).

The research for this question is added below by the workflow before you are asked.
