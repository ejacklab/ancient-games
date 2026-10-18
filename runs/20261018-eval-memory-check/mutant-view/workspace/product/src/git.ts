// Every git call the tool makes: read-only, with GIT_OPTIONAL_LOCKS=0 so git never writes its index file (F3).
import { spawnSync } from "node:child_process";

export interface GitResult {
  readonly code: number;
  readonly stdout: string;
  readonly stderr: string;
}

export function git(cwd: string, args: readonly string[]): GitResult {
  const result = spawnSync("git", [...args], {
    cwd,
    encoding: "utf8",
    env: { ...process.env, GIT_OPTIONAL_LOCKS: "0" },
  });
  return {
    code: result.status ?? -1,
    stdout: result.stdout ?? "",
    stderr: result.stderr ?? "",
  };
}

/** Whether a read-only git command succeeded. */
export function gitOk(cwd: string, args: readonly string[]): boolean {
  return git(cwd, args).code === 0;
}

export function gitOut(cwd: string, args: readonly string[]): string {
  const result = git(cwd, args);
  return result.code === 0 ? result.stdout.trim() : "";
}

/** The lines of output that are not empty. */
export function lines(text: string): string[] {
  return text.split("\n").map((line) => line.trimEnd()).filter((line) => line !== "");
}