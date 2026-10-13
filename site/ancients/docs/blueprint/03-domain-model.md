Status: settled (accepted by EJ on 2026-10-13)
Drawn from: 02-requirements.md R1, R5

# Domain model

- **Person** (R1) — one of the four seats: an id (`fan-li`, `sun-tzu`, `lao-tzu`, `linus`), a name, a "who they
  are" text, and a list of items.
- **Item** (R1.2, R5) — one entry of a person's final list: number, title, kind, rule, their words, source, label,
  from.
- **Kind** — `mindset` · `decision rule` · `algorithm` (as the lists use them).
- **Label** — what the lists call "Words are": `quoted` (the person's own words) · `attributed` (recorded about them).
