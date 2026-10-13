I'll read the brief first.
# 老子 (Laozi) — one trust-tag set for research findings

## Answer

Take away rather than merge: one set of **four** tags — `shown`, `reported`, `inferred`, `absent` — defined once in `docs/workflow-templates/research-file.md` (new section `## Finding tags`, the one copy), with `docs/TASK_TYPES.md`, `docs/FEEDBACK_TEMPLATES.md`, `runs/20261011-agent-memory-graph/check-findings.py` and the draft `.claude/agents/researcher.md` pointing at it. Conditional: if EJ wants these tags used outside research findings (explorer rows, `grade a run` rows), the definition moves to its own file `docs/FINDING_TAGS.md` first, because a template is the wrong home once four kinds of row use it.

## How I decided

1. **Subtract, do not pick a winner — my #1.** 為學日益，為道日損。損之又損，以至於無為。無為而無不為。 — "Pursuing learning, one gains daily; pursuing the Way, one loses daily. Lose and lose again, until one arrives at not-doing. Not doing, and nothing is left undone." Nine words do this job today (`verified`, `confirmed`, `FACT`, `reported`, `unknown`, `gap`, `INFERRED`, `unproven`, `disputed`). Merging them by vote adds a decision layer; subtracting until nothing is left undone (`quoted`) leaves four.

2. **The home is where the row is written — my #6.** 為之於未有，治之於未亂。 — "Act on it before it exists; order it before it is in disorder." `docs/workflow-templates/research-file.md` is the form the researcher fills (`FINDINGS.md` table, `:12–21`) and the only one of the five places where a tag is chosen at the moment a row is written. A definition that sits beside the row cannot drift from it. My reading: the fifth copy of the definitions *is* the disorder — a new file is the cure only when four kinds of row use the set.

3. **The four tags, one line each.**

   | tag | means |
   |---|---|
   | `shown` | I read the cited primary document and it states this claim, as written. |
   | `reported` | I read a source that states this claim, but it is not the primary document that would settle it. |
   | `inferred` | No source states it; it follows from the `shown` rows the row names. |
   | `absent` | I looked for it and did not find it; the row names the query and where. |

   Old words map without rewriting history (read the old word as the new one): `verified` / `confirmed` / `FACT` → `shown`; `reported` → `reported`; `unproven` → `reported` (the vendor blog was read; nothing settles the performance claim); `unknown` / `gap` → `absent`; `INFERRED` → `inferred`. `Disputed` is not a tag — the house rule already makes it two rows.

4. **One measure per tag — my #4.** 為者敗之，執者失之。是以聖人無為故無敗，無執故無失。 — "One who acts on it spoils it; one who holds on to it loses it. So the sage does not act, and therefore does not spoil; does not hold, and therefore does not lose." The reviewer's complaint is right: `reported` said *who spoke* and `unproven` said *whether anything backs it* — one cell holding two grips. The table above asks one question of every tag: *what produced this row?* Primary read → `shown`; non-primary read → `reported`; built from other rows → `inferred`; search came back empty → `absent`. That is also why "is it the primary document" belongs inside `shown`/`reported` rather than in a fifth tag.

5. **The vendor-blog case, worked — my #4 again.** 天下神器，不可為也 — "The world is a sacred vessel; it cannot be acted on." The whole is the problem: the row is "the vendor says X" and "X is true" welded together. Split them: "vendor page states X, no harness published" (`shown`, cited to the page) and "X is true" (`reported` — the read source does not settle it). Each row now has one tag without anything added to it.

6. **Two tags seem to fit: split the claim, then take the weaker — my #14 and my #16.**少則得，多則惑 — "Little, then gained; much, then confused." My #16 is eight parallel statements, not a ladder, so is this set: `shown` is not "better than" `inferred`, it is a different kind of row. If two still fit after splitting, the row takes the tag that claims nothing was read (`reported` over `shown`; `absent` over `inferred`) and the stronger reading becomes its own row. Never both in one cell, never averaged — the house rule, and my #16's check on the set itself: judge it by whether the repo can check it, not by whether it reads well.

7. **`absent` is a first-class tag, not a failure — my #17.** 故有之以為利，無之以為用。 — "So what is there makes for benefit; what is not there makes for use." A searched-for-and-not-found row is the record of the search, and the search is the use. My #17 adds that its words do not say to remove anything — so the tag's whole content is the named query and place, which is what `docs/FEEDBACK_TEMPLATES.md:49` already asks for. That is why `unknown` and `gap` merge into one word.

8. **Keep the three house rules whole — my #10.** 我有三寶，持而保之。一曰慈，二曰儉，三曰不敢為天下先。 — "I have three treasures; I hold and keep them. The first is compassion, the second frugality, the third not daring to be first in the world." One copy of a definition; never upgrade a label; disagreement as two rows. They are held together, not traded: the moment you drop "never upgrade" to make a migration easy, the set has stopped being a check.

9. **The other two sets stay separate — my reading.** Explorer `read`/`ran` answers *what the agent did*, not *what a reader may believe*, and its "`ran` claims only" rule is a gate, not a tag. CLAUDE.md's *quoted* / *my reading* / *not measured* labels a conclusion the main agent writes, not a row with a citation. Fold them only after the four have survived one run; my #18's timing rule (得其時則駕，不得其時則蓬累而行 — "when he gets his time he rides out, when he does not, he drifts away", `attributed`) is why I do not fold them now.

