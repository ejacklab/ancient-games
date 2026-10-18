// Acceptance checks written from SPEC.md Round 20 (DL1-DL4), independently of the implementation.
// The CLI reads the real clock, so deadlines are planted far in the past (up) or with very long budgets (running).
import { afterEach, expect, test } from "bun:test";
import { execFileSync, spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import type { Deadline } from "../src/types.ts";

const CLI = path.resolve(import.meta.dirname, "../src/cli.ts");
const roots: string[] = [];
afterEach(() => {
  for (const root of roots.splice(0)) fs.rmSync(root, { recursive: true, force: true });
});

// Running: started in the past with a budget of centuries. Up: started in 2000 with ten minutes.
const LONG = 100_000_000;

function box() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "hg-r20-deadline-"));
  roots.push(root);
  execFileSync("git", ["init", "-q"], { cwd: root });
  const file = (id: string) => path.join(root, `.harness-guard/deadlines/${id}.json`);
  const plant = (deadline: Deadline) => {
    fs.mkdirSync(path.dirname(file(deadline.id)), { recursive: true });
    fs.writeFileSync(file(deadline.id), JSON.stringify(deadline));
    return deadline;
  };
  const stored = (id: string): Deadline => JSON.parse(fs.readFileSync(file(id), "utf8"));
  const cli = (...args: string[]) => spawnSync(process.execPath, [CLI, ...args], {
    cwd: root, encoding: "utf8", timeout: 10_000,
    env: { ...process.env, BUN_RUNTIME_TRANSPILER_CACHE_PATH: "0", TZ: Intl.DateTimeFormat().resolvedOptions().timeZone },
  });
  return { root, plant, stored, cli };
}

const running = (id: string, start: string, minutes: number, session: string | null, run: string | null): Deadline =>
  ({ id, start, minutes, run, session });
const up = (id: string, start: string, session: string | null, run: string | null): Deadline =>
  ({ id, start, minutes: 10, run, session });

// ---- DL1 --id ------------------------------------------------------------------------------------------------------

test("DL1: status --id shows that deadline, though another session's and older than the session's own", () => {
  const b = box();
  b.plant(running("D-00000001", "2000-01-01T00:00:00.000Z", LONG, "other", "runs/a"));
  b.plant(running("D-00000002", "2001-01-01T00:00:00.000Z", 3 * LONG, "s", "runs/b"));
  const result = b.cli("deadline", "status", "--id", "D-00000001");
  expect(result.status).toBe(0);
  expect(result.stdout).toContain(`of ${LONG} min`);
  expect(result.stdout).not.toContain(`of ${3 * LONG} min`);
  // --session names a session; --id still wins: it acts on that deadline only, whatever its session.
  const withSession = b.cli("deadline", "status", "--id", "D-00000001", "--session", "s");
  expect(withSession.status).toBe(0);
  expect(withSession.stdout).toContain(`of ${LONG} min`);
});

test("DL1: status --id of a deadline that is up says so with exit 1, while the newest one runs", () => {
  const b = box();
  b.plant(up("D-00000001", "2000-01-01T00:00:00.000Z", "s", null));
  b.plant(running("D-00000002", "2001-01-01T00:00:00.000Z", LONG, "s", null));
  const result = b.cli("deadline", "status", "--id", "D-00000001");
  expect(result.status).toBe(1);
  expect(result.stdout).toMatch(/time is up/);
});

test("DL1: wait --id waits on that deadline only: one that is up returns at once, though another runs for centuries", () => {
  const b = box();
  b.plant(up("D-00000001", "2000-01-01T00:00:00.000Z", "other", null));
  b.plant(running("D-00000002", "2001-01-01T00:00:00.000Z", LONG, "s", null));
  const result = b.cli("deadline", "wait", "--id", "D-00000001");
  expect(result.error).toBeUndefined(); // a wait on the running one would be killed by the 10 s timeout
  expect(result.status).toBe(0);
  expect(result.stdout).toMatch(/time is up/);
}, 15_000);

test("DL1: end --id ends that deadline only, whatever its session or run", () => {
  const b = box();
  b.plant(running("D-00000001", "2000-01-01T00:00:00.000Z", LONG, "other", "runs/a"));
  b.plant(running("D-00000002", "2001-01-01T00:00:00.000Z", LONG, "s", "runs/b"));
  b.plant(running("D-00000003", "2002-01-01T00:00:00.000Z", LONG, "s", "runs/a"));
  const result = b.cli("deadline", "end", "--id", "D-00000001");
  expect(result.status).toBe(0);
  expect(result.stdout).toContain("D-00000001 ended");
  expect(b.stored("D-00000001").ended).toEqual(expect.any(String));
  expect(b.stored("D-00000002").ended).toBeUndefined();
  expect(b.stored("D-00000003").ended).toBeUndefined();
});

