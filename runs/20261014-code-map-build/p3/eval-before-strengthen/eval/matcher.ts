import { isDeepStrictEqual } from "node:util";

export type LocationExpectation = { path: string; file: string; line: number };
export type Expectation = {
  includes: LocationExpectation[];
  excludes: LocationExpectation[];
  equals: { path: string; value: unknown }[];
  ambiguous: boolean | null;
  limitReasons: string[];
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

export function matchAnswer(answer: unknown, expect: Expectation): Mismatch[] {
  const failures: Mismatch[] = [];
  for (const text of expect.textIncludes ?? []) {
    if (typeof answer !== "string" || !answer.includes(text)) failures.push({ path: "$stdout", expected: text, actual: answer, message: "text evidence missing" });
  }
  for (const [rule, checks] of [["includes", expect.includes], ["excludes", expect.excludes]] as const) {
    for (const check of checks) {
      const actual = selectPath(answer, check.path);
      const found = actual.some(value => isObject(value) && value.file === check.file && value.line === check.line);
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
  return failures;
}
