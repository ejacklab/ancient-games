# 孫子 (Sun Tzu) — is the check real, or is it the worker's good character?

## Answer

Do not mark a round MET on the part of it that rests on the worker not wanting to cheat. My #2 says rely on what cannot be attacked, not on the other side's restraint; my #12 says fix the conditions, not the person. Conditional on the facts as given — **no case file is held away from the builder before P4** — the eight checks are all legible to the worker, so each verdict below names the residue and how to close it.

- **R1 — strengthen the check.** The marker is real for execution with a side effect, in four commands, on one fixture; the rest of "reads, never runs" is the builder's honesty. Miss: the builder loads the target only in `find`/`where`/`callees` (not in the four run) or writes to `$TMPDIR` — no marker, no snapshot, MET. Add a fixture whose top level throws, run the whole command table against it, and instrument module loads from outside `src/`.
- **R2 — strengthen the check.** The fixtures verify the output, never the mechanism, so a builder can match member names instead of using the checker's implementation lookup and still satisfy `includes`/`ambiguous`. Miss: two interfaces with the same member name, one implemented in `src/` and one in a test file — the name-matcher resolves the wrong one and no fixture fires. Add that fixture, plus a test file whose path matches `--tests` but sits under no `test/` directory.
- **A5 — not loop-ready as a P3 tool MET.** The evaluator marks the agent half — "a whole map is produced unasked" — NOT CHECKED and defers it to P6, so A5's central failure is outside the check; limits are checked for presence, not truth. Miss: the agent runs `map .` for a one-place question, and the builder attaches one boilerplate `{reason:"other", …}` limit to every answer. Make "asked" machine-checkable in the case file, or stop reporting A5 as MET in P3.
- **A2 — strengthen the check.** Presence/absence of known links, the default depth and seen-once are real; completeness and the truth of "contradicts the code" off-fixture are not, and a *wrong* `dynamic`/`unresolved` label is never punished. Miss: a caller reached through a computed member call is dropped with no limit and no fixture exercises one. Add a computed-call fixture and hold out a real-opencode chain case (P4).
- **A3 — strengthen the check.** Count-versus-list and the fake rules are real; `throughFake`, `undecided` and evidence quality stand on the R2 link the fixtures do not fully test. Miss: a statically linked test through an uncalled same-named helper is listed and counted, or every doubtful test is parked in `undecided`. Add the uncalled-helper fixture and require `undecided` to appear only with its limit.
- **A1 — strengthen the check.** Locations and the no-sibling-rule case are real; sibling statuses and the entry set on real modules are not, because A6 is NOT CHECKED in P3. Miss: every sibling row returned `unclear` — legal under the spec, and exactly the "what siblings share and where they differ" the requirement wanted is not delivered. Add a fixture whose correct status is `shared` or `varies`, and fail `unclear` there.
- **L1 — strengthen the check.** The reason codes and the empty marker are checked; whether a stop reason is true, and whether a branch was dropped with no limit at all, is not. Miss: one blanket `{reason:"other", text:"static analysis only"}` on every answer passes every L1 case. Add a fixture where a limit must be absent, and a known-item fixture per reason code.
- **R3 — strengthen the check.** `unshare -rn` and the two snapshots bound a small part; the evaluator itself lists caught connection attempts, other processes, outside-tree writes and downstream training as unproven, and a missing `unshare` makes R3 NOT CHECKED. Miss: the builder attempts an upload, catches the failure and prints success; or caches private source in `$TMPDIR`. Snapshot `$TMPDIR` and make a caught socket/DNS attempt fail.

One residue sits under all eight: the frozen tests' *strength* is nobody's check — the sha256 freeze proves they did not change, not that they could fail. My #7 and #10 put it as the worker will strike where the check is empty; my #11 says the only foreknowledge that is not the worker's own is the kept-away case file. Until P4, call the loop guarded, not loop-ready.

## How I decided

