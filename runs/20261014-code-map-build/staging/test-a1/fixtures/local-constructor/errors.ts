import { Base } from "./base";

export class LocalError extends Base {}

export function rejectParcel(label: string) {
  return new LocalError(label);
}
