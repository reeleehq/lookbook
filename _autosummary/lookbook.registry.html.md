# lookbook.registry

Plugin registry for scorers, filters, embedders, selectors.

Anything that implements one of the protocols in `lookbook.base` can be
registered here under a string id and looked up by the orchestrator. This
is the open-closed boundary in concrete form: new metrics are *registered*,
never *subclassed*.

### Functions

| `register_embedder`(name, \*\*kwargs)                                              |                                             |
|------------------------------------------------------------------------------------|---------------------------------------------|
| `register_filter`(name, \*\*kwargs)                                                |                                             |
| [`register_scorer`](#lookbook.registry.register_scorer)(name, \*\*kwargs) | Decorator form: `@register_scorer("blur")`. |
| `register_selector`(name, \*\*kwargs)                                              |                                             |

### lookbook.registry.register_scorer(name, \*\*kwargs)

Decorator form: `@register_scorer("blur")`.

* **Return type:**
  [`Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)
