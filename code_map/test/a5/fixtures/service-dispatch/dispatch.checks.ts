import { dispatchTicket } from "./module/workflow";
import { Router } from "./port";
import { Effect } from "./runtime";

declare function test(name: string, body: () => void): void;

const simulatedRouter = Router.of({
  routeTicket: () => Effect.succeed("simulated desk"),
});

test("dispatches an incident ticket", () => {
  const task = dispatchTicket("incident-83");
  task.next();
  task.next(simulatedRouter);
});