test.each([["status"], ["wait"], ["end"]])("DL1: %s --id with no deadline file says no deadline <id> and exits 2", (verb: string) => {
  const b = box();
  b.plant(running("D-00000001", "2000-01-01T00:00:00.000Z", LONG, "s", null));
  const result = b.cli("deadline", verb, "--id", "D-0000dead");
  expect(result.error).toBeUndefined();
  expect(result.status).toBe(2);
  expect(result.stderr).toContain("no deadline D-0000dead");
  expect(b.stored("D-00000001").ended).toBeUndefined();
}, 15_000);

test("DL1: status --id of an ended deadline prints <id> ended <time> and exits 0", () => {
  const b = box();
  b.plant({ ...running("D-00000001", "2000-01-01T00:00:00.000Z", LONG, "s", null), ended: "2000-01-02T00:00:00.000Z" });
  const result = b.cli("deadline", "status", "--id", "D-00000001");
  expect(result.status).toBe(0);
  expect(result.stdout).toMatch(/D-00000001 ended \S+/);
});

// ---- DL2 --run -----------------------------------------------------------------------------------------------------

function runBox() {
  const b = box();
  b.plant(running("D-00000001", "2000-01-01T00:00:00.000Z", LONG, "s", "runs/a"));
  b.plant(running("D-00000002", "2001-01-01T00:00:00.000Z", 3 * LONG, "other", "runs/a"));
  // newer, but ended: not open
  b.plant({ ...running("D-00000003", "2002-01-01T00:00:00.000Z", 5 * LONG, "s", "runs/a"), ended: "2002-01-02T00:00:00.000Z" });
  // newest of all, another run
  b.plant(running("D-00000004", "2003-01-01T00:00:00.000Z", 2 * LONG, "s", "runs/b"));
  return b;
}

test("DL2: status --run shows the newest open deadline whose run is DIR", () => {
  const b = runBox();
  const result = b.cli("deadline", "status", "--run", "runs/a");
  expect(result.status).toBe(0);
  expect(result.stdout).toContain(`of ${3 * LONG} min`);
  for (const minutes of [LONG, 5 * LONG, 2 * LONG]) expect(result.stdout).not.toContain(`of ${minutes} min`);
});

test("DL2: --run is compared as deadline start --run stores it, relative to the root", () => {
  const b = runBox();
  for (const dir of [path.join(b.root, "runs/a"), "./runs/a/"]) {
    const result = b.cli("deadline", "status", "--run", dir);
    expect(result.status).toBe(0);
    expect(result.stdout).toContain(`of ${3 * LONG} min`);
  }
});

test("DL2: a deadline recorded by deadline start --run is found by status --run with the same DIR", () => {
  const b = box();
  // starts after the one recorded now, so it is the newest of all
  b.plant(running("D-00000001", "2100-01-01T00:00:00.000Z", LONG, "s", "runs/other"));
  expect(b.cli("deadline", "start", "--minutes", "1000", "--run", "runs/task").status).toBe(0);
  const result = b.cli("deadline", "status", "--run", "runs/task");
  expect(result.status).toBe(0);
  expect(result.stdout).toContain("of 1000 min");
});

test("DL2: end --run ends the newest open deadline of that run only", () => {
  const b = runBox();
  const result = b.cli("deadline", "end", "--run", "runs/a");
  expect(result.status).toBe(0);
  expect(result.stdout).toContain("D-00000002 ended");
  expect(b.stored("D-00000002").ended).toEqual(expect.any(String));
  expect(b.stored("D-00000001").ended).toBeUndefined();
  expect(b.stored("D-00000004").ended).toBeUndefined();
});

test("DL2: wait --run waits on that run's deadline: one that is up returns at once, though another runs", () => {
  const b = box();
  b.plant(up("D-00000001", "2000-01-01T00:00:00.000Z", "s", "runs/a"));
  b.plant(running("D-00000002", "2001-01-01T00:00:00.000Z", LONG, "s", "runs/b"));
  const result = b.cli("deadline", "wait", "--run", "runs/a");
  expect(result.error).toBeUndefined();
  expect(result.status).toBe(0);
  expect(result.stdout).toMatch(/time is up/);
}, 15_000);

test.each([["status"], ["wait"], ["end"]])("DL2: %s --run with no open deadline of DIR says no deadline for <DIR> and exits 2", (verb: string) => {
  const b = runBox();
  b.plant({ ...running("D-00000005", "2004-01-01T00:00:00.000Z", LONG, "s", "runs/zzz"), ended: "2004-01-02T00:00:00.000Z" });
  const result = b.cli("deadline", verb, "--run", "runs/zzz");
  expect(result.error).toBeUndefined();
  expect(result.status).toBe(2);
  expect(result.stderr).toContain("no deadline for runs/zzz");
  for (const id of ["D-00000001", "D-00000002", "D-00000004"]) expect(b.stored(id).ended).toBeUndefined();
}, 15_000);

