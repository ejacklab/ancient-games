// Acceptance checks written from SPEC.md Round 10, independently of the implementation.
import { afterEach, expect, test } from "bun:test";
import { execFileSync, spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { startDeadline, deadlineStatus, progressSummary, endDeadline } from "../src/deadline.ts";
import { handleHook } from "../src/hooks.ts";
import { readJournal } from "../src/journal.ts";
import type { Deadline, HookResult, ProgressSummary } from "../src/types.ts";

const CLI = path.resolve(import.meta.dirname, "../src/cli.ts");
const EPOCH = Date.parse("2026-10-16T02:00:00.000Z");
const roots: string[] = [];
afterEach(() => {
  for (const root of roots.splice(0)) fs.rmSync(root, { recursive: true, force: true });
});

function box() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "hg-deadline-"));
  roots.push(root);
  execFileSync("git", ["init", "-q"], { cwd: root });
  let tick = EPOCH;
  const env = { cwd: root, running: [], now: () => new Date(tick) };
  const at = (minutes: number) => { tick = EPOCH + minutes * 60_000; };
  const write = (file: string, text: string) => {
    const absolute = path.join(root, file);
    fs.mkdirSync(path.dirname(absolute), { recursive: true });
    fs.writeFileSync(absolute, text);
    return absolute;
  };
  const post = (payload: Record<string, unknown> = {}, session = "s") => handleHook({
    session_id: session, cwd: root, hook_event_name: "PostToolUse", tool_name: "Bash",
    tool_input: { command: "true" }, tool_response: { stdout: "", stderr: "", interrupted: false }, ...payload,
  }, env);
  const prompt = (session = "s") => post({ hook_event_name: "UserPromptSubmit", prompt: "work" }, session);
  const cli = (...args: string[]) => spawnSync(process.execPath, [CLI, ...args], {
    cwd: root, encoding: "utf8", timeout: 10_000,
    // The CLI prints local time; bun test runs in UTC, so the child gets the same zone (COO, integration).
    env: { ...process.env, BUN_RUNTIME_TRANSPILER_CACHE_PATH: "0", TZ: Intl.DateTimeFormat().resolvedOptions().timeZone },
  });
  const save = (deadline: Deadline) => write(`.harness-guard/deadlines/${deadline.id}.json`, JSON.stringify(deadline));
  const plant = (overrides: Partial<Deadline> = {}) => {
    const deadline: Deadline = {
      id: "D-00000001", start: env.now().toISOString(), minutes: 10,
      run: null, marks: [50, 80, 100], session: "s", ...overrides,
    };
    save(deadline);
    return deadline;
  };
  const raised = (id: string, session = "s") => readJournal(root).records.filter(
    (r) => r.kind === "raised" && r.session === session && r.ids.includes(id),
  );
  return { root, env, at, write, post, prompt, cli, save, plant, raised };
}

type Box = ReturnType<typeof box>;
function context(result: HookResult): string {
  expect(result.exitCode).toBe(0);
  return result.stdout === "" ? "" : JSON.parse(result.stdout).hookSpecificOutput?.additionalContext ?? "";
}
function claim(b: Box, session = "s") {
  return b.post({ tool_input: { command: `bun ${CLI} deadline start --minutes 10` } }, session);
}
function line(minutes: number, piece: string, state: string, note = "small piece"): string {
  return `- ${new Date(EPOCH + minutes * 60_000).toISOString()} · ${piece} · ${state} · ${note}\n`;
}
function progress(b: Box, node = "worker", text = line(0, "A", "planned") + line(1, "A", "done")) {
  return b.write(`runs/task/nodes/${node}.progress.md`, text);
}

test.each([[], ["--minutes", "0"], ["--minutes", "-1"], ["--minutes", "nope"], ["--minutes", "Infinity"]].map((args) => [args]))(
  "T1 Fails-if: CLI accepts missing or invalid minutes: %j", (args: string[]) => {
    const b = box();
    expect(b.cli("deadline", "start", ...args).status).toBe(2);
    const directory = path.join(b.root, ".harness-guard/deadlines");
    expect(fs.existsSync(directory) ? fs.readdirSync(directory) : []).toEqual([]);
  },
);

