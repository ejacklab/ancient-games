// Unrelated to the Permission service: another object with a permission.assert property path.
type Guard = { assert: (path: string) => boolean };

export const sandbox: { permission: Guard } = { permission: { assert: () => false } };

sandbox.permission.assert = (path: string) => !path.startsWith("/etc");
