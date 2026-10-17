# Dave — five decisions to finish the source-of-truth memory design

## Answer
- **D1:** `project-memory/start-limits.json`. It is a JSON list with one row per limit: `agent`, `limit`, `unit`, `basis`, `source`.
- **D2:** The file is the switch.
  - **File absent:** the Rd3.1b example applies, and every run prints that it does.
  - **File present:** its rows alone apply.
  - **File the tool cannot read** (it does not parse, or has no rows): the check fails.
  - **An agent with no row:** the tool cannot see an agent the file does not name, so the project owner catches this, not the tool.
- **D3:** Every path either side wrote in place of the old one is kept, and the old path stays removed. The merge is reported in `state.md` for the project owner. This is the pattern W6.3a already uses for two supersessions of one entry, applied to `covers`.
- **D4:** Option (a), kept narrow. Add fixed-prefix patterns only, inside `tools/memory_index.py`. No entropy, keyword or JWT rules, and no waiver at the start. The reviewer stays the check for everything the patterns cannot see.
- **D5:** Measure now, in S5. Use sentinels on both sides of the two figures already documented, a control file, and a token that is in no file. The exception: if the owner says agy loads `INDEX.md` in no planned project, skip it until one does.

## How I decided

**D1 — where, and what format**
1. My #5. The YAML's `kit` key says *"`project-memory/`, `AGENTS.md`, `CLAUDE.md` and `runs/` are the project's own"* (read: `SOURCE_OF_TRUTH_REQUIREMENTS.yaml:64-68`). Rd3.1a has the project owner record *their* agents. So the rows belong to one project. My reading: a file in `docs/memory-system/` would travel with the kit and carry one project's agents into the next project.
2. My #5. `.githooks/pre-commit` runs `--check` only when something under `project-memory/` or `tools/memory_index.py` is staged (read). So lowering a limit inside `project-memory/` checks `INDEX.md` in that same commit. The same edit in `docs/memory-system/` would not, and the failure would first show up on someone's later, unrelated memory commit.
3. My reading of `tools/memory_index.py:39,43` (not run): an entry is only `project-memory/entries/[DFLOH]-*.md`. A `.json` file next to `INDEX.md` is never mistaken for an entry.
4. My #4, comparing against the current way. The tool is *"Python 3, standard library only"* (read: `docs/index-md/DESIGN.md:12`).
   - **JSON** ships with every Python 3 (research, verified).
   - **TOML** is standard library only from 3.11, which adds a minimum version the design does not state.
   - **YAML** needs PyYAML (research, verified), which breaks the standard-library rule.
   - TOML's one advantage is comments, and it does not help here. The basis has to be a field that the tool reads and prints (B4.2), not a comment it skips (my reading).
   - So JSON, parsed with an `object_pairs_hook` that rejects a repeated key. The docs say that otherwise the last value silently wins (research, verified).
5. My #9: last round I chose YAML for this file and never said how the tool would parse it. The research shows it cannot without PyYAML. I drop it.
6. Fields. Rd3.1a names agent, limit, unit and basis.
   - I add `source` (*proposed*): a `documented` row with no source cannot be checked. This follows the lesson that each fact carries its source.
   - `unit` is one of the four units the documented figures use: `lines`, `bytes` (UTF-8), `characters`, `utf16_units` (research rows: Claude Code, agy, agy as reported, Qwen).
   - Any other unit fails the check. My reading: a standard-library tool cannot count tokens.
7. Insight `runs/20261016-four-experts-what-counts-as-change/insight.md#F-d8221199`: a check that reads uncommitted state fails depending on *when* it runs. What it changed: check mode reads the limits file from the same tree as the entries (the staging area, or `<rev>`), never from the working tree.

