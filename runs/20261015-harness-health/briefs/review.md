# Review brief — harness_health.py (read-only)

You are reviewing a change in the git worktree `/home/smoke01/dev/ancient-games-harness-health`, branch
`feat/harness-health`, commit `cb808f1` (`git show cb808f1`). You may read any file and run read-only commands
(`git show`, `python3 -m pytest -q tests/test_harness_health.py`, running the script). Do not edit any file.

## What the change is for

A workflow-design method has a readiness step (`.claude/skills/workflow-design/scripts/readiness.py`) that proves which
tools are installed. The new `scripts/harness_health.py` reads how each installed agent harness (Claude Code, Codex,
agy, qwen, dsh, opencode) is configured against ten harness requirements, and for what is absent prints the file, the
key and a snippet the person applies. It must never write a file, never spend model quota, and never print a config
value other than a recognised mode name or a count. `readiness.py` also gains `dsh` and `opencode`.

## The standard you check against (acceptance criteria)

- AC1 readiness lists `dsh` and `opencode`; all prior readiness tests pass.
- AC2 harness_health prints ten requirement rows on any machine, with no project or home path hardcoded or printed as an absolute path.
- AC3 every check that can say `absent` has a test that makes it say so, and one that makes it say `present`.
- AC4 no planted secret value appears in any output (markdown or JSON).
- AC5 every help snippet, applied as its help text says, turns its finding to `present`; the script modifies no file.
- AC6 the full suite passes (baseline before the change: 994 passed; after: 1013 passed).
- AC7 on this machine the output shows: Claude Code has no deny list; Codex has no top-level `sandbox_mode` or `approval_policy`; dsh and opencode are listed. Saved output: `/home/smoke01/dev/ancient-games/runs/20261015-harness-health/evidence/harness-health-this-machine.md`.

Evidence for the key names: `/home/smoke01/dev/ancient-games/runs/20261015-harness-health/evidence/u6-codex-keys.txt`
and `u6-claude-keys.txt` beside it. Mutation check of the tests: `mutation-check.txt` beside it.

## What to return

Plain English Markdown, these sections:

1. **Verdict per criterion** — AC1–AC7: holds / does not hold / cannot tell, each with the file:line or command output that shows it.
2. **Defects** — each: file:line, what is wrong, a concrete input that shows it, severity (high / medium / low). Look in particular for: a value that could leak a secret; a case where a finding says `present` when the harness is not set up (a false reassurance); a crash on an odd config shape (wrong types, empty files, lists where objects are expected); a claim in the output or docstring the evidence does not support; anything project-specific hardcoded.
3. **Tests that would pass on a broken script** — a test that does not check what its name says.
4. **What you did not check.**

Do not suggest new features. Report only what is wrong or unsupported.
