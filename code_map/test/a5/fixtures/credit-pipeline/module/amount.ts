// The credit functions deliberately have no dependency on the warehouse module.

export function unitCredit(quantity: number): number {
  return quantity * 13;
}

export function paddedCredit(quantity: number): number {
  return unitCredit(quantity) + 7;
}
