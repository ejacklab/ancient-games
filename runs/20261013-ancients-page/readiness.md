# Readiness — 20261013-ancients-page

Run 2026-10-13 by the COO (main Claude session). Anything missing becomes a preparation piece at the front.

## Tools

| Tool | Needed for | Command that proved it works | Result |
|---|---|---|---|
| Cloudflare API (MCP) | P5 deploy: Worker + custom domain | `mcp__cloudflare-api__whoami` → EJ's account (address redacted) | works |
| DNS for ejai.ai | P5 | `dns.google/resolve?name=ejai.ai&type=NS` → `bart.ns.cloudflare.com`, `haley.ns.cloudflare.com` | works — DNS is on Cloudflare |
| `ancients.ejai.ai` | P5 | `dns.google/resolve?name=ancients.ejai.ai` → Status 3 (NXDOMAIN) | free to create |
| ejai.ai hosting | U3 | `curl -sI https://ejai.ai` → `vary: x-fh-requested-host` (Firebase Hosting) | reported (header) |
| Firebase CLI 15.2.1 | U3 if Firebase | `firebase login:list` → "No authorized accounts" | **not logged in** — EJ would run `! firebase login` |
| gcloud 562.0.0 | U3 if Firebase | `gcloud auth list` → EJ's account (address redacted) | works |
| opencode 1.18.34, MiniMax | P2 build | used today in run 20261013-four-seats (3 calls, exit 0) | works (lesson: stagger parallel starts) |
| codex-cli 0.160.0, gpt-6.1-sol | P3 tests, P4 review | used today, 4 calls, model reported `gpt-6.1-sol` | works |
| dsh 0.2.0-rc.2 | P1 extraction (DeepSeek flash, EJ's default) | `dsh --version` | reported — no canary this session; P1's first call is the canary |
| Playwright (python) + chromium-1217 | P3 mobile tests | ran `reader_test.py` today: page turns, menu, reload, 0 errors | works |
| `kindle-page` skill | P2 starting point | built and tested today (`~/skills/kindle-page`) | works |
| quote check script | P1 check | scratchpad `final_check.py` / `zh_clause_check.py`; to be copied into the product | works, my script |

## Skills that apply

| Skill | What it covers here |
|---|---|
| `kindle-page` | themes, fonts, Aa menu, footer, settings memory — P2 extends it with a sideways "people" layout |
| `workflow-design` | this design |
| `requirement-check` | the blueprint requirements in P0 |
| `verify-extraction` | P1: an extraction is checked against the source, not by a second read |

## Information

| What is needed | Where it is | Structure | Verified? | Who can read it |
|---|---|---|---|---|
| Final lists | `runs/20261013-four-seats/final-opus/*.md`, `final/*.md` | md, one file per person, headings differ per file | quotes: script-checked today (`comparison.md`) | every engine |
| Bios ("who they are") | `runs/20261013-four-seats/identity/*.md` | md | **not checked** beyond the quotes | every engine |
| Sources | `runs/20261013-four-seats/sources/` + Opus downloads in the session scratchpad | text/html | yes | every engine; scratchpad copies vanish — copying them is an open question to EJ |
| Kindle facts | this session's research (KDP guidelines) | chat + `kindle-page/SKILL.md` | official KDP pages | every engine via the skill |

## Blueprint

- Product: the `ancients.ejai.ai` page. Map: none — **P0 drafts** `site/ancients/docs/blueprint/README.md`.
- Kind of task: **new product** — a public page that does not exist yet.

| Section | Needed? | Status | File | Effect |
|---|---|---|---|---|
| vision | yes | missing | — | P0 writes EJ's own words |
| requirements | yes | missing | — | P0 drafts R1–R6 with criteria; EJ accepts |
| domain model | slice only | missing | — | one paragraph in P0 (person, item, kind, label) |
| business logic | slice only | missing | — | one paragraph (ordering, which list) |
| architecture | yes | missing | — | P0: one decision record — static single file, host (U3) |
| data model | slice only | missing | — | P0: `ancients.json` schema |
| ui/ux | yes | missing | — | P0: layout + DOM contract the tests use |
| non-functional | yes | missing | — | P0: S25 Ultra viewport, load size, no trackers, works offline-ish |

## Missing or unverified

| Item | Effect on the flow |
|---|---|
| Blueprint (all sections) | P0 blueprint piece, EJ accepts before P2 builds |
| dsh not canaried | P1's first call doubles as the canary; failure blocks P1 → EJ |
| Firebase login | only if EJ picks Firebase (U3): EJ runs `! firebase login` |
| S25 Ultra viewport numbers | model knowledge (U5); P3 uses them, EJ's phone is the final check |
