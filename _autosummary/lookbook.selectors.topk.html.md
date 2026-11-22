# lookbook.selectors.topk

Top-K selector: pick the K highest-scoring images by a single metric.

### Classes

| [`TopK`](#lookbook.selectors.topk.TopK)([metric_id, selector_id, descending])   | Sort candidates by `metric_id` (descending) and take the first K.   |
|-----------------------------------------------------------------------------------------------|---------------------------------------------------------------------|

### *class* lookbook.selectors.topk.TopK(metric_id='random_score', selector_id='top_k', descending=True)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Sort candidates by `metric_id` (descending) and take the first K.

#### select(candidates, manifest, k, constraints=None)

Choose the images to keep from the scored candidates.

* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`ImageRef`](lookbook.base.html.md#lookbook.base.ImageRef)]
