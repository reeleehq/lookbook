# lookbook.embedders.mock

Deterministic mock embedder for tests and end-to-end orchestration.

`MockEmbedder` returns a vector seeded by `image_id`, so the same image
always yields the same vector and similar 

```
`
```

image_id\`s yield similar
vectors (a tiny bit). It does not require any ML dependency.

### Classes

| [`MockEmbedder`](#lookbook.embedders.mock.MockEmbedder)([space_id, cost_tier, dim, ...])   | Deterministic, dependency-free embedder for tests.   |
|--------------------------------------------------------------------------------------------------|------------------------------------------------------|

### *class* lookbook.embedders.mock.MockEmbedder(space_id='mock', cost_tier=0, dim=64, seed=0, backend='lookbook:mock')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Deterministic, dependency-free embedder for tests.

The vector is derived from a SHA1 of `image_id` (mixed with `seed`),
expanded to `dim` dimensions, and L2-normalized.
