# lookbook.selectors.quota

Quota-aware selection: pick K from N with per-bin budgets.

The QuotaSelector wraps an inner selector and runs it once per bin. Bins
are derived from a manifest annotation (`bin_metric_id`); quotas are a
mapping from bin label to a count.

Typical use for character LoRAs:

> QuotaSelector(
> : bin_metric_id=”head_pose.yaw_bin”,   # or any nested-key path
>   inner_selector_id=”top_k”,
>   inner_overrides={“metric_id”: “face_quality”},

> )

> # via curate(…)
> constraints = {“quotas”: {“front”: 8, “three_quarter”: 5, “profile”: 3, “back”: 1}}

If a bin doesn’t reach its quota (not enough survivors there), the deficit
falls back to the highest-quality survivors from any bin so the kept-set
size still hits K when possible. Set `strict=True` to disable that fallback.

### Classes

| [`QuotaSelector`](#lookbook.selectors.quota.QuotaSelector)([selector_id, bin_metric_id, ...])   | Per-bin quota selection wrapping an inner Selector.   |
|-----------------------------------------------------------------------------------------------------|-------------------------------------------------------|

### *class* lookbook.selectors.quota.QuotaSelector(selector_id='quota', bin_metric_id='head_pose.yaw_bin', inner_selector_id='top_k', inner_overrides=dict(), strict=False, embedding_space=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Per-bin quota selection wrapping an inner Selector.
