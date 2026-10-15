# harness-guard — specification

The code half of the harness-health hybrid: checks that need no judgment, run at fixed points (harness hooks, a
plugin, a CLI the method's steps call), so an agent cannot skip them once the guard is installed. The judgment half —
writing use cases, fails-if conditions, six whys, fix options — stays with the agent; the guard checks that it was done
and has the required shape.

Runtime: **bun ≥ 1.4, TypeScript, no npm dependencies** (`bun:test` for tests, `Bun.YAML.parse` for YAML,
`node:fs`, `node:path`, `node:os`, `node:crypto`, `node:child_process` only). Generic: no project name, no absolute path, no
user name in code or data. Never prints a secret: the journal and the outputs hold lengths, counts, ids, trap ids and
paths — never raw stdout, stderr, prompts or config values.

Types shared by every module are in `src/types.ts` (fixed; do not change them — if a type is wrong, say so in your
result instead). Each module below lists its exports and its behaviour; each **Fails-if** line is a behaviour the
tests must pin down with a planted input.

## Common

- `Finding = { rule: string; severity: "fail" | "warn"; message: string; fix?: string; ref?: string }`.
  `rule` is a stable id (e.g. `R12.1-empty-output`, `trap:codex-stdin`). `fail` means the guarded thing is wrong;
  `warn` means report only.
- `guardRoot(cwd)` (in `journal.ts`): the git top-level of `cwd` (`git rev-parse --show-toplevel`, run with a 5 s
  timeout); if git fails, `cwd` itself.
- All guard state lives under `<root>/.harness-guard/` (the package's install advice tells the owner to gitignore it).

## M1 — `src/traps.ts`: trap catalogue, engine-call recognition, result check (R12.1)

Data files, YAML, in `data/`: `traps.yaml` and `engines.yaml` (shapes in `src/types.ts`: `Trap`, `EngineSpec`).

**Segments (added in round 2, after the replay of 3,677 past commands found 31 false denies in 37 — the lint read
the whole Bash string).** `recognizeEngineCall` and `lintCommand` work on **segments**, never on the raw string:
- `segments(command: string): Segment[]` (exported; `Segment = { text: string; background: boolean; piped: boolean }`):
  1. Heredoc bodies are removed first: after a line holding `<<WORD`, `<<'WORD'`, `<<"WORD"` or `<<-WORD`, every
     line up to and including the line that is exactly `WORD` (leading tabs allowed for `<<-`) is dropped.
  2. The rest is split into simple commands at newlines, `;`, `&&`, `||`, `|`, a single `&`, `(` and `)` — **outside
     single and double quotes only**. A `&` that is part of a redirection (`2>&1`, `>&2`, `&>file`) is not a separator.
  3. Each simple command is trimmed; empty ones are dropped. Its text keeps its own redirections (`</dev/null`,
     `> out.md`), so `unless` and output redirects are read from the segment.
  4. `piped` is true when the separator right before the segment is `|` (its stdin comes from a pipe).
  5. `background` is true when the separator right after the segment is a single `&`, or the segment is inside a
     `( … )` group whose `)` is followed by a single `&`.
- **The command word.** Before matching, leading wrappers are stripped from a segment's text: `NAME=value`
  assignments, `timeout` with its options and duration, `env` with `-u NAME`, `-i` and `NAME=value` words, `nohup`,
  `time`, `exec`, `command`, and a `runlog.py … --` wrapper (everything up to and including the first standalone
  `--` when the command word ends in `runlog.py`, with or without `python3` before it). What remains starts at the
  command word, and **the `command` regexes in `data/` are anchored to it (`^`)**.
- A segment holding a standalone `--help`, `-h`, `--version` or `-V` word starts no session: it is never an engine
  call and never a command-trap hit.
- `paths_outside_repo` reads path tokens of the **matching segment only**.
- `concurrent` still reads `ctx.running` (whole command lines of other processes) with the trap's regex **unanchored**.

Exports:
- `loadTraps(path?: string): Trap[]` and `loadEngines(path?: string): EngineSpec[]` — default to the package's
  `data/` files. A malformed entry is skipped and reported by `catalogueProblems(path?)`: `string[]`.
- `recognizeEngineCall(command: string, engines?: EngineSpec[]): EngineCall | null`
  - Matches the first segment (in order) whose stripped text matches an `EngineSpec`'s `command` regex; `null` if none.
    Output flags, redirects and `background` are read from that segment.
  - `outputFile`: the value after any of the spec's `output_flags` (`-o FILE`, `-o=FILE`, `--out FILE`), else the
    target of a stdout redirect `> FILE` or `>> FILE` (not `2>`); quotes stripped; `null` if none.
  - `stdoutIsAnswer`: from the spec, but `false` when `outputFile` came from a redirect (the answer went to the file).
  - `statusFile`: for specs with `status_from_out_dir: true` (a wrapper such as `four_experts.py run --out DIR`),
    `DIR/status.json`; else `null`. For such a wrapper `outputFile` is the folder `DIR` itself.
  - `background`: the matching segment's `background`. (A caller that knows more passes `LintContext.background` to
    `lintCommand`.)
- `lintCommand(command: string, ctx: LintContext, traps?: Trap[]): Finding[]` — command traps only, **approved**
  entries only (a `proposed` entry never produces a finding). A trap hits on a segment when its `command` regex matches the
  segment's stripped text **and** its `unless` regex (if any) does not match the segment's text **and** each extra condition it sets holds:
  - `unless_piped: true` → no hit when the segment's `piped` is true (its stdin is already fed);
  - `background: true` → `ctx.background` or the segment's `background`;
  - `concurrent: true` → `ctx.running` (command lines of other running processes) holds a line matching the trap's
    `command` regex;
  - `paths_outside_repo: true` → some absolute path token in the command (a word starting with `/`, quotes stripped,
    ignoring `/dev/null`, `/dev/stdin`, `/dev/stdout`, `/dev/stderr`, `/tmp/…` is **not** ignored) resolves outside
    `ctx.repoRoot`.
  - When a trap sets more than one of `background` / `concurrent`, either one is enough (they are alternatives); every
    other condition must hold.
  - Each hit → `{ rule: "trap:<id>", severity: "fail", message: why, fix, ref: source }`.
- `checkResult(input: ResultInput): Finding[]` — after an engine call:
  - `exitCode` not null and not 0 → `R12.1-exit` (fail); 124 → `R12.1-timeout` (fail) instead.
  - `interrupted` true → `R12.1-interrupted` (fail).
  - When `call.statusFile` is set, the status file is the output check (the wrapper's `outputFile` is a folder):
    skip the two output-file checks below.
  - `call.outputFile` set and the file does not exist → `R12.1-missing-output` (fail); exists but has no
    non-whitespace content → `R12.1-empty-output` (fail).
  - no `outputFile`, `call.stdoutIsAnswer` true, and stdout has no non-whitespace content → `R12.1-empty-output`.
  - each approved **result** trap for `call.engine` (or `engine: any`) whose `stderr` regex matches stderr, or whose
    `output_empty: true` holds → `trap:<id>` (fail).
  - each spec `silent_failures` entry (`{ text, status }`) found in stderr → `R12.1-silent-<status>` (fail).
  - `call.statusFile` set: the file is missing → `R12.1-missing-status` (fail); for each entry whose `ok` is false →
    `R12.1-wrapped-fail` (fail) naming the entry key (not its content).
  - A clean call returns `[]`.
  - Paths are resolved against `input.cwd`.

Fails-if: a `codex exec` command without a stdin redirect passes the lint; `codex exec --help`, `pgrep -f "codex exec"`,
a `grep` pattern or `echo` text naming an engine, or a heredoc body naming one, is flagged or recognised; a codex call
after `timeout 60`, `env -u X` or `runlog.py … --` is not recognised; an absolute path that belongs to another command
on the same line makes an `opencode run` hit; a proposed **result** trap produces a finding; one with `</dev/null` is flagged; a
`proposed` trap produces a finding; an `opencode run` naming a path outside the repo passes; a second `opencode run`
while one runs passes; an empty output file, a missing output file, a non-zero exit, or an "auto-denied" stderr from agy
passes `checkResult`; a clean call produces a finding; a malformed catalogue entry crashes the loader.

## M2 — `src/journal.ts`: failure journal (R12.2)

Journal: `<root>/.harness-guard/journal.jsonl`, one JSON object per line, append-only. Evidence written by the guard:
`<root>/.harness-guard/evidence/<id>.json`.

Exports:
- `guardRoot(cwd: string): string` (see Common).
- `newFailureId(): string` → `F-` + 8 lowercase hex characters (random).
- `validateFailure(rec: unknown, root: string): string[]` — problems; empty when valid. Required: `kind: "failure"`,
  `id` in the `F-xxxxxxxx` form, `time` (ISO 8601), `session` (non-empty string; `"none"` allowed), `found_by`
  (non-empty), `check`, `input`, `expected`, `actual` (non-empty strings), `engine` (non-empty; `"none"` allowed),
  `harness` (non-empty), **`reason` (non-empty after trim)**, **`evidence` (a path that exists, relative to `root` or
  absolute)**. Unknown extra fields are allowed.
- The journal stores the strings it is given. The "no raw content" rule of Common binds the guard's **own** writers (M5
  builds its records from fixed phrases, ids, lengths and paths); a record an agent or the owner writes through the CLI
  holds what they wrote.
- `appendFailure(root: string, rec: FailureRecord): FailureRecord` — validates (throws `JournalError` listing the
  problems if invalid), creates folders as needed, appends one line. Returns the record.
- `appendRecord(root: string, rec: TouchedRecord | GuardErrorRecord): void` — for the other kinds (no evidence check).
- `writeEvidence(root: string, id: string, facts: Record<string, unknown>): string` — writes the evidence JSON and
  returns its path **relative to root**.
- `readJournal(root: string): { records: JournalRecord[]; badLines: number }` — a missing journal is empty; a line that
  is not valid JSON is counted in `badLines` and skipped, never thrown.
- `failuresFor(root: string, session: string | null): FailureRecord[]` — all failures, or only one session's.
- CLI helper `recordFailureFromArgs(root, args)` used by `cli.ts fail` (flags: `--check --input --expected --actual
  --reason --evidence --found-by --engine --harness --session`); missing `--reason` or `--evidence` is an error, not a
  default.

Fails-if: a record with no reason, an empty reason, no evidence, or an evidence path that does not exist is accepted; a
bad line crashes `readJournal`; two appends lose a line; a guard-found record has no evidence file.

## M3 — `src/insight.ts`: insight gate (R12.3)

An insight file is Markdown at `runs/**/insight*.md` (`**` matches zero or more folders, so `runs/insight.md` counts)
or `.harness-guard/insights/*.md` under the root. M3's functions take `root` as given (the caller has already applied
`guardRoot`). It answers
failures by sections: a `##` heading that contains one or more failure ids (`## F-1a2b3c4d` or
`## F-1a2b3c4d, F-5e6f7a8b — short title`). Inside a section, these labelled parts (label at the start of a line,
case-insensitive):
- `Whys:` then a numbered list (`1.` …) of **3 to 6** items.
- `Source:` one of `instruction`, `check`, `tool`, `config` (the changeable source the whys end at).
- `Root cause:` non-empty text on the same line or the next non-empty line.
- `Options:` then a numbered list of **2 or 3** items; each item starts with a kind in brackets — `[rule]`,
  `[check]`, `[tool]` or `[config-advice]` (any other bracketed kind, e.g. `[policy]`, is `R12.3-option-kind`) — and
  contains `evidence:` followed by non-empty text.

