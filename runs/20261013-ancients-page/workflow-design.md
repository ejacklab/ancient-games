# Workflow design — 20261013-ancients-page

A design, not a run. Sequential by default. Method: `docs/WORKFLOW_DESIGN_METHOD.md`. State: `state.md`.
Readiness: `readiness.md`.

## Questions for EJ (answer before running; a blueprint question holds back only the pieces that build on it)

| # | Question | Provisional assumption | Blueprint section |
|---|---|---|---|
| Q1 | Which lists go on the page? | **Opus lists** (`final-opus/`): web-researched, every quote found in the sources. agy's are the fallback | requirements |
| Q2 | What does each person show? | A short **"who they are"** + the **final list** (kind, rule, their words with gloss, source, label). Not the "changes" or "gaps" sections | requirements |
| Q3 | Where is it hosted? | **A Cloudflare Worker** serving the one HTML file, on the custom domain `ancients.ejai.ai`. The DNS is already on Cloudflare and the API works from here. The alternative is Firebase, like `ejai.ai`, which needs you to run `! firebase login` first | architecture |
| Q4 | Order of the people, and where the code lives | 范蠡 → 孫子 → 老子 → Linus. Code in `site/ancients/` in this (public) repo; the content is public anyway | requirements · architecture |
| Q5 | **Accept the blueprint** that P0 drafts (vision, R1–R6, N1–N3) | none: blueprint questions are not answered by silence | all |

You also give the go-ahead for two outward steps separately: the **preview URL** (P4) and the **live deploy** (P5).

## Restatement (method 3.0)

**Objective:** a public page at `https://ancients.ejai.ai` shows the four seats on EJ's Galaxy S25 Ultra. Swiping
left or right changes the person, scrolling up or down reads that person, and it looks and feels very close to a
Kindle page. The workflow can be rerun when the lists change. **In scope:** lists → content, page, mobile tests,
preview, deploy. **Out of scope:** the research itself, the rest of `ejai.ai`, a CMS. **Whys** (short): to read the
seats on the phone in a Kindle look · the lists exist today · EJ's own layout · fails on mangled quotes, a swipe that
fights Android's back gesture, or touching `ejai.ai` · stops when the subdomain is live and accepted · done = mobile
tests pass at S25 Ultra size, the live URL serves the tested file, EJ accepts on the phone. **Provisional
category:** information extraction → ui/ux dev → deploy (deploy has no TASK_TYPES row; first principles).

## Blueprint

- Kind of task: **new product**. Map: `site/ancients/docs/blueprint/README.md`, drafted by P0.
- Acceptance criteria in scope (proposed by P0, fixed when EJ accepts it):
  - **R1 Four people:** R1.1 four panels in the Q4 order; R1.2 each shows name, who they are and every item of its
    list with kind, rule, their words + gloss, source and label.
  - **R2 Sideways = person:** R2.1 a horizontal swipe moves to the next/previous person and snaps to it; R2.2 the
    current name and "n / 4" are visible; R2.3 tapping a name or dot jumps to that person.
  - **R3 Down = read:** R3.1 vertical scrolling never changes the person; R3.2 each person keeps its scroll place
    when you swipe away and back.
  - **R4 Kindle look:** R4.1 the `kindle-page` Aa menu (font, size, spacing, margins, alignment, white/sepia/green/
    black); R4.2 settings and the current person survive a reload; R4.3 nothing in a panel scrolls sideways (no text
    wider than the screen).
  - **R5 Exact quotes:** R5.1 every "their words" on the page equals the content file; R5.2 every Chinese quote passes
    the source check.
  - **R6 Rerun:** R6.1 one command rebuilds the page from the lists and runs the tests.
  - **N1** S25 Ultra size in Chrome for Android (CSS viewport ~412 × 915, DPR ~3.5 — model knowledge, U5);
    **N2** one HTML file, no trackers, no cookies, fonts from Google Fonts only; **N3** the deploy leaves `ejai.ai`
    unchanged (its homepage hash before = after).
- Baseline: `python3 site/ancients/tests/test_mobile.py` (created by P3). Its first run, against an empty page, is the
  red baseline in state.md.
- A piece that builds stops when its criteria pass, the baseline still passes and its "must not change" holds.
  Anything else goes to `site/ancients/docs/blueprint/backlog.md`.

## Pieces, in the order they run

