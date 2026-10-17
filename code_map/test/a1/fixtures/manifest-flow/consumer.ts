import { compileManifest } from "./module/manifest";

export function receiveManifest() {
  return compileManifest(["cargo-27"]);
}
