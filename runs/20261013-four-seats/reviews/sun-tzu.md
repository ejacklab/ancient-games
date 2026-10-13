# sun-tzu — review of design.md
Question: How would this design fail? Where does the opponent — or reality — attack?
## Findings
1. Lines 17–21 — Everything rests on one untested diagnosis (skipped steps, wrong common sense). If the real cause is missing facts, seats that review reasoning will not fix it. — principle: 知彼知己，百戰不殆 — label: my reading
2. Line 36 — 范蠡 decides how many seats run, so 范蠡 alone decides whether 孫子 runs. Line 39 says 范蠡 has the weakest source. One wrong "small task" call removes every check, unreviewed. — principle: 夫未戰而廟算勝者，得算多也 — label: my reading
3. Line 34 — Sequential seats sharing one state file read the earlier seats' conclusions first. They can drift into agreement instead of checking each other. — principle: "A check I wrote and then passed is not independent evidence" (CLAUDE.md) — label: my reading
4. Line 38 — The only guard against copied style or a lazy seat is how the prompt is built. No test checks the output, and the design does not name the engine. — principle: 兵者，詭道也 — label: not measured
5. Whole design — There is no planted flaw the seats must catch, so nobody can show that a seat is able to fail. — principle: "Sabotage (proof the check can fail)" (docs/TASK_TYPES.md:86); 勝兵先勝而後求戰 — label: my reading
6. Line 22 — The rule list "grow[s] from surprises", but the AI cannot see its own defaults. So the first big mistake is the one the list will not cover. Who decides what is "big or irreversible" is unstated. — principle: 知彼知己 — label: my reading
7. Lines 35, 40–41 — 老子 runs after 孫子 and may remove the safeguards 孫子 added. Only choices where "both [are] logical" go to EJ, so this conflict has no stated route to him. — principle: 兵者，詭道也 — label: my reading

## Verdict
It breaks at its gates. One weakly grounded seat sizes the review, the sequential seats can agree with each other, and nothing proves a seat can fail. If the diagnosis in lines 17–21 is wrong, the rest falls with it.

## Open questions for EJ
- Who checks 范蠡's sizing call?
- Should the seats write blind, or is reading in sequence intended?
- One engine for all seats, or different ones?
- Is a sabotage case required before acceptance, and who writes it?
- If 老子's removal conflicts with 孫子's safeguard, who decides?
