# Integration text — draft, applied after round 3 passes and the package moves into the skill

## Method 3.8, new item 13 (appended; items are cited by number, never renumbered)

13. **Code holds what needs no judgment** — the skill's `guard/` package (bun, TypeScript, no dependencies) runs at
   fixed points so an agent cannot skip it once installed: before an engine call it lints the command against a trap
   catalogue (`guard/data/traps.yaml`; only `approved` entries act), after the call it treats a missing or empty
   output, a known silent-failure text or a failing exit as a failure (exit 0 is not success) and logs it to
   `.harness-guard/journal.jsonl` with its evidence, and a session with logged failures cannot stop until an insight
   answers each (six whys to a changeable source, root cause, 2–3 fix options with evidence) and the final message
   names it. Judgment stays with the agent: the whys, the options, use cases and fails-if. Installing the hooks is the
   owner's (`guard/src/cli.ts install --print <harness>`); the agent never edits harness config. Measured once
   (`runs/20261015-ts-hybrid/`, n = 6 per arm on one short task): with the rules in the working folder, agents followed
   them without the hooks; the hooks caught a format slip the rules alone let through, and cost time. Not measured: a
   long session where the rules are out of reach.

## Method 3.1, one sentence after the harness_health sentence

  `guard/src/cli.ts doctor` reports, per harness, whether the guard's hooks are installed and whether the guard
  answers a planted trap (it reads settings key names only and changes nothing).

## SKILL.md step 1 (after "…with help for what is absent)")

   …; `guard/src/cli.ts doctor` says whether the guard's hooks are installed — install is the owner's
   (`install --print <harness>`)

## SKILL.md step 7 (after the dispatch.py sentence)

   With the guard installed, every engine call made through a shell is linted before it runs and its result checked
   after (method 3.8 item 13); without it, call `guard/src/cli.ts lint` and `result` yourself and log a failure with
   `fail` (a reason and evidence are required).

## SKILL.md step 8 (new sentence at the end)

   A run with logged failures ends with an insight (`guard/src/cli.ts insight` lists what is open) named in the final
   report; a use-case register is checked with `guard/src/cli.ts register <file>` (R11.1, R13).
