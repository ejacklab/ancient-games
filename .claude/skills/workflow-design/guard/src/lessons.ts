// Round 18: agent lessons and project facts — reading them, checking them, and choosing the ones that match a call.

import { createHash } from "node:crypto";
import * as fs from "node:fs";
import * as path from "node:path";

export const AGENTS = ["all", "claude-main", "opencode", "codex", "agy", "mcode", "dsh"] as const;
export const KINDS = ["test", "code-edit", "engine-call", "brief", "command"] as const;

// The store beside the guard: .claude/skills/agent-lessons/lessons (L4).
export const DEFAULT_STORE = path.resolve(import.meta.dirname, "../../../agent-lessons/lessons");

export interface Lesson {
  slug: string;
  agents: string[];
  kinds: string[];
  paths: string[];
  commands: string[];
  from: string;
  enforcedBy: string;
  text: string;
}

export interface ProjectFact {
  file: string; // absolute path of the file the fact is about
  fact: string;
}

export interface Query {
  agent: string;
  kinds?: string[];
  paths?: string[]; // absolute, or relative to root
  commands?: string[];
  root: string; // the git root the paths are matched from
}

const SLUG = /^[a-z0-9][a-z0-9-]*$/;

function stringList(value: unknown): string[] | null {
  if (value === undefined || value === null) return [];
  if (!Array.isArray(value) || !value.every((item) => typeof item === "string" && item.trim() !== "")) return null;
  return value.map((item) => item.trim());
}

// One lesson file, or the reason it is not one (L1).
export function parseLesson(file: string): Lesson | { file: string; reason: string } {
  const slug = path.basename(file, ".md");
  const bad = (reason: string) => ({ file, reason });
  if (!SLUG.test(slug)) return bad("the file name is not a slug (lower-case letters, digits and dashes)");
  let text: string;
  try {
    text = fs.readFileSync(file, "utf8");
  } catch {
    return bad("unreadable");
  }
  // The closing --- stands on its own line (crossed review finding 5: "---body" is not a delimiter).
  const match = /^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n([\s\S]*))?$/.exec(text);
  if (match === null) return bad("no front matter between two --- lines");
  let front: unknown;
  try {
    front = Bun.YAML.parse(match[1]!);
  } catch {
    return bad("the front matter is not YAML");
  }
  if (typeof front !== "object" || front === null || Array.isArray(front)) return bad("the front matter is not a mapping");
  const fields = front as Record<string, unknown>;
  const agents = stringList(fields.agents);
  if (agents === null || agents.length === 0) return bad("agents: a non-empty list");
  const unknownAgent = agents.find((agent) => !(AGENTS as readonly string[]).includes(agent));
  if (unknownAgent !== undefined) return bad(`agents: unknown agent ${unknownAgent}`);
  const kinds = stringList(fields.kinds);
  if (kinds === null || kinds.length === 0) return bad("kinds: a non-empty list");
  const unknownKind = kinds.find((kind) => !(KINDS as readonly string[]).includes(kind));
  if (unknownKind !== undefined) return bad(`kinds: unknown kind ${unknownKind}`);
  const paths = stringList(fields.paths);
  if (paths === null) return bad("paths: a list of globs");
  const commands = stringList(fields.commands);
  if (commands === null) return bad("commands: a list of command words");
  if (typeof fields.from !== "string" || fields.from.trim() === "") return bad("from: the insight or memory it came from");
  const enforcedBy = fields.enforced_by === undefined || fields.enforced_by === null ? "" : fields.enforced_by;
  if (typeof enforcedBy !== "string") return bad("enforced_by: a check or test, as text");
  const body = (match[2] ?? "").trim();
  if (body === "") return bad("no lesson text after the front matter");
  return { slug, agents, kinds, paths, commands, from: fields.from.trim(), enforcedBy: enforcedBy.trim(), text: body };
}

function lessonFiles(store: string): string[] {
  try {
    return fs.readdirSync(store).filter((name) => name.endsWith(".md")).sort().map((name) => path.join(store, name));
  } catch {
    return [];
  }
}

// Every valid lesson in the store; an invalid file is skipped (L1).
export function readLessons(store: string): Lesson[] {
  return lessonFiles(store).map(parseLesson).filter((entry): entry is Lesson => "slug" in entry);
}

