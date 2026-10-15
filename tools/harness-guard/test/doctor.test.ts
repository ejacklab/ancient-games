import { afterEach, beforeEach, describe, expect, spyOn, test } from "bun:test";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { doctor } from "../src/doctor.ts";
import type { DoctorHarness, DoctorReport } from "../src/types.ts";

const secret = "SECRET-PLANT-7f3a9c";
const harnesses = ["claude-code", "codex", "qwen", "opencode"];
const settings = [
  ["claude-code", "home/.claude/settings.json"],
  ["claude-code", "project/.claude/settings.json"],
  ["claude-code", "project/.claude/settings.local.json"],
  ["codex", "home/.codex/hooks.json"],
  ["codex", "home/.codex/config.toml"],
  ["qwen", "home/.qwen/settings.json"],
  ["opencode", "home/.config/opencode/plugin/guard.ts"],
  ["opencode", "home/.config/opencode/plugins/guard.ts"],
  ["opencode", "project/.opencode/plugin/guard.ts"],
  ["opencode", "project/.opencode/plugins/guard.ts"],
];
let folder: string;
let home: string;
let projectRoot: string;

beforeEach(() => {
  folder = fs.mkdtempSync(path.join(os.tmpdir(), "hg-"));
  home = path.join(folder, "home");
  projectRoot = path.join(folder, "project");
  fs.mkdirSync(home);
  fs.mkdirSync(projectRoot);
});

afterEach(() => {
  fs.rmSync(folder, { recursive: true, force: true });
});

function writeFile(name: string, text: string): string {
  const file = path.join(folder, name);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, text);
  return file;
}

function config(name: string, command: string): string {
  if (name.endsWith(".ts")) return `export const command = ${JSON.stringify(command)};\n`;
  if (name.endsWith(".toml")) {
    return `[hooks]\nPreToolUse = [{ matcher = "Bash", hooks = [{ type = "command", command = ${JSON.stringify(command)} }] }]\n`;
  }
  return JSON.stringify({ hooks: { PreToolUse: [{ matcher: "Bash", hooks: [{ type: "command", command }] }] } });
}

function row(report: DoctorReport, harness: string): DoctorHarness {
  expect(report.harnesses.map((entry: DoctorHarness) => entry.harness).sort()).toEqual([...harnesses].sort());
  const found = report.harnesses.find((entry: DoctorHarness) => entry.harness === harness);
  expect(found).toBeDefined();
  return found!;
}

function expectNoSecret(action: () => DoctorReport): DoctorReport {
  const printed: string[] = [];
  const spies = [
    spyOn(console, "log").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(console, "warn").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(console, "error").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(process.stdout, "write").mockImplementation((chunk) => { printed.push(String(chunk)); return true; }),
    spyOn(process.stderr, "write").mockImplementation((chunk) => { printed.push(String(chunk)); return true; }),
  ];
  let report: DoctorReport;
  try { report = action(); } finally { for (const spy of spies) spy.mockRestore(); }
  expect(JSON.stringify(report)).not.toContain(secret);
  expect(printed.join("\n")).not.toContain(secret);
  for (const root of [home, projectRoot]) {
    const state = path.join(root, ".harness-guard");
    if (!fs.existsSync(state)) continue;
    for (const name of fs.readdirSync(state, { recursive: true, encoding: "utf8" })) {
      const file = path.join(state, name);
      expect(name).not.toContain(secret);
      if (fs.statSync(file).isFile()) expect(fs.readFileSync(file, "utf8")).not.toContain(secret);
    }
  }
  return report;
}