Order: P0 → P3 → P1 → P2 → P4 → P5 → P6. The tests come before the content because the baseline (P3's red run)
must be recorded before the first piece that builds (design gate G10).

### P0 — Blueprint

- **Steps:** 1. Write vision from EJ's own words (this challenge, and "I really love to read using kindle…"). 2. Draft
  R1–R6 and N1–N3 as above, each through `requirement-check`. 3. Draft the short sections: domain (person, item, kind,
  label), data model (`content/ancients.json` schema), ui/ux (layout and the **DOM contract** the tests use:
  `[data-person]` panels, `#person-name`, `#person-pos`, `.item`, `.words`, `#menu`), architecture (one decision
  record: single static file + host per Q3).
- **Category:** multi step planning · **Pattern:** step · **Builds:** no (blueprint piece; proposes R1.1–R6.1, N1–N3)
- **Check:** EJ accepts (Q5) — kind: EJ · **Needs:** none
- **Contract:** returns `site/ancients/docs/blueprint/{README,vision,requirements,ui-ux,architecture,data-model}.md`;
  may change only those; must not change anything else.
- **Evidence:** the files + EJ's acceptance line, dated, in `state.md`.
- **Role and engine:** planner — COO herself (Opus 5.5, session effort): it is EJ's words plus a short draft, and a
  hand-off would not buy a check.

### P3 — Mobile tests, written before the page

- **Steps:** 1. Write `site/ancients/tests/test_mobile.py` (Playwright, S25 Ultra viewport, touch) from the
  criteria and the DOM contract only — one test per criterion id. 2. Run it against an empty page → all red (the
  baseline). 3. Run it against a planted-broken page (panels without snap; one quote altered) → the matching tests
  must fail.
- **Category:** test script gen · **Pattern:** step + sabotage · **Builds:** yes (tests only)
- **Covers:** R1.1–R5.1, N1 · **Check:** the two red runs above (script).
- **Needs:** P0 · **Contract — may change:** `site/ancients/tests/` · **must not change:** anything else.
- **Evidence:** both runs' output → `nodes/P3-red.txt`; screenshots go to `runs/20261013-ancients-page/shots/`.
- **Context — withheld:** the page code (it does not exist yet) — tests come from criteria, not from an implementation.
- **Role and engine:** tester — Codex `gpt-6.1-sol`, effort high, write, in a git worktree. A different engine from
  the builder (EXECUTOR_KINDS rule 5: tests are not written by the engine that writes the code).

### P1 — Content: lists → `ancients.json`

- **Steps:** 1. For each person, one call extracts *who they are* (from `identity/<seat>.md`) and every final-list
  item (from the Q1 lists) into the P0 schema, **copying every field verbatim** — no rewording. 2. Run
  `check_content.py`. 3. On a failure, feed the script's output back for that person only.
- **Category:** information extraction · **Pattern:** loop · **Builds:** yes (the page's data)
- **Blueprint sections:** data model, requirements (settled) · **Covers:** R1.2, R5.1, R5.2
- **Check:** script `site/ancients/tools/check_content.py`: schema valid; ≤ 20 items per person; every text field
  is a whitespace-normalised substring of its source `.md` (catches paraphrase); every Chinese quote found in
  `runs/20261013-four-seats/sources/` (the quote check from today). **Sabotage:** change one character in one quote →
  the check must fail.
- **Attempt limit:** 3 per person · **Feedback:** the check's failing lines · **Exit:** a fresh Codex node with a
  handoff note, limit 2; then EJ.
- **Needs:** P0 (schema) · **Contract — may change:** `site/ancients/content/`, `site/ancients/tools/check_content.py`
  · **must not change:** `runs/20261013-four-seats/**`
- **Evidence:** `check_content.py` output → `runs/20261013-ancients-page/nodes/P1-check.txt`
- **State:** reads Q1/Q2 answers; writes per-person item counts and pass/fail.
- **Role and engine:** extractor — `dsh` DeepSeek `deepseek-flash` (EJ's default for extraction), read-only on the
  lists, one call per person, sequential; the first call is dsh's canary. The check script is written by the COO.

### P2 — Build the page

- **Steps:** 1. `site/ancients/build.py`: `ancients.json` → `dist/index.html`, reusing the `kindle-page` template's
  themes, fonts, Aa menu and settings memory. 2. Layout: a horizontal scroll-snap row of four full-screen panels,
  each scrolling vertically on its own; a quiet header with the person's name and "n / 4", dots to jump; a Kindle
  footer per person (% read, minutes left). Swipes start away from the screen's edges so Android's back gesture is
  not triggered (U4). 3. Run P3's tests; repair until green.
- **Category:** ui/ux dev · **Pattern:** loop · **Builds:** yes
- **Blueprint sections:** ui/ux, data model, non-functional, architecture (settled) · **Covers:** R1–R4, R6.1, N1, N2
- **Check:** `python3 site/ancients/tests/test_mobile.py` all green + `build.py` exits 0 — script.
- **Attempt limit:** 3 · **Feedback:** the failing tests' output · **Exit:** a fresh Codex node (high), limit 2; then
  EJ.
- **Needs:** P0, P1, P3 · **Contract — may change:** `site/ancients/build.py`, `site/ancients/templates/`,
  `site/ancients/dist/`, `site/ancients/Makefile` · **must not change:** `tests/`, `content/`, `~/skills/kindle-page`
  (copy what it needs).
- **Evidence:** test output + `sha256sum dist/index.html` → `nodes/P2-<attempt>.txt`.
- **Role and engine:** builder — opencode `minimax-coding-plan/MiniMax-M3.1-Flash-Preview`, `--agent build`, in a git
  worktree (EXECUTOR_KINDS: strongest measured frontend results here; opencode priority for build work).

### P4 — Review and preview on the phone

- **Steps:** 1. A blind fixed-checklist review of `dist/index.html` + the P3 screenshots against `ui-ux.md` (Kindle
  look, readability, the sideways/vertical split), with one **planted defect** it must find. 2. With EJ's go-ahead,
  publish to a preview Worker on `*.workers.dev`. 3. EJ checks on the S25 Ultra, especially the edge-back gesture (U4).
- **Category:** code review + human acceptance · **Pattern:** step · **Builds:** no
- **Check:** reviewer finds the planted defect (else its review is void); EJ accepts on the phone — kind: checklist +
  EJ. Findings outside the criteria go to `backlog.md`; a criterion failure sends P2 back for one attempt.
- **Needs:** P2 · **Context — withheld:** P2's reasoning and attempt history.
- **Evidence:** review file `nodes/P4-review.md`; preview URL and EJ's verdict in `state.md`.
- **Role and engine:** reviewer — Claude subagent, Sonnet 5.5 (a different kind from opencode); preview publish by
  the COO through the Cloudflare API.

### P5 — Deploy to `ancients.ejai.ai`

- **Steps:** 1. Record `ejai.ai`'s homepage hash (N3). 2. Per Q3: create Worker `ancients` serving the tested
  `dist/index.html` and attach the custom domain `ancients.ejai.ai`. 3. Check: the live file's sha256 equals P2's;
  `test_mobile.py` passes against the live URL; `ejai.ai`'s hash is unchanged.
- **Category:** deploy (no row — first principles) · **Pattern:** step · **Builds:** yes (configuration)
- **Covers:** N2, N3 · **Check:** the three checks in step 3 — script. **Attempt limit:** 1; on a failure, remove the
  custom domain (one API call) and report.
- **Needs:** P4 accepted + EJ's explicit go (Rule 6: outward-facing).
- **Contract — must not change:** anything on `ejai.ai` or any other Cloudflare zone record.
- **Evidence:** API responses (ids only), the hashes and the live test output → `nodes/P5-deploy.txt`.
- **Role and engine:** deployer — COO herself via the Cloudflare MCP (only she has that tool).

### P6 — Close

- **Steps:** 1. `site/ancients/README.md`: the one rerun command (`make` = build + check content + tests) and how
  to deploy. 2. Blueprint `decisions.md` / `changelog.md` entries. 3. Ledger row in `docs/TASK_TYPES_LEDGER.md`.
- **Role and engine:** COO. **Check:** the rerun command works from a clean checkout (script).

## Joins

P1 + P3 meet at P2: if the tests' idea of the data (from the schema) and the content file disagree, it is a stop —
fix the schema in P0 with EJ, never patch one side.

## Parallel candidates (decided last)

| Pieces | Needs other's result | Shared files | Changes the other | Own check | Worth the join |
|---|---|---|---|---|---|
| P1 ∥ P3 | no | no (content/ vs tests/) | no | yes | small: different engines (dsh, Codex), saves one engine call's clock time |

All five hold, but the saving is small, so **the default stays sequential** (P3 then P1). Unit if run together: two
engine processes alive.

## Predictability

- Design gate: `design_gate.py runs/20261013-ancients-page/design.json` → PASS (2026-10-13), after fixing 8
  findings (empty context fields, no loop on P3, no baseline command).

- Design source: default ⟨information extraction · test script gen · ui/ux dev⟩; deploy from first principles.
  Ledger row reconciled at the end.
- Engine calls: P1 4 (+ up to 3 repairs each) · P3 1–2 · P2 1–3 · P4 1 · P5/P6 by the COO. About 8–14 calls.
- Cost estimate (model knowledge, not measured): dsh ~100k tokens (cheap tier) · Codex ~100–200k · opencode
  ~100–300k · Sonnet ~50k · COO ~150k. Clock: 1–2 hours plus EJ's phone check.
- Success criteria, written before the run: R1.1–R6.1, N1–N3.

## Debuggability

- Labels P0–P6; every node's evidence in `runs/20261013-ancients-page/nodes/`, screenshots in `shots/`.
- Resume from `state.md`: each node is rerunnable alone (`build.py`, `check_content.py`, `test_mobile.py` are plain
  scripts).

## Quality control

- Scripts: `check_content.py` (P1), `test_mobile.py` (P2, P5), sha256 + homepage hash (P5). Judged: P4 checklist.
  EJ: P0 acceptance, P4 phone check, P5 go-ahead.
- Sabotage: one altered quote (P1, P3), panels without snap (P3), a planted UI defect (P4).
- The final "what is missing" pass is P4's checklist against the three-part stop; anything else goes to the backlog.
- Predictability, debuggability and quality control are all shown above.
