# 孫子 (Sun Tzu) — review of the `researcher.md` draft

## Answer

The file is right in shape — the routing description, the source-date rule, the fetch-before-quote rule and the digest-only pass-back are sound — but it is not yet right in enforcement: it omits the repo's own control-query row, which the machine check fails without; it inlines a findings table that contradicts the template it tells the worker to copy; and it leaves its one hard boundary (where `Write` may go) as prose the harness does not enforce. Fix those three, then the smaller items; a "no" here should be an explicit decision, not an omission.

## How I decided

**0. I counted first, and read the primaries, not the brief's summary.** I read the actual file (73 lines), the two check scripts, the template, `TASK_TYPES.md` and the method; then searched the web and read one community digest on Claude Code subagent definition (an official docs fetch returned only navigation, so I could not verify its field table first-hand). The web evidence below is *reported*; the file and script evidence is read (my #1, my #11, my #4).

**1. (matters most) The control-query row is missing — the file cannot pass its own check.** `check-findings.py` fails a findings file that has no control row: its `check()` ends with `if CONTROL not in text.lower(): bad.append(f"{path.name}: no control-query row (the MagmaMem sabotage did not run)")` (quoted, `runs/20261011-agent-memory-graph/check-findings.py`). The draft's item 6 at lines 52–54 says only "Not found is an answer"; it never tells the worker to run a planted control or to write its row. Add a ninth standard item after line 57: "**A control query.** If your brief names one thing that must not exist, run it and give it a row: claim = NOT FOUND, label `unknown`, source = the exact queries you ran. Write that name only in that row, nowhere else, and not in the digest." Rationale: the control is the probe that tests the one thing every label rests on — whether the worker read anything at all (my #11, my #17, my #7). *My reading:* this is a deterministic failure, not a judgement call, so it outranks everything below.

