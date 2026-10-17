# Workflow design — the leftovers, 3 hours, 3 rounds

The main design is `workflow-design.md`. This design covers only the work still open after round A5 closed. The
clock started at 2026-10-17T15:13Z (guard deadline D-148e43dc). The deadline is 18:13Z.

## Restatement

**Objective.** By the deadline:
- every requirement still open has had its build round: A2, A3, A1, L1, R3;
- P4 to P6 have run;
- P7 reports each item as MET, NOT MET or not reached, with the provisional decisions listed for EJ.

**Reading of "3 rounds"** (provisional, the COO's reading). A round is one pass over everything still open. Each open
requirement gets one build attempt per round. An item that fails goes back on the list for the next round, with its
defect as feedback. The run stops after round 3 or at 18:13Z, whichever comes first.

**Time-boxed rules (method 3.8 item 14).**
- A question goes to the experts, not to EJ. The COO decides provisionally.
- These still wait for EJ:
  - push;
  - deleting the private POC folders and the session logs;
  - edits to other designs (`REQUIREMENTS.md`, `CODE_GRAPH.md`);
  - the skill's slug fix;
  - spending beyond the limit.
- The requirements document is not edited. Its wording is EJ's. The provisional wording goes into the report as a
  proposal, and the tests follow it.

## Decisions to make first (experts, 15 min)

Settled in one `experts-decide` run: six experts, question `briefs/leftovers/decisions-question.md`, out
`experts-leftovers/`. The COO picks provisionally and logs each pick with its full text in `decisions.md`.

| # | Decision | What it changes |
|---|---|---|
| 1 | Does a known link that the tool marks `dynamic` count as missing? | A2's tests |
| 2 | Does going into a body written straight into a call add a level? | A2's tests, depth on opencode |
| 3 | Define "known": no definition, Linus's wording, or 老子's wording | A2's tests |
| 4 | Does A5 say "a limit the interface requires for that command is part of the answer"? | wording only |
| 5 | One Fails-if line naming both actors, or a tool line and an agent line | wording only |
| 6 | A3's fake rule: does a test that swaps in a fake reach the real function? | A3's tests |
| 7 | A1's sibling rule: which files count as siblings | A1's tests |
| 8 | What counts as a "test file" | R2, A3 |

Three things the run fixes without asking. Each is an L1 fault found in the code:
- `find` keeps only the best tier of matches and says nothing about the rest;
- `reachableFrom` stops at 400 visits with no limit;
- no A5 case runs `callers`.

## Two lanes

They share no files and no engines.

| | Lane A: build | Lane B: measure |
|---|---|---|
| Work | P3 rounds A2 → A3 → A1 → L1 → R3, the agreed order | P4 maps, P5 L2 one round, P6 integration |
| Engines | Codex (tests), opencode (build) | Claude subagents and `claude -p` |
| Writes | `code_map/` | `runs/…/p4/`, `p5/`, `p6/` |
| Tool used | the live `code_map/src` | a frozen copy, taken at the start (`p4/tool-a5/`) |

Lane B runs on the tool as it stood when A5 closed. Its numbers are labelled with that version. A later fix in Lane
A does not reach them. That is the price of fitting both lanes into 3 hours.

### Lane A — one requirement per step

| Step | Who | Check | Time box |
|---|---|---|---|
| Tests | Codex gpt-6.1-sol, high effort, brief from `briefs/p3/tests-codex.md` with the provisional decisions | the new tests fail on the current tool; COO scope check: nothing outside `test/<req>/` changed | 10 min |
| Freeze | COO, `round_check.py freeze` | file count | — |
| Build | opencode MiniMax-M3.1-Flash-Preview, agent build | — | 30 min (was 60; R2 attempt 2 hit the hour and its code still passed) |
| Round check | COO, `round_check.py check <REQ> <round> --met <MET so far>` with the three held-out sets | PASS or FAIL | 12 min |
| Plants and review | COO plants in private copies; 孫子 and 范蠡 read-only on a copy of `src/` | caught or missed; APPROVE or CHANGE | in the background, while the next requirement's tests run |

- A FAIL, or a CHANGE tied to a requirement line, puts the requirement back on the list for the next round, with
  feedback that names the defect's shape.
- A requirement that fails all three rounds is reported NOT MET.
- While a build runs, Codex writes the next requirement's tests into `staging/test-<req>/`, outside `code_map/`.
  They are copied in after the round check. This keeps the frozen snapshot and `bun test` clean.

### Lane B — runs once, in order

1. **P4 (A6).**
   - The COO runs `map` from `p4/tool-a5/` on the three modules.
   - The evaluator runs A1's checks on each map.
   - A Claude judge scores each map blind against the P1 keys: wrong, missed and correct.
   - Map size is compared with source size.
2. **P5 (L2), round 1 only.**
   - Three modules × two arms (map, and read/grep only), Claude subagents on the same model, the module's fixed
     questions.
   - The COO scores them against the keys and records tokens and time.
   - Rounds 2 and 3 (improve the map, rerun) run only if time is left.
3. **P6.**
   - The COO packages a `code-map` skill (`SKILL.md` plus the frozen tool) inside `p6/`.
   - One real change task per module.
   - Two `claude -p` runs each, with and without the skill.
   - A blind Claude judge, and a script for the counts.
   - Linking the skill into `~/.claude/skills` is harness config, which waits for EJ, so P6 loads it per run from
     the `p6/` folder.

## Budget (my estimate, not measured)

| Time (UTC) | Lane A | Lane B |
|---|---|---|
| 15:13–15:35 | design, decisions | P4 |
| 15:35–16:20 | A2 | P5 |
| 16:20–17:05 | A3 | P6 |
| 17:05–17:50 | A1 | P6 judge, P5 round 2 if time |
| 17:50–18:00 | L1 starts; it is stopped at 18:00 if not done | — |
| 18:00–18:13 | P7 report, insight, success path, local commit | — |

**Expected:** round 1 reaches A2, A3 and A1. L1 and R3 are probably not reached, and rounds 2 and 3 are not
reached at all. The time box bounds the run; the work list is longer than 3 hours at the speed seen so far (an
attempt took 20–60 min). The report says which items were not reached. No item is cut silently.

## Criteria (scored at the end; aims, not gates)

1–5. A2, A3, A1, L1, R3: each has a round check PASS with no regression.
6. A6: three maps, each with A1 MET.
7. L2 report: correctness, build cost, reading tokens, time, wins and losses.
8. P6 report: the with-and-without comparison.
9. P7 report: each provisional decision, with its full text.
10. A local commit. The private paths stay excluded and the secret scan is clean. Push waits for EJ.

## Predictability, debuggability, quality control

- **Predictable:**
  - a fixed order;
  - a time box on every step;
  - a stop at 18:13Z.
- **Debuggable:**
  - one `state.md` line per step;
  - evidence in `evidence/` and `p3/`, `p4/`, `p5/`, `p6/`;
  - progress lines through `deadline status`.
- **Quality control:**
  - the builder writes none of its tests, checks or reviews;
  - held-out sets;
  - planted faults per round;
  - the L2 and P6 arms use the same model, so only the input differs.
