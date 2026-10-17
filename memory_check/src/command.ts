// The command itself: `bun src/cli.ts [--project <repo root>] [--home <dir>] [--since <rev>] [--out <file>]
// [--warn]` — `cli.ts` launches it, `command.ts` is it.
// R3: exit 0 when no MUST fails or could not run, 1 when one does, 2 on a usage error. Nothing is written but
// `--out`'s file (F3, U5).
import { existsSync, statSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import path from "node:path";
import { runChecks } from "./checks.ts";
import { loadGuidelines } from "./guidelines.ts";
import { gitOut } from "./git.ts";
import { renderReport } from "./report.ts";
import { renderWarning } from "./warn.ts";

const USAGE = `memory-check — check a project's memory against docs/memory-system's two guidelines

Usage: memory-check [options]
  --project <path>   the git repository root to check (default: the current folder)
  --home <dir>       the home folder that holds .claude/agent-memory/<name>/ (default: the user's home)
  --since <rev>      check history from this commit instead of the first that touches project-memory/
  --out <file>       write the report here instead of printing it
  --warn             print the session-start warning only (failing MUSTs and a missing AGENTS.md)
  --help             this text`;

interface Options {
  readonly project: string | null;
  readonly home: string | null;
  readonly since: string | null;
  readonly out: string | null;
  readonly warn: boolean;
}

class UsageError extends Error {}

function parseArgs(argv: readonly string[]): Options {
  let project: string | null = null;
  let home: string | null = null;
  let since: string | null = null;
  let out: string | null = null;
  let warn = false;
  for (let index = 0; index < argv.length; index++) {
    const flag = argv[index]!;
    const value = (): string => {
      const next = argv[index + 1];
      if (next === undefined || next.startsWith("--")) throw new UsageError(`${flag} needs a value`);
      index += 1;
      return next;
    };
    switch (flag) {
      case "--project":
        project = value();
        break;
      case "--home":
        home = value();
        break;
      case "--since":
        since = value();
        break;
      case "--out":
        out = value();
        break;
      case "--warn":
        warn = true;
        break;
      case "--help":
      case "-h":
        process.stdout.write(`${USAGE}\n`);
        process.exit(0);
        break;
      default:
        throw new UsageError(`unknown option ${flag}`);
    }
  }
  return { project, home, since, out, warn };
}

/** F2: the project must be given, exist, and be the root of a git repository — else a usage error. */
function projectRootOf(given: string | null): string {
  const root = path.resolve(given ?? process.cwd());
  if (!existsSync(root) || !statSync(root).isDirectory()) {
    throw new UsageError(`${root} does not exist`);
  }
  const top = gitOut(root, ["rev-parse", "--show-toplevel"]);
  if (top === "") throw new UsageError(`${root} is not inside a git repository`);
  if (path.resolve(top) !== root) throw new UsageError(`${root} is not the root of its git repository (${top} is)`);
  return root;
}

export function main(argv: readonly string[]): number {
  let options: Options;
  let root: string;
  let home: string;
  try {
    options = parseArgs(argv);
    root = projectRootOf(options.project);
    home = path.resolve(options.home ?? homedir());
    if (!existsSync(home)) throw new UsageError(`${home} does not exist`);
    if (options.since !== null && gitOut(root, ["rev-parse", "--verify", "--quiet", `${options.since}^{commit}`]) === "") {
      throw new UsageError(`--since ${options.since} names no commit in ${root}`);
    }
  } catch (error) {
    const message = error instanceof UsageError ? error.message : String(error);
    process.stderr.write(`memory-check: ${message}\n${USAGE}\n`);
    return 2;
  }

  const run = runChecks({
    root,
    home,
    since: options.since,
    out: options.out ? path.resolve(options.out) : null,
    guidelines: loadGuidelines(),
  });

  if (options.warn) {
    const warning = renderWarning(run);
    if (warning !== "") process.stdout.write(`${warning}\n`);
  } else if (options.out !== null) {
    writeFileSync(path.resolve(options.out), renderReport(run, path.resolve(options.out)));
    process.stdout.write(`${path.resolve(options.out)}\n`);
  } else {
    process.stdout.write(`${renderReport(run, null)}\n`);
  }
  return run.exitCode;
}
