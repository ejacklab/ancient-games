# Two versions — where lessons live and how they reach each agent

From the six experts' answers (`place-q/compare.md`). Both keep what all six agree on: an engine gets the lesson's
**text inside its brief**, never a path to go read; only the lessons that match that engine, task and paths go in; and
a delivery is tested only by a planted or replayed repeat of the failure.

## Version A — private store, chosen at brief time (no new hook)
- **Store:** a private user-global folder, `~/.agents/lessons/`, outside the public repo: `all.md` for every agent and
  one file per agent type (`claude-main.md`, `opencode.md`, `codex.md`, `agy.md`, `mcode.md`, `dsh.md`).
  Advised by Linus, 范蠡, 孫子, 老子 and Dario (store outside the repo); file per scope by 老子 and Dario.
- **Project facts:** path-keyed entries in the project's own memory (SoT `covers:` entries), so whoever edits that code
  is given them — Linus, 老子, Dario.
- **Delivery:** the main agent selects the matching lessons by engine, kind of task and paths when it writes a brief,
  and reads its own (`claude-main.md`, `all.md`) before the work starts — 老子, Linus, Dario. No per-write hook.
- **Drain:** a lesson enforced by a check or test shrinks to a pointer to that check — 孫子, 老子, Dave.
- **Costs:** selection is the main agent's judgment, so a missed lesson is silent; not shareable across machines
  unless the folder is made a private git repo (孫子).

## Version B — lessons in this repo, pushed by the guard at the write
- **Store:** a lessons skill in this repo (`.claude/skills/agent-lessons/`), linked into `~/.claude/skills` and
  `~/.agents/skills` like workflow-design; each lesson names its agents in one field (`agents: all | opencode | …`).
  Advised by Dave (in the repo); one field per lesson by 孫子 and Dave. **Public**, since the repo is.
- **Project facts:** a lessons file in the code's own folder (`src/LESSONS.md`) — Dave, 范蠡.
- **Delivery:** for the main agent, the guard adds the lessons for a path just before a Write or Edit to it — 范蠡,
  孫子, Dave, Dario. **This needs the guard's PreToolUse hook registered for Write and Edit, which it is not today**
  (Linus; `src/install.ts:28`, `~/.claude/settings.json`) — a change to your settings. For engines, a fixed-rule
  selector script fills the brief's Lessons section — 孫子, Dave.
- **Costs:** public lessons; a settings change; a script to build and test.

## The difference in one line
A trusts the main agent to choose lessons when it plans, and costs nothing new; B makes a program push them at the
moment of the edit, and costs a hook, a script and making the lessons public.

## Open for EJ (from compare.md, the ones that decide between A and B)
- Are lessons public or private — and will any come from your private work projects?
- Main agent: chosen before the work (A), or pushed by the guard at the write (B)?
