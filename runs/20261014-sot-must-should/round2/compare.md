# Four experts and Dave: round 2 on the 22 split ids

EJ, 2026-10-14: *"which source-of-truth requirements are MUST and which are SHOULD can let 4 experts decide"*.
Question: `question.md`. It gives each expert all five round-1 rows for every split id, plus these facts: no
reviewer is assigned, there is no secret scanner and no lint, what `memory_index.py` checks, and the two conflicts.
Answers: `answers/`.

**Rule** (*mine*, stated before round 2 ran): an id or clause is decided when three of the four experts give the
same level to the same clause. Dave is the control and is not counted. Every count below is *my reading* of each
expert's table row, by clause.

## Decided in round 2

| Id | Clause → level | Count | Dave |
|---|---|---|---|
| W1.1 | one file per entry; prefix matches `kind`; id unique; kind and id never change → **MUST** | 4/4 (Linus does not name "one file per entry": 3/4 on that clause) | same |
| W1.1 | the `DD-MM-xxxxxx-YYYY` form; the filename spelling → **SHOULD** | 4/4 form; 3/4 spelling (孫子 silent) | same |
| W1.3 | "one claim per entry" → **MUST** | 3/4 (Linus SHOULD) | SHOULD |
| W1.3 | `**How to apply:**`, section order, sentence count → **SHOULD** | 4/4 | same |
| W2.1 | the definitions → **guidance**; "written before the code" → **SHOULD** | 4/4; 3/4 (范蠡 guidance) | guidance for all |
| W2.2 | the definitions → **guidance**; "a hypothesis is a guess, labelled as one" → **SHOULD** | 4/4; 4/4 | same |
| W3.3 | "nothing from another agent's private state" → **MUST** | 4/4 | SHOULD |
| W3.3 | "no raw transcripts" → **SHOULD** | 3/4 (老子 MUST) | SHOULD |
| W3.4 | **SHOULD** | 3/4 (范蠡 MUST) | same |
| W3.5 | no user memory and no agent memory in the project → **MUST** | 3/4 (Linus SHOULD) | SHOULD |
| W4.1 | "anyone may… no owner, no approval" → **guidance**; `status` only `active`/`superseded`/`retired` → **MUST** | 4/4; 4/4 | same |
| W4.2 | add one `changed:` line → **SHOULD**; "earlier lines are never edited" → **SHOULD** | 4/4; 3/4 (范蠡 MUST) | same |
| W5.1 | "a decision or fact, before the code it governs" → **SHOULD** | 4/4 | same |
| W5.3 | adding `done:` → **SHOULD**; "a mismatch is reported, not settled in `done:`" → **MUST** | 4/4; 3/4 (老子: that is Rd5.3's row, already MUST) | same |
| W6.1 | journals, one file per agent session → **SHOULD** | 3/4 (范蠡 MUST) | same |
| W6.3 | "keeps both sides … Nobody chooses between two claims" → **MUST**; the "both links" part waits on the K4.3 conflict | 4/4 | MUST for links, SHOULD for `changed:` lines |
| W6.3 | "a conflict in `INDEX.md` is resolved by regenerating it" → **SHOULD** | 4/4 | points to K6.3 |
| K1.1 | **SHOULD** | 3/4 (孫子: MUST for "no commit changes governed behaviour with no entry") | same |
| K6.1 | `INDEX.md` equals the build, one line per active entry → **MUST** | 4/4 on the bound; 3/4 on the line form (老子 SHOULD) | same |
| K6.1 | "generated, never edited by hand" → **SHOULD** | 3/4 (范蠡 MUST) | same |
| K6.3 | no committed conflict-marker line → **MUST** | 3/4 (老子 SHOULD) | same |
| K6.3 | regenerate rather than merge by hand → **SHOULD** | 4/4 | same |
| Rd2.1 | the loading mechanisms (imports, hooks, the `AGENTS.md` fallback) → **SHOULD** | 3/4 (老子 guidance) | SHOULD |
| Rd2.3 | credentials → **MUST**; another agent's transcripts → **MUST**; the other four exclusions → **SHOULD** | 4/4; 3/4 (孫子 SHOULD; Linus MUST "where they expose private state"); 4/4 | transcripts SHOULD |
| Rd3.1 | the bound, and the check failing an oversized index → **MUST**; 24 KB / 200 lines → **guidance** (an example) | 4/4; 4/4 | same |
| Rd4.2 | **guidance** | 4/4 | same |
| Rd4.5 | "may read another agent's memory" → **guidance**; attribution (agent name and tool) → **SHOULD** | 3/4 (老子 SHOULD for all); 4/4 | SHOULD for all |

## Still split: these go to EJ

1. **W1.3 `**Why:**` line.**
   - MUST: 孫子 and 老子 (Dave too). 孫子: *"The tool already fails an active entry with no `**Why:**`"*.
   - SHOULD: Linus and 范蠡. Linus says the tool would have to change for this to work: *"the current tool rejects a missing `**Why:**` even though I recommend SHOULD; that mismatch needs explicit resolution before such an override can work"*.
2. **W3.5 "both live in the home folder".**
   - SHOULD: Linus and 孫子. 孫子: *"the location is the method"*.
   - MUST: 范蠡 and 老子, who rated the whole id MUST and did not split the location clause off.
3. **W5.1, the state of unfinished work before a handoff, interruption or context reduction.**
   - MUST: 范蠡 and 老子. 老子: *"Reasoning held only in context leaves with the context and stands in no journal"*.
   - SHOULD: Linus and 孫子 (Dave too). 孫子: *"K5.2's journal read covers a session cut off before it"*.
   - On the human-corrections clause: 范蠡 says MUST, Linus and 孫子 say SHOULD, and 老子 does not say.
4. **W6.1, "Each new entry gets its own file. Agents never append to one shared file".**
   - MUST: 范蠡 and 老子 (Dave too).
   - SHOULD: Linus and 孫子. 孫子: *"the no-loss outcome it serves is gated by W6.3"*.
   - *My reading:* the same rule is already decided MUST under W1.1, "one file per entry". This split is about which row holds the rule, not about the rule itself.
5. **K4.2, no retirement for age.**
   - guidance: 范蠡 and 孫子 (Dave too). 孫子: *"any deletion already fails K4.1"*.
   - SHOULD: Linus.
   - MUST: 老子, *"git holding the bytes is not a substitute for a pointer"*.
6. **Rd2.1, the agent has its instructions and task state before it starts work.**
   - MUST: 范蠡 and 孫子. 孫子: *"Acting before the governing instructions arrive is acting on unknown constraints"*.
   - SHOULD: Linus and 老子 (Dave too). 老子: *"No reviewer is assigned, so nothing stops the session"*.

## Where the levels and the tool disagree (*my reading*, raised by Linus and Dave)

- **W1.1's id form.** All four experts rate it SHOULD, but W1.1's `Fails if` already lists "an id not in the W1.1 form". The cleanup workflow's spec would also make `memory_index.py` reject it as an error. If the form is SHOULD, it needs one of two outcomes:
  - the tool warns instead of failing; or
  - the SHOULD gives a way to override that the tool accepts.

  This bears on the cleanup's Q2.
- **W1.3 `**Why:**`.** This is the same case if EJ picks SHOULD (split item 1).

## Questions the experts raised (merged, for EJ)

1. **Who reviews the judged checks?** None is assigned. If one is assigned at a named moment, these move back to MUST, in the order 老子 and Dave both give: the W2.2 hypothesis label, then W3.4, then Rd2.1.
2. **W3.2 against K4.1/K4.3.** A credential committed inside a claim can't be removed under both rules. Should there be a written exception? (Linus, Dave)
3. **K4.3 against W6.3 "both links".** Which links may an entry gain? (Linus, 孫子, 老子)
4. **No secret scanner exists for W3.2.** (round 1: 孫子, Dave)
5. **Rd3.1's strictest start-file limit**, measured for each agent actually used here. (Linus)
6. **What deadline does "immediately" in W5.1 mean?** (Linus)
7. **Does "sensitive data" in W3.2 cover user preferences and context?** Dave's W3.3 and W3.5 levels depend on the answer. (Dave)

## Check

`four_experts.py check round2`: 5 answers, 2 failures. Both are 老子 writing 為 where his list has 爲 (以深為根, 以約為紀), the same word in two script forms. Claude wrote the check. It does not establish that the experts applied their rules well. The counts above are my reading of each table, by clause. No second reader has checked them.

## EJ's decisions

- 2026-10-14, EJ: *"MUST"* — in reply to the COO's question "The id form `DD-MM-xxxxxx-YYYY`, MUST or SHOULD?". The
  rule: **the W1.1 id form `DD-MM-xxxxxx-YYYY` is MUST; an id not in that form fails** (W1.1's `Fails if`, as already
  written). This overrides the four experts' 4/4 SHOULD for that clause. The other five round-2 splits are still open.
- 2026-10-14, EJ: *"decide the six requirements the experts still split on"*. Decided by the COO on that delegation;
  each level below is **the COO's choice**, not an expert count. The principle, taken from Dave's and 孫子's round-2
  answers and from EJ's id-form decision above: MUST where the tool already stops the commit, or where one rule
  already holds MUST elsewhere; a judged check with no reviewer stays SHOULD.
  1. **W1.3 `**Why:**` line → MUST.** `memory_index.py` already fails an active entry with no `**Why:**`; the same
     reasoning EJ used for the id form. (With 孫子, 老子, Dave; against Linus, 范蠡.)
  2. **W3.5 "both live in the home folder" → SHOULD.** The location is the method; the bound — no user memory and no
     agent memory in the project — is already MUST (3/4). (With Linus, 孫子, Dave.)
  3. **W5.1 the state of unfinished work, and a human correction, before the session ends → SHOULD.** No reviewer can
     stop a handoff today, and the per-session journal (K5.1) holds what was being done. First of the three in line to
     promote if a reviewer is assigned. (With Linus, 孫子, Dave.)
  4. **W6.1 "Each new entry gets its own file. Agents never append to one shared file" → MUST.** It is the same rule as
     W1.1 "one file per entry", already MUST (3/4); one rule gets one level. (With 范蠡, 老子, Dave.)
  5. **K4.2 no retirement for age → guidance.** Deletion is already barred by K4.1 (MUST); a retired entry keeps its
     file and body, and K4.3 lets its status change again. (With 范蠡, 孫子, Dave.)
  6. **Rd2.1 instructions and task state before work starts → SHOULD.** No reviewer can stop a session start, and the
     loading differs by engine; Rd4.1 (MUST) is the gate before any file is edited. (With Linus, 老子, Dave.)
  Not yet written into `SOURCE_OF_TRUTH.md`.
