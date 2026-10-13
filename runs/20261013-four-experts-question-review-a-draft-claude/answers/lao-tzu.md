I'll read the brief first.
# 老子 (Laozi) — draft `.claude/agents/researcher.md`

## Answer

Right in shape, wrong in three places where it re-opens failures the repo already paid for on 2026-10-11: its eight judging rules are not the rules the repo's own checker enforces, a failed read is not separated from a thing that does not exist, and the contradiction stop that TASK_TYPES demands is absent. On current practice the file is sound in its frontmatter but spends ~90 words of `description` in every session's context and leaves `Write` containment as an instruction when the harness now offers a hook. (Web: I fetched the current Claude Code subagent docs, `docs.claude.com/en/docs/claude-code/sub-agents`, and used them; I did not survey community practice, so "current practice" below means the vendor's documented behaviour, not a survey.)

## How I decided

**1. Line 42, "The standard your files are judged by" — replace the eight rules with what `check-findings.py` actually checks.** It enforces: ≥5 rows (`--min-rows 5`); every non-control row carries a 4-digit year in claim+source (`YEAR` regex — so `2026-04 (month only)` **passes**, the month-only lesson does not bite here); every non-control source cell contains a URL or a `file:line`; label in `verified/reported/unknown/unproven`; ≥4 cells; and the control name appears somewhere in the file. The draft enforces things no checker looks at (a verbatim quote, "a source date") and never states the five that do. Worse, line 34 promises "the template's five bold parts" while `validate_result.py` has `DIGEST_HEADINGS = ["Answer", "Confidence", "Decision it triggers"]` — three. A researcher optimising for the draft can drop a checked heading to fit the 20-line cap. Line 34 → "the three parts `validate_result.py` reads: **Answer**, **Confidence**, **Decision it triggers**; Cautions and Gaps if they fit under the cap." — *my #8: a standard nobody can check is not a standard.*

**2. Line 52–53, rule 6 — a failed read must never become NOT FOUND.** The ledger's third2026-10-11 blocker was an executor null return; the draft's only protection is line 57's "failed fetch" under Gaps. Add: *"If a fetch or a read returns nothing, narrow it once and fetch again. If it returns nothing twice, it goes under Gaps as not read. A read that returned nothing is never evidence that the thing does not exist."* — *my #8: 知不知 — the null return is not knowledge of absence.* Cost: one extra call per dead fetch, and a retry rule with no cap teaches endless retry.

**3. Line 51, rule 5 — add the stop.** TASK_TYPES row 100's sabotage is "seed conflicting sources → **the join stops**"; the draft says give both rows and carry on, and the digest's *Decision it triggers* is the only place a stop could surface. Add to rule 5: *"When a contradiction cannot be settled from the sources, stop reading that question and write `CONTRADICTION` in the digest with both rows. Do not pick a side, do not average, do not carry on."* — *my #12: 將欲歙之，必固張之 — the repo already added the stop (stretching) before it taught itself to resolve (shrinking).*

**4. Line 42 — the control query has no instruction.** Add one line: *"A control query the brief gives is a row like any other: name it, cite the queries that returned nothing, label it `unproven`. Never write a control name into any file another worker will read."* — *my #12 again: the control is void if it leaks, and nothing in the draft can leak it today only because no run has named one yet.*

**5. Line 23 and line 13 — the file demands a date the researcher cannot get.** `Produced <date>` and `<YYYYMMDD>`; the researcher has no Bash for `date`, and the docs say a subagent receives only its system prompt plus environment details. Fix line 13: *"The brief's date. If the brief gives none, name the folder `date-unknown-<topic>` and say so under Gaps; never guess today from context."* — *my #2: 知足 — a made-up date is worse than a missing one.*

**6. Line 14 contradicts lines 17 and 17's template.** `runs/<run-id>/nodes/` says "your result file" — singular — while the section below it is "The two files". Method 3.8 item 9 names one home only. Fix: delete line 14, or make it "**both** files go to the run folder the brief names, and the digest must still satisfy `validate_result.py --kind digest`." — *my #4: 執者失之 — two homes for one deliverable is the thing that gets lost.*

**7. Line 4 — `Write` containment is an instruction; the harness now offers a mechanism.** The fact is right that the tool list cannot scope `Write`. Current docs list `hooks` as a subagent frontmatter field, "scoped to this subagent", so a `PreToolUse` hook can deny `Write` outside `docs/research/*/`, `runs/*/nodes/` and the brief's folder. — *my reading; the words of ch. 64 do not say this.* Price: a hard block where today there is a misplaced file.

**8. Line 3 — the `description` is ~90 words and loads into every session.** The docs are explicit that descriptions take up context and should be short. Cut to the dispatch decision, and move "(method 3.8 item 9)" into the body where the rest of the method already lives. Proposed: `Researches from external sources — web, vendor docs, papers, other repositories. Returns a digest and a path, never the full findings. Use for many main sources or web-versus-repo source kinds. Not for this repo's own code, and not for a question one search answers.` — *my #1 and #2: take away until what is left is only the use.*

**9. Line 49–50 — the draft's label set is right; the template is stale, and the file should say so.** `check-findings.py` defaults to exactly `verified/reported/unknown/unproven`. `research-file.md` line 73 lists three; TASK_TYPES row 100 lists `CONFIRMED/INFERRED/GAP/UNPROVEN`. Add: *"Labels are exactly `verified / reported / unknown / unproven` — the set `check-findings.py` checks. Neither the template's three nor TASK_TYPES' four is used."* And fix `unproven`, which line 50 defines as "claimed without evidence" while rule 6 makes a sourceless claim not a finding at all — → *"asserted by a source you read, which supplies no evidence for it."* — *my #4: 為者敗之 — acting on the template as if it were the contract is what breaks the row.*

**10. Line 65 — the budget is unenforceable prose.** `maxTurns` is the only mechanism the harness offers (it marks output partial). Add it or accept the price. — *my #2.*

**More than it needs:** line 73 restates CLAUDE.md's 2026-10-11 labelling rule verbatim, and every custom subagent loads CLAUDE.md (9.2 kB) plus a git-status snapshot unless `omitClaudeMd: true`. Do **not** set `omitClaudeMd` here — that file is the contract you are trying to ship to the worker — but line 73 is the one line that may go. — *my #1.*

## What I need to know

- Is `researcher.md` the canonical label vocabulary (and `research-file.md` corrected), or the template?
- Is Bash acceptable on a web-facing subagent so it runs `check-findings.py` on its own file, or does the contract stay check-after-return? This is the biggest blast-radius decision here and I would not make it myself.
- Which is authoritative for a run-scoped result: `docs/research/<date>-<topic>/` (method 3.8 item 9) or `runs/<run-id>/nodes/`? CLAUDE.md's 2026-10-06 rule says pass-back evidence points into `runs/<run-id>/`, so these two conflict.
- Does the date go into the delegation brief, or does the researcher get `date`?
- Is a PreToolUse hook in scope here, or is the instruction enough?
- `.claude/agents/` is **untracked** in git and there is no `.claude/settings.json`. Is that intended for the file the whole research contract depends on?

## Costs and risks

- The checker-shaped rewrite makes the rules machine-shaped and easy to satisfy narrowly; the researcher may optimise for the checker instead of truth. Keep "not found is an answer" and "never fill the gap from your own knowledge" outside the enumerated list. — *my #2*
- The retry rule costs a call per dead fetch and can teach endless retry; "narrow once" is the cap. — *my #7*
- The contradiction stop creates a new COO action that is not in any template; the main agent must be ready to receive `CONTRADICTION`. — *my #12*
- `date-unknown-<topic>` breaks the `YYYYMMDD` folder convention that `docs/research/` assumes. — *my #2*
- Dropping `runs/<run-id>/nodes/` breaks the `evidence:` back-link into the run folder (CLAUDE.md, 2026-10-06). — *my #4*
- A `Write` deny hook turns a misplaced file into a blocked deliverable; its message must name every folder the researcher may write to. — *my reading*
- Adding Bash hands a web-facing agent arbitrary command execution; `ancient_games/` has a Guard stage precisely because this is the risk. — *my #4*
- Trimming the `description` loses the "(method 3.8 item 9)" trace EJ may want. — *my #1*
- Keeping the template's three labels in place guarantees a future run picks the wrong set. — *my #4*
- Every finding above is `my reading` against the repo's own scripts and the vendor docs; I verified each script's actual check by reading its code, and I read the draft in the repo, not only in the brief. The one thing I did not verify is whether `check-findings.py` is meant to ship as a general checker or stay a per-run script — its `CONTROL = "magmamem"` constant says per-run, which is why item 4 matters more than the other nine.

## How we would know I was right

1. Sabotage it, as TASK_TYPES demands of every row: seed a nonexistent system name, a known divergence with two citations, and two conflicting sources. It must return NOT FOUND with the queries, emit both rows with both citations, and stop at the contradiction.
2. Run `check-findings.py` **on the produced file from inside the subagent**. If it cannot — no Bash — that is the evidence for change 2, not a side note.
3. Produce a five-part digest and a three-part digest. If the one satisfying the draft fails `validate_result.py --kind digest`, or the one satisfying the checker fails the draft, change 1 is proven.
4. Kill the network mid-run and give it a question. A false NOT FOUND means change 2 is not enough.
5. Trim the `description` and re-seed one question that should reach the researcher and one that should not; if delegation changes, the trim cost was not worth it.
6. Check `/tasks` after a hand-off and confirm `model: inherit` is what the run's ledger expects — `docs/EXECUTOR_KINDS.md:60` names "the session model on Claude Code" for the Claude researcher, so `inherit` is right and should stay.
