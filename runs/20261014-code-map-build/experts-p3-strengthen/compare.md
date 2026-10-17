# Four experts — strengthen A5's and A2's checks (base: the COO's proposal)

Question: `../briefs/p3/strengthen-a5-a2-question.md`. Asked: Linus, 范蠡, 孫子, 老子. Linus first failed on the Codex usage limit; his
rerun on 2026-10-16 answered (`status.json` ok, 105 s) and is summarised under "Linus (rerun)".

## A5

| COO item | 范蠡 | 孫子 | 老子 |
|---|---|---|---|
| 1 link case, `site` evidence | keep | keep (frozen test is the stronger home) | keep, as one case that pins the whole answer |
| 2 limit cases (`where <missing>`; no `--tests`) | keep both | keep not-found; **cut** no-`--tests` (A3's fact, charged elsewhere) | keep not-found only, as exact `equals limits[].reason` |
| 3 unasked section on link commands | keep | keep (ambiguous answer keeps `matches`) | cut as separate work: item 1's case covers it (`contract.ts` `allowedSections`) |
| 4 default text output | keep | keep intent; name known unrelated definitions that must not appear | cut as written; **add** a matcher clause: on a text case, `includes`/`excludes` check the text's `file:line` places (today they pass vacuously on text) |
| 5 held-out copy | keep | — | no work: the generator copies every bundled case (`holdout.ts`) |

Added by one expert: 孫子 — a `find` case with file and line; a `chain --up 0 --down 1` case with its depth limit;
exact `equals` on limits, not `limitReasons`; the report lists A5's four clauses and marks one with no case NOT
CHECKED. 范蠡 — `via` and `resolution` present on link answers. All three: the agent's unasked-map part stays P6.

*Verified by the COO:* `contract.ts` checks `site`, `kind`, `via` and the command's own sections on every case and
charges a failure to that case's requirement (`eval/run.ts`), so an A5-labelled link case makes A5's line fire.

## A2

| COO item | 范蠡 | 孫子 | 老子 |
|---|---|---|---|
| 1 chains through anonymous bodies, level ≥ 2, both ways | keep | keep, assert file and line, add the up direction | **cut**: `A2-const-chain` already goes 4 levels down through `Effect.fn`, a const and a property arrow |
| 2 `Effect.fn` step reached through a service | keep | keep, if the real shape is supplied | **cut**: already `A2-const-callers`/`-callees`; the real failure is a detail fixtures do not have |
| 3 A2's own line fires | keep | cut: every A2 line already has a case | cut: same |
| 4 shapes in the frozen tests | keep | fold into the keeps | cut as separate work |

Added: 老子 — one fixture: a body written straight into a call, `Effect.gen(function* () { … })` with no holder;
the tool's `belongsTo` (`nodes.ts`) counts its calls as calls by the surrounding named function, which may show a
link that contradicts the code (*verified by the COO: the rule is in nodes.ts as described; the effect is not
measured*). 孫子 — an `excludes` case (a same-named helper or fake is not a real link); a function reached twice
through an anonymous body shows `seen`; `kind` and `site` on the anonymous link; two same-named `Effect.fn` steps →
`ambiguous` with every candidate. 范蠡 — no over-building beyond the target's shapes.

## Linus (rerun)

*Quoted, condensed:* keep the COO's proposal, strengthened "to check complete relationships, relevant limits and
surplus output". What he adds that the other three did not:

- **A false pass on A2, reproduced.** `A2-computed-member` accepts a made-up link from `obj[key]()` to
  `chain/logic.ts:3` as long as the `dynamic` limit is there. *Verified by the COO with a probe of his own:
  0 mismatches.* The same probe shows `A5-default-text` accepts the right answer followed by a dump (0 mismatches),
  the gap 老子 named.
- **Same-link evidence.** `includes` accepts a caller, a site and a target found on different links; require them on
  the same link.
- **Longer-path-first shared node** (A2, "a known link within the depth is missing"): at depth 3,
  `root → a → shared → leaf` and `root → shared → leaf → tail`, `a` visited first; `tail` must survive the `seen`
  reference. Also reversed sibling order and an upward counterpart. *His reading from `commands.ts:334`, not run.*
- The no-`--tests` limit: he keeps it (范蠡 too); 孫子 and 老子 cut it as A3's fact. The COO's choice stays cut.
- Callback ownership (is an inline callback its own place?): *settled by the spec* — the enclosing function of a
  call is "the nearest function, method or arrow" (spec.md, the rule table), so it is its own place.

## Wording proposals (for the project owner; the checks never change the wording)

- **A2 Fails-if line 2, split by who acts** (范蠡, 孫子): tool — "an ambiguous match is not flagged, or a matching
  candidate is not listed with its location"; agent (P6) — "an ambiguous match is treated as certain, or a
  candidate the agent did not build is not named."
- **A2 "known"** (孫子): "a place / a link the type checker can establish" for "a known place / link".
- **A2 the body that holds the call** (老子): "A link names the body that holds the call. A body written straight
  into a call is a place of its own or a stated limit; it is never shown as a call by the function that surrounds it."
- **A5 unasked sections** (范蠡): "an answer comes inside a dump or with unasked sections, lacks its evidence or
  limits, or a whole map is produced unasked."
- **A5 whole answer and its limits** (老子; 孫子 similar): "A specific question gets that whole answer, with its
  evidence and its limits. Where the answer stops short — a cap, a sample, a first page — it carries the limit that
  says so. A limit the interface requires for that command is part of the answer."
- **A5 the map clause, split by who acts** (孫子): tool — "no command other than a module map returns map content";
  agent (P6) — "the agent runs `map` only when the user asked for a module map."
- **A5 form** (老子): "…in the form the tool answers in, JSON or the default text the agent reads."

- **A5 content boundary** (Linus): "A specific answer contains the requested result, its supporting evidence,
  applicable limits and any candidates needed to resolve ambiguity. It excludes unrelated definitions, links, flows
  and tables, whether they appear in another section or inside the requested payload. This applies to JSON and
  default text output."
- **A2 depth** (Linus, conditional on depth meaning shortest call distance): "The place is level 0; each call link
  adds one level. Every known link reachable within the selected depth is included regardless of traversal order.
  Reaching a function again produces a reference without losing links reachable through a shorter path."

## Check

`four_experts.py check`: 范蠡 and 孫子 pass; 老子 fails on one character, 以約為紀 against his list's 以約爲紀 (a
script variant of the same quote, not an invention); Linus no answer. Engines: 范蠡 agy, 孫子 dsh, 老子 opencode. The
check script was written by Claude and checks sections and citations, not whether a rule was applied well.
