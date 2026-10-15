import { afterEach, beforeEach, describe, expect, spyOn, test } from "bun:test";
import { spawnSync } from "node:child_process";
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
  segments,
} from "../src/traps.ts";
import type { EngineCall, EngineSpec, Finding, LintContext, ResultInput, Segment, Trap } from "../src/types.ts";

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

function checkWithTraps(traps: Trap[], input: ResultInput): Finding[] {
  // A private package copy changes default data without touching the repository.
  fs.mkdirSync(path.join(folder, "src"), { recursive: true });
  for (const name of ["traps.ts", "types.ts"]) {
    fs.copyFileSync(new URL(`../src/${name}`, import.meta.url), path.join(folder, "src", name));
  }
  writeFile("data/traps.yaml", JSON.stringify({ traps }));
  fs.copyFileSync(new URL("../data/engines.yaml", import.meta.url), path.join(folder, "data/engines.yaml"));
  const runner = writeFile("check.ts", `
import { checkResult } from "./src/traps.ts";
console.log(JSON.stringify(checkResult(${JSON.stringify(input)})));
`);
  const child = spawnSync(process.execPath, [runner], { cwd: folder, encoding: "utf8", timeout: 5000 });
  expect(child.error).toBeUndefined();
  expect(child.stdout).not.toContain(secret);
  expect(child.stderr).not.toContain(secret);
  expect(child.status).toBe(0);
  return JSON.parse(child.stdout) as Finding[];
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

describe("command segments", () => {
  test("segments: empty commands and repeated separators are dropped", () => {
    expect(segments(" \n; () ;\n ")).toEqual([]);
    expect(segments("")).toEqual([]);
  });

  test.each(["\n", ";", "&&", "||", "|", "(", ")"])(
    "segments: %j separates trimmed commands", (separator) => {
      expect(segments(`  printf first ${separator} printf second  `)).toEqual([
        { text: "printf first", background: false, piped: false },
        { text: "printf second", background: false, piped: separator === "|" },
      ]);
    },
  );

  test("segments: piped is true only after a pipe and resets at other separators", () => {
    const parts: Segment[] = segments("printf first | cat || printf fallback; printf next && printf done");
    expect(parts.map((part) => part.piped)).toEqual([false, true, false, false, false]);
  });

  test.each(["'", '"'])("segments: separators inside %s quotes stay in the command", (quote) => {
    const text = `printf ${quote}one\n; && || | & ( )${quote}`;
    expect(segments(`${text}; printf done`)).toEqual([
      { text, background: false, piped: false }, { text: "printf done", background: false, piped: false },
    ]);
  });

  test.each(["2>&1", ">&2", "&>log.txt"])(
    "segments: %s remains a redirection rather than a background separator", (redirect) => {
      expect(segments(`opencode run task ${redirect}; printf done`)).toEqual([
        { text: `opencode run task ${redirect}`, background: false, piped: false },
        { text: "printf done", background: false, piped: false },
      ]);
    },
  );

  test("segments: each command retains its own input and output redirections", () => {
    expect(segments("codex exec task </dev/null > answer.md && printf done >> log.txt")).toEqual([
      { text: "codex exec task </dev/null > answer.md", background: false, piped: false },
      { text: "printf done >> log.txt", background: false, piped: false },
    ]);
  });

  test.each(["<<WORD", "<<'WORD'", '<<"WORD"', "<<-WORD"])(
    "segments: %s removes the heredoc body and closing delimiter", (redirect) => {
      const delimiter = redirect === "<<-WORD" ? "\tWORD" : "WORD";
      expect(segments(`cat ${redirect}\nopencode run task &\ncodex exec task\n${delimiter}\nprintf done`)).toEqual([
        { text: `cat ${redirect}`, background: false, piped: false },
        { text: "printf done", background: false, piped: false },
      ]);
    },
  );

  test("segments: a heredoc ends only at the exact delimiter line", () => {
    expect(segments("cat <<WORD\nWORD suffix\ncodex exec task\nWORD\nprintf done")).toEqual([
      { text: "cat <<WORD", background: false, piped: false }, { text: "printf done", background: false, piped: false },
    ]);
  });

  test("segments: a single ampersand backgrounds only its preceding command", () => {
    expect(segments("printf first & printf second && printf third")).toEqual([
      { text: "printf first", background: true, piped: false },
      { text: "printf second", background: false, piped: false },
      { text: "printf third", background: false, piped: false },
    ]);
  });

  test("segments: a backgrounded group marks every command inside it", () => {
    expect(segments("printf before; (codex exec first; codex exec second) & printf after")).toEqual([
      { text: "printf before", background: false, piped: false },
      { text: "codex exec first", background: true, piped: false },
      { text: "codex exec second", background: true, piped: false },
      { text: "printf after", background: false, piped: false },
    ]);
  });

  test("segments: foreground groups and logical operators do not imply background", () => {
    expect(segments("(printf first && printf second) || printf third")).toEqual([
      { text: "printf first", background: false, piped: false },
      { text: "printf second", background: false, piped: false },
      { text: "printf third", background: false, piped: false },
    ]);
  });
});

describe("engine recognition", () => {
  test.each([
    "codex exec --help",
    'pgrep -f "codex exec"',
    "grep -n 'codex exec' commands.txt",
    "grep -E 'opencode run|agy -p' commands.txt",
    'echo "codex exec; opencode run task &"',
    "printf '%s' 'opencode run task /fixture/outside.md &'",
    "cat <<EOF\ncodex exec task\nopencode run /fixture/outside.md &\nEOF",
    "cat <<'EOF'\ncodex exec task\nEOF",
    'cat <<"EOF"\nopencode run task &\nEOF',
    "cat <<-EOF\n\topencode run task &\n\tEOF",
  ])("recognize and lint: engine text in %j starts no session", (command) => {
    expect(recognizeEngineCall(command)).toBeNull();
    expect(lintCommand(command, lintContext({ running: ["opencode run other"] }))).toEqual([]);
  });

  test.each(["--help", "-h", "--version", "-V"])(
    "recognize and lint: standalone %s suppresses engine calls and command traps", (flag) => {
      for (const command of [`codex exec ${flag}`, `opencode run ${flag} /fixture/outside.md &`]) {
        expect(recognizeEngineCall(command)).toBeNull();
        expect(lintCommand(command, lintContext())).toEqual([]);
      }
    },
  );

  test("recognize and lint: help substrings are not standalone help words", () => {
    const command = "codex exec --helpful 'task--version'";
    expect(recognizeEngineCall(command)).toEqual(engineCall());
    expectFailure(lintCommand(command, lintContext()), "trap:codex-stdin");
  });

  test.each([
    "JOB=one OTHER='two words'",
    "timeout 60",
    "timeout --signal TERM --kill-after 5s 60s",
    "timeout -s TERM -k 5 60",
    "timeout --signal=TERM --kill-after=5s 60s",
    "env -u X",
    "env -i JOB=one",
    "env -u X -u Y JOB='two words'",
    "nohup",
    "time",
    "exec",
    "command",
    "runlog.py --runs-root /fixture/runs exec worker --",
    "/fixture/tools/runlog.py --runs-root /fixture/runs exec worker --",
    "python3 /fixture/tools/runlog.py --runs-root /fixture/runs exec worker --",
    "python3 runlog.py --tag='contains--inside' --",
    "JOB=one timeout 60 env -u X nohup time exec command",
  ])("recognize and lint: %s is stripped before matching codex", (wrapper) => {
    const command = `${wrapper} codex exec task`;
    expect(recognizeEngineCall(command)).toEqual(engineCall());
    expectFailure(lintCommand(command, lintContext()), "trap:codex-stdin");
    expect(lintCommand(`${command} </dev/null`, lintContext())).toEqual([]);
  });

  test("recognize: an absolute executable path matches the anchored command word", () => {
    expect(recognizeEngineCall("/fixture/bin/codex exec task </dev/null")).toEqual(engineCall());
    expectFailure(lintCommand("/fixture/bin/codex exec task", lintContext()), "trap:codex-stdin");
  });

  test("recognize: segment order takes precedence over catalogue order", () => {
    const engines: EngineSpec[] = [
      { name: "later", command: "^later run" },
      { name: "earlier", command: "^earlier run", stdout_is_answer: true },
    ];
    expect(recognizeEngineCall("printf ready; earlier run; later run", engines)).toEqual(
      engineCall({ engine: "earlier", stdoutIsAnswer: true }),
    );
  });

  test("recognize: output and background metadata belong to the first matching segment", () => {
    expect(recognizeEngineCall("printf before > before.md; opencode run task & codex exec -o later.md </dev/null")).toEqual(
      engineCall({ engine: "opencode", stdoutIsAnswer: true, background: true }),
    );
    expect(recognizeEngineCall("printf before > before.md; opencode run task > answer.md; printf done &")).toEqual(
      engineCall({ engine: "opencode", outputFile: "answer.md" }),
    );
  });

  test("recognize: help on another segment does not hide a real engine call", () => {
    expect(recognizeEngineCall("printf --help; codex exec task </dev/null")).toEqual(engineCall());
    expect(recognizeEngineCall("codex exec --help; opencode run task")).toEqual(
      engineCall({ engine: "opencode", stdoutIsAnswer: true }),
    );
  });

  test("recognize and lint: a real call after a heredoc survives removal of engine text in the body", () => {
    const command = "cat <<EOF\ncodex exec fake\nopencode run /fixture/outside.md &\nEOF\nopencode run task > answer.md";
    expect(recognizeEngineCall(command)).toEqual(engineCall({ engine: "opencode", outputFile: "answer.md" }));
    expect(lintCommand(command, lintContext())).toEqual([]);
  });

  test("recognize: an engine in a backgrounded group has background status", () => {
    expect(recognizeEngineCall("(printf ready; opencode run task) & printf done")).toEqual(
      engineCall({ engine: "opencode", stdoutIsAnswer: true, background: true }),
    );
  });

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
  test("lint: redirects and unless text in other segments do not excuse codex", () => {
    for (const command of [
      "printf before </dev/null; codex exec task",
      "codex exec task; printf after </dev/null",
      "cat <<EOF\ntext\nEOF\ncodex exec task",
      "codex exec first </dev/null; codex exec second",
    ]) {
      expectFailure(lintCommand(command, lintContext()), "trap:codex-stdin");
    }
    const trap = commandTrap({ command: "^fixture run", unless: "--safe" });
    expectFailure(lintCommand("printf --safe; fixture run", lintContext(), [trap]), "trap:fixture");
  });

  test("lint: codex calls inside a backgrounded group retain the stdin trap", () => {
    expectFailure(lintCommand("(codex exec first; codex exec second) &", lintContext()), "trap:codex-stdin");
    expect(lintCommand("(codex exec first </dev/null; codex exec second </dev/null) &", lintContext())).toEqual([]);
  });

  test("lint: a backgrounded group triggers opencode's background condition", () => {
    expectFailure(lintCommand("(printf ready; opencode run task) & printf done", lintContext()), "trap:opencode-parallel");
    expect(lintCommand("(opencode run task); printf done &", lintContext())).toEqual([]);
  });

  test("lint: redirection ampersands do not trigger the background condition", () => {
    for (const redirect of ["2>&1", ">&2", "&>log.txt"]) {
      expect(lintCommand(`opencode run task ${redirect}`, lintContext())).toEqual([]);
    }
  });

  test("lint: another segment's absolute paths do not belong to opencode", () => {
    for (const command of [
      "python3 /fixture/tools/report.py --runs-root /fixture/runs; opencode run task",
      "opencode run task && cat /fixture/outside.md",
      "cat /fixture/outside.md | opencode run task",
    ]) {
      expect(lintCommand(command, lintContext())).toEqual([]);
    }
  });

  test("lint: runlog wrapper paths are removed before checking the engine command", () => {
    expect(lintCommand(
      'python3 /fixture/tools/runlog.py --runs-root /fixture/runs exec worker -- opencode run "task"',
      lintContext(),
    )).toEqual([]);
  });

  test("lint: concurrent matching finds an engine inside another process's full command line", () => {
    expectFailure(lintCommand("opencode run task", lintContext({
      running: ["timeout 60 env JOB=one /fixture/bin/opencode run other"],
    })), "trap:opencode-parallel");
  });

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

  test("lint: unless_piped suppresses a planted trap only for the piped segment", () => {
    const trap = commandTrap({ command: "^fixture run", unless_piped: true });
    expect(lintCommand("printf task | fixture run", lintContext(), [trap])).toEqual([]);
    expectFailure(lintCommand("fixture run", lintContext(), [trap]), "trap:fixture");
    expectFailure(lintCommand("printf task | cat; fixture run", lintContext(), [trap]), "trap:fixture");
    expectFailure(lintCommand("printf task | fixture run", lintContext(), [{ ...trap, unless_piped: false }]), "trap:fixture");
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
  test.each(["agy", "any"])("result: a proposed stderr trap for %s produces no finding", (engine) => {
    const trap: Trap = {
      id: "proposed-result", status: "proposed", applies: "result", engine,
      stderr: "fixture denial", why: "fixture result denied", fix: "retry", source: "fixture catalogue",
    };
    const input = resultInput({ call: engineCall({ engine: "agy", stdoutIsAnswer: true }), stderr: "fixture denial" });
    expect(checkWithTraps([trap], input)).toEqual([]);
    expectFailure(checkWithTraps([{ ...trap, status: "approved" }], input), "trap:proposed-result");
  });

  test("result: a proposed output-empty trap produces no trap finding", () => {
    const trap: Trap = {
      id: "proposed-empty", status: "proposed", applies: "result", engine: "any", output_empty: true,
      why: "fixture result empty", fix: "retry", source: "fixture catalogue",
    };
    const input = resultInput({ call: engineCall({ engine: "agy", stdoutIsAnswer: true }), stdout: " \n" });
    const findings = checkWithTraps([trap], input);
    expect(findings.map((finding) => finding.rule)).toEqual(["R12.1-empty-output"]);
    expectFailure(checkWithTraps([{ ...trap, status: "approved" }], input), "trap:proposed-empty");
  });

  test("result: command traps do not run as result traps", () => {
    expect(checkWithTraps([
      commandTrap({ engine: "any", stderr: "fixture denial", output_empty: true }),
    ], resultInput({ stderr: "fixture denial" }))).toEqual([]);
  });

  test("result: a result trap can match stderr or empty output independently", () => {
    const trap: Trap = {
      id: "either", status: "approved", applies: "result", engine: "any",
      stderr: "fixture denial", output_empty: true,
      why: "fixture result failed", fix: "retry", source: "fixture catalogue",
    };
    expectFailure(checkWithTraps([trap], resultInput({ stderr: "fixture denial" })), "trap:either");
    expectFailure(checkWithTraps([trap], resultInput({
      call: engineCall({ stdoutIsAnswer: true }), stdout: "", stderr: "",
    })), "trap:either");
    expect(checkWithTraps([trap], resultInput())).toEqual([]);
  });

  test("result: a matching result trap returns its exact finding fields", () => {
    const trap: Trap = {
      id: "result-fields", status: "approved", applies: "result", engine: "codex", stderr: "fixture denial",
      why: "fixture result denied", fix: "retry", source: "fixture catalogue",
    };
    expect(checkWithTraps([trap], resultInput({ stderr: "fixture denial" }))).toEqual([
      { rule: "trap:result-fields", severity: "fail", message: trap.why, fix: trap.fix, ref: trap.source },
    ]);
  });

  test("result: a wrapper output directory uses status rather than file content checks", () => {
    writeFile("results/status.json", JSON.stringify({ first: { ok: true } }));
    expect(checkResult(resultInput({
      call: engineCall({ engine: "four-experts", outputFile: "results", statusFile: "results/status.json" }),
      stdout: "",
    }))).toEqual([]);
  });

  test("result: missing wrapper status does not also report a missing output file", () => {
    const findings = checkResult(resultInput({
      call: engineCall({ engine: "four-experts", outputFile: "missing", statusFile: "missing/status.json" }),
    }));
    expect(findings.map((finding: Finding) => finding.rule)).toEqual(["R12.1-missing-status"]);
  });

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
