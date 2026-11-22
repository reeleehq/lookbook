# lookbook.manifest

Helpers for reading and writing the manifest.

The manifest *is* a `MutableMapping[(image_id, metric_id), Annotation]`.
This module is a tiny ergonomics layer on top — nothing here is essential
to the abstraction; it exists so callers don’t have to spell out tuple keys.

### Functions

| [`get_annotation`](#lookbook.manifest.get_annotation)(manifest, image_id, metric_id)   | Return the annotation if present, else None.                                 |
|--------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| [`has_annotation`](#lookbook.manifest.has_annotation)(manifest, image_id, metric_id)   | Return whether the manifest holds an annotation for `(image_id, metric_id)`. |
| [`image_ids`](#lookbook.manifest.image_ids)(manifest)                             | The set of distinct image_ids that appear in the manifest.                   |
| [`iter_annotations_for`](#lookbook.manifest.iter_annotations_for)(manifest, image_id)        | Yield every annotation for a given image.                                    |
| [`put_annotation`](#lookbook.manifest.put_annotation)(manifest, annotation)            | Write an annotation to the manifest, keyed by (image_id, metric_id).         |
| [`value_of`](#lookbook.manifest.value_of)(manifest, image_id, metric_id[, ...])  | Return the bare value of an annotation (not the wrapper), or default.        |

### lookbook.manifest.get_annotation(manifest, image_id, metric_id)

Return the annotation if present, else None.

* **Return type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Annotation`](lookbook.base.html.md#lookbook.base.Annotation)]

### lookbook.manifest.has_annotation(manifest, image_id, metric_id)

Return whether the manifest holds an annotation for `(image_id, metric_id)`.

* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)

### lookbook.manifest.image_ids(manifest)

The set of distinct image_ids that appear in the manifest.

* **Return type:**
  [`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

### lookbook.manifest.iter_annotations_for(manifest, image_id)

Yield every annotation for a given image.

* **Return type:**
  [`Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator)[[`Annotation`](lookbook.base.html.md#lookbook.base.Annotation)]

### lookbook.manifest.put_annotation(manifest, annotation)

Write an annotation to the manifest, keyed by (image_id, metric_id).

* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)

### lookbook.manifest.value_of(manifest, image_id, metric_id, default=None)

Return the bare value of an annotation (not the wrapper), or default.

* **Return type:**
  [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)
