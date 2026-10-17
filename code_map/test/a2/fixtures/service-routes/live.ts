import { Effect } from "../effect-runtime";
import { Routing } from "./port";

export const routingLayer = Effect.fn("Routing.layer")(function* () {
  const launchDetourFirst = Effect.fn("Routing.launchDetourFirst")(function* () {
    const routing = yield* Routing.Service;
    yield* routing.detourFirst();
    yield* routing.sharedDispatch();
    return 23;
  });

  const launchShortcutFirst = Effect.fn("Routing.launchShortcutFirst")(function* () {
    const routing = yield* Routing.Service;
    yield* routing.sharedDispatch();
    yield* routing.detourFirst();
    return 23;
  });

  const detourFirst = Effect.fn("Routing.detourFirst")(function* () {
    const routing = yield* Routing.Service;
    yield* routing.detourSecond();
    return 23;
  });

  const detourSecond = Effect.fn("Routing.detourSecond")(function* () {
    const routing = yield* Routing.Service;
    yield* routing.sharedDispatch();
    return 23;
  });

  const sharedDispatch = Effect.fn("Routing.sharedDispatch")(function* () {
    const routing = yield* Routing.Service;
    yield* routing.recordDispatch();
    return 23;
  });

  const recordDispatch = Effect.fn("Routing.recordDispatch")(function* () {
    const routing = yield* Routing.Service;
    yield* routing.sealDispatch();
    return 23;
  });

  const sealDispatch = Effect.fn("Routing.sealDispatch")(function* () {
    return 23;
  });

  const receiveCenter = Effect.fn("Routing.receiveCenter")(function* () {
    return 23;
  });

  const receiveDetourFirst = Effect.fn("Routing.receiveDetourFirst")(function* () {
    const routing = yield* Routing.Service;
    yield* routing.receiveCenter();
    return 23;
  });

  const receiveDetourSecond = Effect.fn("Routing.receiveDetourSecond")(function* () {
    const routing = yield* Routing.Service;
    yield* routing.receiveDetourFirst();
    return 23;
  });

  const receiveShared = Effect.fn("Routing.receiveShared")(function* () {
    const routing = yield* Routing.Service;
    yield* routing.receiveDetourSecond();
    yield* routing.receiveCenter();
    return 23;
  });

  const receiveAudit = Effect.fn("Routing.receiveAudit")(function* () {
    const routing = yield* Routing.Service;
    yield* routing.receiveShared();
    return 23;
  });

  const receiveArchive = Effect.fn("Routing.receiveArchive")(function* () {
    const routing = yield* Routing.Service;
    yield* routing.receiveAudit();
    return 23;
  });

  return Routing.of({ launchDetourFirst, launchShortcutFirst, detourFirst, detourSecond, sharedDispatch, recordDispatch, sealDispatch, receiveCenter, receiveDetourFirst, receiveDetourSecond, receiveShared, receiveAudit, receiveArchive });
});

