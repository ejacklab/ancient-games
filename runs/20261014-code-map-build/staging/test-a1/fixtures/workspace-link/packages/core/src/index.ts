export class Ledger {
  readonly entries: string[] = [];
  record(entry: string) {
    this.entries.push(entry);
    return this.entries.length;
  }
}

export function openLedger(): Ledger {
  return new Ledger();
}
