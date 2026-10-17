# Linus Torvalds — improve memory-check next

## Answer

My reading: first prevent the report writer from overwriting memory. Second, carry affected filenames as data through the checks into warnings, if this round’s fixes have not already done that.

## How I decided

1. **My #7 and #2 — establish what is actually known.** The brief’s `findings.md` and `fix-r*.result.md` were absent when checked. The [review report](/home/smoke01/dev/ancient-games/runs/20261017-memory-check-review/review/r1-codex.md) exists, but I cannot call its findings accepted or fixed. These recommendations concern the code currently present.

2. **Rank 1: prevent report destinations from changing memory — my #1, #3 and #13.** This serves the read-only promise in [VISION.md:22](/home/smoke01/dev/ancient-games/memory_check/VISION.md:22). The concrete case is `--out AGENTS.md`: [command.ts:118](/home/smoke01/dev/ancient-games/memory_check/src/command.ts:118) passes that destination directly to `writeFileSync`. My in-memory probe intercepted an attempted overwrite and returned exit 0; the real file remained unchanged. Existing [read-only tests](/home/smoke01/dev/ancient-games/memory_check/test/acceptance.test.ts:46) use a separate `report.md`, so they miss this collision. Have the tool reject report destinations that would change memory, including aliases to those files.

3. **Rank 2: preserve filenames separately from evidence prose — my #9 and #10.** This serves **U3**, giving the starting agent an actionable warning, and **U2**, preserving the affected file’s identity. [RequirementResult](/home/smoke01/dev/ancient-games/memory_check/src/checks.ts:29) carries evidence as text; [warn.ts:48](/home/smoke01/dev/ancient-games/memory_check/src/warn.ts:48) extracts filenames from that prose. My direct probes confirmed that a bare Python filename disappears, while a path containing spaces and Chinese characters is truncated. Preserve file paths when each finding is produced and let warning rendering consume them directly. If the pending fixes already achieve this, count it as done.

4. **My reading — requirement check.** These are provisional recommendations, not accepted requirements. Both pass **who decides, one thing, unit, can it fail, weak words, level, basis and links** as scoped above: the tool decides, each outcome has a concrete failing input, and each serves a named product outcome. No new numerical threshold is needed.

## What I need to know

Which fixes were actually applied? If they already prevent report collisions or preserve complete filenames, omit that recommendation.

## Costs and risks

- **Rank 1 — my #5 and #18:** destination validation adds filesystem edge cases and may reject an output location previously accepted. Resolving only the written pathname would leave aliases untreated.
- **Rank 2 — my #13 and #18:** adding file metadata touches finding producers and renderers. Keep it confined to filenames; changing Python’s entire output protocol would enlarge the work unnecessarily.

## How we would know I was right

- **Rank 1:** independently written tests attempt direct and aliased output destinations targeting instructions, entries, indexes and caches. Every attempt is rejected with original bytes unchanged; an ordinary report destination succeeds.
- **Rank 2:** literal expected filenames survive Python-originated findings, spaces and Unicode exactly, with one warning per qualifying MUST and no entry text.

I wrote the probes above. They establish intercepted write behavior and warning formatting, not independent verification of the complete tool.

**Top one: prevent `--out` from overwriting memory.**