# Coverage trial — results (n=1, requirement W1.1b)

Prediction: `prediction.md` (written before generating and before reading the tests). Briefs: `briefs/a.md`
("List the test cases"), `briefs/b.md` ("Brainstorm every possible scenario … Be exhaustive"). Engine: dsh headless,
deepseek-flash, same requirement text, no access to tests. Outputs: `out/a.md`, `out/b.md`.

All mapping and coverage marks below are the main agent's (*my reading*). "Covered" = an existing test in
`tests/test_memory_index.py` or `tests/test_memory_index_unit.py` exercises an input of the same shape, whatever result
it asserts.

## Raw numbers

| | A | B |
|---|---|---|
| Time | 20 s | 85 s |
| Cases generated | **28** | **200** |
| Cases an existing test covers | 13 | 40 |
| Raw coverage | **46%** | **20%** |
| Coverage over the fixed units | **80%** (4 of 5) | **80%** (4 of 5) |

Same requirement, same engine, same tests — only the brief's wording changed. The list grew about 7 times and the raw
percentage fell from 46% to 20%. The unit percentage did not move. **Prediction held** (*my reading*, n=1).

## Units (fixed before generating)

| Unit | Covered by | A cases | B cases |
|---|---|---|---|
| U1 form | yes — legacy form, five characters, trailing junk, whitespace, non-ASCII digits, missing / empty / nested id (`test_memory_index.py:354`, `:374`; unit `:118`) | 4, 5, 8–11, 16–18, 22 | 11–18, 27–28, 30–38, 152–153 |
| U2 random part's alphabet | yes — uppercase, non-ASCII digits | 6, 7 | 5–10, 96, 154–157, 160 |
| U3 real calendar date | **dropped**: the tests pin the opposite on purpose — `31-02-…` must be accepted, "the form is the whole rule" (unit `:104`, G4.2). A's cases 12–15 expect a violation and contradict that decision; B called them "spec gaps". | 12–15 | 19–26, 29, 158–159 |
| U4 no shared id | yes — duplicates in any status (`:391`; unit `:93`) | 19, 20, 27 | 55–76, 95, 176–184, 188–189, 193, 195 |
| U5 renamed to a different id (git) | **no — no test, and no code**: `tools/memory_index.py` reads `git ls-files` only; nothing outside `runs/` compares ids across a rename | 23–25 | 77–105, 148–151, 164–167, 180, 186–187, 194, 200 |
| U6 a valid id is accepted | yes (`:329`; unit `:104`) | 1–3, 26 | 1–4, 39, 54, 172, 185, 197, 199 |

With U3 dropped by an earlier decision, 4 of 5 units are covered: **80%**, the target, with U5 the one gap.

## Cases that fit no unit (did a run move the denominator?)

| Candidate unit | A | B | Belongs to |
|---|---|---|---|
| Filename id and header id agree | 20–21 | 40–45, 163 | W1.1c (file name), not W1.1b |
| The id's date is the day the entry was written | 28 | 46–53, 138 | W1.1b's text, but not its fails-if — a gap in the requirement |
| Which files the checker scans (temp, hidden, subfolders, symlinks) | — | 71, 114–121, 169, 190 | the checker, not W1.1b |
| Checker robustness (unreadable file, partial write, huge folder, Windows paths) | — | 122, 146–147, 168, 170–171, 191–192 | the checker |
| Report shape (exit code, names every file) | — | 139–145, 161–162 | the checker |
| Out of scope (naming, header format, randomness, future revisions) | — | 107–113, 123–137, 173–175, 181, 196, 198 | W1.1c, W1.2, or not checkable |

Neither run added a unit to W1.1b itself; both found the same one gap in its *text* (the write date, which fails-if
does not name). B's extra classes are about the checker, not the requirement.

**Capture–recapture on classes** (Dave): A found 8 classes, B 11, both 8 → estimate 8 × 11 / 8 = 11 = the union. Same
engine twice, so not independent — a lower bound, nothing more.

## Findings

1. **The drift is real here** (*my reading*, n=1): wording alone moved the list from 28 to 200 and the raw figure from
   46% to 20%. Counting over fixed units gave 80% both times.
2. **The trial found a real gap.** W1.1b's fails-if (c), "git shows an entry file renamed to a different id", has no
   test and no code. Both runs generated rename cases (A: 3, B: about 40). Under R11.1 that unit must be covered or
   marked skippable by the criterion — its consequence (an id that changes breaks every link to it) is the owner's
   call.
3. **A generated cases that contradict a settled decision** (calendar dates). A raw count would have counted them as
   uncovered work; the unit list shows they are settled.
4. **B's 200 are mostly about the checker**, not the requirement — useful for the checker's own requirements, noise
   for W1.1b's percentage.

## What this does not establish

One requirement, one engine, one mapper (the main agent, who also wrote the units). A second mapper could group the
cases differently; nobody checked the marks. It shows the effect exists, not how big it is in general.
