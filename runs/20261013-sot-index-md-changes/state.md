# Run 20261013-sot-index-md-changes — state

**Asked by EJ, 2026-10-13:** *"commit, then ask your subagents, codex, agy and opencode to help me go through the INDEX.md-related design changes"*. The five changes are item 4 of "Open, for EJ" in `docs/index-md/REQUIREMENTS.md`.

**Shape:** one round, four blind readers (claude subagent, codex, opencode, agy), brief `briefs/enhance.md`, reports to `reviews/<engine>.md`; the COO sums them. Engines and flags as in `run.sh` (stdin from /dev/null).

## Log
- 2026-10-13 Committed the item 1–9 work as 0c19b18 before this run.
- 2026-10-13T01:03:39Z ROUND 1 done: codex exit=0 11546B; opencode exit=0 12755B; agy exit=1 0B; 
- 2026-10-13T01:03:56Z agy failed: gemini-3.1-pro-high no longer offered (agy models). Re-run agy alone on gemini-3.8-flash-high; run.sh updated.
- 2026-10-13T01:08:39Z agy rerun exit=0 16373B. All four in; COO summary: summary.md.
- 2026-10-13T04:35:50Z EJ: id form "DD-MM-random 6 digit + char-YYYY"; "the design can suggest the name and user accept". Applied to SOURCE_OF_TRUTH (header, What will be put in, When to write, Still open, size line, W1.1-W1.3 + Fails if, W6 Open narrowed, K6.2, K6.3, K6 Fails if, Rd3.1) and docs/index-md/REQUIREMENTS.md (hedges, G4.1, Open list). W6 entry-conflict question left open; EJ asked "conflict, can we regen again?".
- 2026-10-13T05:08:10Z EJ: "yes write the first one, impact later". Applied: K4.3 claim never rewritten (changed claim = new superseding entry), W6.3 merger keeps both sides, two superseders reported as Rd5.3; Changing entries and Merge conflicts paragraphs; header note. Impact level left for later.