test.each([0, -1, Number.NaN, Number.POSITIVE_INFINITY])("T1: module refuses invalid minutes %s", (minutes) => {
  const b = box();
  expect(() => startDeadline(b.root, { minutes }, b.env.now())).toThrow();
});

test.each(["0,100", "50.5,100", "101,100", "x,100"])("T1: CLI rejects invalid marks %s", (marks) => {
  expect(box().cli("deadline", "start", "--minutes", "10", "--marks", marks).status).toBe(2);
});

test("T1: module persists an unclaimed deadline with defaults and the injected start time", () => {
  const b = box();
  const deadline: Deadline = startDeadline(b.root, { minutes: 10 }, b.env.now());
  expect(deadline).toEqual({ id: expect.stringMatching(/^D-[0-9a-f]{8}$/), start: b.env.now().toISOString(),
    minutes: 10, run: null, marks: [50, 80, 100], session: null });
  expect(JSON.parse(fs.readFileSync(path.join(b.root, `.harness-guard/deadlines/${deadline.id}.json`), "utf8")))
    .toEqual(deadline);
});

test("T1: marks ascend, 100 is added, and run is root-relative", () => {
  const b = box();
  const deadline = startDeadline(b.root, { minutes: 2.5, run: path.join(b.root, "runs/task"), marks: [80, 25] }, b.env.now());
  expect(deadline).toMatchObject({ minutes: 2.5, run: "runs/task", marks: [25, 80, 100], session: null });
});

test("T1: CLI start prints its id and local deadline time and writes the requested settings", () => {
  const b = box();
  const result = b.cli("deadline", "start", "--minutes", "10", "--run", "runs/task", "--marks", "80,50");
  expect(result.status).toBe(0);
  const [file] = fs.readdirSync(path.join(b.root, ".harness-guard/deadlines"));
  const deadline: Deadline = JSON.parse(fs.readFileSync(path.join(b.root, ".harness-guard/deadlines", file!), "utf8"));
  expect(deadline).toMatchObject({ minutes: 10, run: "runs/task", marks: [50, 80, 100], session: null });
  expect(result.stdout).toContain(deadline.id);
  const end = new Date(Date.parse(deadline.start) + deadline.minutes * 60_000);
  expect(result.stdout).toContain(`${String(end.getHours()).padStart(2, "0")}:${String(end.getMinutes()).padStart(2, "0")}`);
});

test("T1: the start Bash hook claims every unclaimed file for its session, leaving owned files alone", () => {
  const b = box();
  const first = b.plant({ session: null });
  const second = b.plant({ id: "D-00000002", session: null });
  const owned = b.plant({ id: "D-00000003", session: "other" });
  claim(b);
  for (const deadline of [first, second, owned]) {
    const stored = JSON.parse(fs.readFileSync(path.join(b.root, `.harness-guard/deadlines/${deadline.id}.json`), "utf8"));
    expect(stored.session).toBe(deadline === owned ? "other" : "s");
  }
});

test("T1: an unrelated Bash call does not claim unclaimed deadlines", () => {
  const b = box();
  const deadline = b.plant({ session: null });
  b.post();
  const stored = JSON.parse(fs.readFileSync(path.join(b.root, `.harness-guard/deadlines/${deadline.id}.json`), "utf8"));
  expect(stored.session).toBeNull();
});

test("T2: deadlineStatus uses the supplied time and ignores another session's deadline", () => {
  const b = box();
  b.plant();
  const before = deadlineStatus(b.root, "s", b.env.now());
  expect(before).not.toBeNull();
  expect(before).not.toBeUndefined();
  b.plant({ id: "D-00000002", session: "other", minutes: 100 });
  expect(deadlineStatus(b.root, "s", b.env.now())).toEqual(before);
  b.at(11);
  expect(deadlineStatus(b.root, "s", b.env.now())).not.toEqual(before);
});

