# Brief — p3-review, attempt 1

## Task (one deliverable)

Review one change to a design for AI-agent project memory. The design is three files: a prose document
(`SOURCE_OF_TRUTH.md`), its requirements (`SOURCE_OF_TRUTH_REQUIREMENTS.yaml`) and a release-notes file. The change
fixes five leftovers from an earlier review. Judge whether each is fixed as decided, and find any contradiction the
change leaves between the three files or inside one. Do not fix anything.

## The five leftovers, and what was decided (by the project's owner)

- **L1** W6.3b's `check` must agree with K6.3b's (W6.3b points to K6.3b).
- **L2** K4.3: after its first commit an entry's `covers` may be corrected in place, with a `changed:` line;
  `source` and `depends_on` still change only by superseding the entry. The claim, `id` and `kind` never change.
- **L2b** W6.3a: a merge keeps every `covers` path either side wrote.
- **L3** The YAML's paths are relative to its own folder; the prose, the YAML, `CACHES.md` and `vision-statements/`
  travel together as one kit.
- **L4** A typo in the prose's "When to write" table ("When the work a decision to build something is complete").
- **L5** Rd3.1a: the project owner decides which agents work on the project, and so the strictest `INDEX.md` limit;
  until the project owner records measured limits, the tool holds the example in Rd3.1b.

## Read only these files, in REVIEW_DIR

- `change.diff` — the change (against the version before it).
- `SOURCE_OF_TRUTH.md`, `SOURCE_OF_TRUTH_REQUIREMENTS.yaml`, `SOURCE_OF_TRUTH_RELEASE_NOTES.md` — the three files
  after the change, in full.

Do not read anything else: not the repo, not other folders, not git history. The YAML already passes scripts that
check its structure (one record shape, unique ids, every link and path resolves). Your job is what a script cannot
see: meaning.

## Return (your final message; write nothing to disk)

```
---
node: p3-review
attempt: 1
engine: claude-subagent
model: <your model id>
status: ok
---
<one sentence: verdict and finding counts>
| leftover | fixed as decided? yes/no | evidence (file:line, quoted) |
|---|---|---|
## Contradictions
- C1 [high|medium|low] file:line vs file:line — "<quote>" / "<quote>" — what disagrees
## Other findings
- O1 file:line — …
```

REVIEW_DIR = /home/smoke01/.claude/jobs/7d643882/tmp/review-sot
