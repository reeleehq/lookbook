# lookbook.embedders.dinov2

DINOv2 embedder via `transformers`.

DINOv2 is the right embedding for *visual* similarity (same scene/object,
robust to style). Voxel51’s benchmarks show it outperforming CLIP on image
classification by 5-28 points on natural-image datasets. For curation, that
makes it the better default for “find redundant shots.”

### Classes

| [`DINOv2Embedder`](#lookbook.embedders.dinov2.DINOv2Embedder)([space_id, cost_tier, ...])   | Facebook DINOv2 image embeddings via HuggingFace transformers.   |
|-----------------------------------------------------------------------------------------------|------------------------------------------------------------------|

### *class* lookbook.embedders.dinov2.DINOv2Embedder(space_id='dinov2_base', cost_tier=2, model_name='facebook/dinov2-base', device=None, backend='transformers:dinov2')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Facebook DINOv2 image embeddings via HuggingFace transformers.

Defaults to ViT-B/14 (~350 MB). Use `facebook/dinov2-small` for
smaller-but-weaker (~85 MB), `facebook/dinov2-large` for stronger
(~1.2 GB).

#### *property* config_hash *: [str](https://docs.python.org/3/builtins/stdtypes.html#str)*

changes whenever a setting that affects its output changes.

* **Type:**
  Cache key for this component

#### embed(ref)

Embed `ref` into this embedder’s vector space.

* **Return type:**
  `ndarray`