test("T2: newest unexpired deadline wins; the latest wins when all have expired", () => {
  const b = box();
  const old = b.plant({ start: new Date(EPOCH - 60_000).toISOString(), minutes: 20 });
  const newer = b.plant({ id: "D-00000002", minutes: 10 });
  const onlyNewer = box();
  onlyNewer.save(newer);
  expect(deadlineStatus(b.root, "s", b.env.now())).toEqual(deadlineStatus(onlyNewer.root, "s", b.env.now()));
  // At minute 11, the older long deadline is still active and the newer one is expired.
  b.at(11);
  const onlyOld = box();
  onlyOld.save(old);
  expect(deadlineStatus(b.root, "s", b.env.now())).toEqual(deadlineStatus(onlyOld.root, "s", b.env.now()));
  b.at(30);
  expect(deadlineStatus(b.root, "s", b.env.now())).toEqual(deadlineStatus(onlyNewer.root, "s", b.env.now()));
});

test("T2: CLI status has exit 2 when no deadline belongs to the selected session", () => {
  const b = box();
  expect(b.cli("deadline", "status", "--session", "s").status).toBe(2);
  b.plant({ session: "other" });
  expect(b.cli("deadline", "status", "--session", "s").status).toBe(2);
});

test("T2 Fails-if: CLI status says time remains after expiry", () => {
  const b = box();
  b.plant({ start: "2000-01-01T00:00:00.000Z" });
  const expired = b.cli("deadline", "status", "--session", "s");
  expect(expired.status).toBe(1);
  expect(expired.stdout).toMatch(/time is up, .* min over/);
});

test("T2: live CLI status shows used, percent, left and local deadline", () => {
  const b = box();
  // A wide interval keeps this CLI test independent of execution time without sleeping.
  b.plant({ start: "2000-01-01T00:00:00.000Z", minutes: 100_000_000 });
  const live = b.cli("deadline", "status", "--session", "s");
  expect(live.status).toBe(0);
  expect(live.stdout).toMatch(/used .* of 100000000 min \(.*%\), .* left, deadline \d{2}:\d{2}/);
});

test("T3 Fails-if: CLI wait returns before the deadline", () => {
  const b = box();
  const env = { now: () => new Date() };
  const started = env.now();
  const deadline = b.plant({ start: started.toISOString(), minutes: 0.05 });
  const result = b.cli("deadline", "wait");
  expect(result.error).toBeUndefined();
  expect(result.status).toBe(0);
  expect(env.now().getTime()).toBeGreaterThanOrEqual(Date.parse(deadline.start) + deadline.minutes * 60_000);
  // COO, review finding 10: the default wait ends at the deadline, so its status says the time is up.
  expect(result.stdout).toMatch(/time is up/);
}, 10_000);

test("T4: progress counts distinct pieces by their latest state and derives age from the injected clock", () => {
  const b = box();
  const file = progress(b, "worker", line(0, "A", "planned") + line(0, "B", "planned") + line(0, "C", "planned")
    + line(1, "A", "start") + line(2, "A", "done") + line(3, "B", "fail"));
  b.at(5);
  const summary: ProgressSummary = progressSummary(file, b.env.now());
  expect(summary).toEqual({ node: "worker", done: 1, total: 3,
    last: { time: new Date(EPOCH + 3 * 60_000).toISOString(), piece: "B", state: "fail" }, ageMinutes: 2, badLines: 0 });
});

test("T4: repeated done events do not inflate the count, and a restarted piece is no longer done", () => {
  const b = box();
  const file = progress(b, "worker", line(0, "A", "done") + line(1, "A", "done") + line(2, "B", "done") + line(3, "A", "start"));
  b.at(4);
  expect(progressSummary(file, b.env.now())).toMatchObject({ done: 1, total: 2, last: { piece: "A", state: "start" } });
});

