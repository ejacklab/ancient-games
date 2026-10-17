# bridge-2 · progress

- 2026-10-18T00:14:00+08:00 · grouping · planned · V6: group the FAIL requirements by `group`, one record per group (`evaluator:<group>`, ids joined by ", ", evidence the group's FAIL cases)
- 2026-10-18T00:14:00+08:00 · baseline · planned · V7: read `--baseline <verdict.json>`, a group FAIL in the baseline becomes the note `- <group> · FAIL in the baseline too · <ids>`
- 2026-10-18T00:14:00+08:00 · verify · planned · `bun test` all pass, `tsgo --noEmit` clean, result file written- 2026-10-18T00:14:00+08:00 · grouping · start · evaluation.ts: failingGroups() + the group loop; readVerdict() factored out so the baseline reads by the same rules
- 2026-10-18T00:14:34+08:00 · grouping · done · V6 and V1 both pass; evidence is the group's ids and its FAIL cases
- 2026-10-18T00:14:00+08:00 · baseline · start · the baseline's own early returns: absent / not JSON / no requirements are all a note, exit 1, no record
- 2026-10-18T00:14:34+08:00 · baseline · done · V7 passes; a held-back group becomes `- <group> · FAIL in the baseline too · <ids>`; --baseline with no value is exit 2
- 2026-10-18T00:14:00+08:00 · verify · start · bun test, tsgo, the four baseline early returns by hand in a scratch root
- 2026-10-18T00:14:34+08:00 · verify · done · 1526 pass / 0 fail, tsgo exit 0; the start lines of the three pieces were written at the end, so this file shows planned → start → done out of order in time
