# Owner-only items — provisional answers (the main agent's picks, from the experts' advice; for EJ to accept or decline)

Nothing below is applied: each changes a text the owner holds (the method, a requirement, the plan's open choices).

## 1. A question that trials cannot answer goes to the owner at once
- Experts (`owner-q/compare.md`, five asked; 老子 not asked: another session's opencode was running): all five pick
  adopt. Their reason, quoted in substance: a trial with no check that can fail it gives no information, so three such
  trials only delay. Four of five add a gate against using it as an escape hatch.
- **My pick: adopt, with the gate.** Proposed rule for method 3.3: "A question no trial can answer — no run, read or
  measurement in reach would settle it — goes to the owner at once, in the next batch of questions, not after three
  failed trials. The agent writes one line with it: which trial or check would answer it, and why it cannot be run.
  In a time-boxed run it is decided provisionally at once and listed for the owner (3.8 item 14)."
- Open inside it (the experts split): outside a time-boxed run, "at once" means the next 3.3 batch (孫子) or a separate
  ask straight away (范蠡). My pick: the next 3.3 batch — one batch of questions is the method's existing shape.

## 2. Claude Code's memory folder in memory-check
- Experts: all five pick (a), list it as present or absent only; all five reject (b), checking it, because the folder
  does not follow the guidelines' entry format and would give false failures. They split on whether it *is* agent
  memory (Linus yes; 孫子 and Dave no, by `SOURCE_OF_TRUTH.md:20`, "memory belonging to one agent name").
- **My pick: (a), on its own line, not as agent memory.** Proposed F1 addition: "It also reports, on a line of its own
  marked 'harness memory, not a location the guidelines name', whether Claude Code's memory folder for the project
  (`<home>/.claude/projects/<project path with / as ->/memory/`) is present or absent, and nothing else about it."
  Present or absent only, no names or counts: file names would show personal facts (孫子, Dario).

## 3. O1 — what counts as "changes something" (plan "every task teaches")
- Experts (2026-10-16, `runs/20261016-four-experts-what-counts-as-change/compare.md`, five of five): detect the
  effect, not the tool; neither option (a) nor (b) alone.
- **My pick:** a change is a path the hook saw written (Write, Edit, MultiEdit) or a change git shows since the prompt
  (HEAD, the working tree, a remote-tracking ref), classified by one path table; an unknown path counts (Linus). Not a
  change: an engine call that only answers (what it writes counts by where it lands), the guard's own journal
  (`.harness-guard/`), and run-folder logs. Memory outside the repo counts, by path.

## 4. O3 — how "main" and "core" are marked
- Experts: the mark belongs to a person, never to the guard or an agent (four say only EJ); the main objectives have
  no file, so a change to them cannot be detected.
- **My pick (Dave's form):** one more value on the register verdict that only the owner writes — accepted as main /
  accepted / declined. A change to the vision always waits for the owner.

## 5. A real project for memory-check's calibration
- A fact only the owner has; no expert can answer it. None was found on this machine with `project-memory/` and
  merges. Until one is named, memory-check is calibrated on fixtures only, and its reports say so.

## Also for the owner (found in this run)
- **EV-R3.2 wording** (`evaluator-decisions.md`, item 8): "writes only inside `runs/<runId>/`, apart from the judge's
  scratch folder in `/tmp`, which it removes before it ends."
- **EV-C3.2 wording** (item 11): "A case whose probes all stay green on its case's mutant is unproven, and its case
  cannot be PASS."
- **Use cases as an evaluator input** (item 10): yes or no; the design is written.
