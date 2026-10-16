// Shared types for harness-guard (SPEC.md). Fixed: modules import these and do not redefine them.

export type Severity = "fail" | "warn";

export interface Finding {
  rule: string;
  severity: Severity;
  message: string;
  fix?: string;
  ref?: string;
}

// ---- M1: catalogue, recognition, result -------------------------------------------------------------------------

export interface Trap {
  id: string;
  status: "approved" | "proposed";
  applies: "command" | "result";
  engine: string; // an EngineSpec name, or "any"
  command?: string; // regex source (command traps)
  unless?: string; // regex source: no hit when it matches
  unless_piped?: boolean; // no hit when the segment's stdin comes from a pipe
  background?: boolean;
  concurrent?: boolean;
  paths_outside_repo?: boolean;
  stderr?: string; // regex source (result traps)
  output_empty?: boolean; // result traps
  why: string;
  fix: string;
  source: string; // where the trap was recorded (a note name or a run path), generic text
  withdraw_when?: string; // R12.6: the observable that would show the trap is no longer needed
}

export interface SilentFailure {
  text: string;
  status: string;
}

export interface EngineSpec {
  name: string;
  command: string; // regex source that recognises a call
  output_flags?: string[]; // e.g. ["-o", "--out"]
  stdout_is_answer?: boolean;
  status_from_out_dir?: boolean; // wrapper writes <out>/status.json
  silent_failures?: SilentFailure[];
}

export interface EngineCall {
  engine: string;
  outputFile: string | null;
  stdoutIsAnswer: boolean;
  statusFile: string | null;
  background: boolean;
}

export interface Segment {
  text: string;
  background: boolean;
  piped: boolean;
}

export interface LintContext {
  repoRoot: string;
  running: string[]; // command lines of other running processes
  background?: boolean;
}

export interface ResultInput {
  call: EngineCall;
  cwd: string;
  exitCode: number | null;
  stdout: string;
  stderr: string;
  interrupted: boolean;
}

// ---- M2: journal ------------------------------------------------------------------------------------------------

export interface FailureRecord {
  kind: "failure";
  id: string; // F-xxxxxxxx
  time: string; // ISO 8601
  session: string;
  found_by: string;
  check: string;
  input: string;
  expected: string;
  actual: string;
  engine: string;
  harness: string;
  reason: string;
  evidence: string; // path, relative to the guard root or absolute
  from?: string; // Round 9: the warning (W-xxxxxxxx) this failure was logged from, when it was one
}

// Round 9: what the guard saw but cannot judge — a guess, not a verdict. The same fields as a failure, so the agent can
// log it as one; it is settled by a failure record whose `from` is its id, or by a dismissed record.
export interface WarningRecord {
  kind: "warning";
  id: string; // W-xxxxxxxx
  time: string;
  session: string;
  check: string;
  input: string;
  expected: string;
  actual: string;
  engine: string;
  harness: string;
  reason: string; // why the guard warned
  evidence: string;
}

// Round 9: the agent's one-line reason that a warning was not a failure; the project owner may overrule it.
export interface DismissedRecord {
  kind: "dismissed";
  time: string;
  session: string;
  id: string; // the warning's id
  reason: string;
}

export interface TouchedRecord {
  kind: "touched";
  time: string;
  session: string;
  path: string; // relative to the guard root
}

export interface GuardErrorRecord {
  kind: "guard_error";
  time: string;
  session: string;
  message: string;
}

// Round 4, D6: the failures a final message has already raised, so a later stop need not name them again.
export interface RaisedRecord {
  kind: "raised";
  time: string;
  session: string;
  ids: string[];
}

// Round 5 (R12.7): a checked result that passed — one line, no evidence.
export interface SuccessRecord {
  kind: "success";
  time: string;
  session: string;
  check: string; // "engine-call" | "test-run"
  engine: string; // engine name, or the test runner label
}

// Round 8: a request from the person arrived — its time only, never its text. It marks where a task starts, so the
// late-criteria check reads the work of this request, not of the whole session.
export interface PromptRecord {
  kind: "prompt";
  time: string;
  session: string;
}

