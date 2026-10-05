# Why it is called "Ancient Games"

**Answer: EJ coined the name, in conversation, on 2026-09-06 at 13:26:32 (+08), about two hours after framing the
research that produced the framework. It is not from a book, a theorist, or an existing theory.**

## What it refers to

The name compresses the **two poles of the research brief** that fed the framework:

- **"Ancient"** = the ancient Chinese war-strategy corpus, named as 孫子兵法 (Sun Tzu's *Art of War*), plus
  "ancient texts" in the brief.
- **"Games"** = **game theory** (with complexity science and modern military strategy as the other two inputs).

The assistant at the naming moment said exactly this, verbatim:

> Good name — it captures the two poles that supplied the framework: 孫子兵法 on one side, game theory on the other.
> Let me record it in the framework's memory files.

It then did exactly that, **nine seconds later** — so a written record exists, not only a chat log
(`~/.claude/projects/-home-smoke01-dev-seza/memory/workflow-philosophy.md`, written 13:26:41, still on disk):

> **Name:** "The Ancient Games" (named by EJ, 2026-09-06). The two poles that supplied its principles:
> 孫子兵法 / ancient Chinese strategy on one side, game theory on the other, with modern military doctrine
> and complexity science in between.
>
> **Principle base:** 114 raw principles from a 4-agent research fan-out, deduplicated to 24 canonical rules.

## Sequence of events (all 2026-09-06, +08)

| Time | Who | Verbatim |
|---|---|---|
| 11:17:19 | EJ | "the next one will be go for a deep research about china war lessons or concept like 孫子兵法， see any rules , that we can use to enhance this parellel taks frameworks, we collect 100 of them first?" |
| 11:22:16 | EJ | "1. Game theory and complexity science + ancient texts + modern military strategy ; 2. A structured research document ; 3. use 4 research agents" |
| 13:20:42 | EJ | "ok I think we change another direction , you first deduplicate 80% similar concepts in the top 100 first" |
| 13:24:50 | EJ | "24 most are from who?" |
| **13:26:32** | **EJ** | **"let's name this new framework the ancient games"** |
| 13:26:37 | assistant | "Good name — it captures the two poles that supplied the framework: 孫子兵法 on one side, game theory on the other." |

The 100 concepts from Chinese war lessons had been clustered by domain just before the naming — game theory (5
clusters leading), complexity (5), modern military (4), ancient/孫子兵法 — so "ancient" and "games" were picked
straight off that table.

## Evidence

- `~/.claude/projects/-home-smoke01-dev-seza/a1db3155-9529-49c3-b157-9a385a8c7b55.jsonl` — the session where it
  happened (project `~/dev/seza`, before the repo moved to `~/dev/ancient-games`). Message index [1024] is EJ's
  naming line; [1027] is the assistant's reply; [1021] is the domain table.
- `~/.claude/projects/-home-smoke01-dev-seza/memory/workflow-philosophy.md` — the written record the assistant
  made nine seconds after the naming; its `originSessionId` is the same session. This is the cleanest evidence:
  it states the meaning, not just the name.
- `~/.claude/history.jsonl` — EJ's prompt history; the naming entry carries epoch `1788672392448`, and its
  neighbours carry `1788664936274` (the research brief).
- The name **predates the repository**: the first commit, `8b5a098` (2026-09-07), is already titled
  "Ancient Games v1: spine from V3_3_SPEC". `git log --all -S"Ancient Games"` finds no earlier commit, because
  the naming happened the day before the repo existed, in the `seza` project.

## CLAUDE.md does not know

Neither `CLAUDE.md` nor `AGENTS.md` explains the name — `CLAUDE.md` only says what the folder is for. There is no
global `~/.claude/CLAUDE.md` on this machine at all. The origin exists only in the conversation record above; no
document in the repo ever states it.

## Status

- Name origin: **documented** (conversation record), not inferred.
- The metaphor ("ancient" + "game") is **explained verbatim** by the assistant at the naming moment.
