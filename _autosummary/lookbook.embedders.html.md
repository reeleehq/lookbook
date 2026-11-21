# lookbook.embedders

Embedders: vector representations per image.

Each submodule registers its embedders into `lookbook.registry.embedders`
on import. Heavy ML deps must be lazy-imported inside `embed()`, never at
module top.

We pre-set `USE_TF=0` and `USE_FLAX=0` so that `transformers` does not try
to load TensorFlow or Flax — both can blow up if the user’s environment
has an incompatible numpy ABI. `setdefault` means we never override a user
who explicitly wants those backends.

### Modules

| [`arcface`](lookbook.embedders.arcface.html.md#module-lookbook.embedders.arcface)   | ArcFace identity embedder.                                          |
|----------------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| [`clip`](lookbook.embedders.clip.html.md#module-lookbook.embedders.clip)         | CLIP embedder via `transformers`.                                   |
| [`dinov2`](lookbook.embedders.dinov2.html.md#module-lookbook.embedders.dinov2)     | DINOv2 embedder via `transformers`.                                 |
| [`mock`](lookbook.embedders.mock.html.md#module-lookbook.embedders.mock)         | Deterministic mock embedder for tests and end-to-end orchestration. |
