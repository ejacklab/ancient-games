import { intakeCrate } from "./module/intake";

export function* collectCrate(label: string) {
  return yield* intakeCrate(label);
}
