import { saveRecord } from "../a/store";

export function nightlyJob() {
  return saveRecord("nightly");
}
