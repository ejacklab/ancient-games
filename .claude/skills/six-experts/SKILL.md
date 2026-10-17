---
name: six-experts
description: Ask EJ's six experts one question or decision — four researched personas, Linus Torvalds (Codex, or mcode when Codex is low), 范蠡 Fan Li (agy, or Claude for web/shell), 孫子 Sun Tzu (dsh / DeepSeek), 老子 Laozi (opencode / MiniMax); Dave (Claude Opus; experiments and data, ten rules, and he loads the project's insights by category before answering); and Dario, the plain control (Claude Sonnet, no rules, no insights) — each on its own engine; then check their citations and compare them side by side. Use when EJ says "ask the experts", "six experts", "four experts", "four seats", "ask Dave", "ask Dario", "what would Linus / 范蠡 / 孫子 / 老子 say", or wants a decision examined from several rule-based viewpoints. NOT for: plain factual lookups (one search answers those), code changes, or anything that needs the experts to act rather than advise.
---

# Six experts

Four experts, each built from a researched list of a real person's own mindsets, decision rules and algorithms
(18–20 numbered items with their words and a source, run `20261013-four-seats` in `~/dev/ancient-games`), and
**Dave**: ten numbered rules written from EJ's description — he loves experiments, is data-driven, and borrows solutions
from nature — and, since 2026-10-16, **the project's insights**: before answering he reads the insight index and the
sections of the categories the question names, and cites the ones he used. **Dario, the plain control**: Claude Sonnet
5.5, with no rules, no identity and no insights. Dave runs on Opus 5.5 (EJ, 2026-10-16), so Dave against Dario
differs in model as well as in rules and insights; to separate the two, run Dario on Opus as a third arm. Each persona answers on a different engine, so their agreement is closer to six views than one model's
echo.

| Expert | Engine | Model |
|---|---|---|
| Linus Torvalds | Codex (read-only) → **mcode** (lightweight) when Codex has 20% or less left | gpt-6.1-sol → MiniMax-M3.1-Flash-Preview |
| 范蠡 Fan Li | agy → **Claude** when the task needs web or shell, or when agy fails | gemini-3.8-flash-medium → claude-opus-5-5 |
| 孫子 Sun Tzu | dsh headless | deepseek-flash |
| 老子 Laozi | opencode (plan mode) | MiniMax-M3.1-Flash-Preview |
| **Dave** — rules + insights | Claude | claude-opus-5-5 |
| **Dario — the plain control** | Claude | claude-sonnet-5-5 |

Mapping, fallback and Dave: EJ, 2026-10-13. Dario and Dave's insights: EJ, 2026-10-16 (run
`runs/20261016-six-experts/`). Dave's model: Opus 5.5 by EJ's choice the same day, over the experts' advice for
Sonnet (D2 there); Dario stays on Sonnet. Dario is the
persona-free baseline the record lacked until then. Why the briefs are built this way (rules applied as instructions, item numbers cited, no invented
facts): `runs/20261013-seats-roleplay/synthesis.md` in the same repo.

## 1. Run

From the project root (opencode can read only files inside it):

```bash
python3 ~/.claude/skills/six-experts/scripts/six_experts.py run "Should we keep Cloudflare analytics on the page?"
```

- `--question-file F` for a long question. Put the facts the experts need **in the question**; they are told not to
  invent missing ones and will list them as questions instead. **Each fact carries its own label and the file:line or
  command that checked it; a fact with neither is marked *recall*.** One "verified" label over a block of facts is
  not allowed: in run `20261017-insight-placement` it covered a recalled fact that was wrong. **A file the question
  cites lives inside the repo:** copy an outside source into the run folder and cite the copy — agy and opencode
  auto-deny reads outside it (run `20261017-agent-lessons`, F-0969936e).
- `--insights instruction,check` names the insight categories Dave loads — the four Source kinds: instruction ·
  check · tool · config (`guard/src/cli.ts insight index` shows them). With none named he chooses from the index. The runner copies
  the index and the sections into the run's `seats/`, so every engine can read them; `check` fails Dave when he cites
  an id that is not in the index, or cites none without "No insight applies".
- For a Dave-against-Dario comparison, run both through the runner (not `--claude-by-caller`), so each runs on its
  own pinned model (Dave Opus, Dario Sonnet) with the same tools.
- `--needs-web` / `--needs-shell` when the task needs either — **you decide this from the task** — then 范蠡 runs
  on Claude, because agy headless cannot use web or shell (soft-denied, exits 0 with nothing).
- **Inside Claude Code, add `--claude-by-caller`.** The script then leaves Dave (and any 范蠡 fallback) to you: for
  each `CALLER` line it prints, start a subagent with "Read <brief> and do what it says." and save its final message
  to the answer path it names. Outside Claude Code the script runs `claude -p` itself.
- `--progress runs/<run>/nodes/experts.progress.md` appends a timestamped line as each expert starts and ends, so the
  caller sees progress while they work; `status.json` records each expert's start and finish time.
