import { expect, test } from "bun:test";
import { aggregateStatus, assessModuleMaps, buildReport, renderReport, type CaseResult } from "../../eval/report.ts";
import { requirementLines } from "../../eval/requirements.ts";

const probe = { command: ["unshare", "-rn", "true"], exitCode: 0, stdout: "", stderr: "" };
function result(status: CaseResult["status"], line: string = requirementLines.R2[0]): CaseResult {
  return { id: "case", source: "cases.json", requirement: "R2", line, args: ["callees", "x"], status,
    reasons: [], failures: [], answer: {}, process: probe, isolation: true, changedFiles: [] };
}

test("NOT MET wins, absent and unchecked inputs are never MET", () => {
  expect(aggregateStatus([])).toBe("NOT CHECKED");
  expect(aggregateStatus(["MET", "NOT CHECKED"])).toBe("NOT CHECKED");
  expect(aggregateStatus(["NOT CHECKED", "NOT MET", "MET"])).toBe("NOT MET");
  expect(aggregateStatus(["MET", "MET"])).toBe("MET");
});

test("a requirement needs every line; an unexercised line stays NOT CHECKED", () => {
  const report = buildReport([result("MET")], [], probe);
  const r2 = report.requirements.find(item => item.requirement === "R2")!;
  expect(r2.status).toBe("NOT CHECKED");
  expect(r2.lines.map(line => line.status)).toEqual(["MET", "NOT CHECKED", "NOT CHECKED", "NOT CHECKED"]);
  expect(report.requirements.find(item => item.requirement === "A6")!.status).toBe("NOT CHECKED");
  expect(report.requirements.find(item => item.requirement === "L2")!.status).toBe("NOT CHECKED");
  const all = buildReport(requirementLines.R2.map(line => result("MET", line)), [], probe);
  expect(all.requirements.find(item => item.requirement === "R2")!.status).toBe("MET");
  expect(buildReport([result("MET"), result("NOT MET")], [], probe).requirements.find(item => item.requirement === "R2")!.status).toBe("NOT MET");
});

test("failure report includes case, arguments, expected/actual and process evidence", () => {
  const failed = result("NOT MET");
  failed.failures.push({ path: "links[].to", expected: "real.ts:4", actual: "fake.ts:9", message: "wrong target" });
  failed.process = { ...probe, exitCode: 7, stdout: "bad answer", stderr: "connection failed" };
  const markdown = renderReport(buildReport([failed], [], probe));
  for (const text of ["case", "callees", "real.ts:4", "fake.ts:9", "bad answer", "connection failed", "P6", "P2 Codex"]) expect(markdown).toContain(text);
});

test("A6 requires all three A1 module maps, including permission, and preserves unchecked/failure status", () => {
  const moduleMap = (path: string, status: CaseResult["status"] = "MET"): CaseResult => ({ ...result(status),
    requirement: "A1", line: requirementLines.A1[0], args: ["map", path] });
  const maps = [moduleMap("opencode/packages/core/src/session"), moduleMap("opencode/packages/core/src/tool"), moduleMap("opencode/packages/ai")];
  expect(assessModuleMaps(maps)).toBeUndefined();
  maps[1]!.args.push("opencode/packages/core/src/permission.ts");
  expect(assessModuleMaps(maps)!.status).toBe("MET");
  expect(assessModuleMaps(maps.slice(0, 2))).toBeUndefined();
  maps[2]!.status = "NOT CHECKED";
  expect(assessModuleMaps(maps)!.status).toBe("NOT CHECKED");
  maps[0]!.status = "NOT MET";
  expect(assessModuleMaps(maps)!.status).toBe("NOT MET");
  maps[0]!.args = ["where", "opencode/packages/core/src/session"];
  expect(assessModuleMaps(maps)).toBeUndefined();
});

test("MET tool parts name their unchecked portions in JSON and beside Markdown verdicts", () => {
  const samples: CaseResult[] = ["R3", "A2", "A3", "A5"].flatMap(requirement => {
    const key = requirement as "R3" | "A2" | "A3" | "A5";
    return requirementLines[key].map(line => ({ ...result("MET", line), requirement: key }));
  });
  const report = buildReport(samples, [], probe);
  const markdown = renderReport(report);
  for (const key of ["R3", "A2", "A3", "A5"]) {
    const requirement = report.requirements.find(item => item.requirement === key)!;
    expect(requirement.status).toBe("MET");
    expect(requirement.displayStatus).toBe("MET (tool part)");
    expect(requirement.unchecked.length).toBeGreaterThan(0);
    expect(markdown).toContain(`| ${key} | MET (tool part) | ${requirement.unchecked.join(" ")} |`);
    expect(requirement.lines.every(line => line.displayStatus === "MET (tool part)" && line.unchecked.length > 0)).toBe(true);
  }
  for (const part of ["caught connection attempts", "writes outside", "git", "training", "selection", "asks", "without being asked"]) expect(markdown).toContain(part);
  expect(markdown).toContain("R1 marker checks run only on the bundled fixtures");
});
