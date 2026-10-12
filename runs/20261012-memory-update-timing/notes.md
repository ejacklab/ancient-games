# What to update immediately, and what at the end of a task or in the background — notes

Recorded 2026-10-12 at EJ's request ("go research what need to immediately update, what can be updated at end of a task").
Question: when should a memory entry be written or updated — right away, or later?
Method: read the project's own earlier research. **No new web research was done for this note.**

## Sources and how they were read

| Source | How read |
|---|---|
| `docs/research/20261011-agent-memory-graph-r2/FINDINGS-s1-architectures.md` (F9, F10, F13) | Lines read directly. Each finding is marked `verified` there with a verbatim quote and a URL. I did not open the URLs. |
| `docs/research/20261011-agent-memory-graph-r2/FINDINGS-s4-retrieval-consolidation.md` (F3, F11, F13, F17) | Same. |
| `runs/20261011-project-memory-engines/RECOMMENDATION.md` (M24, CP7, Write rules, Staleness and contradiction, "What NOT to build") | Lines read directly. |

## What the sources say

**Fast path now, slow path later.** MAGMA's write path: "It decouples latency-sensitive operations via Synaptic Ingestion
(Fast Path) from compute-intensive reasoning via Asynchronous Consolidation (Slow Path)"; and "no blocking LLM reasoning
occurs here, ensuring the agent remains responsive regardless of memory size" (s1-F13; https://ar5iv.labs.arxiv.org/html/2601.03236).

**Background subagents.** Letta: "Dreaming uses background subagents to review recent conversations, consolidate useful
lessons, and update memory without interrupting your active work." It is triggered "after a set number of completed agent
steps or when the context window is compacted" (s1-F9; https://docs.letta.com/configuration/memory.md).

**A separate agent edits memory.** Letta's sleep-time agents: "the primary agent is not provided with tools to edit its core
memory… These tools are attached to the sleep-time agent" (s1-F10; https://www.letta.com/blog/sleep-time-compute/).

**Raw capture is cheap.** "Raw turns cost 3,061× less to write"; raw turns written with no LLM call were non-inferior to an
extraction memory at a tight budget, and extraction wins only at generous budgets (s4-F17; https://arxiv.org/html/2609.34227v1).

**Flag now, recompute later.** AkasicMEM flags affected memories stale at once and "only flags the potentially affected
downstream memories… without eager recomputation"; only retrieval recomputes them (s4-F3; https://arxiv.org/html/2609.25563v1).

**The project's own source.**
- Write rules, triggers: a decision whose reason is not visible in code; a non-obvious constraint or pitfall that cost more
  than one attempt; a human correction; "a checkpoint of unfinished work before a handoff, interruption or context reduction".
- Write rules, when: "at discovery or correction, or at task end… Not every turn; not as a standing per-session obligation (CP7)".
  M24 and CP7 are **CONTESTED** (opencode: session end is a standing write trigger); the basis for M24 is `model knowledge` in
  both claude and codex.
- Staleness and contradiction, consolidation: "periodic, off the critical path, as a proposed PR — merge duplicates, retire
  dead entries, shrink the index — never a silent rewrite."
- "What NOT to build": LLM-chosen ADD/UPDATE/DELETE, or auto-extraction of facts from every turn, is refused (claude; destructive,
  not diff-reviewable).

## My reading — not in the sources

Applied to EJ's kinds and his rule that the source of truth comes first:

| When | What |
|---|---|
| **Immediately** | Decisions and facts (they come before the code). Anything lost if the session died: a human correction, and the state of unfinished work before a handoff, an interruption or context reduction. |
| **End of task, or in a background subagent** | Lessons, observations, hypotheses; merging duplicates; reconciling entries with the code; regenerating `INDEX.md`; runbooks. |

## Not found

- No source compares writing immediately against writing at task end for coding agents. The only direct statement (M24) is
  `model knowledge` and contested.
- The Letta and MAGMA evidence is about chat-style agent memory, not project memory in a repo.
- Whether a background subagent should be allowed to rewrite decisions and facts, or only flag them, is **not decided** (EJ was asked).

## Not checked

- None of the URLs above were opened for this note.
- Claude Code's own mechanism for background work (e.g. subagents run in the background) was not looked up for this purpose.
