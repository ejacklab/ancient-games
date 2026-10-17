// Acceptance tests for the second review's accepted TS findings (runs/20261018-finish-everything, step reproduce),
// one per finding, each built from the finding's own input. Written by the reproduce step (Claude), which wrote none
// of src/.
import { afterEach, describe, expect, test } from "bun:test";
import { mkdirSync, writeFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { join } from "node:path";
import { Project, entryPath, emptyIndex } from "./fixtures/project";

const projects: Project[] = [];
function fixture(memory = true) { const p = new Project(memory); projects.push(p); return p; }
afterEach(() => { for (const p of projects.splice(0)) p.close(); });

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
/** The verdict of one id, with its evidence as the failure message, so a red run shows why. */
function expectState(report: string, id: string) { const r = result(report, id); return expect(r.state, r.evidence); }
function rebuildIndex(p: Project) {
  const r = spawnSync("python3", ["tools/memory_index.py"], { cwd: p.project, env: p.env, encoding: "utf8" });
  expect(r.status, r.stdout + r.stderr).toBe(0);
  p.git("add", "project-memory");
}
const cacheRead = "At session start, read project-memory/.cache/index.sqlite\n";

describe("second review: accepted TS findings", () => {
  test("C2: staging the deletion of all of project-memory/ fails K4.1, not 'not applicable'", () => {
    const p = fixture();
    p.git("rm", "-rq", "project-memory");
    const r = p.run();
    expectState(r.stdout, "SoT:K4.1").toBe("fail");
    expect(r.status).toBe(1);
  });

  test("C3: with --since, a staged source change to an entry with no commit in the range fails K4.3", () => {
    const p = fixture();
    p.write("unrelated.txt", "x\n"); p.commit("Unrelated");
    p.plant(entryPath, "source: docs/clock.md", "source: docs/other.md"); // staged, not committed
    expectState(p.run().stdout, "SoT:K4.3").toBe("fail"); // control: without --since it fails
    expectState(p.run(["--since", "HEAD"]).stdout, "SoT:K4.3").toBe("fail");
  });

  test("C4+A3: a SessionStart hook in .claude/settings.json that opens a cache file fails Rd1", () => {
    const p = fixture(); p.write("project-memory/.cache/index.sqlite", "cache");
    p.write(".claude/settings.json", '{"hooks":{"SessionStart":[{"matcher":".*","hooks":[{"type":"command","command":"cat project-memory/.cache/index.sqlite"}]}]}}\n');
    p.commit("SessionStart hook reads the cache");
    expectState(p.run().stdout, "CACHES:Rd1").toBe("fail");
  });

  test("C5: Rd1 reads the staged AGENTS.md, not the working tree", () => {
    const p = fixture(); p.write("project-memory/.cache/index.sqlite", "cache");
    const agents = "Read project-memory/INDEX.md at session start.\n";
    p.write("AGENTS.md", agents + cacheRead); p.git("add", "AGENTS.md");
    expectState(p.run().stdout, "CACHES:Rd1").toBe("fail"); // control: staged and working tree agree
    p.write("AGENTS.md", agents); // removed in the working tree only, not staged
    expect(p.git("diff", "--cached", "--", "AGENTS.md")).toContain("+" + cacheRead.trim());
    expectState(p.run().stdout, "CACHES:Rd1").toBe("fail");
  });

  // C6 belongs here, not in memory_index.py: its B2.5 keeps an inactive entry's problem a warning so the build is not
  // blocked, while W1.1a's fails-if has no status exemption, so the report reads that warning as a fail (main agent).
  test("C6: a retired D- entry with kind: fact fails W1.1a, though memory_index.py only warns", () => {
    const p = fixture();
    p.plant(entryPath, "kind: decision", "kind: fact");
    p.plant(entryPath, "status: active", "status: retired");
    rebuildIndex(p);
    const r = p.run();
    expectState(r.stdout, "SoT:W1.1a").toBe("fail");
  });

  test("C9: two thematic breaks in the body are not a second header block (W6.1a)", () => {
    const p = fixture();
    p.plant(entryPath, "**How to apply:** Store UTC timestamps.", "---\n\nSee below.\n\n---\n\n**How to apply:** Store UTC timestamps.");
    const r = p.run();
    expectState(r.stdout, "SoT:W6.1a").not.toBe("fail");
    expect(rows(r.stdout).filter((row) => row.state === "fail").map((row) => row.id)).toEqual([]);
    expect(r.status).toBe(0);
  });

  test("C11: a regular file in <home>/.claude/agent-memory/ is not a present agent-memory folder", () => {
    const p = fixture();
    mkdirSync(join(p.home, ".claude/agent-memory"), { recursive: true });
    writeFileSync(join(p.home, ".claude/agent-memory/README.md"), "not an agent's folder\n");
    const r = p.run();
    expect(r.stdout).toContain(".claude/agent-memory"); // the F1 table reports the location
    expect(r.stdout.split("\n").filter((line) => /README\.md\/.*\| present \|/.test(line))).toEqual([]);
  });

  test("C12+A5 (C12): a failing W4.1b warning names the entry file", () => {
    const p = fixture();
    p.plant(entryPath, "status: active", "status: invalid");
    const lines = p.run(["--warn"]).stdout.trim().split("\n").filter((line) => line.includes("SoT:W4.1b"));
    expect(lines).toHaveLength(1);
    expect(lines[0]).toContain("D-17-10-abc123-2026-choice.md");
  });

  test("C12+A5 (A5): a warning names an entry file with a space in full", () => {
    const p = fixture();
    const spaced = "project-memory/entries/D-17-10-abc123-2026-time check.md";
    p.git("mv", entryPath, spaced); rebuildIndex(p); p.commit("Rename the entry");
    p.plant(spaced, "Use UTC for stored timestamps.\n\n**Why:**", "Use local time for stored timestamps.\n\n**Why:**");
    rebuildIndex(p); p.commit("Rewrite the claim");
    const lines = p.run(["--warn"]).stdout.trim().split("\n").filter((line) => line.includes("SoT:K4.3"));
    expect(lines).toHaveLength(1);
    expect(lines[0]).toContain(spaced);
  });

  test("A4: superseded with an empty indented bullet under superseded_by fails K4.1", () => {
    const p = fixture();
    p.plant(entryPath, "status: active", "status: superseded");
    p.plant(entryPath, "superseded_by: []", "superseded_by:\n  -");
    p.write("project-memory/INDEX.md", emptyIndex); p.git("add", "project-memory");
    p.commit("Supersede with an empty link");
    expectState(p.run().stdout, "SoT:K4.1").toBe("fail");
  });
});
