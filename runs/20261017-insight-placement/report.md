# Report — where lessons live and how they reach each agent (20-minute time box)

Six experts answered in about 10 minutes, all checked (workflow wf_c332f8f0-c27; `place-q/compare.md`). The two
versions are in `versions.md`:

- **A — private store, chosen at brief time:** `~/.agents/lessons/` (all.md + one file per agent type); project facts
  as path-keyed entries in the project's memory; the main agent picks the matching lessons when it plans and briefs; no
  new hook.
- **B — lessons in this repo, pushed by the guard at the write:** a lessons skill in this repo (public), project facts
  in a lessons file in the code's folder; the guard adds a path's lessons just before a Write or Edit (needs the
  guard's PreToolUse hook registered for Write and Edit, a settings change); a selector script fills briefs.

All six agree: an engine gets lesson text in its brief, only the matching ones, and a delivery is tested by a planted
repeat. Five of six put the store outside this public repo; Dave alone keeps it in the repo.

Failure: my question said the guard sees every Write and Edit before it runs; it does not (PreToolUse is Bash only).
Linus found it; `insight.md` has the whys and two options.

Open for EJ: public or private lessons (and whether any come from private work projects); main agent's lessons chosen
before the work (A) or pushed at the write (B); the insight's fix option; the other questions in `compare.md`.

## Decided

- **Version B** (EJ: "version B , others follow your pick"): lessons in this repo as a lessons skill linked into both skill roots, each lesson naming its agents; project facts in a lessons file in the code's folder; the guard adds a path's lessons just before a Write or Edit (PreToolUse for Write and Edit, a settings change); a selector script fills briefs. Public, since the repo is. Not built yet: design first (`~/.claude/plans/agent-lessons-version-b.md`).
- Both insights: option 1, applied (`insight-decisions.md`).
