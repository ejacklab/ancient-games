# Four experts — P3 loop check (method 3.5)

Question: `../briefs/p3-loop-check.md`. Asked: Linus, 范蠡, 孫子, Dave.

| | Linus | 范蠡 | 孫子 | Dave (control) |
|---|---|---|---|---|
| Answer (one line, my reading) | not loop-ready: the command is broken, R1 depends on later work, the answer checks accept false claims | not loop-ready: R1 deadlocks, and a block poisons later rounds | strengthen every round; the loop is "guarded, not loop-ready" until a held-out set exists | strengthen: a lookup-table stub scores 8/8 MET; R1 not loop-ready in first place |

## Where they agree

- **R1 is coupled to map, chain, tests and callers**: all four. Fix: judge R1 on the marker and the exit status alone
  (Linus, Dave, 范蠡's first choice), or move R1 later (范蠡, Dave's alternative) (*quoted*).
- **The evaluator command has no `--out`** and exits 2: Linus and Dave, both ran it (*quoted*, measured).
- **The answer checks test shape, not truth**: Linus measured five false answers that are accepted (sibling text,
  flow return text, a chain rooted at the wrong function, a test-path site on the wrong line, an unasked chain on a
  `where` answer); Dave measured that the canned stub passes 8 of 8; 孫子 names the same gap per requirement
  (*quoted*).
- **R3's MET covers only the bounded check** (`unshare -rn` plus snapshots); a caught connection attempt is not seen:
  Linus, 孫子, Dave (*quoted*).

## Where they disagree

| Point | Positions |
|---|---|
| When a requirement is blocked | 范蠡: halt the loop. Design: move on. *My reading:* 范蠡's reason is the spillover (an R1 or R3 fault marks every requirement NOT MET); removing the spillover removes the reason. |
| How to stop a lookup table passing | Dave: a held-out copy of the fixtures, lines shifted and names changed, never seen by the builder. 孫子: more fixtures (same member name in two interfaces, a computed call, an uncalled helper, a sibling row that must be `shared` or `varies`, a limit that must be absent, a top level that throws). Linus: relationship checks (text against its location, chain roots and parent-child links, test-path endpoints, no unasked sections). Not exclusive. |

## What each added

- **Linus:** default text mode and runs without `--tests` are untested workflows.
- **范蠡:** a reviewer CHANGE must count against the 3 attempts, or review rounds are unbounded.
- **孫子:** a test file that matches `--tests` but is under no `test/` folder; snapshot `$TMPDIR` for R3.
- **Dave:** hash every file under `code_map/` outside `src/` (tsconfig, package.json, bun.lock, no bunfig.toml);
  per round, the COO plants 3–5 faults in `src/`; one reviewer control (a diff that hard-codes a fixture answer).

## What the COO does with it (method 3.5: a failure the check would miss strengthens the check)

1. Codex repairs the evaluator (it wrote it): R1 and R3 decoupled and no spillover; Linus's relationship checks; 孫子's
   fixtures; a held-out generator that shifts lines and renames identifiers, run by the COO with a seed the builder
   never sees.
2. The COO reruns the 15 plants, Linus's 5 false answers, and the stub on a held-out copy (Dave's prediction: 30 or
   more of 37 NOT MET).
3. Round check: `--out` added; snapshot of all of `code_map/` outside `src/`; 3–5 COO plants in `src/` after a round
   passes; a reviewer CHANGE uses one of the 3 attempts; move on when blocked (kept: the spillover is removed).
4. The round order stays as designed. R3 and A5 report their unchecked parts beside MET.

## Check

`four_experts.py check`: 4 answers pass; the 老子 FAIL is expected (not asked). Engines: Linus codex, 范蠡 agy (no
fallback), 孫子 dsh, Dave a Claude subagent. The check script was written by Claude and checks sections and citations,
not whether a rule was applied well.