**2. The inlined table contradicts the template the worker is told to copy, and the repo has three label vocabularies.** The draft says "read it first, fill it exactly" (line 17) then inlines a table with four labels (`verified / reported / unknown / unproven`) and a Source of `<URL> (<source date>), quoted: "<verbatim>"` (lines 21–31). The template has three labels and Source `<URL, or file:line>` (`docs/workflow-templates/research-file.md`, lines 14 and 20). `check-findings.py` uses the four (`LABELS = ("verified", "reported", "unknown", "unproven")`); real repo files use three (`docs/research/20261002-workflow-feedback/FINDINGS.md`: 33 `verified`, 17 `reported`, 2 `unknown`); `TASK_TYPES.md` line 100 uses the uppercase four (`CONFIRMED/INFERRED/GAP/UNPROVEN`). "Fill it exactly" is impossible as written. Fix: make one copy authoritative — *my reading* is the code wins, so update `research-file.md` to the four labels plus date and quote, delete the inlined table at lines 21–31 in favour of the pointer, and add one line mapping the TASK_TYPES uppercase names to the lowercase set. Rationale: three vocabularies cannot all be right, and a second copy of a table drifts — this one already has (my #4, my #12).

**3. The write boundary is instruction-only, and `Write` is unrestricted.** Line 15 says "You read anything; you write only there", but the tool list cannot restrict `Write` to a folder. Current practice supports a `PreToolUse` hook in subagent frontmatter (*reported*, [community digest](https://raw.githubusercontent.com/rodrigorjsf/agent-engineering-toolkit/refs/heads/development/docs/general-llm/subagents/research-subagent-best-practices.md); [official subagents docs](https://code.claude.com/docs/en/sub-agents)). Fix: add a hook that rejects a `Write` whose path is not under `docs/research/` or `runs/`, and keep line 15 as the explanation. If EJ will not accept a hook, then line 15 must say the scope is a claim the main agent verifies — not a rule the harness enforces. "If orders are clear and still not followed, it is the officers' fault" only holds if the orders are enforced (my #16, my #2, my #12).

**4. The check is unnamed and the worker cannot run it.** `validate_result.py --kind digest` enforces exactly `**Answer`, `**Confidence`, `**Decision it triggers` and caps the digest at 20 non-empty lines (`DIGEST_HEADINGS`, `--max-lines default 20`). The draft's lines 33–34 say "the template's five bold parts" and never name the script; the worker has no `Bash`. At lines 33–34, write the three enforced parts explicitly (the other two are still required); at line 42, name the command. Then either add `Bash` under a hook allowing only that command, or state plainly "the main agent runs the check; you cannot" — and make that the dispatcher's step. A check the worker cannot run is a check the worker cannot satisfy (my #16, my #8).

**5. The description silently competes with the repo's engine assignment.** `TASK_TYPES.md` lines 98 and 100 assign `web search` and `research and reports` to `agy` (EJ, 2026-10-04); line 3 of the draft routes web-source research to this Claude Code subagent and says nothing about the relation. Add one clause: "This is the Claude Code path for a hand-off the main agent cannot do herself; a node whose engine is `agy` per TASK_TYPES is not this subagent." Rationale: count before committing the node, and name the ground before acting on it (my #1, my #19).

**6. The run-path rule is ambiguous about two files.** Method 3.8 item 4 wants one result file per call at `runs/<id>/nodes/<node>-<attempt>.result.*`; item 9 puts the two research files at `docs/research/<date>-<topic>/`. Lines 13–14 say "your result file goes to `runs/<run-id>/nodes/`" while line 17 requires two files; real runs are split (`runs/20261005-code-graph-tool/FINDINGS.md` at the run root; `docs/research/.../FINDINGS.md` elsewhere). Pin the names for the run case, or always write the pair under `docs/research/` and return the digest as the node result (my #1, my #12).

**7. `maxTurns` is absent.** Current practice recommends a turn cap (*reported*, same digest); the method gives research a wall-clock of about 10 minutes (3.8 item 2) but no turn figure. Add `maxTurns` with EJ's number — I will not invent it. A force that cannot be told to stop is not under command (my #13, my #8).

**8. More than it needs.** Line 5 `model: inherit` is the default (a no-op, though harmless as documentation); lines 64–66 repeat both the description's "not this repo's code" and CLAUDE.md's `/tmp` rule, which the subagent already receives through project memory. Trim to a pointer. Move on advantage only (my #5, my #14).

**9. What is right, and should not be lost in the edits.** The description's two NOT clauses correctly keep the main agent on small research (my #3, my #19); the source-date rule at lines 44–45 (my #1); "a snippet is not a read" at lines 46–47 (my #11); both rows on disagreement at line 51 (my #6); the "Fail looks like" list at lines 59–60 (my #15); and the digest-only return at lines 72–73 (my #7, my #8). *My reading:* these are the file's real value, and each of my fixes should leave them intact.

## What I need to know

1. Is `check-findings.py` to be promoted out of `runs/20261011-agent-memory-graph/` into a stable script, and must the control name stay out of every file a worker reads? (decides 1 and 4)
2. Which label set is authoritative — the three in `research-file.md`, the four in `check-findings.py`, or the uppercase four in `TASK_TYPES.md`? (decides 2)
3. May the researcher hold `Bash` under a `PreToolUse` hook, or is "the main agent runs the checks" fixed? (decides 3 and 4)
4. For a run, which filenames — `<node>-FINDINGS.md`/`<node>-DIGEST.md`, or findings under `docs/research/` and the digest as the node result? (decides 6)
5. What `maxTurns` value does the research budget imply? (decides 7; *not measured* by me)

## Costs and risks

- A `PreToolUse` hook is a script to maintain, and a fail-closed path check can block a legitimate write when a brief names a folder outside the two roots (my #16, my #2).
- Aligning the label set touches the template, `TASK_TYPES.md` and old runs; done piecemeal it leaves a third vocabulary (my #12).
- Adding `Bash` to a web-fetching agent widens the blast radius; the hook, not the prose, must be the guard (my #14, my #4).
- Keeping no `Bash` means the main agent pays a second hand-off and discovers a bad digest after the researcher's context is gone (my #8).
- Naming the control inside `FINDINGS.md` can void the control for any later worker who reads that file; keep it to the one row and out of the digest (my #7).
- Trimming the description too far risks the failure the file exists to fix — the main agent not delegating at all (my #3, my #19).

## How we would know I was right

**Test.** Run one brief with a planted control (a name that must not exist) and one genuine external question through the researcher. Pass means: `validate_result.py DIGEST.md --kind digest` exits 0; `FINDINGS.md` has at least five rows including a control row reading NOT FOUND; every label comes from the single authoritative set; no written file lies outside `docs/research/` or `runs/`; and a false quote planted in a fetched page lands as `unknown`, never `verified`. Today the control row is absent, so `check-findings.py` exits 1 — that is the observable difference (my #17, my #1).

**Measure.** Main-agent repair turns after the researcher returns: target zero; and digest non-empty lines ≤ 20. Before the fix, expect at least one repair turn on the control (my #8, my #20).
