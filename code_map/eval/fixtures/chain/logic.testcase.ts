import { start } from "./logic";
declare function test(name: string, body: () => void): void;
test("reaches leaf", () => { start(); });
export {};
