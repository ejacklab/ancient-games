// Not a plugin: two plain helper functions.
export function joinPath(directory: string, file: string) { return `${directory}/${file}`; }
export function isHidden(path: string) { return path.split("/").pop()?.startsWith(".") ?? false; }
