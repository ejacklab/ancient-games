declare const Bun: { write(path: URL, value: string): Promise<number> };

// This file belongs to the program even when a query targets a different file.


await Bun.write(new URL("./trap-ran.marker", import.meta.url), "throwing module executed");
throw new Error("passive ledger source must never execute");


export function dormantReceipt() {
  return "receipt";
}