*Words to write.*
- **Rd3.1a:** replace "in one file the tool reads" with "in `project-memory/start-limits.json`, which the tool reads".
- **`docs/index-md/REQUIREMENTS.md` B4.1:** add "The limits file is a JSON list. Each row has `agent`, `limit` (a positive whole number), `unit` (`lines`, `bytes`, `characters` or `utf16_units`), `basis` (`measured`, `documented` or `example`) and `source`. Check mode reads it from the same tree as the entries. `INDEX.md` must fit every row, and each run prints each row with its basis."
- **Example row:** `{"agent": "agy", "limit": 24000, "unit": "bytes", "basis": "documented", "source": "https://antigravity.google/docs/rules, read 2026-10-17, per rule file"}`

**D2 — when the example stops**
8. My #1: what would change my mind is any way for the tool to know which agents load `INDEX.md`, other than the file. There is none. The tool reads entries and git, not the engines (read: the tool's docstring, lines 1–15). "Only when every agent has a row" therefore cannot be checked by the tool. Rd3.1a's `who_decides` makes the project owner the one who names the set, so the owner is the check for a missing agent.
9. My #4 and my #8:
   - **Control:** with no file, the tool behaves exactly as today, using its constants. No project changes on upgrade.
   - **Reversible:** deleting the file brings the example back.
   - **Why not an error:** Linus made a missing file an error last round. That would fail every existing project on its first commit after the upgrade, with no defect to fix (my reading).
   - **A bad file fails loudly:** last round, Linus, Sun Tzu, Laozi and Dario all said a malformed file fails (read: `compare.md`).
10. My reading: some agents the owner names have no known limit (opencode and Gemini CLI state none, per the research). Each gets a row with basis `example` and the Rd3.1b values. That makes them "unknown, held at the example", never unlimited.
11. My reading: a file with no rows fails. Otherwise it would switch the size check off with no sign.

*Words to write.*
- **Rd3.1a, last sentence:** "While that file is absent, the tool holds the example in Rd3.1b and says so on every run. Once it exists, its rows alone apply, and a file the tool cannot read, or one with no rows, fails the check."
- **Rd3.1a `fails_if`:** "(until the tool reads the file, the example)" becomes "(while the file is absent, the example)".

**D3 — both sides change one `covers` path**
12. My #5. W6.3a already says *"every `covers` path either side wrote"* is kept, *"Nobody chooses between two claims"*, and two supersessions are *"reported in the task's `state.md` and to the project owner, as in Rd5.3"* (read). Take a base path P that side A replaces with Q and side B replaces with R:
    - Neither side left P alone, so P stays removed.
    - Q and R are both paths a side wrote, so both are kept.
    - The existing words already give "keep both". What they lack is who decides which new path is right.
13. "Keep the path that exists" cannot be enforced. The tool does not read `covers` at all (ran: grep for `covers` in `tools/memory_index.py`, no match), so existence would be the merger's hand check. Both paths may also exist, for example when one side split a file. Either way the merger would be choosing (my reading).
14. Insight `runs/20261016-integrate-r11-r13/insight.md#F-d8a49e5a`: a restated requirement that paraphrases widens or narrows it. What it changed: the addition reuses W6.3a's own words ("wrote", "stays removed", "as in Rd5.3") instead of new ones.

*Words to write.*
- **W6.3a text, after "…records the removal (K4.3).":** "When both sides removed or replaced the same `covers` path and their results differ, it stays removed, every path either side wrote in its place is kept, and whoever does the merge reports it in the task's `state.md` and to the project owner, as in Rd5.3. The project owner corrects `covers` with a `changed:` line (K4.3)."
- **W6.3a `fails_if`, add:** ", or a `covers` path both sides changed goes unreported."

**D4 — the secret scanner**
15. My #5 (ran, via ripgrep). I ran the research table's fixed-prefix patterns over two sets of files:
    - **This repo's Markdown that `.gitignore` does not exclude:** 1 hit. It is AWS's documented example key, `AKIA…EXAMPLE`, quoted at `runs/20261018-sot-finish/s1/dario/answers/dario.md:60`. That is a false positive.
    - **The 48 house memory notes:** 0 hits.
    - **Placeholders matched too, in git-ignored vendored code:** `sk_live_` followed by x's, `glpat-` followed by x's, and the same AWS example key.
    - **Caveats:** my private-key pattern was the header only, looser than gitleaks' rule, which needs a 64-character body. No `project-memory/entries/` exists anywhere here, so nothing ran on real entries. This is one search, so a hint, not a law (my #10).
