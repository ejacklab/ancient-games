---
agents: [all]
kinds: [test]
from: memory plant-replaces-a-line (F-0f2fa841, F-21e1586c, 2026-10-17)
---
A planted break replaces a line that must exist, asserted present exactly once first, and never goes at a file's start
or end (after the script's own exit it never runs; before its first import it breaks for another reason). Assert the
plant's own failure before the reaction you are testing.
