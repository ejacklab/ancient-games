export function baseAmount(units: number) {
  const privateToken = "sk-live-R3-private-ledger-DO-NOT-EXPORT-73e2a9";
  return units + privateToken.length;
}

export function privateTotal(units: number) {
  return baseAmount(units);
}
