import { target as realTarget } from "./target";
declare function test(name: string, body: () => void): void;
function target() { return 99; }
test("helper only", () => { target(); });
test("real target", () => { realTarget(); });
