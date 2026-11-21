# lookbook.diagnose

Set-level diagnosis: what does the kept set cover, what’s missing.

Phase 2 ships cluster-coverage. The function takes the candidate pool and
the kept subset, clusters the candidates by their embeddings, and reports
how many clusters the kept set populates plus which clusters are
empty / underfilled.

This is the read-only counterpart to the selector — same data, different
question. Selectors *choose*; diagnosers *describe*.

### Functions

| [`cluster_coverage`](#lookbook.diagnose.cluster_coverage)(candidates, kept, embeddings, \*)   | Cluster the candidate embeddings into `n_clusters` and report coverage.   |
|-------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|

### lookbook.diagnose.cluster_coverage(candidates, kept, embeddings, , n_clusters=12, random_state=0)

Cluster the candidate embeddings into `n_clusters` and report coverage.

Returns a dict with:

> - `n_clusters`: actual number of clusters used (capped at len(candidates))
> - `n_clusters_filled`: clusters with at least one kept image
> - `cluster_sizes_candidates`: list of int, candidate count per cluster
> - `cluster_sizes_kept`: list of int, kept count per cluster
> - `empty_clusters`: list of int (indexes of clusters with zero kept)
> - `underrepresented_clusters`: clusters with kept_count == 0 and
>   candidate_count >= 2 (the meaningful gaps)
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)
