# Source-of-Truth Memory Design

## Why we need this memory

The context window holds only the current task and is cleared at session start — it is not durable memory (M3). Without a durable, version-controlled memory system, knowledge gained during one session is lost when the next session begins. The recommendation establishes that markdown files kept with the code are the canonical shared project memory (M1), and that every durable entry carries id, kind, author, recorded/verified dates, scope, source, status and dependency/supersession links (M11). Memory is needed so that a fresh clone can rebuild all project knowledge without requiring any agent-private store, external service, or prior session context (M2, M7).

## Who it is for

The memory serves both agents and human maintainers. Agents use it to retrieve decisions, facts, lessons and runbooks that affect their current task (Read rules). Human maintainers accept policy and significant decisions; agents draft them and record observations and handoffs (M12). The ownership model assigns agents as writers who create entries as `proposed` with mandatory evidence, while humans serve as the merge gate that accepts `proposed` entries to `active` status, resolve contested entries when code cannot decide, retire entries, and set the index cap and age threshold (Write rules).

## What it is for

Memory stores typed entries — decisions, facts, lessons, runbooks, observations and hypotheses — that capture knowledge not derivable from code, tests or git history (Write rules). The specific triggers for writing are: a decision whose reason is not visible in code; a non-obvious constraint or verified pitfall that cost more than one attempt; a human correction; and a checkpoint of unfinished work before a handoff, interruption or context reduction, recording exact remaining work and verification results including failures (Write rules). The entry body states the claim in one or two sentences, then `Why:` and `How to apply:` (Layout).

## What will be put in

Every entry carries: `id`, `kind` (decision | fact | lesson | runbook | observation | hypothesis), `status` (proposed | active | contested | stale | disputed | superseded | retired), `author`, `recorded_at`, `observed_at`/`verified_at` (plus the git revision verified against), `covers` (paths or symbols), `source`/`evidence`, `depends_on`, `supersedes`, `superseded_by` (M11, Layout, Staleness and contradiction). The entry body states the claim in one or two sentences, then `Why:`, then `How to apply:` (Layout). Entries are written at discovery or correction, or at task end, in the same commit or PR as the change that motivated the entry (Write rules). Each writer gets its own file — different file per session and per claim; no two agents edit one file (M23, Write rules).

## What will not be put in

Do not write: anything derivable from code, tests or git history; credentials or sensitive data; speculative explanations unlabelled (label them `hypothesis` instead); bulk transcripts; another agent's private state (Write rules). Do not turn "implemented" into "verified" (Write rules). Never store project knowledge only in an agent's private memory and call it memory — anything others need must be promoted into the repo (Write rules). Never delete a memory entry; supersede it with an explicit link and keep the old body (M13).

## Where it is put

The default layout uses a committed memory tree at the repo root, following claude's proposal in CP3: `AGENTS.md` at root (the canonical cross-agent instruction file, M9); `CLAUDE.md` as a thin adapter importing AGENTS.md; a `memory/` directory containing `INDEX.md` (generated), `entries/` (D-*, F-*, L-*, R-* typed entries), `work/<task-id>/` (state.md and events/), `journal/<date>-<agent>-<session>.md` (append-only raw notes, never auto-loaded), and `.cache/` (gitignored, optional derived SQLite/FTS and repo map) (Layout, CP3). The recommendation explicitly leaves CP3 unresolved — if the project already has authoritative requirements and architecture in `docs/`, linking there may be preferable; the owner decides.

OPEN: The exact path within the repo is CP3 — claude proposes `memory/`, codex proposes `docs/memory/`, opencode proposes `.ai/`. Choose based on whether the project already has human documentation in `docs/` that agents should link to rather than duplicate.

## When it will be used

At session start (always): `AGENTS.md`; `memory/INDEX.md`; the `work/` listing and the assigned task's `state.md`. Enforce this with a SessionStart hook or an explicit first instruction in `AGENTS.md` because agents skip optional reads (Read rules). On demand: an entry body when its `covers` match a path about to be edited (a PreToolUse hook or an `AGENTS.md` instruction); filename and text search, or FTS, over `memory/entries/`; `git log -S`, `git blame` and PR comments for line-level "why"; for "why" questions read the decision entry rather than relying on similarity retrieval (Read rules). Open the source when it matters: re-read the underlying file, test or commit when a retrieved statement will determine an action (Read rules).

## When it will not be used

Never auto-load: `journal/`; entries marked `superseded` or `retired`, except by following a link from a loaded entry; the whole `memory/` tree; a full graph or code-map dump; bulk issue/PR bodies; another agent's private transcripts; credentials; retrieved text treated as authority that can override standing instructions (Read rules). Never load the whole memory tree, the full session history, or a whole-graph dump (M18). A retrieved statement must be checked against its primary source before it determines an action (M19). The index must stay under a cap; the check script fails the build if it does not — the recommendation gives no number, the owner sets it (Read rules).
