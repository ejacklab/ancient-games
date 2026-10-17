import { isObject, type Mismatch } from "./matcher.ts";
import { samePlace, sourceEvidence } from "./source.ts";

const nodeKinds = ["function", "method", "arrow", "effect-fn", "property", "class", "variable", "interface-member", "other"];
const limitKinds = ["depth", "dynamic", "outside-repo", "other-process", "not-found", "seen", "other"];
const stepKinds = ["call", "if", "else", "loop", "try", "catch", "return", "yield*"];

export function validateAnswer(answer: unknown, args: string[], testPatterns: string[], root?: string): Mismatch[] {
  const failures: Mismatch[] = [];
  const source = root ? sourceEvidence(root) : undefined;
  const fail = (path: string, expected: unknown, actual: unknown) => failures.push({ path, expected,
    actual: actual === undefined ? { missing: true } : actual, message: "JSON contract violated" });
  function location(value: unknown, path: string): value is Record<string, unknown> {
    if (!isObject(value) || typeof value.file !== "string" || !value.file || value.file.startsWith("/") ||
        !Number.isInteger(value.line) || (value.line as number) < 1 ||
        (value.endLine !== undefined && (!Number.isInteger(value.endLine) || (value.endLine as number) < (value.line as number)))) {
      fail(path, "relative file and positive 1-based line (endLine >= line)", value); return false;
    }
    return true;
  }
  function node(value: unknown, path: string): value is Record<string, unknown> {
    if (!location(value, path)) return false;
    if (typeof value.name !== "string" || !value.name || !nodeKinds.includes(value.kind as string)) {
      fail(path, "named Node with a spec kind", value); return false;
    }
    return true;
  }
  function limit(value: unknown, path: string) {
    if (!isObject(value) || !limitKinds.includes(value.reason as string)) { fail(path, "Limit with stated reason", value); return; }
    if (value.at !== undefined) location(value.at, path + ".at");
    if (value.ref !== undefined) location(value.ref, path + ".ref");
    if (value.reason === "seen" && value.ref === undefined) fail(path, "seen limit with ref", value);
    if (value.reason === "other" && (typeof value.text !== "string" || !value.text.trim())) fail(path, "other limit with text", value);
  }
  function array(value: unknown, path: string, visit: (item: unknown, path: string) => void) {
    if (!Array.isArray(value)) { fail(path, "array", value); return; }
    value.forEach((item, index) => visit(item, `${path}[${index}]`));
  }
  function link(value: unknown, path: string) {
    if (!isObject(value)) { fail(path, "Link", value); return; }
    node(value.from, path + ".from"); location(value.site, path + ".site");
    if (!["call", "new", "service-call"].includes(value.kind as string)) fail(path + ".kind", "call | new | service-call", value.kind);
    if (!["definition", "implementation-lookup"].includes(value.via as string)) fail(path + ".via", "definition | implementation-lookup", value.via);
    if (value.declaration !== undefined) location(value.declaration, path + ".declaration");
    array(value.candidates, path + ".candidates", (candidate, at) => {
      if (!node(candidate, at)) return;
      const testFake = testPatterns.some(pattern => new Bun.Glob(pattern).match(candidate.file as string));
      if (candidate.testFake !== testFake) fail(at + ".testFake", testFake, candidate.testFake);
    });
    const real = Array.isArray(value.candidates) ? value.candidates.filter(candidate => isObject(candidate) && candidate.testFake === false) : [];
    const expectedResolution = real.length === 0 ? "unresolved" : real.length === 1 ? "implementation" : "ambiguous";
    if (value.resolution !== expectedResolution) fail(path + ".resolution", expectedResolution, value.resolution);
    if (value.resolution === "implementation") {
      if (node(value.to, path + ".to")) {
        const target = value.to;
        if (!real.some(candidate => candidate.file === target.file && candidate.line === target.line)) {
          fail(path + ".to", "the sole non-test candidate", value.to);
        }
        if (value.to.kind === "interface-member" || (value.via === "implementation-lookup" && isObject(value.declaration) &&
            value.to.file === value.declaration.file && value.to.line === value.declaration.line)) {
          fail(path + ".to", "an implementation, rather than its interface declaration", value.to);
        }
      }
    } else if (value.to !== undefined) fail(path + ".to", "absent for unresolved or ambiguous links", value.to);
    if (source && !source.isCallSite(value)) fail(path + ".site", "a call in the stated enclosing function on this source line", value.site);
    if (value.resolution === "unresolved" && (typeof value.reason !== "string" || !value.reason.trim())) fail(path + ".reason", "unresolved reason", value.reason);
  }
  function flowStep(value: unknown, path: string) {
    if (!isObject(value)) { fail(path, "Step", value); return; }
    location(value.at, path + ".at");
    if (!stepKinds.includes(value.kind as string)) fail(path + ".kind", stepKinds, value.kind);
    if (typeof value.text !== "string" || !value.text.trim()) fail(path + ".text", "full source text", value.text);
    if (source && !source.hasText(value.at, value.text)) fail(path + ".text", "source text at at (only trailing whitespace normalized)", value.text);
    if (value.children !== undefined) array(value.children, path + ".children", flowStep);
  }
  if (!isObject(answer)) { fail("$", "Answer object", answer); return failures; }
  const fields = ["command", "query", "ambiguous", "matches", "links", "chain", "tests", "map", "limits", "empty"];
  for (const key of Object.keys(answer)) if (!fields.includes(key)) fail(key, "specified Answer fields only", answer[key]);
  if (answer.command !== args[0]) fail("command", args[0], answer.command);
  array(answer.limits, "limits", limit);
  if (answer.query !== undefined && (!Array.isArray(answer.query) || !answer.query.every(query => typeof query === "string"))) fail("query", "string[]", answer.query);
  if (answer.empty !== undefined && answer.empty !== "none found by static analysis") fail("empty", "none found by static analysis", answer.empty);
  const allowedSections: Record<string, string[]> = {
    where: ["matches"], find: ["matches"], callers: ["matches", "links"], callees: ["matches", "links"],
    chain: ["matches", "chain"], tests: ["matches", "tests"], map: ["map"],
  };
  for (const section of ["matches", "links", "chain", "tests", "map"]) {
    if (answer[section] !== undefined && !allowedSections[args[0] ?? ""]?.includes(section)) fail(section, "section belonging to this command", answer[section]);
  }
  if (answer.matches !== undefined) {
    array(answer.matches, "matches", node);
    if (Array.isArray(answer.matches) && answer.ambiguous !== (answer.matches.length > 1)) fail("ambiguous", answer.matches.length > 1, answer.ambiguous);
    if (!["find", "where"].includes(args[0] ?? "") &&
        [answer.links, answer.chain, answer.tests].some(value => value !== undefined)) fail("matches", "candidate-only response, without answer sections", answer.matches);
    if (answer.ambiguous === true && args[0] !== "find" && args[0] !== "where" &&
        [answer.links, answer.chain, answer.tests, answer.map].some(value => value !== undefined)) fail("$", "ambiguous name: candidates only", answer);
  }
  if (answer.links !== undefined) array(answer.links, "links", link);
  if (answer.chain !== undefined) {
    if (!isObject(answer.chain)) fail("chain", "{up, down}", answer.chain);
    else for (const direction of ["up", "down"] as const) {
      const depthFlag = args.indexOf("--" + direction);
      const depth = depthFlag < 0 ? 6 : Number(args[depthFlag + 1]);
      const shown = new Set<string>();
      const rootMatch = /^(.*):(\d+)$/.exec(args[1] ?? "");
      if (rootMatch) shown.add(`${rootMatch[1]}:${rootMatch[2]}`);
      // A shared function may be serialized after a branch that references it.
      function registerShown(value: unknown, path: string) {
        if (!isObject(value)) return;
        const target = isObject(value.link) ? value.link[direction === "down" ? "to" : "from"] : undefined;
        if (isObject(target) && (!isObject(value.stop) || value.stop.reason !== "seen")) {
          const key = `${target.file}:${target.line}`;
          if (shown.has(key)) fail(path + ".stop", "seen with reference to the single shown function", value.stop);
          shown.add(key);
        }
        if (Array.isArray(value.children)) value.children.forEach((child, index) => registerShown(child, `${path}.children[${index}]`));
      }
      const steps = answer.chain[direction];
      if (Array.isArray(steps)) steps.forEach((step, index) => registerShown(step, `chain.${direction}[${index}]`));
      function chainStep(value: unknown, path: string, level: number, parent: unknown) {
        if (!isObject(value)) { fail(path, "ChainStep", value); return; }
        if (value.level !== level || level > depth) fail(path + ".level", `level ${level}, at most ${depth}`, value.level);
        link(value.link, path + ".link");
        const origin = isObject(value.link) ? value.link[direction === "down" ? "from" : "to"] : undefined;
        if (!samePlace(origin, parent)) fail(path + ".link", "link joined to the requested place or parent in " + direction + " direction", value.link);
        if (value.stop !== undefined) limit(value.stop, path + ".stop");
        const target = isObject(value.link) ? value.link[direction === "down" ? "to" : "from"] : undefined;
        if (isObject(target)) {
          const key = `${target.file}:${target.line}`;
          if (isObject(value.stop) && value.stop.reason === "seen" &&
              (!shown.has(key) || !isObject(value.stop.ref) || value.stop.ref.file !== target.file || value.stop.ref.line !== target.line)) {
            fail(path + ".stop", "seen with reference to a shown function", value.stop);
          }
        }
        if (Array.isArray(value.children) && value.children.length && value.stop !== undefined) fail(path + ".children", "no expansion after a stop", value.children);
        if (level === depth && value.stop === undefined) fail(path + ".stop", "depth stop", value.stop);
        array(value.children, path + ".children", (child, at) => chainStep(child, at, level + 1, target));
      }
      array(answer.chain[direction], `chain.${direction}`, (step, at) => chainStep(step, at, 1, rootMatch ? { file: rootMatch[1], line: Number(rootMatch[2]) } : undefined));
    }
  }
  if (answer.tests !== undefined) {
    if (args.includes("--file") && !args.includes("--per-function")) fail("tests", "absent without --per-function", answer.tests);
    if (!isObject(answer.tests)) fail("tests", "TestsAnswer", answer.tests);
    else {
      if (answer.tests.label !== "static-call-path") fail("tests.label", "static-call-path", answer.tests.label);
      if (!Array.isArray(answer.tests.tests) || answer.tests.count !== answer.tests.tests.length) fail("tests.count", Array.isArray(answer.tests.tests) ? answer.tests.tests.length : "tests.length", answer.tests.count);
      const testCase = (value: unknown, path: string) => {
        if (!location(value, path)) return;
        if (typeof value.name !== "string" || !value.name.trim()) fail(path + ".name", "test case name", value.name);
        if (!Array.isArray(value.path) || !value.path.length) fail(path + ".path", "nonempty evidence path", value.path);
        array(value.path, path + ".path", link);
        if (Array.isArray(value.path) && value.path.length) {
          const first = value.path[0]; const last = value.path.at(-1);
          if (!isObject(first) || !samePlace(first.from, value) || (source && !source.isTestStart(value, first))) fail(path + ".path", "first link starts in the named test body", first);
          const asked = /^(.*):(\d+)$/.exec(args[1] ?? "");
          const target = isObject(last) ? last.to : undefined;
          if (asked ? !samePlace(target, { file: asked[1], line: Number(asked[2]) }) :
              (!args.includes("--file") && (!isObject(target) || target.name !== args[1]))) fail(path + ".path", "last link ends at the asked function", target);
        }
        const throughFake = Array.isArray(value.path) && value.path.some(edge => isObject(edge) && edge.kind === "service-call" &&
          Array.isArray(edge.candidates) && edge.candidates.some(candidate => isObject(candidate) && candidate.testFake === true));
        if (value.throughFake !== throughFake) fail(path + ".throughFake", throughFake, value.throughFake);
        if (Array.isArray(value.path)) for (let index = 1; index < value.path.length; index++) {
          const previous = value.path[index - 1]; const next = value.path[index];
          if (!isObject(previous) || !isObject(next) || !samePlace(previous.to, next.from)) fail(path + ".path", "connected static call path", value.path);
        }
      };
      array(answer.tests.tests, "tests.tests", testCase);
      array(answer.tests.undecided, "tests.undecided", testCase);
      const fakeFlag = args.indexOf("--fake-rule"); const rule = fakeFlag < 0 ? undefined : args[fakeFlag + 1];
      const countedFakes = Array.isArray(answer.tests.tests) && answer.tests.tests.some(test => isObject(test) && test.throughFake === true);
      if (rule !== "count" && countedFakes) fail("tests.tests", "fakes counted only with --fake-rule count", answer.tests.tests);
      if (rule !== undefined && Array.isArray(answer.tests.undecided) && answer.tests.undecided.length) fail("tests.undecided", [], answer.tests.undecided);
      if (rule === undefined && Array.isArray(answer.tests.undecided) && answer.tests.undecided.length &&
          (!Array.isArray(answer.limits) || !answer.limits.some(limit => isObject(limit) && limit.reason === "other" && limit.text === "fake rule not set (A3)"))) fail("limits", "fake rule not set (A3)", answer.limits);
    }
  }
  if (answer.map !== undefined) {
    if (!isObject(answer.map)) fail("map", "ModuleMap", answer.map);
    else {
      array(answer.map.definitions, "map.definitions", node); array(answer.map.links, "map.links", link);
      array(answer.map.entries, "map.entries", (entry, path) => {
        if (!isObject(entry)) { fail(path, "entry", entry); return; }
        node(entry.fn, path + ".fn"); array(entry.steps, path + ".steps", flowStep);
      });
      if (answer.map.siblings !== undefined) {
        if (!isObject(answer.map.siblings)) fail("map.siblings", "siblings table", answer.map.siblings);
        else {
          array(answer.map.siblings.members, "map.siblings.members", (member, path) => {
            if (typeof member !== "string") fail(path, "member file", member);
          });
          array(answer.map.siblings.rows, "map.siblings.rows", (row, path) => {
            if (!isObject(row)) { fail(path, "sibling concern", row); return; }
            if (typeof row.concern !== "string" || !row.concern || !["shared", "varies", "unclear"].includes(row.status as string)) fail(path, "named shared/varies/unclear concern", row);
            array(row.cells, path + ".cells", (cell, at) => {
              if (!isObject(cell) || typeof cell.member !== "string" || typeof cell.text !== "string" || !cell.text.trim()) fail(at, "member, text and at", cell);
              else {
                location(cell.at, at + ".at");
                if (!isObject(cell.at) || cell.member !== cell.at.file) fail(at + ".member", "cell belongs to its source file", cell.member);
                if (source && !source.hasText(cell.at, cell.text)) fail(at + ".text", "source text at at (only trailing whitespace normalized)", cell.text);
              }
            });
          });
        }
      }
    }
  }
  const collections = [answer.matches, answer.links];
  if (isObject(answer.chain)) collections.push(answer.chain.up, answer.chain.down);
  if (isObject(answer.tests)) collections.push(answer.tests.tests, answer.tests.undecided);
  if (isObject(answer.map)) collections.push(answer.map.definitions, answer.map.links, answer.map.entries);
  const empty = collections.every(value => value === undefined || (Array.isArray(value) && value.length === 0));
  if (empty !== (answer.empty !== undefined)) fail("empty", empty ? "none found by static analysis" : "absent for a nonempty answer", answer.empty);
  return failures;
}
