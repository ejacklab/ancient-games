## 1. Codex's findings, adjudicated

Abbreviations: **S** = `SOURCE_OF_TRUTH-reviewcopy.md`, **R** = `RECOMMENDATION.md`, **C** = `codex-review-planted.md`.

| codex item | line it cites | verdict | evidence |
|---|---|---|---|
| 1 COVERAGE: PASS | none | CORRECT | The eight headings are in the brief's order at S:13, 17, 21, 25, 29, 33, 39 and 43. |
| 2 GROUNDING, first finding | S:15 | PARTLY | S:15 says "knowledge gained during one session is lost when the next session begins" with no `model knowledge` label. The brief requires one for the design's own additions. Grep for "model knowledge" in S returns nothing. The sentence is an inference from M3 (R:32) and R:111, not a quote. Codex overreaches on "M2/M7 support rebuilding repository memory, not 'all project knowledge'". M2 (R:31) says "a fresh clone can rebuild it", and R:111 supports "without the previous conversation". |
| 2, second finding | S:23 | PARTLY | The kinds list at S:23 carries no Layout cite, and the sentence's only tag is "(Write rules)". The kinds are defined at R:140-141, not in Write rules. But S:27 cites "(M11, Layout, …)" for the same list, and "not derivable from code, tests or git history" is in Write rules (R:153). This is a cite-placement slip, not an unsupported claim. |
| 2, third finding | S:31 | CORRECT | S:31 ends "keep the old body (M16)". M16 (R:45) is "The staleness check is deterministic"; the no-deletion rule is M13 (R:42). The diff against `docs/memory-system/SOURCE_OF_TRUTH.md` shows this is the only changed line. It reads "(M13)" there. `state.md` (the 2026-10-11 codex log entry) calls it the planted control. |
| 2, fourth finding | S:45 | CORRECT (low severity) | S:45 reads "Never load … the full session history … (M18)". M18 (R:47) reads "Never **auto-load**". R:185-187 does say "Never load" for the tree and graph dump, but not for session history. The paragraph opens "Never auto-load:", which softens the slip. |
| 3 NO INVENTED VALUES: FAIL | S:45 | INCORRECT | S:45 says "the recommendation gives no number, the owner sets it". Grep for "500" in S finds nothing. The string "500 entries" appears only in `DESIGN-planted.md:35` and in C:3. Codex's own earlier run on this same file returned item 3 PASS (`nodes/codex-review.stdout.md:3`). |
| 4 OWNERSHIP, first finding | S:19, 27 | CORRECT (omission) | S:19 gives who creates and who accepts. Nothing in S says who may change an entry afterwards. R:165-168 does: after acceptance only `status`, `verified_at` and `superseded_by` change, and fact and lesson bodies change "by diff". The brief requires "who may change it afterwards". S:27 gives only "no two agents edit one file". |
| 4, second finding | S:35 | PARTLY | Correct for `.cache/` and for who runs the INDEX generator. R leaves the generator unnamed too, calling it only "a deterministic script" (R:196). Overstated for AGENTS.md: S:19 puts policy under human acceptance (M12), and R:121 describes AGENTS.md as "canonical standing instructions". Overstated for the journal: the filename `<date>-<agent>-<session>` at S:35 carries the writer. S omits R:158-160 ("append `journal/` and a handoff"), so the omission itself is real. |
| 5 CONSISTENCY, first finding | S:27 vs R:140 | PARTLY | S:27 says "Every entry carries" the full list. R:140 says "use applicable fields". But M11 (R:40) says "Every durable entry carries …", and S:15 follows it. The source contradicts itself, and the design chose the M11 side. |
| 5, second finding | S:35, 41 vs S:9–10, 37 | PARTLY | S:35 does say "default layout … following claude's proposal in CP3". The next sentence says the recommendation "explicitly leaves CP3 unresolved", and S:37 is a proper `OPEN:`. R:116-118 takes the same posture, giving a memory/ default while CP3 is open. S:9-10 is the provenance block, not design text. See section 3. |
| 5, third finding | S:45 vs R:47 | CORRECT | Same slip as the fourth GROUNDING finding. |
| 6 GAPS | S:19, 27, 35 / 37 / 45 / 19 / 27, 41 | PARTLY | Gap 1 (change authority) and gap 5 (drift and contradiction) are real; see section 2. Gaps 2, 3 and 4 are already declared: placement is `OPEN` (S:37), and the cap and age threshold are "the owner sets" (S:45, S:19, R:188-190). They are not defects. |
| VERDICT: REPAIR | — | PARTLY | REPAIR is right (section 4). The stated reason, "a builder cannot determine who may maintain several artifacts", is true but narrower than the evidence. |

## 2. What codex missed

