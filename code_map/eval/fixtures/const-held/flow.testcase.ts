import { start } from "./outside";
declare function test(name: string, body: () => void): void;
test("reaches constant-held leaf", () => { start(1); });
