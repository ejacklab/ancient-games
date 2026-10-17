import { Context, type Task } from "../effect-runtime";

export interface ParcelDeskShape {
  readonly seal: (parcel: string) => Task<number>;
}

export class ParcelDesk extends Context.Service<ParcelDesk, ParcelDeskShape>()("@parcel/Desk") {}
