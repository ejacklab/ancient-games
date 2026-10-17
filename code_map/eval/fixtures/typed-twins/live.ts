import type { SourceApi } from "./api";
export class LiveSender implements SourceApi {
  send(value: number): number { return value + 1; }
}
