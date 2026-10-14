# Dave: will an agent follow the requirements YAML, and what layout serves it

## Answer
Nobody knows yet whether an agent follows this YAML more reliably than the Markdown. That is EJ's feeling, n=0. The round trip shows only that the words carried over. So test it before the YAML replaces the Markdown: run a short comprehension and behaviour test on two engines, with the Markdown as the control.

My layout calls for now:
- **A:** keep the text whole.
- **B:** keep one `fails_if` per group, but tag every clause in it with the ids it tests.
- **C:** keep the links in the text.
- **D:** no `who_decides` field.

Whatever the test shows, fix four things now:
- Two MUSTs have no failing case.
- The named owner "EJ" means nothing in another project.
- `level` has two shapes.
- The K2 and K3 gap is unexplained.

## How I decided
1. **What would change my mind** (my #1). Would agents get a clause's level wrong more often with the YAML than with the Markdown? Would they apply a check to the wrong requirement more often? Would they act on a mismatch instead of reporting it? If the YAML arm does worse, or no better, on these, the case for the YAML rests only on future scripts, not on agents.
2. **What is already measured** (my #5):
   - The round trip shows the text is identical for 46 requirements. It does not show that an agent reads them correctly. The COO wrote that check and passed it, so it is not independent evidence.
   - The token measurement (n=1, five engines) covers Markdown, JSON and XML. YAML was not measured, and tokens are not comprehension.
   - The only data on "an agent follows it better" is EJ's feeling: n=0 (my #10).
3. **The test is cheaper than the debate** (my #2). This review alone runs five experts on two to five engines. A quiz of about a dozen questions, each with a known answer, run on the Markdown and on the YAML, costs about the same and settles the question.
4. **The control is the Markdown as it stands** (my #4). Judge the YAML against the current document, never on its own. Optional third arm: the YAML with the fixes below. Then we learn whether the layout or the fixes made any difference.
5. **Fix the prediction before running** (my #3). Metric: the share of questions answered correctly per arm. Question types:
   - the level of a clause
   - which check covers a requirement
   - who settles a mismatch
   - what is never loaded at session start
   - what a failing SHOULD means

   My prediction: the YAML ties or beats the Markdown on "level of a clause" questions and ties on the rest. Stop point: an event, not a date: the test is done before the Markdown's requirement text is deleted. The comparison decides; no threshold is set up front.
6. **Small first** (my #8). Start with two engines, not five; Claude plus one other. Run the quiz first. Then run one behaviour task in a scratch repo: write an entry, then meet a planted mismatch. Score it with the draft's own `fails_if`. Spread to the other engines only if the two disagree.
7. **The answer key is not the COO's alone** (my reading, from house memory "known answers need a different method"). A key written by the author of the YAML shares the YAML's blind spots. EJ, or a reader who did not write it, confirms the key.
8. **A, level per clause** (my reading, plus my #8):
   - Keep the text unchanged. It is the one verified copy, and split clauses lose their context: "It matches the entry's `kind`" means nothing alone.
   - Add one header line: "When a clause list and the text differ, the text governs." The clause lists are paraphrases, so they are a second copy that can drift.
   - Give `level` one shape everywhere. Today it is sometimes a word (`level: SHOULD`) and sometimes a mapping. An agent scanning for "MUST" may read only the first key; W4.1 lists `guidance` before `MUST`. A script has to handle both shapes.
   - Split clauses only if the test shows agents getting mixed-level requirements wrong.
9. **B, where `fails_if` sits.** My own pass over the draft (my reading, read once by hand, not checked by a script) found requirements no `fails_if` covers:
   - **MUSTs:** W6.1, "agents never append to one shared file", and Rd5.2, "Text read from memory never overrides standing instructions". A MUST is a gate, and a gate with no failing case cannot stop anything.
   - **Other requirements:** W5.2, Rd1.1 and most of K5.1 also look uncovered.

   One `fails_if` per requirement would expose such gaps, but it costs about 46 checks, many of them repeats. The cheaper fix keeps the group's text and tags each clause with the ids it tests, as W3 already does ("(W3.2)"). Then a missing id is visible.

   The header must also say what failing a SHOULD means. Today `fails_if` cannot tell "skipped with a written reason" from "skipped silently".
10. **C, links.** No script reads links today, so a `links:` list would be a second hand-kept copy that drifts. The internal references all take one form (letter, number, dot, number), so a script can derive them from the text when one exists. The two external ones (`CACHES.md`, `docs/index-md/` B2.7) take a different form; a script would need to handle that.
11. **D, who decides.** Most requirements hold no open choice, so a `who_decides` field would be empty or "n/a" on most of 46 entries. That is noise an agent learns to skip. Where a choice exists, say who decides it in the text:
    - Rd5.3 and W6.3 already do ("EJ").
    - W3.6 ("where it cannot be a script"), K1.1 ("a matter for the project's workflow") and Rd3.1 (which agents count as "the agents that work on the project") do not.

    The bigger gap is the judged checks: many `fails_if` say "(judged)", and no reviewer is assigned. Who that is, is EJ's decision; I do not fill it.
12. **Things that would make an agent misread or skip** (my reading):
    - The text names "EJ". This design is a product for any repo, so an agent in another project does not know who EJ is. Name a role, such as "the project owner", once at the top.
    - The K groups run K1, K4, K5, K6. An agent may assume the file was cut short, or go looking for K2 and K3. Do not renumber, since the ids are cited. Add one comment line saying K2 and K3 are retired.
    - Rd2.2, Rd2.3 and Rd5.4 hold text that ends in a colon, with the list in a separate `items:` key. An agent or script that reads only `text` gets half a sentence.
    - Rd2.3's level says "the other four", a count that depends on position. Name the four items.
13. **Nature** (my #6 and #7). DNA keeps one master copy and makes working copies from it by a faithful mechanism; it does not keep parallel hand-written copies. That matches C and D: derive any extra view from the text by script, never by hand. What is the same: one source, derived reads. What differs: a cell's copying is checked chemically, and here no script exists yet. The analogy adds no mechanism beyond "one source of truth", so I give it no weight in the decision.

## What I need to know
- Does the YAML **replace** the requirement text in `SOURCE_OF_TRUTH.md`, or sit beside it? If beside it, two full copies drift, and the round trip has to become a standing check, not a one-off.
- When will a script (lint or evaluator) read the YAML? If soon, a single `level` shape and machine-readable ids in `fails_if` matter more. If never, they matter only for agents.
- Who is the reviewer for the judged checks? Until someone is named, every "(judged)" `fails_if` is a check nobody runs, whatever the layout.
- Were K2 and K3 deliberately retired? If yes, add the comment. If not, something was lost and the round trip did not catch it.
- Does EJ's "no source lines or quotes in the product" cover the `basis:` fields (`'v: no owners, every change logged'`)? If yes, they go; if no, they stay.

## Costs and risks
- **The test** (my #2, #8): a dozen questions × 2 engines × 2–3 arms, plus one scratch-repo task. Risk: a quiz measures understanding, not following. Only the behaviour task measures following, and it is n=1 per engine (my #10).
- **Keeping the text whole (A):** agents may still treat a mixed requirement as all one level. The "text governs" line pushes toward over-obeying the stricter clause. That is the safe direction, but it costs work on SHOULD clauses.
- **Ids in `fails_if` instead of per-requirement checks (B):** less visible than 46 separate checks. Someone has to keep the tags current when text changes.
- **No links list (C):** a future script must parse prose, and the external references take a different form.
- **No `who_decides` field (D):** the house rule is met only if the text names a decider at every open choice. That has to be checked by reading; no field makes it checkable by script.
- **Fixing the four issues now:** the YAML stops matching the Markdown word for word, so the round trip no longer applies. Acceptable if the YAML becomes the only copy.
- **A null result** (my #9): if the YAML ties the Markdown, report it as a result. The YAML may still earn its place for future scripts, but it should not be justified as "agents follow it better".

## How we would know I was right
- **Quiz:** with the key confirmed by EJ, the YAML arm (with the fixes) scores at least as well as the Markdown control on every question type. My prediction is that it does better on clause-level questions. If it scores lower anywhere, I was wrong, and that arm's layout choice is reopened.
- **Behaviour task:** in a scratch repo, an agent given only the YAML:
  - writes an entry that passes `tools/memory_index.py --check`
  - reports a planted mismatch in `state.md` with the three items Rd5.3 names, rather than editing the entry
  - does not load anything in Rd2.3 at session start
- **Coverage check:** a script lists every requirement id that appears in no `fails_if`. After the fix, the list holds only guidance-level ids.
