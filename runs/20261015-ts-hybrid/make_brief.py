#!/usr/bin/env python3
"""Write one node brief for the harness-guard build (run 20261015-ts-hybrid). The COO's helper, not a product file.
Usage: make_brief.py NODE ATTEMPT [--feedback FILE]   — NODE like m1-tests or m1-code."""
import pathlib
import sys

RUN = "runs/20261015-ts-hybrid"
PKG = "tools/harness-guard"
MODULES = {
    "m1": ("M1", "src/traps.ts", "test/traps.test.ts", "traps, engine-call recognition, result check"),
    "m2": ("M2", "src/journal.ts", "test/journal.test.ts", "failure journal"),
    "m3": ("M3", "src/insight.ts", "test/insight.test.ts", "insight gate"),
    "m4": ("M4", "src/register.ts", "test/register.test.ts", "use-case register and coverage"),
    "m5": ("M5", "src/hooks.ts, src/plugins/opencode.ts, src/install.ts, src/doctor.ts, src/cli.ts",
           "test/hooks.test.ts, test/cli.test.ts, test/doctor.test.ts, test/plugin.test.ts", "hook adapters, install, doctor, CLI"),
}
ENGINE = {"m1-code": "opencode", "m1-tests": "codex", "m2-code": "opencode", "m2-tests": "codex",
          "m3-code": "opencode", "m3-tests": "opencode", "m4-code": "opencode", "m4-tests": "codex",
          "m5-code": "opencode", "m5-tests": "codex"}

RESULT = """Write the result file `{run}/nodes/{node}-{attempt}.result.md` (write to `{node}-{attempt}.result.tmp` first, then
rename it). It starts with this header, then the body:

```
---
node: {node}
attempt: {attempt}
engine: {engine}
model: <the model as your tool reports it>
status: ok | fail | partial
started: <UTC time>
ended: <UTC time>
evidence: {run}/nodes/{node}-{attempt}.evidence.txt
---
<first line: the answer in one sentence>
- Files written: <paths>
- Check: <the command you ran and its last lines, e.g. "12 pass, 0 fail">
- CONTRADICTS: <each place SPEC.md or src/types.ts contradicts itself or cannot be met, with the line; or "none">
```

Put the full output of every check you ran in the evidence file. No reasoning in the body."""


def brief(node: str, attempt: str, feedback: str | None) -> str:
    mod, kind = node.split("-")
    label, src, tests, what = MODULES[mod]
    engine = ENGINE[node]
    deps = {"m1": "", "m2": "", "m3": "`src/journal.ts` (M2, done)", "m4": "",
            "m5": "`src/traps.ts`, `src/journal.ts`, `src/insight.ts`, `src/register.ts` (M1–M4, done)"}[mod]
    common_ctx = f"""- `{PKG}/SPEC.md` — the specification. Read the **Common** section and the **{label}** section in full.
- `{PKG}/src/types.ts` — the shared types. Fixed: import them, never redefine or change them.
- `{PKG}/data/traps.yaml`, `{PKG}/data/engines.yaml` — the catalogues (read-only).
- Runtime: bun 1.4.3, TypeScript, **no npm dependencies** (`bun:test`, `Bun.YAML.parse`, `node:*` modules only).
- Style: match `{PKG}/src/types.ts` — short comments, plain names.""" + (f"\n- Already built and tested: {deps}. Use it; do not change it." if deps else "")
    if kind == "tests":
        task = f"""Write the acceptance tests for module {label} ({what}) in `{PKG}/{tests}`, from SPEC.md alone. The
implementation (`{PKG}/{src}`) does not exist yet and is written afterwards by a different engine to pass your tests,
so your tests are the standard it is judged by. Do not write the implementation."""
        standard = f"""- Every **Fails-if** line of the {label} section is pinned by at least one test that plants the wrong input and
  asserts the right outcome; every export listed in {label} is called by at least one test with the exact signature
  SPEC.md gives. Name each test after the behaviour (e.g. `"lint: codex exec without a stdin redirect is a trap"`).
- Tests build their own fixtures in a temporary folder (`fs.mkdtempSync(path.join(os.tmpdir(), "hg-"))`), never in the
  repository; a test that needs a git repository creates one with `git init` in the temp folder.
- Import from the module path exactly as SPEC.md names it (e.g. `import {{ lintCommand }} from "../src/traps.ts"`).
- A test may not depend on the machine (user name, home folder, installed engines, running processes) — pass
  everything through the function arguments SPEC.md defines (`LintContext.running`, `HookEnv`, …).
- Planted secrets: where a function writes or prints anything, one test plants the string `SECRET-PLANT-7f3a9c` in the
  input and asserts it never appears in the output, the journal or an evidence file.
- Check you run: `cd {PKG} && bun test {tests}` — it must run (load) and fail **only** because `{src}` is missing
  (report the exact error). Also `./node_modules/.bin/tsgo --noEmit -p .` will report the missing module; any other
  type error in your test file must be fixed."""
        may = f"`{PKG}/{tests}` and new files under `{PKG}/test/fixtures/` only"
    else:
        task = f"""Implement module {label} ({what}) in `{PKG}/{src}` so that its acceptance tests pass. The tests in
`{PKG}/{tests}` were written by a different engine from SPEC.md and are frozen: you must not change them."""
        standard = f"""- `cd {PKG} && bun test` — every test passes (all modules built so far, not only yours).
- `cd {PKG} && ./node_modules/.bin/tsgo --noEmit -p .` — exit 0, no type errors.
- Behaviour follows SPEC.md, not only the tests: where a test and SPEC.md disagree, do not bend the code to the test —
  stop and report it under CONTRADICTS with the test name and the SPEC line.
- No secret or raw command/prompt text in anything the module writes or prints (the tests plant `SECRET-PLANT-7f3a9c`).
- No new dependency; no change to `package.json`, `tsconfig.json`, `SPEC.md`, `src/types.ts`, `data/`, or any test."""
        may = f"`{PKG}/{src}` only" + (" (and new helper files under `src/` that only it imports)" if mod != "m5" else " (and new helper files under `src/`)")
    fb = ""
    if feedback:
        fb = "\n## Feedback from the previous attempt (the check's real output)\n\n" + pathlib.Path(feedback).read_text() + "\n"
    return f"""# Brief — {node}, attempt {attempt}

You are working in a git worktree; the current folder is the repository root. Work only inside it.

## Task (one deliverable)

{task}

## Context (only what this task needs)

{common_ctx}
- Withheld on purpose: {"the implementation (it does not exist)" if kind == "tests" else "nothing — but the tests' author's reasoning is not given; the tests and SPEC.md are the whole contract"}.
{fb}
## Standard (how it will be judged)

{standard}

The COO will re-run every check you report, and will plant wrong inputs of its own.

## Limits

- May change: {may}; plus the result and evidence files below.
- Must not change: anything else. Do not commit; do not run `git` commands that change the repository.
- Do not start any other AI engine or agent. Do not read or print files outside the repository.

## Write the result to

{RESULT.format(run=RUN, node=node, attempt=attempt, engine=engine)}
"""


if __name__ == "__main__":
    node, attempt = sys.argv[1], sys.argv[2]
    fb = sys.argv[sys.argv.index("--feedback") + 1] if "--feedback" in sys.argv else None
    out = pathlib.Path(RUN) / "briefs" / f"{node}-{attempt}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(brief(node, attempt, fb))
    print(out)
