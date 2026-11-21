# lookbook.selectors.submodular

Submodular selectors over embedding spaces.

Phase 2 ships a greedy facility-location selector implemented in pure
numpy. It’s the right default for “best K from N” when diversity matters:

> f(S) = sum over y in V of max over x in S of similarity(x, y)

> > + alpha \* sum over x in S of quality(x)

The greedy algorithm gives a (1 - 1/e) ≈ 0.63 approximation guarantee.
For typical curation sizes (N ≤ 1000, K ≤ 50), pure numpy is fast enough
and avoids the `apricot` dependency. For larger pools, swap in `apricot`’s
optimized lazy-greedy via the same Selector protocol.

Embeddings are not read from the manifest directly. The pipeline pre-fetches
them from `stores.embeddings[space_id]` and passes them via
`constraints["embeddings"]` as a `dict[image_id, np.ndarray]`.

### Classes

| [`FacilityLocation`](#lookbook.selectors.submodular.FacilityLocation)([selector_id, ...])   | Greedy facility-location subset selection.   |
|-----------------------------------------------------------------------------------------|----------------------------------------------|

### *class* lookbook.selectors.submodular.FacilityLocation(selector_id='facility_location', embedding_space='dinov2_base', quality_metric_id='', weight_quality=0.0, weight_diversity=1.0)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Greedy facility-location subset selection.

The objective is:

```default
f(S) = sum_y max_{x in S} sim(x, y)  +  weight_quality * sum_{x in S} q(x)
```

where `sim` is cosine similarity (assumes embeddings are L2-normalized;
if they are not, the selector normalizes them first) and `q(x)` is the
annotation `quality_metric_id` for `x`, defaulting to 0 when absent.

`weight_quality=0` gives a pure-diversity selection. `weight_quality`
in 0.1–0.5 typically works well for “diverse but high-quality.”
