// Regression tests from Codex's read-only review (runs/20261017-memory-check/nodes/review.codex.md), one per
// finding, each built from the finding's own input. Written by the main agent (Claude), which wrote none of src/.
import { afterEach, describe, expect, test } from "bun:test";
import { chmodSync, mkdirSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { execSync } from "node:child_process";
import { join } from "node:path";
import { Project, entry, entryPath, emptyIndex, indexHeader, singleIndex } from "./fixtures/project";

const projects: Project[] = [];
function fixture(memory = true) { const p = new Project(memory); projects.push(p); return p; }
afterEach(() => { for (const p of projects.splice(0)) p.close(); });

type Row = { id: string; state: string; evidence: string };
function rows(report: string): Row[] {
  return [...report.matchAll(/^- \*\*((?:SoT|CACHES):[^*]+)\*\* \(([^)]+)\) — (pass|fail|needs a reviewer|not applicable|could not run) — (.*)$/gm)]
    .map((m) => ({ id: m[1]!, state: m[3]!, evidence: m[4]! }));
}
function state(report: string, id: string): string {
  const found = rows(report).filter((r) => r.id === id);
  expect(found.length, `one result for ${id}`).toBe(1);
  return found[0]!.state;
}

describe("Codex review findings", () => {
  test("1: an entry memory_index.py cannot decode is not a pass", () => {
    const p = fixture();
    writeFileSync(join(p.project, entryPath), Buffer.concat([Buffer.from(entry), Buffer.from([0xff, 0xfe, 0x0a])]));
    p.git("add", entryPath);
    const r = p.run();
    for (const id of ["SoT:K6.1a", "SoT:K6.2"]) expect(state(r.stdout, id)).not.toBe("pass");
    expect(r.status).toBe(1);
  });

  test("2a: when entry validation stops memory_index.py, the index checks are not passes", () => {
    const p = fixture();
    p.plant(entryPath, "---\nUse UTC", "Use UTC"); // the header loses its closing delimiter (W1.2a)
    p.write("project-memory/INDEX.md", indexHeader + "- [17-10-zzz999-2026](entries/D-x.md) decision: Something else.\n");
    p.git("add", "project-memory");
    const text = p.run().stdout;
    for (const id of ["SoT:K6.1a", "SoT:K6.2", "SoT:Rd3.1a"]) expect(state(text, id), id).not.toBe("pass");
  });

  test("3: staged memory removed from the working tree is still checked from the staged state", () => {
    const p = fixture();
    p.plant(entryPath, "status: active", "status: invalid"); // staged W4.1b break
    rmSync(join(p.project, "project-memory"), { recursive: true, force: true }); // removed, the removal not staged
    expect(state(p.run().stdout, "SoT:W4.1b")).toBe("fail");
  });

  test("4: a staged entry deletion with a matching empty index fails K4.1", () => {
    const p = fixture();
    p.git("rm", "-q", entryPath);
    p.write("project-memory/INDEX.md", emptyIndex); p.git("add", "project-memory/INDEX.md");
    expect(state(p.run().stdout, "SoT:K4.1")).toBe("fail");
  });

  test("5: a claim rewritten and then restored still fails K4.3", () => {
    const p = fixture();
    p.plant(entryPath, "Use UTC for stored timestamps.\n\n**Why:**", "Use local time for stored timestamps.\n\n**Why:**");
    p.commit("Rewrite the claim");
    p.plant(entryPath, "Use local time for stored timestamps.\n\n**Why:**", "Use UTC for stored timestamps.\n\n**Why:**");
    p.commit("Restore the claim");
    expect(state(p.run().stdout, "SoT:K4.3")).toBe("fail");
  });

  test("6: --since does not drop an entry created before the range from K4.3", () => {
    const p = fixture();
    p.write("unrelated.txt", "x\n"); p.commit("Unrelated");
    const since = p.git("rev-parse", "HEAD");
    p.plant(entryPath, "source: docs/clock.md", "source: docs/other.md"); p.commit("Change source in range");
    expect(state(p.run(["--since", since]).stdout, "SoT:K4.3")).toBe("fail");
  });

  test("7: a merge that drops a whole entry added on one side fails", () => {
    const p = fixture();
    p.git("checkout", "-q", "-b", "side");
    const added = "project-memory/entries/O-17-10-def456-2026-note.md";
    p.write(added, entry.replace("17-10-abc123-2026", "17-10-def456-2026").replace("kind: decision", "kind: observation"));
    p.write("project-memory/INDEX.md", singleIndex + "- [17-10-def456-2026](entries/O-17-10-def456-2026-note.md) observation: Use UTC for stored timestamps.\n");
    p.commit("Add an entry on side");
    p.git("checkout", "-q", "main");
    p.git("merge", "-q", "-s", "ours", "--no-edit", "side");
    const text = p.run().stdout;
    expect(["SoT:K4.1", "SoT:W6.3a"].some((id) => state(text, id) === "fail")).toBe(true);
  });

  test("8: K4.1 with no mechanical break is needs a reviewer, not pass (C2)", () => {
    const p = fixture();
    expect(state(p.run().stdout, "SoT:K4.1")).toBe("needs a reviewer");
  });

  test("9: a quoted superseded status without a link fails K4.1", () => {
    const p = fixture();
    p.plant(entryPath, "status: active", 'status: "superseded"');
    p.write("project-memory/INDEX.md", emptyIndex); p.git("add", "project-memory");
    expect(state(p.run().stdout, "SoT:K4.1")).toBe("fail");
  });

  test("10a: an on-demand cache read in AGENTS.md is not an Rd1 fail", () => {
    const p = fixture(); p.write("project-memory/.cache/index.sqlite", "cache");
    p.write("AGENTS.md", "Read project-memory/INDEX.md at session start.\nOn demand, open project-memory/.cache/index.sqlite to search.\n");
    p.commit("On-demand cache read");
    expect(state(p.run().stdout, "CACHES:Rd1")).not.toBe("fail");
  });

  test("10b: a session-start cache read beside a negation is not a pass", () => {
    const p = fixture(); p.write("project-memory/.cache/index.sqlite", "cache");
    p.write("AGENTS.md", "At session start, do not read entries; open project-memory/.cache/index.sqlite.\n");
    p.commit("Start-time cache read");
    expect(state(p.run().stdout, "CACHES:Rd1")).not.toBe("pass");
  });

  test("11: the warning never holds entry text", () => {
    const p = fixture();
    p.plant(entryPath, "Use UTC for stored timestamps.\n\n**Why:**", "Use local time for stored timestamps.\n\n**Why:**");
    p.commit("Rewrite the claim");
    const r = p.run(["--warn"]);
    expect(r.stdout).toContain("K4.3");
    expect(r.stdout).not.toContain("Use local time");
    expect(r.stdout).not.toContain("Use UTC");
  });

  test("12: a git failure is could not run, never an empty pass", () => {
    const p = fixture();
    const bin = join(p.base, "bin"); mkdirSync(bin);
    const real = execSync("command -v git", { encoding: "utf8" }).trim();
    writeFileSync(join(bin, "git"), `#!/bin/sh\nfor a in "$@"; do [ "$a" = log ] && { echo "fatal: injected" >&2; exit 128; }; done\nexec ${real} "$@"\n`);
    chmodSync(join(bin, "git"), 0o755);
    p.env.PATH = `${bin}:${p.env.PATH}`;
    const text = p.run().stdout;
    expect(state(text, "SoT:K4.3")).not.toBe("pass");
    expect(state(text, "SoT:K4.1")).not.toBe("pass");
  });

  test("13: a configured bun transpiler cache gets nothing written into it", () => {
    const p = fixture();
    const cache = join(p.home, "bun-cache"); mkdirSync(cache);
    p.env.BUN_RUNTIME_TRANSPILER_CACHE_PATH = cache;
    p.run();
    expect(readdirSync(cache)).toEqual([]);
  });

  test("14: a fenced YAML example inside one entry is not a second entry (W6.1a)", () => {
    const p = fixture();
    p.plant(entryPath, "**How to apply:** Store UTC timestamps.", "**How to apply:** Store UTC timestamps, for example:\n\n```yaml\n---\nkey: value\n---\n```");
    expect(state(p.run().stdout, "SoT:W6.1a")).not.toBe("fail");
  });
});
