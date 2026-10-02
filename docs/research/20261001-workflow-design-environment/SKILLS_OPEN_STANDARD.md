# Agent Skills as an open standard — 2026-10-01

Status: web research (**reported**, untrusted sources) + local checks (**verified** as marked).

## The standard

- SKILL.md published as an **open standard on 2025-12-18** (agentskills.io), created by Anthropic, stewarded
  through the Agentic AI Foundation. Spec: `github.com/agentskills/agentskills`.
- A skill is a directory with a `SKILL.md` (YAML frontmatter: `name`, `description`) plus optional references,
  assets and scripts.
- Mechanism: **three-level progressive disclosure** — (1) name + description preloaded (~dozens of tokens),
  (2) body loads on trigger, (3) references/scripts on demand. Bundled context is "effectively unbounded"
  because almost none is resident.

## Adoption (reported)

- Within 48 h: Microsoft (VS Code) and OpenAI (ChatGPT + Codex CLI).
- ~32 tools by March 2026; ~40 products on the agentskills.io showcase by June 2026. Named: OpenAI Codex,
  GitHub Copilot, VS Code, Cursor, Google Gemini CLI, JetBrains Junie, Goose, OpenCode, Amp, Factory,
  AWS Kiro, Roo Code, Trae, Windsurf, Databricks Genie Code, Snowflake Cortex Code, Mistral Vibe, Spring AI.
- Ecosystem scale: ~89,753 skills on Vercel's skills.sh; `anthropics/skills` >100k stars (reported, single
  source each).

## The 2026 stack consensus

**MCP/tools = connectivity (ability to act) · Skills = procedural knowledge (how/when) · Scripts =
deterministic execution.** Complementary, not competing (arXiv survey 2602.12430; Anthropic engineering post).

Progressive disclosure was back-ported to tools themselves: MCP Tool Search / `defer_loading` in Claude Code
(Jan 2026). Reported numbers: 50+ MCP tools 72K → 8.7K tokens (−85%); code-execution with filesystem-scoped
MCP defs 150K → 2K (−98.7%); programmatic tool calling 43,588 → 27,297 tokens (−37%) with accuracy
79.5% → 88.1%; agent degradation past 2–3 MCP servers. All **reported**, not reproduced here.

## Local checks (verified 2026-10-01)

- `~/.codex/skills/` exists and holds a skill (`evidence-knowledge-graph`) — Codex CLI has a skills directory.
- `agy --help` shows `--disable-slash-commands  Disable slash command and skill expansion in print mode` —
  agy supports skills; **where it looks for them is unverified**.
- `~/.agents/skills/` exists (vendor-neutral location from the same standard) with EJ's `coding-discipline`.
- The workflow-design skill is symlinked **only** to `~/.claude/skills/workflow-design` → repo
  `.claude/skills/workflow-design` (verified). Codex and agy do not see it yet.

## Consequences for this folder

1. The skill form is **more** valid than when it was built: one SKILL.md can reach all three executor kinds.
2. `~/.agents/skills/` is the candidate cross-tool location (would replace or supplement the `~/.claude`
   symlink).
3. Before relying on reach: extend the readiness canary (docs/EXECUTOR_KINDS.md) to prove each kind actually
   *loads* the skill — directory existence is not loading.
4. Progressive disclosure says a skill body should be thin (trigger + outline), with depth in references/ —
   relevant to the SKILL.md duplication finding (`ALGORITHM_COPIES.md`).

## Sources

- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- https://agentman.ai/blog/agent-skills-ecosystem-report-2026
- https://www.paperclipped.de/en/blog/agent-skills-open-standard-interoperability/
- https://inference.sh/blog/skills/agent-skills-overview
- https://arxiv.org/html/2602.12430v4
- https://www.anthropic.com/engineering/advanced-tool-use
- https://www.anthropic.com/engineering/code-execution-with-mcp
- https://www.developersdigest.tech/blog/skills-over-mcp-progressive-disclosure
- https://www.damiangalarza.com/posts/2026-02-05-mcps-vs-agent-skills/
- https://www.mcpjam.com/blog/claude-agent-skills
- https://tessl.io/blog/anthropic-brings-mcp-tool-search-to-claude-code
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool
