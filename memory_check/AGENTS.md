# memory-check — instructions for every agent working on it

Read first, in this order: `VISION.md`, `USE_CASES.md`, `REQUIREMENTS.md` in this folder. A use case wins over a
requirement that conflicts with it; say so when you find one.

- **What it checks comes from the guidelines only:** `docs/memory-system/SOURCE_OF_TRUTH.md`,
  `docs/memory-system/SOURCE_OF_TRUTH_REQUIREMENTS.yaml` and `docs/memory-system/CACHES.md`. Never edit those three:
  a problem in them is reported, not fixed here.
- **Language:** TypeScript on bun, like `code_map/` and the guard. Tests with `bun test`; types with `tsgo --noEmit`.
- **Reuse:** the index and entry-format checks are `tools/memory_index.py --check`; call it, do not rewrite it.
- **Read only:** the tool writes nothing but its own report. A test proves it on a fixture (`git status` before and
  after).
- **Tests:** each requirement and use case's **Fails if** has a test that fails on a planted break first. Fixtures live
  in `memory_check/test/fixtures/`; never point a test at the real home folder.
- **Evidence and run records** go in `runs/<run-id>/`, not `/tmp`.
- **Engines** get their instructions in a brief file, with the matching agent lessons pasted in
  (`lessons for --agent <engine>`), and their stdin from `/dev/null`.
