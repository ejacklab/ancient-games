import { adjustTotal } from "./adjustment";

declare const Bun: { write(path: URL, value: string): Promise<number> };

await Bun.write(new URL("./ledger-ran.marker", import.meta.url), "ledger executed");

// These definitions remain readable even though the module has a side effect.

export function recordTotal(amount: number) {
  return adjustTotal(amount);
}


export function submitLedger() {
  return recordTotal(17);
}
