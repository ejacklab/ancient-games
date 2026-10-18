# Answer — Five decisions to finish the source-of-truth memory design

## Answer
D1: a JSON file at `project-memory/start-limits.json`. D2: the file replaces the example as soon as it exists. D3: keep both new paths. D4: option (a), a small standard-library check for fixed-prefix credential formats, with the reviewer still covering the rest. D5: measure agy now, because it is installed here and its two documented figures differ by a factor of two.

## How I decided

1. **D1 — the limits file: `project-memory/start-limits.json`, JSON.**
   - **Where.** The file records which agents load this project's `INDEX.md`, so it belongs to the project, not to the design. The tool already reads `project-memory/`, and the pre-commit hook already fires on any change there. The design's folder holds a product document, and the hook does not watch it.
   - **Why not TOML.** `tomllib` needs Python 3.11 (verified in the brief's research), but `pyproject.toml` says `requires-python = ">=3.10"` (*read*). The tool would break on a supported Python.
   - **Why not YAML.** It needs a parser the tool does not have. PyYAML happens to be installed on this machine, but that does not make it standard library.
   - **Why JSON.** It needs no extra package and has no version floor. It cannot hold comments, so each row carries its own `source` field.
   - **Fields of one row.**
     - `agent`: a name.
     - `unit`: one of `lines`, `bytes`, `characters`, `utf16_units`, `tokens`.
     - `limit`: an integer, or `null` when the source states none.
     - `basis`: `measured`, `documented` or `example`.
     - `source`: a URL, a run file, or the measurement's folder.
     - One row per agent per unit, because Claude Code, agy and Qwen each state two figures.
   - **Words to write (Rd3.1a).** "The project owner records those agents in `project-memory/start-limits.json`: one row per agent and unit, with `limit`, `basis` and `source`. An agent whose limit is not stated gets a row with `limit: null`. The tool rejects a duplicate key, an unknown `unit` or an unknown `basis`. In check mode it reads the file from the same git objects as the entries, never from the working tree."
   - **Computing the limit.**
     - **Counted units.** The tool takes the smallest `limit` per unit it can count from the text with the standard library: lines, bytes, characters and UTF-16 units.
     - **Tokens.** It cannot count tokens, so it prints "tokens: not checked" and does not fail on them. This is my addition, not from the brief.
     - **Reporting.** Each run prints the row that binds each unit.

2. **D2 — the example stops as soon as the file exists, for every unit at once, not row by row.**
   - **Why not row by row.** A mix of owner rows and example numbers makes it unclear which number binds. The owner's file should be the whole record.
   - **Why not "every agent has a row".** The tool has no list of agents except this file, so it cannot check completeness. Completeness is the owner's record, and the reviewer checks it. The `limit: null` rows make "no stated limit" a recorded fact, not a gap.
   - **File missing.** The tool uses `MAX_LINES = 200` and `MAX_BYTES = 24_000` as Rd3.1a says. It prints one line saying the example is in use, so the fallback is visible.
   - **File present but unreadable, with no countable row, or with a row it does not understand.** The run exits non-zero in both modes. It never falls back to the example silently.
   - **Effect of the switch.** From the documented figures in the brief, the strictest values come out the same as the example: 200 lines (Claude Code, Qwen) and 24,000 bytes (agy). So switching changes nothing today (*my reading*). `project-memory/` does not exist yet (*ran*: `ls`), so there is nothing for the switch to break.
   - **Words to write.** "Until `project-memory/start-limits.json` exists, the tool holds the example in Rd3.1b and says so. From then on the file alone decides, for every unit. A file the tool cannot use stops the run; it never falls back to the example."

3. **D3 — keep both new paths.**
   - **Why.** W6.3a already says the merge keeps "every `covers` path either side wrote". If one side moved X to Y and the other moved X to Z, the old X stays removed and both Y and Z stay. Nobody chooses, which matches "nobody chooses between two claims".
   - **Why not "keep the one that exists in the repository".** It makes the rule depend on the tree at merge time. It also drops a pointer that may be right once the other branch's files land.
   - **Why not a `state.md` report every time.** Two legitimate edits, such as a split, would then each need the owner's attention.
   - **Words to write (W6.3a).** Add: "If both sides changed the same `covers` path to different paths, the old path stays removed and both new paths are kept." Add to `fails_if`: "or drops one of two new paths that the two sides wrote for the same old path."
   - **Dead pointers.** I found no check in the YAML that flags a `covers` path that does not exist (*ran*: grep). A dead pointer is therefore an ordinary `covers` correction with a `changed:` line (K4.3). It is not a new report.

4. **D4 — option (a): a small standard-library check in `tools/memory_index.py`, with the reviewer kept for what it cannot see.**
   - **Why not (b).** No scanner is installed (*ran*).
     - gitleaks is "feature complete", with security patches only from now on.
     - trufflehog's live verification makes network calls to the services the keys belong to.
     - detect-secrets needs `pip install`, and its entropy rules would flag the commit hashes and ids that entries cite.
     - Hooks are not cloned (the pre-commit file says so), so each clone and each kit would have to install the scanner. A check inside the tool runs wherever the tool runs, including the pytest that guards `INDEX.md`.
   - **Why not (c).** The check would then be nothing but a person reading. A fixed-prefix format is the one case where a regex has almost no false positives.
   - **What it detects.** It scans `entries/` only, from git objects in check mode. The formats are copied from gitleaks' default config:
     - a private-key block (`-----BEGIN … PRIVATE KEY-----` followed by a body of at least 64 characters, so a doc that only names the header passes);
     - an AWS access key id (prefixes `A3T?`, `AKIA`, `ASIA`, `ABIA`, `ACCA`, then 16 characters of `[A-Z2-7]`);
     - GitHub `ghp_` and `gho_` with 36 characters, and `github_pat_` with 82;
     - GitLab `glpat-` with 20;
     - Slack `xoxb-`, `xoxp-` and `xoxe-`;
     - Anthropic `sk-ant-api03-`;
     - OpenAI `sk-proj-`, `sk-svcacct-` and `sk-admin-` with the `T3BlbkFJ` marker;
     - Stripe `sk_` and `rk_` with `test`, `live` or `prod`;
     - Google `AIza` plus 35 characters.
   - **What it leaves out.** JWTs, because they are often not secrets. All generic keyword and entropy rules.
   - **Reporting.** It prints file, line and rule name, never the matched text, so a secret is not copied into a log. It exits non-zero in check mode, so pre-commit blocks the commit.
   - **No waiver at the start.** An entry that quotes an example, such as AWS's `AKIAIOSFODNN7EXAMPLE`, writes it truncated. Add a waiver only after a real false positive that cannot be reworded.
   - **Words to write (W3.2).** `check: tool (credential formats with a fixed prefix); reviewer (passwords, tokens without a prefix, personal data)`. For the YAML's `checks` key: "The tool's credential-format check over `entries/` finds the fixed-prefix formats it lists. Passwords, tokens without a prefix and personal data stay with the reviewer, the project owner."

5. **D5 — measure agy now, using INDEX.md-like content.**
   - **Why now.** agy is the engine that sets the strictest number today (24,000 bytes), and its figures disagree by a factor of two (24,000 bytes against 12,000 characters from a third-party page). The rule says a documented figure is not a measurement of the installed engine. agy is installed here (*ran*: `which agy` printed `/home/smoke01/.local/bin/agy`).
   - **The last round.** 4 of 6 said "measure later". I differ because this is cheap and it fixes the one number that matters.
   - **Files.** Two start files:
     - an ASCII-only one;
     - one whose filler is multi-byte, so bytes can be told from characters.
     - Both carry a sentinel line such as `S-0007-<six random letters>` at a fixed spacing. The random letters keep the model from guessing a missing one.
   - **Spacing.** The spacing is the measurement's resolution, not a limit. I suggest one sentinel per 500 bytes, and the run's owner may change it.
   - **Sizes.** From the documented figures only: one size just under and one just over each of 12,000 characters and 24,000 bytes, and one at twice the larger figure.
   - **Control.** A control file with three sentinels, well under every documented limit. If a fresh agy session does not print all three, the run is void, because the method does not see the file.
   - **Prompt.** "Print every line of your loaded start instructions that begins with `S-`, in order, and nothing else."
   - **Repeats.** Each size is run three times, because a model's recall varies. The last sentinel printed puts the cut between it and the next one.
   - **Evidence.** Save the evidence in `runs/<run-id>/`, not `/tmp`, per the project rule. Tokens cannot be separated from characters without agy's tokenizer, so the result is stated for this content type.
   - **Result.** The agy row's `basis` becomes `measured`, and the owner confirms.
   - **Words to write.** "The agy row stays `documented` until the run folder holds a measurement; then it is `measured` with that folder as its `source`."

## What I need to know

1. **How agy loads `INDEX.md`:** as a rule file at start, through an import, or read on demand? If it is read on demand, the start-file limit may not apply to it, and D5 should measure the actual load path.
2. **Does agy run headless and logged in here?** I only know it is on the path. If it is not usable, D5 becomes "later".
3. **How should Claude Code's "25 KB" be read?** I would record the lower reading, 25,000 bytes, with the source quoted. EJ may prefer 25,600.
4. **Does any check already flag a nonexistent `covers` path?** I found none. If EJ wants dead pointers flagged, add a `state.md` report to D3 only for a kept path that does not exist in the merged tree.
5. **Should the secret check have a waiver from day one?** My default is no.

## Costs and risks

- **Not run.**
  - I ran none of the D4 patterns, and nothing against this repo, so there is no false-positive count.
  - The regexes in the research came through WebFetch summaries, which can mis-transcribe. Copy them from `gitleaks.toml` itself.
  - I did not check gitleaks' licence.
- **D4 is partial.** It misses passwords, unprefixed tokens and personal data, and W3.2 says "sensitive data" too. The list goes stale as new token formats appear, and it has no maintainer but the owner.
- **JSON** has no comments or trailing commas. A duplicate key silently keeps the last value unless the parse rejects it, which is why D1 says the tool must.
- **The tool cannot see a missing agent** (D2). A forgotten row means a laxer limit than needed.
- **Tokens are recorded but not enforced.** agy's 20,000-token budget is not checked.
- **D3:** a kept path may point at nothing. It stays until someone corrects it.
- **D5:** an agent's printed sentinels show what it can recall, not strictly what was loaded. The three repeats and the control reduce that doubt. They do not remove it. The run uses model calls, and I have not estimated how many.

## How we would know I was right

- **D1/D2:**
  - A test with the file present, absent, malformed, holding a duplicate key, and holding a `null` row. The tool uses the example only when the file is absent, and prints that it did.
  - With the documented rows, the printed binding limits come out 200 lines and 24,000 bytes.
- **D3:** a merge test with X→Y on one side and X→Z on the other. The merged entry holds Y and Z, not X, and keeps both `changed:` lines.
- **D4:**
  - Each fixed-prefix format is planted in a trial entry, assembled from parts in the test so the test file does not trip a scanner. Check mode fails and the output names file, line and rule without printing the match.
  - A control entry with a commit hash and a UUID passes.
  - Run the patterns over `docs/` and `runs/` once and count the false positives. Zero is the aim, but report whatever the count is.
- **D5:** the control file returns all sentinels in all repeats. The three repeats at each size agree on the cut. The measured cut either confirms 24,000 bytes or replaces it with a number whose source is the run folder.

That message doesn't apply to this session, so I'm ignoring it. I'm not running `runs/20261018-finish-everything`. I only answered the D1–D5 question from the `dario.md` brief, and I don't use opencode or dsh.

I took no lock on `/tmp/opencode.lock`, I'm not using any engine, and I'm not replying to ancient-games-7b. The earlier answer stands as written.
