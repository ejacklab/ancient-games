declare const Bun: { write(path: URL, value: string): Promise<number> };
await Bun.write(new URL("./EXECUTED.marker", import.meta.url), "repository executed");
export function markerLeaf() { return 1; }
export function markerEntry() { return markerLeaf(); }
