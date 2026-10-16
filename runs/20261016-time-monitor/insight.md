# Insight — run 20261016-time-monitor (time-boxed, 60 min)

## F-173e0190 — Dave's Claude call got no prompt

Whys:
1. Why was a failure logged? Dave's answer was empty after 2 s; the log says "Input must be provided either through stdin or as a prompt argument when using --print".
2. Why no prompt? The runner built `claude -p … --allowedTools Read,Grep,Glob <prompt>`; `--allowedTools` takes several values, so it took the prompt as one more tool name.
3. Why did this not show before? Earlier runs used `--claude-by-caller` (the main agent ran Dave as a subagent), so the runner's own Claude command was not exercised; this run was the first to call it from the runner.
4. Why did nothing catch it? The runner has no test that runs each engine's command shape, and its fallback logic only covers agy.
Source: tool — `.claude/skills/four-experts/scripts/four_experts.py` `command()` for claude.
Root cause: a variadic CLI flag placed before the positional prompt, in a code path no run had exercised.
Options:
1. [tool] Use `--allowedTools=<list>` so the prompt stays positional — done; Dave's rerun answered in 52 s (`nodes/experts.progress.md`). evidence: `experts/logs/dave.first-run.log` vs `experts/answers/dave.md`.
2. [check] A test that builds each engine's command and asserts the prompt is the last argument and no variadic flag precedes it without `=`. evidence: the four-experts skill has no tests in `tests/`.
3. [rule] A runner path is canary-proved (one cheap call) before a run depends on it (method 3.1 readiness). evidence: the agy and opencode paths were proved; the runner's claude path was not.

## F-84636a96 — Laozi wrote 為 where his list has 爲

Whys:
1. Why was a failure logged? The four-experts check found 以約為紀 in Laozi's answer; the list has 以約爲紀.
2. Why the difference? 為 and 爲 are two forms of the same character; the engine (opencode, MiniMax) normalised to the common form.
3. Why does the check fail it? It compares 4+ character runs exactly, by design, so an invented quote cannot pass; it reports the nearest passage so a variant reads differently from an invention.
4. Why does the brief not prevent it? It says "quote only from your list, exactly as written", but gives no reason the forms matter.
Source: instruction — the experts' brief (`assets/brief.md`, "Quote only from your list, exactly as it is written there").
Root cause: an engine normalised a variant character in a quote, and the exact-match check is right to flag it — the quote is not verbatim.
Options:
1. [rule] The brief adds: "copy Chinese quotes character by character from the list; do not normalise variant forms (爲/為, 於/于)". evidence: the check output names a 1-character variant.
2. [check] The check reports a known-variant-only difference as `warn`, not `fail`, with the pair named, so a variant never blocks while an invention still does. evidence: `experts/check.txt` already computes the differing characters.
3. [tool] The runner pastes the list's quotes into the brief instead of a path, so the engine copies them from its own context. evidence: opencode read the list by path.
