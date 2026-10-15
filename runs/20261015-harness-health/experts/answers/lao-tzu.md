I'll read the brief first.
# 老子 (Laozi) — harness health in the readiness step

## Answer

Build `scripts/harness_health.py` beside `readiness.py`, with the same Probe shape and the same four statuses, printing **ten requirement rows, not ten times six**: one line per requirement, a drill-down only where a condition is not good enough, and a Help block that names the file, the key and a ready snippet and then stops. "Good enough" gets a verdict only where the requirement names a concrete thing that exists or does not (a deny list, a sandbox mode, a hook, a second verified engine kind); every other requirement reports the measured number with no verdict, and no comparison happens until the right-hand side lives in a file the person owns. If EJ wants the check to *block* dispatch as well as report, say so — that is N1, and it changes one exit code.

## How I decided

1. **Take nothing away from readiness; add the new group beside it.** My #1: 損之又損，以至於無為 — "Lose and lose again, until one arrives at not-doing. Not doing, and nothing is left undone" (`quoted`). Readiness is the inventory and it does its one job; the health check is a new, separate instrument, not a subtraction from what already works. U4: a new script, same Probe dataclass, called by readiness and rendered as one more group.

2. **Ten rows, not sixty.** My #14: 少則得，多則惑 — "little, then gaining; much, then confused" (`quoted`). Six harnesses × ten requirements is sixty lines, and sixty lines is a report nobody reads. The table's spine is the ten requirements; a harness line appears only where it is not good enough. Same shape as the readiness groups, one level down.

3. **The check must be able to fail before it is trusted.** My #6: 為之於未有，治之於未亂 — "Act on it before it exists; order it before it is in disorder" (`quoted`). Every check gets its planted-wrong-input sabotage as part of the step that builds it, not as a later proof. My #7 closes the same step: 慎終如始，則無敗事 — "Careful at the end as at the beginning: then no undertaking fails" (`quoted`) — the last check written is proved like the first, and readiness's own 26 tests still pass at the end.

4. **Verdicts only where existence is the requirement.** My #8: 知不知上，不知知病。夫唯病病，是以不病 — "To know that you do not know is best… Only by treating sickness as sickness is one not sick" (`quoted`). A key is present or absent; that is a fact, not a judgement. A count is a measurement, and a measurement with nothing to compare it to is not a verdict. So U3 stands with one change: the main agent's "report the measured number with no verdict" becomes "report the number **and** where its comparison value lives; if that place does not exist, the line is `unknown` with the reason".

5. **Every comparison points at something the person wrote.** My #2: 知足不辱，知止不殆，可以長久 — "Knowing what is enough, one is not disgraced; knowing to stop, one is not endangered; one can last long" (`quoted`). A trigger is "measure X against Y", and Y is EJ's to give — a file the doctor reads, or a flag. The script invents no number, and where the number is needed but absent, the row says "no comparison given" rather than guessing one.

6. **Help is a result, not a change.** My #13: 善有果而已，不敢以取強。果而勿矜，果而勿伐，果而勿驕 — "The good one has a result and that is all; he does not dare use it to take strength. Result, and no vaunting; result, and no boasting; result, and no arrogance" (`quoted`). So the help piece gives the exact file, the exact key, a snippet the installed version accepts, and one sentence on what it changes — and never writes it. My #3 closes the step: 功遂身退，天之道 — "The work done, the self withdraws: this is the Way of heaven" (`quoted`). A config the agent changed on a person's machine is a config no one read. U2: advice plus a snippet, handback only.

7. **What the doctor cannot read is named, not filled.** My #8 again: only by calling the sickness a sickness is one not sick. U6 is settled by rule: a probe reads only what has been verified against the installed version, and every other line is `unknown` with the reason and the version it would need. The test carries the version it verified, and a check may not report `verified` without that note in the file.

8. **The doctor diagnoses; the method prescribes.** My #16: 知人者智，自知者明。勝人者有力，自勝者強 — "One who knows others is clever; one who knows himself is clear. One who overcomes others has force; one who overcomes himself is strength" (`quoted`). The script's business is the harness; the design's business is the consequences, and a script that writes method prose is gripping what is not its own — my #4: 執者失之 — "one who holds on to it loses it" (`quoted`). So U5 splits: the script prints the conditions found, and method.md 3.1 gains a **Found → effect on the design** table (found condition → what the design must now do differently: a build node's Guard stakes, or the reviewer must be a script check) beside the existing information-check table. That text is EJ's to accept.

