import type { Store } from "./api";
export class FirstStore implements Store {
  save(value: string): number { return value.length; }
}
