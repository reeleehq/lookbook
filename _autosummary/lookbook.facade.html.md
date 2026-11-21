# lookbook.facade

High-level facades — the one-call entry points into the pipeline.

`curate` is the general one: ingest a source, run scorers/embedders/filters,
select K. `curate_for_character` and `curate_for_environment` are opinionated
presets over it, and `score` is the single-image, single-metric shortcut.

Everything here is re-exported from `lookbook`, which is where callers should
import it from. Plugins are named, never subclassed: each `*_ids` argument
takes registry names, optionally paired with config overrides as a
`(name, kwargs)` tuple.

### Functions

| [`curate`](#lookbook.facade.curate)(source, \*[, k, scorer_ids, ...])     | High-level facade: ingest a source, run a pipeline, return the result.   |
|-----------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|
| [`curate_for_character`](#lookbook.facade.curate_for_character)(source, \*[, k, ...])   | Curate the best reference image(s) of a *known* character from a pool.   |
| [`curate_for_environment`](#lookbook.facade.curate_for_environment)(source, \*[, k, ...]) | Curate the best reference image(s) for a non-person subject.             |
| [`resolve_plugin`](#lookbook.facade.resolve_plugin)(reg, spec, \*[, fresh])       | Look up a plugin from a registry, optionally with config overrides.      |
| [`score`](#lookbook.facade.score)(ref, \*, metric_id[, stores])          | Score one image against one metric.                                      |

### lookbook.facade.curate(source, , k=20, scorer_ids=('random_score',), embedder_ids=(), filter_ids=(), selector_id='top_k', diagnose_clusters=0, stores=None, constraints=None)

High-level facade: ingest a source, run a pipeline, return the result.

Each plugin id may be either a string (“blur”) or a (name, kwargs)
tuple ((“blur”, {“max_side”: 256})) to override the default config.

`diagnose_clusters > 0` runs cluster-coverage diagnosis after selection
and writes the result into the report’s `notes`.

* **Return type:**
  [`RunResult`](lookbook.pipeline.html.md#lookbook.pipeline.RunResult)

### lookbook.facade.curate_for_character(source, , k=1, face_detector='insightface', stores=None, constraints=None)

Curate the best reference image(s) of a *known* character from a pool.

Opinionated facade over [`curate()`](#lookbook.facade.curate), tuned for the “pick the
reference image of this one character” job (IP-adapter conditioning,
model-sheet seeding): every image is scored for resolution, sharpness,
exposure and face quality, then the top `k` are taken by the
composite `face_quality` metric.

Identity is *not* scored — the pool is assumed to already be one
character, so what matters is which frame shows them most usably: in
focus, well exposed, face clearly visible and well sized. To check
whether a *generation* still matches a locked reference, use
[`lookbook.compare_to_reference()`](lookbook.html.md#lookbook.compare_to_reference) instead.

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

### lookbook.facade.curate_for_environment(source, , k=1, stores=None, constraints=None)

Curate the best reference image(s) for a non-person subject.

Opinionated facade over [`curate()`](#lookbook.facade.curate) for pools where face detection
is moot — environment plates, prop references, style boards. Each
image is scored for resolution, sharpness and exposure, folded into
the composite `technical_quality` metric, and the top `k` are
taken.

Unlike [`curate_for_character()`](#lookbook.facade.curate_for_character) this needs no ML dependency — the
scorers run on Pillow + numpy (cv2 is used for sharpness when present,
with a numpy fallback otherwise).

* **Return type:**
  [`RunResult`](lookbook.pipeline.html.md#lookbook.pipeline.RunResult)

### lookbook.facade.resolve_plugin(reg, spec, , fresh=False)

Look up a plugin from a registry, optionally with config overrides.

`spec` is either a registered name or a `(name, kwargs)` tuple. With
`fresh=True` (used for filters with internal state), returns a brand
new instance even when no overrides are given.

### lookbook.facade.score(ref, , metric_id, stores=None)

Score one image against one metric. Returns the bare value.

Caches into the manifest so repeated calls are free.

* **Return type:**
  [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)
