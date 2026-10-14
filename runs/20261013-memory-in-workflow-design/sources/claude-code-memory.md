# Excerpts — Claude Code docs, "How Claude remembers your project"

URL: https://code.claude.com/docs/en/memory (fetched 2026-10-13; the page carries no date).
How read: WebFetch returned the page as raw markdown (50.3 KB), which the harness saved to disk because it was too
large to summarise; the lines below were read in that saved text and copied here verbatim. Line numbers are the saved
file's (`~/.claude/projects/-home-smoke01-dev-ancient-games/f0b8eb74-38a7-48f4-8fd1-65adc42a19cc/tool-results/toolu_01YWP9r1thSDS2FQoR7XJ7YN.txt`).

L24: Claude Code has two complementary memory systems. Both are loaded at the start of every conversation. Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a [PreToolUse hook](/docs/en/hooks-guide) instead. The more specific and concise your instructions, the more consistently Claude follows them.

L31: | **Loaded into** | Every session | Every session (first 200 lines or 25KB) |

L64: CLAUDE.md and CLAUDE.local.md files in the directory hierarchy above the working directory are loaded at launch. Files in subdirectories load on demand. See [How CLAUDE.md files load](#how-claude-md-files-load) for when they load and the full resolution order.

L88: * **Size**: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence. Move instructions that matter for only part of the codebase into [path-scoped rules](#path-specific-rules), which load only when Claude works with matching files. [Imports](#import-additional-files) help you organize a long file but don't reduce its context cost, because imported files also load at launch.

L90: * **Consistency**: if two instructions contradict each other, Claude may pick one arbitrarily. Review your CLAUDE.md files, nested CLAUDE.md files in subdirectories, and [`.claude/rules/`](#organize-rules-with-claude/rules/) periodically to remove outdated or conflicting instructions. To have Claude find them for you, [run a prompt audit](#audit-your-instruction-files).

L326: Settings rules are enforced by the client regardless of what Claude decides to do. CLAUDE.md instructions shape Claude's behavior but are not a hard enforcement layer.

L435: * **A `CLAUDE.md` that tells Claude in words to read `AGENTS.md`**: Claude sees `AGENTS.md` only if it decides to open the file. Delete the `CLAUDE.md` so Claude reads `AGENTS.md` directly, or replace the sentence with an `@AGENTS.md` import.

L476: Auto memory lets Claude accumulate knowledge across sessions without you writing anything. As it works, Claude saves four kinds of notes for itself. Claude records the kind as a `type` field in the memory file's frontmatter:

L478–481: `user` … `feedback` … `project`: ongoing work, deadlines, and decisions that Claude can't derive from the code or git history … `reference` …

L483: Claude skips anything it can derive from the codebase, such as architecture, file paths, or debugging fixes. It also skips anything your CLAUDE.md files already say.

L485: Claude doesn't save something every session. It decides what's worth remembering based on whether the information would be useful in a future conversation.

L546: The first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes first, are loaded at the start of every conversation. Content beyond that threshold is not loaded at session start. Claude keeps `MEMORY.md` concise by moving detailed notes into separate topic files.

L548: After Claude writes to `MEMORY.md`, Claude Code measures the file against the 200-line and 25KB read limits. If the file is near a limit, Claude Code reminds Claude to shorten it: keep one line per entry, move detail into topic files, and merge or drop stale entries. If the file is over a limit, the write still succeeds, but Claude Code returns an [error telling Claude to rewrite the index](/docs/en/errors#memory-index-is-over-its-read-limit), because everything past the limit is dropped on the next load.

L552: Claude Code doesn't load topic files such as `user_role.md` or `feedback_testing.md` at startup. Claude reads them on demand using its standard file tools when it needs the information.

L554: The main conversation's auto memory isn't loaded into [subagents](/docs/en/sub-agents#what-loads-at-startup); the exception is a [fork](/docs/en/sub-agents#fork-the-current-conversation), which inherits the parent conversation and system prompt. A subagent's own auto memory, enabled with the subagent `memory` field, is a separate directory.

L558: When Claude writes a memory file that begins with YAML frontmatter, Claude Code records the write time in a `modified` frontmatter field as an ISO 8601 timestamp. …

L570: When you ask Claude to remember something, like "always use pnpm, not npm" or "remember that the API tests require a local Redis instance," Claude saves it to auto memory. …

L578: CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself. Claude reads it and tries to follow it, but there's no guarantee of strict compliance, especially for vague or conflicting instructions.

L589: If the instruction is something that must run at a specific point, such as before every commit or after each file edit, write it as a [hook](/docs/en/hooks-guide) instead. Hooks execute as shell commands at fixed lifecycle events and apply regardless of what Claude decides to do.

L625: Project-root CLAUDE.md survives compaction: after `/compact`, Claude re-reads it from disk and re-injects it into the session. Nested CLAUDE.md files in subdirectories and rules with [`paths:` frontmatter](#path-specific-rules) load again on demand.

L627: If an instruction disappeared after compaction, it was given only in conversation, lives in a nested CLAUDE.md that hasn't reloaded yet, or is a path-scoped rule that hasn't matched a file since. Add conversation-only instructions to CLAUDE.md to make them persist. …
