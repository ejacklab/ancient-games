import type { Store } from "./api";
export class SecondStore implements Store {
  save(value: string): number { return value.length + 1; }
}
