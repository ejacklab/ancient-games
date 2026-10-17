import { paddedCredit } from "./module/amount";

export function billForCrate(quantity: number): number {
  return paddedCredit(quantity);
}
