# Four experts and Dave — W3.6: can a procedure always be a script, and who decides?

Question: `../question.md`. Answers: `answers/`. One round (EJ, 2026-10-16: *"4 experts will review 1 round"*).

| | Linus | 范蠡 | 孫子 | 老子 | Dave (control) |
|---|---|---|---|---|---|
| Always a script? (*quoted*) | "No: a script can carry out executable work, but printing instructions or requesting a judgment does not mean it performs the whole procedure" | "A procedure cannot always be a script" | "A procedure cannot always be a script" | "No." | "No." |
| The test | executable steps; a scriptable but not-worth-it procedure is a cost judgment the author states | script when "execution and verification can be examined and run deterministically"; a page "where they require human discretion" | three: each step follows from named inputs; an objective check decides the outcome; it will run again on stable ground | "its last step can be written as a command that exits non-zero when the job is not done" | try it: `procedure.sh` + an external `verify.sh`; fails on a person's action or a branch on judgment |
| Who decides | the author when writing; the project owner (or their reviewer) when unclear or disputed | the authoring agent "on the spot"; the project owner when unclear or contested, at review, before it enters `AGENTS.md` | the agent writing it applies the test; the project owner decides what the test leaves open, and any "should not" | the agent writing it, with a reason; the project owner only the cases the agent cannot | the agent, by trying the script; the project owner if contested |

## Where they agree (5 of 5)

- **No, not always.** A step that needs a person's judgement, or whose result no command can check, cannot be
  scripted.
- **Who decides:** the agent writing the procedure, when it writes it, by applying a test; **the project owner when it
  is unclear or contested.** All five, *quoted* above.
- **A page must say why** — name the step that could not be scripted (孫子, 老子, Dave; Linus: "state the concrete
  tradeoff").

## Where they differ (side by side, not averaged)

- **A step that only waits for a person** (an approval, a typed confirmation). 孫子: still a script, "a script that
  stops at that named gate". Linus: a script that only prints instructions or asks for a judgment does not perform the
  procedure. Dave leaves it to EJ.
- **"Can" versus "worth it".** Linus and 孫子 add a cost side: scriptable but not worth building (Linus), or not run
  again on stable ground (孫子); 孫子 gives that "should not" half to the project owner. Dave: a procedure run once is
  task work, not a procedure.
- **The test's wording** differs (table above); every one turns on whether a command can check the result.

## Proposed W3.6 wording (each the expert's own, *quoted*)

- Dave: *"A procedure lives in the repo as a script with an external check; where a step cannot be a command with a
  checkable result — a person's action, or a choice that depends on judging what was seen — it is a page in `docs/`
  that names that step and calls scripts for the rest. The agent writing the procedure decides by trying the script
  first; the project owner decides if it is contested."*
- 孫子: *"A procedure lives in the repo as a script when every step follows from inputs it names, an objective check
  can decide its outcome, and it will run again on ground that stays still; otherwise it lives as a page in `docs/`
  and names which of the three failed. The agent writing the procedure applies this test and records the result; the
  project owner decides the case the test leaves open."*
- 范蠡: *"A procedure lives in the repo as a script if its execution and verification can be examined and run
  deterministically, or as a page in `docs/` where they require human discretion. The authoring agent classifies it on
  the spot, and the project owner decides when unclear or contested during review before it is named in
  `AGENTS.md`."*

## Check

`four_experts.py check`: PASS, 5 answers, 0 failures. The check was written by Claude; it shows every answer has its
sections and cites only items its list has — not that a rule was applied well. Engines: Linus codex gpt-6.1-sol,
范蠡 agy gemini-3.8-flash-medium, 孫子 dsh, 老子 opencode MiniMax-M3.1-Flash-Preview, Dave a Claude subagent.
Nothing in the design was changed.
