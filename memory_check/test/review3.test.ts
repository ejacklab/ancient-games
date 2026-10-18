// Acceptance tests for the Codex review's findings 1-3 (runs/20261018-finish-everything/nodes/codex-review.md, each
// reproduced in codex-review-judge.md), one per finding, each built from the finding's own input. Written by the tests
// step of r20c (Claude), which wrote none of src/.
import { afterEach, describe, expect, test } from "bun:test";
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

const lastBodyLine = "**How to apply:** Store UTC timestamps.";

describe("Codex review: findings 1-3", () => {
  test("F1: a SessionStart hook 'cat <cache> || echo not found' still opens the cache and fails Rd1", () => {
    const p = fixture(); p.write("project-memory/.cache/index.sqlite", "cache");
    p.write(".claude/settings.json", '{"hooks":{"SessionStart":[{"matcher":".*","hooks":[{"type":"command","command":"cat project-memory/.cache/index.sqlite || echo not found"}]}]}}\n');
    p.commit("SessionStart hook reads the cache, with a fallback");
    expectState(p.run().stdout, "CACHES:Rd1").toBe("fail");
  });

  test("F2: a second header block after a body '---' pair with no field line fails W6.1a by its id: line", () => {
    const p = fixture();
    const second = "---\nid: 17-10-def456-2026\nkind: decision\nstatus: active\n---\nUse local time for display.";
    p.plant(entryPath, lastBodyLine, `${lastBodyLine}\n\n---\n\nSee below.\n\n---\n\n${second}`);
    const r = result(p.run().stdout, "SoT:W6.1a");
    expect(r.state, r.evidence).toBe("fail");
    expect(r.evidence).toContain("a second id: line");
  });

  test("F2: a body '---' pair holding 'Note: keep UTC timestamps.' is not a second header block (W6.1a)", () => {
    const p = fixture();
    p.plant(entryPath, lastBodyLine, `---\n\nNote: keep UTC timestamps.\n\n---\n\n${lastBodyLine}`);
    const r = p.run();
    expectState(r.stdout, "SoT:W6.1a").not.toBe("fail");
    expect(rows(r.stdout).filter((row) => row.state === "fail").map((row) => row.id)).toEqual([]);
    expect(r.status).toBe(0);
  });

  test("F3: the K4.1 warning for a staged deletion of an entry names the deleted file", () => {
    const p = fixture();
    p.git("rm", "-q", entryPath);
    p.write("project-memory/INDEX.md", emptyIndex); p.git("add", "project-memory/INDEX.md");
    expectState(p.run().stdout, "SoT:K4.1").toBe("fail"); // control: the deletion is a K4.1 failure
    const lines = p.run(["--warn"]).stdout.trim().split("\n").filter((line) => line.includes("SoT:K4.1"));
    expect(lines).toHaveLength(1);
    expect(lines[0]).toContain("D-17-10-abc123-2026-choice.md");
  });
});
