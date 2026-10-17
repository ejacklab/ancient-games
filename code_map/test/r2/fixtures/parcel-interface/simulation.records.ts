import type { ParcelPort } from "./port";

declare function test(name: string, body: () => void): void;

export class SimulationCourier implements ParcelPort {
  dispatch(_parcel: string): number { return 0; }
}

test("simulates a parcel", () => { new SimulationCourier().dispatch("sample"); });
