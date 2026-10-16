# Insight — run 20261016-six-experts (plan B)

## F-5c21dd69 — my new insight-index.ts did not typecheck

Whys:
1. Why was a failure logged? `tsgo --noEmit` exited 2: `heading.match(ID_RE) ?? []` is typed `RegExpMatchArray | never[]`, and `includes(id)` on it rejected a string.
2. Why did I write it that way? I copied the pattern from `insight.ts`, where the same expression is assigned to a variable already typed `string[]`.
3. Why did the copy lose the type? In the new code the result went into a `const` with no annotation, so TypeScript inferred the union.
4. Why was it caught only at the type check? I wrote the module in one go and ran tsgo after, as the build pattern says — the check did its job.
Source: tool — TypeScript's inference of `?? []` as `never[]`; caught by the type check, as designed.
Root cause: a copied expression lost its declared type, so the empty-array fallback was inferred as never[].
Options:
1. [rule] An empty-array fallback is always written with its type (`const ids: string[] = x ?? []`). evidence: the fix was that one annotation.
2. [check] Keep running tsgo before any test, as now; it caught this in one step. evidence: `tsgo` exit 2, then clean after the fix.

## F-7f938bdf — my question sent opencode experts to a file outside the repo

Whys:
1. Why was a failure logged? Linus (28 bytes) and Laozi (empty) on opencode gave no answer; both ended with exit 0.
2. Why? Each tried to read `~/.claude/plans/six-experts-dave-insights.md`, named in my question; opencode auto-rejected it ("external_directory … auto-rejecting") and the run ended.
3. Why did my question name that path? I pointed at the plan where it lives instead of copying it into the run folder.
4. Why was the known trap not applied? My memory says opencode rejects files outside the repo ("copy inputs in"), but nothing checks a question file's paths before the runner starts.
Source: check — nothing checks that the paths a question names are inside the repo before an opencode expert reads it.
Category: spec
Root cause: an input outside the repo, in a question to an engine that silently rejects such paths, with no pre-flight check.
Options:
1. [check] six_experts.py run refuses (or copies in) any path in the question file that lies outside the working directory, before starting opencode experts. evidence: both failures read `~/.claude/plans/…`; the rerun with `runs/…/plan.md` did not.
2. [tool] The runner adds to opencode's prompt: "if a file is refused, say so in the answer" so a rejection is visible instead of an empty answer. evidence: the log shows the rejection, the answer does not.
3. [rule] A question file names only paths inside the run folder; plans and notes are copied in first. evidence: memory `opencode-parallel-db-lock` already says "copy inputs in".

## F-b696193d — I changed start()'s signature and broke the other session's quota tests

Whys:
1. Why was a failure logged? The Python suite failed 4 tests in `tests/test_six_experts_codex_quota.py`: `fake_start() takes 8 positional arguments but 9 were given`.
2. Why? I added a 9th parameter (`model`) to `start()` and passed it positionally on every call, including Linus's.
3. Why did that reach the tests? The quota tests replace `start` with an 8-argument fake; I had run them before the change (8/8) and not after.
4. Why not after? I ran only the new runner tests and the guard suite after the Dave/Dario edit, not every test that patches `start`.
Source: instruction — the main agent's habit of running only the tests it just wrote after changing a shared function's signature.
Category: own-work
Root cause: a shared function's signature changed without running every test that replaces it.
Options:
1. [rule] After changing a function's signature, grep the tests for the name (`start`, `fake_start`) and run those before anything else. evidence: one grep finds `tests/test_six_experts_codex_quota.py`.
2. [tool] Pass optional parameters by keyword and only when set (`**seat_model(...)`), so existing callers and fakes keep their shape — done. evidence: 31/31 after the change.
3. [check] The runner's tests include one that calls `start` through a strict 8-argument fake, so a widened signature fails there first. evidence: the quota tests did exactly that, by accident.
