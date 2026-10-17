import { Effect } from "../effect-runtime";
import { Warehouse } from "./port";

// A source-defined chain extends eight call links each way from dispatchCenter.
export const warehouseLayer = Effect.fn("Warehouse.layer")(function* () {
  const dockEight = Effect.fn("Warehouse.dockEight")(function* () {
    const warehouse = yield* Warehouse.Service;
    return yield* warehouse.dockSeven();
  });

  const dockSeven = Effect.fn("Warehouse.dockSeven")(function* () {
    const warehouse = yield* Warehouse.Service;
    return yield* warehouse.dockSix();
  });

  const dockSix = Effect.fn("Warehouse.dockSix")(function* () {
    const warehouse = yield* Warehouse.Service;
    return yield* warehouse.dockFive();
  });

  const dockFive = Effect.fn("Warehouse.dockFive")(function* () {
    const warehouse = yield* Warehouse.Service;
    return yield* warehouse.dockFour();
  });

  const dockFour = Effect.fn("Warehouse.dockFour")(function* () {
    const warehouse = yield* Warehouse.Service;
    return yield* warehouse.dockThree();
  });

  const dockThree = Effect.fn("Warehouse.dockThree")(function* () {
    const warehouse = yield* Warehouse.Service;
    return yield* warehouse.dockTwo();
  });

  const dockTwo = Effect.fn("Warehouse.dockTwo")(function* () {
    const warehouse = yield* Warehouse.Service;
    return yield* warehouse.dockOne();
  });

  const dockOne = Effect.fn("Warehouse.dockOne")(function* () {
    const warehouse = yield* Warehouse.Service;
    return yield* warehouse.dispatchCenter();
  });

  const dispatchCenter = Effect.fn("Warehouse.dispatchCenter")(function* () {
    const warehouse = yield* Warehouse.Service;
    return yield* warehouse.shelfOne();
  });

  const shelfOne = Effect.fn("Warehouse.shelfOne")(function* () {
    const warehouse = yield* Warehouse.Service;
    return yield* warehouse.shelfTwo();
  });

  const shelfTwo = Effect.fn("Warehouse.shelfTwo")(function* () {
    const warehouse = yield* Warehouse.Service;
    return yield* warehouse.shelfThree();
  });

  const shelfThree = Effect.fn("Warehouse.shelfThree")(function* () {
    const warehouse = yield* Warehouse.Service;
    return yield* warehouse.shelfFour();
  });

  const shelfFour = Effect.fn("Warehouse.shelfFour")(function* () {
    const warehouse = yield* Warehouse.Service;
    return yield* warehouse.shelfFive();
  });

  const shelfFive = Effect.fn("Warehouse.shelfFive")(function* () {
    const warehouse = yield* Warehouse.Service;
    return yield* warehouse.shelfSix();
  });

  const shelfSix = Effect.fn("Warehouse.shelfSix")(function* () {
    const warehouse = yield* Warehouse.Service;
    return yield* warehouse.shelfSeven();
  });

  const shelfSeven = Effect.fn("Warehouse.shelfSeven")(function* () {
    const warehouse = yield* Warehouse.Service;
    return yield* warehouse.shelfEight();
  });

  const shelfEight = Effect.fn("Warehouse.shelfEight")(function* () {
    return 31;
  });

  return Warehouse.of({ dockEight, dockSeven, dockSix, dockFive, dockFour, dockThree, dockTwo, dockOne, dispatchCenter, shelfOne, shelfTwo, shelfThree, shelfFour, shelfFive, shelfSix, shelfSeven, shelfEight });
});

