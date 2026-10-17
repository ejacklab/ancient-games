status: done

One sentence: the Round 17 acceptDone. Tests written at `.claude/skills/workflow-design/guard/test/round17-crossed.test.ts` — 15 cases, all passing (15 pass / 0 fail, 256 expect() calls), `tsgo --noEmit` clean; progress and result files written, nothing committed.

- V2 group (warning `R12.2-command-error`): F-bdea5631's `bun test …; ls <gone>` shape, `&&`, `||`, `timeout 60 …`, `env -u NO_COLOR …`.
- V1 group (failure `R12.2-test-failed`): piped to `tail`/`grep`, last after `cd … &&`, two runners, a not-last runner whose summary speaks, plus D1/D2 controls (other command's stdout, interrupt).
- CONTRADICTS: none; one underdetermined point noted in the result (which runner label a two-runner call's `input` names).
st.ts; ls /tmp/gone-worktree` (F-bdea5631's shape) | 2 | warning `R12.2-command-error`, `ls call`, `exit 2` |
| `pytest -q && echo done` | 1 | warning, `echo call`, `exit 1` |
| `pytest -q \|\| echo fallback ran` | 1 | warning, `echo call`, `exit 1` |
| `timeout 60 bun test …; ls /tmp/gone-worktree` | 2 | warning, `ls call`, `exit 2` |
| `env -u NO_COLOR pytest -q && git status` | 128 | warning, `git call`, `exit 128` |
| `pytest -q ; ls /tmp/gone-worktree` (evidence facts: exit and command word, no output text) | 2 | warning, `ls call`, `exit 2` |

V1 — the runner made the exit, or its own summary says so (Round 17 V1):

| command | exit | verdict asserted |
|---|---|---|
| `pytest -q 2>&1 \| tail -3`, no summary | 1 | failure `R12.2-test-failed`, `pytest run`, `exit 1` |
| `bun test test/round17.test.ts \| grep -n failed`, no summary | 1 | failure, `bun test run`, `exit 1` |
| `cd work && pytest -q` | 1 | failure, `pytest run`, `exit 1` |
| `pytest -q ; cargo test` | 1 | failure, `exit 1`, input `pytest run` or `cargo test run` |
| `pytest -q ; ls /tmp/gone-worktree`, output holds `3 failed, 2 passed` | 2 | failure, `pytest run`, `3 failed` |
| `timeout 60 env -u NO_COLOR pytest -q && ls …`, output holds `2 failed, 9 passed` | 2 | failure, `pytest run`, `2 failed` |
| `pytest -q 2>&1 \| tail -3` (PostToolUse, stdout summary) | — | failure, `pytest run`, `4 failed` |
| control: `pytest -q ; ls …` (PostToolUse, summary in another command's stdout) | — | no record |
| control: `cd work && pytest -q` with `is_interrupt` | 1 | no record |

Each case also asserts exactly one record in the journal (no second failure, no warning, no other kind), the id form
(`F-`/`W-` + 8 hex), `session`, `harness`, `found_by` for the failure, a non-empty reason, an evidence file that exists and
parses, and the one context line (D4's "already in the journal" for a failure, Round 9's `harness-guard warning <id>` plus
`dismiss` for a warning). Planted output text (`PRIVATE-OUTPUT-4b91ce`) is checked absent from the result, the journal and
every state file before each behavioural assertion.

## Command and its last lines

```
cd .claude/skills/workflow-design/guard && bun test test/round17-crossed.test.ts
```

```
bun test v1.4.3 (c6da4a4d3)

 15 pass
 0 fail
 256 expect() calls
Ran 15 tests across 1 file. [81.00ms]
```

Counts: 15 tests, 15 pass, 0 fail, 256 `expect()` calls. `bunx tsgo --noEmit -p .` in the same folder exits 0.

## CONTRADICTS

none.

One underdetermined point, not a contradiction: with two runners (`pytest -q ; cargo test`) V1 judges the call by the last
test-run segment, but D1's record says `input: "<runner> run"` and the specification names no canonical label for which of two
runners it is; the case therefore accepts `pytest run` or `cargo test run` (the code writes `pytest run`, the first run's
label). If EJ wants one rule, the SPEC line to add is Round 4 D1's `input: "<runner> run"`.