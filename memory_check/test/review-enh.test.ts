// Acceptance tests for the enhance step's picks E-1 and E-2 (runs/20261017-memory-check-review), one per finding,
// each built from the finding's own input. Written by the reproduce-enh step (Claude), which wrote none of src/.
import { afterEach, describe, expect, test } from "bun:test";
import { chmodSync, existsSync, mkdirSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { execSync } from "node:child_process";
import { join } from "node:path";
import { Project, entryPath } from "./fixtures/project";

const projects: Project[] = [];
function fixture(memory = true) { const p = new Project(memory); projects.push(p); return p; }
afterEach(() => { for (const p of projects.splice(0)) { try { chmodSync(join(p.project, "CLAUDE.md"), 0o644); } catch {} p.close(); } });

type Row = { id: string; level: string; state: string; evidence: string };
function rows(report: string): Row[] {
  return [...report.matchAll(/^- \*\*((?:SoT|CACHES):[^*]+)\*\* \(([^)]+)\) — (pass|fail|needs a reviewer|not applicable|could not run) — (.*)$/gm)]
    .map((m) => ({ id: m[1]!, level: m[2]!, state: m[3]!, evidence: m[4]! }));
}
function result(report: string, id: string) {
  const found = rows(report).filter((r) => r.id === id);
  expect(found.length, `one result for ${id}`).toBe(1);
  return found[0]!;
}
const unread = ["pass", "not applicable"]; // what a result may not be when its read did not work (E-1)
const breakHeader = (p: Project) => p.plant(entryPath, "---\nUse UTC", "Use UTC"); // the header is not closed (W1.2a)
function failingGit(p: Project, when: string) {
  const bin = join(p.base, "bin"); mkdirSync(bin);
  const real = execSync("command -v git", { encoding: "utf8" }).trim();
  writeFileSync(join(bin, "git"), `#!/bin/sh\ncase " $* " in ${when}) echo "fatal: injected ls-files" >&2; exit 128;; esac\nexec ${real} "$@"\n`);
  chmodSync(join(bin, "git"), 0o755);
  p.env.PATH = `${bin}:${p.env.PATH}`;
}

describe("E-1: a pass or not applicable needs a read that worked", () => {
  test("E-1a: a failed git ls-files is could not run, never every SoT record not applicable with exit 0", () => {
    const p = fixture();
    failingGit(p, `*" ls-files "*" --cached "*`);
    const r = p.run();
    const w12a = result(r.stdout, "SoT:W1.2a"); // the final pass (checks.ts:282) behind the early return at :212
    expect(unread).not.toContain(w12a.state);
    expect(w12a.evidence).toContain("injected ls-files");
    expect(unread).not.toContain(result(r.stdout, "SoT:K6.1a").state); // an AFTER_ENTRIES record (checks.ts:64)
    expect(r.status).toBe(1);
  });

  test("E-1b: an unreadable session-start file is not an Rd1 pass", () => {
    const p = fixture(); p.write("project-memory/.cache/index.sqlite", "cache");
    p.write("CLAUDE.md", "At session start, open project-memory/.cache/index.sqlite.\n");
    chmodSync(join(p.project, "CLAUDE.md"), 0o000);
    expect(unread).not.toContain(result(p.run().stdout, "CACHES:Rd1").state);
  });

  test("E-1c: with an unborn HEAD memory_index.py reads no staging area, so a staged break is not a pass", () => {
    const p = fixture();
    p.git("checkout", "-q", "--orphan", "fresh"); // HEAD names no commit; the index still holds the memory
    breakHeader(p);
    const r = p.run();
    expect(unread).not.toContain(result(r.stdout, "SoT:W1.2a").state);
    expect(r.status).toBe(1);
  });

  test("E-1d: in a SHA-256 repository a staged break is not a pass", () => {
    const p = fixture();
    rmSync(join(p.project, ".git"), { recursive: true, force: true });
    p.git("init", "-q", "--object-format=sha256", "-b", "main");
    p.git("config", "core.hooksPath", "/dev/null");
    p.commit("Initial fixture, SHA-256");
    expect(p.git("rev-parse", "HEAD")).toHaveLength(64);
    breakHeader(p);
    const r = p.run();
    expect(unread).not.toContain(result(r.stdout, "SoT:W1.2a").state);
    expect(r.status).toBe(1);
  });

  test("E-1 control: the planted break fails W1.2a in an ordinary repository", () => {
    const p = fixture(); breakHeader(p);
    expect(result(p.run().stdout, "SoT:W1.2a").state).toBe("fail");
  });

  test("E-1 control: OUTSIDE_PROJECT_MEMORY (checks.ts:57) keeps W3.5a its own result when ls-files fails", () => {
    const p = fixture();
    failingGit(p, `*" ls-files "*" --cached "*`);
    expect(result(p.run().stdout, "SoT:W3.5a").state).toBe("needs a reviewer");
  });

  test("E-1 control: a repository with no project-memory/ stays not applicable, exit 0", () => {
    const p = fixture(false);
    const r = p.run();
    expect(result(r.stdout, "SoT:W1.2a").state).toBe("not applicable");
    expect(r.status).toBe(0);
  });
});

describe("E-2: --out never writes over a memory location", () => {
  const targets: [string, (p: Project) => string][] = [
    ["E-2a: project-memory/INDEX.md", (p) => join(p.project, "project-memory/INDEX.md")],
    ["E-2b: an entry", (p) => join(p.project, entryPath)],
    ["E-2c: AGENTS.md", (p) => join(p.project, "AGENTS.md")],
    ["E-2d: INDEX.md through '..'", (p) => `${p.project}/project-memory/entries/../INDEX.md`],
    ["E-2e: INDEX.md through a symlink", (p) => { const link = join(p.base, "link.md"); symlinkSync(join(p.project, "project-memory/INDEX.md"), link); return link; }],
  ];
  test.each(targets)("%s is a usage error and no byte changes", (_name, target) => {
    const p = fixture();
    const out = target(p);
    const status = p.git("status", "--short"); const before = p.hashes();
    const r = p.run(["--out", out]);
    expect({ hashes: p.hashes(), status: p.git("status", "--short") }).toEqual({ hashes: before, status });
    expect(r.status).toBe(2);
  });

  test("E-2 control: --out report.md still writes", () => {
    const p = fixture();
    const out = join(p.base, "report.md");
    const r = p.run(["--out", out]);
    expect(existsSync(out)).toBe(true);
    expect(r.status).toBe(0);
  });
});
