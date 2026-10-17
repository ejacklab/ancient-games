# Answer — Five decisions to finish the source-of-truth memory design

## Answer
D1: JSON file `project-memory/index-limits.json`, one row per agent and unit. D2: the example stops as soon as a valid file exists. D3: keep both new paths. D4: option (a), a small standard-library check of fixed-prefix token formats in `memory_index.py`, with the reviewer still checking everything else. D5: measure agy now, only if agy can be called in this run, using random sentinels and a control file.

## How I decided
I checked `tools/memory_index.py` and the Rd3.1a, Rd3.1b, W3.2 and W6.3a records. The tool's constants are `project-memory/…` paths and `ENTRY_NAME` matches only `entries/[DFLOH]-*.md`, so a JSON file in `project-memory/` is not mistaken for an entry. This repo has no `project-memory/` folder yet. I did not re-check the research's external claims.

1. **D1: JSON in the project's own folder.**
   - **Path:** The file records which agents load this project's `INDEX.md`, and Rd3.1a gives that choice to the project owner. So it sits beside `INDEX.md`, not in the design's folder, which should not hold per-project data.
   - **Format:** JSON needs no new dependency and has no Python-version floor. The four YAML votes did not say how a standard-library-only tool would parse YAML. PyYAML happens to be installed here, but it is not standard library. TOML is my second choice. It has comments, but `tomllib` needs Python 3.11 or later, and I don't know the tool's floor. JSON has no comments, so a `source` field carries the note.
   - **Words to write (Rd3.1a):**
     - "The limits file is `project-memory/index-limits.json`: a JSON list of rows, one per agent and unit. A row has `agent`, `unit` (`lines`, `bytes`, `characters`, `utf16_code_units` or `tokens`), `limit` (a whole number), `basis` (`measured`, `documented` or `example`) and `source` (the URL, file or run folder the figure comes from). `INDEX.md` must fit every row, because limits in different units cannot be ranked."
     - Example row: `{"agent": "agy", "unit": "bytes", "limit": 24000, "basis": "documented", "source": "docs/memory-system/CACHES.md"}`.
   - **Why one row per agent and unit:** The facts show agents with two limits. Claude Code has 200 lines and 25 KB. agy has 24,000 bytes plus a 20,000-token budget. One row per agent would force a choice between them.
   - **How the tool reads it:**
     - The tool reads the file from the same git object as `INDEX.md`, since check mode reads only git objects.
     - It rejects repeated keys with an `object_pairs_hook`.
     - It can count lines, bytes, characters and UTF-16 code units. It cannot count tokens without a tokenizer. A `tokens` row is therefore printed as "not checked", never skipped silently.

2. **D2: the example stops when a valid file exists, as a whole, not row by row.**
   - **Why not row by row:** The example is two constants (lines and bytes), not per-agent values, so there is no clean way to say which row replaces which constant.
   - **Why not "every agent has a row":** The file is the list of agents, and the project owner decides that list (`who_decides` in Rd3.1a). The tool cannot find an agent that is absent from the file, so this rule could not be checked.
   - **Words to write (Rd3.1b):**
     - "If `index-limits.json` does not exist, the tool uses 200 lines and 24,000 bytes and prints that it did. If it exists, only its rows apply. The owner may copy the example's two numbers in as rows with basis `example`."
     - "A file that does not parse, repeats a key, has no rows, has a unit the tool does not know, or has a limit that is not a whole number fails the check. It never falls back to the example."
   - **Reporting:** Every run prints each row it used and its basis, so a "documented" figure is not read as measured.

3. **D3: keep both new paths.**
   - **Why:** Dropping a needed `covers` path costs a missed read, which is the failure in Rd4.1. Keeping an extra one costs a spurious read. The cost of keeping is smaller.
   - **How it fits the existing rule:** W6.3a already says "keeps both sides … every `covers` path either side wrote". The gap is only the case where both sides touched the old path, which the rule leaves unstated.
   - **Words to write (W6.3a):** "A `covers` path both sides changed, by removing it or replacing it with different paths, is removed. Every new path either side wrote is kept, with both `changed:` lines. Nobody chooses between the new paths."
   - **Fails_if addition:** add "or drops a path one side wrote".
   - **Reporting:** No separate `state.md` report. Both `changed:` lines already show the divergence, and a kept path that no longer exists is an ordinary stale-path finding.

