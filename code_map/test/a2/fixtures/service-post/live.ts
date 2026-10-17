import { Effect } from "../effect-runtime";
import { Post } from "./port";

export const postLayer = Effect.fn("Post.layer")(function* () {
  const archive = Effect.fn("Post.archive")(function* (receipt: number) {
    return receipt + 3;
  });

  const stamp = Effect.fn("Post.stamp")(function* (parcel: string) {
    const post = yield* Post.Service;
    return yield* post.archive(parcel.length);
  });

  return Post.of({ stamp, archive });
});
