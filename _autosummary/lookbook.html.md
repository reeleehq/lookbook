# lookbook

lookbook — distill image pools into reference sets for personalized model training.

Public facade. The package is split across:

- `lookbook.base`      — Protocols and core types (Annotation, Manifest)
- `lookbook.store`     — Repository pattern (Stores) over `dol`
- `lookbook.refs`      — ImageRef implementations
- `lookbook.manifest`  — Manifest helpers
- `lookbook.registry`  — Plugin registries (scorers, filters, embedders, selectors)
- `lookbook.pipeline`  — Pipeline orchestrator
- `lookbook.facade`    — curate / score / curate_for_\* entry points
- `lookbook.interactive` — human-in-the-loop curate loop
- `lookbook.scorers`   — Per-image scorer modules (registered on import)
- `lookbook.selectors` — Selector modules (registered on import)
- `lookbook.io`        — Ingest, export

Plugin registries are accessed as `lookbook.registry.scorers` etc. (not
`lookbook.scorers`, which is the submodule that *holds* scorers).

This module only re-exports; it defines nothing of its own — not even a
`from __future__ import annotations`, so `dir(lookbook)` stays the public API
plus the submodules.

### Functions

| [`compare_to_reference`](#lookbook.compare_to_reference)(reference_image, ...[, ...])   | Compare a candidate to a reference in one call → [`SimilarityResult`](#lookbook.SimilarityResult).   |
|------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| [`curate`](#lookbook.curate)(source, \*[, k, scorer_ids, ...])            | High-level facade: ingest a source, run a pipeline, return the result.                                                |
| [`curate_for_character`](#lookbook.curate_for_character)(source, \*[, k, ...])          | Curate the best reference image(s) of a *known* character from a pool.                                                |
| [`curate_for_environment`](#lookbook.curate_for_environment)(source, \*[, k, ...])        | Curate the best reference image(s) for a non-person subject.                                                          |
| [`curate_interactive`](#lookbook.curate_interactive)(source, \*, on_decision[, ...])  | Run the pipeline in rounds, taking keep/reject decisions per round.                                                   |
| [`get_stores`](#lookbook.get_stores)(\*[, root, images_store, ...])           | Build the lookbook Stores bundle.                                                                                     |
| [`ingest`](#lookbook.ingest)(source)                                      | Materialize a source into a list of ImageRefs.                                                                        |
| [`to_local_path`](#lookbook.to_local_path)(ref, \*[, cache_dir])                 | Return a filesystem path where the bytes of `ref` can be read.                                                        |
| [`score`](#lookbook.score)(ref, \*, metric_id[, stores])                 | Score one image against one metric.                                                                                   |
| [`value_of`](#lookbook.value_of)(manifest, image_id, metric_id[, ...])      | Return the bare value of an annotation (not the wrapper), or default.                                                 |

### Classes

| [`Annotation`](#lookbook.Annotation)(image_id, metric_id, value[, ...])     | A single annotation produced by a Scorer or Embedder for one image.     |
|----------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------|
| [`BytesImageRef`](#lookbook.BytesImageRef)(payload[, image_id, metadata])      | An image stored as raw bytes in memory.                                 |
| [`Embedder`](#lookbook.Embedder)(\*args, \*\*kwargs)                      | Computes a vector representation in some named embedding space.         |
| [`Filter`](#lookbook.Filter)(\*args, \*\*kwargs)                        | Predicate over annotations that decides whether to keep an image.       |
| [`IdentitySimilarity`](#lookbook.IdentitySimilarity)([metric_id, cost_tier, ...])   | Score a candidate image's identity-likeness to a locked reference.      |
| [`ImageRef`](#lookbook.ImageRef)(\*args, \*\*kwargs)                      | Anything that knows its identity and how to be opened lazily.           |
| [`PathImageRef`](#lookbook.PathImageRef)(path[, image_id, metadata])          | An image referenced by filesystem path.                                 |
| [`Pipeline`](#lookbook.Pipeline)([scorers, embedders, filters, ...])      | An ordered set of scorers + embedders + filters + a final selector.     |
| [`RunResult`](#lookbook.RunResult)(run_id, kept, candidates, ...[, ...])   | The result of running a pipeline.                                       |
| [`Scorer`](#lookbook.Scorer)(\*args, \*\*kwargs)                        | Computes one annotation per image.                                      |
| [`Selector`](#lookbook.Selector)(\*args, \*\*kwargs)                      | Chooses a subset of size up-to-K from candidates given the manifest.    |
| [`SimilarityResult`](#lookbook.SimilarityResult)(identity_cosine, score, ...)     | Outcome of comparing a candidate against a (possibly pooled) reference. |
| [`Stores`](#lookbook.Stores)(images, manifest, runs, embeddings[, ...]) | Bundle of all stores lookbook uses for persistence.                     |
| [`UrlImageRef`](#lookbook.UrlImageRef)(url[, image_id, metadata, \_cached])  | An image referenced by URL.                                             |
| [`InteractiveDecision`](#lookbook.InteractiveDecision)(\*[, keep, reject, stop])     | One round's verdict from the caller.                                    |

### *class* lookbook.Annotation(image_id, metric_id, value, config_hash='', cost_tier=0, timestamp=\_utcnow(), backend='')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

A single annotation produced by a Scorer or Embedder for one image.

The (image_id, metric_id) pair is the manifest key. `config_hash` is the
cache key — re-running with the same config yields a cache hit; changing
a threshold or model invalidates.

#### *property* key *: [Tuple](https://docs.python.org/3/library/typing.html#typing.Tuple)[[str](https://docs.python.org/3/builtins/stdtypes.html#str), [str](https://docs.python.org/3/builtins/stdtypes.html#str)]*

The image’s manifest key.

### *class* lookbook.BytesImageRef(payload, image_id='', metadata=dict())

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

An image stored as raw bytes in memory.

#### bytes()

Return the raw image bytes.

* **Return type:**
  [`bytes`](#lookbook.BytesImageRef.bytes)

#### local_path(, cache_dir=None)

Materialize the bytes into a file (cached by image_id).

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

#### open()

Open the image (a PIL image).

### *class* lookbook.Embedder(\*args, \*\*kwargs)

Bases: [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)

Computes a vector representation in some named embedding space.

#### embed(ref)

Embed `ref` into this embedder’s vector space.

* **Return type:**
  [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)

### *class* lookbook.Filter(\*args, \*\*kwargs)

Bases: [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)

Predicate over annotations that decides whether to keep an image.

#### keep(ref, manifest)

Return whether `ref` passes this filter.

* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)

### *class* lookbook.IdentitySimilarity(metric_id='identity_similarity', cost_tier=2, requires=(), backend='lookbook:identity_similarity', reference_embedding=None, reference_image=None, reference_images=None, embedder='arcface', threshold=0.85, aggregation='max', normalization='rescale')

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
[`SimilarityResult.as_dict()`](#lookbook.SimilarityResult.as_dict)) so it persists through the manifest’s
default codec. Use [`compare_to_reference()`](#lookbook.compare_to_reference) for a one-call facade that
returns the typed [`SimilarityResult`](#lookbook.SimilarityResult).

#### compare(ref)

Compare one candidate ref against the reference; typed result.

* **Return type:**
  [`SimilarityResult`](lookbook.scorers.identity.html.md#lookbook.scorers.identity.SimilarityResult)

#### *property* config_hash *: [str](https://docs.python.org/3/builtins/stdtypes.html#str)*

changes whenever a setting that affects its output changes.

* **Type:**
  Cache key for this component

#### score(ref, manifest)

Scorer-protocol entry point — returns the JSON-able result dict.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### *class* lookbook.ImageRef(\*args, \*\*kwargs)

Bases: [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)

Anything that knows its identity and how to be opened lazily.

#### bytes()

Return the raw image bytes.

* **Return type:**
  [`bytes`](#lookbook.ImageRef.bytes)

#### open()

Open the image (a PIL image).

* **Return type:**
  [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)

### *class* lookbook.InteractiveDecision(, keep=(), reject=(), stop=False)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

One round’s verdict from the caller.

#### keep

```
``
```

image_id\`\`s the caller wants to lock into the final
selection. They’re added immediately, removed from the
candidate pool, and not shown again.

* **Type:**
  [`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`...`](https://docs.python.org/3/builtins/constants.html#Ellipsis)]

#### reject

```
``
```

image_id\`\`s the caller never wants to see again in
this run.

* **Type:**
  [`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`...`](https://docs.python.org/3/builtins/constants.html#Ellipsis)]

#### stop

When True, the loop terminates after applying this
round’s keep/reject and returns whatever is in the
confirmed-kept set so far (clipped to `k`).

* **Type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)

### *class* lookbook.PathImageRef(path, image_id='', metadata=dict())

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

An image referenced by filesystem path.

#### bytes()

Return the raw image bytes.

* **Return type:**
  [`bytes`](#lookbook.PathImageRef.bytes)

#### local_path(, cache_dir=None)

Return the existing on-disk path. `cache_dir` is ignored.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

#### open()

Open the image (a PIL image).

### *class* lookbook.Pipeline(scorers=list(), embedders=list(), filters=list(), selector=None, diagnose_clusters=0)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

An ordered set of scorers + embedders + filters + a final selector.

#### run(candidates, , k, stores=None, constraints=None, run_id=None)

Score, embed, filter, and select.

`stores` defaults to in-memory. Pass `get_stores()` for the user’s
app data folder defaults.

* **Return type:**
  [`RunResult`](lookbook.pipeline.html.md#lookbook.pipeline.RunResult)

### *class* lookbook.RunResult(run_id, kept, candidates, selector_id, scorer_ids, started_at, finished_at, report=dict())

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

The result of running a pipeline.

#### to_record()

Return the run as a JSON-serialisable dict.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### *class* lookbook.Scorer(\*args, \*\*kwargs)

Bases: [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)

Computes one annotation per image. Idempotent w.r.t. config_hash.

#### score(ref, manifest)

Score `ref`; the result is stored in the manifest under this scorer’s id.

* **Return type:**
  [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)

### *class* lookbook.Selector(\*args, \*\*kwargs)

Bases: [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)

Chooses a subset of size up-to-K from candidates given the manifest.

#### select(candidates, manifest, k, constraints=None)

Choose the images to keep from the scored candidates.

* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`ImageRef`](lookbook.base.html.md#lookbook.base.ImageRef)]

### *class* lookbook.SimilarityResult(identity_cosine, score, passed, threshold, per_reference=tuple(), aggregation='max', n_references=0)

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

### *class* lookbook.Stores(images, manifest, runs, embeddings, root=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Bundle of all stores lookbook uses for persistence.

### *class* lookbook.UrlImageRef(url, image_id='', metadata=dict(), \_cached=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

An image referenced by URL.

The bytes are fetched on first access and cached on the instance.

#### bytes()

Return the raw image bytes.

* **Return type:**
  [`bytes`](#lookbook.UrlImageRef.bytes)

#### local_path(, cache_dir=None)

Download (once) and return the local path.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

#### open()

Open the image (a PIL image).

### lookbook.compare_to_reference(reference_image, candidate_image, , embedder='arcface', threshold=0.85, aggregation='max', normalization='rescale')

Compare a candidate to a reference in one call → [`SimilarityResult`](#lookbook.SimilarityResult).

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
  [`SimilarityResult`](lookbook.scorers.identity.html.md#lookbook.scorers.identity.SimilarityResult)

### lookbook.curate(source, , k=20, scorer_ids=('random_score',), embedder_ids=(), filter_ids=(), selector_id='top_k', diagnose_clusters=0, stores=None, constraints=None)

High-level facade: ingest a source, run a pipeline, return the result.

Each plugin id may be either a string (“blur”) or a (name, kwargs)
tuple ((“blur”, {“max_side”: 256})) to override the default config.

`diagnose_clusters > 0` runs cluster-coverage diagnosis after selection
and writes the result into the report’s `notes`.

* **Return type:**
  [`RunResult`](lookbook.pipeline.html.md#lookbook.pipeline.RunResult)

### lookbook.curate_for_character(source, , k=1, face_detector='insightface', stores=None, constraints=None)

Curate the best reference image(s) of a *known* character from a pool.

Opinionated facade over [`curate()`](#lookbook.curate), tuned for the “pick the
reference image of this one character” job (IP-adapter conditioning,
model-sheet seeding): every image is scored for resolution, sharpness,
exposure and face quality, then the top `k` are taken by the
composite `face_quality` metric.

Identity is *not* scored — the pool is assumed to already be one
character, so what matters is which frame shows them most usably: in
focus, well exposed, face clearly visible and well sized. To check
whether a *generation* still matches a locked reference, use
[`lookbook.compare_to_reference()`](#lookbook.compare_to_reference) instead.

`face_detector` names the registered face-box scorer:

- `"insightface"` — real RetinaFace detection; needs
  `pip install lookbook[person]`. The default.
- `"mock_face"` — the deterministic centred-box detector, for tests
  and demos without the ML dependency.

Images with no detected face score `0` and sort last; the pool is
never filtered down to empty, so a small or awkward pool still yields
a best-effort pick.

* **Return type:**
  [`RunResult`](lookbook.pipeline.html.md#lookbook.pipeline.RunResult)

### lookbook.curate_for_environment(source, , k=1, stores=None, constraints=None)

Curate the best reference image(s) for a non-person subject.

Opinionated facade over [`curate()`](#lookbook.curate) for pools where face detection
is moot — environment plates, prop references, style boards. Each
image is scored for resolution, sharpness and exposure, folded into
the composite `technical_quality` metric, and the top `k` are
taken.

Unlike [`curate_for_character()`](#lookbook.curate_for_character) this needs no ML dependency — the
scorers run on Pillow + numpy (cv2 is used for sharpness when present,
with a numpy fallback otherwise).

* **Return type:**
  [`RunResult`](lookbook.pipeline.html.md#lookbook.pipeline.RunResult)

### lookbook.curate_interactive(source, , on_decision, k=20, present=8, max_rounds=20, scorer_ids=('random_score',), embedder_ids=(), filter_ids=(), selector_id='top_k', stores=None, constraints=None)

Run the pipeline in rounds, taking keep/reject decisions per round.

Args mirror [`lookbook.curate()`](#lookbook.curate) plus:

* **Parameters:**
  * **on_decision** ([`Union`](https://docs.python.org/3/library/typing.html#typing.Union)[[`Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)[[[`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`ImageRef`](lookbook.base.html.md#lookbook.base.ImageRef)], [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]], [`InteractiveDecision`](lookbook.interactive.html.md#lookbook.interactive.InteractiveDecision)], [`Sequence`](https://docs.python.org/3/library/typing.html#typing.Sequence)[[`InteractiveDecision`](lookbook.interactive.html.md#lookbook.interactive.InteractiveDecision)]]) – A callable or a pre-recorded sequence of
    [`InteractiveDecision`](#lookbook.InteractiveDecision). The callable receives the
    round’s top candidates and an info dict
    `{round, n_kept_so_far, n_pool_remaining}`.
  * **present** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – How many candidates to surface per round.
  * **max_rounds** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Hard cap on iterations; a defensive guard against
    broken decision callables that never stop.
* **Return type:**
  [`RunResult`](lookbook.pipeline.html.md#lookbook.pipeline.RunResult)
* **Returns:**
  A [`RunResult`](#lookbook.RunResult) whose `kept` list is the confirmed
  set (in the order they were kept). `candidates` carries the
  same as the final round’s pre-selection candidate pool.

### lookbook.get_stores(, root=None, images_store=None, manifest_store=None, runs_store=None, embeddings=None)

Build the lookbook Stores bundle.

All arguments are optional. When `root` is None and no stores are
supplied, the user’s app data folder is used. Pass `dict()` for any
slot to keep that store in memory (useful for tests).

```pycon
>>> stores = get_stores(
...     images_store={}, manifest_store={}, runs_store={}, embeddings={}
... )
>>> stores.manifest is not None
True
```

* **Return type:**
  [`Stores`](lookbook.store.html.md#lookbook.store.Stores)

### lookbook.ingest(source)

Materialize a source into a list of ImageRefs.

```pycon
>>> import tempfile, os
>>> with tempfile.TemporaryDirectory() as d:
...     for name in ['a.jpg', 'b.png', 'note.txt']:
...         open(os.path.join(d, name), 'wb').close()
...     refs = ingest(d)
>>> sorted(os.path.basename(r.path) for r in refs)
['a.jpg', 'b.png']
```

* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`ImageRef`](lookbook.base.html.md#lookbook.base.ImageRef)]

### lookbook.score(ref, , metric_id, stores=None)

Score one image against one metric. Returns the bare value.

Caches into the manifest so repeated calls are free.

* **Return type:**
  [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)

### lookbook.to_local_path(ref, , cache_dir=None)

Return a filesystem path where the bytes of `ref` can be read.

Works on any object that exposes `.local_path(cache_dir)` — i.e.
every concrete `ImageRef` shipped with lookbook. Provided as a
free function so downstream code doesn’t need to know which subtype
it has.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

### lookbook.value_of(manifest, image_id, metric_id, default=None)

Return the bare value of an annotation (not the wrapper), or default.

* **Return type:**
  [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)

### Modules

| [`registry`](lookbook.registry.html.md#module-lookbook.registry)       | Plugin registry for scorers, filters, embedders, selectors.        |
|------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| [`base`](lookbook.base.html.md#module-lookbook.base)               | Core protocols and types for lookbook.                             |
| [`diagnose`](lookbook.diagnose.html.md#module-lookbook.diagnose)       | Set-level diagnosis: what does the kept set cover, what's missing. |
| [`embedders`](lookbook.embedders.html.md#module-lookbook.embedders)     | Embedders: vector representations per image.                       |
| [`facade`](lookbook.facade.html.md#module-lookbook.facade)           | High-level facades — the one-call entry points into the pipeline.  |
| [`filters`](lookbook.filters.html.md#module-lookbook.filters)         | Filters: per-image keep/drop decisions.                            |
| [`http`](lookbook.http.html.md#module-lookbook.http)               | HTTP surface for lookbook, built with `qh` over FastAPI.           |
| [`interactive`](lookbook.interactive.html.md#module-lookbook.interactive) | Interactive curate loop — keep the human in the loop.              |
| [`io`](lookbook.io.html.md#module-lookbook.io)                   | IO: ingest sources into ImageRefs, export results to disk.         |
| [`manifest`](lookbook.manifest.html.md#module-lookbook.manifest)       | Helpers for reading and writing the manifest.                      |
| [`mcp`](lookbook.mcp.html.md#module-lookbook.mcp)                 | MCP surface for lookbook, built with `fastmcp`.                    |
| [`pipeline`](lookbook.pipeline.html.md#module-lookbook.pipeline)       | Pipeline orchestrator.                                             |
| [`profiles`](lookbook.profiles.html.md#module-lookbook.profiles)       | Subject profiles — declarative recipes loaded from YAML.           |
| [`refs`](lookbook.refs.html.md#module-lookbook.refs)               | Concrete `ImageRef` implementations.                               |
| [`report`](lookbook.report.html.md#module-lookbook.report)           | Run report — what happened during a curation pass.                 |
| [`scorers`](lookbook.scorers.html.md#module-lookbook.scorers)         | Scorers: per-image annotation producers.                           |
| [`selectors`](lookbook.selectors.html.md#module-lookbook.selectors)     | Selectors: choose K from N given the manifest.                     |
| [`store`](lookbook.store.html.md#module-lookbook.store)             | Repository pattern for lookbook persistence.                       |
