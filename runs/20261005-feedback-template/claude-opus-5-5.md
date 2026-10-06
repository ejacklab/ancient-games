My improved template is **`Changed / Why / Proof / Look / Effort`**. It is the `code generation` template plus one field, **Look**, for the human checkpoint. I took **Accepted** off the worker's summary: it belongs to you, not the worker. The full whys are in `runs/20261005-feedback-template/claude.md`, which is the only file I created. In that folder I read only `BRIEF.md`; there was no answer from the other engine to see.

**What changed, and the why that settles each:**

- **Accepted, removed.** The worker writes its summary before you have looked. So all it can write is "pending", which tells you nothing, or "yes", which means checking its own work in the field you read first. → *fact*: the summary always comes before your acceptance.
- **Look, added.** Where you see the change (screenshot, URL or steps), which states it shows, and which it does not.
  - It is separate from Proof because Proof is a machine check (the build exits 0) and Look is what you judge. In one field, "build passed" can stand in for "looks right".
  - The task-type table's sabotage test ("break a component → the build fails") only catches breakage. A wrong or ugly layout only your check catches, so your check needs a precise input.
  - Naming the states it does not show turns silent gaps into visible ones. Whether that list is ever complete → *no one can answer*; it is a guess (n=0).
- **Proof, narrowed** to the command and its result. A verifier can re-run a command but not an opinion. → *fact*.
- **Why, kept.** The worker's restatement shows a misread task in one line, before you spend time looking at the screen. → *value judgement*: your attention is the scarcest check in the loop (a guess, n=0).
- **Changed, kept** with the same wording as code generation. The task-type table describes ui/ux as "codegen loop + human checkpoint", so one verifier can read both. → *fact*.
- **Effort, kept**, but I left its unit open rather than choosing one.

**Questions for you:**

1. **Effort:** does it count attempts out of the limit, tokens, or minutes? This applies to the code generation and test script templates too.
2. **Accepted:** should the summary file keep a blank `Accepted:` line that you fill in, or should your verdict go in a separate record?
3. **Look:** should it be a screenshot file, a URL, or steps? That depends on whether opencode or Codex can render pages headless in your setup, which I didn't check.
