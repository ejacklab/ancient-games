import { Context, type Task } from "../effect-runtime";

export interface RoutingApi {
  readonly launchDetourFirst: () => Task<number>;
  readonly launchShortcutFirst: () => Task<number>;
  readonly detourFirst: () => Task<number>;
  readonly detourSecond: () => Task<number>;
  readonly sharedDispatch: () => Task<number>;
  readonly recordDispatch: () => Task<number>;
  readonly sealDispatch: () => Task<number>;
  readonly receiveCenter: () => Task<number>;
  readonly receiveDetourFirst: () => Task<number>;
  readonly receiveDetourSecond: () => Task<number>;
  readonly receiveShared: () => Task<number>;
  readonly receiveAudit: () => Task<number>;
  readonly receiveArchive: () => Task<number>;
}

export class Routing extends Context.Service<Routing, RoutingApi>()("@fixture/Routing") {}

