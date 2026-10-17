// R2: the warning — one line per failing MUST and for a missing AGENTS.md, with ids and file names, never entry
// text; nothing else; empty when there are none. `--warn` prints it; the session-start hook that also prints it is
// a harness change R2 leaves to the owner (R12.3), and no file under project-memory/.cache/ is ever opened here
// (Rd1): nothing in the run reads a cache file, only whether the folder is there.
import type { CheckRun, RequirementResult } from "./checks.ts";

const TOOL_COMMAND = /^python3 .*--check\s+\(in .*\) → exit -?\d+(, output: [^;]*)?;?/;
/** The file names in an evidence line, and nothing else of the entry: no claim, no body, no text. */
const FILE_NAME = /(project-memory\/entries\/[\w.\-]+|project-memory\/INDEX\.md|AGENTS\.md)/g;

function filesIn(evidence: string): string {
  return [...new Set([...evidence.matchAll(FILE_NAME)].map((match) => match[1]!))].join(", ");
}

/** The one break of the evidence, without the command and output memory_index.py's own. */
function firstBreak(evidence: string): string {
  const withoutCommand = evidence.replace(TOOL_COMMAND, "");
  const first = withoutCommand.split(";")[0] ?? withoutCommand;
  const trimmed = first.trim();
  return trimmed.length <= 200 ? trimmed : `${trimmed.slice(0, 199)}…`;
}

function warningFor(result: RequirementResult): string {
  const files = filesIn(result.evidence);
  const where = files === "" ? "" : ` — files: ${files}`;
  return `memory-check: ${result.id} fails: ${firstBreak(result.evidence)}${where}`;
}

export function renderWarning(run: CheckRun): string {
  // F1 failing is the missing AGENTS.md, which has its own line below: one line per thing, not two.
  const lines = run.results
    .filter((result) => result.id !== "F1" && result.level === "MUST" && result.verdict === "fail")
    .map(warningFor);
  const missingAgents = run.results.find((result) => result.id === "F1" && result.verdict === "fail");
  if (missingAgents) {
    lines.push(`memory-check: AGENTS.md is missing — file: ${run.root}/AGENTS.md (it is required, F1)`);
  }
  return lines.join("\n");
}