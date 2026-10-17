import * as Auth from "./auth";

export function authorize(token: string) {
  return Auth.header(token);
}

export function authorizeUser(user: string, secret: string) {
  return Auth.header(user, secret);
}