4. **D4: option (a), with the reviewer kept.**
   - **Why not (b):** None of gitleaks, trufflehog or detect-secrets is installed. The hooks are not cloned, so each clone would need its own install.
     - gitleaks is "feature complete" and moving to security patches only.
     - trufflehog's live verification makes network calls.
     - detect-secrets is a pip package and the tool is standard library only.
   - **Why not (c):** A fixed-prefix check has near-zero false positives, and the tool already scans entry files for conflict markers (B2.7), so the check fits next to that.
   - **What it detects (patterns from gitleaks' default config, taken from the research):**
     - AWS access key IDs with the prefixes `A3T…`, `AKIA`, `ASIA`, `ABIA` and `ACCA`, plus 16 characters.
     - A PEM private-key block with a body of 64 or more characters.
     - GitHub `ghp_`, `gho_`, `ghu_`, `ghs_` and `ghr_` plus 36 characters, and `github_pat_` plus 82.
     - GitLab `glpat-`, Slack `xox…`, Anthropic `sk-ant-api03-…`, OpenAI `sk-(proj|svcacct|admin)-…T3BlbkFJ…`, Stripe `(sk|rk)_(test|live|prod)_…`, and Google `AIza` plus 35.
   - **What it leaves out:** entropy rules (commit hashes and UUIDs would trip them), generic `password=` rules, and JWTs (often not secret).
   - **Waiver:** a `secret-scan:allow` comment on the line. All three outside tools have a line waiver, so a quoted example needs one here too.
   - **Failure output:** the file, line and pattern name, never the matched text.
   - **Words to write (W3.2):**
     - "`check: tool (known token formats); reviewer (everything else)`."
     - Replace the `checks` key text with: "The tool finds credentials in known token formats in `entries/`. Passwords, tokens with no fixed prefix, and sensitive data are the reviewer's check."

5. **D5: measure agy now, if it can be called in this run.**
   - **Why agy, and why now:** agy is the only agent whose documented figures conflict (24,000 bytes against 12,000 characters from a third-party page). If 12,000 is right, a 24,000-byte `INDEX.md` passes the check and is silently cut. Rd3.1a says "a documented figure is not a measurement of the installed engine". Claude Code, Qwen and dsh are not stricter than the example, so I would not measure them now.
   - **How:**
     - Make a rule file of ASCII text with a random hex token every 500 bytes, up to about 30,000 bytes. Counters like S001, S002 are guessable, so the tokens must be random.
     - Make a control file of about 2,000 bytes, with its own token, under any limit.
     - Start a fresh agy session in an empty folder and ask it to list every token it sees, in order.
     - The last token seen gives the cut. With ASCII text, 12,000 characters and 24,000 bytes land at different offsets.
     - Repeat the run at least three times.
     - Repeat once with 3-byte characters, to tell bytes from characters.
   - **Where it goes:** Write the evidence under `runs/<run-id>/` and add a row with basis `measured` whose `source` is that folder. If agy cannot be called, measure later, and the row stays `documented` or `example` until then.

## What I need to know
1. What is the lowest Python version the tool and hook must run on? If 3.11 or later is guaranteed, D1 could be TOML with comments.
2. Is `journal/` in scope for W3.2? Raw session notes are likelier to hold pasted secrets than entries. The `checks` key only mentions `entries/`. I scoped D4 to `entries/`.
3. Is agy installed and callable here? Which file does it load at session start, so the sentinel file goes in the right place?
4. Does any existing check fail a `covers` path that no longer exists? D3 relies on that.
5. Which agents does the owner say load `INDEX.md`? I did not list them.

## Costs and risks
- **D1/D2:**
  - JSON has no comments or trailing commas, so a hand-edit slip is a parse failure. It reports line and column, and it fails loudly.
  - A partial file drops the example's 24,000-byte limit without warning. Only the printed rows show it.
  - A `tokens` row is never checked. agy's token budget stays unchecked, though ASCII text reaches the byte limit first.
- **D3:** Extra paths mean extra reads and can pile up as stale paths.
- **D4:**
  - It catches only known formats. Passwords, prefix-less tokens and personal data still depend on the reviewer, so it can give false comfort.
  - A waiver comment silences the check, so the reviewer must read waivers in the diff.
  - A quoted AWS documentation example (for instance the usual `AKIA…EXAMPLE` ID) would match and need the waiver.
  - The regexes come from a project that is winding down, so they can go stale.
  - Entry files still pass the check, so existing git history is not scanned.
  - It adds a job to `memory_index.py` beyond building the index.
  - Failure logs could leak a key if the match text were printed. The design prints only the file, line and pattern name.
  - I did not run the patterns on the real `entries/`, so there is no false-positive count.
- **D5:**
  - The agent's own report is the measuring instrument, and it can misreport.
  - The result is one engine version, and an update can change it.
  - It costs a few agy calls.
  - By house rules it should not change the design on n=1 alone. It sets one row's basis to `measured` with its version.

## How we would know I was right
- **D1/D2 tests:**
  - A missing file uses the example and prints a notice.
  - With a valid file holding a bytes row, an `INDEX.md` one byte over fails and one byte under passes.
  - A file with a repeated key, a bad unit or no rows fails, and does not fall back.
  - A `tokens` row prints "not checked".
  - `--check <rev>` reads that revision's limits file, not the working tree's.
- **D3:** A merge fixture where both sides replace path A with B and C leaves B and C, drops A, and keeps both `changed:` lines.
- **D4 tests:**
  - A fixture with one fake key per pattern fails. The fakes are built by string concatenation at test time, so the test file does not trip the scanners.
  - An entry that quotes only a PEM header passes.
  - A waived line passes.
  - The failure output never contains the fake key.
  - Running the check over the real `entries/` gives a false-positive count, and I would expect it to be 0.
- **D5:**
  - The control token appears in every run.
  - The cut is at the same offset in three or more runs.
  - The ASCII and multi-byte runs show whether the unit is bytes or characters.
  - The new row has basis `measured` and points to the run folder.
  - If the measured limit is below 24,000, the check fails on an `INDEX.md` that used to pass. That would show the measurement mattered.
