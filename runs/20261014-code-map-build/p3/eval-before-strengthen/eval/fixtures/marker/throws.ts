declare const Bun: { write(path: URL, value: string): Promise<number> };
await Bun.write(new URL("./EXECUTED.marker", import.meta.url), "throwing source executed");
export function throwEntry() { return 1; }
throw new Error("fixture top level must never run");
