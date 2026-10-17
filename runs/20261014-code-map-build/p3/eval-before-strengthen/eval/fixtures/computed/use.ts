export function computed(obj: Record<string, () => number>, key: string) {
  return obj[key]();
}
