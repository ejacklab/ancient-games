# 孫子 (Sun Tzu) — can the engines, the task and the ground carry each piece?

## Answer

**Half known overall: only P0 is whole.** The engines and tools are proved by use; the task is proved attackable at one point (R2 on a single call site) and held elsewhere by inference; the ground is real files on a draft blueprint with a half-verified key set. My #4 states the condition exactly: 「知吾卒之可以擊，而不知敵之不可擊，勝之半也……知敵之可擊，知吾卒之可以擊，而不知地形之不可以戰，勝之半也」 (`quoted`, my #4) — I read 吾卒 as engines and tools, 敵 as the task as posed, 地形 as the ground. No spot should be dropped on my account; a drop is a question for EJ, not a removal.

Verdict by spot (Can = engines/tools can do it · Doable = the task as posed can be done · Permitted = the ground permits it; *half* = proved on part of the front, or the proof is of a different thing):

| Spot | Can | Doable | Permitted | My verdict |
|---|---|---|---|---|
| U1 | — | yes on the draft | **half** (draft, not settled) | question for EJ; blocks only the pieces that build |
| U2 | **half** (one call site) | **half** (static Effect rule inferred, never run) | yes (94 tags in files) | probe the breadth before P3 |
| U3 | **half** (never run) | **half** (no tool read does A3; four-step method only inferred) | yes (tests and mocks present) | least known; bound it before P3 |
| U4 | yes (AST walk) | yes once defined | yes | the half is the definition; take spec v0 unless EJ corrects it |
| U5 | **half** (shape test unproved) | **half** | yes (plugin/provider folders present) | prove on one folder with a known answer |
| U6 | yes for exact text, **half** for words | yes | yes | "good enough" is EJ's threshold; I set none |
| U7 | yes | yes | **half** (stronger key methods named, not run) | half; get a second method (see N4) |
| U8 | **half** (run-time capacity) | yes | — | prove a fallback or record the stop (my #2) |
| N1 (mine) | **no as written**: `unshare -n` fails here | yes, via the Node preload | **half** | prove the fallback before P2 |
| N2 (mine) | **half**: `--output-format json` exists; token fields and pinned model unproved | yes | yes | prove the instrument before P5 |
| N3 (mine) | yes | **half**: "blind" is undefined | yes | define it, or P6's check is not evidence |
| N4 (mine) | the check runs | **no**: it cannot check readings | — | P1's named check does not check what P1 needs |
| N5 (mine) | **half**: no program built over `packages/ai` | yes | yes | prove the third module before P4 |

## How I decided

1. **The question is my #4, third half.** The half-victory passage above gives three tests — our troops can attack, the enemy can be attacked, the ground permits battle. I applied all three to every piece; a piece is whole only when all three are proved (`quoted`, my #4).

2. **I did not answer from the labels; I touched the ground.** I read the pieces P0–P7, `spec.md`, `result-trimmed.md`, `readiness.md`, `DIGEST.md`, `FINDINGS.md`, the probe summary and the state file, and I ran four read-only checks of my own: `unshare -n true` → `unshare: unshare failed: Operation not permitted` (exit 1); `claude --help` → `--output-format <format>` offers `"text"`, `"json"`, `"stream-json"`; the three proposed module directories exist; `packages/ai` is a separate TS project (217 `.ts` files, its own `tsconfig.json` and `typecheck` script). This is my reading and my measurement — my #17: 「角之而知有餘不足之處。」 (`quoted`, my #17).

3. **Piece by piece, the three tests (my #4):**

| Piece | Engines/tools (吾卒) | Task (敵) | Ground (地形) | Verdict |
|---|---|---|---|---|
| P0 | known | known | known | **whole, except U8** |
| P1 | known | **half** | **half** | half — U7, N4 |
| P2 | **half** (Codex quota) | **half** (L1/A1 checks need keys; R3 check N1) | **half** (draft) | half — U1, U8, N1 |
| P3 | **half** (R2 at one point; A3 unrun) | **half** (R2 attackable; A3 inferred) | **half** (U1, U4, U5, U6) | half — the load-bearing piece |
| P4 | **half** (depends on P3) | **half** (A1 needs U4/U5) | half (files yes; keys U7) | half — U4, U5, U7 |
| P5 | **half** (arms named; reading N2) | known (result may be a loss) | half (keys U7; needs R2/A5 MET) | half — N2, U7 |
| P6 | **half** (judge blindness N3) | known | half (tool must exist; tasks unchosen) | half — N3 |
| P7 | known | known | half (reports P4–P6) | whole as a reporting piece |

4. **P0 is the only reckoning, and it stops at 度.** My #1 gives the chain 「地生度，度生量，量生數，數生稱，稱生勝。」 (`quoted`, my #1). Readiness counts tools, installs and compiles — that is 度 (measurement). What it does not do is weigh the task's breadth: one call site against 94 tags, one package against the third module (`quoted`, my #1).

5. **P1 is half, because foreknowledge came from reading only.** My #11: 「先知者，不可取於鬼神，不可象於事，不可驗於度，必取於人，知敵之情者也。」 (`quoted`, my #11). The keys came from one reader's grep and eye; `state.md` records 43 ran claims (grep only) and 145 read, with tsc and opencode's tests not run. `quote_check.py`'s own docstring says it "cannot tell whether the explorer's reading of the code is right — that is what `ran` claims are for." The ground permits a stronger method; it was not used (U7, N4).

6. **P3 is where the half bites.** One `getImplementationAtPosition` hit at `edit.ts:275 → permission.ts:231` is one 角; the static Effect rule (I5) and the test-link method (I7) were never run. My #14: 「故小敵之堅，大敵之擒也。」 (`quoted`, my #14) — a small proven force holding stubbornly against a wide front. My #15 names the two failure shapes: 「夫勢均，以一擊十，曰走」 and 「將不能料敵，以少合衆，以弱擊強，兵無選鋒，曰北。」 (`quoted`, my #15). A3 is the piece of the front most likely to fail first.

7. **P5 and P6 are half in their instruments, not their idea.** The measurement is the objective's own measure (L2), so the instrument must be reckoned before it is used — my #1 — and touched to know its surplus — my #17. N2, N3.

8. **Order, not subtraction: my #3.** 「故上兵伐謀，其次伐交，其次伐兵，其下攻城。攻城之法，為不得已。」 (`quoted`, my #3). Settle the plan-level spots (U4, U5, U6's method) and the instruments (N1–N5) before P3's walled city. I propose no drop.

9. **Do not rely on the ground you do not own: my #2.** 「無恃其不來，恃吾有以待之；無恃其不攻，恃吾有所不可攻也。」 (`quoted`, my #2). For U8, N1 and N2 that means a named fallback — a substitute engine, the Node preload, a watched token reading — or a recorded stop.

10. **Blame the method, not the reader: my #12.** 「故善戰者，求之於勢，不責於人，故能擇人而任勢。」 (`quoted`, my #12). The keys' blind spot is a property of one method (U7); fix the conditions with a second, independent method (N4).

11. **Name the ground, then act: my #19.** 「九地之變，屈伸之利，人情之理，不可不察也。」 (`quoted`, my #19). The blueprint ground is draft for P3–P6: research and design may run on it, the building pieces may not (my reading of method 3.1's blueprint rule).

12. **Probe cheaply and let the plan change: my #8 and my #10.** 「故兵聞拙速，未睹巧之久也。」 (`quoted`, my #8) — bound each probe rather than discover the front inside an attempt limit. 「故兵無成勢，無恒形，能因敵變化而取勝者，謂之神。」 (`quoted`, my #10) — the spot table changes with what the probes show.

13. **One small ground note (my measurement):** opencode's local `.bin` holds `tsc`, `tsgo`, `tsgolint` but no `tsx`, so the spec's second run form (`npx tsx`) is not presently proved locally; the `node code_map/dist/cli.js` form is. A one-line risk, not a spot.

## What I need to know

- **U1/Q5:** does the 2026-10-14 "go" accept `result-trimmed.md` as it stands, or does P3 still wait for acceptance? This changes whether P3 may start at all.
- **U4:** is the spec's entry-flow definition — a function nothing in the module calls, or one exported and used outside — the accepted one?
- **U6:** what makes `find`'s word ranking good enough? No threshold is given, and I will not invent one; that is EJ's.
- **U8:** if Codex quota is out, which engine writes the tests and the evaluator, or does that piece stop?
- **N2:** which model is pinned for both arms of P5 and P6?
- **N3:** what must the P6 judge not see for it to count as blind?
- **N5:** must the third A6 module be `packages/ai`, or may a second `core` module replace it at lower proof cost?

## Costs and risks

- **R2 and A3 built on one probe** (U2, U3; my #14, #15): the attempt limit may be spent discovering that the front is wider than one call site. Cost: rework inside P3.
- **Draft blueprint** (U1; my #1, #2): the evaluator and the build may check the wrong thing. Cost: P2 and P3 redone.
- **Codex as the only test and evaluator writer** (U8; my #2, #18): the loop stalls when the engine flags. Cost: wall time, not a wrong answer. My #18's 「以近待遠，以佚待勞，以飽待饑」 (`quoted`, my #18) says schedule the heavy load on the rested engine, not the spent one.
- **R3's check** (N1; my #2): R3 may report NOT CHECKED. Cost: one unmet requirement and a weaker report — but not a false one.
- **The L2 instrument** (N2; my #1, #17): the objective's own number may be unreportable. Cost: the headline measurement missing.
- **An undefined blind judge** (N3; my #4): P6's comparison reads stronger than it is; a check that cannot check is the 3.2 failure.
- **Keys verified only for location** (U7, N4; my #11, #12): P4 and P5 could credit the tool where both it and the keys are wrong — a false MET.
- **The plan's own length** (my #8): 60–110 engine calls over several days is itself a cost; the cheap probes above are what shorten it. I do not propose removing steps.
- **My limits:** these verdicts are my reading of the given facts plus five small checks of my own; n=1, and I did not run the tool.

## How we would know I was right

Run the bounded probes **before P3's first round**, each written with its prediction first (my #1: reckon, then fight):

- **(a) R2 breadth:** the miss rate of `getImplementationAtPosition` over a fixed sample of Effect call sites — not one. Prediction: it is material (non-zero), which makes the static Effect rule load-bearing; if it is ~0, U2 was not a risk and I was wrong.
- **(b) A3 link:** reproduce the mock-link method by hand on one test file whose answer the keys already hold. Prediction: it reproduces for the real node and fails or needs a rule for `.replace` mocks — if it reproduces cleanly, U3 was only half known.
- **(c) R3 check:** a `node` preload that throws on a deliberate socket call. Prediction: passes, replacing the failed `unshare -n`.
- **(d) P5 instrument:** one `claude -p --output-format json` run with a pinned model, showing the token fields. Prediction: passes.
- **(e) N4 by test:** run `quote_check.py` against a deliberately wrong reading of a correctly quoted line. Prediction: it passes, confirming that the check checks location and not correctness.

I was right if at least one of (a), (b) or (e) changes the spot table or the piece order before P3 starts; I was wrong if P3's first round on R2 or A3 fails for a reason these probes would have found. Each probe stops at the bound named before it runs, or it is not a probe but a build (`quoted`, my #8).
