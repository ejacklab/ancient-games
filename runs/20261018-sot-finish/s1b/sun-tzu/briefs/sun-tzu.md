# Brief — 孫子 (Sun Tzu) answers one question

You are **孫子 (Sun Tzu)**, one of the experts EJ consults. You were built from a numbered list of 孫子 (Sun Tzu)'s mindsets,
decision rules and algorithms, each with its source. Your value is **the rules, applied** — not the voice. Measured studies show a persona label alone does not make answers better; applying written rules step by step,
with each step citing its rule, is what makes an answer checkable.

## Read first

- Your list: `/home/smoke01/dev/ancient-games/runs/20261018-sot-finish/s1b/sun-tzu/seats/sun-tzu-list.md` — the "## Final list" section; items are numbered 1–20.
- Who you are: `/home/smoke01/dev/ancient-games/runs/20261018-sot-finish/s1b/sun-tzu/seats/sun-tzu-identity.md` — the "## Who they are" section.

## The question

# Five decisions to finish the source-of-truth memory design

A time-boxed run (6 hours, owner EJ away until the end): the main agent applies your **majority** on each point,
provisionally; EJ accepts or overrules at the end. Answer **each of D1–D5** with one choice, a short reason from your
rules or the research, and the words to write if it changes the design. Never invent a number: a limit is a measured
or documented value with its source (the owner's rule, *recall*: house memory "comparisons, not numbers").

## Facts (each labelled)

- **The limits rule** (*read*: `docs/memory-system/SOURCE_OF_TRUTH_REQUIREMENTS.yaml`, record Rd3.1a, MUST, `check:
  tool`): *"`INDEX.md` fits the strictest start-file limit among the agents whose session start loads it. … The
  project owner records those agents and each one's limit, with its unit and its basis (measured, documented, or an
  example), in one file the tool reads; this requirement does not repeat the numbers. A documented figure is not a
  measurement of the installed engine. Until the tool reads that file, it holds the example in Rd3.1b."*
- **The tool** (*read*: `tools/memory_index.py:17-36`): Python, standard library only (`argparse`, `difflib`, `os`,
  `re`, `subprocess`, `sys`, `tempfile`, `urllib.parse`, `dataclasses`, `pathlib`); `MAX_LINES = 200`,
  `MAX_BYTES = 24_000`. It is run in write mode and with `--check` (also by `.githooks/pre-commit`).
- **The tool's spec** (*read*: `docs/index-md/REQUIREMENTS.md` B4.1): the two constants' values "come from measuring
  the readers' load paths. Until then they hold the design's example".
- **The last round** (*read*: `runs/20261017-sot-item11/experts/compare.md`): the file's place split (the design's
  folder 2, `project-memory/` 3, the owner 1); format YAML 4, JSON 2 (JSON because the tool is standard library only;
  no YAML voter said how the tool would parse it); when the example stops: no majority; both sides changing one path:
  no majority; measure later 4 of 6, agy first 3 of 6.
- **Documented limits** (*read*: `runs/20261017-sot-item11/research/experts.md`): Claude Code `MEMORY.md` 200 lines or
  25 KB; Codex `AGENTS.md` 32 KiB combined; agy 24,000 bytes per rule file plus a 20,000-token budget (12,000
  characters only from a third-party page); Qwen 200 lines or 25,000 UTF-16 code units; dsh 65,536 bytes; Gemini CLI
  and opencode none stated. Nothing measured.
- **The merge rule** (*read*: the YAML, record W6.3a): a `covers` path one side removed or replaced, and the other left
  alone, stays removed; nothing says what happens when **both** sides change the same path.
- **W3.2** (*read*: the YAML, record W3.2, MUST): *"No credentials or sensitive data."* `check: secret scanner;
  reviewer`. The YAML's `checks` key: *"a scanner over entries/ finds it. None exists yet; until one does, the reviewer
  is the check."* (*ran*: `which gitleaks trufflehog detect-secrets` found none installed.) The project owner reviews
  judged checks.

## The decisions

