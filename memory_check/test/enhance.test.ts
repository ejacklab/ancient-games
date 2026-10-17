// Tests for the enhance round (runs/20261017-memory-check/enhance-q/compare.md, the main agent's picks): R1's
// unstaged line and final Not applicable section, R2/U3's could-not-run MUSTs in the warning. Written by the main
// agent (Claude), which wrote none of src/.
import { afterEach, describe, expect, test } from "bun:test";
import { execSync } from "node:child_process";
import { chmodSync, mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { Project, entryPath } from "./fixtures/project";

const projects: Project[] = [];
function fixture(memory = true) { const p = new Project(memory); projects.push(p); return p; }
afterEach(() => { for (const p of projects.splice(0)) p.close(); });

const ROW = /^- \*\*((?:SoT|CACHES):[^*]+)\*\* \(([^)]+)\) — (pass|fail|needs a reviewer|not applicable|could not run) — (.*)$/;

describe("enhance round", () => {
  test("R1: every not applicable result is in a final ## Not applicable section, and only there", () => {
    const text = fixture(false).run().stdout;
    const lines = text.split("\n");
    const start = lines.indexOf("## Not applicable");
    expect(start).toBeGreaterThan(0);
    expect(lines.slice(start + 1).some((l) => l.startsWith("## "))).toBe(false); // it is the last section
    const before = lines.slice(0, start).map((l) => ROW.exec(l)).filter(Boolean);
    const after = lines.slice(start + 1).map((l) => ROW.exec(l)).filter(Boolean);
    expect(before.some((m) => m![3] === "not applicable")).toBe(false);
    expect(after.length).toBeGreaterThan(0);
    expect(after.every((m) => m![3] === "not applicable")).toBe(true);
  });

  test("R1: the report counts project-memory files changed but not staged", () => {
    const p = fixture();
    writeFileSync(join(p.project, entryPath), "an unstaged edit\n");
    p.write("project-memory/entries/O-18-10-new000-2026-x.md", "an untracked new file\n");
    const text = p.run().stdout;
    expect(text).toMatch(/2 files? under `?project-memory\/`? (are )?changed but not staged/);
  });

  test("R1: with nothing unstaged the count is 0", () => {
    expect(fixture().run().stdout).toMatch(/0 files? under `?project-memory\/`? (are )?changed but not staged/);
  });

  test("R2/U3: a MUST that could not run is in the warning", () => {
    const p = fixture();
    const bin = join(p.base, "bin"); mkdirSync(bin);
    const real = execSync("command -v git", { encoding: "utf8" }).trim();
    writeFileSync(join(bin, "git"), `#!/bin/sh\nfor a in "$@"; do [ "$a" = log ] && { echo "fatal: injected" >&2; exit 128; }; done\nexec ${real} "$@"\n`);
    chmodSync(join(bin, "git"), 0o755);
    p.env.PATH = `${bin}:${p.env.PATH}`;
    const report = p.run().stdout;
    const notRun = report.split("\n").map((l) => ROW.exec(l)).filter((m) => m && m[2] === "MUST" && m[3] === "could not run").map((m) => m![1]);
    expect(notRun.length).toBeGreaterThan(0);
    const warning = p.run(["--warn"]).stdout;
    for (const id of notRun) expect(warning).toContain(id!);
  });
});
