# 范蠡 (Fan Li): five decisions to finish the source-of-truth memory design

## Answer
- **D1.** Put the limits in `project-memory/start-limits.json`, which belongs to the project. Use JSON. A row is one agent and one unit, with six fields: `agent`, `load_path`, `unit`, `limit`, `basis`, `source`.
- **D2.** The example stops **row by row**. A row whose figure is measured or documented *for the load path `INDEX.md` uses* replaces the example for that agent.
  - If the file is missing, the example holds, and every run prints that it is the example.
  - A file the tool cannot parse fails the check.
  - Every reader gets a row. An agent whose figure is not known has `basis: example` and no `limit`. An agent left out of the file is the reviewer's finding.
- **D3.** Report the clash in the task's `state.md` and to the project owner. Until the owner decides, keep every path either side wrote. W6.3a already says this, so the merger chooses nothing.
- **D4.** Choose **(a)**: a small standard-library check in `tools/memory_index.py`. It looks only for credential formats with a fixed prefix, has no entropy rules and no waiver, and leaves everything else to the reviewer. It is built in its own later run.
- **D5.** Measure **later, on a trigger**, and only agy. The trigger is a project's limits file naming agy as a reader while that project's `INDEX.md` is larger than the lowest figure any source gives for agy. If no project ever names agy, never measure.

## How I decided

**D1: where and what format**
1. My #14 (*quoted*): 「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也。」 Say who is better at what.
   - The design gives the method. Only the project owner knows which agents load `INDEX.md` (Rd3.1a `who_decides`: project owner).
   - A file in the design's folder would travel with the kit into every project and carry another project's agents. So the file belongs to the project.
2. My #2 (*quoted*): 「節事者與地」. Regulating affairs goes with Earth, the ground you already stand on (my reading of how it applies).
   - The tool already reads only under `project-memory/` (*read*: `tools/memory_index.py:38-40`).
   - Its check mode reads git objects (*read*: `:5-6`, `:11`). A file there is read from the same commit as the entries, so the tool needs no new place to look.
3. My #3 (*quoted*): 「自若以處」, stay as you are; 韋昭: 無妄動也, no reckless move.
   - The tool is standard library only (*read*: `:17-28`).
   - JSON ships with Python and has no minimum version (research, verified python docs).
   - TOML adds a Python 3.11 floor. Neither the tool, its spec nor the design states a Python version (*ran*: grep for a version in `docs/index-md/REQUIREMENTS.md`, the tool and `SOURCE_OF_TRUTH.md` found none).
   - YAML needs PyYAML (verified).
   - JSON has no comments. The `source` field does that job.
   - Last round I marked my JSON point as *recall*. It now rests on the research.
4. A row covers one agent and one unit. Claude Code's "200 lines or 25 KB" becomes two rows, so the tool compares each row against one count in one unit without converting (my reading).

**Words to write (D1).**
- Rd3.1a: replace "in one file the tool reads" with "in `project-memory/start-limits.json`, which the tool reads from the same tree or commit as the entries".
- `docs/index-md/REQUIREMENTS.md` B4.1: replace the last two sentences with:

  > "The script reads the limits from `project-memory/start-limits.json`: from the working tree in write mode, and from the staging area or the commit in check mode. The file is a JSON object. Its `agents` key is a list of rows, one per agent and unit. Each row has `agent`; `load_path` (how `INDEX.md` reaches that agent at session start); `unit` (`lines`, `bytes` for UTF-8 bytes, `characters`, `utf16` for UTF-16 code units, or another unit); `limit`; `basis` (`measured`, `documented` or `example`); and `source` (where the figure is written: a URL, or the run file that holds the measurement and the engine version). A row with `basis: example` has no `limit`."

**D2: when the example stops**
5. My #1 (*quoted*): 「人事至矣，天應未也，王姑待之。」 When one had come and the other had not, he told the king to wait.
   - A figure only applies where it meets the load path `INDEX.md` really uses.
   - The research gives Claude Code's 200 lines or 25 KB for `MEMORY.md` (*read*: `runs/20261017-sot-item11/research/experts.md`, per the question). If `INDEX.md` reaches Claude Code another way, that row holds the example.
