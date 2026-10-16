// M5: the Claude-protocol hook handler (SPEC.md M5). One handler serves every harness: PreToolUse denies a
// catalogued command trap, PostToolUse logs an engine call that answered nothing, PostToolUseFailure logs the agent's
// own failures (round 4, D1 and D2), Stop blocks while a failure has no insight. Nothing here prints a prompt,
// stdout, stderr or config value: only ids, rules, lengths and paths.

import { createHash } from "node:crypto";
import * as fs from "node:fs";
import * as path from "node:path";
import { checkCriteria, isCriteriaFile, loadCriteria, score } from "./criteria.ts";
import { appendFailure, appendRecord, failuresFor, guardRoot, newFailureId, readJournal, writeEvidence } from "./journal.ts";
import { answered, greatAnswered, openFailures } from "./insight.ts";
import { findPathFiles, loadPath } from "./paths.ts";
import { coverage, isRegisterFile, loadRegister, validateRegister } from "./register.ts";
import { checkResult, commandWord, engineCallSite, lintCommand, recognizeTestRun, segments } from "./traps.ts";
import type { Finding, GuardErrorRecord, HookEnv, HookResult, PromptRecord, TouchedRecord, RaisedRecord, SuccessRecord } from "./types.ts";

const HARNESS = "claude-code";
const NO_SESSION = "none";
const WRITE_TOOLS = new Set(["Write", "Edit", "MultiEdit"]);

const QUIET: HookResult = { exitCode: 0, stdout: "", stderr: "" };

const INSIGHT_FORMAT = [
  "Write the insight to .harness-guard/insights/<name>.md (any name ending .md), or to runs/<run>/insight.md in a",
  "project with run folders — one ## heading per failure id, and inside it:",
  "  ## F-xxxxxxxx — short title",
  "  Whys: 3–6 numbered items, ending at the instruction, check, tool or config.",
  "  Source: one of instruction, check, tool, config (the first word decides; the rest is detail).",
  "  Root cause: one line naming that changeable source.",
  "  Options: 2–3 items, each starting with a kind ([rule], [check], [tool] or [config-advice]) and ending with evidence: <path or fact>.",
];

// The context line says the failure is in the journal already, so the agent does not log it a second time (round 3, C23).
const ALREADY_LOGGED = "already in the journal; do not log them again. An insight answering them is required before you stop.";

// A failure the agent caused is answerable like any other, and one section may answer several of them (round 4, D4).
const OWN_FAILURES = "your own failures count — answer them in the insight; one section may answer several ids with one cause.";

// The format an unanswered failure is told to use.
function insightReason(ids: string[]): string {
  return [
    `harness-guard: ${ids.length} logged failure(s) have no valid insight: ${ids.join(", ")}.`,
    ...INSIGHT_FORMAT,
  ].join("\n");
}

function quiet(): HookResult {
  return { ...QUIET };
}

function block(reason: string): HookResult {
  return { exitCode: 0, stdout: `${JSON.stringify({ decision: "block", reason })}\n`, stderr: "" };
}

function context(event: string, additionalContext: string): HookResult {
  return {
    exitCode: 0,
    stdout: `${JSON.stringify({ hookSpecificOutput: { hookEventName: event, additionalContext } })}\n`,
    stderr: "",
  };
}

