// Long routes precede shortcuts in both source and call order.
export function beginInspection() {
  inspectCorridor();
  inspectHub();
}

export function inspectCorridor() {
  return inspectCorner();
}

export function inspectCorner() {
  return inspectHub();
}

export function inspectHub() {
  return recordInspection();
}

export function recordInspection() {
  return sealInspection();
}

export function sealInspection() { return 41; }

export function receiveInspection() { return 37; }

export function receiveCorridor() {
  return receiveInspection();
}

export function receiveCorner() {
  return receiveCorridor();
}

export function receiveHub() {
  receiveCorner();
  return receiveInspection();
}

export function receiveRecord() {
  return receiveHub();
}

export function receiveSeal() {
  return receiveRecord();
}

export function splitInspection() {
  inspectLeft();
  inspectRight();
}

export function inspectLeft() {
  return combineInspection();
}

export function inspectRight() {
  return combineInspection();
}

export function combineInspection() {
  return finishInspection();
}

export function finishInspection() { return 43; }

export function repeatInspection() {
  combineInspection();
  return combineInspection();
}

export function inspectCycle() {
  return resumeCycle();
}

export function resumeCycle() {
  return inspectCycle();
}

export function inspectSelf() {
  return inspectSelf();
}

export class Receipt {
  constructor() {
    finishInspection();
  }
}

export function createReceipt() {
  return new Receipt();
}

export function pointAtInspection() {
  return combineInspection;
}

