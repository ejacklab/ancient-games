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

export type JournalRecord = FailureRecord | TouchedRecord | GuardErrorRecord;

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