6. My #4 (*quoted*): 「得時無怠，時不再來，天予不取，反為之災。」 Once a row has its figure, use it at once.
   - Waiting until every agent has a row would let one unknown agent block a known limit.
   - Row by row is never looser than the rule. The index fails if it goes over any row's limit, which is the strictest limit taken one unit at a time.
7. My #3 (*quoted*): 「時不至，不可彊生；事不究，不可彊成。」 A missing file is not forced into existence: the example holds, as Rd3.1a's own text says.
   - B4.2 already prints the size on every run, so the run can also print which limit applied and its basis (*read*: `docs/index-md/REQUIREMENTS.md:67`).
8. My reading: a file that exists but cannot be read must fail. If it fell back silently, it would hide the owner's record.
   - The tool cannot see an agent missing from the file. That is why every reader gets a row, with `basis: example` when no figure is known.
   - An agent left out is found by the reviewer, since the owner decides the set.
9. My #5 (*quoted*): 「唯謀不遷」, the plan does not shift: one rule, one text. Three texts disagree today:
   - the YAML's `how_to_read` says "Rd3.1a's interim numbers hold only until the limit is measured" (*read*: `SOURCE_OF_TRUTH_REQUIREMENTS.yaml:24-25`). The numbers are now in Rd3.1b, so this line is also out of date;
   - B4.1 says "Until then", meaning until measured (*read*: `:63-66`);
   - Rd3.1a says "Until the tool reads that file".

   The MUST record governs over a reading note (my reading). The other two are changed to match.

**Words to write (D2).**
- Rd3.1a: replace the last sentence with "The tool holds the example in Rd3.1b while the file is absent, and for each agent whose row has no measured or documented limit."
- Rd3.1a `fails_if`: replace "(until the tool reads the file, the example)" with "(where the file records none for an agent, the example)".
- Rd3.1b: replace "Until it reads the project owner's file (Rd3.1a)" with "Where the project owner's file (Rd3.1a) records no measured or documented limit".
- `how_to_read`: replace the line with "Rd3.1b's example numbers hold only where Rd3.1a's file records no measured or documented limit."
- B4.1: add

  > "The index fails if it exceeds any row's `limit` in that row's unit. Where the file is absent, and for a row with `basis: example`, the script holds the design's example (`MAX_LINES`, `MAX_BYTES`). The check fails on a file that does not parse, a repeated key, a row missing a field, or a `basis` not in the list. A row whose unit the script cannot count (for example tokens) is printed as not checked by the script, never as passed; the reviewer checks it."

- B4.2: replace with "Every run prints the size against each limit it applied, with that limit's agent and basis."

**D3: both sides change the same `covers` path**
10. My #14: the merger is not the one who can judge which of two renames is right. The YAML gives contested choices to the project owner (*read*: `roles`, `:49-53`; W6.3a `who_decides: project owner`).
11. My #5, 「唯謀不遷」: W6.3a already has a plan for this.
    - It says "keeps both sides … every `covers` path either side wrote", and "Nobody chooses between two claims".
    - Two supersessions of one entry are "reported in the task's `state.md` and to the project owner".
    - The same rule applies here; this case gets no new one.
12. My #3 (*quoted*): 「待其來者而正之」, wait for what comes and set it right. The owner removes the wrong path afterwards with a `changed:` line.
13. Why not "keep the path that exists in the repository":
    - The tool never reads `covers` (*ran*: grep for `covers` in `tools/memory_index.py`: no match). That rule would be the merger's unchecked judgment, which is choosing.
    - Both paths may exist (for example a file split in two), or neither.
    - A dead path is still caught: the vision makes every reader check a decision or fact against the code before acting, and report a mismatch (*read*: vision statement, "What it will never do").

