# Relay — one official set of research trust tags (2026-10-13)

**Where the idea came from:** the relay idea (experts take turns improving one copy, compared with answering in parallel) is from a post EJ read on X, not EJ's own finding (EJ, 2026-10-13). Author and link not recorded.

Asked by EJ: *"start with linux then pass to another expert, let's all 5 of them take turn improve the same copy.
let's see the end will it be better than the 范蠡's version"*.

## Design
- Order: Linus (codex) → 范蠡 (agy; Claude if agy fails) → 孫子 (dsh) → 老子 (opencode) → Dave (Claude subagent).
  The skill's table order; chosen by the main agent, EJ named only the first.
- Every step gets the same `facts.md` as the parallel run `runs/20261013-four-experts-question-this-repo-has-several/`
  (no new facts, so the comparison is fair), plus the current copy with earlier authors' names removed.
- Each step returns the complete copy under `### The copy`, not a diff, and lists kept / changed / added / removed.
- Step folders: `step-<n>-<id>/` (the skill's normal run folder). `copy-<n>.md` = the copy after step n.

## How "better" is judged — written before step 1 ran
Compared: `copy-5.md` (relay end) vs 范蠡's parallel proposal (`.../answers/fan-li.md`, Answer section).
One blind judge: a fresh Claude subagent (Sonnet), not told who wrote which, order A/B by coin flip recorded here
after the verdict. Note: Claude also runs Dave (and 范蠡 on fallback), so the judge is not a different kind from every
author — stated, not fixed.
The judge applies each version to five cases and reports, per case, the tag(s) it gives and whether a careful
researcher could read the definitions two ways:
1. A vendor blog says "our system is 60% faster"; no benchmark shown.
2. A paper's own reported benchmark numbers, read in the paper (the case that got `verified` in one section and
   `reported` in another in run 2).
3. A claim found only in someone's blog post about a paper; the paper was not read.
4. A search for a named system that returned nothing.
5. A conclusion drawn from two other findings.
Then: (a) does each tag measure one thing; (b) how many files change; (c) anything left ambiguous.
Verdict: A better / B better / no real difference — with the case numbers that decide it. The judge's verdict is
advice; EJ decides.

## Known differences from the parallel run (stated before the result)
- The relay is told not to search the web; the parallel experts could (范蠡 and Dave did, as Claude). The relay
  works from `facts.md` and the copy only. Reason: the question is a synthesis over the repo's own facts; the main
  web finding (Admiralty code: grade source and information separately) is already in the copy from step 2 on only
  if an expert brings it from knowledge.
- 范蠡's parallel answer ran on Claude (`--needs-web`); in the relay 范蠡 runs on agy unless it fails.
