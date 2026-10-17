import type { PermissionApi } from "./api";
export class LivePermission implements PermissionApi {
  assert(path: string): boolean {
    return path.length > 0;
  }
}
const Layer = { succeed<T>(service: T) { return { service }; } };
export const liveLayer = Layer.succeed<PermissionApi>(new LivePermission());
