import { isDeepStrictEqual } from "node:util";

export type LocationExpectation = { path: string; file: string; line: number };
export type Expectation = {
  includes: LocationExpectation[];
  excludes: LocationExpectation[];
  equals: { path: string; value: unknown }[];
  shapes?: { path: string; value: unknown }[];
  ambiguous: boolean | null;
  limitReasons: string[];
  exactLimitReasons?: string[];
  textIncludes?: string[];
};
export type Mismatch = { path: string; expected: unknown; actual: unknown; message: string };

export function isObject(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function descendants(value: unknown): unknown[] {
  if (!isObject(value) || !Array.isArray(value.children)) return [];
  return value.children.flatMap(child => [child, ...descendants(child)]);
}

/** Missing values stay absent; [] collects values, and children searches descendants. */
export function selectPath(value: unknown, path: string): unknown[] {
  let values: unknown[] = [value];
  for (const segment of path.split(".")) {
    const match = /^([A-Za-z_$][\w$]*)(\[\])?$/.exec(segment);
    if (!match) throw new Error(`Invalid expectation path: ${path}`);
    const key = match[1]!;
    const array = Boolean(match[2]);
    values = values.flatMap(parent => {
      if (key === "children") return descendants(parent);
      if (!isObject(parent) || !Object.hasOwn(parent, key)) return [];
      const child = parent[key];
      return array ? (Array.isArray(child) ? child : []) : [child];
    });
  }
  return values;
}

export function collectLimitReasons(value: unknown): string[] {
  if (Array.isArray(value)) return value.flatMap(collectLimitReasons);
  if (!isObject(value)) return [];
  const reasons: string[] = [];
  if (Array.isArray(value.limits)) {
    for (const limit of value.limits) {
      if (isObject(limit) && typeof limit.reason === "string") reasons.push(limit.reason);
    }
  }
  if (isObject(value.stop) && typeof value.stop.reason === "string") reasons.push(value.stop.reason);
  for (const [key, child] of Object.entries(value)) {
    if (key !== "limits" && key !== "stop") reasons.push(...collectLimitReasons(child));
  }
  return reasons;
}

/** Objects pin only written fields; arrays require a one-to-one match, in any order. */
function matchesShape(actual: unknown, expected: unknown): boolean {
  if (Array.isArray(expected)) {
    if (!Array.isArray(actual) || actual.length !== expected.length) return false;
    const items = actual;
    const compatible = expected.map(item => items.map(value => matchesShape(value, item)));
    const owners = new Map<number, number>();
    function assign(index: number, visited: Set<number>): boolean {
      for (let candidate = 0; candidate < items.length; candidate++) {
        if (!compatible[index]![candidate] || visited.has(candidate)) continue;
        visited.add(candidate);
        const owner = owners.get(candidate);
        if (owner === undefined || assign(owner, visited)) {
          owners.set(candidate, index); return true;
        }
      }
      return false;
    }
    return expected.every((_, index) => assign(index, new Set()));
  }
  if (isObject(expected)) return isObject(actual) && Object.entries(expected).every(([key, value]) =>
    Object.hasOwn(actual, key) && matchesShape(actual[key], value));
  return isDeepStrictEqual(actual, expected);
}

export function matchAnswer(answer: unknown, expect: Expectation): Mismatch[] {
  const failures: Mismatch[] = [];
  for (const text of expect.textIncludes ?? []) {
    if (typeof answer !== "string" || !answer.includes(text)) failures.push({ path: "$stdout", expected: text, actual: answer, message: "text evidence missing" });
  }
  for (const [rule, checks] of [["includes", expect.includes], ["excludes", expect.excludes]] as const) {
    for (const check of checks) {
      const actual = typeof answer === "string" ? answer : selectPath(answer, check.path);
      const place = `${check.file}:${check.line}`.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      const found = typeof actual === "string"
        ? new RegExp(`(^|[^\\w./\\\\-])${place}(?=$|[^0-9])`).test(actual)
        : actual.some(value => isObject(value) && value.file === check.file && value.line === check.line);
      if (found !== (rule === "includes")) failures.push({
        path: check.path, expected: { [rule]: { file: check.file, line: check.line } },
        actual, message: `${rule} location check failed`,
      });
    }
  }
  for (const check of expect.equals) {
    const selected = selectPath(answer, check.path);
    const actual = check.path.includes("[]") || check.path.split(".").includes("children") ? selected : selected[0];
    if (!isDeepStrictEqual(actual, check.value)) failures.push({
      path: check.path, expected: check.value, actual: actual === undefined ? { missing: true } : actual,
      message: "equals check failed",
    });
  }
  for (const check of expect.shapes ?? []) {
    const selected = selectPath(answer, check.path);
    const actual = check.path.includes("[]") || check.path.split(".").includes("children") ? selected : selected[0];
    if (!matchesShape(actual, check.value)) failures.push({
      path: check.path, expected: check.value, actual: actual === undefined ? { missing: true } : actual,
      message: "shape check failed",
    });
  }
  if (expect.ambiguous !== null) {
    const actual = isObject(answer) ? answer.ambiguous : undefined;
    if (actual !== expect.ambiguous) failures.push({ path: "ambiguous", expected: expect.ambiguous,
      actual: actual ?? { missing: true }, message: "ambiguous check failed" });
  }
  const reasons = collectLimitReasons(answer);
  for (const reason of expect.limitReasons) {
    if (!reasons.includes(reason)) failures.push({ path: "limits/stop", expected: reason, actual: reasons,
      message: "limit reason missing" });
  }
  if (expect.exactLimitReasons !== undefined &&
      !isDeepStrictEqual([...new Set(reasons)].sort(), [...new Set(expect.exactLimitReasons)].sort())) {
    failures.push({ path: "limits/stop", expected: expect.exactLimitReasons, actual: reasons,
      message: "exact limit reasons check failed" });
  }
  return failures;
}
