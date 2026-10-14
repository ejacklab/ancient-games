# Four experts — do agents use memory well on their own, and should the method say how?

Run in sequence (EJ's instruction): Linus → 范蠡 → 孫子 → 老子, each reading the research report as the previous
expert left it (`../report.md`, versions v0–v4). Dave (the control) was not run. COO (Claude `claude-opus-5-5`),
2026-10-13.

| | Linus | 范蠡 | 孫子 | 老子 |
|---|---|---|---|---|
| Q1: agents use memory well alone? | partly | partly | **no** | **no** |
| Q2: change the method? | yes, one change | yes, one small change | partly | partly |
| His change | O6: pointer to SoT + a memory contract in each node's fields | O7: pointer + "delivered by brief, import or hook, never as a request to read it" | O8: O7 + the brief names what a node must **not** receive | O9: pointer + delivery + "what a node writes is kept only when the run's end, or a later reader, names it" |
| Main items used | #2, #7, #9, #10, #13 | #1, #2, #4, #5, #13, #16 | #1, #2, #4, #12, #13, #16 | #1, #2, #3, #17, #18, #19 |

## Where they agree (*my reading*, each point *quoted* in report §6)
- Replace method §4's three-file project-memory paragraph (L494–510) with a pointer to `SOURCE_OF_TRUTH.md`.
- The designer, not the model, decides what memory reaches a node and when.
- Nothing from O3–O5 (a write evaluator, per-engine memory switches, refreshing App. B) until a run shows the harm.
- "More memory" is not the lever: Linus "does not depend on that ranking", 范蠡 "regulating, not filling", 孫子
  "narrow, never widen", 老子 "subtraction".

## Where they disagree (side by side, not averaged)
- **Q1.** Linus and 范蠡: "partly". 孫子: "the report's 'partly' is the harness working, not the agent knowing". 老子:
  "the timing is given from outside, and the keeping is unchecked from within". *My reading*: same evidence; "partly"
  answers whether the reads happen, "no" answers who knows to make them.
- **Per-node contract.** Linus wants one in every node. 范蠡: SoT already fixes timing and checks, so a per-node copy is
  "a second copy". 孫子 sides with 范蠡 for a different reason ("one whole copy").
- **Writes.** Only 老子 limits what is kept. It conflicts with SoT W4.1 (no owners, no gate) and K5.2 (the writer
  chooses), and he says to drop it if EJ won't change those.

## What each added that the others did not
- Linus: a matched-task test to run before enlarging anything; M13, stored notes leaking a worker's reasoning to a
  verifier.
- 范蠡: two gaps in this repo, both *verified* by the researcher: `AGENTS.md` only asks agents in words to read
  `CLAUDE.md`, and some of EJ's rules exist only in Claude's auto memory. Non-Claude nodes see neither unless they choose
  to look.
- 孫子: the denial half, already in SKILL.md L82 in general form; his clause applies it to memory entries.
- 老子: the outgoing half (what leaves the store). He also claimed two copies of the state template; **wrong**:
  `.claude/skills/workflow-design/assets/templates` is a symlink to `docs/workflow-templates` (COO checked, `ls -la`).

## What they need to know (merged, for EJ)
1. Will `SOURCE_OF_TRUTH.md` be built before the next workflow that needs project memory? (`project-memory/` does not
   exist today, COO checked.) If not, 范蠡's interim: keep §4's three files marked "until SoT is built".
2. Do your workflows use Codex, agy or opencode nodes? Has one ever broken a rule that lived only in `CLAUDE.md` or
   Claude's auto memory?
3. What extra tokens or time would you accept for fewer missed decisions (Linus)?
4. Would you change SoT W4.1/K5.2 for 老子's keep-when-named rule?

## Check
- `four_experts.py check`: FAIL, 6 failures, all 老子's Chinese. Five are one-character script variants (為/爲,
  敗/败). One normalises his list's bracketed Guodian transcription `亘（恒）于其○（且）成也败之` (list L80). None is
  invented. "dave: no answer file" is expected. Sabotage: 2 failures, so the check can fail. The check was written by
  Claude; it does not establish that a rule was applied correctly, or that the advice is good.
- Engines (`status.json`): Linus codex gpt-6.1-sol; 范蠡 Claude subagent (opus), because the task needs web; 孫子 dsh
  deepseek-flash; 老子 opencode MiniMax-M3.1-Flash-Preview.
- All four read the same question and the same growing report, so their agreement is not independent. EJ decides.
