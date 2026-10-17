export const requirementLines = {
  R1: ["mapping a fixture whose top level writes a marker creates that marker"],
  R2: [
    "an implementation the lookup finds has no link",
    "a declaration is presented as proof of an implementation",
    "a test fake is unlabelled or presented as the real implementation",
    "an unresolved or ambiguous target is unmarked",
  ],
  R3: ["protected content leaves the machine or enters git"],
  A1: ["a claim lacks its location or contradicts the code, or a checked example misses a known item"],
  A2: [
    "a known place is not found",
    "an ambiguous match is treated as certain, or a candidate not built is not named",
    "a known link within the depth is missing, or a shown link contradicts the code",
    "a link lacks its kind or location",
    "a function reached twice is shown twice",
  ],
  A3: [
    "the count differs from the list, or a link lacks its evidence",
    "a test with a known path is missing",
    "static links are called coverage",
    "the per-function file report runs without the user's request",
  ],
  A5: ["an answer comes only inside a dump or without its evidence or limits, or a whole map is produced unasked"],
  A6: ["fewer than three modules are mapped, or a map fails A1"],
  L1: ["a branch stops early without a reason, or an empty result is presented as proof of absence"],
  L2: ["it leaves out correctness, the build cost, the reading tokens or the time, or hides a worse result"],
} as const;

export type Requirement = keyof typeof requirementLines;
export type Status = "MET" | "NOT MET" | "NOT CHECKED";

export const uncheckedParts = [
  { requirement: "A2", status: "NOT CHECKED", reason: "P6 checks the agent's selection and naming of candidates it did not build." },
  { requirement: "A3", status: "NOT CHECKED", reason: "P6 checks whether the agent asks the user before requesting a per-function file report." },
  { requirement: "A5", status: "NOT CHECKED", reason: "P6 checks whether the agent requests a whole map without being asked." },
  { requirement: "R3", status: "NOT CHECKED", reason: "Network isolation and filesystem snapshots do not establish absence of caught connection attempts, writes outside the observed trees, putting content in git, transmission by other processes, or training use." },
] as const;
