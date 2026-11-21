# lookbook.pipeline

Pipeline orchestrator.

A `Pipeline` is a list of scorers (and, later, filters/embedders) plus a
final selector. Running it:

1. Topologically orders the scorers by their `requires` declarations.
2. Walks them in cost-tier order, writing results to the manifest.
3. Hands the surviving candidates plus the read-only manifest to the
   selector.

The orchestration is a hand-rolled topo walk. Swapping in `meshed.DAG` for
richer dependency graphs and caching was planned but never taken up; nothing
in the package imports `meshed`. Whoever does make that switch: the
`Scorer.requires` field is already the dependency graph.

### Classes

| [`Pipeline`](#lookbook.pipeline.Pipeline)([scorers, embedders, filters, ...])    | An ordered set of scorers + embedders + filters + a final selector.   |
|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| [`RunResult`](#lookbook.pipeline.RunResult)(run_id, kept, candidates, ...[, ...]) | The result of running a pipeline.                                     |

### *class* lookbook.pipeline.Pipeline(scorers=list(), embedders=list(), filters=list(), selector=None, diagnose_clusters=0)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

An ordered set of scorers + embedders + filters + a final selector.

#### run(candidates, , k, stores=None, constraints=None, run_id=None)

Score, embed, filter, and select.

`stores` defaults to in-memory. Pass `get_stores()` for the user’s
app data folder defaults.

* **Return type:**
  [`RunResult`](#lookbook.pipeline.RunResult)

### *class* lookbook.pipeline.RunResult(run_id, kept, candidates, selector_id, scorer_ids, started_at, finished_at, report=dict())

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

The result of running a pipeline.
