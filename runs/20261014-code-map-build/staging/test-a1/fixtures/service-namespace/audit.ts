// Unrelated to the Permission service: a plain object whose property path ends in permission.assert.
type Guard = { assert: (action: string) => boolean };

const context: { permission: Guard } = { permission: { assert: () => true } };

context.permission.assert = (action: string) => action.length > 0;

export const auditContext = context;