1. my #2 ("Do not rely on their not coming; rely on having the means to meet them"): for each piece I asked what still holds if the builder satisfies the check and not the requirement. The part that holds only because the builder would not do that is the good-character residue.
2. my #12 ("seeks it in 勢 and does not demand it of people"; "he can choose his people and rely on 勢"): the remedy is always to move the ground — a different fixture, a held-out case, an instrumented runner — never to ask the builder to be careful.
3. my #1 ("More wins, fewer does not, how much less none at all?"; the chain "Ground gives rise to measurement… weighing to victory"): I compared each piece's Fails-if line against what the round actually measures. R1's own line is entangled with map/chain/tests/callers, and an R1 or R3 fault marks every requirement NOT MET — there the count is of the wrong thing, which my #1 forbids.
4. my #7 ("Attack where they are unprepared, and come out where they do not expect"; "These are the strategist's victories; they cannot be handed down in advance") and my #10 ("avoids the solid and strikes the empty"; "no fixed 勢 and no constant form"): the builder reads the frozen tests and the evaluator, and P3 holds nothing back, so the worker sees the whole check. That is a target, not a character test.
5. my #11 ("Foreknowledge … must be got from people who know the enemy's situation"; the converted spy "must be treated most generously"): the P4 answer keys, kept from builders, are the only foreknowledge the worker cannot manufacture. Before P4 there is none.
6. my #16 ("If orders are not clear and not drilled in, it is the general's fault; if they are clear and still not followed, it is the officers' fault"; "Generous but unable to direct, loving but unable to command … like spoiled children"): `unclear`, `dynamic`, `unresolved`, `undecided` and `{reason:"other"}` are legal escapes with no check on their use, so a clear order is not an enforced one.
7. my #15 ("The general has five dangers… These five are the general's faults"): I listed the escapes from step 6 as the worker's handles, each one a place the check can be turned against itself.
8. my #13 ("commands of the ruler not to be accepted"): I did not accept the brief's own acceptance list. Where "the evaluator reports MET" is not a check on that requirement (A5, A6, L2), I said so.
9. my reading (no item): on the evidence given — "the tests are not yet written, so not yet shown for them" — nothing establishes that the frozen tests can fail; the evaluator's 15-of-15 planted-answer record is evidence for the evaluator, not for the tests.
10. my reading (no item): I treat "the worker" as the builder whose `src/` the round judges, and where the reliance actually falls on Codex (test strength) or the COO (freeze, plants), I named that party instead.

## What I need to know

- Does P3 get any held-out case at all, or does all held-out checking begin at P4? If none, all eight verdicts weaken to "guarded by the builder's character."
- Is there a recorded pre-build failing run of the frozen tests? If yes, step 9 narrows; if no, test strength is unverified for all eight.
- Does the evaluator exercise the full command table on the marker fixture, or only map/chain/tests/callers? If full, R1 narrows.
- Is `unshare` guaranteed on the build host? If not, R3 can be reported NOT CHECKED and the round advance anyway.
- May a round be marked MET when the evaluator returns only NOT CHECKED parts (A5, A6, L2)? If yes, "MET" and "checked" differ and the loop's stop condition needs restating.

## Costs and risks

- Holding out cases (my #11) costs the builder fast feedback and can fail a round for an interface reason not in the spec — the price of a check the worker cannot target.
- Same-name and unconventional-test-path fixtures (R2, A2) cost evaluator work and a fresh plant each; without them the checks stay satisfiable by shape, not mechanism.
- Requiring a limit to be absent (L1) and a sibling status to be non-`unclear` (A1) risks false NOT MET on genuinely hard inputs; each needs its own fixture and plant, or it punishes honesty.
- Instrumenting the runner for socket/DNS attempts and `$TMPDIR` (R3) adds an evaluator dependency or a wrapper; the spec bars new *tool* dependencies, not evaluator ones, but it is work that can misfire.
- Calling A5 not loop-ready defers it to P6; that costs schedule, and the alternative costs a false MET.
- The deepest risk (my #1): a check that measures the wrong thing — R1 spending its three attempts on map/chain/tests/callers while the round says R1 — will close the round on a fault the round never named.

## How we would know I was right

Run one attempted cheat per piece against the check as written and report which produce NOT MET: (a) load the marker fixture from `find` instead of the four commands; (b) resolve a same-named member by name instead of the checker's lookup; (c) attach a blanket `other` limit to every answer; (d) drop a computed-call caller with no limit; (e) list a test through an uncalled helper; (f) return `unclear` on every sibling row; (g) stop a branch early with no limit; (h) attempt an upload and catch the failure. I am right if the pieces I called strengthen/not-loop-ready are the ones that pass their cheat, and wrong if any of them catches it. Two rounds per cheat — with and without the added instrument — and the count of NOT MET among those eight is the measure.
