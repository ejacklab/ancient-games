import type { RelayApi } from "./api";
export class RelayLive implements RelayApi {
  deliver(value: number): number { return value + 1; }
}
