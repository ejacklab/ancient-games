# Claude Code's built-in memory for subagents — notes

Recorded 2026-10-12 at EJ's request ("no need reinvent we can just record it and use it"), in the folder EJ agreed to.
Question: does Claude Code already give each agent name its own memory, with a config and an index?
Answer: **yes**. Everything below is from the two pages named here; nothing is from memory of mine.

## Sources and how they were read

| Page | How read |
|---|---|
| https://code.claude.com/docs/en/sub-agents (section "Enable persistent memory", "Persistent memory tips", frontmatter reference) | **Through `WebFetch`, i.e. a summary written by a small model.** Its quotes are second-hand. The last 8,547 of 108,547 characters were **not read**. |
| https://code.claude.com/docs/en/memory (section "Auto memory") | `WebFetch` output was saved to disk and the relevant lines (31, 36, 512–556) were read in the saved text. Those quotes are first-hand. |

## What the docs say

**Config = one frontmatter field in the agent's own markdown file** (sub-agents, frontmatter reference):
`memory | No | Persistent memory scope: user, project, or local. Enables cross-session learning.`
There is no separate config file.

**Purpose** (sub-agents): "The `memory` field gives the subagent a persistent directory that survives across
conversations. The subagent uses this directory to build up knowledge over time, such as codebase patterns, debugging
insights, and architectural decisions."

**Folder per agent, by scope** (sub-agents, table):

| Scope | Directory | Use when |
|---|---|---|
| `user` | `~/.claude/agent-memory/<name-of-agent>/` | the subagent should remember learnings across all projects |
| `project` | `.claude/agent-memory/<name-of-agent>/` | the knowledge is project-specific and shareable via version control |
| `local` | `.claude/agent-memory-local/<name-of-agent>/` | project-specific but not checked into version control |

**Index file** (sub-agents): "The subagent's system prompt also includes the first 200 lines or 25KB of `MEMORY.md` in
the memory directory, whichever comes first, with instructions to curate `MEMORY.md` if it exceeds that limit."
Memory page, first-hand (line 538): "`MEMORY.md` acts as an index of the memory directory." Line 532: "Index, one line per
memory, loaded into every session." Line 552: topic files "are not loaded at startup. Claude reads them on demand."
Line 548: after a write, Claude Code measures `MEMORY.md` against the 200-line / 25KB limits and reminds Claude to
shorten it — "keep one line per entry, move detail into topic files, and merge or drop stale entries".

**Tools** (sub-agents): "Read, Write, and Edit tools are automatically enabled so the subagent can manage its memory files."

**System prompt** (sub-agents): "The subagent's system prompt includes instructions for reading and writing to the memory directory."

**No leakage from the main session** (memory page, line 554): the main conversation's auto memory is not loaded into
subagents; the exception is a fork, which inherits the parent conversation and system prompt.

**Switch** (sub-agents): subagent memory is part of auto memory. If auto memory is turned off (`autoMemoryEnabled`
setting or `CLAUDE_CODE_DISABLE_AUTO_MEMORY`), the `memory` field has no effect.

**Tips** (sub-agents, "Persistent memory tips"): `project` is the recommended default scope. Ask the agent to check its
memory before work and to save what it learned after. Put memory instructions in the agent's markdown file; the doc's
example text: "Update your agent memory as you discover codepaths, patterns, library locations, and key architectural
decisions. This builds up institutional knowledge across conversations. Write concise notes about what you found and
where."

**Main-session auto memory, for comparison** (memory page, first-hand): lives at `~/.claude/projects/<project>/memory/`
(line 512); `autoMemoryDirectory` in `settings.json` can move it (line 516); the folder holds a `MEMORY.md` index plus
one topic file per memory (lines 528–535); memory files are excluded from the transcript-cleanup sweep (line 542).

## How it maps to EJ's idea (my reading, not the docs')

- EJ's `agent/<agent name>/<memory files>` plus an index file = `…/agent-memory/<name>/` with `MEMORY.md`.
- An agent here is identified by its **agent name** — the `name` in the agent's markdown file, written `<name-of-agent>` in the docs — not by one session of it.
- EJ wanted user and agent memory outside the project repo. The `user` scope puts it in `~/.claude/agent-memory/`.
  That folder could itself be a git repo — **the docs do not say so; this is my idea and is untested.**
- EJ's rule "log when and which model changed it" is **not** built in. Claude Code does not record who changed an entry.
- The 200-line / 25KB limit is Claude Code's own default, for `MEMORY.md` only. It is not a value for our project memory
  index cap, which stays `OPEN` in `docs/memory-system/SOURCE_OF_TRUTH.md`.

## Not checked

- The last 8,547 characters of the sub-agents page.
- Whether Codex, opencode or other tools have anything like this.
- Whether `~/.claude/agent-memory/` works as a git repo, or with a symlink.
- Whether built-in types (`Explore`, `Plan`, …) accept a `memory` field, or only custom agent files.
- Which Claude Code version introduced the field.

## Decisions by EJ (2026-10-12)

- Agent memory is identified by **agent name** (not "agent type").
- The scope is **agent**. `user`, `project` and `local` are Claude Code's names for *where the memory folder is stored*,
  not memory scopes (see the section above for the three folders).
- **Where the memory is put follows Claude Code**: its folders and its `MEMORY.md` index (EJ: "location of where the
  memory put, yes should be following the claude code").
- **Agent-name memory is stored in the home folder** — Claude Code's `user` location, `~/.claude/agent-memory/<name>/`
  (EJ, 2026-10-12: "yes, should be at the home folder"). It stays outside every project repo. This matches EJ's earlier
  remark that user and agent memory should be outside the project repo.
