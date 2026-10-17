import { Effect } from "../effect-runtime";
import { Permission } from "./contract";

declare function test(name: string, body: () => void): void;

test("has only a fake permission", () => {
  Permission.of({
    assert: () => Effect.succeed(false),
  });
});
