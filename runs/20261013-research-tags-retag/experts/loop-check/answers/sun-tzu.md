# 孫子 (Sun Tzu) — what the check leaves to the worker's character

## Answer

R4 and R5 are **not loop-ready as written**: their schema script is a real check the worker cannot edit, but it only certifies the *container* (143 lines, the id set, the tag vocabulary), while the two things the pass exists for — a blind tag and a tag that follows the quoted definitions — are left entirely to the worker's good character. Concretely, a worker that opens `key/old-labels.json` and copies it, or tags all 143 rows `reported` without reading them, passes the script 143/143. **If** the run can be given a working directory that holds only the brief and `blind/rows.md` (or a captured read-log the worker cannot write), then both pieces become loop-ready after that one change; the schema script itself is sound and should stay.

Per piece id:

- **R4 — not loop-ready as written (why), then strengthen (how).** Failure the check misses: the worker reads `key/old-labels.json` and copies the old labels; the sheet is well-formed, and the control pass silently becomes a copy of the key, which manufactures a false "no measurable difference" in R6. Repair: enforce the blind in the environment, not by instruction (my #2, #12); prove it with a plant row whose tag under the four old definitions the COO knows, and a hand-tagged sample of ~10 rows compared by script (my #17).
- **R5 — not loop-ready as written (why), then strengthen (how).** Same blind hole as R4, plus the check cannot see the new rule's substance: `split` with both parts tagged `reported`, or `stuck` with `why:"x"`, passes while saying nothing about whether the definition genuinely splits or genuinely sticks. Repair: enforce the blind; if the design means a split's parts to differ, have the script require two different tags; treat the `why` and the split meaning as an independent hand-read sample, and plant one row whose known answer is a split and one whose known answer is stuck (my #17).
- **R2 (named in the facts, not a tagged piece) — note, not loop-ready as an independent check.** The counter wrote the key, the fixture, the prediction and the reading, so it edits its own check; the design already says the counts are not independent evidence. Repair: a non-COO writes or approves the fixture, or EJ recounts a sample by hand (my #2).

## How I decided

1. My #2: split the ground. 「不可勝在己，可勝在敵」 — "Being unbeatable lies with oneself; being beatable lies with the enemy." The COO's script is her own ground; the worker's forbearance is the enemy's ground. Build on the first, not the second.
2. My #2 again: 「無恃其不來，恃吾有以待之；無恃其不攻，恃吾有所不可攻也」 — do not rely on the worker not reading the key; rely on the worker having no way to read it. "By instruction" is not that.
3. My #12: 「故善戰者，求之於勢，不責於人」 — "the skilled fighter seeks victory in 勢 and does not demand it of his people." An instruction is a demand on character; the environment is 勢. Change the 勢 (my #12's 「勇怯，勢也」).
4. My #4: this is half a victory. The script 「知吾卒之可以擊」 (the format can be checked) but not 「敵之不可擊」 (that the tag content was decided by the definitions). 「知彼知己，勝乃不殆」 — the design knows the script and the definitions, but not the ground: whether the worker can reach the key.
5. My #10: 「避實而擊虛」 — the script strikes the solid (line count, id set, tag list) and leaves the empty (meaning, blindness) untouched. Worse, 「形人而我無形」 is reversed: the COO's form (key, old labels on disk) is legible while the worker's is not.
6. My #17: probe. 「策之而知得失之計，作之而知動靜之理，形之而知死生之地，角之而知有餘不足之處」 — set a plant, make the worker take form, touch him in contact. A known-answer row converts good character into an observable; R1's own leak count (13 tag-like words in the Finding text) shows the same probe is already aimed at the caller.
7. My #13, with 謀攻's three ways the ruler troubles his army: "do not read the repository" is a command with no ground — 「不知軍之不可以進而謂之進…是為縻軍」 — a ruler ordering what he cannot make true hobbles his own force. Either give the command ground or drop it.
8. My #15: the worker's conscientiousness is a virtue the script cannot see, and a virtue relied on is a lever. A fault only when the plan leans on it.
9. My #14: a second attempt by the same worker is the same force. The attempt limit bounds repetition; it does not add independence.
10. My #7: renumbering and dropping the Label column are concealment (「能而示之不能」), and concealment works only against a side that cannot look. My #2 governs.
11. My #2 again, for R2: a check the worker can edit is not the ground. The design says so itself.

## What I need to know

1. Can `dsh headless` be run with a working directory that contains only the brief and `blind/rows.md`, with the rest of the repository out of reach? If yes, the verdict flips to loop-ready with that one change; if no, character is the only blind.
2. Can the run capture a read/command log, written outside the worker's "may change" file (`tags/control.jsonl`), so a script can assert the withheld paths were never opened?
3. Is the per-row shape frozen to `{"id","tag"}` / `split` / `stuck`, or may a soft field (a short quoted reason per row) be added? Without one, tag content cannot be script-checked at all.
4. May rows outside the 143 be added as plants, or would that disturb R2's denominator and the control comparison? If not, a plant must sit inside the 143 with a known answer, which contaminates the set.
5. For R2: will EJ or anyone other than the COO write or approve the fixture (and recount a sample), or does the count stay self-certified?

## Costs and risks

- Enforcing the working directory: setup work, and dsh may need the repository for config/skills, so the isolation may not be available — cost is a run change (my #2).
- Plant rows: they change any denominator they sit in, and a mis-marked plant produces a false failure (my #17).
- Hand sample: costs COO/EJ time, cannot be blind if the sampler knows the old labels, and a small sample misses (my #4, #17).
- Independent second tagger: roughly doubles the ~25–40k tokens per pass, and agreement is not correctness (my #14).
- Enforcing the blind removes the worker's reach to `docs/RESEARCH_TAGS.md`; R5's brief quotes it, so a misquote would go uncorrected by the worker — check the quote at design time (my reading, from #13's ruler who does not know the army).
- Leaving it as written: the false "no measurable difference" is unfalsifiable after the fact, and the pass's cost is spent for no independent result (my #4's half victory; my #2).

## How we would know I was right

Run one probe pass with the withheld files deliberately left in reach and no instruction. Measure the count of rows whose tag equals `key/old-labels.json`; if it climbs toward 143/143, the blind rested on character, and my reading is confirmed. Then run the enforced version with two plant rows of known answers: success is both plants tagged as known and the read-log showing no access to the withheld paths. Compare the four totals of the schema-only and enforced passes — a material difference is the direct measure that the old check was not real.
