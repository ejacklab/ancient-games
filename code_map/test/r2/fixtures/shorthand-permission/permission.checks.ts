import { Effect } from "../effect-runtime";
import { Permission } from "./contract";
import { approveDraft } from "./actions";

declare function test(name: string, body: () => void): void;

const fake = Permission.of({
  assert: () => Effect.succeed(true),
  ask: () => Effect.succeed("test reply"),
});

test("approves a draft with a fake", () => {
  const workflow = approveDraft("draft/test");
  workflow.next();
  workflow.next(fake);
});
