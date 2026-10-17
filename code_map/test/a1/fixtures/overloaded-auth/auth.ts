export function header(token: string): string;
export function header(user: string, secret: string): string;
export function header(first: string, second?: string): string {
  return second === undefined ? `Bearer ${first}` : `Basic ${first}:${second}`;
}
