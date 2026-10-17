import { normalizeManifest, logManifest } from "../support";

export class ManifestBook {
  record(label: string) {
    return normalizeManifest(label);
  }
}

export function compileManifest(labels: string[]) {
  const book = new ManifestBook();
  for (const label of labels) {
    if (label.length === 0) {
      continue;
    } else {
      book.record(label);
    }
  }
  try {
    logManifest(
      "manifest-audit: preserve every character of this deliberately long source literal; its tail is the evidence that the command has not shortened the returned step text: AUDIT_TAIL_862",
    );
  } catch (error) {
    return "audit-failed";
  }
  return "compiled";
}

export function exportedButUncalled() {
  return "idle";
}

function privateManifest() {
  return "private";
}
