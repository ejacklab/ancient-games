import { Context, type Task } from "../effect-runtime";

export interface PostApi {
  readonly stamp: (parcel: string) => Task<number>;
  readonly archive: (receipt: number) => Task<number>;
}

export class Post extends Context.Service<Post, PostApi>()("@fixture/Post") {}
