# Progress — the evaluator's parser reads the paragraph form (DATA.md E1 rule 9)

- 2026-10-18T01:52:00+08:00 · read · planned · DATA.md E1 rule 9, the paragraph tests, both new fixtures, and the frozen rules 1-8 tests
- 2026-10-18T01:52:20+08:00 · read · start · read rule 9 and the two paragraph fixtures line by line
- 2026-10-18T01:55:34+08:00 · read · done · rule 9 read; the four early returns of _read_groups (group heading, heading, bullet, plain line) listed; index-md's `## B — ` headings noted as the collision with rule 1
- 2026-10-18T01:55:40+08:00 · design · planned · decide how a heading group opens without adding an empty group to index-md
- 2026-10-18T01:58:00+08:00 · design · done · a heading group is made when its first paragraph lands (lazily); a requirement paragraph is a group of its own only when no heading group holds it; both at column 0
- 2026-10-18T02:00:00+08:00 · code · planned · extend _read_groups with a paragraph branch, leaving the bullet branch as it is
- 2026-10-18T02:00:10+08:00 · code · start · HEADING_GROUP, PARAGRAPH_START, FAILS_IF_IN_TEXT, _paragraph, _paragraph_title, _starts_fails_if, _paragraph_fails_if, _new_group
- 2026-10-18T02:05:00+08:00 · code · fail · a block quote holding `**Fails if**` mid-line stalled the loop: the Fails if paragraph test searched anywhere, and _paragraph returned the same index
- 2026-10-18T02:07:00+08:00 · code · done · a paragraph is read only from a line that begins nothing else, and a Fails if paragraph only when the marker opens it; rules 1-8 byte-identical on the four old fixtures
- 2026-10-18T02:08:00+08:00 · verify · planned · python3 -m pytest -q tests/test_evaluator_*.py
- 2026-10-18T02:10:04+08:00 · verify · done · 184 passed in 39.98s
- 2026-10-18T02:10:05+08:00 · report · planned · write result.md
- 2026-10-18T02:10:12+08:00 · report · done · result.md written; CONTRADICTS names the one line of rule 9 that cannot be met as written