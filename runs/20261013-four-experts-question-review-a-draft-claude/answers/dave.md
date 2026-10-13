# Dave — review of the draft `researcher.md` subagent

## Answer
The draft is mostly right. Its standard (lines 42–60) already covers both 2026-10-11 lessons: month-only dates and not-found as an answer. Three things are wrong in ways that will show up in the first real run:
- **The tool list exposes planted controls.** Read, Grep and Glob reach the whole repo, and the repo names the planted control.
- **Quotes from WebFetch are not verbatim.** WebFetch returns a small model's answer, not the page.
- **The Write and budget limits are not enforced.** The harness can enforce both, through a hook and `maxTurns`, but the draft relies on instructions only.

Fix those three, then run the draft against the current way (general-purpose with the contract pasted) on one question before anyone relies on it.

## How I decided
1. **What would change my mind** (my #1): any of the three problems failing to reproduce. That means a run where the researcher cannot reach run files, its quotes match the live page, or a write outside its folder is blocked without a hook. I checked what I could in this session (steps 2–4). I ran nothing that writes.
2. **Data already in the repo** (my #5), all of it read directly:
   - `runs/20261011-agent-memory-graph/check-findings.py` hard-codes the control name (`CONTROL = "..."`). It fails any file that has no row for that control: *"no control-query row (the … sabotage did not run)"*.
   - The same name appears in at least 10 files under `runs/20261011-agent-memory-graph-r2/`.
   - The draft gives the researcher Read, Grep and Glob, and line 15 says *"You read anything"*. So the worker can open the very files that name the control. Under the repo's rule, a control named in a file the worker reads is void.
   - Two further points are my reading. The repo is public on GitHub, so that name is burnt for every later run, including web searches. And because of the hard-coded name, check-findings.py as written will fail every researcher run that has no planted control.
3. **WebFetch, quoted from this session's own tool description:** *"Fetches a URL, converts the page to markdown, and answers `prompt` against it using a small fast model."* Line 48 says *"A quote is copied, not paraphrased"*, but the researcher only ever sees the small model's reply, and it has no Bash to fetch the raw page. My reading: the draft cannot guarantee a verbatim quote. Only a check outside the researcher can. That is my #4: never trust a claim checked only by the one who made it.
4. **Current practice** (web, read in this session, labelled *reported*):
   - The Claude Code subagent docs (code.claude.com/docs/en/sub-agents) list frontmatter fields beyond the four in the facts: `disallowedTools`, `maxTurns`, `hooks`, `skills`, `permissionMode`, `memory`, `effort` and others.
   - The page says a subagent `PreToolUse` hook can *"allow some operations of a tool while blocking others"*. Its example script *"exits with code 2 to block"*.
   - So the fact that Write can be limited to a folder *"only by the instructions"* looks wrong. A Write hook should be able to enforce the path. This is my reading of the docs; I have not tested it.
   - Caveat from the same page: project subagent hooks run *"only after you trust the folder"*.
   - Anthropic's multi-agent research post (2025-06-13) says: *"Subagents call tools to store their work in external systems, then pass lightweight references back to the coordinator."* This matches method 3.8 item 9, so the files-plus-digest design is current practice.
   - The same post says: *"Each subagent needs an objective, an output format, guidance on the tools and sources to use, and clear task boundaries."* The draft has the objective, format and boundaries. Source-quality guidance is thin: the post says early agents favoured *"SEO-optimized content farms over authoritative but less highly-ranked sources"*.
   - The post also gives effort sizes: *"Simple fact-finding requires just 1 agent with 3-10 tool calls."*
5. **Line 14 and `validate_result.py`** (my #5). `validate_result.py --kind result` needs the header keys `node, attempt, engine, model, status, started, ended, evidence`. Line 14 sends a "result file" to `runs/<run-id>/nodes/` but never gives its shape, so it will fail that check.
6. **Labels** (my reading). The draft's four labels match `LABELS` in check-findings.py. The code is the arbiter, so keep them, and flag the TASK_TYPES `CONFIRMED/INFERRED/GAP/UNPROVEN` row for cleanup rather than mixing the two sets. But the definitions put two different measures on one label:
   - `reported` says *who* the source is (a secondary source).
   - `unproven` says *whether evidence was shown* ("claimed without evidence").
   - The draft's own example at line 38 (a vendor blog claiming 60%) fits both.
7. **Nature** (my #6, my #7; general knowledge, not looked up this session). In honeybee nest-site choice, a scout's dance only points to the site. Recruits fly there and inspect it themselves before a quorum forms. The digest-plus-path design already does the pointing. What it lacks is that independent re-inspection, which here is the main agent re-reading a quote against the live page. The analogy fits only if the re-check really is independent of the scout's report. So it supports change 2 below and adds nothing more; I drop it after that.
8. **Ranking the changes** (my #8 and my #10). Each change is small and reversible. I ranked them by how likely each is to break the first real run, judged from n=1 runs only.

**Changes, most important first:**

1. **Line 4: drop `Grep, Glob`. Line 15: replace "You read anything" with:**
   "You read your brief, `docs/workflow-templates/research-file.md`, and external sources. You never read `runs/`, `docs/research/` other than your own folder, or scripts."
   - Optionally enforce it with a `PreToolUse` hook on `Read`.
   - Separately, retire the 2026-10-11 control name: it is burnt in a public repo. Each run needs a fresh control, written only in that run's brief as an ordinary question.
2. **Line 48: add:**
   "WebFetch returns a model's answer, not the page. Ask it for the exact sentence and mark the row `quoted via WebFetch`."
   - Outside this file: the main agent runs a quote check after the researcher returns (fetch each URL raw, then search the page for the quoted text), the same way check-findings.py is run after.
3. **Frontmatter: add a `hooks:` `PreToolUse` entry with matcher `Write`.** It exits 2 for any path outside `docs/research/**` and `runs/*/nodes/**`. Lines 13–15 can then say the limit is enforced.
4. **Frontmatter: add `maxTurns:`.** Line 67 then has a stop the harness enforces. I give no number: take it from the tool-call counts of the 2026-10-11 runs.
   - **Line 57, add:** "A fetch that returns nothing or stops at the length limit (WebFetch reads about 100,000 characters per call; continue with `offset`) is a Gaps entry, never silence." This is the "one call returned nothing" lesson.
5. **Line 14: either delete it, or give the file's shape.** If kept, it must list the eight header keys that `validate_result.py --kind result` requires.
6. **Lines 49–50: define `unproven` by what was read**, not by who said it, or ask EJ which they mean (see below). Add one line saying the four labels follow check-findings.py and the TASK_TYPES row is flagged for cleanup.
7. **Line 46: add a source-quality line:**
   "Prefer the primary (paper, repo, vendor docs) over a write-up of it. If only a write-up was found, label it `reported` and name the primary under Gaps."
8. **Line 48: add a note on `|`:** a quote containing `|` breaks the table, because check-findings.py splits cells on it. The researcher must write such a quote outside the table or note the character.
9. **Leave as is:**
   - Line 3: do not add "use proactively". The repo's default is that the main agent researches herself.
   - Lines 72–73: the digest labels are good.
   - Line 5: `model: inherit` is fine. But TASK_TYPES names agy as the engine for research, so log this Claude subagent in the ledger as a challenger. Do not change the table on n=0.

**What is more than it needs:** only Grep and Glob, and line 14 unless runs actually use it.

## What I need to know
- Will this subagent run inside workflows that plant a control? If yes, check-findings.py needs the control name passed in as an argument instead of hard-coded. If no, the main agent needs a different check, because the current one fails every file.
- What does EJ mean by `unproven`: "the source shows no evidence" or "no source was read"? Change 6 depends on it, and I will not pick for them.
- May the researcher have Bash, limited to fetching pages? If yes, it could get raw pages and real quotes, and change 2 moves inside the subagent. If no, the quote check stays with the main agent.
- The `maxTurns` figure: measured from the 2026-10-11 runs, or set by EJ.

## Costs and risks
- **Change 1** (from my #5): a fresh control name every run, plus a Read hook to maintain if it is enforced. Without the hook it is instructions only, and a worker could still open a run file.
- **Change 2** (from my #4): a new quote-check script for the main agent. Expect it to fail some honest rows, since pages change and markdown conversion alters whitespace. It needs a looser match rule, and that is n=0.
- **Change 3** (from my #2): a hook script in the agent file. It runs only in a trusted folder, so in an untrusted one the limit silently reverts to instructions. I have not tested it.
- **Change 4** (from my #3): a turn cap that is too low cuts research short. The Gaps line hides it only if the researcher fails to write the cap into Gaps.
- **All changes** (from my #10): the evidence behind every point is two runs on one day plus my reading of docs. That is a hint, not a law.

## How we would know I was right
Write this down before running (my #3):
- **Metrics:** check-findings defects; the share of quotes found in the raw page; `validate_result.py --kind digest` pass or fail; lines returned to the main agent; tool calls.
- **Prediction:** the researcher type has no more defects than the current way. The quote match is below 100% in both arms until change 2 lands. Both arms report the fresh control as NOT FOUND.
- **Stop date:** one week out.

The run (my #4, my #2, my #8):
- **Arm A:** `general-purpose` with the contract pasted.
- **Arm B:** the revised `researcher`.
- **Both arms:** the same external question, with one fresh made-up name in the brief, stated as an ordinary question.
- **Hook test:** one deliberate Write to `/tmp` in arm B must be blocked.
- **Reporting** (my #9 and my #10): report the result whichever way it goes. If A matches B, the subagent buys only what the facts claim, the contract arriving without pasting, and the case for a custom type is that alone. n=1 per arm is a hint.
