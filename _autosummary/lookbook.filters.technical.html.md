# lookbook.filters.technical

Phase 1 filters — cheap funnel.

Filters consume the manifest and return True/False per image. Two of them
(`NoExactDuplicate`, `NoNearDuplicate`) carry per-pipeline state and must
be re-instantiated for each new run; the rest are stateless.

Each filter exposes a `name` attribute (the filter id) so the run report
can attribute drops back to the rule that fired.

### Functions

| [`fresh_filter`](#lookbook.filters.technical.fresh_filter)(filter_id, \*\*overrides)   | Return a fresh instance of a registered filter.   |
|-------------------------------------------------------------------------------------------|---------------------------------------------------|

### Classes

| [`ExposureRange`](#lookbook.filters.technical.ExposureRange)([max_underexposed_frac, ...])   | Drop images that are mostly black or mostly white.                  |
|------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| [`MinBlur`](#lookbook.filters.technical.MinBlur)([threshold, name])                    | Drop images whose Laplacian variance is below `threshold` (blurry). |
| [`MinResolution`](#lookbook.filters.technical.MinResolution)([min_long_side, name])          | Drop images whose long side is below `min_long_side` pixels.        |
| [`NoExactDuplicate`](#lookbook.filters.technical.NoExactDuplicate)([name, \_seen])              | Keep at most one image per `file_hash`.                             |
| [`NoNearDuplicate`](#lookbook.filters.technical.NoNearDuplicate)([max_distance, name, ...])    | Keep at most one image per near-duplicate cluster.                  |

### *class* lookbook.filters.technical.ExposureRange(max_underexposed_frac=0.5, max_overexposed_frac=0.5, name='exposure_range')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Drop images that are mostly black or mostly white.

Defaults: drop if more than 50% of pixels are below 16 or above 240.

### *class* lookbook.filters.technical.MinBlur(threshold=100.0, name='min_blur')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Drop images whose Laplacian variance is below `threshold` (blurry).

### *class* lookbook.filters.technical.MinResolution(min_long_side=1024, name='min_resolution')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Drop images whose long side is below `min_long_side` pixels.

Reads the `resolution` annotation. If absent, the filter keeps the image
(under the principle that filters never drop on missing evidence).

### *class* lookbook.filters.technical.NoExactDuplicate(name='no_exact_duplicate', \_seen=set())

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Keep at most one image per `file_hash`.

The first image in iteration order to claim a hash wins; later images
with the same hash are dropped.

### *class* lookbook.filters.technical.NoNearDuplicate(max_distance=5, name='no_near_duplicate', \_seen_hashes=list())

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Keep at most one image per near-duplicate cluster.

Clusters are formed greedily: the first image to be visited is the
cluster representative, and any later image whose `phash` is within
`max_distance` Hamming bits is dropped.

### lookbook.filters.technical.fresh_filter(filter_id, \*\*overrides)

Return a fresh instance of a registered filter.

Stateful filters (dedup) must be re-instantiated per pipeline; the
registry holds a singleton, so call this when building a fresh pipeline.
