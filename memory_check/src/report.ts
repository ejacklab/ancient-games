// R1: one Markdown report per run — the snapshot in the first line (C5), the locations (F1), how many files under
// `project-memory/` are changed but not staged, then every requirement with its id, level, result and evidence, MUSTs
// first, a list of what needs a reviewer, and last a section holding every "not applicable" result.
import type { CheckRun, RequirementResult, Verdict } from "./checks.ts";
import type { UnstagedMemory } from "./gitchecks.ts";

const LEVEL_ORDER: Record<string, number> = { MUST: 0, SHOULD: 1, guidance: 2, "not stated in CACHES.md": 3 };

function byLevelThenId(a: RequirementResult, b: RequirementResult): number {
  const levels = (LEVEL_ORDER[a.level] ?? 9) - (LEVEL_ORDER[b.level] ?? 9);
  return levels !== 0 ? levels : a.id.localeCompare(b.id);
}

function verdictOf(result: RequirementResult): string {
  return result.verdict;
}

/** One result line, with its evidence on the same line so a diff of two reports shows the change. */
function line(result: RequirementResult): string {
  return `- **${result.id}** (${result.level}) — ${verdictOf(result)} — ${result.evidence}`;
}

function count(results: readonly RequirementResult[], verdict: Verdict): number {
  return results.filter((one) => one.verdict === verdict).length;
}

/** R1: every "not applicable" result is printed in the last section and nowhere else, so each section drops them. */
function applicable(results: readonly RequirementResult[]): RequirementResult[] {
  return results.filter((result) => result.verdict !== "not applicable");
}

/** R1: how many files under `project-memory/` the working tree changed and the staged snapshot does not hold. */
function unstagedLine(unstaged: UnstagedMemory): string[] {
  const command = "(git status --porcelain -uall -- project-memory; the checks read the staged state, C5)";
  if (unstaged.error !== null) {
    return ["", "## Files changed but not staged (R1)", "", `- the count could not be read: ${unstaged.error}`];
  }
  const shown = unstaged.files.slice(0, 5).map((file) => `\`${file}\``);
  const more = unstaged.files.length > 5 ? ` … and ${unstaged.files.length - 5} more` : "";
  return [
    "",
    "## Files changed but not staged (R1)",
    "",
    `- ${unstaged.count} file${unstaged.count === 1 ? "" : "s"} under \`project-memory/\` changed but not staged, and so ` +
      `not checked by this run${shown.length === 0 ? "" : `: ${shown.join(", ")}${more}`} ${command}`,
  ];
}

export function renderReport(run: CheckRun, outFile: string | null): string {
  const { snapshot, results, locations } = run;
  const own = results.filter((result) => !result.id.includes(":"));
  const sot = results.filter((result) => result.id.startsWith("SoT:"));
  const caches = results.filter((result) => result.id.startsWith("CACHES:"));

  const first =
    `# memory-check — snapshot: files: ${snapshot.filesView}; history: ${snapshot.historyView} — project: ${run.root}`;
  const head = [
    first,
    "",
    `Guidelines this report is checked against (the tool's own copy, C1): ${run.guidelines.version}`,
    `Records: ${sot.length} from SOURCE_OF_TRUTH_REQUIREMENTS.yaml (SoT:), ${caches.length} Core requirements from CACHES.md (CACHES:).`,
    "",
  ];

  const locationLines = [
    "## Memory locations (F1, F2)",
    "",
    "| location | path | state |",
    "|---|---|---|",
    ...locations.map(
      (one) =>
        `| ${one.name} | \`${one.path}\` | ${one.present ? "present" : "absent"}${
          one.present && one.children !== null ? ` (${one.children} item(s))` : ""
        } |`,
    ),
    "",
  ];

  const section = (title: string, list: readonly RequirementResult[]): string[] =>
    list.length === 0 ? [] : [`## ${title}`, "", ...list.map(line), ""];

  const body = [
    ...head,
    ...locationLines,
    ...unstagedLine(run.unstaged),
    "",
    "## The tool's own requirements",
    "",
    ...applicable(own).map(line),
    "",
    ...section("Results — MUST", applicable(sot.filter((one) => one.level === "MUST")).sort(byLevelThenId)),
    ...section("Results — SHOULD", applicable(sot.filter((one) => one.level === "SHOULD")).sort(byLevelThenId)),
    ...section("Results — guidance", applicable(sot.filter((one) => one.level === "guidance")).sort(byLevelThenId)),
    ...section("Results — CACHES.md Core requirements (no level in CACHES.md)", applicable(caches).sort(byLevelThenId)),
    ...needsReviewer(results),
    ...notes(run),
    "## This run",
    "",
    `- Report ${outFile ? `written to ${outFile}` : "printed to stdout (no --out)"}`,
    "- Read only: nothing was created, changed or deleted except the report; every git call used GIT_OPTIONAL_LOCKS=0 (F3)",
    "- The session-start hook is not installed: R2 leaves that harness change to the owner (R12.3)",
    "- Not calibrated on a real project: no project has been named to calibrate against (design-decisions.md 15)",
    `- Counts: ${count(results, "fail")} fail, ${count(results, "pass")} pass, ${count(results, "needs a reviewer")} needs a reviewer, ${count(results, "not applicable")} not applicable, ${count(results, "could not run")} could not run`,
    "- CACHES.md gives its requirements no level, so none of them gates the exit code (R3 counts MUSTs only)",
    "",
    ...notApplicable(results),
  ];
  return body.join("\n");
}

/** R1: the last section, holding every "not applicable" result in the same row format as the other sections. */
function notApplicable(results: readonly RequirementResult[]): string[] {
  const list = results.filter((result) => result.verdict === "not applicable").sort(byLevelThenId);
  if (list.length === 0) return ["## Not applicable", "", "- none", ""];
  return ["## Not applicable", "", ...list.map(line), ""];
}

function needsReviewer(results: readonly RequirementResult[]): string[] {
  const list = results.filter((result) => result.verdict === "needs a reviewer");
  if (list.length === 0) return ["## Needs a reviewer", "", "- none", ""];
  return [
    "## Needs a reviewer",
    "",
    ...list.map(
      (result) =>
        `- **${result.id}** (${result.level}) — fails if: ${result.failsIf || "(guidance)"} — why not the tool: ${result.evidence}`,
    ),
    "",
  ];
}

function notes(run: CheckRun): string[] {
  const lines: string[] = ["## Notes from tools/memory_index.py", ""];
  const all = [...run.indexTool.stdout, ...run.indexTool.stderr];
  if (all.length === 0) lines.push("- it printed nothing");
  for (const one of all) lines.push(`- \`${one}\``);
  if (run.notes.length > 0) {
    lines.push("", "## Notes from this tool", "");
    for (const one of run.notes) lines.push(`- ${one}`);
  }
  lines.push("");
  return lines;
}