export type JournalRecord = FailureRecord | TouchedRecord | GuardErrorRecord | RaisedRecord | SuccessRecord | PromptRecord
  | WarningRecord | DismissedRecord;

// Round 5 (R12.7): the path of a successful task, a YAML file.
export interface PathStep {
  did: string;
  engine?: string;
  model?: string;
  check?: string;
}

export interface SuccessPath {
  path: 1;
  session: string;
  category: string;
  objective: string;
  steps: PathStep[];
  decisions?: string[];
  measures: Record<string, number>; // e.g. seconds, failures, retries, checks_passed, successes
  failures?: string[]; // the check ids of this session's failure records
  parent?: string; // relative path of the parent's path file
  change?: string; // what this child changed from its parent
  aim?: { measure: string; parent_value: number; lower_is_better: boolean };
  great?: { comparison: string; evidence: string };
}

// Round 6 (R12.7 score): the criteria a task is scored against, a YAML file written before the work.
export interface Criterion {
  id: string; // e.g. C1, or a register unit id such as UC1/f1
  text: string;
  met?: boolean | null; // null or absent until the agent marks it
  evidence?: string; // a path or a fact; required once met is set
}

export interface CriteriaFile {
  criteria: 1;
  session: string;
  request: string; // the request in a few words (never a secret)
  items: Criterion[];
}

export interface Score {
  met: number;
  total: number;
  percent: number | null; // one decimal; null when total is 0
  unmarked: string[]; // ids with no met value
}

export interface PathReport {
  file: string;
  findings: Finding[];
  better: boolean | null; // null when there is no parent or no aim
  gainPercent: number | null; // signed: positive means improved on the aim's measure
  repeatedFailures: string[];
}

// ---- M3: insight ------------------------------------------------------------------------------------------------

export interface InsightOption {
  kind: string; // rule | check | tool | config-advice, or what was written
  text: string;
  evidence: string; // "" when missing
}

export interface InsightSection {
  ids: string[];
  whys: string[];
  source: string | null;
  rootCause: string | null;
  options: InsightOption[];
}

// ---- M4: register -----------------------------------------------------------------------------------------------

export interface Decision {
  by?: string;
  verdict?: "accepted" | "declined";
  at?: string;
}

export interface UseCase {
  id: string;
  origin: "user" | "ai";
  decision?: Decision;
  purpose?: string;
  fails_if?: string[];
  min_acceptance?: string[];
  safety?: boolean;
}

export interface Requirement {
  id: string;
  origin: "user" | "ai";
  decision?: Decision;
  purpose?: string;
  serves?: string[];
  fails_if?: string[];
  targets?: Record<string, string>;
}

export interface Conflict {
  use_case: string;
  requirement: string;
  result?: string;
  shown_to_owner?: boolean;
  resolution?: string;
}

export interface CoverageEntry {
  unit: string;
  covered_by?: string[];
  skippable?: { reason?: string };
}

export interface Register {
  register: 1;
  frozen?: string;
  use_cases?: UseCase[];
  requirements?: Requirement[];
  conflicts?: Conflict[];
  coverage?: CoverageEntry[];
}

export interface Unit {
  id: string; // UC1/f1, UC1/m2, RQ1/f1
  text: string;
  safety: boolean;
}

export interface CoverageReport {
  total: number;
  covered: number;
  percent: number;
  target: 80;
  findings: Finding[];
}

// ---- M5: hooks --------------------------------------------------------------------------------------------------

export interface HookEnv {
  cwd: string;
  running: string[];
  now: () => Date;
}

export interface HookResult {
  exitCode: number;
  stdout: string;
  stderr: string;
}

export interface DoctorHarness {
  harness: string;
  guard: "installed" | "absent" | "unknown";
  answers: boolean | null;
  note: string;
}

export interface DoctorReport {
  harnesses: DoctorHarness[];
  health: { ok: boolean; summary: string } | null;
}
