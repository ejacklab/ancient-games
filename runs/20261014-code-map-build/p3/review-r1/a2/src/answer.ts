export type NodeKind =
  | "function" | "method" | "arrow" | "effect-fn" | "property" | "class" | "variable" | "interface-member" | "other";

export type Loc = { file: string; line: number; endLine?: number };
export type Node = Loc & { name: string; kind: NodeKind };

export type LimitReason = "depth" | "dynamic" | "outside-repo" | "other-process" | "not-found" | "seen" | "other";
export type Limit = { at?: Loc; reason: LimitReason; text?: string; ref?: Loc };

export type Candidate = Node & { testFake: boolean };

export type Link = {
  from: Node;
  site: Loc;
  kind: "call" | "new" | "service-call";
  declaration?: Loc;
  resolution: "implementation" | "ambiguous" | "unresolved";
  to?: Node;
  candidates: Candidate[];
  via: "definition" | "implementation-lookup";
  reason?: string;
};

export type ChainStep = { level: number; link: Link; children: ChainStep[]; stop?: Limit };

export type TestCase = { file: string; line: number; name: string; path: Link[]; throughFake: boolean };
export type TestsAnswer = { label: "static-call-path"; count: number; tests: TestCase[]; undecided: TestCase[] };

export type StepKind = "call" | "if" | "else" | "loop" | "try" | "catch" | "return" | "yield*";
export type Step = { kind: StepKind; at: Loc; text: string; children?: Step[] };

export type Siblings = {
  members: string[];
  rows: { concern: string; status: "shared" | "varies" | "unclear"; cells: { member: string; text: string; at: Loc }[] }[];
};

export type ModuleMap = {
  definitions: Node[];
  links: Link[];
  entries: { fn: Node; steps: Step[] }[];
  siblings?: Siblings;
};

export type Answer = {
  command: string;
  query: string[];
  ambiguous?: boolean;
  matches?: Node[];
  links?: Link[];
  chain?: { up: ChainStep[]; down: ChainStep[] };
  tests?: TestsAnswer;
  map?: ModuleMap;
  limits: Limit[];
  empty?: "none found by static analysis";
};

export const emptyMarker = "none found by static analysis" as const;

export function isEmptyAnswer(answer: Answer): boolean {
  const collections: (Node[] | Link[] | ChainStep[] | TestCase[] | unknown[] | undefined)[] = [answer.matches, answer.links];
  if (answer.chain) collections.push(answer.chain.up, answer.chain.down);
  if (answer.tests) collections.push(answer.tests.tests, answer.tests.undecided);
  if (answer.map) collections.push(answer.map.definitions, answer.map.links, answer.map.entries);
  return collections.every(value => value === undefined || value.length === 0);
}

export function finish(answer: Answer): Answer {
  if (answer.empty === undefined && isEmptyAnswer(answer)) return { ...answer, empty: emptyMarker };
  return answer;
}

/** One limit per reason, at the first place it happened; each link keeps its own reason. */
export class LimitLog {
  private items: Limit[] = [];
  private keys = new Set<string>();

  add(limit: Limit): void {
    const key = limit.reason === "other" ? JSON.stringify(limit) : limit.reason;
    if (this.keys.has(key)) return;
    this.keys.add(key);
    this.items.push(limit);
  }

  addReason(reason: LimitReason, at?: Loc, text?: string): void {
    this.add(at ? { at, reason, ...(text ? { text } : {}) } : { reason, ...(text ? { text } : {}) });
  }

  get all(): Limit[] {
    return this.items;
  }
}