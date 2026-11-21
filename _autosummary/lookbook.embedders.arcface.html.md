# lookbook.embedders.arcface

ArcFace identity embedder.

ArcFace embeddings are the standard for face *identity* verification —
neither CLIP nor DINOv2 reliably tells you “this is the same person.”
For character-LoRA curation that’s the load-bearing question.

`InsightFaceArcFace` shares the underlying model weights with
`InsightFaceDetect` (both go through the `FaceAnalysis` app). The
embedder reads the `face_box` annotation from the manifest to know where
to crop, then runs ArcFace on that crop.

### Classes

| [`InsightFaceArcFace`](#lookbook.embedders.arcface.InsightFaceArcFace)([space_id, cost_tier, ...])   | Real ArcFace embeddings via insightface.       |
|---------------------------------------------------------------------------------------------------|------------------------------------------------|
| [`MockArcFaceEmbedder`](#lookbook.embedders.arcface.MockArcFaceEmbedder)([space_id, cost_tier, ...])  | Deterministic mock identity embedder, no deps. |

### *class* lookbook.embedders.arcface.InsightFaceArcFace(space_id='arcface', cost_tier=2, model_name='buffalo_l', det_size=640, backend='insightface:arcface')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Real ArcFace embeddings via insightface.

The implementation is intentionally a thin wrapper. `insightface`’s
`FaceAnalysis.get(img)` returns Face objects with `.embedding` already
L2-normalized; we just pick the largest face’s embedding.

The “right” face is the one whose `bbox` overlaps the manifest’s
`face_box` if available; otherwise the largest by area.

### *class* lookbook.embedders.arcface.MockArcFaceEmbedder(space_id='arcface_mock', cost_tier=1, dim=512, seed=0, backend='lookbook:mock_arcface')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Deterministic mock identity embedder, no deps.

The vector is keyed by `image_id`, so:

- Same image always yields the same vector.
- Different images yield different vectors.
- There is no “same person” signal — different images of one person
  get unrelated vectors. Useful only for orchestration tests.
