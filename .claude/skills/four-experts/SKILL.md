---
name: four-experts
description: Ask EJ's four experts — Linus Torvalds (Codex), 范蠡 Fan Li (agy, or Claude when the task needs web or shell), 孫子 Sun Tzu (dsh / DeepSeek), 老子 Laozi (opencode / MiniMax) — plus Dave, the control (Claude; experiments, data, nature-inspired solutions), one question or decision, each answering through its own numbered decision rules on its own engine; then check their citations and compare them side by side. Use when EJ says "ask the four experts", "four seats", "ask Dave", "what would Linus / 范蠡 / 孫子 / 老子 say", or wants a decision examined from several rule-based viewpoints. NOT for: plain factual lookups (one search answers those), code changes, or anything that needs the experts to act rather than advise.
---

# Four experts and Dave

Four experts, each built from a researched list of a real person's own mindsets, decision rules and algorithms
(18–20 numbered items with their words and a source, run `20261013-four-seats` in `~/dev/ancient-games`), and
**Dave, the control**: ten numbered rules written from EJ's description — he loves experiments, is data-driven, and
borrows solutions from nature. Each answers on a different engine, so their agreement is closer to five views than
one model's echo.

| Expert | Engine | Model |
|---|---|---|
| Linus Torvalds | Codex (read-only) | gpt-6.1-sol |
| 范蠡 Fan Li | agy → **Claude** when the task needs web or shell, or when agy fails | gemini-3.8-flash-medium → claude-opus-5-5 |
| 孫子 Sun Tzu | dsh headless | deepseek-flash |
| 老子 Laozi | opencode (plan mode) | MiniMax-M3.1-Flash-Preview |
| **Dave — the control** | Claude | claude-opus-5-5 |

Mapping, fallback and Dave: EJ, 2026-10-13. EJ chose Dave as the control instead of a plain no-persona answer, so
there is no persona-free baseline: a comparison shows what each rule set adds relative to the others, not relative
to a plain model. Why the briefs are built this way (rules applied as instructions, item numbers cited, no invented
facts): `runs/20261013-seats-roleplay/synthesis.md` in the same repo.

## 1. Run

From the project root (opencode can read only files inside it):

```bash
python3 ~/.claude/skills/four-experts/scripts/four_experts.py run "Should we keep Cloudflare analytics on the page?"
```

- `--question-file F` for a long question. Put the facts the experts need **in the question**; they are told not to
  invent missing ones and will list them as questions instead.
- `--needs-web` / `--needs-shell` when the task needs either — **you decide this from the task** — then 范蠡 runs
  on Claude, because agy headless cannot use web or shell (soft-denied, exits 0 with nothing).
- **Inside Claude Code, add `--claude-by-caller`.** The script then leaves Dave (and any 范蠡 fallback) to you: for
  each `CALLER` line it prints, start a subagent with "Read <brief> and do what it says." and save its final message
  to the answer path it names. Outside Claude Code the script runs `claude -p` itself.
- `--only dave` (or any comma list of ids: `linus,fan-li,sun-tzu,lao-tzu,dave`) with `--out <existing run>` adds
  those answers to a run and keeps the others.
- Output: `runs/<date>-four-experts-<slug>/` (or `four-experts/…` when there is no `runs/`): `question.md`,
  `seats/` (the lists used, frozen), `briefs/`, `answers/<id>.md`, `logs/`, `status.json`.
- 范蠡 falls back from agy to Claude automatically when agy returns nothing, an error, a timeout, or an answer
  without the required sections (a plan instead of the answer). `status.json` records the reason; the failed agy
  output is kept as `answers/fan-li.agy-failed.md`.

## 2. Check

```bash
python3 ~/.claude/skills/four-experts/scripts/four_experts.py check <run dir>
python3 ~/.claude/skills/four-experts/scripts/four_experts.py check <run dir> --sabotage   # must report ≥ 2 failures
```

It checks every answer has the five sections, cites at least one item, cites only item numbers its list has, and
writes any run of 4+ Chinese characters exactly as its list or identity file does (on a miss it shows the nearest
passage, so a 趙/赵 script change reads differently from an invention). **What it does not establish:** that a rule
was applied *correctly*, or that the advice is good — read for that. The script was written by Claude; say so when
resting a conclusion on it.

## 3. Compare (the caller writes `compare.md` in the run folder)

```
# Four experts and Dave — <question>

| | Linus | 范蠡 | 孫子 | 老子 | Dave (control) |
|---|---|---|---|---|---|
| Answer (one line) | | | | | |
| Main items used | #… | #… | #… | #… | #… |

## Where they agree
## Where they disagree   (side by side, quoted; never averaged)
## What each added that the others did not
## What they need to know   (the questions, merged, for EJ)
## Check   (`check` result; engines and any fallback from status.json)
```

Label each line *quoted* (from an answer), *my reading*, or *not measured*. **EJ decides; the experts advise.** In a
time-boxed run (EJ gave a time or a number of rounds) the main agent decides from their advice instead, marks the
decision provisional with this run folder, and EJ accepts or declines it at the end (workflow-design method 3.8
item 14).
Do not pick a winner by vote count — five engines answering one brief still share the brief.

## Used by workflow-design (method 3.3 and 3.5)

The workflow-design method calls this skill at two steps (EJ, 2026-10-13), each with only the experts who named it
as where their rules are reliable (`runs/20261013-four-experts-where-in-ej-s-workflow/compare.md`):

| Method step | `--only` | Question template (fill the Facts, pass with `--question-file`) |
|---|---|---|
| 3.3 unclear spots, once the list is written | `linus,sun-tzu,lao-tzu,dave` | `assets/questions/unclear-spots.md` |
| 3.5 before a piece runs as a loop | `linus,fan-li,sun-tzu,dave` | `assets/questions/loop-check.md` |
| a decision in a time-boxed run (3.8 item 14) | all five | `assets/questions/time-boxed-decision.md` |

Their answers are advice: a raised spot is added and marked *raised by*, a "drop it" goes to EJ as a question, a
failure a check would miss strengthens the check or sends the piece back to the unclear list. The design's state file
records the run folder, or *not asked* with the reason.

## Notes

- Plain English Markdown briefs for every engine; replies in English; EJ referred to as they/them (EJ, 2026-10-13).
  Chinese appears only where an expert quotes its own list.
- The skill lives in the Ancient Games repo (`.claude/skills/four-experts/`), linked into `~/.claude/skills` and
  `~/.agents/skills`. The four lists are read from `$FOUR_EXPERTS_SEATS` (default `runs/20261013-four-seats` in
  that repo),
  files `final-opus/<id>.md` and `identity/<id>.md` — the one copy. Dave's are in this skill's `assets/seats/`. Each
  run folder keeps a frozen copy of what was used.
- Engine calls: prompts in files, stdin from `/dev/null`, a timeout per call (`--timeout`, default 1800 s), the
  model named explicitly. Claude calls drop `ANTHROPIC_API_KEY` so they use the subscription login.