- **An approve-or-change question runs with `--card --vote`.** That is a question whose answer is `APPROVE`, or
  `CHANGE` with the exact words. **You decide this from the question**, as with `--needs-web`. In the experts-decide
  workflow, pass `approveOrChange: true`. Any other question runs without the two flags.
  - `--card` puts each persona's rules in its brief as a card: who they are, then one line per rule (heading and the
    Rule's first sentence, no quotes or sources). The brief tells the expert to read nothing else but the files the
    question names, and to run no shell. The full list and identity are still copied to `seats/` for `check`.
  - `--vote` sets the answer form: `APPROVE` or `CHANGE`, a short cited **Why**, and **What I need to know**. The run
    writes `form.txt`, and `check` then requires these three sections instead of the five.
  - Basis: run `20261017-experts-speed-trial`, one rerun of round 3 with both flags (n=1). The round's wait went from
    94 s to 48 s, with the same verdicts. The two flags' effects are not separated.
- `--only dave` (or any comma list of ids: `linus,fan-li,sun-tzu,lao-tzu,dave,dario`) with `--out <existing run>` adds
  those answers to a run and keeps the others.
- Output: `runs/<date>-six-experts-<slug>/` (or `six-experts/…` when there is no `runs/`): `question.md`,
  `seats/` (the lists used, frozen), `briefs/`, `answers/<id>.md`, `logs/`, `status.json`.
- 范蠡 falls back from agy to Claude automatically when agy returns nothing, an error, a timeout, or an answer
  without the required sections (a plan instead of the answer). `status.json` records the reason; the failed agy
  output is kept as `answers/fan-li.agy-failed.md`.
- Linus moves from Codex to mcode (`~/.minimax-code/bin/mcode`) in two cases. Before the run, the lower of Codex's two
  windows (5-hour and weekly, read from the newest rate-limit snapshot in `~/.codex/sessions/`) may have 20% or less
  left. During the run, Codex may stop on its usage limit; the failed log is then kept as `logs/linus.codex-failed.log`.
  `status.json` records `fallback_from: codex` and the reason. mcode, not opencode: 老子 is on opencode, and opencode
  cannot run twice at once (parallel starts can fail with "database is locked"). mcode runs lightweight — no tools, so
  it cannot write — and cannot open files, so the runner pastes the brief and its two files into
  `briefs/linus.pasted.md` and gives it on stdin. On mcode Linus shares 老子's model (not its engine), so read their
  agreement as one model's, not two.

## 2. Check

```bash
python3 ~/.claude/skills/six-experts/scripts/six_experts.py check <run dir>
python3 ~/.claude/skills/six-experts/scripts/six_experts.py check <run dir> --sabotage   # must report ≥ 2 failures
```

It checks every answer has the five sections. For each persona (not Dario, who has no list) it also checks the answer
cites at least one item, cites only item numbers its list has, and writes any run of 4+ Chinese characters exactly as
its list or identity file does; Dave must cite insight ids from his index or say "No insight applies" (on a miss it shows the nearest
passage, so a 趙/赵 script change reads differently from an invention). **What it does not establish:** that a rule
was applied *correctly*, or that the advice is good — read for that. The script was written by Claude; say so when
resting a conclusion on it.

## 3. Compare (the caller writes `compare.md` in the run folder)

```
# Six experts — <question>

| | Linus | 范蠡 | 孫子 | 老子 | Dave (rules + insights) | Dario (plain control) |
|---|---|---|---|---|---|---|
| Answer (one line) | | | | | | |
| Main items used | #… | #… | #… | #… | #… | — |
| Insights cited | — | — | — | — | <file>#<id> … | — |

## Where they agree
## Where they disagree   (side by side, quoted; never averaged)
## What each added that the others did not
## What they need to know   (the questions, merged, for EJ — and written out in your message to EJ, each one
                             with its options; never a count or this file alone)
## Check   (`check` result; engines and any fallback from status.json)
```

Label each line *quoted* (from an answer), *my reading*, or *not measured*. **EJ decides; the experts advise.** In a
time-boxed run (EJ gave a time or a number of rounds) the main agent decides from their advice instead, marks the
decision provisional with this run folder, and EJ accepts or declines it at the end (workflow-design method 3.8
item 14).
Do not pick a winner by vote count — five engines answering one brief still share the brief.

## Used by workflow-design (method 3.3 and 3.5)

In a time-boxed run, ask them through the saved workflow `.claude/workflows/experts-decide.js` (each expert in its
own subfolder, each answer checked, one rerun for a missing answer, `compare.md` written, the decision left to the
main agent); its `whenToUse` gives the args.

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
- The skill lives in the Ancient Games repo (`.claude/skills/six-experts/`), linked into `~/.claude/skills` and
  `~/.agents/skills`. The four lists are read from `$SIX_EXPERTS_SEATS` (default `runs/20261013-four-seats` in
  that repo),
  files `final-opus/<id>.md` and `identity/<id>.md` — the one copy. Dave's are in this skill's `assets/seats/`. Each
  run folder keeps a frozen copy of what was used.
- Engine calls: prompts in files, stdin from `/dev/null`, a timeout per call (`--timeout`, default 1800 s), the
  model named explicitly. Claude calls drop `ANTHROPIC_API_KEY` so they use the subscription login.
