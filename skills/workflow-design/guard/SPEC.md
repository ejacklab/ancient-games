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
  holds what they wrote. `writeEvidence` and `appendRecord` are the guard's own writers: they drop raw-content keys
  (`stdout`, `stderr`, `prompt`, `command`, `config` and the like) before writing.
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
  `target: 80` (a unit counts as covered only when `covered_by` holds a non-blank entry), and findings:
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

**`src/plugins/opencode.ts`** — default export `HarnessGuardPlugin: (ctx: { directory: string }) =>
Promise<{ "tool.execute.before": (input: { tool: string }, output: { args: { command?: string } }) => Promise<void> }>`;
the hook, for `input.tool === "bash"`, runs `lintCommand` on `output.args.command` with `repoRoot: guardRoot(ctx.directory)`
and `running: []` and **throws** an `Error` with the finding text on any fail finding. (Blocking by
throwing is *reported* by opencode's docs, not verified here.)

**`src/install.ts`** — `installSnippet(harness: "claude-code" | "codex" | "qwen" | "opencode", guardDir: string):
string`. Prints only; never writes a file. Claude Code / Codex / Qwen: the settings JSON for PreToolUse (Bash),
PostToolUse (Bash|Write|Edit|MultiEdit), PostToolUseFailure (Bash), Stop, SubagentStop, SessionStart, each
`{"type":"command","command":"bun <guardDir>/src/cli.ts hook claude"}`, with a first line saying which file it goes in
and that `.harness-guard/` belongs in `.gitignore`. opencode: the line that places `src/plugins/opencode.ts` in a
plugins folder. Codex and Qwen snippets say their payload match is reported, not verified.

**`src/doctor.ts`** — `doctor(opts: DoctorOptions): DoctorReport`, with
`DoctorOptions = { home: string; projectRoot: string; healthScript?: string | null; run?: (argv: string[]) => { code:
number; stdout: string } }` (tests pass a temporary `home` and `projectRoot`, and a fake `run`). Files read, per harness:
claude-code — `<home>/.claude/settings.json`, `<projectRoot>/.claude/settings.json`, `<projectRoot>/.claude/settings.local.json`;
codex — `<home>/.codex/hooks.json`, `<home>/.codex/config.toml`; qwen — `<home>/.qwen/settings.json`; opencode — the
files in `<home>/.config/opencode/plugin(s)/` and `<projectRoot>/.opencode/plugin(s)/`. `guard` is `installed` when a
read file's hook command (or, for opencode, a plugin file) contains `harness-guard`; `absent` when every file is missing
or readable without it; `unknown` when a file exists but cannot be read or parsed. `answers` is computed once
(`handleHook` on a planted `codex exec` PreToolUse payload must deny) and reported on every row. `health`: when
`healthScript` is given, `run(["python3", healthScript, "--json"])`; `ok` is exit 0 with JSON that parses;
`summary` is `"<n> findings"` from the JSON's `findings` array length, or the error kind — never the script's text.
Then: `doctor(opts): DoctorReport`: per harness, `guard: "installed" | "absent" | "unknown"` from the
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

## Round 3 — changes from the review and the measurements (these override earlier lines where they differ)

Sources: `runs/20261015-ts-hybrid/nodes/review-1.result.md` (R# = its row), the E1/E2/E4 measurements
(`effectiveness/`). Each item is a behaviour the tests must pin with the input given.

- **C1 (R1) Background calls are not checked on return.** PostToolUse / PostToolUseFailure skip the result check — no
  record, no output — when the recognised call's segment is `background`, or `tool_input.run_in_background` is true,
  or `tool_response.backgroundTaskId` is present. (Its result is not known yet.)
- **C2 (R2) Output flags and `>` are read outside quotes only.** `recognizeEngineCall` reads output flags and
  redirects from the segment's unquoted words; a `>` or `-o` inside a quoted prompt is prompt text. The failure record's
  `input` is `"<engine> call"` plus, when an output file was found, its **basename** — never other command text.
- **C3 (R5) The working folder of a call.** The hook resolves paths against `payload.cwd` when it is a string, else
  `env.cwd`; and when segments before the engine segment hold `cd DIR` (absolute or relative), against that folder.
  `ResultInput.cwd` is that resolved folder.
- **C4 (R20) A failure exit belongs to the engine only when the engine segment is the last one in its pipeline.**
  On PostToolUseFailure, when the engine segment is followed by `|` or `&&`/`||`/`;` and more segments, `exitCode` is
  `null` (the output checks still run).
- **C5 (R3) Insight files:** every `*.md` file under `.harness-guard/insights/` counts, whatever its name; under
  `runs/**`, files named `insight*.md`.
- **C6 (R4) Numbered lists:** after `Whys:` or `Options:`, blank lines are skipped until the first item; an item's
  indented continuation lines are joined to it; the list ends at the next unindented line that is not an item, or the
  next label, or the next heading.
- **C7 (E4) `Source:`** passes when its first word (letters and `-`) is one of the four; the rest of the line is detail.
- **C8 (R8) Malformed register entries:** a list item that is not a mapping is a `R13-malformed` fail finding naming
  its list and position; validation and coverage never throw on any YAML shape.
- **C9 (R19) A touched register that no longer exists** is skipped at Stop (no block).
- **C10 (R21) Raise check needs the field:** when the Stop payload has no `last_assistant_message` string, the raise
  check is skipped (the insight check still applies).
- **C11 (R11) A hook payload that is not JSON, or empty stdin,** is a quiet exit 0 with one stderr line — never exit 2.
- **C12 (R10) Agent records are stored as given:** `appendFailure` never redacts; only `writeEvidence` and
  `appendRecord` drop raw-content keys.
- **C13 (R17) Evidence may be a file or a folder** that exists.
- **C14 (R18) doctor health:** JSON that is not an object, or has no `findings` array, is `ok: false`,
  `summary: "unexpected JSON"` — never a throw.
- **C15 (R6) opencode install:** `installSnippet("opencode", guardDir)` prints the **content of a one-line plugin
  file** — `export { default } from "<guardDir>/src/plugins/opencode.ts";` — and the folder to put it in, so the
  installed file imports by absolute path.
- **C16 (R7) doctor opencode:** a plugin file counts as `installed` when its text contains `harness-guard` anywhere.
- **C17 (R9) Concurrency list:** the CLI drops only the hook's own process and its parent (by pid) from `running`,
  never by a text match.
- **C18 (R12) Heredocs** open with `<<` with or without a space before it (`cat<<EOF`, `x>f<<EOF`).
- **C19 (R13, E2) More segment starts:** backticks and `$(` … `)` also split segments; the shell words `do`, `then`,
  `else`, `elif`, `!` and `{` at the start of a segment are stripped like wrappers.
- **C20 (R14) codex stdin:** any input redirect — `< FILE`, `0<FILE`, `<<<` — satisfies the trap (`unless`).
- **C21 (R15, E1) opencode paths:** redirect targets (`>`, `>>`, `2>`, `&>`) are not paths opencode reads and never
  count; absolute paths **inside a quoted word** do count (a brief path in the prompt is the recorded trap 3), split
  on whitespace within the quotes.
- **C22 (R16) agy 502:** the trap matches `Bad Gateway` or `502` next to `HTTP`, `status` or `error` — not a bare
  `502` in other text.
- **C23 (E4) No duplicate:** the PostToolUse context line says the failure is already logged and gives its id, so the
  agent does not log it again: "harness-guard logged <ids> — already in the journal; do not log them again. An insight
  answering them is required before you stop."
- **C24 (E4 round 2) The Stop block names where to write.** The block reason for open failures says: write the
  insight to `.harness-guard/insights/<name>.md` (or `runs/<run>/insight.md` in a project with run folders), with the
  heading and parts listed — so the agent does not search for the location.

## Round 4 — the agent's own failures (R12.2: a failure is anything that went wrong, whoever caused it)

Facts this round rests on (verified once, Claude Code 2.1.300, `runs/20261015-ts-hybrid/evidence/n1b/`): a Bash call
that exits non-zero fires **PostToolUseFailure** with `error` = `"Exit code N\n<output>"`; a `grep` with no match fires
PostToolUse (Claude Code classes it as no error); a failed **Edit** fired no hook at all.

- **D1 Test runs that fail are failures.** A Bash segment whose command word (after the wrappers of M1) is a test runner
  — `pytest`, `python`/`python3 -m pytest`, `bun test`, `npm test`, `npm run test`, `yarn test`, `pnpm test`,
  `npx jest`, `npx vitest`, `go test`, `cargo test` — is a **test run**. It is a failure when PostToolUseFailure fires
  for it, or when PostToolUse fires and its stdout matches `\b[1-9]\d* (failed|errors?)\b` (a pipe can hide the exit)
  — stdout counts only when every segment after the test run is piped from it (`pytest | tail -3`); after `&&`, `;` or
  `||`, other commands write to the same stdout (found in long-session round 2).
  Record: `check: "R12.2-test-failed"`, `input: "<runner> run"`, `expected: "all tests pass"`, `actual`: the count of
  failed tests when the text gives one (`"3 failed"`), else `"exit <N>"` — never the output text. Evidence: the counts,
  the exit and the runner name.
- **D2 Other Bash calls that error are failures.** PostToolUseFailure for a Bash call that is neither an engine call
  (M1/M5 handle those) nor a test run: `check: "R12.2-command-error"`, `input: "<command word> call"`, `expected:
  "exit 0"`, `actual: "exit <N>"`. Skipped when `is_interrupt` is true (a person stopped it).
- **D3 Unknown paths are not checked.** An output path or a `cd` target that holds `$`, a backtick or a glob character
  (`*`, `?`, `[`) cannot be known from the text: the engine result check is skipped (no record) — never a
  `missing-output` failure. (Found live: `> $R/answer.txt` was logged as missing.)
- **D4 One context line per failure kind.** The PostToolUse / PostToolUseFailure context line names each new id and
  says it is already logged (as C23), and for D1/D2 adds: "your own failures count — answer them in the insight; one
  section may answer several ids with one cause".
- **D5 Not observable:** errors of non-Bash tools (Edit, Write, Read) fire no hook in 2.1.300; the agent logs them
  with `fail`. No code for them this round.

Fails-if: a failing `pytest` run (exit 1) has no record; `pytest -q | tail -3` showing "2 failed" with exit 0 has no
record; a passing test run has a record; `false` has no record; an interrupted call has a record; a `grep` with no match
(PostToolUse) has a record; a record holds test output text; `codex exec x -o $OUT/r.md </dev/null` with no such file
logs `missing-output`.
- **D6 Raise once.** When a Stop finds every pending failure of the session answered and the final message names the
  insight file(s), it writes a `raised` record (`{kind: "raised", time, session, ids}`) for those failures; a later Stop
  asks to name only failures not yet raised. (Found live: the guard asked this session to repeat the insight path at
  every stop.)
