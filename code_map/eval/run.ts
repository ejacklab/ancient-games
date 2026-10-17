import { mkdir, rm, writeFile } from "node:fs/promises";
import { resolve, dirname } from "node:path";
import { loadCaseFile, type LoadedCaseFile, type EvalCase } from "./case-file.ts";
import { validateAnswer } from "./contract.ts";
import { matchAnswer, type Mismatch } from "./matcher.ts";
import { captureProcess, compareSnapshots, shellQuote, snapshotFiles, type ProcessResult } from "./process.ts";
import { assessModuleMaps, buildReport, renderReport, type CaseResult, type Observation } from "./report.ts";
import { requirementLines } from "./requirements.ts";

export type EvalOptions = { tool: string; cases: string[]; out: string; cwd?: string };

export function parseArguments(args: string[]): EvalOptions {
  let tool = ""; let out = ""; const cases: string[] = [];
  for (let index = 0; index < args.length; index++) {
    const flag = args[index]; const value = args[++index];
    if (!value || !["--tool", "--cases", "--out"].includes(flag!)) throw new Error("Usage: bun eval/run.ts --tool <command> [--cases <file>]... --out <dir>");
    if (flag === "--tool") tool = value;
    else if (flag === "--out") out = value;
    else cases.push(value);
  }
  if (!tool.trim() || !out) throw new Error("--tool and --out are required");
  if (!cases.length) cases.push(resolve(import.meta.dir, "cases/fixtures.json"));
  return { tool, out: resolve(out), cases };
}

export function toolArguments(file: LoadedCaseFile, test: EvalCase): string[] {
  return [...test.args, ...file.project.flatMap(project => ["--project", project]), "--root", file.root,
    ...(test.tests ?? file.tests).flatMap(pattern => ["--tests", pattern]), ...(test.format === "text" ? [] : ["--json"])];
}

async function evaluateCase(options: EvalOptions, file: LoadedCaseFile, test: EvalCase, probe: ProcessResult): Promise<CaseResult> {
  const cwd = options.cwd ?? process.cwd();
  const args = toolArguments(file, test);
  const marker = file.root === resolve(import.meta.dir, "fixtures") ? resolve(file.root, "marker/EXECUTED.marker") : undefined;
  if (marker) await rm(marker, { force: true });
  const before = await snapshotFiles([file.root, cwd]);
  const command = `${options.tool} ${args.map(shellQuote).join(" ")}`;
  const isolation = probe.exitCode === 0;
  const processResult = await captureProcess(isolation ? ["unshare", "-rn", "--", "sh", "-c", command] : ["sh", "-c", command], cwd);
  const after = await snapshotFiles([file.root, cwd]);
  const observedChanges = compareSnapshots(before, after);
  const markerCreated = marker ? await Bun.file(marker).exists() : undefined;
  if (marker) await rm(marker, { force: true });
  // The deliberate R1 marker has its own verdict; its creation must not contaminate R3.
  const changedFiles = observedChanges.filter(change => !markerCreated || (change.path !== marker && change.path !== dirname(marker!)));
  const failures: Mismatch[] = [];
  let answer: unknown = null;
  try {
    answer = test.format === "text" ? processResult.stdout : JSON.parse(processResult.stdout);
    failures.push(...matchAnswer(answer, test.expect));
    if (test.format !== "text") failures.push(...validateAnswer(answer, test.args, test.tests ?? file.tests, file.root));
    else if (!processResult.stdout.trim()) failures.push({ path: "$stdout", expected: "nonempty default text answer", actual: processResult.stdout, message: "text answer missing" });
  } catch (error) {
    failures.push({ path: "$stdout", expected: "one JSON Answer", actual: processResult.stdout, message: String(error) });
  }
  const reasons: string[] = [];
  let status: CaseResult["status"];
  if (test.requirement === "R1") {
    failures.length = 0;
    if (processResult.exitCode !== 0) failures.push({ path: "$process.exitCode", expected: 0, actual: processResult.exitCode, message: "R1 reading must succeed even when top-level source throws" });
    if (markerCreated) failures.push({ path: "$marker", expected: "marker absent", actual: marker, message: "R1 repository source was executed" });
    if (!marker) reasons.push("Runtime R1 marker checks use only bundled fixtures, not held-out or external copies.");
    status = failures.length ? "NOT MET" : marker ? "MET" : "NOT CHECKED";
  } else if (test.requirement === "R3") {
    failures.length = 0;
    if (changedFiles.length) failures.push({ path: "$filesystem", expected: "no writes under root or working directory", actual: changedFiles, message: "R3 filesystem changed" });
    if (!isolation) reasons.push(`unshare -rn unavailable (exit ${probe.exitCode}): ${probe.stderr.trim()}`);
    status = failures.length ? "NOT MET" : isolation ? "MET" : "NOT CHECKED";
  } else {
    if (test.requirement === "L2") reasons.push("P5 measures L2; matching a code-map answer cannot establish its cost against reading.");
    if (!test.expect.includes.length && !test.expect.excludes.length && !test.expect.equals.length &&
        !test.expect.shapes?.length && test.expect.exactLimitReasons === undefined &&
        test.expect.ambiguous === null && !test.expect.limitReasons.length && !test.expect.textIncludes?.length) reasons.push("No expectation exercises this Fails-if line.");
    status = test.requirement === "L2" ? "NOT CHECKED" : failures.length ? "NOT MET" : reasons.length ? "NOT CHECKED" : "MET";
  }
  return { id: test.id, source: file.source, requirement: test.requirement, line: test.line,
    args, status, reasons, failures, answer, process: processResult, isolation, changedFiles, observedChanges, markerCreated };
}

