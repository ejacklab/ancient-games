import { afterEach, describe, expect, test } from "bun:test";
import { mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { join, basename } from "node:path";
import { spawnSync } from "node:child_process";
import { Project, entry, entryPath, singleIndex, emptyIndex, indexHeader, repository, toolRoot } from "./fixtures/project";

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
function fails(report: string) { return rows(report).filter((r) => r.state === "fail").map((r) => r.id).sort(); }
const cacheIds = ["B1", "B2", "B3", "B4", "B5", "K1", "K2", "K3", "Rd1", "Rd2", "Rd3"];
// Only specification metadata is parsed; expected outcomes never come from src/.
const yaml = readFileSync(join(toolRoot, "guidelines/SOURCE_OF_TRUTH_REQUIREMENTS.yaml"), "utf8");
const records = [...yaml.matchAll(/          - id: (\S+)\n([\s\S]*?)(?=          - id:|      - id:|  - title:|$)/g)].map((m) => ({
  id: `SoT:${m[1]}`, level: m[2]!.match(/            level: (.+)/)![1]!, check: m[2]!.match(/            check: (.+)/)![1]!,
}));

describe("Find", () => {
  test("F1/U1: every present location and agent directory is found", () => {
    const p = fixture(); p.write("CLAUDE.md", "@AGENTS.md\n");
    for (const dir of ["work", "journal", ".cache"]) mkdirSync(join(p.project, "project-memory", dir));
    mkdirSync(join(p.home, ".claude/agent-memory/fixture-agent"), { recursive: true });
    const r = p.run(); expect(r.stdout).toContain(p.project);
    for (const name of ["AGENTS.md", "CLAUDE.md", "project-memory/INDEX.md", "project-memory/entries", "project-memory/work", "project-memory/journal", "project-memory/.cache", ".claude/agent-memory"]) {
      const line = r.stdout.split("\n").find((l) => l.startsWith("|") && l.includes(name));
      expect(line, name).toContain("present");
    }
    expect(r.stdout).toContain("fixture-agent");
  });
  test("F1: absent AGENTS.md fails", () => { const p = fixture(); rmSync(join(p.project, "AGENTS.md")); const r = p.run(); expect(r.status).toBe(1); expect(r.stdout).toMatch(/F1[^\n]*fail/); });
  test("F1/U1: optional locations really are absent", () => { const p = fixture(false); const r = p.run(); for (const path of ["CLAUDE.md", "project-memory/INDEX.md", "project-memory/work", "project-memory/journal", "project-memory/.cache", ".claude/agent-memory"]) expect(r.stdout.split("\n").find((l) => l.startsWith("|") && l.includes(path))).toContain("absent"); });
  test("F2/U6: explicit external project wins over current directory", () => { const p = fixture(); const other = fixture(false); const r = p.run([], other.project); expect(r.stdout.split("\n")[0]).toContain(p.project); expect(result(r.stdout, "SoT:W1.2a").state).toBe("pass"); });
  test("F2: default project is cwd", () => { const p = fixture(); const r = p.run([], p.project, false); expect(r.status).toBe(0); expect(r.stdout.split("\n")[0]).toContain(p.project); });
  for (const kind of ["missing", "subdirectory", "notgit"]) test(`F2/U6: ${kind} project is usage error`, () => { const p = fixture(); const path = join(p.project, kind); if (kind !== "missing") mkdirSync(path); const r = p.run(["--project", path]); expect(r.status).toBe(2); expect(r.stdout).not.toContain("# memory-check"); });
  for (const out of [false, true]) test(`F3/U5: all fixture bytes and git status unchanged, out=${out}`, () => {
    const p = fixture(); p.write("project-memory/.cache/ignored.sqlite", "ignored bytes"); p.write("untracked.txt", "untracked bytes");
    const status = p.git("status", "--short"); const before = p.hashes();
    const r = p.run(out ? ["--out", join(p.project, "report.md")] : []); const after = p.hashes();
    if (out) { expect(after["project/report.md"]).toBeDefined(); delete after["project/report.md"]; }
    const afterStatus = p.git("status", "--short").split("\n").filter((l) => l !== "?? report.md").join("\n");
    expect({ hashes: after, status: afterStatus }).toEqual({ hashes: before, status });
    expect(r.status).toBe(0);
  });
});

describe("Check and report", () => {
  test("C1/R1/T1: all guideline records and levels, with version", () => {
    expect(records).toHaveLength(64); const p = fixture(); const text = p.run().stdout;
    expect(text).toMatch(/SOURCE_OF_TRUTH_REQUIREMENTS.yaml\s+\S+/); expect(text).toMatch(/CACHES.md\s+\S+/);
    expect(rows(text)).toHaveLength(records.length + cacheIds.length);
    for (const record of records) expect(result(text, record.id).level).toBe(record.level);
    for (const id of cacheIds) result(text, `CACHES:${id}`);
  });
  test("C1/C2/U4: every reviewer-only check is listed for a person", () => {
    const text = fixture().run().stdout; const section = text.split(/## Needs a reviewer/i)[1]; expect(section).toBeDefined();
    for (const record of records.filter((r) => /reviewer/.test(r.check) && !/tool|git/.test(r.check))) {
      expect(result(text, record.id).state).toBe("needs a reviewer");
      expect(section).toContain(record.id);
    }
  });
  test("C1: check none (a definition or permission) is not applicable while memory is present", () => {
    const text = fixture().run().stdout;
    const states = records.filter((record) => record.check === "none").map((record) => ({ id: record.id, state: result(text, record.id).state }));
    expect(states).toEqual(states.map((row) => ({ id: row.id, state: "not applicable" }))); // C1 corrected 2026-10-17: a definition has nothing to check
  });
  test("C2: five states, evidence for every pass/fail, mixed check remains reviewer", () => {
    const text = fixture().run().stdout; const all = rows(text); expect(all.length).toBe(75);
    for (const row of all) expect(["pass", "fail", "needs a reviewer", "not applicable", "could not run"]).toContain(row.state);
    const missingEvidence = all.filter((row) => ["pass", "fail"].includes(row.state) && !/(?:\S+:\d+|git |python3 .*--check[\s\S]*(?:output|exit))/.test(row.evidence));
    expect(missingEvidence).toEqual([]);
    expect(result(text, "SoT:W1.3a").state).toBe("needs a reviewer");
  });
  test("C3: existing index checker output is pinned and its failure is propagated", () => {
    const p = fixture();
    const check = () => spawnSync("python3", [join(repository, "tools/memory_index.py"), "--check"], { cwd: p.project, env: p.env, encoding: "utf8" });
    const good = check(); expect(good.status).toBe(0); expect(good.stdout + good.stderr).toBe("INDEX.md: 5/200 lines, 261/24000 bytes\nproject-memory/INDEX.md in the staging area is up to date\n");
    p.plant("project-memory/INDEX.md", "decision: Use UTC for stored timestamps.", "decision: Use local time.");
    expect(check().status).toBe(1); const text = p.run().stdout;
    expect(result(text, "SoT:K6.1a").state).toBe("fail"); expect(result(text, "SoT:K6.2").state).toBe("fail");
  });
  test("C4: absent optional memory and cache never fail", () => {
    const text = fixture(false).run().stdout;
    for (const record of records.filter((record) => !["SoT:W3.5a", "SoT:W3.5b", "SoT:Rd1.1"].includes(record.id))) { const row = result(text, record.id); expect(row.state).toBe("not applicable"); expect(row.evidence).toContain("absent"); }
    for (const id of cacheIds) { const row = result(text, `CACHES:${id}`); expect(row.state).toBe("not applicable"); expect(row.evidence).toContain("absent"); }
  });
  test("C5: first line names staged snapshot and first-memory history range", () => {
    const p = fixture(false); const before = p.git("rev-parse", "HEAD"); p.write(entryPath, entry); p.write("project-memory/INDEX.md", singleIndex); p.commit("Introduce memory"); const first = p.git("rev-parse", "HEAD");
    const line = p.run().stdout.split("\n")[0]!; expect(line).toMatch(/stag/); expect(line).toContain(first.slice(0, 7)); expect(line).toMatch(/history.*(?:HEAD|[a-f0-9]{7})/); expect(line).not.toContain(before.slice(0, 7));
    p.write(entryPath, "unstaged malformed memory"); expect(result(p.run().stdout, "SoT:W1.2a").state).toBe("pass");
  });
  test("C5: --since is printed and excludes earlier deletion", () => {
    const p = fixture(); p.git("rm", entryPath); p.write("project-memory/INDEX.md", emptyIndex); p.commit("Delete entry");
    const original = p.run(); expect(result(original.stdout, "SoT:K4.1").state).toBe("fail");
    p.write("note.txt", "later\n"); p.commit("Later snapshot"); const since = p.git("rev-parse", "HEAD");
    const selected = p.run(["--since", since]); expect(selected.stdout.split("\n")[0]).toContain(since.slice(0, 7)); expect(result(selected.stdout, "SoT:K4.1").state).not.toBe("fail");
  });
  test("C5/R3: shallow history could not run exits 1", () => {
    const p = fixture(); writeFileSync(join(p.project, ".git/shallow"), p.git("rev-parse", "HEAD") + "\n");
    expect(p.git("rev-parse", "--is-shallow-repository")).toBe("true"); const r = p.run(); expect(r.status).toBe(1); const row = result(r.stdout, "SoT:K4.3"); expect(row.state).toBe("could not run"); expect(row.evidence).toMatch(/shallow/i);
  });
  test("C6: present cache checks B2.2/Rd1, leaves others to reviewer", () => {
    const p = fixture(); p.write("project-memory/.cache/index.sqlite", "opaque cache"); const text = p.run().stdout;
    expect(result(text, "CACHES:B2").state).toBe("pass"); expect(result(text, "CACHES:Rd1").state).toBe("pass");
    for (const id of cacheIds.filter((id) => !["B2", "Rd1"].includes(id))) expect(result(text, `CACHES:${id}`).state).toBe("needs a reviewer");
  });
  test("R1: --out writes one Markdown report, MUST results first", () => {
    const p = fixture(); const path = join(p.project, "report.md"); const r = p.run(["--out", path]); expect(r.status).toBe(0);
    const text = readFileSync(path, "utf8"); expect(text).toMatch(/^# .*staged/); expect(text.indexOf("Memory locations")).toBeLessThan(text.indexOf("**SoT:"));
    const all = rows(text).filter((r) => ["MUST", "SHOULD", "guidance"].includes(r.level)); let lower = false;
    for (const row of all) { if (row.level !== "MUST") lower = true; if (lower) expect(row.level).not.toBe("MUST"); }
  });
  test("R2/U3: clean warning is empty", () => { const r = fixture().run(["--warn"]); expect(r.stdout).toBe(""); expect(r.stderr).toBe(""); expect(r.status).toBe(0); });
  test("R2/U3: missing AGENTS prints exactly one warning with file and id", () => { const p = fixture(); rmSync(join(p.project, "AGENTS.md")); const r = p.run(["--warn"]); const lines = r.stdout.trim().split("\n"); expect(lines).toHaveLength(1); expect(lines[0]).toContain("F1"); expect(lines[0]).toContain("AGENTS.md"); expect(r.stdout).not.toContain("Use UTC"); });
  test("R2/U3: broken index warns once per failing MUST, no entry text", () => {
    const p = fixture(); p.plant("project-memory/INDEX.md", "decision: Use UTC for stored timestamps.", "decision: private planted text.");
    const r = p.run(["--warn"]); const lines = r.stdout.trim().split("\n"); expect(lines).toHaveLength(2);
    for (const id of ["SoT:K6.1a", "SoT:K6.2"]) expect(lines.some((l) => l.includes(id) && l.includes("INDEX.md"))).toBe(true);
    expect(r.stdout).not.toContain("private planted text"); expect(r.stdout).not.toContain("Use UTC"); expect(r.status).toBe(1);
  });
  test("R3: failing MUST exits 1 and valid fixture exits 0", () => { const p = fixture(); expect(p.run().status).toBe(0); p.plant(entryPath, "status: active", "status: unknown"); expect(p.run().status).toBe(1); });
  for (const args of [["--unknown"], ["--project"], ["--since", "missing-revision"]]) test(`R3: usage error ${args.join(" ")} exits 2`, () => { expect(fixture().run(args).status).toBe(2); });
});

// U2 insists on exactly one failure per planted requirement, even where the spec duplicates a clause.
const plants: [string, string, string, string][] = [
  ["SoT:W1.1a", entryPath, "kind: decision", "kind: fact"],
  ["SoT:W1.1b", entryPath, "id: 17-10-abc123-2026", "id: malformed"],
  ["SoT:W1.2a", entryPath, "\n---\nUse UTC", "\n--\nUse UTC"],
  ["SoT:W1.3a", entryPath, "**Why:** Shared clocks need one time zone.", "Rationale: Shared clocks need one time zone."],
  ["SoT:W4.1b", entryPath, "status: active", "status: invalid"],
  ["SoT:W6.1a", entryPath, "**How to apply:** Store UTC timestamps.", "---\nid: 17-10-def456-2026\nkind: observation\nstatus: active\n---\nSecond entry.\n**Why:** Second reason.\n**How to apply:** Store UTC timestamps."],
  ["SoT:K4.1", entryPath, "status: active", "status: superseded"],
  ["SoT:K4.3", entryPath, "source: docs/clock.md", "source: docs/other.md"],
  ["SoT:K6.1a", "project-memory/INDEX.md", "decision: Use UTC", "decision: Use local time instead of UTC"],
  ["SoT:K6.2", "project-memory/INDEX.md", "decision: Use UTC", "decision: Use local time instead of UTC"],
  ["SoT:K6.3a", entryPath, "\n**Why:**", "\n<<<<<<< planted\n**Why:**"],
  ["CACHES:B2", ".gitignore", "project-memory/.cache/", "different-cache/"],
  ["CACHES:Rd1", "AGENTS.md", "Read project-memory/INDEX.md at session start.", "At session start open project-memory/.cache/index.sqlite."],
];
describe("U2 planted breaks", () => {
  for (const [id, path, before, after] of plants) test(`U2 ${id}: exactly the planted requirement fails`, () => {
    const needsHistory = ["SoT:K4.1", "SoT:K4.3"].includes(id);
    const p = fixture(needsHistory);
    if (!needsHistory) { p.write(entryPath, entry); p.write("project-memory/INDEX.md", singleIndex); p.git("add", "project-memory"); }
    p.write("project-memory/.cache/index.sqlite", "cache");
    // Instructions/ignore rules are bracketed to keep all replacement plants away from file edges.
    if (["AGENTS.md", ".gitignore"].includes(path)) { p.write(path, `# Fixture\n${readFileSync(join(p.project, path), "utf8")}\n# End fixture\n`); p.commit("Bracket fixture rules"); }
    p.plant(path, before, after);
    if (id === "SoT:K4.1") { p.write("project-memory/INDEX.md", emptyIndex); p.git("add", "project-memory/INDEX.md"); }
    const report = p.run().stdout;
    const row = result(report, id); expect(row.state).toBe("fail"); expect(row.evidence).toContain(basename(path));
    // U2 corrected 2026-10-17: two ids that share one fails_if (K6.1a, K6.2) fail together.
    const shared = ["SoT:K6.1a", "SoT:K6.2"];
    expect(fails(report)).toEqual(shared.includes(id) ? shared : [id]);
  });
  test("U2 SoT:Rd3.1a: oversized literal index fails only size", () => {
    const p = fixture(false);
    p.write(entryPath, readFileSync(join(import.meta.dir, "fixtures/oversized-entry.md"), "utf8"));
    p.write("project-memory/INDEX.md", readFileSync(join(import.meta.dir, "fixtures/oversized-index.md"), "utf8"));
    p.git("add", "project-memory");
    expect(Buffer.byteLength(readFileSync(join(p.project, "project-memory/INDEX.md")))).toBeGreaterThan(24000);
    const independent = spawnSync("python3", [join(repository, "tools/memory_index.py"), "--check"], { cwd: p.project, env: p.env, encoding: "utf8" });
    expect(independent.status).toBe(1); expect(independent.stdout + independent.stderr).toContain("24000");
    const text = p.run().stdout; expect(result(text, "SoT:Rd3.1a").state).toBe("fail"); expect(fails(text)).toEqual(["SoT:Rd3.1a"]);
  });
});

describe("History and exemptions", () => {
  for (const [field, replacement] of [["source: docs/clock.md", "source: docs/other.md"], ["depends_on: []", "depends_on:\n  - 16-10-abc123-2026"], ["covers:\n  - src/time.ts", "covers:\n  - src/clock.ts"]]) {
    test(`U2 SoT:K4.3: immutable header/change log ${field.split(":")[0]}`, () => {
      const p = fixture(); p.write("project-memory/.cache/index.sqlite", "cache"); p.plant(entryPath, field!, replacement!);
      const text = p.run().stdout; expect(result(text, "SoT:K4.3").state).toBe("fail"); expect(fails(text)).toEqual(["SoT:K4.3"]);
    });
  }
  test("C1/U2 SoT:K4.1: committed deletion with current literal index", () => {
    const p = fixture(); p.write("project-memory/.cache/index.sqlite", "cache"); p.git("rm", entryPath); p.write("project-memory/INDEX.md", emptyIndex); p.commit("Delete entry");
    expect(p.git("log", "--diff-filter=D", "--name-only", "--format=", "--", entryPath)).toContain(entryPath);
    const text = p.run().stdout; expect(result(text, "SoT:K4.1").state).toBe("fail"); expect(fails(text)).toEqual(["SoT:K4.1"]);
  });
  test("C1: superseded entry with a replacement link is not a deletion", () => {
    const p = fixture(); p.plant(entryPath, "status: active", "status: superseded"); p.plant(entryPath, "superseded_by: []", "superseded_by:\n  - 18-10-def456-2026");
    p.write("project-memory/INDEX.md", emptyIndex); p.git("add", "project-memory");
    expect(result(p.run().stdout, "SoT:K4.1").state).not.toBe("fail");
  });
  test("C1: covers correction with a new changed line is allowed", () => {
    const p = fixture(); p.plant(entryPath, "  - src/time.ts", "  - src/clock.ts");
    p.plant(entryPath, "  - 2026-10-17T00:00:00Z fixture created", "  - 2026-10-17T00:00:00Z fixture created\n  - 2026-10-17T01:00:00Z fixture corrected path");
    expect(result(p.run().stdout, "SoT:K4.3").state).toBe("pass");
  });
  test("C1: SHOULD history with a written-reason exemption needs a reviewer", () => {
    const p = fixture(); p.plant(entryPath, "  - src/time.ts", "  - src/clock.ts"); p.write("project-memory/journal/session.md", "Notes from session one.\n"); p.commit("Edit without changed log; rationale needs human judgment");
    p.write("project-memory/journal/session.md", "Rewritten notes.\n"); p.commit("Rewrite journal");
    const text = p.run().stdout;
    for (const id of ["W2.1b", "W4.2", "W5.1", "W6.1b", "W6.2", "K1.1", "K5.1"]) expect(result(text, `SoT:${id}`).state).toBe("needs a reviewer");
  });
  test("C1: two entries superseding one needs a reviewer", () => {
    const p = fixture();
    p.write("project-memory/entries/O-17-10-def456-2026-one.md", entry.replace("17-10-abc123-2026", "17-10-def456-2026").replace("kind: decision", "kind: observation").replace("status: active", "status: retired").replace("supersedes: []", "supersedes:\n  - 16-10-aaaaaa-2026"));
    p.write("project-memory/entries/O-17-10-ghi789-2026-two.md", entry.replace("17-10-abc123-2026", "17-10-ghi789-2026").replace("kind: decision", "kind: observation").replace("status: active", "status: retired").replace("supersedes: []", "supersedes:\n  - 16-10-aaaaaa-2026"));
    p.git("add", "project-memory"); expect(result(p.run().stdout, "SoT:W6.3a").state).toBe("needs a reviewer");
  });
  test("R2: warning mode never includes opaque cache content", () => {
    const p = fixture(); p.write("project-memory/.cache/index.sqlite", "CACHE_PRIVATE_SENTINEL");
    const r = p.run(["--warn"]); expect(r.stdout).toBe(""); expect(r.stderr).toBe("");
  });
});

describe("U2 git requirements", () => {
  test("U2 SoT:W1.1a: git records a kind-prefix rename", () => {
    const p = fixture(); p.write("project-memory/.cache/index.sqlite", "cache");
    const renamed = entryPath.replace("/D-", "/F-"); p.git("mv", entryPath, renamed); p.plant(renamed, "kind: decision", "kind: fact");
    p.write("project-memory/INDEX.md", indexHeader + "- [17-10-abc123-2026](entries/F-17-10-abc123-2026-choice.md) fact: Use UTC for stored timestamps.\n"); p.commit("Forbidden kind rename");
    expect(p.git("diff", "-M", "--name-status", "HEAD^", "HEAD")).toMatch(/R\d+\s+project-memory\/entries\/D-/);
    const text = p.run().stdout; expect(result(text, "SoT:W1.1a").state).toBe("fail"); expect(fails(text)).toEqual(["SoT:W1.1a"]);
  });
  test("U2 SoT:W1.1b: git records an id rename", () => {
    const p = fixture(); p.write("project-memory/.cache/index.sqlite", "cache");
    const renamed = entryPath.replace("abc123", "def456"); p.git("mv", entryPath, renamed); p.plant(renamed, "id: 17-10-abc123-2026", "id: 17-10-def456-2026");
    p.write("project-memory/INDEX.md", indexHeader + "- [17-10-def456-2026](entries/D-17-10-def456-2026-choice.md) decision: Use UTC for stored timestamps.\n"); p.commit("Forbidden id rename");
    expect(p.git("diff", "-M", "--name-status", "HEAD^", "HEAD")).toMatch(/R\d+/);
    const text = p.run().stdout; expect(result(text, "SoT:W1.1b").state).toBe("fail"); expect(fails(text)).toEqual(["SoT:W1.1b"]);
  });
  test("U2 SoT:W6.3a: merge discards the other side's covers and changed line", () => {
    const p = fixture(); p.write("project-memory/.cache/index.sqlite", "cache"); p.git("checkout", "-qb", "right");
    p.plant(entryPath, "  - src/time.ts", "  - src/time.ts\n  - src/right.ts");
    p.plant(entryPath, "  - 2026-10-17T00:00:00Z fixture created", "  - 2026-10-17T00:00:00Z fixture created\n  - 2026-10-17T01:00:00Z right added coverage"); p.commit("Right coverage");
    p.git("checkout", "-q", "main"); p.write("left.txt", "left side\n"); p.commit("Left work"); p.git("merge", "-q", "--no-ff", "-s", "ours", "right", "-m", "Discard right metadata");
    expect(p.git("rev-list", "--parents", "-n", "1", "HEAD").split(" ")).toHaveLength(3);
    expect(p.git("show", `HEAD^2:${entryPath}`)).toContain("src/right.ts"); expect(readFileSync(join(p.project, entryPath), "utf8")).not.toContain("src/right.ts");
    const text = p.run().stdout; expect(result(text, "SoT:W6.3a").state).toBe("fail"); expect(fails(text)).toEqual(["SoT:W6.3a"]);
  });
});

test("R2/U3: warning includes a history MUST failure", () => {
  const p = fixture(); p.plant(entryPath, "source: docs/clock.md", "source: docs/replaced.md");
  expect(result(p.run().stdout, "SoT:K4.3").state).toBe("fail");
  const warning = p.run(["--warn"]).stdout.trim().split("\n");
  expect(warning).toHaveLength(1); expect(warning[0]).toContain("SoT:K4.3"); expect(warning[0]).toContain("D-17-10-abc123-2026-choice.md");
});
