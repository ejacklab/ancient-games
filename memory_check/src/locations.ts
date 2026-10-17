// F1: the memory locations the guidelines name, each reported present or absent. No file inside a location is
// read to decide it: the tool asks the file system whether it is there, and nothing else.
import { existsSync, readdirSync, statSync } from "node:fs";
import path from "node:path";

export interface Location {
  /** The name the guideline uses for it: `AGENTS.md`, `project-memory/entries/`, `agent memory`. */
  readonly name: string;
  /** Absolute path, as given to the file system. */
  readonly path: string;
  readonly present: boolean;
  /** For a folder: how many direct children it holds (a name is never read). */
  readonly children: number | null;
}

export const AGENTS_MD = "AGENTS.md";

const IN_PROJECT: readonly { name: string; path: string }[] = [
  { name: "AGENTS.md", path: "AGENTS.md" },
  { name: "CLAUDE.md", path: "CLAUDE.md" },
  { name: "project-memory/INDEX.md", path: "project-memory/INDEX.md" },
  { name: "project-memory/entries/", path: "project-memory/entries" },
  { name: "project-memory/work/", path: "project-memory/work" },
  { name: "project-memory/journal/", path: "project-memory/journal" },
  { name: "project-memory/.cache/", path: "project-memory/.cache" },
];

export const PROJECT_LOCATIONS = IN_PROJECT;

function isFolder(full: string): boolean {
  try {
    return statSync(full).isDirectory();
  } catch {
    return false;
  }
}

function childrenCount(full: string): number | null {
  if (!isFolder(full)) return null;
  try {
    return readdirSync(full).length;
  } catch {
    return null;
  }
}

/**
 * The agent memory the design places in the home folder (`docs/memory-system/SOURCE_OF_TRUTH.md`, What it is
 * for): one folder per agent name. The tool cannot know which agents work on the project, so it reports the
 * names it finds, and absent when there is no such folder.
 */
function agentMemory(home: string): Location[] {
  const folder = path.join(home, ".claude", "agent-memory");
  const absent: Location = {
    name: "agent memory (<home>/.claude/agent-memory/<name>/)",
    path: folder,
    present: false,
    children: null,
  };
  if (!isFolder(folder)) return [absent];
  let names: string[] = [];
  try {
    names = readdirSync(folder).sort();
  } catch {
    return [absent];
  }
  if (names.length === 0) return [absent];
  return names.map((name) => {
    const full = path.join(folder, name);
    return { name: `agent memory ${name}/`, path: full, present: existsSync(full), children: childrenCount(full) };
  });
}

export function findLocations(root: string, home: string): Location[] {
  const inProject: Location[] = IN_PROJECT.map((location) => {
    const full = path.join(root, location.path);
    return { name: location.name, path: full, present: existsSync(full), children: childrenCount(full) };
  });
  return [...inProject, ...agentMemory(home)];
}

export function agentsMdMissing(root: string): boolean {
  return !existsSync(path.join(root, AGENTS_MD));
}