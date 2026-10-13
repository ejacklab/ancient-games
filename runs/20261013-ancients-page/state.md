# State — 20261013-ancients-page

Rules: one writer at a time. Read this file before your step; update it after. It holds progress and results only —
never reasoning; put notes in your own output file. Never delete a log line.

## Challenge (verbatim)

> you design a workflow that help create a page that display these 4 person details a single page ancients.ejai.ai .
> I use to view on my mobile phone S25 Ultra, and make it very near kindle page , and I am able to scroll left and
> right to change person details , and up and down to read.

## Restatement (method 3.0)

**Objective:** one public page at `https://ancients.ejai.ai` shows the four seats — 范蠡, 孫子, 老子, Linus Torvalds —
read on EJ's Galaxy S25 Ultra: swipe left/right changes person, scroll up/down reads that person, and it looks and
feels very close to a Kindle page (colour, spacing, font size, font). The workflow that produces it can be rerun when
the lists change. **In scope:** turning the final lists into page content, the page, mobile tests, a preview, the
deploy to the subdomain. **Out of scope:** changing the research itself, the rest of `ejai.ai`, other devices beyond
"works on a normal phone browser", a CMS or editing UI.

Six whys: (1) EJ reads on the phone and loves the Kindle look — a page to *read* the seats, not a dashboard;
(2) the four final lists exist as of today; (3) a single page with sideways people / downward reading — EJ's own
shape, taken as given; (4) fails if quotes are mangled on the way (the whole run was about faithful quotes), if a
sideways swipe fights Android's edge-back gesture, or if the deploy touches `ejai.ai` itself; (5) stops at the
subdomain going live with EJ's acceptance; (6) done = mobile test script passes at S25 Ultra size, the live URL serves
the tested file, and EJ accepts it on the phone.

Provisional category (inferred): information extraction → ui/ux dev → deploy (deploy has no row: "ship and operate" is
out of focus in TASK_TYPES; it gets first principles here).

## Baseline

`git status --short` before this run folder: see the session's opening snapshot (many untracked runs/ folders; none
under `runs/20261013-ancients-page/` or `site/`).

## Product baseline

New product — no test command exists yet. P3 creates it (`site/ancients/tests/`); its first run, against the empty
page, is recorded here as the red baseline.

## Steps

| # | Step | Status | Output file |
|---|---|---|---|
| 1 | Intake, readiness and blueprint check | done | readiness.md |
| 2 | Algorithm and unclear spots | done | workflow-design.md |
| 3 | Size decision | done | (below) |
| 4 | Workflow design | done | workflow-design.md |
| 5 | EJ answers questions, accepts blueprint | doing — Q1–Q4 defaults taken (EJ: "ok let's execute"); P0 drafted, awaiting EJ's acceptance | site/ancients/docs/blueprint/ |
| 6 | Run P1–P6 | todo | nodes/ |

## Blueprint

Kind of task: **new product** (a public web page). Map: none yet — P0 drafts `site/ancients/docs/blueprint/`.
Needed sections not settled: vision, requirements, ui/ux, non-functional: **missing**; architecture: **missing**
(one decision record: host); domain, business logic, data model: missing, one paragraph each for this slice.

## Size decision

