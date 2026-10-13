# Brief, stage 1 — literature review: how to generate `INDEX.md`

You are one of four independent researchers. You do not see the others' work in this stage.

## The problem

Read `/home/smoke01/dev/ancient-games/docs/memory-system/SOURCE_OF_TRUTH.md` first, in full. It is an accepted design
for a project's memory: plain markdown files in the repo. The part this research is about:

- Each memory entry is its own file under `project-memory/entries/`, with a YAML-style header (`id`, `kind`,
  `status`, `covers`, …) and a one- or two-sentence claim.
- `project-memory/INDEX.md` is **generated** from `entries/`: one line per active entry (id, kind, one-line claim),
  never edited by hand (K6).
- Every agent reads `INDEX.md` at session start (Rd2.1), so it must fit the strictest start-file size limit of the
  agents that read it (Rd3).
- A fresh clone must be able to read memory with no network, no cache and no private store (Rd1.2).
- Several agents work at once, each on its own git branch or worktree (W6). Each new entry is its own file, so
  entries rarely conflict — but a single generated `INDEX.md` that every branch rewrites is one shared file.
- Still open in the design: which tool generates `INDEX.md`, what runs it, and when (K6).

## Your question

**What is the best algorithm for generating `INDEX.md`, according to what already exists in the open-source world?**

Cover all of these:
1. **Building the lines:** what is read from each entry, what is written, the order, and how the output stays the same
   for the same input.
2. **When it runs and what runs it:** at commit, at merge, in CI, at session start, on demand.
3. **Git:** committed or not; how parallel branches avoid or resolve conflicts on it.
4. **Size:** what happens when the index outgrows the start-file limit.
5. **Checking:** how anyone can tell the index is in step with the entries.

Look for real prior art: tools, projects and write-ups that generate an index or a combined file from many small
files kept in git, and files written as an index for AI agents. Search the web and GitHub. Prefer primary sources
(the project's own README, docs or code) over blog summaries.

## Rules

- Every finding names its source (URL) and says whether you **quoted** it from that source, or it is **my reading**.
  Quote the source's own words where a claim rests on them.
- If you looked for something and did not find it, say so. Do not fill a gap with a guess.
- Do not change any file in the repo. Read only.
- No design of your own in this stage beyond what the sources support; the proposal comes in stage 2.

## Output — one markdown report

```
# INDEX.md generation — literature review (<your engine name>)

## Sources
| id | source (name + URL) | what it is | date or version, if shown |

## Findings
Each finding: an id (<your prefix>1, <your prefix>2, …), one or two sentences, its source id, and the label
"quoted" (with the quote) or "my reading".
Group them under the five headings of the question.

## What I looked for and did not find

## Gaps and disagreements between sources
```

The launcher tells you your engine name, your finding-id prefix and where the report goes.