**Words to write (D3).** W6.3a:
- after "its `changed:` line records the removal (K4.3).", add: "When both sides change the same `covers` path differently, the merge keeps every path either side wrote, and the clash is reported in the task's `state.md` and to the project owner, who removes the wrong path with a `changed:` line."
- in `fails_if`, add: "or a `covers` path both sides changed differently goes unreported."

**D4: secret scanner**
14. My #14: a regex is better than a reviewer at exact formats, on every commit. The reviewer is better at passwords, tokens with no prefix and personal data, which the research says no prefix check finds. So split the work by who is better at it.
15. My #18 (*quoted*): 「審備則可以戰乎？」 Examine the preparations; the list glosses 備 as 守禦之備, defensive preparations. With the reviewer alone, W3.2, a MUST, is guarded by a single judged check. The cheap, exact part is there to add.
16. My #11 (*quoted*): 「用力甚少」, very little force. The tool and its pre-commit hook already run on every commit, and Python `re` runs the fixed-prefix patterns in a few lines.
    - The patterns come from the research table, quoted from gitleaks' default config: AWS access key IDs, private key blocks, GitHub (`ghp_` `gho_` `ghu_` `ghs_` `ghr_` `github_pat_`), GitLab, Slack, Anthropic, OpenAI, Stripe, Google.
    - The generic rule, JWT and entropy are left out. Entropy rules flag commit hashes, and this knowledge repo cites them (research, the researcher's reading).
    - Leaving out the generic rule also avoids its 3.11-only `(?-i:…)`.
17. My #3, 「自若以處」: (b) would be a reckless move.
    - None of the three scanners is installed (*ran*, research).
    - gitleaks is "feature complete", with security patches only (verified).
    - trufflehog's live check calls the services the keys belong to (the researcher's reading).
    - detect-secrets needs pip.
    - Each needs someone to install it in every project.
18. No waiver: my #5, applied to W3.2, which is a MUST with no exception (my reading). My #7 (*quoted*): 「王若蚤圖之，其事又將未可知也。」 Do not plan early: add a waiver only once a real false positive is recorded.

**Words to write (D4).**
- YAML `checks.secret scanner`:

  > "`tools/memory_index.py`, in write mode or with --check, fails an entry under entries/ that holds a credential in one of the fixed-prefix formats it lists (AWS access key IDs, private key blocks, GitHub, GitLab, Slack, Anthropic, OpenAI, Stripe and Google API keys; patterns from gitleaks' default config). A match is never waived: an entry that must mention a key format names it without a whole key. It finds no password, no token without a prefix and no personal data; for those the reviewer is the check."

- W3.2's `check:` stays "secret scanner; reviewer".
- The build run adds the B-record to `docs/index-md/REQUIREMENTS.md`.

