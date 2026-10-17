import { markerEntry } from "./main";
declare function test(name: string, body: () => void): void;
test("marker entry", () => { markerEntry(); });
export {};
