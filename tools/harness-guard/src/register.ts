// M4: use-case register and coverage (SPEC.md M4). A register is the owner's own YAML: what was asked for, what the
// agent added, what was decided, and which test covers which unit. The guard reads ids, counts and hashes out of it;
// the register's own text stays in the file.

import { createHash } from "node:crypto";
import * as fs from "node:fs";
import * as path from "node:path";
import type { CoverageEntry, CoverageReport, Finding, Register, Requirement, Unit, UseCase } from "./types.ts";

const TARGET = 80;
const VISION = "vision";

export class RegisterError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "RegisterError";
  }
}

function isEntry(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function nonEmptyString(value: unknown): value is string {
  return typeof value === "string" && value.trim() !== "";
}

// At least one usable item: empty and blank entries do not count as written.
function filled(value: unknown): boolean {
  return Array.isArray(value) && value.some(nonEmptyString);
}

function idOf(entry: { id?: unknown }): string {
  return nonEmptyString(entry.id) ? entry.id : "(no id)";
}

function list<T>(value: T[] | undefined): T[] {
  return Array.isArray(value) ? value : [];
}

function useCaseList(r: Register): UseCase[] {
  return list(r.use_cases);
}

function requirementList(r: Register): Requirement[] {
  return list(r.requirements);
}

function coverageList(r: Register): CoverageEntry[] {
  return list(r.coverage);
}

// ---- loading ---------------------------------------------------------------------------------------------------

export function loadRegister(file: string): Register {
  const name = path.basename(file);
  let parsed: unknown;
  try {
    parsed = Bun.YAML.parse(fs.readFileSync(file, "utf8"));
  } catch {
    // The parser's own message would carry the source line, so the diagnostic stays generic.
    throw new RegisterError(`register ${name}: cannot be read or parsed`);
  }
  if (!isEntry(parsed) || parsed.register !== 1) {
    throw new RegisterError(`register ${name}: has no numeric "register: 1" marker`);
  }
  return parsed as unknown as Register;
}

export function isRegisterFile(file: string): boolean {
  const name = path.basename(file);
  return name === "register.yaml" || name.endsWith(".register.yaml");
}

// ---- acceptance -------------------------------------------------------------------------------------------------

type Verdict = "accepted" | "declined" | null;

function hasDecision(entry: { decision?: unknown }): boolean {
  return isEntry(entry.decision);
}

function verdictOf(entry: { decision?: { verdict?: unknown } }): Verdict {
  const verdict = entry.decision?.verdict;
  return verdict === "accepted" || verdict === "declined" ? verdict : null;
}

// A use case is accepted when the owner asked for it and no decision declined it, or when the agent's own
// case was accepted. Requirements are accepted the same way.
function accepted(entry: { origin?: unknown; decision?: { verdict?: unknown } }): boolean {
  const verdict = verdictOf(entry);
  if (verdict === "declined") return false;
  return entry.origin === "user" || verdict === "accepted";
}

// ---- units ------------------------------------------------------------------------------------------------------

function normalise(value: string): string {
  return value.toLowerCase().replace(/\s+/g, " ").trim();
}

export function units(r: Register): Unit[] {
  const built: Unit[] = [];
  const seen = new Set<string>();

  // A repeat of an earlier text adds nothing to the count: a variant is not a second unit.
  const add = (id: string, value: unknown, safety: boolean): void => {
    if (!nonEmptyString(value)) return;
    const key = normalise(value);
    if (seen.has(key)) return;
    seen.add(key);
    built.push({ id, text: value, safety });
  };

  for (const useCase of useCaseList(r)) {
    if (!accepted(useCase)) continue;
    const safety = useCase.safety === true;
    list(useCase.fails_if).forEach((item, i) => add(`${idOf(useCase)}/f${i + 1}`, item, safety));
    list(useCase.min_acceptance).forEach((item, i) => add(`${idOf(useCase)}/m${i + 1}`, item, safety));
  }
  for (const requirement of requirementList(r)) {
    if (!accepted(requirement)) continue;
    list(requirement.fails_if).forEach((item, i) => add(`${idOf(requirement)}/f${i + 1}`, item, false));
  }
  return built;
}

export function freezeHash(list: Unit[]): string {
  return createHash("sha256").update(JSON.stringify(list.map(({ id, text }) => [id, text]))).digest("hex");
}

// ---- validation -------------------------------------------------------------------------------------------------

export function validateRegister(r: Register): Finding[] {
  const findings: Finding[] = [];
  const knownUnits = new Set(units(r).map((unit) => unit.id));

  for (const useCase of useCaseList(r)) {
    const id = idOf(useCase);
    if (useCase.origin === "ai" && !hasDecision(useCase)) {
      findings.push({
        rule: "R13.1-no-decision",
        severity: "fail",
        message: `use case ${id}: an AI-origin entry needs a decision by the owner`,
        fix: "add decision: { by: <who>, verdict: accepted | declined }",
      });
    } else if (hasDecision(useCase) && !nonEmptyString(useCase.decision?.by)) {
      findings.push({
        rule: "R13.1-no-decision",
        severity: "fail",
        message: `use case ${id}: the decision names no "by"`,
        fix: "add decision.by",
      });
    }
    if (!accepted(useCase)) continue;
    if (!nonEmptyString(useCase.purpose) || !filled(useCase.fails_if) || !filled(useCase.min_acceptance)) {
      findings.push({
        rule: "R13.2-missing",
        severity: "fail",
        message: `use case ${id}: an accepted use case needs a purpose, at least one fails_if and at least one min_acceptance`,
        fix: "fill the three parts before the use case is built",
      });
    }
  }

  for (const requirement of requirementList(r)) {
    const id = idOf(requirement);
    if (requirement.origin === "ai" && !hasDecision(requirement)) {
      findings.push({
        rule: "R13.1-no-decision",
        severity: "fail",
        message: `requirement ${id}: an AI-origin entry needs a decision by the owner`,
        fix: "add decision: { by: <who>, verdict: accepted | declined }",
      });
    } else if (hasDecision(requirement) && !nonEmptyString(requirement.decision?.by)) {
      findings.push({
        rule: "R13.1-no-decision",
        severity: "fail",
        message: `requirement ${id}: the decision names no "by"`,
        fix: "add decision.by",
      });
    }
    if (!nonEmptyString(requirement.purpose) || !filled(requirement.serves)) {
      findings.push({
        rule: "R13.5-no-purpose",
        severity: "fail",
        message: `requirement ${id}: a requirement needs a purpose and at least one serves id (or "${VISION}")`,
        fix: "say what it is for and which use case or the vision it serves",
      });
    }
    if (requirement.origin === "ai" && !accepted(requirement)) {
      findings.push({
        rule: "R13.5-not-binding",
        severity: "warn",
        message: `requirement ${id}: an AI requirement the owner did not accept is not binding and is excluded from the units`,
        fix: "accept it in the register or drop it",
      });
    }
    for (const serves of list(requirement.serves)) {
      if (!nonEmptyString(serves) || serves === VISION) continue;
      if (!isKnownId(serves, r)) {
        findings.push({
          rule: "R13-unknown-ref",
          severity: "fail",
          message: `requirement ${id}: serves names ${serves}, which is not a use case or requirement of this register`,
          fix: "name an existing id or the vision",
        });
      }
    }
  }

  const caseRefs = caseIds(r);
  const requirementRefs = requirementIds(r);
  for (const conflict of list(r.conflicts)) {
    const entry: Record<string, unknown> = isEntry(conflict) ? conflict : {};
    const useCase: unknown = entry.use_case;
    const requirement: unknown = entry.requirement;
    if (isEntry(conflict) && conflict.shown_to_owner !== true) {
      findings.push({
        rule: "R13.7-conflict-not-shown",
        severity: "fail",
        message: `conflict ${String(useCase)} vs ${String(requirement)}: not shown to the owner`,
        fix: "show the conflict to the owner and set shown_to_owner: true",
      });
    }
    if (nonEmptyString(useCase) && !caseRefs.has(useCase)) {
      findings.push({
        rule: "R13-unknown-ref",
        severity: "fail",
        message: `conflict names the use case ${useCase}, which this register does not hold`,
        fix: "name an existing use case id",
      });
    }
    if (nonEmptyString(requirement) && !requirementRefs.has(requirement)) {
      findings.push({
        rule: "R13-unknown-ref",
        severity: "fail",
        message: `conflict names the requirement ${requirement}, which this register does not hold`,
        fix: "name an existing requirement id",
      });
    }
  }

  for (const entry of coverageList(r)) {
    const unit: unknown = isEntry(entry) ? entry.unit : undefined;
    if (!nonEmptyString(unit) || knownUnits.has(unit)) continue;
    findings.push({
      rule: "R13-unknown-ref",
      severity: "fail",
      message: `coverage names the unit ${unit}, which no accepted entry produces`,
      fix: "name a unit of units(r) or drop the entry",
    });
  }

  return findings;
}

function caseIds(r: Register): Set<string> {
  return new Set(useCaseList(r).map((useCase) => idOf(useCase)));
}

function requirementIds(r: Register): Set<string> {
  return new Set(requirementList(r).map((requirement) => idOf(requirement)));
}

function isKnownId(id: string, r: Register): boolean {
  return caseIds(r).has(id) || requirementIds(r).has(id);
}

// ---- coverage ---------------------------------------------------------------------------------------------------

function isSkipped(entry: CoverageEntry | undefined): boolean {
  return entry !== undefined && isEntry(entry.skippable);
}

function skipReason(entry: CoverageEntry | undefined): string {
  if (entry === undefined || !isEntry(entry.skippable)) return "";
  const reason: unknown = entry.skippable.reason;
  return nonEmptyString(reason) ? reason.trim() : "";
}

export function coverage(r: Register): CoverageReport {
  const list = units(r);
  const entries = new Map<string, CoverageEntry>();
  for (const entry of coverageList(r)) {
    const unit: unknown = isEntry(entry) ? entry.unit : undefined;
    if (nonEmptyString(unit)) entries.set(unit, entry);
  }

  const findings: Finding[] = [];

  if (!nonEmptyString(r.frozen)) {
    findings.push({
      rule: "R11.1-not-frozen",
      severity: "fail",
      message: "the register has no frozen hash, so this count has no fixed start",
      fix: `set frozen: ${freezeHash(list)}`,
    });
  } else if (r.frozen !== freezeHash(list)) {
    findings.push({
      rule: "R11.1-frozen-mismatch",
      severity: "fail",
      message: "the frozen hash is not the hash of the current units, so the units changed and a new count must start",
      fix: `set frozen: ${freezeHash(list)}`,
    });
  }

  let covered = 0;
  for (const unit of list) {
    const entry = entries.get(unit.id);
    const coveredBy = entry !== undefined && isEntry(entry) && Array.isArray(entry.covered_by) ? entry.covered_by : [];
    const isCovered = coveredBy.some(nonEmptyString);
    if (isCovered) covered += 1;

    if (isSkipped(entry)) {
      if (skipReason(entry) === "") {
        findings.push({
          rule: "R11.1-skip-no-reason",
          severity: "fail",
          message: `unit ${unit.id}: skippable without a reason`,
          fix: "give skippable.reason, or cover the unit",
        });
      }
      if (unit.safety) {
        findings.push({
          rule: "R11.1-safety-skipped",
          severity: "fail",
          message: `unit ${unit.id}: a safety unit cannot be skipped`,
          fix: "cover it with a test",
        });
      }
    } else if (!isCovered) {
      findings.push({
        rule: "R11.1-basic-uncovered",
        severity: "fail",
        message: `unit ${unit.id}: no test covers it and it is not skippable`,
        fix: "add a coverage entry naming a test, or a skippable with a reason",
      });
    }
  }

  const percent = list.length === 0 ? 0 : Math.round((covered / list.length) * 1000) / 10;
  if (percent < TARGET) {
    findings.push({
      rule: "R11.1-below-target",
      severity: "warn",
      message: `coverage is ${percent}% of ${list.length} units, below the ${TARGET}% target`,
      fix: "cover more units or state why the rest are skipped",
    });
  }

  return { total: list.length, covered, percent, target: TARGET, findings };
}