**D5: measuring agy**
19. My #3, 「時不至，不可彊生；事不究，不可彊成。」, and my #9 (*quoted*), 「天地未形，而先為之征，其事是以不成」: no `INDEX.md` exists yet (*ran*: no `project-memory/` here, 0 tracked files). A measurement now decides nothing.
20. My #7, 「王若蚤圖之，其事又將未可知也。」: a measurement holds for one installed agy version. Measured years before it matters, it may no longer hold by then.
21. My #4, 「得時無怠」: once the trigger fires, measure at once, before that `INDEX.md` is relied on.
22. My #10 (*quoted*): 「無過天極，究數而止」, stop when the count runs out. Measure only agy, because only agy has a reported figure below the example: 12,000 characters, from a third-party page (*read*: research per the question).
23. How, when the trigger fires (my reading of the brief's sentinel method):
    - Use two test files through agy's real load path for `INDEX.md`. One is ASCII. The other is mostly multi-byte characters (CJK), so bytes and characters come apart.
    - Each file has random marker strings that cannot be guessed, placed just below and just above each figure any source gives for agy (24,000 bytes; 12,000 characters; the 20,000-token budget).
    - A control file sits below the lowest figure. All its markers must be listed, or the test is void.
    - At session start, ask agy to list every marker it sees. The highest marker it lists gives the bracket; a listed marker that is not in the file voids the run.
    - Run each file twice. If the two runs differ, it is not a measurement.
    - Write the result and agy's version to the run folder, and change agy's row to `basis: measured`.

**Words to write (D5).** Nothing in the design: this is an action, not part of the product. Add a line to the run's `state.md` TODO:

> "Measure agy's start-file limit when a project's limits file names agy and that project's `INDEX.md` is larger than the lowest figure any source gives for agy (today 12,000 characters, third-party, `runs/20261017-sot-item11/research/experts.md`); then change agy's row to `basis: measured`."

## What I need to know
1. **Does a documented figure for the same load path end the example, or only a measured one?** This was last round's open question 1.
   - If documented counts, D2 stands as written.
   - If only measured counts, every row holds the example until it is measured. D5's measurement would then be the only way out of the example for agy, and each other engine would need its own measurement.
2. **In the first project that adopts the kit, which agents load `INDEX.md` at session start, and by which path?**
   - If agy is not among them, D5's trigger cannot fire and the answer is "never".
   - If it is, the trigger is live.

## Costs and risks
- **D1, JSON** (#3): no comments, and quote and comma traps in a hand-edited file. A repeated key silently keeps the last value unless the tool rejects it (research, python docs), so the tool must reject it.
  - **File in `project-memory/`** (#14): the kit ships no filled file. Until a project's owner writes one, the example applies. If nobody writes it, the example applies forever; it is printed on every run, but it can be ignored.
- **D2, row by row** (#4, #1):
  - A documented figure may not match the installed engine; Rd3.1a says so itself.
  - The tool cannot see an agent missing from the file; only the reviewer can.
  - "Not checked" lines for tokens can be ignored.
  - For combined budgets, the tool checks only `INDEX.md`. Being under a combined figure such as Codex's 32 KiB alone does not mean the whole start load fits.
- **D3** (#14, #3): until the owner acts, an entry may point to a path that no longer exists. The tool does not check `covers`, so only a reader's check before acting catches it. Every clash adds work for the owner.
- **D4** (#14, #18, #11):
  - It costs code and tests in a later run.
  - It blocks a commit that quotes a whole example key. My reading, not run: AWS's documentation example access key ID matches the AKIA pattern.
  - It finds only the listed formats, and only in the current entries, not in git history.
  - A pass may be read as "no secrets". The `checks` text has to say what it does not find.
  - New key formats need a code change, and the copied patterns come from a project that now gets security patches only.
- **D5** (#7, #9, #4):
  - "Later" can quietly become "never". Nothing but the owner's reading of the printed size watches the trigger.
  - Until agy is measured, if the 12,000-character report is right, agy could cut an `INDEX.md` that passes the tool's check, and nobody would know.
  - A measurement costs agy calls and holds for one agy version.

## How we would know I was right
- **D1/D2: tool tests in the build run.**
  - With no file, the output names the Rd3.1b example and fails one line over `MAX_LINES`.
  - A documented row below the example fails just above its own limit.
  - A repeated key, a missing field or an unknown `basis` each fail.
  - A `tokens` row prints "not checked" and is never counted as passed.
  - `--check <rev>` reads the limits file from that commit.
  - In the first project, each run's printout shows which agents still hold the example.
- **D3:** in a scratch repo, two branches rename one `covers` path to different paths. The merged entry holds both, `state.md` has the report line, and the owner's fix appears as a `changed:` line. A merge that keeps one path silently fails the reviewer.
- **D4:**
  - A test entry with one fake whole key in each listed format fails the check once per format. A clean `entries/` passes.
  - Over the first project's `entries/`, compare false positives against credentials caught. If false positives come first and outnumber the catches, the no-waiver default is wrong.
- **D5:** when the trigger fires:
  - the control file's markers are all listed;
  - the cut falls between two markers in both files;
  - the ASCII and CJK pair shows whether the unit is bytes or characters;
  - repeating the test on a later agy version gives the same cut, or a recorded difference.

  If the trigger never fires, "never" was the right price.
