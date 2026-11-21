# lookbook.scorers.identity

Cross-image identity / likeness scorer — compare a candidate to a reference.

Every scorer in [`lookbook.scorers`](lookbook.scorers.html.md#module-lookbook.scorers) rates a *single* image’s technical or
face quality. This module adds the missing primitive: a scorer that **compares**
a candidate image against a locked **reference** (or a pool of references) and
returns an identity-similarity number in `[0, 1]` (1 = same identity).

This is the measurement substrate for a “reference supervisor” — answering
 *“does this generation still match the locked reference?”* with a number a
caller can gate on. It reuses lookbook’s existing embedders unchanged:

- `arcface` (InsightFace `buffalo_l`) for **face identity** — the default;
  neither CLIP nor DINOv2 reliably says “same person”.
- `clip` / `dinov2` for **non-face subjects** (locations, architecture,
  props) — injected via the same `embedder=` seam.

## Design notes

- **The embedder is injected, never hard-wired.** [`IdentitySimilarity`](#lookbook.scorers.identity.IdentitySimilarity)
  accepts an [`Embedder`](lookbook.base.html.md#lookbook.base.Embedder), a registry name (resolved
  lazily), or a bare `embed_fn(ref) -> vector` callable. This keeps the heavy
  ML deps (torch / insightface) behind lookbook’s usual lazy boundary —
  importing this module pulls in nothing heavy — and makes the cosine math
  unit-testable with a fake embedder returning known vectors.
- **The reference is embedded once.** Pass a precomputed `reference_embedding`
  (a single vector or a stacked array of vectors for a pool), or a reference
  image / list of images that the scorer embeds **once at construction** and
  caches. Candidates are never made to pay for re-embedding the reference.
- **Set aggregation** is explicit: when the reference is a pool, the per-view
  similarities are aggregated by `aggregation` (default `"max"` — “matches
  *any* locked view”, the right default for a supervisor; `"mean"` is the
  stricter “matches the *average* view”).
- The result carries a `passed` flag against an injectable `threshold`.
  This is **advisory** — the consumer (e.g. reelee’s reference supervisor)
  decides whether to hard-block. Nothing here raises on a low score.

### Module Attributes

| [`DFLT_THRESHOLD`](#lookbook.scorers.identity.DFLT_THRESHOLD)     | Default normalized-similarity threshold for the advisory pass/fail gate.   |
|---------------------------------------------------------------------|----------------------------------------------------------------------------|
| [`DFLT_EMBEDDER`](#lookbook.scorers.identity.DFLT_EMBEDDER)      | Default embedder used when none is injected.                               |
| [`DFLT_AGGREGATION`](#lookbook.scorers.identity.DFLT_AGGREGATION)   | How to fold a pool of per-reference similarities into one number.          |
| [`DFLT_NORMALIZATION`](#lookbook.scorers.identity.DFLT_NORMALIZATION) | How to map a cosine in `[-1, 1]` onto `[0, 1]`.                            |
| [`METRIC_ID`](#lookbook.scorers.identity.METRIC_ID)          | The metric_id this scorer writes to the manifest.                          |

### Functions

| [`compare_to_reference`](#lookbook.scorers.identity.compare_to_reference)(reference_image, ...[, ...])   | Compare a candidate to a reference in one call → [`SimilarityResult`](#lookbook.scorers.identity.SimilarityResult).   |
|------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| [`cosine_similarity`](#lookbook.scorers.identity.cosine_similarity)(u, v)                             | Cosine similarity in `[-1, 1]` between two vectors.                                                                   |
| [`normalize_cosine`](#lookbook.scorers.identity.normalize_cosine)(cosine, \*[, normalization])       | Map a cosine in `[-1, 1]` onto `[0, 1]` (1 = identical direction).                                                    |

### Classes

| [`IdentitySimilarity`](#lookbook.scorers.identity.IdentitySimilarity)([metric_id, cost_tier, ...])   | Score a candidate image's identity-likeness to a locked reference.      |
|----------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------|
| [`SimilarityResult`](#lookbook.scorers.identity.SimilarityResult)(identity_cosine, score, ...)     | Outcome of comparing a candidate against a (possibly pooled) reference. |

### lookbook.scorers.identity.DFLT_AGGREGATION *: [str](https://docs.python.org/3/builtins/stdtypes.html#str)* *= 'max'*

How to fold a pool of per-reference similarities into one number.

### lookbook.scorers.identity.DFLT_EMBEDDER *: [str](https://docs.python.org/3/builtins/stdtypes.html#str)* *= 'arcface'*

Default embedder used when none is injected. `"arcface"` is the identity
space; swap for `"clip"` / `"dinov2"` for non-face subjects.

### lookbook.scorers.identity.DFLT_NORMALIZATION *: [str](https://docs.python.org/3/builtins/stdtypes.html#str)* *= 'rescale'*

How to map a cosine in `[-1, 1]` onto `[0, 1]`.

- `"rescale"`: `(cos + 1) / 2` — order-preserving over the full range;
  the safe default for any embedder (CLIP/DINOv2 cosines can go negative).
- `"clamp"`: `max(0, cos)` — for L2-normalized identity spaces where a
  negative cosine just means “unrelated” and should floor at 0.

### lookbook.scorers.identity.DFLT_THRESHOLD *: [float](https://docs.python.org/3/builtins/functions.html#float)* *= 0.85*

Default normalized-similarity threshold for the advisory pass/fail gate.
On the `[0, 1]` scale (1 = same identity). 0.85 mirrors the common
ArcFace “same person” operating point; owner-tunable per call.

### *class* lookbook.scorers.identity.IdentitySimilarity(metric_id='identity_similarity', cost_tier=2, requires=(), backend='lookbook:identity_similarity', reference_embedding=None, reference_image=None, reference_images=None, embedder='arcface', threshold=0.85, aggregation='max', normalization='rescale')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Score a candidate image’s identity-likeness to a locked reference.

Unlike the single-image scorers, this one is **stateful by reference**:
it holds the reference embedding(s) and compares each candidate against
them. Construct one per locked subject, then `score` every generation.

Construction (provide exactly one of the reference inputs):

- `reference_embedding` — a precomputed vector (1-D) or pool (2-D /
  sequence of vectors). Cheapest; the reference is never re-embedded.
- `reference_image` — a single [`ImageRef`](lookbook.base.html.md#lookbook.base.ImageRef) (or
  anything the injected embedder accepts), embedded **once** at
  construction and cached.
- `reference_images` — a pool of refs, each embedded once.

Parameters (keyword-only past the embedder seam):

- `embedder` — registry name (`"arcface"` default), an `Embedder`
  object, or a bare `embed_fn(ref) -> vector` callable. Injectable so
  tests pass a fake embedder and non-face subjects pass `"clip"` /
  `"dinov2"`.
- `threshold` — advisory pass/fail cutoff on the `[0, 1]` scale.
- `aggregation` — `"max"` (default) | `"mean"` | `"min"` over the
  reference pool.
- `normalization` — cosine → `[0, 1]` map; see `DFLT_NORMALIZATION`.

The `score(ref, manifest)` method returns a JSON-able dict (see
[`SimilarityResult.as_dict()`](#lookbook.scorers.identity.SimilarityResult.as_dict)) so it persists through the manifest’s
default codec. Use [`compare_to_reference()`](#lookbook.scorers.identity.compare_to_reference) for a one-call facade that
returns the typed [`SimilarityResult`](#lookbook.scorers.identity.SimilarityResult).

#### compare(ref)

Compare one candidate ref against the reference; typed result.

* **Return type:**
  [`SimilarityResult`](#lookbook.scorers.identity.SimilarityResult)

#### score(ref, manifest)

Scorer-protocol entry point — returns the JSON-able result dict.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### lookbook.scorers.identity.METRIC_ID *: [str](https://docs.python.org/3/builtins/stdtypes.html#str)* *= 'identity_similarity'*

The metric_id this scorer writes to the manifest.

### *class* lookbook.scorers.identity.SimilarityResult(identity_cosine, score, passed, threshold, per_reference=tuple(), aggregation='max', n_references=0)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Outcome of comparing a candidate against a (possibly pooled) reference.

#### identity_cosine

The aggregated **raw cosine** in `[-1, 1]` (pre-normalization). The
`identity_cosine` name is kept for the supervisor’s vocabulary even
when the embedder is CLIP/DINOv2 — it is the cosine in whatever space
the embedder defines.

* **Type:**
  [`float`](https://docs.python.org/3/builtins/functions.html#float)

#### score

The aggregated similarity normalized to `[0, 1]` (1 = same identity).
This is what the gate compares against `threshold`.

* **Type:**
  [`float`](https://docs.python.org/3/builtins/functions.html#float)

#### passed

`score >= threshold`. **Advisory only** — the consumer decides
whether to act on it.

* **Type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)

#### threshold

The threshold used for `passed` (on the `[0, 1]` scale).

* **Type:**
  [`float`](https://docs.python.org/3/builtins/functions.html#float)

#### per_reference

The per-reference normalized similarities before aggregation. Length
is the size of the reference pool. Lets callers see *which* locked view
matched (e.g. `argmax` for `aggregation="max"`).

* **Type:**
  [`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`float`](https://docs.python.org/3/builtins/functions.html#float), [`...`](https://docs.python.org/3/builtins/constants.html#Ellipsis)]

#### aggregation

The aggregation applied over `per_reference`.

* **Type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

#### n_references

Size of the reference pool.

* **Type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)

#### as_dict()

JSON-able view (what the scorer writes to the manifest).

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### lookbook.scorers.identity.compare_to_reference(reference_image, candidate_image, , embedder='arcface', threshold=0.85, aggregation='max', normalization='rescale')

Compare a candidate to a reference in one call → [`SimilarityResult`](#lookbook.scorers.identity.SimilarityResult).

The supervisor’s headline verb. `reference_image` may be a single image
ref or a **pool** (any sequence of refs) — the pool is embedded once and
folded by `aggregation`. `candidate_image` is a single ref.

All inputs are whatever the injected `embedder` accepts — typically an
[`ImageRef`](lookbook.base.html.md#lookbook.base.ImageRef), but with a fake/callable embedder they
can be anything (tests pass plain ids).

* **Parameters:**
  * **embedder** ([`Union`](https://docs.python.org/3/library/typing.html#typing.Union)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), Embedder, [`Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)[[[`ImageRef`](lookbook.base.html.md#lookbook.base.ImageRef)], [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]]) – Registry name (`"arcface"` default for faces; `"clip"` / `"dinov2"`
    for scenes/architecture), an `Embedder` object, or a bare
    `embed_fn(x) -> vector` callable.
  * **threshold** ([`float`](https://docs.python.org/3/builtins/functions.html#float)) – Advisory pass/fail cutoff on the `[0, 1]` scale (1 = same identity).
  * **aggregation** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – How to fold a reference pool — `"max"` (default), `"mean"`, `"min"`.
  * **normalization::** – Cosine → `[0, 1]` map — `"rescale"` (default) or `"clamp"`.
* **Returns:**
  `.score` (∈ `[0, 1]`), `.passed` (advisory), `.identity_cosine`
  (raw cosine), and the per-reference breakdown.
* **Return type:**
  [`SimilarityResult`](#lookbook.scorers.identity.SimilarityResult)

### lookbook.scorers.identity.cosine_similarity(u, v)

Cosine similarity in `[-1, 1]` between two vectors.

Safe against unnormalized inputs and zero vectors (returns 0.0 when either
has zero magnitude, which is what a no-face ArcFace embedding yields).

```pycon
>>> cosine_similarity(np.array([1.0, 0.0]), np.array([1.0, 0.0]))
1.0
>>> cosine_similarity(np.array([1.0, 0.0]), np.array([-1.0, 0.0]))
-1.0
>>> cosine_similarity(np.array([1.0, 0.0]), np.array([0.0, 1.0]))
0.0
>>> cosine_similarity(np.array([0.0, 0.0]), np.array([1.0, 0.0]))
0.0
```

* **Return type:**
  [`float`](https://docs.python.org/3/builtins/functions.html#float)

### lookbook.scorers.identity.normalize_cosine(cosine, , normalization='rescale')

Map a cosine in `[-1, 1]` onto `[0, 1]` (1 = identical direction).

```pycon
>>> normalize_cosine(1.0)
1.0
>>> normalize_cosine(-1.0)
0.0
>>> normalize_cosine(0.0)
0.5
>>> normalize_cosine(-0.3, normalization="clamp")
0.0
>>> normalize_cosine(0.6, normalization="clamp")
0.6
```

* **Return type:**
  [`float`](https://docs.python.org/3/builtins/functions.html#float)
