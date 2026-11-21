# lookbook.embedders.clip

CLIP embedder via `transformers`.

CLIP is the right embedding for *semantic* similarity (same concept, different
style). It’s also what LAION-Aesthetic-V2 and CLIP-IQA both consume, so when
those scorers land they can share the cached features computed here.

### Classes

| [`CLIPEmbedder`](#lookbook.embedders.clip.CLIPEmbedder)([space_id, cost_tier, ...])   | OpenAI CLIP image embeddings via HuggingFace transformers.   |
|---------------------------------------------------------------------------------------------|--------------------------------------------------------------|

### *class* lookbook.embedders.clip.CLIPEmbedder(space_id='clip_vit_b32', cost_tier=2, model_name='openai/clip-vit-base-patch32', device=None, backend='transformers:clip')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

OpenAI CLIP image embeddings via HuggingFace transformers.

Defaults to ViT-B/32 (~150 MB, fast enough for CPU). Use ViT-L/14 by
setting `model_name="openai/clip-vit-large-patch14"` for higher-quality
semantic embeddings (slower, ~600 MB).
