import { requirementLines, uncheckedParts, type Requirement, type Status } from "./requirements.ts";
import type { Mismatch } from "./matcher.ts";
import type { ProcessResult, FileChange } from "./process.ts";

export type CaseResult = {
  id: string; source: string; requirement: Requirement; line: string; args: string[];
  status: Status; reasons: string[]; failures: Mismatch[]; answer: unknown;
  process: ProcessResult; isolation: boolean; changedFiles: FileChange[]; observedChanges?: FileChange[]; markerCreated?: boolean;
};
export type Observation = { id: string; requirement: Requirement; line: string; status: Status; reason?: string };

export function aggregateStatus(statuses: Status[]): Status {
  if (statuses.includes("NOT MET")) return "NOT MET";
  if (!statuses.length || statuses.includes("NOT CHECKED")) return "NOT CHECKED";
  return "MET";
}

export function assessModuleMaps(cases: CaseResult[]): Observation | undefined {
  const suffixes = ["packages/core/src/session", "packages/core/src/tool", "packages/ai"];
  const maps = cases.filter(result => result.requirement === "A1" && result.args[0] === "map");
  const checks = suffixes.map(suffix => maps.filter(result => {
    const firstFlag = result.args.findIndex(arg => arg.startsWith("--"));
    const paths = result.args.slice(1, firstFlag < 0 ? undefined : firstFlag).map(arg => arg.replaceAll("\\", "/").replace(/\/$/, ""));
    const hasPath = (expected: string) => paths.some(path => path === expected || path.endsWith("/" + expected));
    return hasPath(suffix) && (suffix !== "packages/core/src/tool" || hasPath("packages/core/src/permission.ts"));
  }));
  if (checks.some(check => !check.length)) return undefined;
  return { id: "A6-three-module-A1-checks", requirement: "A6", line: requirementLines.A6[0],
    status: aggregateStatus(checks.flatMap(check => check.map(result => result.status))),
    reason: "A6 is derived from A1 cases for the three specified opencode module-map commands." };
}

function totals(statuses: Status[]) {
  return Object.fromEntries((["MET", "NOT MET", "NOT CHECKED"] as const).map(status => [status, statuses.filter(item => item === status).length]));
}

export function buildReport(cases: CaseResult[], observations: Observation[], isolationProbe: ProcessResult) {
  const requirements = Object.entries(requirementLines).map(([requirement, lines]) => {
    const checks = lines.map(line => {
      const casesForLine = cases.filter(result => result.requirement === requirement && result.line === line);
      const observationsForLine = observations.filter(result => result.requirement === requirement && result.line === line);
      const status = aggregateStatus([...casesForLine.map(result => result.status), ...observationsForLine.map(result => result.status)]);
      const reasons = [...casesForLine.flatMap(result => result.reasons), ...observationsForLine.flatMap(result => result.reason ? [result.reason] : [])];
      if (!casesForLine.length && !observationsForLine.length) reasons.push(requirement === "A6" ? "No opencode case files for the three modules were supplied." : requirement === "L2" ? "P5 measures cost against reading; this evaluator does not measure L2." : "No case exercises this Fails-if line.");
      return { line, status, caseIds: casesForLine.map(result => result.id), observations: observationsForLine, reasons };
    });
    const unchecked = uncheckedParts.filter(part => part.requirement === requirement).map(part => part.reason);
    const status = aggregateStatus(checks.map(check => check.status));
    return { requirement, status, displayStatus: status === "MET" && unchecked.length ? "MET (tool part)" : status, unchecked, lines: checks.map(check => ({ ...check,
      displayStatus: check.status === "MET" && unchecked.length ? "MET (tool part)" : check.status, unchecked })) };
  });
  return {
    checker: "P2 Codex evaluator; authored independently of the future tool builder",
    scope: "MET records the fixture/case checks assigned to this evaluator, not a proof for all repositories. Canned-stub results test the evaluator, not a real code-map tool.",
    r1Scope: "R1 marker checks run only on the bundled fixtures; held-out and external copies have no runtime marker check.",
    requirements, cases, uncheckedParts, isolationProbe,
    totals: { requirements: totals(requirements.map(item => item.status)),
      lines: totals(requirements.flatMap(item => item.lines.map(line => line.status))), cases: totals(cases.map(result => result.status)) },
  };
}

export type Report = ReturnType<typeof buildReport>;

export function renderReport(report: Report): string {
  const rows = ["# Code-map evaluation", "", report.checker, "", report.scope, "", report.r1Scope, "", "| Requirement | Status | Unchecked part |", "|---|---|---|"];
  for (const requirement of report.requirements) rows.push(`| ${requirement.requirement} | ${requirement.displayStatus} | ${requirement.unchecked.join(" ")} |`);
  rows.push("", "## Fails-if lines", "");
  for (const requirement of report.requirements) {
    for (const line of requirement.lines) {
      rows.push(`- **${requirement.requirement} ${line.displayStatus}** — ${line.line}. Cases: ${line.caseIds.join(", ") || "none"}.`);
      if (line.unchecked.length) rows.push(`  - Unchecked: ${line.unchecked.join(" ")}`);
      for (const reason of [...new Set(line.reasons)]) rows.push(`  - ${reason}`);
    }
  }
  rows.push("", "## Failures", "");
  for (const result of report.cases.filter(result => result.status === "NOT MET")) {
    rows.push(`### ${result.id} (${result.requirement})`, "", `Case file: ${result.source}`, "", `Arguments: \`${JSON.stringify(result.args)}\``, "",
      `Exit: ${result.process.exitCode}. Isolation: ${result.isolation}.`, "", "```json", JSON.stringify(result.failures, null, 2), "```", "",
      "Tool stdout:", "```text", result.process.stdout, "```", "Tool stderr:", "```text", result.process.stderr, "```", "");
  }
  rows.push("## Parts not checked", "");
  for (const part of report.uncheckedParts) rows.push(`- **${part.requirement} ${part.status}** — ${part.reason}`);
  rows.push("", "## Totals", "", "```json", JSON.stringify(report.totals, null, 2), "```", "");
  return rows.join("\n");
}
