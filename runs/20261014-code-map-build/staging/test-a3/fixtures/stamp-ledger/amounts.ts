// Deliberately separate the declarations from the fixture's test lines.
export const stampPrefix = "ledger/";

export function unitStamp(quantity: number) {
  return quantity * 13;
}

export function paddedStamp(quantity: number) {
  return unitStamp(quantity) + 5;
}
