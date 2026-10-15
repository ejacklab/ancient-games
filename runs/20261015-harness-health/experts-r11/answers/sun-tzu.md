# 孫子 (Sun Tzu) — label the harness list at readiness; do not pretend to verify it there

## Answer

Keep the list as a set of lines readiness **labels** — `verified` / `reported` / `unknown` / `MISSING` — and do not let readiness claim to *verify* a line whose evidence only exists after dispatch. Change seven lines so each names its observable and its check, split three (R2, R6, R9) because each is several rules in one sentence, and drop none: every one of the twelve names a real failure. Do not enforce the 80% until Q1 and Q2 are answered. My reading of the facts you gave: the built check scores 0 of 7 because it reads **config**, while all seven recorded failures were **behaviour at dispatch** — it is measuring the wrong ground (my #17, my #20).

### Verdicts, R1–R11.2

"Can fail" means: a named input makes it fail. "Fails the eight" uses the requirement-check names: who decides · one thing · unit · can it fail · weak words · level · basis · links.

| Line | Verdict | Checkable at readiness? | The check that can fail | Fails the eight on |
|---|---|---|---|---|
| **R1** context delivery | **Change** | Partly | File at the declared path exists and is non-empty, and every doc/skill it names resolves (no quota). Fails on: missing path, empty file, a named doc absent. | unit (budget in tokens/bytes/files?), weak words (*short, durable*), can fail ("not a dumping ground" has no failing input), who decides (who sets the budget), level (method written as MUST) |
| **R2** well-designed tools | **Split** | (a) yes; (b) no — needs a planted call | (a) every tool declares a name, purpose and boundary; fails on an undocumented tool. (b) send one deliberately invalid call; the error must name the field and the fix; fails on a silent error. The probe is shown failing once first (house rule). | one thing (interface + errors + boundaries), weak words (*simple, unambiguous, explicit*), can fail (as worded, no input fails it), who decides (who judges *unambiguous*) |
| **R3** planning/structure | **Keep**, move the check to step 2 | No — tasks do not exist at step 1; readiness sees only the template | At step 2: a step with no done-criterion fails. At readiness: the task format has a required done-criterion field. | weak words (*clear*), links ("so the agent doesn't declare victory early" is a causal claim with no basis), level (method → SHOULD) |
| **R4** state/memory | **Change** | Partly | The state file's last entry names the next action and the evidence path (no quota); fails if it names neither, or points at a step not in the table. The real check — a fresh session resumes from the file alone — is a drill and costs a session. | can fail (a directory existing is not resumability), weak words (*clean handoffs*), who decides (who judges "where it stopped"), one thing (checkpoint + handoff) |
| **R5** independent verification | **Keep** | Partly | Every task names a verifier and the verifier's command resolves; fails if the verifier is the builder or the command does not exist. Independence, and that it can fail, are shown by a planted wrong input (my #15: a check that cannot fail is a fault). | who decides (who judges *independent*), one thing (run the checks; use a separate evaluator), weak word (*independent*) |
| **R6** guardrails/permissions | **Keep** — MUST earned for the safety bound only | Config read = `reported`; a safe denial probe = `verified` | A planted forbidden action (a write outside the sandbox, a denied command) is refused and the refusal is logged; fails if it succeeds or no deny rule exists. For agy/qwen/dsh/opencode the format is unverified → `unknown`, no claim. | one thing (sandbox + privilege + policies + injection = split it), who decides (which actions are risky), level (injection defence is method, not MUST) |
| **R7** recovery/retries | **Change** | Declaration only, not idempotence | Each dispatch declares re-run safety, a rollback point and a retry limit; a planted failing step exhausts the limit and stops; fails if it loops or the declaration is absent. *Sensible* must become an EJ number or a stated comparison — I will not invent it. | weak words (*sensible, idempotent*), can fail (as worded, nothing fails it), unit (retries per step or per engine?), who decides (who sets the limit) |
| **R8** human gates | **Keep** | Config read = `reported`; a planted approval probe = `verified` | A planted action that requires approval blocks until approved or refused; fails if it proceeds. The built check already found the bypass prompt skipped — that **is** the check returning fail. | who decides (which calls need judgement), one thing (approve + decide), weak word (*risky*) |
| **R9** observability | **Split** | No prior logs → not verifiable; run one no-quota action and look | (a) each dispatch writes one line with engine, command, exit code, duration, output length or hash, cost; fails if a dispatch has no line, or the line lacks output. (b) anomaly rule: exit 0 with empty output or no change fails. Guard: never print a secret — record length/hash or redact. | unit (cost in what currency, tokens of whose), one thing (five kinds of record), can fail (*every* is not falsifiable), weak word (*anomaly*) |
| **R10** feedback loop | **Keep** | Register existence only (`reported`) | Every recorded failure links to a rule/check/tool, and that fix is shown failing once; fails on a failure with no fix, or a fix with no check. The 0-of-7 backtest is this check returning a bad number. | can fail (the loop as worded cannot), who decides (who calls a fix permanent), one thing (fix the mistake; review the scaffold), unit (review how often) |
| **R11.1** 80% judged | **Change**; do not enforce yet | Cannot count prompts — they do not exist at step 1; readiness lists the judges | At step 2's gate: a step (R3's unit) or an acceptance criterion (Q1's unit) with no named pre-existing judge fails. The 80% is `n=0`: keep it as a target measured over runs, not a gate. | unit (prompts or criteria — Q1), who decides (who counts), level (method → SHOULD), links (the judge attaches at step 2 — its own claim). Basis passes, because it is labelled `n=0` |
| **R11.2** first signal | **Keep** | The declaration is readable (`verified` as a plan); that it *runs first* is shown only by running | A judge with no first check and no written reason; a first check that cannot fail on its own; a first check slower than the thing it judges — each fails. *Fast* is comparison-defined, which passes weak words. | one thing (first signal + duration + exception), unit ("less time" needs the judged duration written), who decides (who writes the duration). Correctly marked SHOULD |

I agree with the main agent's placement: readiness lists which judges exist; the count happens after step 2, when the prompts exist (my #1: count before you commit — but count what is actually there; my #19: name the ground, then act as prescribed).

### Q1 — prompts or acceptance criteria?

Conditional, and it depends on which failure you want the 80% to catch. **If the failure is "a result reached the human unjudged", count acceptance criteria**: pass/fail attaches to a criterion, and a prompt with one judge over five criteria would otherwise score as judged while four are not. **If the failure is "a prompt was sent with no judge attached", count prompts**, because that is the unit the method's step 2 already numbers. My reading: criteria, because it is the finer unit and finds more unjudged results — my #14 「故兵非貴益多也」 (`quoted`), numbers are not the goal; finding the gap is. Price: the number falls and bookkeeping rises. **The deciding fact is EJ's: which failure is the 80% meant to catch?** I did not choose.

### Q2 — does a design-standard document count as a judge?

**Only something that can return pass or fail.** A standard is 度 — measurement — until a named person or rule reads a result against it and can say *fail*. My #11 `quoted`: 「先知者，不可取於鬼神，不可象於事，不可驗於度，必取於人，知敵之情者也。」 A document that cannot fail is context (R1), not a judge; counting it would count a shelf. So a design standard counts only when paired with a named applier and a named failing input.

### What the list misses

- **N1 — an output check per dispatch.** Nothing says a dispatched result must carry evidence the work happened. *Catches*: exit 0 with empty output (agy soft-deny, opencode auto-reject) marked done. My #7 「兵者，詭道也」 (`quoted`) / my #17: the failure concealed itself as success.
- **N2 — dispatch preconditions per engine.** stdin redirected, a concurrency/lock rule, and the write policy. *Catches*: the `codex exec` hang, opencode "database is locked", the worktree heredoc refusal. My #1 (know the ground) / my #14 (do not send two at one resource).
- **N3 — a deadline per dispatch.** *Catches*: a hung engine read as slow progress (codex hang, agy 502). My #8 「故兵聞拙速，未睹巧之久也」 (`quoted`) / my #18 (do not press).
- **N4 — a prescription for `unknown`/`MISSING`.** The four labels name the ground but the list does not say what work may be sent on an unverifiable line. *Catches*: a task sent to an engine whose guardrails were never verified. My #13 (the road not taken) / my #19 (name the ground, then act).
- **N5 — spend authority per dispatch.** *Catches*: a canary spending quota without EJ's go-ahead. My #11 says pay for foreknowledge; the house rule overrides — this tension needs EJ.
- **N6 — a per-engine contract.** What each engine can do, its read-only form, its structured output, its known failure modes. *Catches*: agy plan mode stopping at a plan, a task sent to an engine that cannot do it. My #17 (probe and read the signs).
- **N7 — the meta-rule: every check is shown failing once on a planted wrong input before it is trusted.** R11.2's "can fail on its own" is a claim; without the demonstration it is a claim about a claim. *Catches*: the built check's 0 of 7. My #15 「凡此五者，將之過也，用兵之災也」 (`quoted`) — a check that always passes is the "loving the people" fault.
- **N8 — name who wrote the check and what it does not establish.** *Catches*: "configured is not enforced" being read as compliance. My #20 (the closing line is the king's, not Sunzi's — attribute correctly).

## How I decided

1. **my #1 (「多算勝，少算不勝」, `quoted`)** — a requirement is a claim of advantage; count what you have before committing. Readiness is the temple reckoning: which of the five matters can I actually inspect now? So I asked each line: what evidence exists *at step 1*, with no quota?
2. **my #2 (「無恃其不來，恃吾有以待之」, `quoted`)** — readiness can secure only what is in your own hands: files, paths, a local command. It cannot make an engine behave, so no line that depends on engine behaviour may be called `verified` there.
3. **my #4 (know the other and yourself, `quoted`)** — the "other" here is the failure mode. Five of the seven failures were not knowing the engine's behaviour.
4. **my #5 (move only on advantage, `quoted`)** — I kept or changed each line by the failure it catches, not by how good it sounds.
5. **my #6 (mix harm into benefit, `quoted`)** — for each line I stated its cost beside its gain.
6. **my #7 and #17 (`quoted`)** — the seven failures exited 0. Exit code is not a sign; output is. This produced N1, N3 and the split of R9.
7. **my #8 (`quoted`)** — R11.2's first signal is sound: a check costing more than the thing it judges blunts the force.
8. **my #11 (`quoted`)** — a config file is 度; the true situation at dispatch is learned from probes and logs. Hence config reads are `reported`, never `verified`, and a document is not a judge (Q2).
9. **my #13 («途有所不由…», `quoted`)** — neither readiness nor the health check should take a road it cannot prove; the honest output is `unknown`/`MISSING`.
10. **my #14 (ratio of forces, `quoted`)** — spend the check in proportion to the failure; "more judges" is not the goal.
11. **my #15 (five dangers, `quoted`)** — every check has a virtue that is a handle: the over-cautious check that never fails, the check set on dying that always fails. This produced N7 and R5.
12. **my #16 (orders clear first, `quoted`)** — Q1 and Q2 are unclear orders; until they are clear the count cannot be held against anyone.
13. **my #19 (`quoted`)** — the four labels are the ground; each must carry its prescription (N4), and the list is a condition→response table, not a sequence.
14. **my #20 (judge by the unit and the tax, `attributed`)** — the unit of measure decides what you see; config was the wrong unit (my reading of the 0-of-7 backtest).
15. **my reading** — the requirements' author is unknown, so their ten lines are `attributed`, not a standard; R11 is EJ's, and its wording is still proposed.

## What I need to know

- **Q1** — which failure the 80% must catch: an unjudged result, or an unjudged prompt? It changes the unit.
- **Q2** — may a standard count as a judge without a pass/fail applier? I answered no; confirm.
- **May readiness run the harness at all** (a no-quota `--version`/`--help`), or read files only? This decides whether R2, R6 and R8 can ever be `verified` rather than `reported`.
- **Is there budget for planted-failure probes and a resume drill?** R4, R5, R6, R7 and R11.2 all need one to be more than a declaration.
- **Are `unknown` and `MISSING` a gate or a report?** N4 cannot be written until this is answered.
- **Is the ten-line source known enough to quote?** If not, it stays `attributed` and cannot be cited as a standard (my #16, my #20).

## Costs and risks

- A check with teeth costs a dispatch or a drill; the config reader costs nothing and proves little (my #11, my #8).
- Every line kept adds bookkeeping to every run; a checklist can itself become a dumping ground (my #1).
- Marking a line `unknown` honestly protects nothing without a prescription — it is a silent risk (my #13, my #19, N4).
- Counting over criteria lowers the 80% and adds bookkeeping; counting over prompts hides unjudged criteria (my #14, Q1).
- A denial probe or planted failure can cause harm if not sandboxed; never edit config — advice only (house rule; my #15).
- Enforcing the 80% before Q1/Q2 invites box-ticking: one weak judge per prompt (my #14, R11.1).
- The skill runs in other projects, so the list must stay engine-agnostic; hardcoding this machine's paths is the "constant form" fault (my #10, house rule).
- My #11 says pay for foreknowledge (spies are worth the gold); the house rule forbids a canary without EJ's go-ahead. I follow the binder and flag the conflict rather than resolve it.

## How we would know I was right

- **Backtest the revised list against the seven recorded failures.** For each, the revised list must name either a readiness check or a post-dispatch check that catches it, and the count must beat the built check's **0 of 7**. If a failure still has no check at either stage, my split/change was insufficient.
- **Show one check failing once.** Plant an empty-output dispatch; the N1 check must fail it *before* the check is trusted, and its log line must show the planted input.
- **Move the unit.** Count R11.1 under prompts and under criteria. If the two numbers differ, the unit matters and Q1 must be fixed by EJ; if they are equal, Q1 is moot and I was over-cautious.
- **A fresh reader test.** Hand the four labels and the list to a reader who did not write it; every line must be fillable with `verified`/`reported`/`unknown`/`MISSING` and a prescription, without guessing. A line they cannot fill is a line I failed to change.
