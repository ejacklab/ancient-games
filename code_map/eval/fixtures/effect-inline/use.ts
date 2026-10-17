import { Effect } from "./effect";
import { InlineService } from "./api";
export function launchInline() {
  return Effect.gen(function* () {
    const service = yield* InlineService;
    return service.handle(1);
  });
}