9. **The four requirements that are not properties of the harness are named, not probed.** My #14 again, and my #4: gripping the whole is losing it. R2, R3, R7 and the per-run parts of R5 and R8 are judged per run by gates that already exist. U7: one line each, "covered by `<path>`", and the path is checked for existence — that line can fail if the gate file moves. The doctor never claims them.

10. **Check the harness the design will actually dispatch to, but list everything found.** U1: probe every harness found, one drill-down per harness, and `--harness` narrows the *verdict* to the ones the design uses. My #15: 水善利萬物而不爭，處眾人之所惡 — "Water benefits all ten thousand things and does not contend; it settles where the crowd finds distasteful" (`quoted`). Listing costs nothing and the person can see the whole field; the verdict is only about the harnesses that will run the work. Cost: a design that dispatches to a harness nobody probed gets an unknown, which is the honest answer.

11. **Requirement by requirement, the checks are:**

    | # | What the doctor looks at | Verdict rule | Help |
    |---|---|---|---|
    | R1 | project + user instruction files exist and are readable; skills folders non-empty | existence only; line count reported, never judged | pointer to the missing file name; the doctor writes no instruction file |
    | R2 | — | `covered by` the dispatcher adapters and the per-run gates | none |
    | R3 | — | `covered by` the state template and `design_gate.py` | none |
    | R4 | the memory and history directories each harness leaves on disk | existence | pointer to the path; no size threshold |
    | R5 | how many *distinct* engine kinds are `verified` on this machine, against the kinds the design names | a comparison, against the design's own list — no number invented | if one kind only: the note that the reviewer must be a script check, because a builder cannot be its own reviewer (my #16) |
    | R6 | deny list present; sandbox mode explicitly set; approval policy set; which hook events are installed | existence per item; the hook event list is `unknown` until verified against the installed version | the snippet for the missing key, handback only |
    | R7 | — | `covered by` the dispatch timers and bounded repair rounds | none |
    | R8 | whether the harness has an approval mechanism configured | existence | snippet for the key that sets it |
    | R9 | whether each harness leaves a log or event trail on disk, and where | existence and the path | pointer to the path; no retention threshold |
    | R10 | whether the project's feedback pieces (why-chain hook, task-types ledger) are present | existence, plus `covered by` naming the file | pointer to what to create; the doctor does not create it |

12. **The empty space is where the work happens.** My #17: 三十輻共一轂，當其無，有車之用 — "Thirty spokes share one hub; in its nothing lies the cart's use" — and 故有之以為利，無之以為用 — "what is there makes for benefit; what is not there makes for use" (`quoted`). The doctor's value is not in listing settings that exist; it is in the space the doctor does not fill — no verdict where nothing is verifiable, no number where no comparison exists, no edit where advice is enough. The report should say so in one line at the top: what was not looked at is listed as not looked at.

13. **One secret rule, from the start.** My #19: 以深為根，以約為紀 — "He takes depth as the root and restraint as the rule" (`quoted`). The doctor touches config files, and config files hold keys. The rule readiness already follows for qwen — read the key names, never the values — becomes a rule for every file the doctor opens, and one test plants a key in every file shape the doctor reads and fails if any value appears in the output.

14. **The doctor never prints a total.** My #2 again, applied to the whole report: knowing what is enough is knowing where you stop, and a roll-up "harness healthy" containing unknowns is not enough to know anything. There is no overall grade. The nearest thing to a total is a count of rows by status, stated as a count.

## What I need to know

