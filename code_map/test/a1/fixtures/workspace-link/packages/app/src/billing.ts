// @ts-ignore -- the test links @fixture/core into node_modules only while it runs (COO fix, 2026-10-17).
import { openLedger } from "@fixture/core";

export function bill(amount: number) {
  const ledger = openLedger();
  return ledger.record(`bill:${amount}`);
}
