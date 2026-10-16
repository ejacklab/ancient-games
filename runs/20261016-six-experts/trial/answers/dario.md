# Answer — What a pre-flight check should verify in a question file or worker brief

## Answer
Verify, in this order: the engine can read the file; nothing in it should not reach an outside engine; its required headings are present; no placeholders are left; every input it names exists; its output location is usable; and it fits the engine's context window. Deliberately do not verify whether the question is good, whether the facts in it are true, or whether the engine choice is right, because a script cannot judge those and a pass would mislead.

## How I decided
1. **How I ranked.** I ranked by how often a defect costs a whole engine call, multiplied by how bad and how hard to undo it is. I was not given a failure history, so this is my reasoning, not measurement (see "What I need to know").
2. **Item 1: the engine can read it.**
   - *Looks for:* the file exists, is non-empty, is valid UTF-8, and the path in the "read <file>" line is absolute and resolves.
   - *How a script tells:* `stat`, a size check, a decode, and a check that the path is inside the root the engine is allowed to read. This part is per engine.
   - *Prevents:* a call that exits 0 and does nothing, or answers about a file it never saw.
3. **Item 2: nothing goes out that should not.**
   - *Looks for:* credentials and private material, because Codex, MiniMax, DeepSeek and Gemini are third parties. It checks for key and token patterns, private-key blocks, `.env`-style lines, and any path or name on an owner-kept "private" list.
   - *How a script tells:* regexes plus a deny list.
   - *Prevents:* an irreversible leak. It is rare but the worst outcome here, so it sits second.
4. **Item 3: the contract is present.**
   - *Looks for:* the headings the template requires (question or task, how to answer, exact output format for question files; the node-brief fields for worker briefs), each exactly once.
   - *How a script tells:* read the required heading list from the template file itself, so there is one copy, and match it against the brief.
   - *Prevents:* a brief with no output format, or two conflicting ones, which gives an answer the comparison step cannot read.
5. **Item 4: no leftovers.**
   - *Looks for:* `TODO`, `TBD`, `FIXME`, `{{ }}`, and `<placeholder>` text outside the "Write exactly this" block.
   - *How a script tells:* a regex that skips the output-format block, which legitimately contains `<...>`.
   - *Prevents:* the engine answering a half-filled template.
6. **Item 5: named inputs exist.**
   - *Looks for:* every repo path the brief tells the engine to read.
   - *How a script tells:* extract paths from an "inputs" section (or backticked repo-relative paths with an extension) and `stat` them. Paths the worker is to create are declared as outputs and skipped.
   - *Prevents:* the engine hunting for, or inventing, a missing input. This may need a small template change that separates inputs from outputs.
7. **Item 6: the output location is usable** (worker briefs only).
   - *Looks for:* a declared output path whose folder exists and is inside the allowed write area.
   - *How a script tells:* `stat` the directory and compare it with the write scope.
   - *Prevents:* work done and then lost or refused.
8. **Item 7: it fits.**
   - *Looks for:* file size compared with the smallest context window among the engines the file may go to.
   - *How a script tells:* a byte or word count against the window value in the engine config.
   - *Prevents:* silent truncation. I rank it last because most briefs are small.
9. **What it should not verify, and why.**
   - *Whether the question is clear or the right one:* a word-count proxy would pass bad briefs and fail good ones, and a pass would be read as "reviewed".
   - *Whether facts in the brief are true or current:* a script cannot know. The path checks in items 5 and 6 are the only honest part of this.
   - *Whether the engine suits the task:* that is a design choice, not a property of the file.
   - *Style, tone and length:* only add these if a style rule has already caused a failure.
   - *The shape of the CLI call* (stdin redirect, flags): that belongs in the runner's tests, not the file check.
   - *Fixing the file:* it reports and fails, nothing more.
10. **Report what a pass means.** A pass says "structurally sound, nothing banned", not "good brief". The check is written by the same side that writes the template, so it is not independent evidence of quality.

## What I need to know
- **What have past engine calls actually failed on because of the file?** Real failures should set the order and cut items that never fire. My ranking could change a lot.
- **Which engines can read files outside the repo, or in which folders?** This decides whether item 1 is one rule or one per engine.
- **Does a script downstream parse the answer headings?** If nothing parses them, item 3 is much weaker.
- **Who keeps the "private" list for item 2, and what is on it?** That is for EJ to decide, and I should not guess it.
- **Do all worker briefs follow `node-brief.md` with fixed headings?** If not, item 3 cannot be written for them.
- **What share of the context window counts as too big for item 7?** I will not invent that number. EJ should say whether it is a block or only a warning.
- **Does a failed check block, or can the main agent override it with a written reason?** I assume it blocks with a logged override.

## Costs and risks
- **False fails:** a valid brief gets blocked, people learn to bypass the check, and then it protects nothing. A logged override helps.
- **Placeholder and path heuristics can misfire:** angle brackets in examples, URLs, example paths, and output paths that do not exist yet.
- **Two copies drifting:** if the heading list is not read from the template, every template change needs a matching check change.
- **The secrets scan gives false comfort:** it catches known formats only, not private business content. Never report "no secrets found", only "no known patterns found".
- **It does not see the engine's side:** sandbox rules, quota, login and timeouts still fail after a pass.
- **Maintenance:** a script that is never exercised rots.
- **Time:** small, because it is `stat` and regex with no AI call. It is still added to every engine call, so each item has to earn its place.
- **My own uncertainty:** the order and the item list come from reasoning, not from failure data.

## How we would know I was right
1. **Seeded-bad test (can it fail?).** Take one good brief and break it once per item: empty file, planted fake key, a deleted required heading, a leftover `TODO`, a missing input path, an unusable output folder, an oversized file. Every variant must fail on exactly its own item. Then run the check on several past briefs known to have worked, and all of them must pass.
2. **Replay.** Run the check over briefs from past engine calls that failed, and count how many it would have caught and by which item. Items that catch nothing are candidates to remove.
3. **Live log.** For each real call, record the file, engine, verdict, failed items, and the outcome (empty output, wrong format, missing input, none).
   - *Escapes:* calls that passed the check but failed for a reason an item covers. Any escape means that item is wrong.
   - *False fails:* checks the main agent overrode as wrong. A high rate for one item means fix or drop it.
   - *Hits per item:* how many times each item fired, compared with its time cost.
4. **Cost.** The check's wall time should be negligible next to an engine call. If it is not, that is a defect.
5. **What would show I was wrong:** the log shows engine-call failures from file defects that none of these items covers, or the top item never fires while another item catches most of the problems.
