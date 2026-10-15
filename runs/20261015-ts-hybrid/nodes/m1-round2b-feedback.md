Small repair after your attempt 2. The COO resolved two points in SPEC.md (re-read the M1 section):

1. **A pipe into codex is fed stdin, so it is not the trap.** Your attempt-2 change made
   `lint: a pipe in another segment does not satisfy the codex stdin exception` expect `trap:codex-stdin` for
   `printf task | codex exec -`. That would block a correct command (a false deny — the very thing round 2 fixes).
   SPEC now gives `Segment` a `piped` field (true when the separator before it is `|`) and traps an `unless_piped`
   condition; `data/traps.yaml` sets `unless_piped: true` on `codex-stdin` and its `unless` regex no longer mentions
   the pipe. `src/types.ts` exports `Segment`. Change that test to expect **no** finding, and add tests for
   `segments(...).piped` (true after `|`, false after `||`, `;`, `&&`, and for the first segment) and for a planted
   trap with `unless_piped: true` against a piped and an unpiped segment.
2. SPEC line about recognition `background` now says it is the matching segment's `background` (your CONTRADICTS);
   no test change needed if yours already follow the Segments rules.

Change nothing else.