// Every invalid lesson file and why (`lessons check`).
export function checkLessons(store: string): { file: string; reason: string }[] {
  return lessonFiles(store).map(parseLesson).filter((entry): entry is { file: string; reason: string } => !("slug" in entry));
}

const FACT = /^- `([^`/]+)` — (.+)$/;

// The project facts about one file: the lines of the LESSONS.md in its folder that name it (L2).
export function factsFor(file: string): ProjectFact[] {
  const folder = path.dirname(file);
  let text: string;
  try {
    text = fs.readFileSync(path.join(folder, "LESSONS.md"), "utf8");
  } catch {
    return [];
  }
  const name = path.basename(file);
  return text.split("\n").flatMap((line) => {
    const match = FACT.exec(line.trim());
    return match !== null && match[1] === name ? [{ file, fact: match[2]!.trim() }] : [];
  });
}

// A test file: a path segment test or tests, or a name with .test. or _test., or one starting test_ (L3).
export function isTestFile(file: string): boolean {
  const parts = file.split(/[\\/]/);
  const name = parts[parts.length - 1] ?? "";
  return parts.slice(0, -1).some((part) => part === "test" || part === "tests")
    || name.includes(".test.") || name.includes("_test.") || name.startsWith("test_");
}

function relativeTo(root: string, file: string): string {
  const absolute = path.resolve(root, file);
  const relative = path.relative(root, absolute);
  // Outside the root only when the first segment is "..", not a name that starts with it (crossed review finding 4).
  const outside = relative === ".." || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative);
  return outside ? absolute : relative.split(path.sep).join("/");
}

// Whether one lesson matches the query (L3).
export function matches(lesson: Lesson, query: Query): boolean {
  if (!lesson.agents.includes("all") && !lesson.agents.includes(query.agent)) return false;
  const files = (query.paths ?? []).map((file) => relativeTo(query.root, file));
  for (const file of files) {
    if (lesson.paths.some((glob) => new Bun.Glob(glob).match(file))) return true;
    if (lesson.kinds.includes(isTestFile(file) ? "test" : "code-edit")) return true;
  }
  if ((query.commands ?? []).some((word) => lesson.commands.includes(word))) return true;
  return (query.kinds ?? []).some((kind) => lesson.kinds.includes(kind));
}

// The line a lesson is given as: its text, or its pointer once a check enforces it (L3).
export function lessonLine(lesson: Lesson): string {
  return lesson.enforcedBy === "" ? `- ${lesson.text.replace(/\s+/g, " ")} (${lesson.slug})` : `- ${lesson.slug}: enforced by ${lesson.enforcedBy}`;
}

export function factLine(root: string, fact: ProjectFact): string {
  return `- ${relativeTo(root, fact.file)}: ${fact.fact}`;
}

// The matching lessons, then the project facts of the paths given (L4).
export function lessonsFor(store: string, query: Query): { lessons: Lesson[]; facts: ProjectFact[] } {
  const lessons = readLessons(store).filter((lesson) => matches(lesson, query));
  const facts = (query.paths ?? []).flatMap((file) => factsFor(path.resolve(query.root, file)));
  return { lessons, facts };
}

// ---- once per session (L5) ---------------------------------------------------------------------------------------

// One marker file per shown key, created only if absent: two hooks at once cannot lose a mark, and a mark that cannot
// be written means the key is not given — a hold the retry would meet again is worse than no hold (crossed review
// findings 2 and 3). `.harness-guard/lessons-shown/<hash of session>/<hash of key>`, the key as the file's text.
function hash(text: string): string {
  return createHash("sha256").update(text).digest("hex").slice(0, 16);
}

export function shownFolder(root: string, session: string): string {
  return path.join(root, ".harness-guard", "lessons-shown", hash(session));
}

// The keys not yet shown in this session (and agent); marks them shown before it returns.
export function takeUnshown(root: string, session: string, keys: string[]): string[] {
  const unique = [...new Set(keys)];
  if (unique.length === 0) return [];
  const folder = shownFolder(root, session);
  try {
    fs.mkdirSync(folder, { recursive: true });
  } catch {
    return [];
  }
  return unique.filter((key) => {
    try {
      fs.writeFileSync(path.join(folder, hash(key)), `${key}\n`, { flag: "wx" });
      return true;
    } catch {
      return false; // shown already (EEXIST), or the mark cannot be written: either way, not given now
    }
  });
}
