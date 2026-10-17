import { createHash } from "node:crypto";
import { lstat, readFile, readlink, readdir } from "node:fs/promises";
import { join } from "node:path";

export type ProcessResult = { exitCode: number; stdout: string; stderr: string; command: string[] };
export type FileSnapshot = Record<string, string>;
export type FileChange = { path: string; change: "added" | "removed" | "modified" };

export function shellQuote(value: string): string { return "'" + value.replaceAll("'", "'\\''") + "'"; }

export async function captureProcess(command: string[], cwd: string): Promise<ProcessResult> {
  try {
    const child = Bun.spawn(command, { cwd, stdout: "pipe", stderr: "pipe", stdin: "ignore" });
    const [exitCode, stdout, stderr] = await Promise.all([child.exited, new Response(child.stdout).text(), new Response(child.stderr).text()]);
    return { exitCode, stdout, stderr, command };
  } catch (error) {
    return { exitCode: -1, stdout: "", stderr: String(error), command };
  }
}

export async function snapshotFiles(roots: string[]): Promise<FileSnapshot> {
  const snapshot: FileSnapshot = {};
  async function visit(path: string) {
    if (Object.hasOwn(snapshot, path)) return;
    const stat = await lstat(path, { bigint: true }).catch(error => {
      if (error.code === "ENOENT") return undefined;
      throw error;
    });
    if (!stat) return;
    const metadata = `${stat.mode}:${stat.size}:${stat.mtimeNs}:${stat.ctimeNs}`;
    if (stat.isSymbolicLink()) snapshot[path] = `symlink:${metadata}:${await readlink(path)}`;
    else if (stat.isDirectory()) {
      snapshot[path] = `directory:${stat.mode}:${stat.mtimeNs}:${stat.ctimeNs}`;
      for (const entry of (await readdir(path)).sort()) await visit(join(path, entry));
    } else if (stat.isFile()) snapshot[path] = `file:${metadata}:${createHash("sha256").update(await readFile(path)).digest("hex")}`;
    else snapshot[path] = `other:${metadata}`;
  }
  for (const root of [...new Set(roots)].sort()) await visit(root);
  return snapshot;
}

export function compareSnapshots(before: FileSnapshot, after: FileSnapshot): FileChange[] {
  return [...new Set([...Object.keys(before), ...Object.keys(after)])].sort().flatMap(path => {
    if (before[path] === after[path]) return [];
    const change = before[path] === undefined ? "added" : after[path] === undefined ? "removed" : "modified";
    return [{ path, change }];
  });
}
