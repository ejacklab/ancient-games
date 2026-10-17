declare const Bun: { write(path: URL, value: string): Promise<number> };

// Even an imported dependency must be read without running its top level.

await Bun.write(new URL("./dependency-ran.marker", import.meta.url), "dependency executed");


export function adjustTotal(amount: number) {
  return amount + 3;
}