16. My #9: my first try used the OpenAI marker `T3BlbkFJ` on its own. It hit the copies of this question's own table, 16 lines. A pattern must be the whole key shape, never a fragment.
17. My #4, comparing against reviewer-only. The reviewer reads after the commit. My reading: a credential in a commit stays in history until history is rewritten, and the key has to be rotated. The pre-commit hook runs `--check` *before* the commit. The difference is when it is caught, not how much: the measured count of real secrets today is zero either way.
18. My #8 rules out the outside scanners. A pattern list in the tool is a few standard-library lines, with nothing to install, and is easy to remove. The outside scanners (research, verified):
    - none is installed here;
    - gitleaks is "feature complete", with security patches only from now on;
    - trufflehog's live check calls the services the keys belong to;
    - detect-secrets is not standard library, and its hex entropy rule would have to sift commit ids. Crude count (ran): 46 of 48 memory notes hold a run of 7 or more hex digits. Dates and run ids count too, so this is the pool such a rule would sift, not what it would flag.
    - each one adds an install step to every project that uses the kit.
19. My #6 and #7. *Recall, not deciding:* innate immunity recognises conserved markers at the barrier, cheaply.
    - **Same:** vendor prefixes are markers the issuer added so that keys can be found (research: GitHub blog).
    - **Different:** a password has no marker, and that is the key condition. So the analogy holds for prefixed credentials only, which is exactly the scope I give the tool.
20. My #8 and #1: no waiver at the start. The one hit was an example, and an entry's author can shorten it (`AKIA…EXAMPLE`). A false positive that cannot be reworded is what would change this.
21. My reading: the report names the file, line and rule, never the matched text. Printing the match would put the secret into hook and CI output.

*Words to write.*
- **YAML `checks.secret scanner`:** "`tools/memory_index.py`, in write mode or with --check, fails an entry that holds a credential in a fixed-prefix form (the list is in `docs/index-md/`). It cannot find passwords, tokens with no fixed prefix, or personal data: for those, the reviewer is the check."
- **New B item in `docs/index-md/REQUIREMENTS.md`:** "The script fails an entry that matches one of these patterns, taken from gitleaks' default config:
  - AWS access key id;
  - a private-key block with a body;
  - GitHub `ghp_`, `gho_`, `ghu_`, `ghs_`, `ghr_`, `github_pat_`;
  - GitLab `glpat-`;
  - Slack `xoxb-`, `xoxp-`, `xoxe-`;
  - Anthropic `sk-ant-api03-`;
  - OpenAI (the full key shape around `T3BlbkFJ`);
  - Stripe `sk_` and `rk_` with `live`, `test` or `prod`;
  - Google `AIza`.

  It has no entropy, keyword or JWT rules. It reports file, line and rule, never the value. There is no waiver: an entry that quotes an example writes it shortened."

  My reading (not run under Python `re`): none of these patterns needs the `(?-i:…)` group, so there is no 3.11 floor.

**D5 — measure agy**
22. My #5: nothing has been measured. Two figures conflict:
    - 24,000 bytes per file, documented on the official page (verified);
    - 12,000 characters, from a third-party page (reported).

    The tool's live default *is* the 24,000-byte figure (read: `tools/memory_index.py:30-36`). If the older figure holds for the installed agy 1.4.0, the tool passes an `INDEX.md` that agy cuts short. A MUST would then fail without anyone seeing it.
23. My #2: S5 is budgeted at about 15 minutes (read: `workflow-design.md:46`), and two expert rounds have already argued this question.
24. My #1: if the owner says agy loads `INDEX.md` in no planned project, the measurement decides nothing. In that case, skip it until one does.
25. My #3: write the prediction down before the call.
    - **Metric:** which sentinels agy reports.
    - **Expected, from the official page:** every sentinel before 24,000 bytes is seen, and none after.
    - **Expected, from the reported figure:** a cut near 12,000.
    - **Stop:** the end of S5.
