import type { ParcelPort } from "./port";

export class BicycleCourier implements ParcelPort {
  dispatch(parcel: string): number {
    return parcel.length + 11;
  }
}

export class RailCourier implements ParcelPort {
  dispatch(shipment: string): number {
    return shipment.length + 37;
  }
}

// The spelling alone cannot establish an implementation of ParcelPort.
export interface NumericPort { dispatch(value: number): string }
export class UnrelatedCourier implements NumericPort {
  dispatch(value: number): string { return String(value); }
}
