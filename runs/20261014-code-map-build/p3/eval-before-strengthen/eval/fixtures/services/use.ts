import { Permission } from "./api";
export function* checkPermission(path: string) {
  const permission = yield* Permission.Service;
  return permission.assert(path);
}
