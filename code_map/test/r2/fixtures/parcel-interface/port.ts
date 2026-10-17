export interface ParcelPort {
  dispatch(parcel: string): number;
}

export interface ReceiptPort {
  readonly receipt: (ticket: string) => number;
}

export declare function externalReceipt(ticket: string): number;
