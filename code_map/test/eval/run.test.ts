import { afterEach, expect, test } from "bun:test";
import { mkdir, mkdtemp, readFile, rm, symlink, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { evaluate, parseArguments } from "../../eval/run.ts";
import { captureProcess, shellQuote, snapshotFiles, compareSnapshots } from "../../eval/process.ts";
import { requirementLines } from "../../eval/requirements.ts";
import { loadCaseFile } from "../../eval/case-file.ts";

const packageDir = resolve(import.meta.dir, "../..");
const evalDir = resolve(packageDir, "eval");
const casePath = resolve(evalDir, "cases/fixtures.json");
const tool = `${shellQuote(process.execPath)} ${shellQuote(resolve(evalDir, "stub/stub.ts"))}`;
const scratchPaths: string[] = [];
async function scratch() {
  const path = await mkdtemp(resolve(import.meta.dir, ".scratch-"));
  scratchPaths.push(path); return path;
}
afterEach(async () => {
  for (const path of scratchPaths.splice(0)) await rm(path, { recursive: true, force: true });
});

test("CLI options accept repeated cases, use fixtures by default, reject unknown/missing options", () => {
  expect(parseArguments(["--tool", "bun tool.ts", "--out", "out"]).cases).toEqual([casePath]);
  expect(parseArguments(["--cases", "a.json", "--tool", "bun tool.ts", "--cases", "b.json", "--out", "out"]).cases).toEqual(["a.json", "b.json"]);
  expect(() => parseArguments(["--tool", "bun tool.ts"])).toThrow();
  expect(() => parseArguments(["--tool", "bun tool.ts", "--out"])).toThrow();
  expect(() => parseArguments(["--unknown", "x"])).toThrow();
});

test("shell arguments preserve metacharacters as literal data", async () => {
  const cwd = await scratch();
  const value = "line\n' ; $(touch ACCIDENTAL_WRITE) `touch ACCIDENTAL_WRITE`";
  const script = 'console.log(JSON.stringify(process.argv.slice(1)))';
  const result = await captureProcess(["sh", "-c", `${shellQuote(process.execPath)} -e ${shellQuote(script)} ${shellQuote(value)}`], cwd);
  expect(result.exitCode).toBe(0);
  expect(JSON.parse(result.stdout)).toEqual([value]);
  expect(await Bun.file(resolve(cwd, "ACCIDENTAL_WRITE")).exists()).toBe(false);
});

test("filesystem snapshots find same-size edits, additions, deletions and symlink changes", async () => {
  const cwd = await scratch();
  await writeFile(resolve(cwd, "edit"), "one");
  await writeFile(resolve(cwd, "remove"), "old");
  await symlink("edit", resolve(cwd, "link"));
  const before = await snapshotFiles([cwd, cwd]);
  await writeFile(resolve(cwd, "edit"), "two");
  await rm(resolve(cwd, "remove"));
  await writeFile(resolve(cwd, "added"), "new");
  await rm(resolve(cwd, "link"));
  await symlink("added", resolve(cwd, "link"));
  const changes = compareSnapshots(before, await snapshotFiles([cwd]));
  for (const [name, change] of [["edit", "modified"], ["remove", "removed"], ["added", "added"], ["link", "modified"]] as const) {
    expect(changes).toContainEqual({ path: resolve(cwd, name), change });
  }
});

test("full stub run reports all exercised lines MET, A6/L2 NOT CHECKED, and preserves process evidence", async () => {
  const cwd = await scratch();
  const report = await evaluate({ tool, cases: [casePath], out: resolve(cwd, "report"), cwd });
  const available = report.isolationProbe.exitCode === 0;
  expect(report.totals.cases["NOT MET"]).toBe(0);
  expect(report.totals.lines.MET).toBe(available ? 18 : 17);
  expect(report.totals.lines["NOT CHECKED"]).toBe(available ? 2 : 3);
  for (const requirement of report.requirements) {
    if (requirement.requirement === "A6" || requirement.requirement === "L2" || (requirement.requirement === "R3" && !available)) expect(requirement.status).toBe("NOT CHECKED");
    else expect(requirement.status).toBe("MET");
  }
  expect(report.cases).toHaveLength((await loadCaseFile(casePath)).cases.length);
  expect(report.cases.every(result => result.process.exitCode === 0 && result.process.stdout.length > 0 && result.changedFiles.length === 0)).toBe(true);
  expect(await Bun.file(resolve(cwd, "report/report.md")).exists()).toBe(true);
  const persisted = JSON.parse(await readFile(resolve(cwd, "report/report.json"), "utf8"));
  expect(persisted.totals).toEqual(report.totals);
  expect(persisted.uncheckedParts.every((part: any) => part.status === "NOT CHECKED")).toBe(true);
}, 30_000);

test("breaking an editable canned answer is detected even for duplicate commands", async () => {
  const cwd = await scratch();
  const answerPath = resolve(evalDir, "stub/answers/R2-test-fake.json");
  const original = await readFile(answerPath, "utf8");
  const broken = JSON.parse(original); broken.links[0].candidates[1].testFake = false;
  try {
    await writeFile(answerPath, JSON.stringify(broken));
    const loaded = await loadCaseFile(casePath);
    const caseFile = resolve(cwd, "cases.json");
    await writeFile(caseFile, JSON.stringify({ ...loaded, cases: loaded.cases.filter(sample => sample.id === "R2-test-fake") }));
    const report = await evaluate({ tool, cases: [caseFile], out: resolve(cwd, "report"), cwd });
    expect(report.cases[0]!.status).toBe("NOT MET");
    expect(report.cases[0]!.process.stderr).toContain("Conflicting canned answers");
    expect(report.cases[0]!.failures.length).toBeGreaterThan(0);
  } finally { await writeFile(answerPath, original); }
}, 30_000);

test("R1 executes the marker check, detects an importing tool and removes the marker", async () => {
  const cwd = await scratch();
  const importingTool = resolve(cwd, "importing-tool.ts");
  await writeFile(importingTool, `await import(${JSON.stringify(resolve(evalDir, "fixtures/marker/main.ts"))});\nconsole.log(JSON.stringify({command: 'map', limits: [], empty: 'none found by static analysis'}));\n`);
  const loaded = await loadCaseFile(casePath);
  const originalCase = loaded.cases.find(sample => sample.id === "R1-map")!;
  const caseFile = resolve(cwd, "cases.json");
  await writeFile(caseFile, JSON.stringify({ ...loaded, cases: [{ ...originalCase,
    expect: { includes: [], excludes: [], equals: [], ambiguous: null, limitReasons: [] } }] }));
  const report = await evaluate({ tool: `${shellQuote(process.execPath)} ${shellQuote(importingTool)}`, cases: [caseFile], out: resolve(cwd, "report"), cwd });
  expect(report.cases[0]!.markerCreated).toBe(true);
  expect(report.requirements.find(item => item.requirement === "R1")!.status).toBe("NOT MET");
  expect(report.cases[0]!.failures.some(failure => failure.path === "$marker")).toBe(true);
  expect(await Bun.file(resolve(evalDir, "fixtures/marker/EXECUTED.marker")).exists()).toBe(false);
}, 30_000);

test("R3 detects a tool write in the working directory", async () => {
  const cwd = await scratch();
  const target = resolve(cwd, "target"); await mkdir(target);
  const writingTool = resolve(cwd, "writing-tool.ts");
  await writeFile(writingTool, "await Bun.write('UNAUTHORIZED', 'changed'); console.log(JSON.stringify({command:'where',limits:[],empty:'none found by static analysis'}));");
  const caseFile = resolve(cwd, "cases.json");
  await writeFile(caseFile, JSON.stringify({ project: [resolve(target, "tsconfig.json")], root: target, tests: [], cases: [{ id: "writes", requirement: "R3", line: requirementLines.R3[0], args: ["where", "x"], expect: { includes: [], excludes: [], equals: [], ambiguous: null, limitReasons: [] } }] }));
  const report = await evaluate({ tool: `${shellQuote(process.execPath)} ${shellQuote(writingTool)}`, cases: [caseFile], out: resolve(cwd, "report"), cwd });
  expect(report.cases[0]!.changedFiles.some(change => change.path === resolve(cwd, "UNAUTHORIZED"))).toBe(true);
  expect(report.cases[0]!.failures.some(failure => failure.path === "$filesystem")).toBe(true);
  expect(report.requirements.find(item => item.requirement === "R3")!.status).toBe("NOT MET");
}, 30_000);

test("unavailable unshare records exit/output and reports R3 NOT CHECKED", async () => {
  const cwd = await scratch();
  const target = resolve(cwd, "target"); await mkdir(target);
  const bins = resolve(cwd, "bin"); await mkdir(bins); await symlink("/bin/sh", resolve(bins, "sh"));
  const caseFile = resolve(cwd, "cases.json");
  await writeFile(caseFile, JSON.stringify({ project: [resolve(target, "tsconfig.json")], root: target, tests: [], cases: [{ id: "offline", requirement: "R3", line: requirementLines.R3[0], args: ["where", "unknown"], expect: { includes: [], excludes: [], equals: [], ambiguous: null, limitReasons: [] } }] }));
  const out = resolve(cwd, "report");
  const child = Bun.spawn([process.execPath, resolve(evalDir, "run.ts"), "--tool", tool, "--cases", caseFile, "--out", out], {
    cwd, env: { ...process.env, PATH: bins }, stdout: "pipe", stderr: "pipe",
  });
  const [exit, stdout, stderr] = await Promise.all([child.exited, new Response(child.stdout).text(), new Response(child.stderr).text()]);
  expect({ exit, stderr }).toEqual({ exit: 0, stderr: "" });
  expect(stdout).toContain("NOT CHECKED");
  const report = JSON.parse(await readFile(resolve(out, "report.json"), "utf8"));
  expect(report.isolationProbe.exitCode).not.toBe(0);
  expect(report.isolationProbe.stderr.length).toBeGreaterThan(0);
  expect(report.requirements.find((item: any) => item.requirement === "R3").status).toBe("NOT CHECKED");
  expect(report.cases[0].reasons.join(" ")).toContain("unshare -rn unavailable");
}, 30_000);

test("stub fallback is exactly the required empty static-analysis response", async () => {
  const result = await captureProcess([process.execPath, resolve(evalDir, "stub/stub.ts"), "where", "not-a-fixture-command"], packageDir);
  expect(result.exitCode).toBe(0);
  expect(JSON.parse(result.stdout)).toEqual({ command: "where", limits: [], empty: "none found by static analysis" });
});

test("R1/R3 judge observations despite incorrect JSON, and faults leave other requirement statuses unchanged", async () => {
  const cwd = await scratch();
  const loaded = await loadCaseFile(casePath);
  const caseFile = resolve(cwd, "observations.json");
  const samples = loaded.cases.filter(sample => ["R1-map", "R3-offline", "A5-specific-answer"].includes(sample.id));
  await writeFile(caseFile, JSON.stringify({ ...loaded, cases: samples }));
  const answer = JSON.parse(await readFile(resolve(evalDir, "stub/answers/A5-specific-answer.json"), "utf8"));
  const marker = resolve(evalDir, "fixtures/marker/EXECUTED.marker");
  const toolPath = resolve(cwd, "observations.ts");
  const makeTool = async (fault: "none" | "marker" | "write" | "exit") => {
    await writeFile(toolPath, `
      const command = process.argv[2];
      if (${JSON.stringify(fault)} === "marker") await Bun.write(${JSON.stringify(marker)}, "executed");
      if (${JSON.stringify(fault)} === "write") await Bun.write("UNAUTHORIZED", String(Math.random()));
      if (${JSON.stringify(fault)} === "exit") process.exitCode = 1;
      // Safety cases deliberately receive invalid JSON. Only the A5 question gets its correct answer.
      console.log(command === "where" && process.argv[3] === "leaf" ? ${JSON.stringify(JSON.stringify(answer))} : "wrong answer");
    `);
  };
  const run = async () => evaluate({ tool: `${shellQuote(process.execPath)} ${shellQuote(toolPath)}`, cases: [caseFile], out: resolve(cwd, "report"), cwd });
  await makeTool("none"); const baseline = await run();
  expect(baseline.cases.find(sample => sample.requirement === "R1")!.status).toBe("MET");
  expect(baseline.cases.find(sample => sample.requirement === "R3")!.status).toBe(baseline.isolationProbe.exitCode === 0 ? "MET" : "NOT CHECKED");
  const statuses = (report: typeof baseline, omit: string) => report.requirements.filter(item => item.requirement !== omit).map(item => [item.requirement, item.status]);
  await makeTool("marker"); const r1Fault = await run();
  expect(r1Fault.requirements.find(item => item.requirement === "R1")!.status).toBe("NOT MET");
  expect(statuses(r1Fault, "R1")).toEqual(statuses(baseline, "R1"));
  expect(r1Fault.cases.find(sample => sample.requirement === "A5")!.failures).toEqual([]);
  await makeTool("exit"); const exitFault = await run();
  expect(exitFault.requirements.find(item => item.requirement === "R1")!.status).toBe("NOT MET");
  expect(statuses(exitFault, "R1")).toEqual(statuses(baseline, "R1"));
  await makeTool("write"); const r3Fault = await run();
  expect(r3Fault.requirements.find(item => item.requirement === "R3")!.status).toBe("NOT MET");
  expect(statuses(r3Fault, "R3")).toEqual(statuses(baseline, "R3"));
  expect(r3Fault.cases.find(sample => sample.requirement === "A5")!.failures).toEqual([]);
}, 30_000);

test("top-level throw fixture is not executed by the stub, and an importing tool fails R1", async () => {
  const cwd = await scratch();
  const loaded = await loadCaseFile(casePath);
  const caseFile = resolve(cwd, "throws.json");
  await writeFile(caseFile, JSON.stringify({ ...loaded, cases: loaded.cases.filter(sample => sample.id === "R1-top-level-throws") }));
  const baseline = await evaluate({ tool, cases: [caseFile], out: resolve(cwd, "safe"), cwd });
  expect(baseline.cases[0]!.status).toBe("MET");
  const importing = resolve(cwd, "throws.ts");
  await writeFile(importing, `await import(${JSON.stringify(resolve(evalDir, "fixtures/marker/throws.ts"))});`);
  const failed = await evaluate({ tool: `${shellQuote(process.execPath)} ${shellQuote(importing)}`, cases: [caseFile], out: resolve(cwd, "failed"), cwd });
  expect(failed.cases[0]!.process.exitCode).not.toBe(0);
  expect(failed.cases[0]!.status).toBe("NOT MET");
  expect(failed.cases[0]!.failures.some(failure => failure.path === "$process.exitCode")).toBe(true);
  expect(failed.cases[0]!.process.stderr).toContain("fixture top level must never run");
}, 30_000);
