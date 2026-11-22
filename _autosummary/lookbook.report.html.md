# lookbook.report

Run report — what happened during a curation pass.

The report is the user-facing artifact alongside the kept set. It explains
*why* images were dropped and what the kept set looks like, in terms a
human (or an LLM agent) can act on.

Phase 1 ships the drop-attribution part. Coverage / set-level diagnosis
lands in Phase 2 alongside embeddings.

### Functions

| [`attribute_drops`](#lookbook.report.attribute_drops)(candidates, filters, manifest)   | Apply filters in order, attributing each drop to the first filter that rejected it.   |
|---------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|

### Classes

| [`Report`](#lookbook.report.Report)([n_candidates, n_survivors, n_kept, ...])   | Summary of a pipeline run.   |
|-----------------------------------------------------------------------------------------------------|------------------------------|

### *class* lookbook.report.Report(n_candidates=0, n_survivors=0, n_kept=0, dropped_by_filter=dict(), scorer_ids=list(), selector_id='', notes=dict())

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Summary of a pipeline run.

#### human()

Render a short human-readable summary.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

#### to_dict()

Return the report as a plain dict.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### lookbook.report.attribute_drops(candidates, filters, manifest)

Apply filters in order, attributing each drop to the first filter
that rejected it.

Returns (survivors, drop_counts_by_filter_name).

* **Return type:**
  [`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`ImageRef`](lookbook.base.html.md#lookbook.base.ImageRef)], [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`int`](https://docs.python.org/3/builtins/functions.html#int)]]