export async function evaluate(options: EvalOptions) {
  const files = await Promise.all(options.cases.map(loadCaseFile));
  const probe = await captureProcess(["unshare", "-rn", "--", "true"], options.cwd ?? process.cwd());
  const results: CaseResult[] = [];
  const observations: Observation[] = [];
  // Sequential runs make before/after snapshots attributable to one tool invocation.
  for (const file of files) for (const test of file.cases) {
    const result = await evaluateCase(options, file, test, probe);
    results.push(result);
    observations.push({ id: result.id, requirement: "R3", line: requirementLines.R3[0],
      status: result.changedFiles.length ? "NOT MET" : probe.exitCode !== 0 ? "NOT CHECKED" : "MET",
      reason: probe.exitCode !== 0 ? `unshare -rn unavailable (exit ${probe.exitCode}): ${probe.stderr.trim()}` :
        result.changedFiles.length ? "Tool changed files under root or working directory; see case evidence." : undefined });
    if (result.markerCreated !== undefined) observations.push({ id: result.id, requirement: "R1", line: requirementLines.R1[0],
      status: result.markerCreated || result.process.exitCode !== 0 ? "NOT MET" : "MET",
      reason: result.markerCreated ? "The tool created the marker; see case evidence. The evaluator removed it." :
        result.process.exitCode !== 0 ? "The tool did not exit 0 while reading bundled source." : undefined });
  }
  const markerCommands = new Set(results.filter(result => result.markerCreated !== undefined).map(result => result.args[0] === "tests" && result.args.includes("--file") ? "tests --file" : result.args[0]));
  if (markerCommands.size) {
    const missing = ["where", "find", "callers", "callees", "chain", "tests", "tests --file", "map"].filter(command => !markerCommands.has(command));
    observations.push({ id: "R1-required-commands", requirement: "R1", line: requirementLines.R1[0],
      status: missing.length ? "NOT CHECKED" : "MET", reason: missing.length ? `Marker fixture was not checked with: ${missing.join(", ")}.` : undefined });
  }
  const moduleAssessment = assessModuleMaps(results);
  for (const result of results.filter(result => result.requirement === "A6")) {
    if (result.status === "NOT MET") continue;
    if (!moduleAssessment || moduleAssessment.status === "NOT CHECKED") {
      result.status = "NOT CHECKED";
      result.reasons.push("A6 needs A1 map checks for all three opencode modules, including tool with permission.ts.");
    } else if (moduleAssessment.status === "NOT MET") {
      result.status = "NOT MET";
      result.failures.push({ path: "$A6", expected: "A1 passes for all three opencode module maps", actual: moduleAssessment, message: "A module map failed A1" });
    }
  }
  if (moduleAssessment) observations.push(moduleAssessment);
  const report = buildReport(results, observations, probe);
  await mkdir(options.out, { recursive: true });
  await writeFile(resolve(options.out, "report.json"), JSON.stringify(report, null, 2) + "\n");
  await writeFile(resolve(options.out, "report.md"), renderReport(report));
  return report;
}

if (import.meta.main) {
  try {
    const options = parseArguments(Bun.argv.slice(2));
    const report = await evaluate(options);
    console.log("Requirements:", JSON.stringify(report.totals.requirements));
    console.log("Fails-if lines:", JSON.stringify(report.totals.lines));
    console.log("Cases:", JSON.stringify(report.totals.cases));
    console.log("Report:", resolve(options.out, "report.json"));
    if (report.requirements.some(result => result.status === "NOT MET")) process.exitCode = 1;
  } catch (error) {
    console.error(String(error)); process.exitCode = 2;
  }
}
