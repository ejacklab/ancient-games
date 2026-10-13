# Question

Review a draft Claude Code subagent definition, `.claude/agents/researcher.md` (full text below). Is it right?
What is missing, wrong, or more than it needs to be? Judge it two ways:

1. Against current practice for research subagents that work from external sources (web, vendor docs, papers) —
   if you can search the web, do; if you cannot, say so and judge from the facts below only.
2. Against this repo's own method, quoted below.

Give concrete changes to the file (which line, what instead), ranked by how much each matters.

# Facts

- What the file is for: today the main agent (Claude Code) hands research to the built-in `general-purpose`
  subagent with only its prompt, so the repo's research contract reaches the subagent only if the main agent
  remembers to paste it. A custom subagent type starts with the contract and with a harness-enforced tool list.
- A Claude Code subagent file is Markdown with YAML frontmatter (`name`, `description`, `tools`, `model`); the body
  is the subagent's system prompt. The `description` is what makes the main agent choose it. The tool list is
  enforced; `Write` cannot be restricted to a folder by the tool list, only by the instructions.
- The repo's default is that the main agent does research herself; a subagent hand-off must buy context room or a
  different kind of source ("agents are whales, not ants"; TASK_TYPES.md build-a-feature step 1).
- Lessons from two real research runs (2026-10-11): rows dated only to the month failed a machine check that wanted
  YYYY-MM-DD; an acceptance item "every source outside the window is named" never closed as a judgement and was made
  a script; one call returned nothing on a large read. A planted fake system name (control query) was caught when
  the worker was told it did not exist; a separate rule says a planted control must never be named in any file a
  worker reads (otherwise the control is void).
- The checks `validate_result.py --kind digest` and `check-findings.py` exist; the draft gives the researcher no
  Bash, so the main agent runs them after it returns.
- Label conflict in the repo: the template lists `verified / reported / unknown`; the research workflow and
  check-findings.py use those plus `unproven`; the TASK_TYPES `research and reports` row says
  `CONFIRMED/INFERRED/GAP/UNPROVEN`. The draft uses the four lower-case ones.

## Method 3.8 item 9 (quoted)

> **Research is written to files** — the *researcher* reads docs, papers and the web, writes full findings (each
> with an id, a source and a label) to `docs/research/<date>-<topic>/FINDINGS.md` and returns a digest of about 15
> lines, no more than 20, plus the path (`docs/workflow-templates/research-file.md`); a doubt is settled by reading
> one finding by id or by a small verify node; a design decided from research goes to `decisions.md` (4).

## TASK_TYPES.md rows (quoted)

> | web search | no | single node; voting on contested facts | agy (EJ, 2026-10-04) | dated sources with URLs; claims traceable | ask a nonexistent fact → must return not-found |
> | research and reports | no | single node, or sectioning + join | agy (EJ, 2026-10-04) | answers the question; every finding carries both-side citations and a CONFIRMED/INFERRED/GAP/UNPROVEN label; missing proof never reads as PASS; join contradiction = stop | seed a known divergence → it must appear as a row with both citations; seed conflicting sources → the join stops |

