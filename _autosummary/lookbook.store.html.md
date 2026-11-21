# lookbook.store

Repository pattern for lookbook persistence.

Three stores hold the package’s state. All three are MutableMappings so the
backend (filesystem, SQLite, S3, Mongo, in-memory) is swappable:

- `images`: image_id -> record about the image, e.g. `{"path": ...}`
- `manifest`: “image_id–metric_id” -> Annotation (as dict via codec)
- `runs`: run_id -> run record (recipe, kept set, report)

The default factory wires everything to JSON-on-disk under the user’s app
data folder (via config2py). Tests pass `dict()` everywhere to skip I/O.

### Functions

| [`get_stores`](#lookbook.store.get_stores)(\*[, root, images_store, ...])   | Build the lookbook Stores bundle.                             |
|----------------------------------------------------------------------------------------------|---------------------------------------------------------------|
| [`manifest_codec`](#lookbook.store.manifest_codec)(store)                       | Wrap a string-keyed JSON-dict store so it speaks Annotations. |

### Classes

| [`Stores`](#lookbook.store.Stores)(images, manifest, runs, embeddings[, ...])   | Bundle of all stores lookbook uses for persistence.   |
|------------------------------------------------------------------------------------------------------|-------------------------------------------------------|

### *class* lookbook.store.Stores(images, manifest, runs, embeddings, root=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Bundle of all stores lookbook uses for persistence.

### lookbook.store.get_stores(, root=None, images_store=None, manifest_store=None, runs_store=None, embeddings=None)

Build the lookbook Stores bundle.

All arguments are optional. When `root` is None and no stores are
supplied, the user’s app data folder is used. Pass `dict()` for any
slot to keep that store in memory (useful for tests).

```pycon
>>> stores = get_stores(
...     images_store={}, manifest_store={}, runs_store={}, embeddings={}
... )
>>> stores.manifest is not None
True
```

* **Return type:**
  [`Stores`](#lookbook.store.Stores)

### lookbook.store.manifest_codec(store)

Wrap a string-keyed JSON-dict store so it speaks Annotations.

Keys flow as `(image_id, metric_id) <-> "image_id--metric_id.json"`.
Values flow as `Annotation <-> dict`.

* **Return type:**
  [`MutableMapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.MutableMapping)
