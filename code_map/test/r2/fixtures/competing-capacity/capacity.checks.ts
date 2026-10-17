import { Effect } from "../effect-runtime";
import { Capacity } from "./contract";

declare function test(name: string, body: () => void): void;

test("uses a capacity substitute", () => {
  Capacity.of({
    reserve: () => Effect.succeed(900),
  });
});