describe("doctor settings", () => {
  test("doctor: missing files are absent, and the planted trap answers on every harness", () => {
    const calls: string[][] = [];
    const report: DoctorReport = doctor({ home, projectRoot, run: (argv: string[]) => {
      calls.push(argv);
      return { code: 0, stdout: "{}" };
    } });
    for (const harness of harnesses) expect(row(report, harness)).toMatchObject({ guard: "absent", answers: true });
    expect(report.health).toBeNull();
    expect(calls).toEqual([]);
  });

  test.each(settings)("doctor: %s is installed from a guard command in %s", (harness: string, name: string) => {
    writeFile(name, config(name, "bun /opt/harness-guard/src/cli.ts hook claude"));
    const report = doctor({ home, projectRoot });
    expect(row(report, harness)).toMatchObject({ guard: "installed", answers: true });
    for (const other of harnesses.filter((entry) => entry !== harness)) expect(row(report, other).guard).toBe("absent");
  });

  test.each(settings)("doctor: %s is absent when %s has no guard", (harness: string, name: string) => {
    writeFile(name, config(name, "echo another-hook"));
    expect(row(doctor({ home, projectRoot }), harness)).toMatchObject({ guard: "absent", answers: true });
  });

  test.each(settings.filter(([, name]) => name!.endsWith(".json") || name!.endsWith(".toml")))(
    "doctor: %s reports an unparseable %s as unknown",
    (harness: string, name: string) => {
      writeFile(name, name.endsWith(".toml") ? "[hooks\ncommand = [" : '{"hooks":');
      expect(row(doctor({ home, projectRoot }), harness)).toMatchObject({ guard: "unknown", answers: true });
    },
  );

  test.each(settings)("doctor: %s reports an unreadable %s as unknown", (harness: string, name: string) => {
    const file = writeFile(name, config(name, "echo another-hook"));
    const readFile = fs.readFileSync;
    const spy = spyOn(fs, "readFileSync").mockImplementation(((...args: Parameters<typeof fs.readFileSync>) => {
      if (String(args[0]) === file) throw Object.assign(new Error("permission denied"), { code: "EACCES" });
      return readFile(...args);
    }) as typeof fs.readFileSync);
    let report: DoctorReport;
    try { report = doctor({ home, projectRoot }); } finally { spy.mockRestore(); }
    expect(row(report, harness)).toMatchObject({ guard: "unknown", answers: true });
  });

  test.each(settings.filter(([, name]) => name!.endsWith(".json")))(
    "doctor: %s does not mistake a non-hook value in %s for installation",
    (harness: string, name: string) => {
      writeFile(name, JSON.stringify({ token: `harness-guard ${secret}`, hooks: {} }));
      const report = expectNoSecret(() => doctor({ home, projectRoot }));
      expect(row(report, harness).guard).toBe("absent");
    },
  );
});

describe("doctor health", () => {
  test.each([0, 2])("doctor: exit zero with JSON reports %s findings without raw settings or script text", (count: number) => {
    writeFile("home/.claude/settings.json", JSON.stringify({ token: secret, hooks: {} }));
    const healthScript = writeFile("health.py", `# ${secret}\n`);
    const calls: string[][] = [];
    const report = expectNoSecret(() => doctor({ home, projectRoot, healthScript, run: (argv: string[]) => {
      calls.push(argv);
      return { code: 0, stdout: JSON.stringify({ findings: Array.from({ length: count }, () => ({ message: secret })), raw: secret }) };
    } }));
    expect(calls).toEqual([["python3", healthScript, "--json"]]);
    expect(report.health).toEqual({ ok: true, summary: `${count} findings` });
  });

  test.each([
    [7, JSON.stringify({ findings: [], raw: secret })],
    [0, `not JSON ${secret}`],
    [7, `script failed ${secret}`],
  ])("doctor: health exit %s with output %j reports an error kind without script text", (code: number, stdout: string) => {
    const healthScript = writeFile("health.py", `# ${secret}\n`);
    const report = expectNoSecret(() => doctor({ home, projectRoot, healthScript, run: () => ({ code, stdout }) }));
    expect(report.health).not.toBeNull();
    expect(report.health!.ok).toBe(false);
    expect(report.health!.summary.trim().length).toBeGreaterThan(0);
    expect(report.health!.summary).not.toContain(stdout);
  });

  test("doctor: a null health script does not run a process", () => {
    const calls: string[][] = [];
    const report = doctor({ home, projectRoot, healthScript: null, run: (argv: string[]) => {
      calls.push(argv);
      return { code: 0, stdout: '{"findings":[]}' };
    } });
    expect(report.health).toBeNull();
    expect(calls).toEqual([]);
  });
});