design — steps: 11, unclear spots: 5, risk: **high** (public URL on EJ's domain; quotes must stay exact).

## Unclear spots

| Id | What is unclear | Kind | Blueprint section | Blocks | Depends on |
|---|---|---|---|---|---|
| U1 | Which lists go on the page: Opus, agy, or both merged | decision | requirements | P1 | — |
| U2 | What each person shows beyond the final list (a "who they are", the Gaps) | decision | requirements | P1 | U1 |
| U3 | Host: Cloudflare Worker + custom domain, or Firebase like `ejai.ai` | decision | architecture | P5 | — |
| U4 | Whether a left/right swipe in the page collides with Android's edge-back gesture on the S25 Ultra | unknown | ui/ux | P4 acceptance | P2 |
| U5 | S25 Ultra CSS viewport (model knowledge: ~412 × 915, DPR ≈ 3.5) | information | non-functional | P3 numbers | — |

## Questions for EJ (one batch)

See workflow-design.md, top.

## Log (append only)

- 2026-10-13 step 1 done: readiness — Cloudflare API works as EJ; ejai.ai DNS on Cloudflare, site on Firebase; ancients.ejai.ai NXDOMAIN; firebase CLI not logged in; opencode/codex/dsh/playwright present.
- 2026-10-13 step 2–4 done: design written; 5 unclear spots; 5 questions for EJ.
- 2026-10-13 design gate PASS after 8 findings fixed; P3 moved before P1 (baseline before first builder, G10).
- 2026-10-13 run started (EJ: "ok let's execute the workflow"); Q1–Q4 on their defaults.
- 2026-10-13 P0 done (draft): blueprint drafted in site/ancients/docs/blueprint/; waiting for EJ's acceptance (Q5) — P3 onward do not start until then.
- 2026-10-13 design changes for EJ's one-hour target: P1 by a parser script (verbatim by construction) instead of dsh; P3 ∥ P2 (two engine processes alive); no git worktrees (site/ancients is untracked, a worktree would not contain it) — each engine limited to its own paths by brief.
- 2026-10-13 P1 done: extract_content.py + check_content.py → PASS 4 persons, 76 items (18/20/19/19); sabotage (one altered character) caught. Evidence nodes/P1-check.txt. Opus-fetched sources copied into runs/20261013-four-seats/sources/<seat>/extra/.
- 2026-10-13 P3 done: Codex wrote tests/test_mobile.py (14 checks: R1.1–R5.1, N2); Chromium cannot launch in Codex's sandbox (reported, not faked); COO ran the red baseline: 0/14, every test failing with a real reason. Evidence nodes/P3-red.txt.
- 2026-10-13 P2 attempt 1 blocked (executor failure, not counted): opencode auto-rejected reading ~/skills (external_directory), exit 0 with no work; template copied to site/ancients/templates/kindle-reference.html; attempt 2 running.
- 2026-10-13 P5 prep: before-snapshot saved (nodes/P5-before.txt): ejai.ai sha256 9a61057f…, 7 DNS records, workers: neurosync.
- 2026-10-13 P4 verdict: reviewer (Sonnet, blind) found the planted defect (green theme button removed from review/index.html; real dist unchanged) → review valid. Real finding: #aa flush to the right screen edge (right:-.9rem), tap targets 26–34 px. Fixed by COO. Other findings to backlog.
- 2026-10-13 P5 preview: wrangler login (EJ approved OAuth); deployed to ancients.hojipago.workers.dev; sha256 = dist; test N2 fixed (the document URL itself is not a request the page makes); preview 14/14 ×2; R1.2 "panel count=0" seen once, not repeated. Evidence nodes/P5-preview.txt.
- 2026-10-13 P5 live: deployed with --domain ancients.ejai.ai on EJ's command; live sha256 = dist; ejai.ai hash and the 7 DNS records unchanged (one AAAA added for ancients). Tests 13/14 — N2 FAIL: Cloudflare Web Analytics (zone-wide auto-install) injects its beacon. Waiting for EJ's decision. Evidence nodes/P5-deploy.txt.
- 2026-10-13 D1: EJ "Cloudflare analytics on ancients.ejai.ai can keep" → N2 widened, test updated; live 14/14, local 14/14; sabotage (example.com request) → N2 FAIL. Evidence nodes/P5-deploy.txt.
- 2026-10-13 P6 done: site/ancients/README.md (rebuild + deploy commands), blueprint decisions.md D1 + changelog, ledger row. `make -C site/ancients` rerun after the N2 change: content PASS 76, build 156,910 bytes, 14/14. Open: EJ's own S25 check of the Android edge-back gesture (U4) not yet reported.
- 2026-10-13 U4 closed: EJ checked on the S25 Ultra — "swipe works fine, no back gesture". The run's acceptance is complete.