1. **Contested rows are cited as settled.** S:27 cites M23 alone, but M23 is CONTESTED (R:52, CP4 R:79-82).
   - S:27 says entries are written "at discovery or correction, or at task end". That is M24, also CONTESTED (R:53, CP7 R:95-99).
   - S:41 states the session-start read set as fact. That is M17, CONTESTED (R:46, CP6 R:90-93).
   - S:35 puts a "derived SQLite/FTS" cache in the layout. SQLite's role is M6, CONTESTED (R:35, CP1).
   - Only CP3 is flagged (S:37).
2. **No `model knowledge` label appears anywhere in S.** The brief requires one for every addition. Codex caught only the S:15 instance. S:15's "external service" is also not in M2 or M7 (R:31, R:36).
3. **Staleness is dropped, and S:19 invites an age reading.** S:19 has humans set "the age threshold" and never says staleness is computed from code drift, not age. R:18-19, R:44 (M15) and R:211-214 say age may only add a flag. S has no drift flag and no `disputed` handling beyond status words (S:19, 27). A builder reading S:19 would build age-based expiry.
4. **The layout lacks places the design requires.** S:19 makes `evidence:` mandatory, but S:35 has no `work/<task-id>/evidence/` (R:134) and no claim files (R:160). It also drops R:124-125 ("Never hand-edited") for `INDEX.md`.
5. **`OPEN` is not used in the required form.** The brief wants `OPEN: <what, and by whom>`. S:37 omits the "by whom". The cap (S:45) and the age threshold (S:19) are prose, not `OPEN:`. Codex lists these only as gaps.

## 3. What codex overstated or got wrong

- **Item 3 does not survive.** S:45 contains no "500". Codex's earlier run on the same file passed item 3 (`nodes/codex-review.stdout.md:3`). No file on disk has both M16 at line 31 and "500" at line 45: `DESIGN-planted.md` has M13 at 21 and 500 at 35, and S has M16 at 31 and no 500. Either codex read a copy that is no longer on disk, or it invented the finding. I cannot tell which. C:3 is a false positive against the file I was told to judge, and it makes the rest of C less trustworthy.
- **Double counting.** The S:45 "auto-" slip is reported as a GROUNDING finding and again as a CONSISTENCY finding (C:2, C:5). It is one defect.
- **Provenance cited as design text.** Codex cites S:9–10 as the design leaving placement OPEN. S:5-6 says only the text below the block is the engine's output, so S:9-10 was added by someone else and is not opencode's.
- **Source inconsistency charged to the design.** The "every field" finding blames S:27 for a split inside R (R:40 vs R:140).
- **Gaps 2–4 presented as gaps.** These are already `OPEN` or owner-decided (see the GAPS row in section 1).
- **Headline reason.** The VERDICT line says ownership is unknowable for "several artifacts". The design does state the agent/human split (S:19), and R leaves the INDEX generator and AGENTS.md maintainer unnamed. What the design actually lacks is the change rules R already gives at R:158-168.

## 4. My verdict on the design

DESIGN: REPAIR — the design cites M16 where M13 is meant (S:31) and drops "auto-" from M18 (S:45). It carries no `model knowledge` labels, which the brief requires (S:15). It omits R's post-acceptance change rules (R:165-168) despite the brief's "who may change it afterwards". It presents CONTESTED rows as settled (S:27, 41). Each of these is a small edit. None is a rebuild.

HEADLINE: AGREE — "ownership is incomplete" is the right headline, with a caveat. It breaks a non-negotiable brief rule ("One maker per artifact"), and the missing answer is sitting in R:158-168. The headline should also name the unlabelled additions and the contested rows silently settled (section 2, points 1-2). The mechanical citation slips are the cheapest fixes, not the main failure. This is my reading, not a measurement.

## 5. Reconciling my earlier PASS with codex's FAIL

Both are right on different things, and I overstated my PASS.

- **Line 31.** My check ran on `DESIGN-planted.md`, where line 21 correctly says M13 (`nodes/verify.stdout.md:2` cites M13 at line 21). Codex ran on S, which has M16. On the file I saw, my PASS was true. On S, codex is right.
- **Lines 15 and 45.** These are identical in both files (the diff shows only lines 31 and 45 differ, after the 10-line provenance offset). My PASS ("no mismatched citation", `verify.stdout.md:2`) missed the unlabelled addition at line 15 and the dropped "auto-" at line 45. Codex was right and I was too lenient. My check matched citation ids to rows. It did not test whether the cited row supports the sentence.
- **What this says about the four-item checklist.** It had no ownership, consistency or label-compliance item, so it could not see the failures the brief cares about most. It was validated by one control, the planted 500, and one control proves nothing about the other defect classes. I wrote that check and then passed it, so it is not independent evidence. That is the caveat CLAUDE.md asks for.
- **Codex is not a clean referee either.** It caught the M16 control, but it asserts a defect (500) that is absent from the file it names. The two reviewers fail in opposite directions: mine is lenient and codex's can be wrong. Neither verdict should stand alone.

Not established: which file codex actually read, and whether the design was edited between 10:11 and 10:28. I did not re-run codex.
