import type { Store } from "./api";
export function saveValue(store: Store) {
  return store.save("value");
}
