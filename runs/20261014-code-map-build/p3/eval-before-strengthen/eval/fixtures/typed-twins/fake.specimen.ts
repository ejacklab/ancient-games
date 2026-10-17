import type { TestApi } from "./api";
import { viaSource } from "./use"; import { LiveSender } from "./live";
declare function test(name: string, body: () => void): void;
export class FakeSender implements TestApi {
  send(value: string): string { return value; }
}
test("source sender", () => { viaSource(new LiveSender()); });
