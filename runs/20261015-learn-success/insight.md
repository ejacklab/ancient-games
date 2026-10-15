# Insight — run 20261015-learn-success (the main agent's session)

## F-cf3f3a6e — the guard suite was red during the parallel build

Whys:
1. Why was the run red? 22 tests from rounds 1–4 asserted "a passing call writes no record", and one round-5 path test expected a child with no aim to fail.
2. Why did the old tests fail? Round 5 S1 makes a passing call write a `success` line, which those assertions forbid; the code worker followed the newer SPEC and was not allowed to change tests.
3. Why was that not settled before the parallel start? The COO's round-5 spec did not list which older assertions S1 contradicts, so the conflict surfaced only when the pieces met.
4. Why was the aim test red? The paths worker read "aim must name a measure" as applying only when an aim is present; the spec did not say a child must have one in so many words.
Source: instruction (the round-5 spec, the COO's)
Root cause: the spec for a parallel build named new behaviour but not the older assertions it overturns, nor one required field in plain words.
Options:
1. [rule] A spec that changes behaviour lists the older tests it contradicts, so the test writer updates them in the same round. evidence: the 22 assertions in test/hooks.test.ts, round3.test.ts, round4.test.ts, updated by the COO after the fact.
2. [check] Before a parallel start, run the old suite against a one-line stub of the new behaviour to see what it breaks. evidence: S1's stub (write a success line) would have shown the 22 at 14:51.
3. [tool] The guard's D1 should read bun's own summary ("23 fail"), which it missed — it logged "21 error" from other text. evidence: this record's actual field against the bun output of the same run.

## F-1b6f6a0f — a lookup command ended with exit 2

Whys:
1. Why exit 2? The command's last part, `ls .claude/skills/workflow-design/guard/.harness-guard`, listed a folder that does not exist.
2. Why list it? The main agent checked whether the guard had written state inside its own package folder, which it never does — the journal lives at the git top-level.
3. Why that guess? The main agent did not use the guard's own `guardRoot` rule when it looked.
Source: instruction
Root cause: an exploratory check written without the guard's own location rule; harmless, but an errored call by R12.2.
Options:
1. [rule] Look for guard state at the git top-level only (`.harness-guard/` there). evidence: SPEC Common, guardRoot.
2. [tool] Add `cli.ts where` that prints the guard root and journal path for the current folder. evidence: this lookup.
