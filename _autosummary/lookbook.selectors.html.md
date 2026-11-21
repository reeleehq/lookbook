# lookbook.selectors

Selectors: choose K from N given the manifest.

Each submodule registers its selectors into `lookbook.registry.selectors`.

### Modules

| [`quota`](lookbook.selectors.quota.html.md#module-lookbook.selectors.quota)           | Quota-aware selection: pick K from N with per-bin budgets.            |
|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| [`submodular`](lookbook.selectors.submodular.html.md#module-lookbook.selectors.submodular) | Submodular selectors over embedding spaces.                           |
| [`topk`](lookbook.selectors.topk.html.md#module-lookbook.selectors.topk)             | Top-K selector: pick the K highest-scoring images by a single metric. |
