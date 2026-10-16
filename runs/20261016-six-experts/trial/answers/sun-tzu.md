# 孫子 (Sun Tzu) — what a pre-flight check should verify

## Answer

Run one no-AI, filesystem-and-text pass before every engine call, and gate the brief's **ground** and its **contract** only — never its meaning (my #2, my #10, my #13). In order of value, the pass checks these eight things; anything a script cannot check without judging belongs to the verifier and to EJ.

1. **Every named path and section anchor exists, is non-empty, and is readable by the engine that will read it.** (my #4, my #11)
   - *Looks for:* each file the brief tells the engine to read; each section it names (for example the list's `## Final list`); whether each path is inside the call's readable root.
   - *How a script tells:* parse backticked and `runs/...` paths, resolve them against the call's working directory, assert `is_file()` and non-zero size, assert the named heading is present in the text. For an engine that cannot read outside the project (opencode), fail any path outside the project root.
   - *Prevents:* the engine reads a missing or foreign file and answers from recall — a billed call returning a plausible, unverifiable answer. The runner already copies seat files into the run folder because an out-of-project folder cannot be read.

2. **The answer shape the brief demands equals the shape the post-check will grade.** (my #16, my #10)
   - *Looks for:* the top-level headings in the brief's "Write exactly this" block, against the grader's expected headings or the result template the brief names.
   - *How a script tells:* parse the `## ` headings from the brief's output block; compare them as a set to the grader's constant (the runner's `SECTIONS`) or to the template file the node brief names.
   - *Prevents:* one fact kept in two places drifting apart — a correct answer failed by a stale grader, or a grader passing a file that has the headings and nothing under them. Today `six_experts.py` and `assets/brief.md` hard-code the same headings independently.

3. **The output contract matches the route that will run it.** (my #4)
   - *Looks for:* whether the brief requires the engine to write a result file, or to give the answer as its final message; the engine/route named; the parent directory of any result path.
   - *How a script tells:* if the brief names a result path and the engine itself writes, assert the engine is a writing form (`--write`/build) and `parent.is_dir()`; if the route captures stdout (the six-experts runner, or the Claude wrapper that writes for a read-only Codex/agy node), assert the brief asks for the answer as the final message instead.
   - *Prevents:* the documented exit-0-no-file. `qwen` writes nothing when the write tool is withheld, `agy` soft-denies a tool and still exits 0; the empty result surfaces only at handoff, after the call is spent (`docs/EXECUTOR_KINDS.md`, "How a failure shows").

4. **The list's item numbers are exactly 1..n, and the brief states that n.** (my #1, my #14)
   - *Looks for:* the numbered item headings under the list's `## Final list`; the brief's line that promises "items are numbered 1–n".
   - *How a script tells:* parse the item numbers; assert `sorted(nums) == list(range(1, n+1))` (no gaps, no duplicates); assert the brief's stated n equals it.
   - *Prevents:* an invented citation passing. The post-check computes `n_items = max(nums)` and only tests `1 <= c <= n`, so a gap or a duplicate in the list silently disarms the very guard that reads it (`six_experts.py:77-79`, `check_one`).

5. **No order is left unsubstituted.** (my #16, my #18: 「圍師必闕」 `quoted` — leave a way out, do not pen the worker in)
   - *Looks for:* format keys `{...}` in generated briefs; the `<...>` fields of the node-brief template; the template's explicit "unclear spot" note.
   - *How a script tells:* regex the known key and field patterns; each must be replaced, or carry the template's "unclear spot" note rather than a blank.
   - *Prevents:* the engine answers a literal `{question}`, or reads `<the check, as the worker can run it>` as its standard and invents one — and is then blamed for the writer's unclear order (`node-brief.md`: "A part that cannot be filled is an unclear spot, not a blank").

6. **The question in the brief is the question on record, and is not empty.** (my #1, my #17)
   - *Looks for:* the brief's question block against the run's `question.md`, or the node's task id.
   - *How a script tells:* exact string or hash comparison; reject a whitespace-only block.
   - *Prevents:* a hand-edited brief asking a different question. The answer is then filed correctly by shape and wrongly by content, and nothing notices.

7. **What must be withheld is not in the brief.** (my #10: 「避實而擊虛」 `quoted`; my #12)
   - *Looks for:* the paths or strings the brief itself declares withheld (the node-brief's "what is withheld on purpose"; the six-experts brief has no such field today).
   - *How a script tells:* grep the brief for each declared withheld path or string; fail on a hit.
   - *Prevents:* a blind verifier or a persona is contaminated, and the independence that justified the second call is gone — silently (`EXECUTOR_KINDS.md` rule 5; the six-experts seats must not see each other's answers).

8. **The force named is the force that will run, with a fresh canary on record.** (my #11: 「先知者，不可取於鬼神，不可象於事，不可驗於度，必取於人，知敵之情者也。」 `quoted`; my #17)
   - *Looks for:* the one engine, model and effort the brief names; the run's canary log; the catalog of the binary that will actually make the call.
   - *How a script tells:* parse the names — exactly one engine, one model, not blank; assert a passing canary for that engine, model and binary, recent enough for the run; assert the model is in that binary's catalog. Read the log; do not re-run the canary here.
   - *Prevents:* the bundled-runtime trap — three diagnoses in two days, where a bundled binary lacks the named model, the error blames the account, and the call is spent for nothing (`EXECUTOR_KINDS.md`, "The bundled-runtime trap").

### What it should deliberately not verify

- **Whether the brief is one thing, true, or good.** A script cannot read meaning, and asking it to is the walled city, the method for when there is no alternative (my #3). The verifier and EJ own it.
- **The answer's quality, correctness or usefulness, and whether the engine will answer well.** There is no answer yet, and foreknowledge does not come from measurement (my #11). Only the run and the verifier can show it.
- **Politeness, voice, tone, persona.** The brief's own premise is that the rules applied, not the voice, make an answer checkable, so a voice gate buys nothing measurable (my #6).
- **Whether the list's Chinese quotes are true to their sources.** That is collation, a separate piece; the pre-flight only ensures the *answer's* quotes stay inside the list, which is post-flight (my #10 — strike where the post-check does not look, not where it does).
- **Whether the engine is installed, logged in, or has quota.** That is readiness' canary, once per run; re-probing it on every call is precisely the tax the brief warns against (my #8, my #14: 「故兵非貴益多也，惟無武進，足以併力、料敵、取人而已。夫惟無慮而易敵者，必擒於人。」 `quoted`).
- **The post-check's work.** Item cites, Chinese verification and required sections all read an answer that does not exist yet; duplicating them at pre-flight doubles the cost for no new failure (my #14).

## How I decided

1. I treated the check as the reckoning before battle: count what the brief carries before committing a force, because the count is cheap and the force is not (my #1: 「兵者，國之大事，死生之地，存亡之道，不可不察也。」 `quoted`; and the chain 「地生度，度生量，量生數，數生稱，稱生勝」 `quoted`).
2. I asked what makes the call unwinnable no matter how good the engine is, and put those first, because a script can own them and the engine cannot — do not rely on the engine being careful, rely on the brief having what cannot be attacked (my #2: 「故用兵之法，無恃其不來，恃吾有以待之；無恃其不攻，恃吾有所不可攻也。」 `quoted`).
3. I re-read the list while working, then read the two brief templates and the runner (`assets/brief.md`, `assets/brief-plain.md`, `docs/workflow-templates/node-brief.md`, `six_experts.py`) and looked for one fact kept in two places: the headings, the item count, the result path against the engine's write mode. Those are the empty ground the pre-flight should strike (my #10: 「避實而擊虛」; 「水因地而制行，兵因敵而制勝」 `quoted`).
4. I used the executor table as the ground and the force: read-only and plan forms cannot write, opencode cannot read outside the project, `qwen` and `agy` can exit 0 with no file. Knowing the brief but not the engine is half a victory (my #4: 「勝之半也」 `quoted`).
5. I kept only items a script can answer yes/no without an AI call, because the check pays on every call and must be quick — clumsy speed beats a slow perfect gate (my #8: 「兵聞拙速，未睹巧之久也」 `quoted`; my #14, `quoted` above).
6. I ordered by silence and price: a failure the engine can hide and the handoff will not see — a missing file, an unwritable destination, a stale contract — ranks above one the post-check already reports (my reading of `EXECUTOR_KINDS.md`'s failure table).
7. I put the item-number check in because the guard's own range test rests on `n_items = max(nums)`; a gap in the list defeats the guard silently, and only a script can see it (my reading of `six_experts.py`).
8. I left judgment out on purpose: not every road is taken, and a check that asks for one-task, truth, quality and voice is an army sent at a walled city (my #3; my #13: 「途有所不由，軍有所不擊，城有所不攻，地有所不爭，君命有所不受。」 `quoted`).
9. I fixed the *conditions*, not the worker: the pre-flight changes the brief before the call instead of exhorting the engine inside the brief to be careful (my #12: 「故善戰者，求之於勢，不責於人，故能擇人而任勢。」 `quoted`).
10. I named the general's fault, not the officer's: an unclear or contradictory brief is the writer's, and the check should say so before the engine is blamed for it (my #15: 「凡此五者，將之過也，用兵之災也。」 `quoted`; my #16: 「約束不明，申令不熟，將之罪也；既已明而不如法者，吏士之罪也。」 `quoted`).
11. I made the check prove itself by probing, not by assumption: the same items become sabotage mutants, and it is replayed over the briefs that already exist (my #17: 「故策之而知得失之計，作之而知動靜之理，形之而知死生之地，角之而知有餘不足之處。」 `quoted`).
12. I judged it by the frugal measure — what the house breeds, per unit — not by the size of the checklist (my #20: 「赵毋失其故法，晋国归焉。」 `attributed`, a narrated bamboo dialogue).
13. *Proposed change to the pattern:* add a named **pre-flight** step to the brief-writing piece. Today that piece has no check of its own, and its output is the only thing the engine sees, so "small pieces, each with its own check" does not yet cover the piece that writes the check's own input. It changes the method by one gate before dispatch, one line per failure in the state file, and one sabotage set — no extra engine call (my #16).

## What I need to know

1. Does one script gate both artifacts — the question file and the worker brief — or one script each? The items differ, and a shared check would have to be common to both.
2. For a worker brief: does the worker write a result file, or return a final message the wrapper captures? Item 3's rule flips on this.
3. Who owns the withheld list and the allowed engine/model list, and where is each kept as one copy? Without an owned list, items 7 and 8 are judgment, not script.
4. May the pre-flight read the grader's constants and the executor table live, or must it embed them? Item 2 is only correct if the brief and the grader cannot drift apart again.
5. Is a declared unclear spot a pass with a note or a fail? The node brief calls it "not a blank"; the check must know whether to let it through (items 5 and 6).

## Costs and risks

- **Every item is a tax on every call** (my #8, my #14). If it never fires over a hundred calls it has bought nothing. Keep it to one filesystem-and-text pass, no subprocess and no network; read the canary log instead of re-running it.
- **A false failure costs a round and can block a good brief** (my #16, my #2). A shape check stricter than the grader rejects what the grader would have passed; enforce only what the pattern actually promises.
- **A brief can name the right files and never use them** (my #2). You can make yourself unbeatable; you cannot make the enemy certain to be beaten. The check narrows the blind spots; the judgment stays.
- **Item 4's contiguity rule may fail a list deliberately numbered with gaps** (my #13, my #14). That invariant needs EJ's agreement, not an assumption; if it is wrong, the check changes, not the list.
- **Item 7 needs its withheld list written down first** (my #11). A missing or stale list gives false confidence, which is worse than no check because it is trusted.
- **The check can become a third copy of facts already held elsewhere** and drift silently (my #12, my #16). Point it at one source of truth, or the cure becomes the next defect.
- **It cannot fix the file** — by design — so every failure costs the main agent a repair (my #13). That is the honest price of a gate that will not silently rewrite the order it is checking.
- **A passing pre-flight is not a good brief**, and it can make the writer lazier (my #2). Record what it catches, and read a rising pass rate with falling answer quality as a warning, not a win.

## How we would know I was right

1. **Sabotage, once, per item.** Take real generated briefs and inject each failure the check claims to catch: delete a referenced file, rename one required heading, point a write-task at Codex `-s read-only`, leave `{question}` in place, drop item 7 from a copy of the list, inject a withheld path, name a model the binary lacks. Each mutant must fail with its own message, and a clean brief must pass. Until this runs, the check is not known to be able to fail (my #17; the canary sabotage rule in `EXECUTOR_KINDS.md`).
2. **Replay over what already exists.** Run it across every `runs/*/question.md`, `runs/*/briefs/*.md` and `runs/*/nodes/*.md`. Hand-read a sample of the hits: a check that fires on many real historical briefs is either finding rot or is wrong, and only the reading tells which (my #1, my #11).
3. **Log every pass and failure beside the call.** Compare the post-check's "missing section / no answer file" failures and the empty-answer rate before and after the pre-flight, against a flat engine-call count. The observable claim: calls lost to a bad brief fall while the call count does not rise (my #20 — judge by the unit the house breeds, not by the size of the staff).
4. **A pre-flight that never fires is not proven useless, only unproven.** The sabotage run is the proof it can fail; the replay is the proof it reads real artifacts; without both, a green pre-flight and a dead one look identical (my #17).