test("T4 Fails-if: malformed progress breaks parsing or is not counted", () => {
  const b = box();
  const file = progress(b, "worker", "not a progress line\n" + line(0, "A", "planned")
    + "- not-a-date · X · done · bad date\n" + line(1, "X", "unknown") + line(2, "A", "done"));
  b.at(4);
  expect(progressSummary(file, b.env.now())).toEqual({ node: "worker", done: 1, total: 1, badLines: 3,
    last: { time: new Date(EPOCH + 2 * 60_000).toISOString(), piece: "A", state: "done" }, ageMinutes: 2 });
});

test("T4: an empty progress file has no last event or age", () => {
  const b = box();
  expect(progressSummary(progress(b, "empty", ""), b.env.now())).toEqual({ node: "empty", done: 0, total: 0,
    last: null, ageMinutes: null, badLines: 0 });
});

test("T4 Fails-if: status crashes on malformed progress or prints raw progress text", () => {
  const b = box();
  const secret = "RAW_STDOUT_MUST_STAY_PRIVATE";
  progress(b, "worker", `stdout: ${secret}\n` + line(1, "A", "done", `piece complete; stdout: ${secret}`) + `prompt: ${secret}\n`);
  b.plant({ run: "runs/task", start: "2000-01-01T00:00:00.000Z" });
  const result = b.cli("deadline", "status", "--session", "s");
  expect(result.status).toBe(1);
  expect(result.stdout).toMatch(/worker: 1\/1 pieces, last A done .* min ago/);
  expect(result.stdout + result.stderr).not.toContain(secret);
  expect(result.stdout).not.toContain("stdout:");
});

for (const event of ["PostToolUse", "PostToolUseFailure"]) {
  test(`T5 Fails-if: ${event} misses a passed mark or announces it twice`, () => {
    const b = box();
    const deadline = b.plant();
    const payload = event === "PostToolUseFailure"
      ? { hook_event_name: event, tool_input: { command: "grep needle absent" }, exit_code: 1, error: "exit 1" }
      : { hook_event_name: event };
    b.at(4.9);
    expect(context(b.post(payload))).not.toContain("harness-guard time:");
    for (const [minutes, mark] of [[5.1, 50], [8.1, 80]] as const) {
      b.at(minutes);
      const text = context(b.post(payload));
      expect(text).toContain("harness-guard time:");
      expect(b.raised(`deadline:${deadline.id}:${mark}`)).toHaveLength(1);
      expect(context(b.post(payload))).not.toContain("harness-guard time:");
      expect(b.raised(`deadline:${deadline.id}:${mark}`)).toHaveLength(1);
    }
  });

  test(`T5 Fails-if: ${event} fails to say time is up on every call after expiry`, () => {
    const b = box();
    const deadline = b.plant();
    b.at(11);
    for (let i = 0; i < 2; i++) {
      const text = context(b.post({ hook_event_name: event, ...(event === "PostToolUseFailure" ? { exit_code: 1, error: "exit 1" } : {}) }));
      expect(text).toContain("harness-guard time is up");
      expect(text).toContain("stop trying, finish the report, and put what is open to the owner.");
    }
    expect(b.raised(`deadline:${deadline.id}:100`)).toHaveLength(1);
  });
}

test("T5: mark reminder follows the specified time context format", () => {
  const b = box();
  b.plant();
  b.at(6);
  expect(context(b.post())).toMatch(/harness-guard time: .* of 10 min used \(.*%\), .* left — deadline \d{2}:\d{2}/);
});

test("T5: expired reminder follows the specified time-up format", () => {
  const b = box();
  b.plant();
  b.at(11);
  expect(context(b.post())).toMatch(/harness-guard time is up \(.* min over\): stop trying, finish the report, and put what is open to the owner\./);
});

