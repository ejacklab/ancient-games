import { afterEach, beforeEach, describe, expect, spyOn, test } from "bun:test";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import {
  catalogueProblems,
  checkResult,
  lintCommand,
  loadEngines,
  loadTraps,
  recognizeEngineCall,
} from "../src/traps.ts";
import type { EngineCall, EngineSpec, Finding, LintContext, ResultInput, Trap } from "../src/types.ts";

const secret = "SECRET-PLANT-7f3a9c";
let folder: string;

beforeEach(() => {
  folder = fs.mkdtempSync(path.join(os.tmpdir(), "hg-"));
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

function commandTrap(changes: Partial<Trap> = {}): Trap {
  return {
    id: "fixture",
    status: "approved",
    applies: "command",
    engine: "fixture",
    command: "\\bfixture run\\b",
    why: "fixture command failed its condition",
    fix: "satisfy the fixture condition",
    source: "fixture catalogue",
    ...changes,
  };
}

function lintContext(changes: Partial<LintContext> = {}): LintContext {
  return { repoRoot: path.join(folder, "repo"), running: [], ...changes };
}

function engineCall(changes: Partial<EngineCall> = {}): EngineCall {
  return {
    engine: "codex",
    outputFile: null,
    stdoutIsAnswer: false,
    statusFile: null,
    background: false,
    ...changes,
  };
}

function resultInput(changes: Partial<ResultInput> = {}): ResultInput {
  return {
    call: engineCall(),
    cwd: folder,
    exitCode: 0,
    stdout: "answer",
    stderr: "",
    interrupted: false,
    ...changes,
  };
}

function expectFailure(findings: Finding[], rule: string): void {
  expect(findings).toContainEqual(expect.objectContaining({ rule, severity: "fail" }));
  for (const finding of findings) expect(finding.severity).toBe("fail");
}

function expectNoSecret(action: () => unknown): void {
  const printed: string[] = [];
  const spies = [
    spyOn(console, "log").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(console, "warn").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(console, "error").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(process.stdout, "write").mockImplementation((chunk) => { printed.push(String(chunk)); return true; }),
    spyOn(process.stderr, "write").mockImplementation((chunk) => { printed.push(String(chunk)); return true; }),
  ];
  let output: unknown;
  try {
    output = action();
  } finally {
    for (const spy of spies) spy.mockRestore();
  }
  expect(JSON.stringify(output)).not.toContain(secret);
  expect(printed.join("\n")).not.toContain(secret);
  const state = path.join(folder, ".harness-guard");
  if (fs.existsSync(state)) {
    for (const name of fs.readdirSync(state, { recursive: true, encoding: "utf8" })) {
      const file = path.join(state, name);
      if (fs.statSync(file).isFile()) expect(fs.readFileSync(file, "utf8")).not.toContain(secret);
    }
  }
}

describe("catalogues", () => {
  test("catalogue: defaults load the package traps and engines without problems", () => {
    const trapFile = new URL("../data/traps.yaml", import.meta.url);
    const engineFile = new URL("../data/engines.yaml", import.meta.url);
    const traps = Bun.YAML.parse(fs.readFileSync(trapFile, "utf8")) as { traps: Trap[] };
    const engines = Bun.YAML.parse(fs.readFileSync(engineFile, "utf8")) as { engines: EngineSpec[] };
    expect(loadTraps()).toEqual(traps.traps);
    expect(loadEngines()).toEqual(engines.engines);
    expect(catalogueProblems()).toEqual([]);
  });

  test("catalogue: an explicit YAML trap file preserves approved and proposed entries", () => {
    const file = writeFile("traps.yaml", `traps:
  - id: local
    status: approved
    applies: command
    engine: fixture
    command: 'fixture run'
    why: local reason
    fix: local fix
    source: local source
  - id: suggestion
    status: proposed
    applies: result
    engine: any
    stderr: denied
    why: proposed reason
    fix: proposed fix
    source: proposed source
`);
    expect(loadTraps(file)).toEqual([
      commandTrap({ id: "local", command: "fixture run", why: "local reason", fix: "local fix", source: "local source" }),
      { id: "suggestion", status: "proposed", applies: "result", engine: "any", stderr: "denied",
        why: "proposed reason", fix: "proposed fix", source: "proposed source" },
    ]);
    expect(catalogueProblems(file)).toEqual([]);
  });

  test("catalogue: an explicit engine file retains optional recognition and result fields", () => {
    const engine: EngineSpec = {
      name: "fixture", command: "fixture run", output_flags: ["-o", "--out"],
      stdout_is_answer: true, status_from_out_dir: true,
      silent_failures: [{ text: "quiet denial", status: "denied" }],
    };
    const file = writeFile("engines.yaml", JSON.stringify({ engines: [engine] }));
    expect(loadEngines(file)).toEqual([engine]);
    expect(catalogueProblems(file)).toEqual([]);
  });

  test.each([
    ["null", null],
    ["scalar", 7],
    ["missing required fields", { id: "broken" }],
    ["unknown status", { ...commandTrap(), status: "enabled" }],
    ["unknown applies", { ...commandTrap(), applies: "both" }],
    ["invalid regex", { ...commandTrap(), command: "[" }],
    ["invalid unless regex", { ...commandTrap(), unless: "[" }],
  ])("catalogue: a trap with %s is skipped and reported without losing valid neighbours", (_name, invalid) => {
    const first = commandTrap({ id: "first" });
    const last = commandTrap({ id: "last" });
    const file = writeFile("traps.yaml", JSON.stringify({ traps: [first, invalid, last] }));
    expect(loadTraps(file)).toEqual([first, last]);
    const problems: string[] = catalogueProblems(file);
    expect(problems.length).toBeGreaterThan(0);
    for (const problem of problems) expect(typeof problem).toBe("string");
  });

  test.each([
    ["null", null],
    ["scalar", 7],
    ["missing command", { name: "broken" }],
    ["missing name", { command: "fixture" }],
    ["invalid regex", { name: "broken", command: "[" }],
  ])("catalogue: an engine with %s is skipped and reported without losing valid neighbours", (_name, invalid) => {
    const first: EngineSpec = { name: "first", command: "first run" };
    const last: EngineSpec = { name: "last", command: "last run" };
    const file = writeFile("engines.yaml", JSON.stringify({ engines: [first, invalid, last] }));
    expect(loadEngines(file)).toEqual([first, last]);
    const problems: string[] = catalogueProblems(file);
    expect(problems.length).toBeGreaterThan(0);
    for (const problem of problems) expect(typeof problem).toBe("string");
  });

  test("catalogue: malformed config values are absent from diagnostics and printed output", () => {
    const trapFile = writeFile("traps.yaml", JSON.stringify({ traps: [{ status: secret }] }));
    const engineFile = writeFile("engines.yaml", JSON.stringify({ engines: [{ command: secret }] }));
    expectNoSecret(() => {
      expect(loadTraps(trapFile)).toEqual([]);
      expect(loadEngines(engineFile)).toEqual([]);
      const trapProblems = catalogueProblems(trapFile);
      const engineProblems = catalogueProblems(engineFile);
      expect(trapProblems.length).toBeGreaterThan(0);
      expect(engineProblems.length).toBeGreaterThan(0);
      return { trapProblems, engineProblems };
    });
  });
});

describe("engine recognition", () => {
  test.each([
    ["codex exec 'task' </dev/null", "codex", false],
    ["opencode run 'task'", "opencode", true],
    ["agy -p 'task'", "agy", true],
    ["dsh headless 'task'", "dsh", true],
    ["qwen -p 'task'", "qwen", true],
    ["claude -p 'task'", "claude", true],
    ["python3 four_experts.py run", "four-experts", false],
  ])("recognize: %s uses the default %s engine", (command, engine, stdoutIsAnswer) => {
    expect(recognizeEngineCall(command)).toEqual(engineCall({ engine, stdoutIsAnswer }));
  });

  test("recognize: a command that matches no engine returns null", () => {
    expect(recognizeEngineCall("printf 'hello'")).toBeNull();
    expect(recognizeEngineCall("", [])).toBeNull();
    expect(recognizeEngineCall("codex exec task", [])).toBeNull();
  });

  test("recognize: the first matching supplied engine wins", () => {
    const engines: EngineSpec[] = [
      { name: "first", command: "fixture", stdout_is_answer: true },
      { name: "second", command: "fixture run", stdout_is_answer: false },
    ];
    expect(recognizeEngineCall("fixture run", engines)).toEqual(engineCall({ engine: "first", stdoutIsAnswer: true }));
  });

  test("recognize: omitted stdout-answer metadata defaults to false", () => {
    const engines: EngineSpec[] = [{ name: "fixture", command: "fixture run" }];
    expect(recognizeEngineCall("fixture run", engines)).toEqual(engineCall({ engine: "fixture" }));
  });

  test.each([
    ["-o answer.md", "answer.md"],
    ["-o=answer.md", "answer.md"],
    ["--out answer.md", "answer.md"],
    ['--out="answer file.md"', "answer file.md"],
    ["-o 'answer file.md'", "answer file.md"],
  ])("recognize: output flag %s supplies an unquoted output path", (flag, outputFile) => {
    const engines: EngineSpec[] = [{ name: "fixture", command: "fixture run", output_flags: ["-o", "--out"], stdout_is_answer: true }];
    expect(recognizeEngineCall(`fixture run ${flag}`, engines)).toEqual(
      engineCall({ engine: "fixture", outputFile, stdoutIsAnswer: true }),
    );
  });

  test("recognize: the default codex long output flag is supported", () => {
    expect(recognizeEngineCall('codex exec --output-last-message "answer file.md" task')).toEqual(
      engineCall({ outputFile: "answer file.md" }),
    );
  });

  test.each([
    ["> answer.md", "answer.md"],
    [">> answer.md", "answer.md"],
    ['> "answer file.md"', "answer file.md"],
    [">> 'answer file.md'", "answer file.md"],
  ])("recognize: stdout redirect %s moves the answer to a file", (redirect, outputFile) => {
    expect(recognizeEngineCall(`opencode run task ${redirect}`)).toEqual(
      engineCall({ engine: "opencode", outputFile, stdoutIsAnswer: false }),
    );
  });

  test("recognize: a stderr redirect does not supply an output file", () => {
    expect(recognizeEngineCall("opencode run task 2> errors.txt")).toEqual(
      engineCall({ engine: "opencode", stdoutIsAnswer: true }),
    );
  });

  test("recognize: stdout redirection is found after a stderr redirect", () => {
    expect(recognizeEngineCall("opencode run task 2> errors.txt > answer.md")?.outputFile).toBe("answer.md");
  });

  test("recognize: an explicit output flag takes precedence over stdout redirection", () => {
    expect(recognizeEngineCall("codex exec -o answer.md task > log.txt")).toEqual(
      engineCall({ outputFile: "answer.md" }),
    );
  });

  test("recognize: a wrapper output directory supplies its status file", () => {
    expect(recognizeEngineCall('python3 four_experts.py run --out "results folder"')).toEqual(
      engineCall({ engine: "four-experts", outputFile: "results folder", statusFile: path.join("results folder", "status.json") }),
    );
  });

  test.each([
    ["opencode run task &", true],
    ["opencode run task &  ", true],
    ["opencode run 'task &'", false],
    ['opencode run "task &"', false],
    ["opencode run task && printf done", false],
  ])("recognize: background status respects shell quotes in %s", (command, background) => {
    expect(recognizeEngineCall(command)?.background).toBe(background);
  });

  test("recognize: prompt text is absent from the returned call and printed output", () => {
    expectNoSecret(() => {
      const call = recognizeEngineCall(`codex exec '${secret}' -o answer.md`);
      expect(call).toEqual(engineCall({ outputFile: "answer.md" }));
      return call;
    });
  });
});

describe("command lint", () => {
  test("lint: codex exec without a stdin redirect is a trap", () => {
    expectFailure(lintCommand("codex exec 'task'", lintContext()), "trap:codex-stdin");
  });

  test.each(["</dev/null", "< /dev/null", "<<EOF\ntask\nEOF"])(
    "lint: codex exec with %s does not trigger the stdin trap", (redirect) => {
      expect(lintCommand(`codex exec 'task' ${redirect}`, lintContext())).toEqual([]);
    },
  );

  test("lint: stdin piped into codex does not trigger the stdin trap", () => {
    expect(lintCommand("printf task | codex exec -", lintContext())).toEqual([]);
  });

  test("lint: a proposed catalogue trap never produces a finding", () => {
    expect(lintCommand("agy --mode plan -p task", lintContext())).toEqual([]);
    expect(lintCommand("fixture run", lintContext(), [commandTrap({ status: "proposed" })])).toEqual([]);
  });

  test("lint: result traps do not run as command traps", () => {
    expect(lintCommand("fixture run", lintContext(), [commandTrap({ applies: "result", stderr: "fixture" })])).toEqual([]);
  });

  test("lint: a matching approved command trap returns its exact finding fields", () => {
    const trap = commandTrap();
    expect(lintCommand("fixture run", lintContext(), [trap])).toEqual([
      { rule: "trap:fixture", severity: "fail", message: trap.why, fix: trap.fix, ref: trap.source },
    ]);
  });

  test("lint: every matching trap produces a finding", () => {
    const findings = lintCommand("fixture run", lintContext(), [commandTrap({ id: "first" }), commandTrap({ id: "second" })]);
    expect(findings).toHaveLength(2);
    expectFailure(findings, "trap:first");
    expectFailure(findings, "trap:second");
  });

  test("lint: a nonmatching command or matching unless suppresses a trap", () => {
    const trap = commandTrap({ unless: "--safe" });
    expect(lintCommand("other run", lintContext(), [trap])).toEqual([]);
    expect(lintCommand("fixture run --safe", lintContext(), [trap])).toEqual([]);
    expectFailure(lintCommand("fixture run", lintContext(), [trap]), "trap:fixture");
  });

  test("lint: a second opencode run is trapped using supplied running commands", () => {
    expectFailure(lintCommand("opencode run task", lintContext({ running: ["opencode run other"] })), "trap:opencode-parallel");
  });

  test("lint: a foreground opencode run with no other matching process is clean", () => {
    expect(lintCommand("opencode run task", lintContext({ running: ["printf opencode", "codex exec other"] }))).toEqual([]);
  });

  test.each(["opencode run task &", "opencode run task &  "])(
    "lint: %s is trapped without a concurrent process", (command) => {
      expectFailure(lintCommand(command, lintContext()), "trap:opencode-parallel");
    },
  );

  test("lint: caller-supplied background status triggers the opencode trap", () => {
    expectFailure(lintCommand("opencode run task", lintContext({ background: true })), "trap:opencode-parallel");
  });

  test("lint: a quoted ampersand does not background an opencode run", () => {
    expect(lintCommand("opencode run 'task &'", lintContext())).toEqual([]);
    expect(lintCommand('opencode run "task &"', lintContext())).toEqual([]);
  });

  test("lint: a background-only trap requires background status", () => {
    const trap = commandTrap({ background: true });
    expect(lintCommand("fixture run", lintContext(), [trap])).toEqual([]);
    expectFailure(lintCommand("fixture run &", lintContext(), [trap]), "trap:fixture");
  });

  test("lint: a concurrent-only trap requires a matching supplied process", () => {
    const trap = commandTrap({ concurrent: true });
    expect(lintCommand("fixture run &", lintContext(), [trap])).toEqual([]);
    expectFailure(lintCommand("fixture run", lintContext({ running: ["fixture run other"] }), [trap]), "trap:fixture");
  });

  test("lint: other conditions remain required when background and concurrent are alternatives", () => {
    const trap = commandTrap({ background: true, concurrent: true, paths_outside_repo: true });
    const ctx = lintContext();
    expect(lintCommand(`fixture run ${path.join(ctx.repoRoot, "input.md")} &`, ctx, [trap])).toEqual([]);
    expectFailure(lintCommand(`fixture run ${path.join(folder, "outside.md")} &`, ctx, [trap]), "trap:fixture");
  });

  test("lint: opencode naming an absolute path outside the repo is trapped", () => {
    expectFailure(lintCommand(`opencode run ${path.join(folder, "outside.md")}`, lintContext()), "trap:opencode-outside-repo");
  });

  test("lint: quoted paths with spaces outside the repo are trapped", () => {
    const file = path.join(folder, "outside file.md");
    expectFailure(lintCommand(`opencode run '${file}'`, lintContext()), "trap:opencode-outside-repo");
    expectFailure(lintCommand(`opencode run "${file}"`, lintContext()), "trap:opencode-outside-repo");
  });

  test("lint: a sibling sharing the repo name prefix is still outside", () => {
    const ctx = lintContext();
    expectFailure(lintCommand(`opencode run ${ctx.repoRoot}-sibling/input.md`, ctx), "trap:opencode-outside-repo");
  });

  test("lint: resolving dot segments can move an absolute path outside the repo", () => {
    const ctx = lintContext();
    expectFailure(lintCommand(`opencode run ${ctx.repoRoot}/../outside.md`, ctx), "trap:opencode-outside-repo");
  });

  test("lint: repo paths and relative paths are clean", () => {
    const ctx = lintContext();
    for (const file of [ctx.repoRoot, path.join(ctx.repoRoot, "input.md"), "input.md"]) {
      expect(lintCommand(`opencode run ${file}`, ctx)).toEqual([]);
    }
  });

  test.each(["/dev/null", "/dev/stdin", "/dev/stdout", "/dev/stderr"])(
    "lint: the special path %s is ignored", (file) => {
      expect(lintCommand(`opencode run task ${file}`, lintContext())).toEqual([]);
    },
  );

  test("lint: a path under the temporary directory is not ignored", () => {
    expectFailure(lintCommand(`opencode run ${path.join(folder, "input.md")}`, lintContext()), "trap:opencode-outside-repo");
  });

  test("lint: a clean command returns no findings", () => {
    expect(lintCommand("printf hello", lintContext())).toEqual([]);
    expect(lintCommand("codex exec task", lintContext(), [])).toEqual([]);
  });

  test("lint: prompt text never appears in findings or printed output", () => {
    expectNoSecret(() => {
      const findings = lintCommand(`codex exec '${secret}'`, lintContext({ repoRoot: folder }));
      expectFailure(findings, "trap:codex-stdin");
      return findings;
    });
  });
});

describe("result check", () => {
  test.each([1, 2, 127, -1])("result: exit code %s fails even with a nonempty answer", (exitCode) => {
    expectFailure(checkResult(resultInput({ exitCode })), "R12.1-exit");
  });

  test("result: exit 124 reports timeout instead of generic exit failure", () => {
    const findings = checkResult(resultInput({ exitCode: 124 }));
    expectFailure(findings, "R12.1-timeout");
    expect(findings.map((finding: Finding) => finding.rule)).not.toContain("R12.1-exit");
  });

  test.each([0, null])("result: exit code %s is clean when nothing else fails", (exitCode) => {
    expect(checkResult(resultInput({ exitCode }))).toEqual([]);
  });

  test("result: an interrupted call fails even after exit zero", () => {
    expectFailure(checkResult(resultInput({ interrupted: true })), "R12.1-interrupted");
  });

  test("result: a missing output file fails despite nonempty stdout", () => {
    expectFailure(checkResult(resultInput({ call: engineCall({ outputFile: "missing.md" }) })), "R12.1-missing-output");
  });

  test.each(["", " \n\t\r "])("result: output file content %j is empty", (text) => {
    writeFile("answer.md", text);
    expectFailure(checkResult(resultInput({ call: engineCall({ outputFile: "answer.md" }) })), "R12.1-empty-output");
  });

  test("result: a nonempty relative output file is resolved against input cwd", () => {
    writeFile("nested/answer.md", " \nanswer\t ");
    expect(checkResult(resultInput({ call: engineCall({ outputFile: "nested/answer.md" }), stdout: "" }))).toEqual([]);
  });

  test("result: a nonempty absolute output file is accepted", () => {
    const outputFile = writeFile("answer.md", "answer");
    expect(checkResult(resultInput({ call: engineCall({ outputFile }), stdout: "" }))).toEqual([]);
  });

  test("result: output file contents are absent from findings, prints and guard files", () => {
    writeFile("answer.md", secret);
    expectNoSecret(() => {
      const findings = checkResult(resultInput({ call: engineCall({ outputFile: "answer.md" }), exitCode: 1 }));
      expectFailure(findings, "R12.1-exit");
      return findings;
    });
  });

  test.each(["", " \n\t\r "])("result: stdout answer content %j is empty", (stdout) => {
    expectFailure(checkResult(resultInput({ call: engineCall({ engine: "opencode", stdoutIsAnswer: true }), stdout })), "R12.1-empty-output");
  });

  test("result: a nonempty stdout answer is clean", () => {
    expect(checkResult(resultInput({ call: engineCall({ engine: "opencode", stdoutIsAnswer: true }) }))).toEqual([]);
  });

  test("result: empty stdout is allowed when stdout is not the answer", () => {
    expect(checkResult(resultInput({ stdout: "" }))).toEqual([]);
  });

  test("result: an output file takes precedence over empty stdout answer content", () => {
    writeFile("answer.md", "answer");
    expect(checkResult(resultInput({ call: engineCall({ engine: "opencode", outputFile: "answer.md", stdoutIsAnswer: true }), stdout: "" }))).toEqual([]);
  });

  test.each(["auto-denied", "soft-denied"])("result: agy %s stderr fails even with exit zero and a partial answer", (stderr) => {
    expectFailure(checkResult(resultInput({ call: engineCall({ engine: "agy", stdoutIsAnswer: true }), stderr })), "trap:agy-soft-deny");
  });

  test.each(["502", "Bad Gateway"])("result: agy %s stderr triggers its approved result trap", (stderr) => {
    expectFailure(checkResult(resultInput({ call: engineCall({ engine: "agy", stdoutIsAnswer: true }), stderr })), "trap:agy-502");
  });

  test("result: an empty agy stdout answer triggers the approved output-empty trap", () => {
    const findings = checkResult(resultInput({ call: engineCall({ engine: "agy", stdoutIsAnswer: true }), stdout: " \n" }));
    expectFailure(findings, "R12.1-empty-output");
    expectFailure(findings, "trap:agy-empty");
  });

  test("result: an empty agy output file triggers its output-empty trap", () => {
    writeFile("answer.md", " \t");
    const findings = checkResult(resultInput({ call: engineCall({ engine: "agy", outputFile: "answer.md", stdoutIsAnswer: true }) }));
    expectFailure(findings, "R12.1-empty-output");
    expectFailure(findings, "trap:agy-empty");
  });

  test("result: agy result traps and silent failures do not apply to another engine", () => {
    expect(checkResult(resultInput({ stderr: "auto-denied soft-denied 502 Bad Gateway print timeout" }))).toEqual([]);
  });

  test.each([["print timeout", "timeout"], ["auto-denied", "denied"]])(
    "result: agy silent text %s reports status %s even inside a longer stderr", (text, status) => {
      expectFailure(checkResult(resultInput({ call: engineCall({ engine: "agy", stdoutIsAnswer: true }), stderr: `prefix ${text} suffix` })), `R12.1-silent-${status}`);
    },
  );

  test("result: each matching silent failure produces a finding", () => {
    const findings = checkResult(resultInput({ call: engineCall({ engine: "agy", stdoutIsAnswer: true }), stderr: "print timeout; auto-denied" }));
    expectFailure(findings, "R12.1-silent-timeout");
    expectFailure(findings, "R12.1-silent-denied");
    expectFailure(findings, "trap:agy-soft-deny");
  });

  test("result: a clean agy call does not trigger its conditional traps", () => {
    expect(checkResult(resultInput({ call: engineCall({ engine: "agy", stdoutIsAnswer: true }) }))).toEqual([]);
  });

  test("result: a missing wrapper status file fails", () => {
    expectFailure(checkResult(resultInput({ call: engineCall({ engine: "four-experts", statusFile: "results/status.json" }) })), "R12.1-missing-status");
  });

  test("result: wrapper status entries that are all ok are clean", () => {
    writeFile("results/status.json", JSON.stringify({ first: { ok: true }, second: { ok: true } }));
    expect(checkResult(resultInput({ call: engineCall({ engine: "four-experts", statusFile: "results/status.json" }) }))).toEqual([]);
  });

  test("result: each failed wrapper status entry is named without its content", () => {
    const statusFile = writeFile("results/status.json", JSON.stringify({
      first: { ok: false, stderr: secret },
      second: { ok: false, stdout: secret },
      clean: { ok: true },
    }));
    expectNoSecret(() => {
      const findings = checkResult(resultInput({ call: engineCall({ engine: "four-experts", statusFile }) }));
      const wrapped = findings.filter((finding: Finding) => finding.rule === "R12.1-wrapped-fail");
      expect(wrapped).toHaveLength(2);
      for (const key of ["first", "second"]) {
        expect(wrapped.some((finding: Finding) => finding.message.includes(key))).toBe(true);
      }
      expectFailure(findings, "R12.1-wrapped-fail");
      return findings;
    });
  });

  test("result: independent exit, interruption and file failures are all reported", () => {
    const findings = checkResult(resultInput({ exitCode: 1, interrupted: true, call: engineCall({ outputFile: "missing.md" }) }));
    expectFailure(findings, "R12.1-exit");
    expectFailure(findings, "R12.1-interrupted");
    expectFailure(findings, "R12.1-missing-output");
  });

  test("result: stdout and stderr secrets are absent from findings, prints and guard files", () => {
    expectNoSecret(() => {
      const findings = checkResult(resultInput({
        call: engineCall({ engine: "agy", stdoutIsAnswer: true }),
        stdout: secret, stderr: `auto-denied ${secret}`, exitCode: 1,
      }));
      expectFailure(findings, "trap:agy-soft-deny");
      expectFailure(findings, "R12.1-exit");
      return findings;
    });
  });
});