// ---- DL3 end never guesses -----------------------------------------------------------------------------------------

test("DL3: end with neither flag and two open deadlines ends none, lists each open id with its run, exits 2", () => {
  const b = box();
  b.plant(running("D-00000001", "2000-01-01T00:00:00.000Z", LONG, "s", "runs/a"));
  b.plant(running("D-00000002", "2001-01-01T00:00:00.000Z", LONG, "other", "runs/b"));
  const result = b.cli("deadline", "end");
  expect(result.status).toBe(2);
  expect(result.stderr).toMatch(/D-00000001.*runs\/a/);
  expect(result.stderr).toMatch(/D-00000002.*runs\/b/);
  expect(b.stored("D-00000001").ended).toBeUndefined();
  expect(b.stored("D-00000002").ended).toBeUndefined();
});

test("DL3: end --session with two open deadlines in that session ends none and exits 2", () => {
  const b = box();
  b.plant(running("D-00000001", "2000-01-01T00:00:00.000Z", LONG, "s", "runs/a"));
  b.plant(running("D-00000002", "2001-01-01T00:00:00.000Z", LONG, "s", "runs/b"));
  const result = b.cli("deadline", "end", "--session", "s");
  expect(result.status).toBe(2);
  expect(result.stderr).toMatch(/D-00000001.*runs\/a/);
  expect(result.stderr).toMatch(/D-00000002.*runs\/b/);
  expect(b.stored("D-00000001").ended).toBeUndefined();
  expect(b.stored("D-00000002").ended).toBeUndefined();
});

test("DL3: end with neither flag and exactly one open deadline ends that one, as before", () => {
  const b = box();
  b.plant({ ...running("D-00000001", "2000-01-01T00:00:00.000Z", LONG, "s", "runs/a"), ended: "2000-01-02T00:00:00.000Z" });
  b.plant(running("D-00000002", "2001-01-01T00:00:00.000Z", LONG, "other", "runs/b"));
  const result = b.cli("deadline", "end");
  expect(result.status).toBe(0);
  expect(result.stdout).toContain("D-00000002 ended");
  expect(b.stored("D-00000002").ended).toEqual(expect.any(String));
});

test("DL3: end --session with one open deadline in that session ends it, though another session has one open", () => {
  const b = box();
  b.plant(running("D-00000001", "2000-01-01T00:00:00.000Z", LONG, "s", "runs/a"));
  b.plant(running("D-00000002", "2001-01-01T00:00:00.000Z", LONG, "other", "runs/b"));
  const result = b.cli("deadline", "end", "--session", "s");
  expect(result.status).toBe(0);
  expect(result.stdout).toContain("D-00000001 ended");
  expect(b.stored("D-00000001").ended).toEqual(expect.any(String));
  expect(b.stored("D-00000002").ended).toBeUndefined();
});

// ---- DL4 unchanged -------------------------------------------------------------------------------------------------

test("DL4: status with neither flag keeps today's choice — the session's newest running deadline — with several open", () => {
  const b = box();
  b.plant(running("D-00000001", "2000-01-01T00:00:00.000Z", LONG, "s", "runs/a"));
  b.plant(up("D-00000002", "2020-01-01T00:00:00.000Z", "s", "runs/b")); // newer, but up
  b.plant(running("D-00000003", "2021-01-01T00:00:00.000Z", 3 * LONG, "other", "runs/c")); // another session's
  const own = b.cli("deadline", "status", "--session", "s");
  expect(own.status).toBe(0);
  expect(own.stdout).toContain(`of ${LONG} min`);
  // Every session: the newest running one of all.
  const all = b.cli("deadline", "status");
  expect(all.status).toBe(0);
  expect(all.stdout).toContain(`of ${3 * LONG} min`);
});

test("DL4: wait with neither flag keeps today's choice and does not refuse when several are open", () => {
  const b = box();
  const start = new Date().toISOString();
  b.plant(running("D-00000001", start, 0.03, "s", "runs/a")); // about 2 s
  b.plant(up("D-00000002", "2000-01-01T00:00:00.000Z", "s", "runs/b"));
  b.plant(running("D-00000003", "2000-01-01T00:00:00.000Z", LONG, "other", "runs/c"));
  const result = b.cli("deadline", "wait", "--session", "s");
  expect(result.error).toBeUndefined();
  expect(result.status).toBe(0);
  expect(result.stdout).toMatch(/time is up/);
  expect(Date.now()).toBeGreaterThanOrEqual(Date.parse(start) + 0.03 * 60_000);
}, 15_000);
