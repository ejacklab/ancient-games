import type { RelayApi } from "./api";
export class RelayFake implements RelayApi {
  deliver(value: number): number { return value; }
}