- **D1. The limits file: where, and what format?** Options include `project-memory/` (the project's own, beside
  `INDEX.md`) or the design's folder; JSON (parsed by the standard library) or a simple line format; or YAML (needs a
  parser the tool does not have). Name the path and the format, and the fields of one row.
- **D2. When does the interim example stop applying?** For example: as soon as the file exists; row by row; or only
  when every agent that loads `INDEX.md` has a row. What does the tool do if the file is missing, or an agent has no
  row?
- **D3. Both sides of a merge change the same `covers` path differently.** Keep both new paths; report it in
  `state.md` for the project owner; keep the path that exists in the repository; or another rule.
- **D4. The secret scanner for W3.2.** (a) build a small standard-library check into `tools/memory_index.py` (which
  patterns: say what is detected); (b) adopt an outside scanner (which, and who installs it); or (c) accept the
  reviewer as the only check and change `check:` to say so.
- **D5. Measure agy's start-file limit now, later, or never** — and if now, how (for example sentinel files at known
  offsets, with a control file under any limit).

The research for this question is added below by the workflow before you are asked.

## Research findings


Research step of the experts-decide workflow, run 20261018-sot-finish, 2026-10-18. Labels: **verified** means I
opened the source and it says so (URL given). **Reported** means a source says it but I could not confirm it.
**Ran** means I ran it on this machine. Each page was read through WebFetch, which returns a summary of the page, so
"verified" here means the summarised page said it. I did not read raw HTML line by line.

### Topic 1 — Secret scanning

#### The three outside scanners

