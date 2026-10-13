# Relay result — relay copy vs 范蠡's parallel version (2026-10-13)

**Where the idea came from:** the relay idea (experts take turns improving one copy, compared with answering in parallel) is from a post EJ read on X, not EJ's own finding (EJ, 2026-10-13). Author and link not recorded.

Recorded by the main agent (Claude). Plan, written before step 1: `plan.md`.

## Verdict (quoted, blind judge — Claude Sonnet subagent, read only `judge/A.md` and `judge/B.md`)

**"B better."** Mapping revealed after the verdict (`judge/mapping.txt`): **A = 范蠡's parallel version, B = the relay's
final copy (`copy-5.md`).** So the relay copy won.

Deciding points, quoted from the judge:
- Case 2 (a paper's own benchmark numbers — the case that went two ways in the real run 2): "B settles it as
  `verified`, scoped to the paper's own conditions. A moves the split from `verified`/`reported` to `verified`/`unproven`."
- Case 5 (a conclusion drawn from two findings): "B states plainly that an inference is untagged prose and inherits
  nothing. A is mildly self-contradictory."
- Tag purity: "A mixes access and content across `reported`/`verified`/`unproven`."
- Against B: "case 3 is ambiguous in B but clear in A, and B is roughly twice as long, with a heavy adoption gate."
- Cases 1 and 4: tie.

## What the relay changed, step by step (from each step's answer)

| Step | Expert (engine) | Main change |
|---|---|---|
| 1 | Linus (codex) | first copy: four lower-case tags with tighter definitions; split "the source says X" from "X holds"; INFERRED/GAP become prose; one new file `docs/RESEARCH_TAGS.md` |
| 2 | 范蠡 (agy) | "never upgrade a label in place" moved into the main rules; no definition change on n=1 (also turned paths into `file://` links) |
| 3 | 孫子 (dsh) | every tag measures one thing — the evidence in hand; primary/secondary relative to the exact claim; a re-tag of the accepted run as the adoption test; restored the paper-benchmark example |
| 4 | 老子 (opencode) | the ladder became four parallel answers; a `verified` row must show what was inspected; dropped two examples |
| 5 | Dave (Claude) | the re-tag became a blind experiment with a control pass; `unknown` narrowed (no "could not obtain"); the contradiction case; TASK_TYPES `|` parse warning |

## Limits (my reading)

- n=1: one relay, one judge, five cases I wrote.
- The judge is Claude (Sonnet); Dave and two 范蠡 runs were Claude too. Not a different kind from every author.
- Not a fair fight on information: the relay had five passes and the parallel 范蠡 had one; the relay had no web, 范蠡
  had web. The relay copy is ~4× longer; the judge was told length is a cost.
- The case list was written before the relay ran (`plan.md`); the judge's wording of each case is mine.
- Open in the winner (quoted): case 3 — "a secondary source that cites a paper sits on the `reported`/`unproven`
  boundary"; and it is silent on `research-agent-memory.js` and the skills export, which hold copies of the definitions.

## Adopted (2026-10-13)

EJ: *"fix case 3 then adopt the relay version"*. The main agent fixed case 3 in `copy-6-case3.md` over three blind
Sonnet checks (round 1: two boundary cases; round 2: four; round 3: 9 of 10 clean, the tenth closed by wording not
re-checked). The fix changed `reported` to "a locator for the source, not yet inspected". Adopted as
`docs/RESEARCH_TAGS.md`; the re-tag with a control in that file is the check still owed.
