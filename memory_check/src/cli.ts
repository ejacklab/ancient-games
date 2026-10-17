// The command's launcher: `bun src/cli.ts [options]`.
//
// F3, U5: a run must write nothing but its own report, and that covers what the runtime writes too. Bun caches the
// transpiled form of every source file of 4 KB or more in `$BUN_RUNTIME_TRANSPILER_CACHE_PATH`, which by default is
// `$HOME/.bun/install/cache/@t@` — the home folder of the project being checked, when `--home` points at it. That
// variable is read before any JavaScript runs, so nothing written in this repository can redirect it. This file is
// therefore only a launcher: no static imports and far under 4 KB, so nothing in it is ever cached. It re-runs the
// same command through the same bun binary with the transpiler cache switched off, forwarding the arguments, the
// standard streams and the exit code; that second run reads every module with the cache off and writes none either.
// A caller who has already chosen a cache directory keeps it — the launcher runs once, and only when the variable is
// unset.
const CACHE_PATH_VAR = "BUN_RUNTIME_TRANSPILER_CACHE_PATH";

const args = Bun.argv.slice(2);

if (process.env[CACHE_PATH_VAR] === undefined) {
  const child = Bun.spawnSync({
    cmd: [process.execPath, import.meta.path, ...args],
    env: { ...process.env, [CACHE_PATH_VAR]: "0" },
    stdin: "inherit",
    stdout: "inherit",
    stderr: "inherit",
  });
  process.exit(child.exitCode);
}

const { main } = await import("./command.ts");
process.exit(main(args));