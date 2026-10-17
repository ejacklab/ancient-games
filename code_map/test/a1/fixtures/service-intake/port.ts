import { Context, type Task } from "../effect-runtime";

export interface DepotShape {
  readonly acceptCrate: (label: string) => Task<boolean>;
  readonly recordCrate: (label: string) => Task<string>;
}

export class Depot extends Context.Service<Depot, DepotShape>()("@fixture/Depot") {}
