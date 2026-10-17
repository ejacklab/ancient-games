import { Effect } from "../runtime";
import { Router } from "../port";

export function ticketLabel(ticket: string): string {
  return `desk:${ticket}`;
}

export const routingLayer = Effect.fn("Router.layer")(function* () {
  const routeTicket = Effect.fn("Router.routeTicket")(function* (ticket: string) {
    const label = ticketLabel(ticket);
    return yield* Effect.succeed(label);
  });

  return Router.of({ routeTicket });
});
