# Question — how should memory-check work, before any code is written?

The owner (EJ) asked for a TypeScript tool that checks what memory a project has against the two memory guidelines
and gives a report and a warning. The design docs are written; your advice shapes the build. The owner decides.

Rules for this question:
- Rest each point on a fact below (each carries its source) or one you check in this repository; a point from memory
  only is labelled *recall* and does not decide alone.
- Every file you need is inside this repository.

## Facts
- The tool's vision, use cases (U1–U6) and requirements (F1–F3, C1–C4, R1–R3): `memory_check/VISION.md`,
  `memory_check/USE_CASES.md`, `memory_check/REQUIREMENTS.md`; agent instructions `memory_check/AGENTS.md`. U4–U6 and
  the requirement groups are marked *proposed*. (Source: those files.)
- The guidelines it checks: `docs/memory-system/SOURCE_OF_TRUTH.md`, `docs/memory-system/SOURCE_OF_TRUTH_REQUIREMENTS.yaml`
  (64 records: id, level, check, fails_if — listed one per line in `runs/20261017-memory-check/sot-requirements.txt`),
  and `docs/memory-system/CACHES.md`, section "Core requirements" (B1–B5, K1–K3, Rd1–Rd3). (Source: those files.)
- Of the 64 records, about 20 have a `check` of `tool` or `git`; the rest are `reviewer` or `none`. (Source:
  `sot-requirements.txt`, counted by the main agent.)
- `tools/memory_index.py` already builds and checks `project-memory/INDEX.md` (`--check`, `--check <rev>`), the entry
  header and claim format, duplicate ids, conflict markers and the index size. (Source: `tools/memory_index.py`
  lines 1–15 and its function list.)
- This repository has no `project-memory/` folder today. (Source: `ls project-memory` fails.)
- Other TypeScript tools here run on bun with `bun test`: `code_map/`, `.claude/skills/workflow-design/guard/`.
  (Source: their `package.json`.)
- The owner chose that the warning is both a command and a session-start hook; installing the hook needs the owner's
  yes to the settings diff. (Source: this session's decision, recorded in `memory_check/REQUIREMENTS.md` R2.)

## The decision
1. **Which requirements can a tool really check, and how?** For the `tool`/`git` records and the CACHES requirements:
   which are checkable on files alone, which need git history, and which need something the tool cannot see. Cite ids.
2. **What is missing or misleading in the four docs** — a use case or requirement that would make the tool give a
   wrong answer, or a check the docs ask for that cannot be built.
3. **The build:** how to split it into small pieces that can each be tested on a fixture, and how to test the
   checks without circularity (a known answer computed differently from the check).

End with your recommended plan in eight lines or fewer.