- **N1 · decision · blocks the exit codes.** Does a not-good-enough condition *block* dispatch (`exit 1`, like `--require`) or only inform? If it blocks, exactly which conditions block, and is that the same list as `--require-harness`, or EJ's own?
- **N2 · decision · blocks every comparison in R5.** Where do comparison values live — a per-machine file, a per-project file, or command-line flags? What is the file's path and shape? Any "measure X against Y" check is dead without Y's address.
- **N3 · unknown · blocks R6, R8, R9.** The exact key names and file locations for sandbox, permissions, approval policy, hooks and logs, per installed harness version. I will not name a key the installed version has not been checked against.
- **N4 · decision.** A harness whose config format is unverified: `unknown` (honest) or `MISSING` (a fail in the exit-code vocabulary)? My provisional: `unknown` with the reason, because "expected and not there" is a claim about a format we have not confirmed. EJ's call.
- **N5 · decision · any count.** For the numbers with no existence meaning — instruction-file length, allow-list size, log retention — does EJ want a comparison value at all? If not, those rows report the number and stop there.
- **N6 · decision · U1's default.** Which harnesses do designs actually dispatch to in practice? That list is what `--harness` narrows to, and it is the set the verdict is about.
- **N7 · decision · U5's landing.** Which gate rule in `design_gate.py` (a new G-number?) treats the health group as a start condition, and what a `unknown` row does to it: block, warn, or nothing?
- **N8 · decision.** Does the report get compared against the previous run's report (drift), and if so, by readiness or by a separate step? My provisional: last, and by a separate `--compare`, because a check that reads two runs' state is a different instrument from one that reads a config.

## Costs and risks

- **A longer readiness.** The health group adds reads and lines to a step that runs at the front of every design and is meant to be cheap. My #6: the difficult work is made at the easy stage — so the cost is paid there on purpose, and it should be measured (readiness's runtime before and after, same machine), not assumed small.
- **Format drift makes a check quietly useless.** A key name verified today is wrong after a harness upgrade, and the check then reports something false with confidence. My #8: treating the sickness as a sickness is the only cure — so a check may not report `verified` without the version it was verified against recorded beside it, and after an upgrade its lines are expected to go to `unknown`, not to fail silently (my #6: 治之於未亂 — order it before it is in disorder).
- **A doctor that grips.** Any auto-fix that edits `~/.claude/settings.json` or `~/.codex/config.toml` can break a working machine, and the challenge already puts it out of scope. My #4: 執者失之. Snippet and handback only; the cost of that choice is that a person must still do the edit.
- **A green report that is mostly unknown.** Six harnesses, several formats unverified — the realistic first run is mostly `unknown`, which can read as failure and be ignored, or be written off. Cost is real and unavoidable; my #2 says the answer is not a verdict but naming what is not known, and my #14 says a long list of unknowns is itself the thing not to print — hence ten rows and drill-down.
- **One more rule in a method that already has many.** Each check adds a line to a method people must follow. My #18 (attributed): 吾所以告子，若是而已 — "What I have to tell you is this, and only this" — is the standard I would hold the design to: ten requirement rows, and nothing added to the ten.
- **Blocking would slow every design.** If N1 becomes "block", a design stops for a condition the person may not care about. My #13's cost named plainly: a gate that fires on a stale file is a gate people learn to bypass.

## How we would know I was right

- Every one of the ten rows shows a status, a proof (a command or a path) and, where a condition is not good enough, the exact file and key — and **no row shows a verdict that came from a number the script chose**. This is checkable by reading the output against the script.
- Each check is shown failing once on a planted wrong input before it is trusted, and the count of sabotages equals the count of checks that can fail. If any check has no sabotage, it is not finished.
- The Help block is proved by a test that plants a deliberately wrong snippet (wrong key name, wrong file path, a value that is a real secret) and fails if the help text changes to match the wrong input or prints the value.
- After one harness is upgraded, its rows go to `unknown` rather than reporting stale verdicts — one observed instance is the test (n=1).
- One run of a real design shows the **Found → effect on the design** table being used: the design names a different Guard stake, or a script check in place of an agent reviewer, and says which line of the health table caused it. The claim fails if the health table is printed and nothing in the design changes.
- The secrets test: every config file the doctor opens has a key planted in it, and the whole output — markdown and `--json` — contains no value. One run, machine-checked by grep.
- The cost measure: readiness's wall time before and after, same machine, recorded beside the run's evidence. If the added time is not worth the rows it produces, the answer is fewer rows, not a faster script.
