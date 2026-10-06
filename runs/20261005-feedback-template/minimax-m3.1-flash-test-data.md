I'll start by reading the project instructions, since AGENTS.md points to CLAUDE.md.
Now let me read the task-type docs and check whether the run directory exists.
Two engines have already answered in that folder. The brief says work blind, so I'll read only the briefs and shared knowledge — not their answers.
Now the task-type definition and how evidence paths work, to settle the `Location` question.
The result-file template is decisive for the `Location` question — let me read it.
Two more things: how the template is embedded in a brief (constrains field design), and the ledger's state for this type.
I read the knowledge docs (not the other engines' answers — working blind as instructed). Here's my answer.

## Verdict

**Confirm the three fields, change all three, and drop `Location`** — but not by adding a field: by moving the path onto the line that already exists.

```
## Summary
- Created:   tests/fixtures/users_valid.json — 200 valid users, incl. unicode + max-length names
             tests/fixtures/users_invalid.json — 12 invalid rows, one per schema violation
- Validated: ajv -s schemas/user.schema.json tests/fixtures/users_*.json → 212 rows, 0 violations
- Coverage:  N1.1 null name → users_invalid.json:4;  B1.2 255-char name → users_valid.json:88 required but not covered: none
```

First line: 200 valid + 12 invalid fixtures for the user schema, all schema-clean, four required edge cases covered.

## Whys — `Created`: keep, path must be on the line

1. Why does it exist? The type is `mixed`: a validation-only run is read-only and creates nothing (TASK_TYPES.md:92). A reader who sees no `Created` cannot tell "the schema was already satisfied" from "the worker built nothing and said nothing".
2. Why one line each, not a count? A count cannot be checked. Lines can be diffed one-for-one against `ls` — the same move as the worked example in `node-brief.md:57` ("compare counts"). A count the reader takes on trust is a claim; a line list is a check.
3. Why does the line carry the path? Because the check is *schema validation of files*. A name without a path cannot be validated without guessing where it is. **Stop — fact** (`node-brief.md:27`: the check as the worker can run it).

## Whys — `Location`: **remove** (the open question, settled)

1. Why add it? So the reader can find the fixture files to validate them.
2. Why isn't the result file's `evidence:` enough? Because `evidence` is **one** path and is defined as "the path to the proof: the command and its output, or file:line" (`result-file.md:16`); `validate_result.py` only checks that it *exists*. A validator command's output says "0 violations" — it does not enumerate the N files. **Fact.**
3. Is there a version where `evidence` *is* enough? Yes: point it at the fixture **directory**. Then the reader can list it and `Location` is redundant.
4. Then why not drop the path from `Created` too and let the directory speak? Because half the check is the *edge case → fixture* mapping, and a directory listing has no mapping. So the path belongs on the line carrying the case — which is `Created`/`Coverage`, not a separate field.
5. Why does `test cases gen` keep `Location`, then? Because there **N tests ≠ M files**: `Created` names the cases, `Location` maps them to `file:line` *and what code they target* (`FEEDBACK_TEMPLATES.md:31`). The mapping is load-bearing. For data, one fixture = one file, so the mapping is 1:1 and already sits on the line. **Fact, not judgement: `Location` earns its keep when item count ≠ file count.**

Caveat I'd not decide myself: the 1:1 breaks if the deliverable is a *generator* (one seed script → N files). Then either `Created` names the outputs, or the node is really `code generation`. **Which of those two it is, is the human's call.**

## Whys — `Validated`: keep the field, change what is in it

1. Why does it exist? Only the worker ran the validator, and the check is schema validation.
2. Why not leave it to the verifier? It can — that *is* the sabotage test (`TASK_TYPES.md:92`: corrupt a row → the validator rejects). So if the field is only the word *passed*, it adds nothing the header's `evidence` doesn't already carry, re-runnable by definition.
3. So what survives? What re-running doesn't give you: **which schema, and how many rows**. Two validators disagree about "valid", and the count is what the reader compares the directory listing against. That is the field's whole content.
4. Why is the worker its writer? It is the only one who knows which command it ran; nothing else records it. And it is **not** a verdict: "my command returned 0 violations" is a fact about a run, not a judgement of adequacy — so it survives the writer rule.
5. Why does bare "passed" specifically fail? It is unfalsifiable: *passed* is also what a worker writes when it eyeballed the data and never ran anything. In `20261004-runner-independent-fixes`, every correction in the run came from verification, **not** from a worker's report — including a wrong premise (`docs/TASK_TYPES_LEDGER.md:20`). A bare claim is the shape that has to be ignored. *(n=0 for the frequency; the ledger case is n=1.)*

## Whys — `Coverage`: keep the field, **re-key it**

1. Why does it exist? Half the check is an edge-case coverage list.
2. Who decides which edge cases must be covered? Not the worker. Required cases come from the requirements (`R1.1`, `N1.1`) — the design's artifact, not the worker's.
3. Why does that bite harder here than elsewhere? If the worker both invents the edge cases and reports coverage of them, the field is uncheckable — it grades its own homework, and a missed edge case is precisely what it cannot see. Keyed to named requirements, the check becomes "did you cover N1.1", which is decidable.
4. Why not argue from first principles when the sibling already settled it? `test cases gen`'s `Coverage` is defined as "which **acceptance criteria** the cases exercise (`R1.1`, `N1.1`, …)" (`FEEDBACK_TEMPLATES.md:30`). The proposal's "the edge cases covered" is keyed to the worker's own list. **Two meanings under one name, and the weaker one is the one being imported.** Copy the sibling.
5. Why no separate `Gaps` field? `Look` already set the pattern — the negative lives *inside* the field ("and which states it does NOT show", `FEEDBACK_TEMPLATES.md:33`). So `Coverage` ends with "required but not covered: none".
6. Is `Coverage` even the right name? Its meaning here is edge cases, not acceptance criteria. **Open for EJ:** (a) keep the name and add a labelled second row to the vocabulary table, or (b) rename to `Edges`. I lean (a) — consistency bought at the cost of a worse name at the read site is a bad trade.

## Whys — `Effort`: absent, confirmed — with one hole

1. Why absent? The rule is loop-types-only, and the default pattern is a single node (`TASK_TYPES.md:92`).
2. Why does that not worry me? A validation-only run creates no loop by construction.
3. Then why flag it? Because the sabotage for this type is *the validator rejects*. A reject is either a fail or a second attempt — and "attempt 2" is exactly what `loop?` is silent about. **Open for EJ:** does "retry after the check rejects" make a type a loop (so `Effort` appears)? `TASK_TYPES.md:84` records that a binary column already made one whole category "look like a lie" — is `loop?` tri-state like `Touches product`? I did not invent the answer.

## The three questions this brief's rules leave open

Per `CLAUDE.md:62` I evaluated rather than applied them:

- **"every field has a writer, and the writer is the worker"** — passes source, one-thing, unit. Fails *can it fail*: name one input — a field the worker fills honestly that encodes a judgement only the human may make (`Coverage: sufficient`, `Validated: good enough`). The rule catches **who writes**, not **what the worker may claim**. Should the rule add that a worker field is a *claim about a run*, never a verdict on adequacy? Level (MUST?) unspecified; basis n=1 type, two engines.
- **"Effort goes on every loop type"** — unit is fine and measured. Fails *can it fail* as above.
- **Weak words in the proposal** — "the edge cases covered" (undefined set) and "schema validation passed" (no schema, no count). Both fixed above.

---

Plan mode is on, so I wrote nothing. Say the word and I'll write this to `runs/20261005-feedback-template/minimax-m3.1-flash-test-data.md` — and, since the brief's blind period is over, I can read the three existing answers and report where we disagree.
