export interface PermissionApi {
  assert(path: string): boolean;
}
export namespace Permission {
  export const Service = {
    *[Symbol.iterator](): Generator<unknown, PermissionApi, PermissionApi> {
      return yield {};
    },
  };
}
