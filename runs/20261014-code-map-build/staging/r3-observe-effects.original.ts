import fs from "node:fs";
import promises from "node:fs/promises";
import net from "node:net";
import http from "node:http";
import https from "node:https";
import dgram from "node:dgram";
import tls from "node:tls";
import dns from "node:dns";
import dnsPromises from "node:dns/promises";
import childProcess from "node:child_process";
import { mock } from "bun:test";
import { fileURLToPath } from "node:url";

// Observe calls before forwarding them, so caught errors and transient writes stay visible.
// This covers JS APIs, not direct native syscalls or work done by another process.
const auditPrefix = "R3_EFFECT ";
const originalWriteSync = fs.writeSync;
function record(kind: string, api: string, args: unknown[]) {
  const path = args[0];
  if (kind === "file" && (path === 1 || path === 2)) return;
  const target = path instanceof URL ? fileURLToPath(path)
    : Buffer.isBuffer(path) ? path.toString() : path;
  Reflect.apply(originalWriteSync, fs, [2, `${auditPrefix}${JSON.stringify({ kind, api, target })}\n`]);
}

function observe(object: any, name: string, kind: string, api: string) {
  const original = object[name];
  if (typeof original !== "function") return;
  object[name] = function (...args: unknown[]) {
    record(kind, api, args);
    return Reflect.apply(original, this, args);
  };
}

const writers = [
  "writeFile", "appendFile", "truncate", "unlink", "rm", "rmdir", "mkdir", "mkdtemp",
  "rename", "copyFile", "cp", "link", "symlink", "chmod", "chown", "lchmod", "lchown",
  "utimes", "lutimes", "write", "writev", "ftruncate", "fchmod", "fchown", "futimes",
];
for (const name of writers) {
  observe(fs, name, "file", `fs.${name}`);
  observe(fs, `${name}Sync`, "file", `fs.${name}Sync`);
  observe(promises, name, "file", `fs.promises.${name}`);
}
observe(fs, "createWriteStream", "file", "fs.createWriteStream");

function opensForWrite(flags: unknown) {
  if (typeof flags === "string") return /[wa+]/.test(flags);
  return typeof flags === "number" && (flags & (
    fs.constants.O_WRONLY | fs.constants.O_RDWR | fs.constants.O_CREAT |
    fs.constants.O_TRUNC | fs.constants.O_APPEND
  )) !== 0;
}
for (const [object, name, label] of [
  [fs, "open", "fs.open"], [fs, "openSync", "fs.openSync"], [promises, "open", "fs.promises.open"],
] as const) {
  const original = object[name];
  (object as any)[name] = function (...args: unknown[]) {
    if (opensForWrite(args[1])) record("file", label, args);
    return Reflect.apply(original, this, args);
  };
}

observe(Bun, "write", "file", "Bun.write");
const originalFile = Bun.file;
Bun.file = function (...args: Parameters<typeof Bun.file>) {
  const file = Reflect.apply(originalFile, Bun, args);
  for (const name of ["writer", "write", "delete"]) {
    const original = (file as any)[name];
    if (typeof original === "function") (file as any)[name] = function (...values: unknown[]) {
      record("file", `Bun.file.${name}`, args);
      return Reflect.apply(original, file, values);
    };
  }
  return file;
} as typeof Bun.file;

for (const [object, names, label] of [
  [net.Socket.prototype, ["connect"], "net.Socket"],
  [http, ["request", "get"], "http"], [https, ["request", "get"], "https"],
  [tls, ["connect"], "tls"],
  [dgram.Socket.prototype, ["connect", "send"], "dgram.Socket"],
  [dns, ["lookup", "lookupService", "resolve", "resolve4", "resolve6", "resolveAny", "reverse"], "dns"],
  [dnsPromises, ["lookup", "lookupService", "resolve", "resolve4", "resolve6", "resolveAny", "reverse"], "dns.promises"],
  [Bun, ["connect", "listen", "udpSocket", "serve"], "Bun"],
  [globalThis, ["fetch"], "globalThis"],
] as const) {
  for (const name of names) observe(object, name, "network", `${label}.${name}`);
}
const OriginalWebSocket = globalThis.WebSocket;
globalThis.WebSocket = new Proxy(OriginalWebSocket, {
  construct(target, args, newTarget) {
    record("network", "WebSocket", args);
    return Reflect.construct(target, args, newTarget);
  },
});

// A subprocess could bypass this observer; do not silently treat that as observed work.
for (const name of ["spawn", "spawnSync", "exec", "execSync", "execFile", "execFileSync", "fork"]) {
  observe(childProcess, name, "subprocess", `child_process.${name}`);
}
for (const name of ["spawn", "spawnSync"]) observe(Bun, name, "subprocess", `Bun.${name}`);
// Bun does not synchronize changed default objects into named builtin exports.
// Forwarding module mocks make both import styles use the same observed functions.
for (const [name, object] of [
  ["fs", fs], ["fs/promises", promises], ["net", net], ["http", http], ["https", https],
  ["dgram", dgram], ["tls", tls], ["dns", dns], ["dns/promises", dnsPromises], ["child_process", childProcess],
] as const) {
  for (const specifier of [name, `node:${name}`]) mock.module(specifier, () => ({ ...object, default: object }));
}
