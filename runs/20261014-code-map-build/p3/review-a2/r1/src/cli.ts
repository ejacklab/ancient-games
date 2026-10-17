import { writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import type { Answer } from "./answer.ts";
import { answerFor, type Options } from "./commands.ts";
import { renderText } from "./render.ts";

const commands = new Set(["where", "find", "callers", "callees", "chain", "tests", "map"]);

const valuedFlags = new Set(["--project", "--root", "--tests", "--siblings", "--up", "--down", "--fake-rule", "--file", "--out"]);

interface Parsed {
  options: Options;
  out?: string;
}

export function parseArguments(argv: string[]): Parsed {
  const project: string[] = [];
  const tests: string[] = [];
  const siblings: string[] = [];
  const query: string[] = [];
  let root = process.cwd();
  let json = false;
  let perFunction = false;
  let up: number | undefined;
  let down: number | undefined;
  let fakeRule: "count" | "exclude" | undefined;
  let file: string | undefined;
  let out: string | undefined;
  const command = argv[0];
  if (!command || !commands.has(command)) {
    throw new Error(`Usage: code-map <${[...commands].join("|")}> <query> --project <tsconfig.json> [--root <dir>] [--tests <glob>]... [--json]`);
  }
  for (let index = 1; index < argv.length; index++) {
    const flag = argv[index]!;
    if (flag === "--json") {
      json = true;
      continue;
    }
    if (flag === "--per-function") {
      perFunction = true;
      continue;
    }
    if (valuedFlags.has(flag)) {
      const value = argv[++index];
      if (value === undefined) throw new Error(`${flag} needs a value`);
      if (flag === "--project") project.push(value);
      else if (flag === "--tests") tests.push(value);
      else if (flag === "--siblings") siblings.push(value);
      else if (flag === "--root") root = value;
      else if (flag === "--out") out = value;
      else if (flag === "--file") file = value;
      else if (flag === "--up") up = positiveInteger(flag, value);
      else if (flag === "--down") down = positiveInteger(flag, value);
      else if (flag === "--fake-rule") {
        if (value !== "count" && value !== "exclude") throw new Error("--fake-rule needs count or exclude");
        fakeRule = value;
      }
      continue;
    }
    if (flag.startsWith("--")) throw new Error(`unknown option ${flag}`);
    query.push(flag);
  }
  if (!project.length) throw new Error("--project <tsconfig.json> is required");
  return {
    out,
    options: {
      command,
      query,
      project,
      root: resolve(root),
      tests,
      siblings,
      up,
      down,
      fakeRule,
      file,
      perFunction,
      json,
    },
  };
}

function positiveInteger(flag: string, value: string): number {
  const number = Number(value);
  if (!Number.isInteger(number) || number < 0) throw new Error(`${flag} needs a whole number of levels`);
  return number;
}

export async function run(argv: string[]): Promise<number> {
  let parsed: Parsed;
  try {
    parsed = parseArguments(argv);
  } catch (error) {
    console.error(String(error instanceof Error ? error.message : error));
    return 2;
  }
  const json = parsed.options.json;
  let answer: Answer;
  try {
    answer = answerFor(parsed.options);
  } catch (error) {
    console.error(String(error instanceof Error ? error.message : error));
    return 2;
  }
  const text = json ? JSON.stringify(answer) : renderText(answer);
  if (parsed.out) await writeFile(resolve(parsed.out), `${text}\n`);
  else console.log(text);
  return 0;
}

if (import.meta.main) process.exitCode = await run(Bun.argv.slice(2));