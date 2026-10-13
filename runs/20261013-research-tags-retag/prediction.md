# Prediction — written before either tagger started

Written by the COO (Claude Opus 5.5), 2026-10-13, UTC time below. The same text was sent to EJ in the chat before
R4 started, so its order is witnessed outside this repository.

## Metric

For each pass, against the old labels, counted by `count.py`: *same* / *moved* / *split* / *stuck*. Reported on
**140 rows** (the 143 without the three MagmaMem control rows R058, R091, R120, which the new rules make gap prose,
not tagged rows) and on all 143. "Movement" is reported two ways: *moved* alone, and *moved + split*.

Plus one sharp test, the two claims that got different tags in the accepted run (INDEX.md:255–256):
- Zep's numbers from one paper: R090 (s2-F2, old `verified`) and R004 (s5-F18, old `reported`);
- Mem0's numbers from one paper: R008 (s1-F3, old `verified`), R014 (s4-F19) and R056 (s5-F17), old `reported`.

## Expected result (my prediction)

1. **Control pass:** same on 105–125 of 140; moved 15–35. In at least one of the two pairs above, the rows still get
   different tags.
2. **New-rule pass:** moved + split on 30–60 of 140, mostly old `reported` → `verified` (a paper's own numbers,
   quoted) and old `verified` → split (a primary source that only asserts). Stuck: 0–3.
3. **Sharp test:** under the new rules, every row in each pair gets the same tag (or the same split).
4. If a second control pass runs: the two control passes disagree on fewer rows than either disagrees with the old
   labels.

## Void conditions, fixed now (any one voids the comparison; reported, not repaired)

- a pass's audit shows a read outside its two files (`run_pass.py` returns 2);
- the control pass agrees with the old labels on all 143 rows (a sign of copying, not agreement);
- the new-rule sheet is identical to the control sheet;
- a pass fails its plants or schema twice (attempt limit 2) → to EJ.

## Reading, fixed now (from `docs/RESEARCH_TAGS.md`, step 6)

Any stuck row in the new-rule pass → the definitions go back to EJ. New-rule movement no larger than control
movement → no measurable difference, reported as a result.

## Stop date

2026-10-14.
Written: 2026-10-13T13:18:58Z
