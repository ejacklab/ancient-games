import { Effect } from "../runtime";
import { Router } from "../port";

// Submit the ticket through the injected routing service.

export const dispatchTicket = Effect.fn("Desk.dispatch")(function* (ticket: string) {
  const router = yield* Router.Service;
  return yield* router.routeTicket(ticket);
});
