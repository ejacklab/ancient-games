# Report — agent lessons, Version B (time-boxed: 3 hours or 3 rounds, whichever first)

**3 rounds in about 27 of 180 minutes. Lessons now live in one store and travel to every project; the guard gives the
main agent the matching ones by holding a call once — shown working live, before the call ran, in all three planted
arms and not in the control.**

## What exists now
- **The store:** `.claude/skills/agent-lessons/` — `SKILL.md` and 17 lessons, one file each: 3 from today's chosen
  insights and 14 moved from my memory (engine traps, testing rules), 1 of them a pointer to the check that enforces it.
  Linked into `~/.claude/skills` and `~/.agents/skills`, exported with the bundle, named in the bootstrap.
- **Project facts:** a `LESSONS.md` in the code's own folder (`guard/src/LESSONS.md`, 3 facts).
- **`lessons for --agent A --kinds … --paths … --commands …`** prints the matching lessons and facts for a brief;
  `lessons check` reports bad lesson files.
- **The hook:** before a Write/Edit/MultiEdit (by path) or a Bash call (by command, e.g. `codex exec`, `claude -p`,
  `jq`), the first call each agent makes that a new lesson matches is held, with the lessons as the reason; the retry
  runs. Each agent — the main one and each subagent — gets each lesson once.
- **Briefs:** the node-brief template has a Lessons section; each six-experts brief ends with its engine's lessons
  (Dario none); crossed-build-check refuses a test brief without one.
- Guard spec Round 18; guard 1462/1462, tsgo clean, Python 1136, workflow harnesses pass.

## The live test (P8, `p8/timeline.md`)
Headless Claude (Haiku) in scratch projects, the guard's PreToolUse from a temporary settings file in the run folder
(your user settings not loaded and not changed):
- **test edit:** the first Edit of a test file was held with the testing lessons; the agent checked them ("I already
  read the existing test, and I'm using the same `expect(...).toBe(...)` form"), sent it again, done.
- **project fact:** the first Edit of `src/math.ts` was held with the planted fact; the agent judged it did not apply
  to a rename, sent it again, done.
- **command:** `jq '.nmae'` was held with the print-keys lesson; the agent then ran `jq 'keys'`, found the field is
  `name`, and answered right — the lesson changed what it did.
- **control:** a read-only task, no hold.
n=1 per arm, no arm without lessons to compare against: delivery is shown; whether mistakes fall is not measured.

## Provisional decisions (yours to accept or decline)
1. **Holding the call once**, not adding context (five of six experts; the docs say context arrives "alongside the
   tool result", too late for the call).
2. **Marks per agent** (session + `agent_id`): subagents' calls carry the parent session id (docs), and in round 1
   the crossed-check workflow's agents used up every lesson before the main agent saw one.
3. **An enforced lesson never holds a call** — its check acts already; the first live hold on me was only such a
   pointer.
4. **A command entry is a word plus the words the command must hold** (`codex exec`, `claude -p`): my three live holds
   before this were all noise (`claude --help`, a pointer, a `python3` script).
5. **Engine traps are lessons for the caller**, keyed by the engine's command, not lessons in the engine's own brief.

## Needs your yes or your word
- **The settings change** (`settings-diff.md`): your PreToolUse matcher `Bash` → `Bash|Write|Edit|MultiEdit`, so file
  lessons reach me. Not applied (R12.3).
- **The installer** (`guard/src/install.ts`, crossed review finding 1): the same matcher, so `install --print` prints
  it. The auto-mode classifier denied my edit as self-modification; not made.
- **A guard defect found at the end:** `deadline status` and `deadline end` without `--session` act on the newest open
  deadline of any session — another session's 60-minute deadline answered my status call; a plain `end` would have
  ended it. I ended mine by its session.

## Failures and insights (`insight.md`)
- **Lessons used up by subagents** — options: marks per agent (applied provisionally), main agent only, or a rule to
  treat installed hook paths as live before saving. My pick: per agent.
- **F-0969936e** — 范蠡's agy call got nothing: a file read was auto-denied (my question cited a file outside the
  repo, my reading). Options: cite only files inside the repo; six_experts refuses an outside path; widen the agy
  lesson. My pick: the rule, cite only files inside the repo.
- Also: three C17 guard tests failed once while the experts' engines ran and passed on rerun (they read the process
  list) — flaky, not fixed.
