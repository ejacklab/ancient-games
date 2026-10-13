# Four seats on "how should an AI agent role-play a person to solve a problem?" — synthesis

Written by Claude (main session), 2026-10-13. Inputs: `out/{fan-li,sun-tzu,lao-tzu,linus}.md`, brief `briefs/common.md`.

| Seat | Engine | Web | Findings | Read |
|---|---|---|---|---|
| 范蠡 | opencode, MiniMax M3.1 Flash, plan mode | yes | 20 | abstracts / metadata only |
| 孫子 | Claude subagent, Opus 5.5 | yes | 18 | abstracts only |
| 老子 | agy, gemini-3.8-flash-medium | **no** (headless denies fetch) | 7 | from memory |
| Linus | Codex, gpt-6.1-sol, `--search`, read-only | yes | 8 | **full texts** (ACL PDFs, arXiv HTML, W3C) |

## Checks I ran (main session — my checks, not independent)

- **All 36 cited arXiv ids exist** and their real titles fit the claims (`out/arxiv-titles.txt`, arXiv API). Existence
  only — not that each claim matches the paper.
- **Spot-check of claims against abstracts** (arXiv API summaries):
  - 老子 #1 says Kong et al. 2308.07702 found role prompts "inconsistent… often no better" — **wrong**: the abstract says
    role-play prompting "consistently surpasses the standard zero-shot approach across most datasets" (AQuA 53.5→63.8%).
    孫子 and Linus report it correctly.
  - 老子 #5 cites Perez et al. 2212.09251 for "persona prompting… increasing hallucination rates and invented
    citations" — **not supported**: the abstract is about model-written evaluations, sycophancy and inverse scaling.
  - 老子 #7 cites promptingguide.ai for a specific claim, from memory — not checkable as stated.
  - 范蠡 #10 (Upworthy: no-persona τ 0.361 / top-1 49.2% vs persona panel τ 0.084 / 34.6%), #11 (PersonaGym: GPT-4.1 same
    score as LLaMA-3-8b), #14 (Consilium: persona not model determines behaviour) — **match** their abstracts.
- Lesson (n=1): the no-web seat produced the two wrong citations. A research role needs an engine that can fetch.

## Where all four agree (independent engines, same brief)

1. **A persona label alone does not make answers more accurate, and can make them worse.** Measured: Zheng et al.
   2311.10054 (162 roles, no gain), Wharton 2512.05858 (expert personas no gain on GPQA/MMLU-Pro), Gupta et al.
   2311.04892 (bias in 80% of personas on GPT-3.5), Upworthy 2609.25010 (no-persona beat a persona panel at predicting
   real clicks).
2. **What helps is structure, not voice:** a designed role prompt (Kong 2308.07702), itemised rules/playbooks (ACE
   2510.04618), explicit reasoning rules (2404.17218). → For the seats: **apply the numbered rules as instructions and
   cite them per step; the person's style adds nothing.**
3. **The known failures:** style copied instead of mind (Ran 2406.18921), invented quotes / anachronism (TimeChara
   2405.18027), instruction drift within ~8 turns (Li 2402.10962 — re-read the list each step).
4. **Several personas debating: mixed.** Debate can help (Du 2305.14325), but voting explains most of the gain (Choi
   2508.17536), and diversity of *models* matters (ReConcile 2309.13007). → Agreement of four personas on **one**
   model counts as about one vote; four different engines is closer to real diversity. *my reading*
5. **Nobody has measured EJ's design** — deciding through a real person's quoted rules versus a plain answer. All four
   say `not measured`. Linus and 范蠡 propose the same test: plain prompt vs rules-only vs rules+identity, same facts,
   reviewers blind to the condition, judged on unsupported claims and correct rule use.

## The example — "what colour should a landing page be?"

- **No seat named a hue as *the* answer.** 孫子 and 范蠡 refused outright; 老子 and Linus gave a conditional default
  (light neutral / white background, dark text) marked as a starting point, not measured.
- **Common answer:** (1) settle what needs no visitors first — text contrast (WCAG 2.2 AA 4.5:1 normal text, 3:1 large;
  Linus fetched the W3C page); (2) base = the brand palette on a readable neutral; (3) **one accent colour, used only
  for the one main action** (孫子 正/奇, 老子 frugality, 范蠡 盈而不溢); (4) if it matters, a pre-registered A/B test of the
  accent only, with the metric, minimum lift, sample size and stop date fixed before; 孫子 adds an A/A run first.
- **Same questions back from all four:** whose page/brand, the one action, who visits and on what device, existing
  page and its traffic.
- **Colour research:** 范蠡 found Labrecque & Milne 2012 (colour → perceived brand personality) and no study of colour
  → conversion; 孫子 found none either. So "blue = trust" is a hypothesis, not a rule.
- 孫子 and 范蠡 both said colour is likely the lowest lever: test offer and headline first.

## Open for EJ (from Linus's requirement check)

"More logical and checkable than a plain AI answer" has no measure yet: what observable result counts as "more
logical", what as "more checkable", and what improvement over the plain answer would justify using a seat?
