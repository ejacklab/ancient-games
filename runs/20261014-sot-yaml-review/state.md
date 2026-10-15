# State — the source-of-truth memory design (as of 2026-10-14)

Rules: one writer at a time. Read this file before your step; update it after. It holds progress and results only —
never reasoning. Never delete a log line.

## Where we are now

The design is `docs/memory-system/`:
- `SOURCE_OF_TRUTH.md` — the design, prose only (155 lines): why, who it is for (the project owner defined), what goes
  in, where, when. Its requirements section is a pointer to the YAML. No history in it.
- `SOURCE_OF_TRUTH_REQUIREMENTS.yaml` — the 46 requirements as 64 records (mixed-level requirements split into
  clauses), each with one `level`, `fails_if`, `check`, `who_decides`, `links`. Built by `build_requirements.py` in
  this folder, which also checks it (loads, one shape, ids unique, all 46 covered, links resolve).
- `SOURCE_OF_TRUTH_RELEASE_NOTES.md` — the history, newest first.

The tool `tools/memory_index.py` checks the id form and conflict markers (merged `6415a1c`, pushed).

**Committed and pushed:** `66f3bcc` (the three files and this run folder).

## Steps

| # | Step | Status | Output |
|---|---|---|---|
| 1 | MUST/SHOULD levels for the 46 requirements | done | `runs/20261014-sot-must-should/` (rounds 1–2, EJ's id-form MUST, the COO's six) |
| 2 | memory_index.py: id form and conflict markers | done, merged, pushed | `runs/20261014-memory-index-cleanup/` |
| 3 | History out of the design, into release notes | done, pushed `66f3bcc` | `docs/memory-system/` |
| 4 | Requirements to YAML: draft, four experts' review | done | `experts/compare.md` |
| 5 | Requirements to YAML: the majority layout, "project owner" | done, pushed `66f3bcc` | `docs/memory-system/SOURCE_OF_TRUTH_REQUIREMENTS.yaml` |
| 6 | Commit and push 3–5 | done | `66f3bcc` |

## Log (append only)

- 2026-10-14 EJ: *"this md file is a memory design doc … I don't think we should have those logs or status at the starting of the file … then you can create another release note"* → history moved to `SOURCE_OF_TRUTH_RELEASE_NOTES.md`.
- 2026-10-14 EJ: *"I got a feeling this memory design doc better change to use yaml format"*, then *"we can have this doc point to a YAML file"* → draft `draft-SOURCE_OF_TRUTH_REQUIREMENTS.yaml` (word for word, round trip identical).
- 2026-10-14 EJ: *"yes ask the 4 experts to review the draft"* → `experts/`; check 3 failures, all 老子 script or variant readings (為/爲 twice, 吾/我有三寶). Majority: split mixed-level requirements (4/4), `fails_if` per requirement (4/4), `links:` (3/4), `who_decides` on open choices (4/4). Dave (control): test first, keep A and B.
- 2026-10-14 EJ: *"yes 1 and 2, use project owner, skip the test"* → YAML rebuilt to the majority layout (`build_requirements.py`: 64 records, checks pass); `SOURCE_OF_TRUTH.md` points to it; "EJ" → "the project owner". New wording the COO wrote is listed in the release notes (2026-10-14). Suite: 993 passed, 1 failed (`test_skills_export_is_current`, another session's uncommitted skill edits, not this work).
- 2026-10-15 EJ: *"commit and push"* → `66f3bcc` pushed (`3f74440..66f3bcc`).
- 2026-10-15 EJ: *"ask the 4 experts to review"* → `runs/20261015-sot-final-review/` (check: 3 failures, 老子's answer cut short after its reasoning). EJ: *"yes apply 1-5, project owner reviews"* → K4.1 retired-with-reason, K1.1 supersession steps, MUST stops what its fails_if names, W1.2 key-line moved to SHOULD, SHOULD reason in `state.md`, scanner marked absent, YAML governs over prose, project owner reviews. YAML rebuilt (checks pass). Pushed `fe30559`.

## TODO next

1. ~~Commit and push~~ — done 2026-10-15, `66f3bcc`.
2. ~~Who reviews the judged checks~~ — the project owner, or someone they name (EJ, 2026-10-15).
3. **The open `who_decides`:** W3.6 (whether a procedure can be a script) and Rd3.1a (which agents work on the
   project, so the strictest `INDEX.md` limit). EJ's decision.
4. ~~Linus's five behaviour gaps~~ — retiring, superseding and what a MUST stops settled 2026-10-15. Was: **Linus's five behaviour gaps** (`experts/answers/linus.md`, step 6): retiring an entry with no replacement; K1.1
   "change the entry first" against K4.3 "never rewrite a claim"; what work a failed MUST stops; Rd4.1 reads
   entries but its old check said decisions (now entries); Rd2's check against the link exception (now handled in
   Rd2.3b). Three are open product questions for EJ.
5. **Review the COO's new wording** in the YAML (release notes, 2026-10-14): the five new `fails_if`, the W1.2 split,
   the `who_decides` values.
6. **No secret scanner exists** for W3.2's `check: secret scanner`. Build one, or accept reviewer only.
7. **Ledger row** for run `20261014-memory-index-cleanup` in `docs/TASK_TYPES_LEDGER.md`, once the other session's
   uncommitted edits there are committed.
8. **Cleanup:** remove branch `fix/index-id-and-markers` and worktree `../ancient-games-index-clean` (merged), on EJ's
   word.
9. **Not done by EJ's choice:** the agent test, YAML against Markdown (all five experts asked for it). Whether agents
   follow the YAML better stays *not measured*.
10. **Left from the 2026-10-15 review** (`runs/20261015-sot-final-review/experts/compare.md`): W6.3b says `check: tool`
    but K6.3b, which it points to, says `reviewer`; K4.3 lets an entry gain only four things after its first commit, so
    a stale `covers` path can only be fixed by superseding (Dave); `basis` paths assume this repo's folders; the prose
    typo "When the work a decision to build something is complete"; the tool hard-codes the `INDEX.md` limit (200
    lines, 24,000 bytes) that Rd3.1a leaves unassigned.
