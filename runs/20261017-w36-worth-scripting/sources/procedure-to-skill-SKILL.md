---
name: procedure-to-skill
description: "Turn a 'how do I deploy/reinstall/run X' procedure into a skill — a runnable scripts/procedure.sh plus scripts/verify.sh — instead of a CLAUDE.md note or a chat answer that has to be re-explained next time. Use when about to write down a multi-step operational procedure anywhere other than a script: in CLAUDE.md, in a memory note, or as a one-off chat answer meant to be reused. NOT for a fact with no steps (that's a memory note or a CLAUDE.md line), or a procedure specific to one throwaway task."
---

# Procedure To Skill

Grounded in `research/2026-09-agent-memory-systems.md` (`~/dev/research/`) — CLAUDE.md is
context, not enforced configuration, capped at ~200 lines for adherence; its own guidance
says a multi-step procedure belongs in a skill. This closes the gap between knowing that
and actually doing it every time.

## The rule

**The procedure is the memory. A prose description of a procedure is a summary of the
memory, and summaries drift** — the same failure mode as an extracted algorithm
(`verify-extraction`), one layer up: here what's being extracted is a sequence of
operational steps instead of a function's logic.

## Procedure

1. Scaffold: `python3 scripts/scaffold_skill.py <name> "<one-sentence description>"`
   (defaults to `~/skills/<name>/`; refuses to overwrite an existing skill without
   `--force`, so it never clobbers real work by accident).
2. Fill `scripts/procedure.sh` with the actual steps. This file *is* the memory from now
   on — when the real steps change, edit this, not a note somewhere else.
3. Fill `scripts/verify.sh` with a real, **external** check: a health endpoint, a
   process/pod status, a smoke test against the actual result. Not a check that only
   re-reads the procedure script's own exit code — that would just restate "the script
   ran," which is a weaker claim than "the thing worked," and only the second is safe to
   report to a user.
4. Both stubs exit non-zero by default and say so on stderr — an unfilled skill can never
   be mistaken for a working one, before or after `--force`.
5. Symlink into the loaded location if it isn't already there:
   `ln -s ~/skills/<name> ~/.claude/skills/<name>` — the scaffolder prints this command
   whenever `~/.claude/skills/<name>` doesn't exist yet.

## When *not* to do this

A single fact with no steps — a URL, a hostname, a config value — is a memory note or a
CLAUDE.md line, not a skill; skills cost a name+description in every session's context,
so reserve them for things worth that cost: a procedure someone will actually run again.

## Related

- `verify-extraction` — the same "make it runnable, don't trust the prose" rule, applied
  to an algorithm read out of code instead of an operational procedure.
- `e2e-probe` — a stable e2e probe spec is exactly the kind of procedure this scaffolds;
  its `run.json` spec can live inside `scripts/procedure.sh` once it's finalized for one
  environment.
