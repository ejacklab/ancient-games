# 范蠡 (Fan Li): review of the draft `researcher.md` subagent

## Answer
The draft is mostly right. Its split of roles, its rules for each row, and its "not found is an answer" rule should stay. But it shouldn't become the research route yet. Three preparations are still open:
1. Its read reach can expose a planted control.
2. Its NOT FOUND rows would fail the check the main agent is meant to run afterwards.
3. It quietly forks the template's labels and row shape when it should point to one copy.

If EJ settles the label set and the check script is made general, then the ranked changes below are enough to adopt it.

## How I decided
1. **I checked the preparations before saying "fight" (my #18, 「審備則可以戰乎？」, quoted).** I read three things in the repo, read-only. I also fetched the current Claude Code subagent and hooks docs (code.claude.com/docs/en/sub-agents, /hooks) and Anthropic's research-system write-up (anthropic.com/engineering/multi-agent-research-system, 2025-06-13). What I read:
   - `runs/20261011-agent-memory-graph/check-findings.py`, lines 1–60
   - the digest check in `.claude/skills/workflow-design/scripts/validate_result.py`
   - the live `.claude/agents/researcher.md`, which matches the brief's copy
2. **Gap 1: the read reach can void a planted control (my #18).** The check script hard-codes `CONTROL = "magmamem"`, and it lives inside the repo. The draft gives the researcher `Read, Grep, Glob` over the whole repo. Any file the worker can grep counts as "a file a worker reads", so a planted name kept anywhere in the repo is exposed. The draft's generic rule 6 is safe because it names no plant. The leak comes from the tools.
3. **Gap 2: the check rejects what the draft asks for (my #18).** `check-findings.py` exempts only the MagmaMem control row. Any other `F` row without a URL or a 4-digit year fails it. So rule 6 ("Write NOT FOUND with the queries you ran"), written as an F-row, fails the check that is supposed to run afterwards. The script also fails any file that has no MagmaMem row. It is specific to one run and can't be "run after it returns" on new research as it stands. The date rule is fine: the script only needs a year, so "2026-04 (month only)" passes. The YYYY-MM-DD failure on 2026-10-11 came from the workflow's JSON check, not from this script.
4. **Gap 3: a plan made at court shouldn't change in the field (my #5, 「天節固然，唯謀不遷」, quoted).** The draft says "read it first, fill it exactly" about the template. Then it changes two things:
   - It adds a fourth label, `unproven`.
   - It turns the Source column into URL + date + quote.

   That changes the plan in the field: a second copy that disagrees with the first. The template's three labels describe how far the source is from the claim. `unproven` describes whether the source shows evidence. Those are two different measures. The draft's own example row F7 (a vendor blog claiming 60% with no harness) is both `reported` and `unproven`, and the draft doesn't say which one wins.
5. **Which label set wins is for people to settle (my #2, 「定傾者與人」, quoted).** Three label sets exist: the template's, the workflow's, and TASK_TYPES' CONFIRMED/INFERRED/GAP/UNPROVEN. Choosing between them is EJ's call, not the file's. Until EJ chooses, the matter hasn't run its course (my #3, 「事不究，不可彊成」, quoted).
6. **Say who is better at what (my #14).** The draft's division is good and should stay: the researcher gathers, the main agent runs the checks, the explorer reads repo code. But TASK_TYPES names agy as the research engine (EJ, 2026-10-04), while this file creates a Claude researcher. The file should say when Claude is the better choice. My reading: when the result has to be written into the repo and the tool list has to be enforced by the harness.
7. **Full without overflowing (my #2, 「天道盈而不溢」, quoted).** `Grep` and `Glob` are more than a researcher of external sources needs. It needs `Read` only for the template and its brief. The description shouldn't be given "use proactively" (the docs suggest that phrase to encourage delegation). That would contradict the repo's rule that the main agent researches herself by default. The same goes for contention being the last resort (my #13).
8. **Stop when the count runs out (my #10, 「究數而止」, quoted).** The docs list a `maxTurns` field enforced by the harness. My reading: it is worth adding only as a generous outer limit, because a cut-off before the digest is written loses the return.
9. **What the harness can enforce today, read from the docs.** The fact "Write cannot be restricted to a folder" is true of the tool list only. Subagent frontmatter accepts `hooks`, and a `PreToolUse` hook can block a call with exit code 2. A hook matching `Write` could refuse paths outside the allowed folders. *Not verified:* that the Write input field is called `file_path`. The docs only imply it through a `${tool_input.file_path}` example.
10. **Current practice for research agents (Anthropic, quoted from that article).**
    - "use primary sources over lower-quality secondary sources", because agents tended to pick "SEO-optimized content farms"
    - "Each subagent needs an objective, an output format, guidance on the tools and sources to use, and clear task boundaries"
    - outputs go to a filesystem, with "lightweight references back to the coordinator"

    The draft already meets the objective, format, boundaries and file-output points. It lacks the push toward primary sources.

**Concrete changes, ranked by how much each matters:**

1. **`tools:` line.** Change to `tools: WebSearch, WebFetch, Read, Write` (drop `Grep, Glob`). Add to "Where you write": "You read only `docs/workflow-templates/research-file.md` and the files your brief names; never `runs/` or any script." Outside this file: keep plant names out of the repo until after the verdict, so move `CONTROL` out of `check-findings.py` and pass it as an argument. *(my #18)*
2. **Rule 6.** Instead of an F-row, use: "Write NOT FOUND under `## Gaps`, with the queries you ran and the date — not as an F-row." If EJ wants NOT FOUND as rows, then `check-findings.py` must accept them. Either way, generalise the script (control and min-rows as arguments) and move it next to `validate_result.py` before the draft relies on it. *(my #18)*
3. **The "read it first, fill it exactly" line and the FINDINGS block.** Settle the labels and row shape in `research-file.md` first, then make the agent file point to it rather than restating it. Separately, define `unproven` as "the source itself gives no evidence for the claim" and say whether it replaces `reported` or comes alongside it. Then fix row F7 to match. *(my #5, #2)*
4. **The frontmatter.** Add a `hooks:` `PreToolUse` entry with matcher `Write`, running a script that exits 2 for any path outside `docs/research/` and `runs/*/nodes/`. *(my #18)*
5. **The "result file goes to `runs/<run-id>/nodes/`" line.** That file is undefined: the template has only FINDINGS and DIGEST. Either name it (what it holds and who reads it) or delete the line. *(my #4: a thing started and not finished turns back on you)*
6. **Rule 8, add:** "An empty or cut-short fetch is a failed fetch, not an absence. Read on with WebFetch's `offset`, retry once, then record it in Gaps." This addresses the 2026-10-11 empty large read. Also add: "Write FINDINGS.md early and rewrite it as rows grow, so a cut-off keeps what was found." *(my #4)*
7. **Rule 4, add:** "Before you write `reported`, search once for the primary (paper, repo, spec, vendor doc) and fetch it if it exists." *(my #12, cross-check before engaging; applying it here is my reading)*
8. **Rule 7.** Fix the exact phrase as `outside the window (<source date>)` so a script can find it. The acceptance item about the window only closed once it became a script. *(my reading)*
9. **`model: inherit`.** This is a question for EJ, not a fix. The research engine in TASK_TYPES is agy. *(my #14)*
10. **Optional:** `maxTurns:` as an outer limit, set well above the brief's budget. *(my #10)*

## What I need to know
- **Which label set wins.** If EJ picks CONFIRMED/INFERRED/GAP/UNPROVEN, then changes 3 and 2 change shape, and `check-findings.py`'s `LABELS` changes too.
- **Is this Claude researcher an exception to the agy row, or a challenger** under the 20% rule and logged in `TASK_TYPES_LEDGER.md`? If it's a challenger, add the ledger entry and leave the table alone.
- **What the `runs/<run-id>/nodes/` "result file" is meant to hold.** If it's the digest, change 5 becomes "write DIGEST.md there".
- **Whether a controlled run should plant its control in the brief only.** If yes, change 1's instruction is enough without a Read hook. If plants must also be safe from a worker that ignores instructions, a `PreToolUse` hook on `Read` is needed too.

## Costs and risks
- **Change 1 (dropping Grep/Glob and limiting reads), my #18.** The researcher can't check repo files to avoid duplicating earlier research. The main agent has to name prior research in the brief. The read limit is instruction-only unless a hook is added.
- **Change 2 (NOT FOUND to Gaps, general check), my #18.** Changes a script that two finished runs used. Re-run it on their files to make sure it gives the same verdicts.
- **Change 3 (one copy of the template), my #5.** Waits on EJ, so the agent can't be adopted today. Changing the template also changes what earlier FINDINGS files are judged by.
- **Change 4 (Write hook), my #18.** One more script to maintain. The `file_path` field name isn't verified, and hooks are ignored if the agent ever ships as a plugin. A wrong hook blocks every write and the run returns nothing.
- **Changes 6 and 7 (retries, early writes, primary sources), my #4 and #12.** More fetches per question, so more tokens and time.
- **Change 10 (`maxTurns`), my #10.** Set too low, it cuts the agent off before the digest and the main agent gets nothing back.
- **Not adopting at all (my #3: wait).** The research contract keeps reaching subagents only when the main agent remembers to paste it.

## How we would know I was right
1. Run `check-findings.py` as it is today on a FINDINGS file written by the draft that contains one NOT FOUND F-row. I predict it fails that row and also fails "no control-query row". After change 2, the same file passes.
2. Give the draft researcher a brief with a fake system name. Leave a file in `runs/` that names it as a plant, then look at the transcript. If it called Grep/Glob/Read on that file, the leak in step 2 above is real. After change 1, the transcript shows no such call, and the control is caught or missed on its merits.
3. With the hook from change 4, ask the agent to write to `/tmp/x.md`. The write is refused with the hook's message. A write to `docs/research/<date>-test/FINDINGS.md` goes through.
4. After change 3, `grep -c unproven docs/workflow-templates/research-file.md .claude/agents/researcher.md` shows the label defined once, in the template only.
5. On one real research hand-off, `validate_result.py --kind digest` and the general `check-findings.py` both pass with no hand edits by the main agent.
