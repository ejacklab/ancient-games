import type { SourceApi, TestApi } from "./api";
export function viaSource(api: SourceApi) {
  return api.send(1);
}
export function viaTest(api: TestApi) {
  return api.send("value");
}