function isEntry(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function objectField(source: Record<string, unknown>, name: string): Record<string, unknown> {
  return isEntry(source[name]) ? source[name] as Record<string, unknown> : {};
}

function text(value: unknown): string {
  return typeof value === "string" ? value : "";
}

// A session id the payload did not carry is its own bucket, never another session's.
function sessionOf(payload: Record<string, unknown>): string {
  const session = payload.session_id;
  return typeof session === "string" && session.trim() !== "" ? session : NO_SESSION;
}

function findingText(finding: Finding): string {
  return `${finding.rule}: ${finding.message} Fix: ${finding.fix ?? "see the rule"}`;
}

function fails(findings: Finding[]): Finding[] {
  return findings.filter((finding) => finding.severity === "fail");
}

// ---- PreToolUse --------------------------------------------------------------------------------------------------

function handlePreToolUse(payload: Record<string, unknown>, env: HookEnv): HookResult {
  if (payload.tool_name !== "Bash") return quiet();
  const command = text(objectField(payload, "tool_input").command);
  if (command === "") return quiet();
  const findings = fails(lintCommand(command, { repoRoot: guardRoot(env.cwd), running: env.running }));
  if (findings.length === 0) return quiet();
  const reason = findings.map(findingText).join("; ");
  return {
    exitCode: 0,
    stdout: `${JSON.stringify({
      hookSpecificOutput: { hookEventName: "PreToolUse", permissionDecision: "deny", permissionDecisionReason: reason },
    })}\n`,
    stderr: "",
  };
}

// ---- PostToolUse -------------------------------------------------------------------------------------------------

// The exit code of a failed tool call: a number in the payload or the response, else the number the tool error's first
// line reports ("Exit code N"), else 1 because the tool failed.
function exitCodeOf(payload: Record<string, unknown>, failed: boolean): number | null {
  if (!failed) return null;
  const response = objectField(payload, "tool_response");
  for (const source of [payload, response]) {
    for (const key of ["exit_code", "exitCode"]) {
      const value = source[key];
      if (typeof value === "number" && Number.isFinite(value)) return value;
    }
  }
  // The error text is read for its exit number only; none of the rest of it is stored.
  const reported = /^Exit code (\d+)/.exec(text(payload.error).trim());
  return reported === null ? 1 : Number(reported[1]);
}

function stdoutOf(payload: Record<string, unknown>): string {
  return text(objectField(payload, "tool_response").stdout);
}

function stderrOf(payload: Record<string, unknown>): string {
  const response = objectField(payload, "tool_response");
  for (const source of [response, payload]) {
    const value = text(source.stderr);
    if (value !== "") return value;
    const error = text(source.error);
    if (error !== "") return error;
  }
  return "";
}

// What a failure record says, and the facts its evidence holds: lengths, counts, ids and paths, never content.
interface FailureSpec {
  finding: Finding;
  input: string;
  expected: string;
  actual: string;
  facts: Record<string, unknown>;
}

function recordFailure(root: string, payload: Record<string, unknown>, env: HookEnv, spec: FailureSpec): string {
  const id = newFailureId();
  const evidence = writeEvidence(root, id, { rule: spec.finding.rule, ...spec.facts });
  // An engine record names the engine; the agent's own failure names none, because no engine made it.
  const engine = typeof spec.facts.engine === "string" ? spec.facts.engine : "none";
  appendFailure(root, {
    kind: "failure",
    id,
    time: env.now().toISOString(),
    session: sessionOf(payload),
    found_by: "guard",
    check: spec.finding.rule,
    input: spec.input,
    expected: spec.expected,
    actual: spec.actual,
    engine,
    harness: HARNESS,
    reason: spec.finding.message,
    evidence,
  });
  return id;
}

// A checked result that passed: one line, no evidence, no context line (round 5, S1). It holds the check id and the
// engine or runner name only, never command or output text.
function recordSuccess(root: string, payload: Record<string, unknown>, env: HookEnv, check: "engine-call" | "test-run", engine: string): void {
  const record: SuccessRecord = { kind: "success", time: env.now().toISOString(), session: sessionOf(payload), check, engine };
  appendRecord(root, record);
}

// The record of an engine call that answered nothing: the engine and, when there was one, the output file's name, never
// the command or the prompt (round 3, C2).
function engineSpec(finding: Finding, facts: {
  engine: string;
  outputName: string | null;
  exitCode: number | null;
  stdoutLength: number;
  stderrLength: number;
  interrupted: boolean;
}): FailureSpec {
  const input = facts.outputName === null ? `${facts.engine} call` : `${facts.engine} call (${facts.outputName})`;
  return {
    finding,
    input,
    expected: "an answer from the engine call",
    actual: "the call answered nothing usable",
    facts: {
      engine: facts.engine,
      outputName: facts.outputName,
      exitCode: facts.exitCode,
      stdoutLength: facts.stdoutLength,
      stderrLength: facts.stderrLength,
      interrupted: facts.interrupted,
    },
  };
}

// A call that is still running has no result to check: it was backgrounded with "&", the tool was told to run it in
// the background, or the harness answered with a background task (round 3, C1).
function runsInBackground(payload: Record<string, unknown>, response: Record<string, unknown>, background: boolean): boolean {
  if (background) return true;
  if (objectField(payload, "tool_input").run_in_background === true) return true;
  const task = response.backgroundTaskId;
  return task !== undefined && task !== null;
}

// ---- the agent's own failures (round 4, D1 and D2) ---------------------------------------------------------------

// A test run's own summary: how many tests failed. Zero, a word after the count and text that merely mentions "failed"
// are not summaries.
const FAILED_SUMMARY = /\b([1-9]\d*) (failed|errors?)\b/;

// The command word whose exit a failed call reports: the last segment's, whatever came before it in the pipeline.
function failingCommandWord(command: string): string | null {
  const parts = segments(command);
  for (let index = parts.length - 1; index >= 0; index--) {
    const word = commandWord(parts[index]!.text);
    if (word !== null) return word;
  }
  return null;
}

// The guard's own query commands exit 1 to say "findings" — an answer, not an error (Round 8; cli.ts: 0 ok, 1
// findings, 2 usage). Only the last segment's exit is the call's, so only it is read.
const GUARD_QUERY = /\/src\/cli\.ts\s+(insight|criteria|register|path)\b/;

function guardQueryAnswered(command: string, exitCode: number | null): boolean {
  const parts = segments(command);
  const last = parts[parts.length - 1];
  return exitCode === 1 && last !== undefined && GUARD_QUERY.test(last.text);
}

// The agent's own failure, when this event is one: a test run that failed (D1) or another Bash call that errored (D2).
// An engine call is not one — M5 has already checked it — and a person stopping a call is not a failure (D2, which D1
// follows: an interrupted run was not the agent's mistake either).
function ownFailureSpec(payload: Record<string, unknown>, command: string, failed: boolean): FailureSpec | null {
  if (payload.is_interrupt === true) return null;
  const stdout = stdoutOf(payload);
  const stderr = stderrOf(payload);
  const interrupted = objectField(payload, "tool_response").interrupted === true;
  const runner = recognizeTestRun(command);
  if (runner !== null) {
    // A failure event says so by itself; a success event says so only when its stdout carries a summary, which is
    // how a pipeline hides the exit (D1).
    // stdout speaks for the test run only when everything after it is its own pipeline (`pytest | tail -3`); after
    // `&&`, `;` or `||` other commands write to the same stdout (long-session round 2, B2).
    const ownsStdout = testRunOwnsStdout(command);
    const summary = failed ? FAILED_SUMMARY.exec(stderr) : ownsStdout ? FAILED_SUMMARY.exec(stdout) : null;
    if (!failed && summary === null) return null;
    const exitCode = failed ? exitCodeOf(payload, true) : null;
    const failedCount = summary === null ? null : Number(summary[1]);
    const actual = summary === null ? `exit ${exitCode}` : `${summary[1]} ${summary[2]}`;
    return {
      finding: {
        rule: "R12.2-test-failed",
        severity: "fail",
        message: summary === null
          ? `the ${runner} run exited with code ${exitCode}`
          : `the ${runner} run reported ${actual}`,
        fix: "read which tests failed, fix the cause, run them again",
      },
      input: `${runner} run`,
      expected: "all tests pass",
      actual,
      facts: {
        runner,
        failedCount,
        exitCode,
        stdoutLength: stdout.length,
        stderrLength: stderr.length,
        interrupted,
      },
    };
  }
  if (!failed) return null;
  const word = failingCommandWord(command);
  if (word === null) return null;
  const exitCode = exitCodeOf(payload, true);
  // An exit of zero is not an error, wherever the event came from — the same rule M1's result check follows.
  if (exitCode === 0) return null;
  if (guardQueryAnswered(command, exitCode)) return null;
  return {
    finding: {
      rule: "R12.2-command-error",
      severity: "fail",
      message: `the command exited with code ${exitCode}`,
      fix: "read the error, fix the cause, run the command again",
    },
    input: `${word} call`,
    expected: "exit 0",
    actual: `exit ${exitCode}`,
    facts: {
      commandWord: word,
      exitCode,
      stdoutLength: stdout.length,
      stderrLength: stderr.length,
      interrupted,
    },
  };
}

// The runner of a test run that passed (round 5, S1): recognised, not interrupted, not in the background (C1), and with
// no failure summary anywhere in its stdout — stricter than D1, which reads stdout only when the run owns it, so a
// failing run followed by `; echo` is never counted as green. Null when it is not one.
function greenTestRun(payload: Record<string, unknown>, response: Record<string, unknown>, command: string): string | null {
  const runner = recognizeTestRun(command);
  if (runner === null) return null;
  if (payload.is_interrupt === true || response.interrupted === true) return null;
  const run = segments(command).find((segment) => recognizeTestRun(segment.text) !== null);
  if (runsInBackground(payload, response, run?.background === true)) return null;
  if (FAILED_SUMMARY.test(stdoutOf(payload))) return null;
  return runner;
}

// The folder the call ran in: the payload's own cwd when it has one, the environment's otherwise (round 3, C3).
function workingFolder(payload: Record<string, unknown>, env: HookEnv): string {
  const own = payload.cwd;
  return typeof own === "string" && own.trim() !== "" ? own : env.cwd;
}

// The one context line for an event that logged failures: every new id, once, with what to do about them (round 4, D4).
function logged(ids: string[], own: boolean): HookResult {
  const tail = own ? `${ALREADY_LOGGED} Note: ${OWN_FAILURES}` : ALREADY_LOGGED;
  return context("PostToolUse", `harness-guard logged ${ids.join(", ")} — ${tail}`);
}

function handlePostToolUse(payload: Record<string, unknown>, env: HookEnv, root: string, failed: boolean): HookResult {
  if (payload.tool_name === "Bash") {
    const command = text(objectField(payload, "tool_input").command);
    if (command === "") return quiet();
    const response = objectField(payload, "tool_response");
    const site = engineCallSite(command, workingFolder(payload, env));

    // No engine call: the failure, if any, is the agent's own (D1, D2).
    if (site === null) {
      const own = ownFailureSpec(payload, command, failed);
      if (own !== null) return logged([recordFailure(root, payload, env, own)], true);
      // A green test run is a success line (round 5, S1).
      const runner = failed ? null : greenTestRun(payload, response, command);
      if (runner !== null) recordSuccess(root, payload, env, "test-run", runner);
      return quiet();
    }

    // A path the text cannot name is not checked: no record, never a missing-output failure (round 4, D3).
    if (!site.outputKnown || !site.cwdKnown) return quiet();
    if (runsInBackground(payload, response, site.call.background)) return quiet();
    const stdout = stdoutOf(payload);
    const stderr = stderrOf(payload);
    const interrupted = response.interrupted === true;
    // A failing segment after the engine is not the engine's exit (round 3, C4).
    const exitCode = site.endsWithEngine ? exitCodeOf(payload, failed) : null;
    const call = site.call;
    const findings = fails(checkResult({ call, cwd: site.cwd, exitCode, stdout, stderr, interrupted }));
    if (findings.length === 0) {
      // A clean engine call is a success line; only PostToolUse writes one (round 5, S1).
      if (!failed) recordSuccess(root, payload, env, "engine-call", call.engine);
      return quiet();
    }
    // The command text is never stored: the engine name and the output file's name say which call it was.
    const facts = {
      engine: call.engine,
      outputName: call.outputFile === null ? null : path.basename(call.outputFile),
      exitCode,
      stdoutLength: stdout.length,
      stderrLength: stderr.length,
      interrupted,
    };
    const ids = findings.map((finding) => recordFailure(root, payload, env, engineSpec(finding, facts)));
    return logged(ids, false);
  }

  if (!failed && WRITE_TOOLS.has(text(payload.tool_name))) {
    const file = text(objectField(payload, "tool_input").file_path);
    // A register or a criteria file (round 6, K2) the session wrote is checked at Stop.
    if (file === "" || !(isRegisterFile(file) || isCriteriaFile(file))) return quiet();
    const record: TouchedRecord = {
      kind: "touched",
      time: env.now().toISOString(),
      session: sessionOf(payload),
      path: path.relative(root, path.resolve(env.cwd, file)),
    };
    appendRecord(root, record);
  }
  return quiet();
}

// ---- Stop --------------------------------------------------------------------------------------------------------

// The register files this session touched, newest path last, each once.
function touchedRegisters(root: string, session: string): string[] {
  const names: string[] = [];
  for (const record of readJournal(root).records) {
    if (record.kind !== "touched" || record.session !== session) continue;
    const file = path.resolve(root, record.path);
    if (!names.includes(file)) names.push(file);
  }
  return names;
}

function registerFindings(root: string, session: string): { rule: string; file: string }[] {
  const found: { rule: string; file: string }[] = [];
  for (const file of touchedRegisters(root, session)) {
    if (!isRegisterFile(file)) continue;
    // A register this session touched and then deleted or renamed is not checked (round 3, C9).
    if (!fs.existsSync(file)) continue;
    const name = path.relative(root, file);
    let register;
    try {
      register = loadRegister(file);
    } catch {
      found.push({ rule: "register-unreadable", file: name });
      continue;
    }
    // Only rule ids and file names: the register's own text never enters a reason.
    for (const finding of fails([...validateRegister(register), ...coverage(register).findings])) {
      found.push({ rule: finding.rule, file: name });
    }
  }
  return found;
}

function handleStop(payload: Record<string, unknown>, root: string, env: HookEnv): HookResult {
  const session = sessionOf(payload);

  const open = openFailures(root, session);
  if (open.length > 0) return block(insightReason(open.map((record) => record.id)));

  const sessionFailures = failuresFor(root, session);
  // The raise step needs the final message to check: a payload without that string is asked, not told (round 3, C10).
  const last = payload.last_assistant_message;
  // Raise once (round 4, D6): failures a final message has already raised need not be named again at a later stop.
  const raised = new Set(
    readJournal(root).records.flatMap((record) => (record.kind === "raised" && record.session === session ? record.ids : [])),
  );
  const pending = sessionFailures.filter((record) => !raised.has(record.id));
  if (pending.length > 0 && typeof last === "string") {
    const answers = answered(root);
    const names = [...new Set(pending.map((record) => answers.get(record.id)).filter((name): name is string => name !== undefined))];
    if (names.length === 0 || !names.every((name) => last.includes(name))) {
      return block(`harness-guard: raise the insight: name ${names.join(", ")} in your final message. The insight must be a section of one of these files, and it must answer every failure of this session.`);
    }
    const record: RaisedRecord = { kind: "raised", time: new Date().toISOString(), session, ids: pending.map((r) => r.id) };
    appendRecord(root, record);
  }

  const failed = registerFindings(root, session);
  if (failed.length > 0) {
    const lines = failed.map(({ rule, file }) => `  ${rule} (fail) in ${file}`);
    return block(["harness-guard: the register files this session touched still have failing checks:", ...lines].join("\n"));
  }
  const criteria = criteriaStep(root, session, raised, env);
  if (criteria !== null) return criteria;
  return pathAsk(root, session, raised, env);
}

// ---- the score (round 6, K2) -------------------------------------------------------------------------------------

// The failure checks the criteria step itself writes: they are not the work, so they never make criteria late.
const CRITERION_CHECK = "criterion:";
const LATE_CHECK = "R12.7-criteria-late";

function byCriteriaStep(check: string): boolean {
  return check.startsWith(CRITERION_CHECK) || check === LATE_CHECK;
}

// The criteria files this session touched, each once with the time of its first touch, as root-relative paths.
function touchedCriteria(root: string, session: string): { file: string; first: number }[] {
  const found: { file: string; first: number }[] = [];
  for (const record of readJournal(root).records) {
    if (record.kind !== "touched" || record.session !== session || !isCriteriaFile(record.path)) continue;
    const file = path.relative(root, path.resolve(root, record.path));
    const time = Date.parse(record.time);
    const seen = found.find((entry) => entry.file === file);
    if (seen === undefined) found.push({ file, first: time });
    else if (time < seen.first) seen.first = time;
  }
  return found;
}

// The state of a file, so a block for it is given once per state: a short hash of its bytes, never its text.
function fileState(file: string): string {
  try {
    return createHash("sha256").update(fs.readFileSync(file)).digest("hex").slice(0, 16);
  } catch {
    return "unreadable";
  }
}

// One failure record the criteria step writes; its evidence is the criteria file itself.
function criteriaFailure(root: string, session: string, env: HookEnv, file: string, check: string, expected: string, actual: string, reason: string): void {
  appendFailure(root, {
    kind: "failure",
    id: newFailureId(),
    time: env.now().toISOString(),
    session,
    found_by: "guard",
    check,
    input: path.basename(file),
    expected,
    actual,
    engine: "none",
    harness: HARNESS,
    reason,
    evidence: file,
  });
}

// For each criteria file this session touched: a file that is unreadable, fails its checks or has unmarked items blocks
// once per file state (rules and ids only, never item text); each item marked not met becomes a failure; criteria
// first written after the work's first checked result become one late failure. New failures block like any other.
function criteriaStep(root: string, session: string, raised: Set<string>, env: HookEnv): HookResult | null {
  const files = touchedCriteria(root, session);
  if (files.length === 0) return null;

  const records = readJournal(root).records;
  // What this session's journal already holds: a criterion's failure is written once per id, a late one once per file.
  const checks = new Set<string>();
  const lateFiles = new Set<string>();
  for (const record of records) {
    if (record.kind !== "failure" || record.session !== session) continue;
    checks.add(record.check);
    if (record.check === LATE_CHECK) lateFiles.add(record.evidence);
  }
  const workTimes = records
    .filter((record) => record.session === session && (record.kind === "success" || (record.kind === "failure" && !byCriteriaStep(record.check))))
    .map((record) => Date.parse(record.time))
    .filter((time) => Number.isFinite(time));
  const promptTimes = records
    .filter((record) => record.session === session && record.kind === "prompt")
    .map((record) => Date.parse(record.time))
    .filter((time) => Number.isFinite(time));
  // Round 8: the work a criteria file must precede is the work of its own request — what came after the last prompt
  // before the file was first touched. A session with no prompt records reads from its start, as before.
  const firstWorkOf = (touched: number): number | null => {
    const start = Math.max(-Infinity, ...promptTimes.filter((time) => time <= touched));
    const after = workTimes.filter((time) => time > start);
    return after.length === 0 ? null : Math.min(...after);
  };

  const lines: string[] = [];
  const states: string[] = [];
  let wrote = false;

  for (const { file, first } of files) {
    const absolute = path.resolve(root, file);
    // A criteria file this session touched and then deleted or renamed is not checked (as for registers, C9).
    if (!fs.existsSync(absolute)) continue;

    const firstWork = Number.isFinite(first) ? firstWorkOf(first) : null;
    if (firstWork !== null && first > firstWork && !lateFiles.has(file)) {
      criteriaFailure(root, session, env, file, LATE_CHECK, "criteria written before the work", "criteria written after the work began", "the criteria were written after the work's first checked result");
      lateFiles.add(file);
      wrote = true;
    }

    let loaded;
    let problems: string[];
    try {
      loaded = loadCriteria(absolute);
      const result = score(loaded);
      problems = [
        // K1's messages name items by id or position, never by their text.
        ...fails(checkCriteria(loaded)).map((finding) => `${finding.rule} (${finding.message})`),
        ...(result.unmarked.length > 0 ? [`unmarked: ${result.unmarked.join(", ")}`] : []),
      ];
    } catch {
      loaded = null;
      problems = ["R12.7-criteria-unreadable"];
    }

    if (problems.length > 0) {
      const state = `criteria-state:${file}:${fileState(absolute)}`;
      if (!raised.has(state)) {
        lines.push(`  ${file}: ${[...new Set(problems)].join("; ")}`);
        states.push(state);
      }
    }

    if (loaded === null) continue;
    const items = Array.isArray(loaded.items) ? loaded.items : [];
    for (const item of items) {
      if (!isEntry(item) || item.met !== false) continue;
      const id = typeof item.id === "string" ? item.id.trim() : "";
      const check = `${CRITERION_CHECK}${id}`;
      if (id === "" || checks.has(check)) continue;
      criteriaFailure(root, session, env, file, check, "met", "not met", "a criterion of the task was not met");
      checks.add(check);
      wrote = true;
    }
  }

  if (lines.length > 0) {
    const record: RaisedRecord = { kind: "raised", time: env.now().toISOString(), session, ids: states };
    appendRecord(root, record);
    return block(["harness-guard: the criteria files this session touched are not scored yet — mark each criterion met: true|false with evidence:", ...lines].join("\n"));
  }
  if (wrote) {
    const open = openFailures(root, session);
    if (open.length > 0) return block(insightReason(open.map((record) => record.id)));
  }
  return null;
}

// ---- the path of a success (round 5, S5) ---------------------------------------------------------------------------

// The guard's own folder as the agent should type it: relative to the root when it lies inside it.
function guardDirFor(root: string): string {
  const dir = path.resolve(import.meta.dirname, "..");
  const relative = path.relative(root, dir);
  return relative === "" ? "." : relative.startsWith("..") || path.isAbsolute(relative) ? dir : relative;
}

// The path files that name this session, as root-relative paths. A file that does not load names no session.
function sessionPathFiles(root: string, session: string): { file: string; great: boolean }[] {
  const found: { file: string; great: boolean }[] = [];
  for (const file of findPathFiles(root)) {
    try {
      const loaded = loadPath(path.join(root, file));
      if (loaded.session === session) found.push({ file, great: loaded.great !== undefined && loaded.great !== null });
    } catch {
      continue;
    }
  }
  return found;
}

// A session with a success line is asked once to record its path, or, when a path file of its claims a great success
// with no valid `## great:` insight section, to write that section — the same block, once: the ask writes a `raised`
// record with id "path", so a later stop does not ask again.
function pathAsk(root: string, session: string, raised: Set<string>, env: HookEnv): HookResult {
  if (raised.has("path")) return quiet();
  if (!readJournal(root).records.some((record) => record.kind === "success" && record.session === session)) return quiet();
  const files = sessionPathFiles(root, session);
  const answeredGreat = files.some((entry) => entry.great) ? greatAnswered(root) : new Set<string>();
  const greatMissing = files.filter((entry) => entry.great && !answeredGreat.has(path.normalize(entry.file))).map((entry) => entry.file);
  if (files.length > 0 && greatMissing.length === 0) return quiet();

  const record: RaisedRecord = { kind: "raised", time: env.now().toISOString(), session, ids: ["path"] };
  appendRecord(root, record);
  const lines = [`harness-guard: record the path of this task — run \`bun ${guardDirFor(root)}/src/cli.ts path new --session ${session} --out runs/<run>/success-path.yaml\` (or .harness-guard/paths/<name>.yaml), fill steps, decisions and measures; for a similar task, name a parent and what you changed`];
  if (greatMissing.length > 0) {
    lines.push(`${greatMissing.join(", ")} claims a great success with no valid insight section; add one to an insight file: \`## great: <path file>\` with Comparison:, Cause: and Options: (1–3 numbered items, each starting with [rule], [check] or [tool] and holding evidence:).`);
  }
  return block(lines.join("\n"));
}

// ---- SessionStart ------------------------------------------------------------------------------------------------

function handleSessionStart(payload: Record<string, unknown>, root: string): HookResult {
  const session = sessionOf(payload);
  const others = openFailures(root, null).filter((record) => record.session !== session);
  if (others.length === 0) return quiet();
  const ids = others.map((record) => record.id);
  return context("SessionStart", `harness-guard: ${ids.length} failure(s) from other sessions in this repository are still unanswered: ${ids.join(", ")}. Raise an insight for each before you finish.`);
}

// ---- UserPromptSubmit (round 6, K2) -------------------------------------------------------------------------------

// Before the work starts, the session is asked once to write the criteria it will be scored on: not when it has already
// touched a criteria file, and not again once asked (a `raised` record with id "criteria"). The prompt is never read.
function handleUserPromptSubmit(payload: Record<string, unknown>, root: string, env: HookEnv): HookResult {
  const session = sessionOf(payload);
  const prompt: PromptRecord = { kind: "prompt", time: env.now().toISOString(), session };
  appendRecord(root, prompt);
  const records = readJournal(root).records.filter((record) => record.session === session);
  if (records.some((record) => record.kind === "touched" && isCriteriaFile(record.path))) return quiet();
  if (records.some((record) => record.kind === "raised" && record.ids.includes("criteria"))) return quiet();
  const record: RaisedRecord = { kind: "raised", time: env.now().toISOString(), session, ids: ["criteria"] };
  appendRecord(root, record);
  return context(
    "UserPromptSubmit",
    `harness-guard: before you start, write the criteria this request will be scored on — \`bun ${guardDirFor(root)}/src/cli.ts criteria new --out runs/<run>/criteria.yaml\` (or .harness-guard/criteria/<name>.yaml), one item per thing the result must get right; mark each met or not met with evidence at the end.`,
  );
}

// ---- handler -----------------------------------------------------------------------------------------------------

function dispatch(payload: Record<string, unknown>, env: HookEnv): HookResult {
  const root = guardRoot(env.cwd);
  switch (payload.hook_event_name) {
    case "PreToolUse":
      return handlePreToolUse(payload, env);
    case "PostToolUse":
      return handlePostToolUse(payload, env, root, false);
    case "PostToolUseFailure":
      return handlePostToolUse(payload, env, root, true);
    case "Stop":
    case "SubagentStop":
      return handleStop(payload, root, env);
    case "SessionStart":
      return handleSessionStart(payload, root);
    case "UserPromptSubmit":
      return handleUserPromptSubmit(payload, root, env);
    default:
      return quiet();
  }
}

// A guard bug must not freeze the agent: the handler returns exit 1, one safe stderr line and a guard_error record.
export function handleHook(payload: unknown, env: HookEnv): HookResult {
  try {
    if (!isEntry(payload)) return quiet();
    return dispatch(payload, env);
  } catch (error) {
    const session = (() => {
      try {
        return isEntry(payload) ? sessionOf(payload) : NO_SESSION;
      } catch {
        return NO_SESSION;
      }
    })();
    const message = "harness-guard: an internal error was caught; the guard is failing open";
    try {
      const record: GuardErrorRecord = { kind: "guard_error", time: env.now().toISOString(), session, message };
      appendRecord(guardRoot(env.cwd), record);
    } catch {
      // The journal itself is what failed; the one-line stderr still stands.
    }
    const kind = error instanceof Error ? error.name : "Error";
    return { exitCode: 1, stdout: "", stderr: `${message} (${kind})\n` };
  }
}

// True when every segment after the first test-run segment is piped from the one before it.
function testRunOwnsStdout(command: string): boolean {
  const list = segments(command);
  const at = list.findIndex((segment) => recognizeTestRun(segment.text) !== null);
  if (at < 0) return false;
  return list.slice(at + 1).every((segment) => segment.piped);
}