Exports:
- `findInsightFiles(root: string): string[]` — relative paths, sorted.
- `parseInsight(text: string): InsightSection[]`.
- `checkSection(s: InsightSection): Finding[]` — `R12.3-whys-count`, `R12.3-source`, `R12.3-root-cause`,
  `R12.3-options-count`, `R12.3-option-kind`, `R12.3-option-evidence` (all fail); plus the heuristic
  `R12.3-why-ends-at-person` (**warn**) when the last why reads as "forgot", "careless", "I missed" or "the model was
  wrong" — a heuristic, labelled as one in its message.
- `answered(root: string): Map<string, string>` — failure id → the relative path of the first insight file holding a
  section for it **with no fail findings**.
- `openFailures(root: string, session: string | null): FailureRecord[]` — failures (that session's, or all) with no
  entry in `answered`.

Fails-if: a failure with no section, a section with 2 whys or 7, no source or an unknown one, no root cause, 1 option
or 4, an option with no kind or no evidence counts as answered; a valid section is not; a section answering two ids
does not answer both.

## M4 — `src/register.ts`: use-case register and coverage (R13, R11.1)

A register is YAML with top-level `register: 1` (shape `Register` in `src/types.ts`).

Exports:
- `loadRegister(path: string): Register` — throws `RegisterError` on YAML that does not parse or lacks `register: 1`.
- `isRegisterFile(path: string): boolean` — the file name ends `.register.yaml` or is `register.yaml`.
- `validateRegister(r: Register): Finding[]`:
  - `R13.1-no-decision` (fail): a use case or requirement with `origin: ai` and no `decision`, or a decision with no
    `by`.
  - `R13.2-missing` (fail): an **accepted** use case missing `purpose`, `fails_if` (≥1) or `min_acceptance` (≥1).
    A use case is accepted when `origin: user` and no decision says `declined`, or `origin: ai` with
    `decision.verdict: accepted`.
  - `R13.5-no-purpose` (fail): a requirement with no `purpose`, or no `serves` (≥1 id or `vision`).
  - `R13.5-not-binding` (warn): an AI requirement not accepted — excluded from units.
  - `R13.7-conflict-not-shown` (fail): a conflict without `shown_to_owner: true`.
  - `R13-unknown-ref` (fail): a `serves`, conflict or coverage entry naming an id that does not exist.
- `units(r: Register): Unit[]` — for each accepted use case: one unit per `fails_if` item (`<id>/f<n>`) and per
  `min_acceptance` item (`<id>/m<n>`), `safety` taken from the use case; for each accepted requirement: one per
  `fails_if` item (`<id>/f<n>`). Units whose normalised text (lower case, whitespace collapsed) repeats an earlier
  unit's are dropped (a variant does not add to the count).
- `freezeHash(units: Unit[]): string` — sha256 hex of the canonical JSON of `[id, text]` pairs in order.
- `coverage(r: Register): CoverageReport` — `total`, `covered` (units with ≥1 `covered_by`), `percent` (one decimal),
  `target: 80`, and findings:
  - `R11.1-not-frozen` (fail): `frozen` missing; `R11.1-frozen-mismatch` (fail): `frozen` ≠ `freezeHash(units(r))`
    — the units changed, so a new count must start.
  - `R11.1-basic-uncovered` (fail): a unit with no `covered_by` and no `skippable`.
  - `R11.1-skip-no-reason` (fail): `skippable` without a non-empty `reason`.
  - `R11.1-safety-skipped` (fail): a safety unit marked skippable.
  - `R11.1-below-target` (**warn**, never fail): `percent` < 80.

Fails-if: an AI case with no decision passes; an accepted case missing min_acceptance passes; a requirement with no
purpose passes; an unshown conflict passes; a variant case raises the percentage; an uncovered basic unit passes; a
skippable safety unit passes; below 80% is a fail; a changed unit list keeps its old freeze.

## M5 — `src/hooks.ts`, `src/plugins/opencode.ts`, `src/install.ts`, `src/doctor.ts`, `src/cli.ts`

**`handleHook(payload: unknown, env: HookEnv): HookResult`** — the Claude-protocol handler (Claude Code; the same
payload names are reported for Codex, Qwen and the dsh bridge). `HookEnv` supplies `cwd`, `running` (process command
lines) and `now`, so the handler is testable without a harness. Dispatch on `hook_event_name`:
- **PreToolUse**, `tool_name: "Bash"`: `lintCommand(tool_input.command, …)`. Any fail finding → stdout JSON
  `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"<rule>:
  <message> Fix: <fix>"}}` (all hits joined), exit 0. No hit → no output, exit 0.
- **PostToolUse**, `tool_name: "Bash"`: if `recognizeEngineCall` matches, `checkResult` with `tool_response.stdout`,
  `tool_response.stderr`, `tool_response.interrupted`, `exitCode: null`. Each fail finding → one failure record
  (`found_by: "guard"`, `session: session_id`, `harness: "claude-code"`, `check: <rule>`, `input`: the engine and the
  output path — never the command's prompt text, `expected`/`actual`: short fixed phrases, `reason`: the finding
  message, `evidence`: `writeEvidence` with lengths, exit, rule ids). Then stdout JSON `{"hookSpecificOutput":
  {"hookEventName":"PostToolUse","additionalContext":"harness-guard logged <n> failure(s): <ids> — <rules>. Log it in
  your report; an insight is required before you stop."}}`. No finding → no output.
  `tool_name` `Write`, `Edit` or `MultiEdit` with `tool_input.file_path` a register file → a `touched` record.
- **PostToolUseFailure**, `tool_name: "Bash"`: same as PostToolUse, with `exitCode` from a numeric `exit_code` /
  `exitCode` field if present, else 1 (the tool failed), stderr from `error` if a string.
- **Stop** (and **SubagentStop**): `open = openFailures(root, session_id)`.
  - `open` non-empty → stdout JSON `{"decision":"block","reason":"…"}` naming each open id and the insight format
    (heading with the id; Whys 3–6; Source; Root cause; Options 2–3 with kind and evidence). Blocks **every** time
    while open, whatever `stop_hook_active` says (R12.3 is MUST; the harness's own block cap is the loop guard).
  - else, if this session has failures and `last_assistant_message` does not contain the relative path of an insight
    file that answers them → block with reason "raise the insight: name <path> in your final message" (R12.3 raise).
  - else, each register file in this session's `touched` records → `validateRegister` + `coverage`; fail findings →
    block with them listed; warn findings → no block.
  - else no output, exit 0.
- **SessionStart**: open failures of **other** sessions in this root → `additionalContext` listing them (raise), else
  nothing.
- Anything else, or a payload that is not an object → no output, exit 0.
- An exception inside the handler → `HookResult` with exit 1, a one-line stderr message, and a best-effort
  `guard_error` record. (Fail-open: a guard bug must not freeze the agent, and it is recorded.)

`HookResult = { exitCode: number; stdout: string; stderr: string }`.

**`src/plugins/opencode.ts`** — default export an opencode plugin: `tool.execute.before` for the bash tool runs
`lintCommand` on `output.args.command` and **throws** an `Error` with the finding text on any fail finding. (Blocking by
throwing is *reported* by opencode's docs, not verified here.)

**`src/install.ts`** — `installSnippet(harness: "claude-code" | "codex" | "qwen" | "opencode", guardDir: string):
string`. Prints only; never writes a file. Claude Code / Codex / Qwen: the settings JSON for PreToolUse (Bash),
PostToolUse (Bash|Write|Edit|MultiEdit), PostToolUseFailure (Bash), Stop, SubagentStop, SessionStart, each
`{"type":"command","command":"bun <guardDir>/src/cli.ts hook claude"}`, with a first line saying which file it goes in
and that `.harness-guard/` belongs in `.gitignore`. opencode: the line that places `src/plugins/opencode.ts` in a
plugins folder. Codex and Qwen snippets say their payload match is reported, not verified.

**`src/doctor.ts`** — `doctor(opts): DoctorReport`: per harness, `guard: "installed" | "absent" | "unknown"` from the
key names of its settings (a hook command containing `harness-guard`; values never printed), and `answers: true|false`
from calling `handleHook` in-process on a planted PreToolUse trap payload (it must deny); plus, when a
`harness_health.py` path is given and runs, its JSON summary counts. Markdown output.

**`src/cli.ts`** — `bun src/cli.ts <command>`: `hook claude` (stdin → `handleHook` → stdout/stderr/exit), `lint
<command…>`, `result --engine E --out FILE [--exit N] [--stderr-file F]`, `fail <flags>`, `insight [--session S]`
(lists open failures and invalid sections; exit 1 if any open), `register <file>` (validate + coverage; exit 1 on a fail
finding), `install --print <harness>`, `doctor [--health PATH]`. Exit codes: 0 ok, 1 findings, 2 usage.

Fails-if: a catalogued trap command is allowed; a clean command is denied; an empty engine output writes no record or
writes one without evidence; a good call writes a record; Stop lets a session with an unanswered failure end, or blocks
a session with none; Stop lets the agent end without naming the insight; a touched register with a fail finding passes
Stop; `install --print` writes a file; a handler exception freezes the agent (exit 2) or crashes without output.