test("T5: the injected clock reaches time-up exactly at the deadline", () => {
  const b = box();
  b.plant();
  b.at(10);
  expect(context(b.post())).toContain("harness-guard time is up");
});

test("T5: crossing multiple marks between calls records each mark exactly once", () => {
  const b = box();
  const deadline = b.plant();
  b.at(9);
  expect(context(b.post())).toContain("harness-guard time:");
  for (const mark of [50, 80]) expect(b.raised(`deadline:${deadline.id}:${mark}`)).toHaveLength(1);
  expect(context(b.post())).not.toContain("harness-guard time:");
});

test("T5 Fails-if: an expired deadline from another session reminds this one", () => {
  const b = box();
  const deadline = b.plant({ session: "other" });
  b.at(11);
  expect(context(b.post())).not.toContain("harness-guard time");
  expect(b.raised(`deadline:${deadline.id}:100`)).toEqual([]);
  expect(context(b.post({}, "other"))).toContain("harness-guard time is up");
});

test("T5: reminders show no more than five workers and never echo raw progress text", () => {
  const b = box();
  const secret = "RAW_PROMPT_MUST_STAY_PRIVATE";
  for (let i = 0; i < 7; i++) progress(b, `worker-${i}`, `${secret}\n` + line(1, "A", "done", `finished piece; prompt: ${secret}`));
  b.plant({ run: "runs/task" });
  b.at(6);
  const text = context(b.post());
  expect(text.match(/worker-\d: 1\/1 pieces, last A done 5(?:\.0)? min ago/g)).toHaveLength(5);
  expect(text).not.toContain(secret);
});

test("T5: timer context joins the warning context produced by the same hook", () => {
  const b = box();
  b.plant();
  b.at(6);
  const text = context(b.post({ hook_event_name: "PostToolUseFailure", tool_input: { command: "grep needle absent" },
    exit_code: 1, error: "exit 1" }));
  expect(text).toMatch(/harness-guard warning W-[0-9a-f]{8}/);
  expect(text).toContain("harness-guard time:");
});

test("T6 Fails-if: ask-the-time repeats; the first ask joins the K2 criteria reminder", () => {
  const b = box();
  const first = context(b.prompt());
  expect(first).toContain("harness-guard: ask the owner how much time you have to try (unless they said), then record it:");
  expect(first).toContain("deadline start --minutes N --run runs/<run>");
  expect(first).toContain("before you start, write the criteria this request will be scored on");
  expect(b.raised("deadline-ask")).toHaveLength(1);
  expect(b.raised("criteria")).toHaveLength(1);
  expect(context(b.prompt())).not.toContain("ask the owner how much time");
  expect(b.raised("deadline-ask")).toHaveLength(1);
  expect(context(b.prompt("other"))).toContain("ask the owner how much time");
  expect(b.raised("deadline-ask", "other")).toHaveLength(1);
});

test("T6: owning a deadline suppresses the time ask, while another session's deadline does not", () => {
  const b = box();
  b.plant();
  expect(context(b.prompt())).not.toContain("ask the owner how much time");
  expect(b.raised("deadline-ask")).toEqual([]);
  expect(context(b.prompt("other"))).toContain("ask the owner how much time");
});

// COO, Round 10 correction: between marks every call still carries the time (research F1, F3, F6).
test("between marks, every call adds a one-line clock", () => {
  const b = box();
  b.plant();
  b.at(2);
  const first = context(b.post({ hook_event_name: "PostToolUse" }));
  expect(first).toMatch(/^harness-guard clock: 2\/10 min \(20%\), 8 left$/);
  b.at(3);
  expect(context(b.post({ hook_event_name: "PostToolUse" }))).toMatch(/^harness-guard clock: 3\/10 min/);
});