26. My #4 and insight `runs/20261016-four-experts-what-counts-as-change/insight.md#F-21e1586c`: a planted failure must be shown to be the planted one. What it changed: two controls.
    - A control file well under both figures, with its own sentinel, must be reported.
    - One random token placed in no file must *not* be reported.
    - A run where either control fails is recorded as "method failed", never as "limit found" (my #9).
27. Method (my reading, built from the brief's sentinel idea):
    - Use a scratch workspace with no other rule file.
    - Put the test file in the load path the owner names for agy. If none is named, use `AGENTS.md` at the workspace root, and say the result covers that path only.
    - Fill it with ASCII and place random sentinels just under and just over 12,000 and 24,000. These positions come from the two documented figures, not from a new number.
    - Run it more than once: one run is a hint (my #10).
    - If time allows, a second file with multi-byte filler tells characters from bytes.
    - Copy the evidence into `runs/20261018-sot-finish/`.

*Words to write:* nothing in the design now. If the measured cut is under 24,000 bytes, the Rd3.1b example and the tool's constants need revisiting. That is a separate decision for the owner.

*Proposed change to the pattern:* a measuring piece writes its prediction (metric, expected result, stop) to its output file before its first engine call, and its check compares the two. This would change S5's brief.

Insight categories: none was named, so I chose `check` (F-d8221199, F-21e1586c) and `instruction` (F-d8a49e5a) from the index.

## What I need to know
1. **Which agents load `INDEX.md` at session start, and by which path, in the first project that adopts the kit?**
   - If agy is not among them, D5 becomes "not until it is".
   - If agy loads it as a `.agents/rules/` file rather than through `AGENTS.md`, S5 measures that path instead.

## Costs and risks
- **D1** (my #4): JSON has no comments, and a stray trailing comma blocks a commit until it is fixed. That is loud, but it is a stop. Each project writes its own file; the kit ships none.
- **D2** (my #10):
  - An agent the owner forgets to list is never checked, because the tool cannot see it.
  - A project can stay on the example forever. Printing it on every run makes this visible but does not fix it.
- **D3** (my #9): a wrong new path stays in `covers` until the owner acts. Every both-sides change costs the owner one decision.
- **D4** (my #8):
  - S4 grows by one piece: a spec line, tests and code.
  - Quoted examples trip it (1 in this repo's Markdown, measured) and have to be shortened.
  - It misses passwords, tokens with no prefix and personal data, so the reviewer still carries those.
  - Tests must build key-shaped strings at run time, so the public repo never holds a literal one. My reading, not checked: GitHub's push protection may flag such a string.
- **D5** (my #2, #10):
  - About 15 minutes of S5.
  - The result rests on agy reporting what it read. If it misses a sentinel that was loaded, that reads as a cut. The controls catch a total miss, not one skipped sentinel, so repeat runs matter.
  - The result holds for agy 1.4.0 and one load path only.

## How we would know I was right
- **D1 and D2, as S4 tests:**
  - With no file, the example is used and printed.
  - A row looser than the example lets an `INDEX.md` that is over the example pass.
  - A trailing comma, a repeated key, an unknown unit or basis, or an empty list each fail the check.
  - `--check <rev>` uses `<rev>`'s file, not a different working-tree copy (F-d8221199).
- **D3:** on the first merge where both sides changed one path, the reviewer finds both new paths, no old path, both `changed:` lines, and a `state.md` report.
- **D4:**
  - A test entry with a key-shaped string built at run time fails, and the failure names that rule and that line (F-21e1586c).
  - A control entry with a shortened example passes.
  - A private-key header with no body passes.
  - Prediction for the first project's real entries: no flag that is neither a credential nor a quoted example. A flag of any other kind removes that pattern.
- **D5:** first the controls must pass: the control sentinel is reported and the absent token is not. Then the cut position is compared with the written prediction.
  - **Cut under 24,000 bytes:** the example is wrong for agy, and measuring was right.
  - **Cut at 24,000:** the page is confirmed and the 12,000 report is closed. That null result is reported with the same weight (my #9).
