// M5: the Claude-protocol hook handler (SPEC.md M5). One handler serves every harness: PreToolUse denies a
// catalogued command trap, PostToolUse logs an engine call that answered nothing, Stop blocks while a failure has
// no insight. Nothing here prints a prompt, stdout, stderr or config value: only ids, rules, lengths and paths.

import * as path from "node:path";
import { appendFailure, appendRecord, failuresFor, guardRoot, newFailureId, readJournal, writeEvidence } from "./journal.ts";
import { answered, openFailures } from "./insight.ts";
import { coverage, isRegisterFile, loadRegister, validateRegister } from "./register.ts";
import { checkResult, lintCommand, recognizeEngineCall } from "./traps.ts";
import type { Finding, GuardErrorRecord, HookEnv, HookResult, TouchedRecord } from "./types.ts";

const HARNESS = "claude-code";
const NO_SESSION = "none";
const WRITE_TOOLS = new Set(["Write", "Edit", "MultiEdit"]);

const QUIET: HookResult = { exitCode: 0, stdout: "", stderr: "" };

const INSIGHT_FORMAT = [
  "Write the insight before you stop, in runs/<run>/insight*.md, one section per id:",
  "  ## F-xxxxxxxx — short title",
  "  Whys: 3–6 numbered items, ending at the instruction, check, tool or config.",
  "  Source: one of instruction, check, tool, config.",
  "  Root cause: one line naming that changeable source.",
  "  Options: 2–3 items, each starting with a kind ([rule], [check], [tool] or [config-advice]) and ending with evidence: <path or fact>.",
];

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

// The exit code of a failed tool call: a number in the payload or the response, else 1 because the tool failed.
function exitCodeOf(payload: Record<string, unknown>, failed: boolean): number | null {
  if (!failed) return null;
  const response = objectField(payload, "tool_response");
  for (const source of [payload, response]) {
    for (const key of ["exit_code", "exitCode"]) {
      const value = source[key];
      if (typeof value === "number" && Number.isFinite(value)) return value;
    }
  }
  return 1;
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

function recordFailure(root: string, payload: Record<string, unknown>, env: HookEnv, finding: Finding, facts: {
  engine: string;
  outputName: string;
  exitCode: number | null;
  stdoutLength: number;
  stderrLength: number;
  interrupted: boolean;
}): string {
  const id = newFailureId();
  const evidence = writeEvidence(root, id, {
    rule: finding.rule,
    engine: facts.engine,
    outputName: facts.outputName,
    exitCode: facts.exitCode,
    stdoutLength: facts.stdoutLength,
    stderrLength: facts.stderrLength,
    interrupted: facts.interrupted,
  });
  appendFailure(root, {
    kind: "failure",
    id,
    time: env.now().toISOString(),
    session: sessionOf(payload),
    found_by: "guard",
    check: finding.rule,
    input: `${facts.engine} ${facts.outputName}`,
    expected: "an answer from the engine call",
    actual: "the call answered nothing usable",
    engine: facts.engine,
    harness: HARNESS,
    reason: finding.message,
    evidence,
  });
  return id;
}

function handlePostToolUse(payload: Record<string, unknown>, env: HookEnv, root: string, failed: boolean): HookResult {
  if (payload.tool_name === "Bash") {
    const command = text(objectField(payload, "tool_input").command);
    if (command === "") return quiet();
    const call = recognizeEngineCall(command);
    if (call === null) return quiet();
    const response = objectField(payload, "tool_response");
    const stdout = stdoutOf(payload);
    const stderr = stderrOf(payload);
    const interrupted = response.interrupted === true;
    const exitCode = exitCodeOf(payload, failed);
    const findings = fails(checkResult({ call, cwd: env.cwd, exitCode, stdout, stderr, interrupted }));
    if (findings.length === 0) return quiet();
    // The command text is never stored: the engine name and the output file's name say which call it was.
    const facts = {
      engine: call.engine,
      outputName: call.outputFile === null ? "stdout" : path.basename(call.outputFile),
      exitCode,
      stdoutLength: stdout.length,
      stderrLength: stderr.length,
      interrupted,
    };
    const ids = findings.map((finding) => recordFailure(root, payload, env, finding, facts));
    const rules = findings.map((finding) => finding.rule);
    return {
      exitCode: 0,
      stdout: `${JSON.stringify({
        hookSpecificOutput: {
          hookEventName: "PostToolUse",
          additionalContext: `harness-guard logged ${ids.length} failure(s): ${ids.join(", ")} — ${rules.join(", ")}. Log it in your report; an insight is required before you stop.`,
        },
      })}\n`,
      stderr: "",
    };
  }

  if (!failed && WRITE_TOOLS.has(text(payload.tool_name))) {
    const file = text(objectField(payload, "tool_input").file_path);
    if (file === "" || !isRegisterFile(file)) return quiet();
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

function handleStop(payload: Record<string, unknown>, root: string): HookResult {
  const session = sessionOf(payload);

  const open = openFailures(root, session);
  if (open.length > 0) return block(insightReason(open.map((record) => record.id)));

  const sessionFailures = failuresFor(root, session);
  if (sessionFailures.length > 0) {
    const answers = answered(root);
    const names = [...new Set(sessionFailures.map((record) => answers.get(record.id)).filter((name): name is string => name !== undefined))];
    const last = text(payload.last_assistant_message);
    if (names.length === 0 || !names.every((name) => last.includes(name))) {
      return block(`harness-guard: raise the insight: name ${names.join(", ")} in your final message. The insight must be a section of one of these files, and it must answer every failure of this session.`);
    }
  }

  const failed = registerFindings(root, session);
  if (failed.length > 0) {
    const lines = failed.map(({ rule, file }) => `  ${rule} (fail) in ${file}`);
    return block(["harness-guard: the register files this session touched still have failing checks:", ...lines].join("\n"));
  }
  return quiet();
}

// ---- SessionStart ------------------------------------------------------------------------------------------------

function handleSessionStart(payload: Record<string, unknown>, root: string): HookResult {
  const session = sessionOf(payload);
  const others = openFailures(root, null).filter((record) => record.session !== session);
  if (others.length === 0) return quiet();
  const ids = others.map((record) => record.id);
  return context("SessionStart", `harness-guard: ${ids.length} failure(s) from other sessions in this repository are still unanswered: ${ids.join(", ")}. Raise an insight for each before you finish.`);
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
      return handleStop(payload, root);
    case "SessionStart":
      return handleSessionStart(payload, root);
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