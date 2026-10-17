import { privateTotal } from "./module/ledger";

export function submitLedger(units: number) {
  return privateTotal(units);
}
