import { externalReceipt, type ParcelPort, type ReceiptPort } from "./port";

export function submitParcel(port: ParcelPort) {
  return port.dispatch("fragile");
}

export function collectReceipt(port: ReceiptPort) {
  return port.receipt("ticket-42");
}

export function collectExternalReceipt() {
  return externalReceipt("ticket-99");
}
