import { Context, type Task } from "../effect-runtime";

export interface WarehouseApi {
  readonly dockEight: () => Task<number>;
  readonly dockSeven: () => Task<number>;
  readonly dockSix: () => Task<number>;
  readonly dockFive: () => Task<number>;
  readonly dockFour: () => Task<number>;
  readonly dockThree: () => Task<number>;
  readonly dockTwo: () => Task<number>;
  readonly dockOne: () => Task<number>;
  readonly dispatchCenter: () => Task<number>;
  readonly shelfOne: () => Task<number>;
  readonly shelfTwo: () => Task<number>;
  readonly shelfThree: () => Task<number>;
  readonly shelfFour: () => Task<number>;
  readonly shelfFive: () => Task<number>;
  readonly shelfSix: () => Task<number>;
  readonly shelfSeven: () => Task<number>;
  readonly shelfEight: () => Task<number>;
}

export class Warehouse extends Context.Service<Warehouse, WarehouseApi>()("@fixture/Warehouse") {}

