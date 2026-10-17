import type { PermissionApi } from "./api";
import { checkPermission } from "./use";
declare function test(name: string, body: () => void): void;
export class FakePermission implements PermissionApi {
  assert(_path: string): boolean { return true; }
}
test("uses fake permission", () => {
  const fake = new FakePermission();
  // The generator receives only the fake; this test never imports the live layer.
  const workflow = checkPermission("test");
  workflow.next();
  workflow.next(fake);
});