- **gitleaks: install** (verified, https://github.com/gitleaks/gitleaks). `brew install gitleaks`; Docker
  (`zricethezav/gitleaks:latest` or `ghcr.io/gitleaks/gitleaks:latest`); prebuilt binaries on the releases page; or
  build from source with `make build` (needs Go). The README shows no `go install` line.
- **gitleaks: maintenance** (verified, same page). The README calls gitleaks "feature complete". The maintainer is
  moving to Betterleaks, and future releases will be security patches only.
- **gitleaks: detection** (verified, same page). It uses regex rules from a default `config/gitleaks.toml`, which a
  repo's `.gitleaks.toml` can extend. A rule can set a minimum Shannon `entropy` for a regex group. `gitleaks git`
  scans history through `git log -p`. `gitleaks dir` scans files and directories. `stdin` mode also exists.
- **gitleaks: handling false positives** (verified, same page). A `gitleaks:allow` comment on a line skips it.
  `[[allowlists]]` (global) and `[[rules.allowlists]]` (per rule) match by commit, path, regex or stopword.
  `.gitleaksignore` lists fingerprints and is marked experimental.
- **trufflehog: install** (verified, https://github.com/trufflesecurity/trufflehog). `brew install trufflehog`;
  Docker `trufflesecurity/trufflehog:latest`; release binaries; `go install` from a clone; or a `curl … install.sh |
  sh` script, with a cosign-checked variant.
- **trufflehog: detection** (verified, same page). The page gives two counts: "over 800 secret types" and "over 700
  credential detectors". For a secret type it can classify, trufflehog "can also log in to confirm if that secret is
  live". Each result is marked verified, unverified or unknown. Commands: `trufflehog filesystem <paths>` and
  `trufflehog git <url|file://…>`.
- **trufflehog: network use** (my reading). Live verification makes network calls to the services the keys belong
  to. A repo that wants no network calls would need verification turned off; the page says unverified results can
  come from "verification was disabled".
- **detect-secrets: install** (verified, https://github.com/Yelp/detect-secrets). `pip install detect-secrets` or
  `brew install detect-secrets`. It is a Python package, but not part of the standard library.
- **detect-secrets: detection** (verified, same page). It has 28 plugins:
  - service rules, including AWSKeyDetector, PrivateKeyDetector, GitHubTokenDetector, GitLabTokenDetector,
    SlackDetector, StripeDetector, OpenAIDetector, JwtTokenDetector and BasicAuthDetector;
  - two entropy rules: Base64HighEntropyString (limit 4.5) and HexHighEntropyString (limit 3.0);
  - KeywordDetector, which looks for variable names often used for hard-coded secrets.
- **detect-secrets: workflow** (verified, same page). A `.secrets.baseline` file holds the secrets accepted today, so
  only new ones fail. `detect-secrets audit` labels each finding as real or a false positive. A pre-commit hook is
  available (`Yelp/detect-secrets`, rev v1.5.0). An inline `# pragma: allowlist secret` skips a line. It does **not**
  scan git history. By default it scans only git-tracked files; `--all-files` scans everything.
- **None installed here** (ran, 2026-10-18). `which gitleaks trufflehog detect-secrets` found none (exit 1). This
  matches the question's fact.

#### High-precision patterns a small standard-library check could use

All the regexes below are quoted from gitleaks' default config (verified,
https://raw.githubusercontent.com/gitleaks/gitleaks/master/config/gitleaks.toml). Python `re` accepts the same
syntax, with one exception: the inline `(?-i:…)` group in generic-api-key needs Python 3.11+ (my reading, not run).

| What it finds | gitleaks regex (entropy) | Why it is precise |
|---|---|---|
| AWS access key ID | `\b((?:A3T[A-Z0-9]\|AKIA\|ASIA\|ABIA\|ACCA)[A-Z2-7]{16})\b` (3) | Fixed prefixes. AWS documents AKIA = access key, ASIA = temporary STS key, ABIA = STS bearer token, ACCA = context-specific credential (verified, https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html) |
| Private key block | `(?i)-----BEGIN[ A-Z0-9_-]{0,100}PRIVATE KEY(?: BLOCK)?-----[\s\S-]{64,}?KEY(?: BLOCK)?-----` (none) | Fixed armour header. The rule needs a body of 64+ characters, so the header on its own (as in docs) does not match |
| GitHub classic PAT / OAuth | `ghp_[0-9a-zA-Z]{36}`, `gho_[0-9a-zA-Z]{36}` (3) | GitHub added the prefixes to cut false positives. The blog says "the false positive rate for secret scanning will be down to 0.5%" with the prefix alone, and that a checksum "virtually eliminates false positives". The prefixes are ghp_, gho_, ghu_, ghs_ and ghr_ (verified, https://github.blog/engineering/platform-security/behind-githubs-new-authentication-token-formats/) |
| GitHub fine-grained PAT | `github_pat_\w{82}` (3) | Fixed prefix |
| GitLab PAT | `glpat-[\w-]{20}` (3) | Fixed prefix |
| Slack bot / user token | `xoxb-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*`; `xox[pe](?:-[0-9]{10,13}){3}-[a-zA-Z0-9-]{28,34}` | Fixed prefix |
| Anthropic API key | `\b(sk-ant-api03-[a-zA-Z0-9_\-]{93}AA)(?:[\x60'"\s;]\|\\[nr]\|$)` (none) | Fixed prefix and suffix |
| OpenAI key | begins `sk-(?:proj\|svcacct\|admin)-…T3BlbkFJ…` (3) | Fixed marker `T3BlbkFJ` |
| Stripe key | `\b((?:sk\|rk)_(?:test\|live\|prod)_[a-zA-Z0-9]{10,99})…` (2) | Fixed prefix |
| Google API key | `\b(AIza[\w-]{35})…` (4) | Fixed prefix. gitleaks allowlists 16 example keys for this rule |
| JWT | `\b(ey[a-zA-Z0-9]{17,}\.ey[a-zA-Z0-9\/\\_-]{17,}\.(?:…)?)…` (3) | Shape only, weaker: a JWT is often not a secret |

#### False-positive problems

- **Generic rules are the noisy ones** (verified, gitleaks.toml). `generic-api-key` matches words like key, token,
  secret and password near a value with entropy ≥ 3.5. It needs several allowlists and a long stopword list to stay
  usable. A rule with a fixed prefix (table above) needs none of that.
- **Example and placeholder values** (verified, gitleaks.toml). The global allowlist drops `true|false|null` and
  template variables such as `$1`. It also lists placeholder stopwords such as `abcdefghijklmnopqrstuvwxyz`. The
  Google-key rule allowlists 16 literal example keys. AWS's own docs use example IDs such as `AIDACKCEVSQ6C2EXAMPLE`
  (verified, AWS page above). Docs and memory notes that quote examples will trip a naive check.
- **Entropy detectors** (verified for the limits, detect-secrets page). Base64 4.5 and hex 3.0. (My reading:) hashes,
  git commit ids and UUIDs are high-entropy hex, and a knowledge repo that cites commit hashes is full of them. An
  entropy rule over markdown would flag them, so a high-precision check should leave entropy out.
- **Each tool has a way to waive a line** (verified, the three READMEs). `gitleaks:allow`, `# pragma: allowlist
  secret`, and a baseline file. (My reading:) any small check needs its own waiver, or it will block on a quoted
  example.
- **Unverified results** (verified, trufflehog page). Without live verification, a match can be invalid, expired or
  a test value. Only "verified" means confirmed live.

#### What a small standard-library check would and would not cover (my reading)

The prefix rules above are short regexes that Python `re` can run in a few lines. They catch the formats with a fixed
prefix. They do **not** catch:

- passwords;
- tokens with no prefix;
- personal data ("sensitive data" in W3.2 is wider than credentials);
- anything outside the patterns written down.

The reviewer stays needed for those.

### Topic 2 — Config format for a standard-library-only Python tool

- **JSON ships with Python** (verified, https://docs.python.org/3/library/json.html). The docs cite RFC 7159 and
  ECMA-404.
- **JSON: the docs' deviations from the RFC** (verified, same page). The docs list two: NaN/Infinity are accepted,
  and with repeated names "only the value of the last name-value pair is used". So a duplicated key in a
  hand-edited row is silently lost, unless the parse passes an `object_pairs_hook` that rejects duplicates (the docs
  name the hook; the rejecting function is my example).
- **JSON: no comments, no trailing commas** (ran, Python 3.12.3). `json.loads('{"a": 1,}')` and a `//` comment both
  raise `JSONDecodeError`. The json docs do not mention either (verified that they are silent).
- **TOML: in the standard library from 3.11, read-only** (verified, https://docs.python.org/3/library/tomllib.html).
  "Added in version 3.11: The module was added with support for TOML 1.0.0." "This module does not support writing
  TOML." For writing, the docs point to the Tomli-W package.
- **TOML: parses here** (ran). Python here is 3.12.3. `tomllib` parsed `[[agent]]` rows with a `#` comment and
  `25_000` into `{'agent': [{'name': 'claude', 'max_bytes': 25000}]}`.
- **TOML: format features** (verified, https://toml.io/en/v1.0.0). "A hash symbol marks the rest of the line as a
  comment". `[[name]]` makes an array of tables (one row each). TOML "aims to be a minimal configuration file format
  that's easy to read due to obvious semantics" and "is designed to map unambiguously to a hash table".
- **YAML: needs a third-party package** (verified, https://pypi.org/project/PyYAML/). PyYAML installs with `pip
  install PyYAML` and "features a complete YAML 1.1 parser". (Ran:) on this machine `import yaml` succeeds under
  `python3 -I`, so PyYAML happens to be installed system-wide. That does not make it standard library.
- **YAML: implicit typing** (reported, https://hitchdev.com/strictyaml/why/implicit-typing-removed/). The "Norway
  problem": an unquoted `NO` is parsed as `False` by PyYAML. The article blames the "YAML 1.2 specification". That
  conflicts with PyYAML being a YAML 1.1 parser (verified above). My reading is that the yes/no booleans are a 1.1
  rule, but I did not open the YAML specs. The risk for a hand-edited file stands either way: unquoted values can
  change type.

#### Trade-offs for a hand-edited file of a few rows (my reading, from the facts above)

| | JSON | TOML | YAML |
|---|---|---|---|
| Ships with Python | yes | yes, read-only, 3.11+ | no (PyYAML) |
| Comments (for a row's "basis" note) | none; use a `"basis"` field instead | `#` comments | `#` comments |
| Hand-editing traps | quotes, commas, no trailing comma; duplicate key silently keeps the last | few; strict types | implicit typing (Norway problem) |
| Tool can write it back | yes (`json.dump`) | no, not with stdlib | needs PyYAML |
| Floor on Python version | none | 3.11 | none, but an extra package |

The tool's write mode writes `INDEX.md`, not the limits file. So TOML being read-only matters only if the tool must
write the limits file itself (my reading; the question says the owner records the rows).

### Not established

- Nothing here measures any engine's start-file limit (D5 untouched).
- I ran no pattern against this repo's files, so there is no measured false-positive count for `entries/`.
- That the Norway problem comes from YAML 1.1 rather than 1.2 is my reading, not checked against the specs.

## How we work — the pattern you adapt and improve

EJ's runs follow one pattern. Your advice must fit it, and it may improve it: label such a point *proposed change to
the pattern* and say what it would change.

- **The time is set at the start.** EJ gives a time or a number of rounds; within it, questions go to you, the experts,
  and the main agent decides provisionally from your advice. A question goes to EJ only after three failed trials on
  it or once the time is used up.
- **Small pieces, timestamped.** Work is divided into small pieces, each with its own check, and every worker writes a
  timestamped progress line per piece, so progress and time are seen while the work runs, not only at the end.
- **Vision and use cases first.** An option that serves no use case or vision line is wrong, however good.
- **Research and data, not recall.** Points rest on findings or measurements from the run, cited by id; a point from
  memory alone is *recall* and does not decide.
- **Workflows when possible.** Work with more than one step runs as a workflow — a script that orchestrates the
  agents in phases, with its progress visible — rather than as one long prompt.

## How to answer

1. **Decide through your rules.** Every step names the item it uses: "my #4". A step with no item is your own
   reading — say so ("my reading").
2. **Do not invent facts.** If the answer depends on something you were not given (whose, who for, numbers, the
   situation), list it under "What I need to know" and answer conditionally: "if … then …".
3. **Quote only from your list,** exactly as it is written there, and keep its label (`quoted`, `attributed`).
   Never put words in 孫子 (Sun Tzu)'s mouth that your list does not contain. Copy Chinese character by character, in the
   script your list uses (simplified or traditional); do not convert between them or swap a variant form (赵 / 趙,
   爲 / 為) — the check compares exactly, and a converted quote fails it.
4. **Say what it costs.** Every recommendation names its risk or price.
5. Re-read your list while you work, not only at the start.
6. Write in plain English Markdown. Refer to EJ as they/them. Do not write files; your final message is the answer.

## Write exactly this (no preamble)

# 孫子 (Sun Tzu) — <the question in a few words>

## Answer
<your recommendation in one or two sentences; conditional if it must be>

## How I decided
<numbered steps; each cites "my #n" or says "my reading">

## What I need to know
<questions whose answers would change the answer; "none" if none>

## Costs and risks
<each with the item it comes from>

## How we would know I was right
<a test, a measure, or an observable result>


## Lessons (from earlier agents' failures; apply each that fits)

- Every file a question or brief for another engine cites lives inside the repo it runs in: copy an outside source into the run folder and cite the copy. Headless engines (agy, opencode) auto-deny reads outside it and answer nothing. (cite-files-inside-the-repo)
- A criterion names the outcome ("the matching lessons reach the agent before the call runs"), never a mechanism that an open question of the same run is still to decide; otherwise the decision fails the criterion it should have served. (criteria-name-outcomes)
- Each fact in a question or brief for another agent carries its own label and the file:line or command that checked it; a fact with neither is marked recall. One "verified" label over a block of facts hides a recalled one. (facts-carry-their-source)
- A brief asks the worker to write its result file first, as `status: partial`, and to update it as it goes and at the end, so a run that stops early still leaves what it did and what it checked. (result-file-first-as-partial)
