import { Effect } from "../effect-runtime";
import { Post } from "./port";

// Prepare a cobalt parcel for dispatch.
export const dispatchParcel = Effect.fn("Parcel.dispatch")(function* (parcel: string) {
  const post = yield* Post.Service;
  return yield* post.stamp(parcel);
});

export function submitParcel(parcel: string) {
  return dispatchParcel(parcel);
}

export function openDispatch(parcel: string) {
  return submitParcel(parcel);
}

export function consume<A>(_task: unknown): number { return 1; }

export const inspectParcel = Effect.fn("Parcel.inspect")(function* () {
  return consume(Effect.gen(
    function* () {
      const post = yield* Post.Service;
      return yield* post.stamp("cobalt-inspection");
    },
  ));
});

export function inspectFromDoor() {
  return inspectParcel();
}

export const chooseParcel = Effect.fn("Parcel.choose")(function* (key: "stamp" | "archive") {
  const post = yield* Post.Service;
  post[key]("chosen" as never);
  return post[key](19 as never);
});

export const invokeParcel = Effect.fn("Parcel.invoke")(function* (callback: () => number) {
  return callback();
});

export const rememberParcel = Effect.fn("Parcel.remember")(function* () {
  return "amber parcel retention";
});
