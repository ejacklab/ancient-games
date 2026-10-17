## F-60cad515 — read Linus's answer file after his run had failed

Whys:
1. `sed -n … experts-p3-strengthen/answers/linus.md` exited 2: the file did not exist.
2. It did not exist because Linus's run failed: Codex answered "You've hit your usage limit … try again at 3:16 AM" and exited 1 after 4 s.
3. I read the answer files without first gating on the run: `four_experts.py run` returns 1 when an asked expert is not ok (`four_experts.py:202`), but my command ended in `; tail …`, so the background task reported exit 0.
4. `status.json` records the failure as `problem: "empty answer"`, which hides the engine's own error line (the usage limit), so even the status read did not say why.
5. The four-experts skill orders run → check, but does not say to read nothing from `answers/` until `check` (or `status.json`'s `ok`) has passed for that expert.

Source: tool — `four_experts.py` reports an engine error (usage limit) as "empty answer"; and my command shape masked its exit code.
Root cause: `four_experts.py` collapses an engine's error output into "empty answer", and my `run …; tail` call discarded the run's non-zero exit.

Options:
1. [tool] In `four_experts.py`, when an engine exits non-zero with no answer, put the engine log's last `ERROR:` line in `status.json` `problem` (for example "usage limit until 3:16 AM"). evidence: experts-p3-strengthen/status.json linus `problem: "empty answer"`; experts-p3-strengthen/logs/linus.log shows "You've hit your usage limit".
2. [rule] Before reading any `answers/<id>.md`, read `status.json` and skip every expert whose `ok` is false; run the engine call with `set -o pipefail` or without a trailing `; tail` so its exit code survives. evidence: `four_experts.py:202` returns 1 when an expert fails; the task wrapper reported exit 0.
3. [check] Before a step that needs Codex, probe its quota with `codex exec -s read-only "Say OK." </dev/null` and stop on an `ERROR:` line. evidence: the probe at 2026-10-15T17:39Z returned the usage-limit error in under 5 s.

## F-d325a7cc — R3's round check saw files change under code_map/ during the run

Whys:
1. The held-out set reported "Tool changed files under root or working directory" for R3 (`p3/R3-ar1-interference/`).
2. The changed files were `code_map/node_modules/.cm-round-dsh/report.*` and `.cm-round-opencode/report.*`: the
   two A1 builders' evaluator output.
3. The builders wrote there because my A1 briefs told them to use `--out node_modules/.cm-round-<engine>`, a path I
   picked so that opencode's permission check would not reject it.
4. Each build copy's `node_modules` is a link to `code_map/node_modules`, so the copies' writes landed inside the
   code_map folder that the R3 check was watching.
5. I ran builds in copies alongside round checks to fit the time box, and treated the copies as separate without
   checking what they share through links.

Source: the COO's brief and setup (method 3.7: parallel only when the units share no state).
Root cause: the build copies share `node_modules` with `code_map/` through a link, and the briefs pointed writes into
it.

Options:
1. [rule] A build brief puts every output inside its own copy and never into `node_modules/`. evidence: the L1, A1
   round-2 and A2 round-2 briefs say "Never write into node_modules/" and write `--out <name>-scratch` inside the
   copy; the later checks saw no interference. **Applied.**
2. [check] `round_check.py` lists `code_map/node_modules/.*` folders that are not packages, before and after, and
   fails the run on a change there with "another job wrote into code_map". evidence: the R3 report's `changedFiles`.
3. [rule] Run no round check while a build copy that links into `code_map/` is running. evidence: the A3, L1 and A1
   checks ran beside builds and passed or failed for real reasons; only R3 caught the writes.

## F-f91899ca — a private case expected a call one level too deep

Whys:
1. `OC-M1-callees-attempt` stayed NOT MET for both A1 builds.
2. It expected step.ts:94 among `attempt`'s direct callees.
3. Line 94 is inside `const executeTool = (call) => {...}`, a named arrow. By the spec's rule (the nearest function,
   method or arrow), that call belongs to `executeTool`, one level below.
4. I wrote the case on 2026-10-15 from the answer key's claim about the chain, without applying that rule to each
   expected site.

Source: the COO's case file (private).
Root cause: the expected sites were copied from a reading of the chain, not checked against the spec's
enclosing-function rule.

Options:
1. [rule] Before a private case is used, check each expected `callees` site by hand against the nearest enclosing
   function, and record the check in the case file. evidence: the corrected case expects step.ts:126 (the call to
   `executeTool`), and the old file is kept as `core.v2.json`. **Applied to this case.**
2. [check] Run the tool once on each new case, and read every expected site the tool misses before counting it as a
   tool fault. evidence: reading the A1 failure is how this was found. It was also the second COO case error, after
   `OC-M2-edit-to-assert` on 2026-10-15.
