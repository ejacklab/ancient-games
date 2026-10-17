import { Context, type Task } from "./runtime";

export interface Routing {
  readonly routeTicket: (ticket: string) => Task<string>;
}

export class Router extends Context.Service<Router, Routing>()("@desk/Router") {}
