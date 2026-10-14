# Four experts and Dave — which source-of-truth requirements are MUST, SHOULD or guidance (round 1)

EJ, 2026-10-14: *"which source-of-truth requirements are MUST and which are SHOULD can let 4 experts decide"*.
Question: `question.md`. Per-id levels of all five: `matrix.md`.

| | Linus | 范蠡 | 孫子 | 老子 | Dave (control) |
|---|---|---|---|---|---|
| Answer (one line, *quoted*) | "Reserve MUST for preserving identity, evidence, confidentiality, authority boundaries and a usable handoff" | "MUST strictly to structural defenses, irreversible data-loss boundaries, capacity ceilings, and plan-integrity gates" | "Assign MUST only where failure is silent and unrecoverable" | "MUST only where failing destroys a record nothing else keeps, or puts a secret or another person's private state into a committed repo" | "SHOULD covers everything a reviewer has to judge, because n=0 and nobody does that reviewing yet" |
| Pure MUST ids (*my count*, from `matrix.md`) | 8 | 37 | 19 | 19 | 15 |

## Where they agree

*My count*, four experts only.
- **13 ids, all four:** MUST — W3.2, K4.1, Rd1.2, Rd5.2, Rd6.1; SHOULD — W3.1, W3.6, W5.2, Rd4.4; guidance — W4.3,
  Rd4.3, Rd5.4, Rd5.5.
- **11 ids, three of four:** MUST — K4.3, K6.2, Rd4.1, Rd5.1, Rd5.3; SHOULD — W1.2, W6.2, K5.1, K5.2, Rd1.1, Rd2.2.
- Dave differs from the four on 2 of the 13: W5.2 (guidance) and Rd6.1 (SHOULD).

## Where they disagree

22 ids (`matrix.md`, "split"). Most splits are about **clauses**, not the whole id: for example W1.1, *quoted* —
Linus "MUST keep identity and kind stable … SHOULD use the prescribed filename and random-id scheme"; 范蠡 "MUST";
老子 "SHOULD for the name and id form; MUST for 'kind and id never change'". 范蠡 (agy, Gemini) is the outlier: MUST
on 37 of 46.

## What each added

- **Dave and Linus:** W3.2 (no credentials) conflicts with K4.1/K4.3 (never delete, never rewrite a claim). A
  credential committed inside a claim cannot be removed under both.
- **Linus:** K4.3 lists what an entry may gain after its first commit, and W6.3's "both links" may not fit that list.
- **Dave, verified by reading the tool:** which MUSTs `memory_index.py` already enforces, and which are unbuilt.
- **老子, 孫子, Dave:** a judged MUST with no assigned reviewer is a MUST in name only.

## What they need to know (merged, for EJ)

1. Is a reviewer assigned for the judged checks? Several ids move between MUST and SHOULD on this (老子, 孫子, Dave).
2. W3.2 against K4.1/K4.3: a written exception for removing a credential? (Dave, Linus)
3. K4.3 against W6.3's "both links". (Linus)
4. A secret scanner for W3.2? None exists. (孫子, Dave)
5. Rd3.1's strictest start-file limit, measured per agent. (Linus, 孫子, 老子)

## Check

`four_experts.py check`: 4 failures — 3 are 老子 script variants (為/爲, 輻 typed 輖), 1 is 孫子's 破國為次, which is
not in his list (the classical line is 破國次之): a misquote, not used for any level. The check was written by Claude;
it does not establish that the rules were applied well. Engines (`status.json`): Linus codex gpt-6.1-sol, 范蠡 agy
gemini-3.8-flash-medium (no fallback), 孫子 dsh, 老子 opencode, Dave a Claude subagent.

## Next

Round 2 on the 22 split ids: each expert sees all five round-1 rows and gives a final level. Rule for the result,
*mine, stated before round 2 runs*: an id is decided when three of the four give the same level to the same clause;
any id still split after round 2 goes to EJ with both sides quoted.
