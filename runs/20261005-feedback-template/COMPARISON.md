# Two engines improve the ui/ux dev feedback template — 2026-10-05

Both were given the same brief and the method's own tool — the six whys. Neither saw the other.

## The convergence (the part that matters)

**Both independently found that `Accepted` is broken.** The worker writes the summary *before* the human looks, so
`Accepted` can only ever be "pending" or a lie. Claude removed it; MiniMax kept it but renamed it `Verdict`, marked it
*filled by the human*, and left it blank until then.

**Both renamed `Proof`.** For UI there is usually no re-runnable command; the "proof" is *what the human looks at*.
Claude: `Look`. MiniMax: `Shown at`.

**Both kept `Changed`, `Why`, `Effort`**, and both left **Effort's unit open** (rounds, tokens, or minutes?).

## The merged template

```
Changed / Look / Why / Verdict / Effort
```

| field | filled by | the improvement |
|---|---|---|
| **Changed** | worker | claude: unchanged wording. minimax: add **blast radius** — *"what else it renders into, unchecked"* |
| **Look** | worker | route + viewport/device + data state; **which states it does NOT show** — turns a silent gap visible |
| **Why** | worker | kept by both; the restatement exposes a misread task before the human looks |
| **Verdict** | **human** | `accepted / accepted-with-changes / rejected` + the one thing the next round must do. Blank until the human writes it |
| **Effort** | worker | the loop's thrash signal (3 rounds, one screen); unit left open |

## The six-whys, done properly

Both reached the three kinds of answer the method asks for:

- **fact** — a build stays green while a shared component renders wrong elsewhere (minimax, `Changed` why-4)
- **value judgement** — the worker's restatement of intent is where worker and client most often differ (both, `Why`)
- **unanswerable** — "which states it does not show, is that list ever complete?" → *"no one can answer"* (claude)

## What they disagreed on, and what is open

1. **Effort's unit** — rounds / tokens / minutes. Both left it open; it applies to `code generation` and
   `test script gen` too.
2. **The human verdict's home** — a blank `Verdict:` line in the summary, or a separate record? minimax's gap 3.
   The run needs to know "worker done, waiting on human" either way.
3. **Keep `Effort` on human-in-loop types?** minimax questions it — the wall-clock cost there is human wait, not
   tokens, so "3 rounds" is less about thrash and more about the human. Open.

## The deeper point

This is the design rule the user asked for — *"the LLM may suggest a better template"* — working. Two engines, given a
default, each returned a better one with the reasons attached, and the six-whys surfaced a defect (`Accepted`) that a
field list alone would not have.