10. **What the established schemes say (checked today).** GRADE, fetched from gradeworkinggroup.org 2026-10-13: it grades *certainty in a body of evidence* per outcome, across named domains (risk of bias, imprecision, inconsistency, indirectness, publication bias), separately from *strength of recommendation*, and it publishes minimum requirements for claiming GRADE was used and discourages "modified GRADE approaches" and multiple variations of the system. Three things apply here: certainty is not a property of one row; source-standing and claim-standing are separate outputs; and one system, defined once and used as published, is the whole point — which is exactly the failure this repo has. The Oxford CEBM 2011 Levels (search snippets only — the page returned no content twice, so I did not read it): it ranks *study designs* by level, i.e. it grades the kind of source, not the sentence, which supports keeping primary/secondary as a property of the citation. What I could **not** verify: the two-axis "messenger vs message" form of the information spectrum; the one page I read grades sources on a single authority axis, so I do not claim it for this decision.

11. **Files that change, to point at it.**

    - `docs/workflow-templates/research-file.md` — new `## Finding tags` section holding the four definitions and the old-word map; FINDINGS table row (`:12–21`) and the digest Confidence line (`:30`, which counts "verified / reported / unknown").
    - `docs/TASK_TYPES.md:100` — `CONFIRMED/INFERRED/GAP/UNPROVEN` → `shown | reported | inferred | absent`; keep "missing proof never reads as PASS" and "join contradiction = stop" verbatim.
    - `docs/FEEDBACK_TEMPLATES.md` — `web search` block (`:47–50`): `FACT` → `shown`, `INFERRED` → `inferred`, `GAP` → `absent`, `Disputed:` stays a line and not a tag; `research and reports` block (`:130`, `:135`) → the four.
    - `runs/20261011-agent-memory-graph/check-findings.py` — `LABELS` (`:19`) and the `--labels` default (`:66`) become the four plus the old-word map so the ten existing files still pass; docstring `:8–9` updated.
    - `.claude/agents/researcher.md` (draft, unadopted) — replace the copied four with a pointer to the definition, not a copy.
    - Not changed: `docs/workflow-templates/explorer-file.md`, CLAUDE.md (step 9).

## What I need to know

- Does EJ read `FINDINGS.md`, or only the 15-line `DIGEST.md`? If only digests, `shown` and `reported` can share one count line and I would shorten the set to three.
- Does the agent-memory-graph store label counts as data? `runs/20261011-agent-memory-graph/design.md:126` writes "label counts" per section — if that becomes a persisted store, the rename is a data migration, not a doc edit.
- Is `unproven` load-bearing as a gate anywhere, or only a word? It appears 3 times in the agent-memory-graph files; I found no check that fails on it.
- Which do the 2–5 `gap` rows per old file mean today — a searched-for absence, or an unread document? The counts are word counts over whole files, so this may be noise (my #8's discipline: 知不知上，不知知病 — "Knowing not-knowing: highest. Not-knowing knowing: sickness" — and the witnesses disagree on the second clause's wording, so I do not settle it myself).

## Costs and risks

- **Two vocabularies live for a while** (my #1: 損之又損 — the loss is repeated, not finished). The checker must accept the old words for the pre-2026-10-13 files. The price is that for one period the repo is exactly as inconsistent as it is now. Bound it with my #7: 民之從事，常於幾成而敗之。慎終如始，則無敗事 — "People often fail when they are close to finishing. Careful at the end as at the beginning: then no undertaking fails." The mapping is deleted when the last old findings file is archived, as a checklist item with a name and a date, not as an intention.
- **~300 `reported` rows may need re-reading.** `reported` is narrowed to "read, and not the primary document". Old rows used it more loosely. Re-reading history costs a researcher pass; leaving the old meaning silently is worse (my #8: do not pretend a reading you cannot check).
- **The alarm word disappears.** A claim with nothing behind it will now read `reported`, which sounds calmer than `unproven`. `docs/TASK_TYPES.md:100` ("missing proof never reads as PASS") and the checker's dated-URL rule must carry that weight instead of the word.
- **`shown` cannot be machine-checked** — only its citation form can. One tag's truth depends on a human having read the source (my #16).
- **If the set is wrong, it is wrong everywhere at once** — one definition, one home. My #1's price: subtraction is cheap to undo by adding, which is exactly why the tie-break rule in step 6 must be written down now.

## How we would know I was right

- **Worked case:** run the vendor-blog row from the 2026-10-13 review through the new definitions. If it yields two rows, two tags, and no judgment call, the set does what it was built for; if it still needs a fifth tag, my #1 went too far.
- **Retro-fit test:** the ten agent-memory-graph findings files pass `check-findings.py` under the four plus the map, with **zero** rows upgraded. Any row that needs an upgrade to pass is a finding about my map, not about the file.
- **One-command measure after the next research run:** grep the new findings files for the old words — `verified|reported|unknown|gap|confirmed|inferred|unproven|disputed` — counting each in the tag position only. Any hit is a copy that was not pointed at the definition, and the run failed the change (my #4: whoever acts on it spoils it — five local copies are what broke this).
- **Observable:** `docs/TASK_TYPES.md:100`, `docs/FEEDBACK_TEMPLATES.md:47–50` and `:130` contain no tag definition of their own, only a path. A definition reappearing in a second file is the regression signal.