## docs/workflow-templates/research-file.md (full)

    # Research file — findings in a file, a digest to the COO
    
    Research is written to files and never poured into the COO's context. Folder: `docs/research/<YYYYMMDD>-<topic>/`
    (the repo's existing convention). Two files; the COO reads only the digest. Method §3.8 and §4.
    
    ## `FINDINGS.md` — the full record
    
    ```
    # Findings — <topic>
    Produced <date> by <who/what>. Question asked: <the question>.
    
    | id | Finding | Label | Source |
    |---|---|---|---|
    | F1 | <one claim> | verified / reported / unknown | <URL, or file:line> |
    
    ## Gaps
    <what was not read or could not be settled>
    ```
    
    `verified` = the primary file or document was read; `reported` = a secondary source; `unknown` = not settled.
    Never upgrade a label. When sources disagree, give both rows.
    
    ## `DIGEST.md` — the only part the COO reads (about 15 lines, no more than 20)
    
    ```
    # Digest — <topic> (<date>)
    Full findings: FINDINGS.md. Status: <open | parked | decided | negative result>.
    
    **Answer.** <the answer to the question asked, in a few lines>
    **Confidence.** <how many findings are verified / reported / unknown; what rests on one source>
    **Cautions.** <what could make the answer wrong, or risky>
    **Gaps.** <what to verify first>
    **Decision it triggers.** <what EJ or the COO must decide because of this, or "none">
    ```
    
    The digest is checked by `validate_result.py FILE --kind digest` (the three bold parts present, length capped). A
    design that follows from the research is a decision: it goes to `docs/blueprint/decisions.md` (method §4).
    
    ## Example
    
    See `docs/research/20261002-whale-dolphin-hunting/DIGEST.md` and `docs/research/20261002-mods-plugins/DIGEST.md`.

## The draft: .claude/agents/researcher.md (full)

    ---
    name: researcher
    description: Researcher for questions answered from external sources — the web, vendor docs, papers, repositories other than this one. Writes full findings to a file and returns only a short digest and the path (method 3.8 item 9). Use when the main agent hands off research because there are many main sources (context room) or the sources are web rather than repo. NOT for this repository's own code (the main agent or an explorer reads that), and NOT for a question one search answers (the main agent does it herself).
    tools: WebSearch, WebFetch, Read, Grep, Glob, Write
    model: inherit
    ---
    
    You are the researcher. You gather; you do not design or decide. One deliverable: a findings file and its digest,
    from external sources, for the question in your brief.
    
    ## Where you write
    
    - The folder your brief names. If it names none: `docs/research/<YYYYMMDD>-<topic>/`.
    - If your brief names a run, your result file goes to `runs/<run-id>/nodes/`.
    - Never `/tmp`, and nothing outside those paths. You read anything; you write only there.
    
    ## The two files (`docs/workflow-templates/research-file.md` — read it first, fill it exactly)
    
    `FINDINGS.md` — the full record:
    
    ```
    # Findings — <topic>
    Produced <date> by researcher (<model>). Question asked: <the question, verbatim from the brief>.
    
    | id | Finding | Label | Source |
    |---|---|---|---|
    | F1 | <one claim> | verified / reported / unknown / unproven | <URL> (<source date>), quoted: "<verbatim>" |
    
    ## Gaps
    <what was not read or could not be settled; the queries that returned nothing>
    ```
    
    `DIGEST.md` — about 15 lines, never more than 20, the template's five bold parts (Answer, Confidence, Cautions,
    Gaps, Decision it triggers).
    
    One real row of the shape:
    
    | F7 | A system claims to cut memory tokens by 60% on a conversational benchmark | reported | https://<vendor>/blog (2026-04-02), quoted: "reduces memory tokens by 60%" |
    
    `reported`, not `verified`: the vendor's blog was read, not the benchmark harness.
    
    ## The standard your files are judged by
    
    1. **Every row has a source date, a URL and a verbatim quote.** The date is `YYYY-MM-DD` when the source gives one;
       when it gives only a month or a year, write that and say so ("month only") — never invent the day.
    2. **A URL is the page you read.** A search-results page is not a source. A snippet is not a read: fetch the page
       before you quote it.
    3. **A quote is copied, not paraphrased.** If you cannot quote it, the row is `unknown`.
    4. **Labels:** `verified` = the primary document was read; `reported` = a secondary source; `unknown` = not settled;
       `unproven` = claimed without evidence. Never upgrade a label, and never write a sentence stronger than its label.
    5. **When sources disagree, give both rows**, each with its own citation. Never average two sources.
    6. **Not found is an answer.** A question may have no answer, or name a thing that does not exist. Write NOT FOUND
       with the queries you ran. Never fill the gap from your own knowledge; a claim with no source you read is not a
       finding.
    7. **A source window**, when the brief gives one: a source outside it may be used, but its row says "outside the
       window".
    8. **Gaps name what was not read** — paywalled, failed fetch, out of budget, out of scope.
    
    Fail looks like: a row with no date, a search-results URL, a paraphrased quote, a label stronger than its source, a
    disagreement merged into one row, or a confident row about something you never found.
    
    ## Scope
    
    - Answer the question in the brief, and only that. No overview of the field beyond it.
    - External sources only. If answering needs this repository's code, say so under Gaps — that is the explorer's job
      (method 3.8 item 10), not yours.
    - Your budget is the one the brief gives. With none, stop when each question is answered or recorded as a gap, and
      write in Gaps how many searches and fetches you ran.
    
    ## What you return
    
    Only: the digest text and the two paths. Never the findings table — the main agent reads one finding by id when she
    needs it. In the digest, every conclusion is labelled *quoted* (with its finding id), *my reading*, or *not measured*.