// COO, after the Codex review of round 10 (runs/20261016-time-monitor/nodes/review.result.md).
test("review 2: a command that only mentions deadline start, or failed, claims nothing", () => {
  const b = box();
  b.plant({ session: null });
  b.post({ hook_event_name: "PostToolUse", tool_name: "Bash", tool_input: { command: 'echo "deadline start"' },
    tool_response: { stdout: "", stderr: "", interrupted: false } }, "other");
  b.post({ hook_event_name: "PostToolUseFailure", tool_name: "Bash", tool_input: { command: "bun x/src/cli.ts deadline start --minutes 5" },
    exit_code: 2, error: "x" }, "other");
  expect(JSON.parse(fs.readFileSync(path.join(b.root, ".harness-guard/deadlines/D-00000001.json"), "utf8")).session).toBeNull();
  b.post({ hook_event_name: "PostToolUse", tool_name: "Bash", tool_input: { command: "bun x/src/cli.ts deadline start --minutes 5" },
    tool_response: { stdout: "", stderr: "", interrupted: false } }, "s");
  expect(JSON.parse(fs.readFileSync(path.join(b.root, ".harness-guard/deadlines/D-00000001.json"), "utf8")).session).toBe("s");
});

test("review 4: the 100% block carries the workers once, then time-up alone", () => {
  const b = box();
  b.plant({ run: "runs/task" });
  b.write("runs/task/nodes/w.progress.md", "- 2026-01-01T00:00:00Z · P1 · done · ok\n");
  b.at(10);
  const first = context(b.post({ hook_event_name: "PostToolUse" }));
  expect(first).toContain("(100%)");
  expect(first).toContain("w: 1/1 pieces");
  expect(first).toContain("harness-guard time is up (0 min over)");
  const second = context(b.post({ hook_event_name: "PostToolUse" }));
  expect(second).not.toContain("w: 1/1 pieces");
  expect(second).toContain("harness-guard time is up");
});

test("review 5: a deadline file whose id is not D-xxxxxxxx, or not its file name, is no deadline", () => {
  const b = box();
  b.write(".harness-guard/deadlines/bad.json", JSON.stringify({ id: "../unexpected", start: new Date(0).toISOString(), minutes: 5, run: null, marks: [100], session: null }));
  b.write(".harness-guard/deadlines/D-00000002.json", JSON.stringify({ id: "D-00000003", start: new Date(0).toISOString(), minutes: 5, run: null, marks: [100], session: "s" }));
  b.post({ hook_event_name: "PostToolUse", tool_name: "Bash", tool_input: { command: "bun x/src/cli.ts deadline start --minutes 5" },
    tool_response: { stdout: "", stderr: "", interrupted: false } });
  expect(fs.existsSync(path.join(b.root, ".harness-guard/unexpected.json"))).toBe(false);
  expect(deadlineStatus(b.root, "s", new Date(0))).toBeNull();
});

test("review 6: minutes too large to be a time are refused", () => {
  const b = box();
  expect(() => startDeadline(b.root, { minutes: 1e308 }, new Date())).toThrow();
  expect(b.cli("deadline", "start", "--minutes", "1e308").status).toBe(2);
});

test("review 7: a fractional budget at its exact end is 0 min over", () => {
  const b = box();
  b.plant({ minutes: 2.5 });
  b.at(2.5);
  expect(context(b.post({ hook_event_name: "PostToolUse" }))).toContain("time is up (0 min over)");
});

// COO: a task that finishes early ends its deadline, so the clock does not run into the next task.
test("deadline end stops the clock and the time-up line", () => {
  const b = box();
  b.plant();
  b.at(2);
  expect(context(b.post({ hook_event_name: "PostToolUse" }))).toContain("harness-guard clock:");
  endDeadline(b.root, "s", new Date(EPOCH + 2 * 60_000));
  b.at(3);
  expect(context(b.post({ hook_event_name: "PostToolUse" }))).toBe("");
  b.at(20);
  expect(context(b.post({ hook_event_name: "PostToolUse" }))).toBe("");
  expect(deadlineStatus(b.root, "s", new Date(EPOCH + 20 * 60_000))).toBeNull();
});
