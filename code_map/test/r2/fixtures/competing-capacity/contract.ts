import { Context, type Task } from "../effect-runtime";

export interface Interface {
  readonly reserve: (units: number) => Task<number>;
}

export class Capacity extends Context.Service<Capacity, Interface>()("@app/Capacity") {}
