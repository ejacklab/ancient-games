import { Effect } from "../../effect-runtime";
import { Depot } from "../port";

// Methods live inside the layer rather than in top-level declarations.
export const depotLayer = Effect.fn("Depot.layer")(function* () {
  const acceptCrate = Effect.fn("Depot.acceptCrate")(function* (label: string) {
    return yield* Effect.succeed(label.startsWith("crate/"));
  });

  return Depot.of({
    acceptCrate,
    *recordCrate(label: string) {
      return yield* Effect.succeed(`stored:${label}`);
    },
  });
});
