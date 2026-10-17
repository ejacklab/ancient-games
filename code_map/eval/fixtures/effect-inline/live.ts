import type { InlineApi } from "./api";
export class InlineLive implements InlineApi {
  handle(value: number): number { return value + 1; }
}
