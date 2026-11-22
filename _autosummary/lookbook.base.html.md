# lookbook.base

Core protocols and types for lookbook.

This module is the open-closed boundary of the package. Every extension point
is a `typing.Protocol` here. Heavy ML dependencies must NOT be imported in
this module — keep it pure-Python so the laptop tier of the package stays
import-light.

### Classes

| [`Annotation`](#lookbook.base.Annotation)(image_id, metric_id, value[, ...])   | A single annotation produced by a Scorer or Embedder for one image.   |
|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| [`Embedder`](#lookbook.base.Embedder)(\*args, \*\*kwargs)                    | Computes a vector representation in some named embedding space.       |
| [`Filter`](#lookbook.base.Filter)(\*args, \*\*kwargs)                      | Predicate over annotations that decides whether to keep an image.     |
| [`ImageRef`](#lookbook.base.ImageRef)(\*args, \*\*kwargs)                    | Anything that knows its identity and how to be opened lazily.         |
| [`Scorer`](#lookbook.base.Scorer)(\*args, \*\*kwargs)                      | Computes one annotation per image.                                    |
| [`Selector`](#lookbook.base.Selector)(\*args, \*\*kwargs)                    | Chooses a subset of size up-to-K from candidates given the manifest.  |

### *class* lookbook.base.Annotation(image_id, metric_id, value, config_hash='', cost_tier=0, timestamp=\_utcnow(), backend='')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

A single annotation produced by a Scorer or Embedder for one image.

The (image_id, metric_id) pair is the manifest key. `config_hash` is the
cache key — re-running with the same config yields a cache hit; changing
a threshold or model invalidates.

#### *property* key *: [Tuple](https://docs.python.org/3/library/typing.html#typing.Tuple)[[str](https://docs.python.org/3/builtins/stdtypes.html#str), [str](https://docs.python.org/3/builtins/stdtypes.html#str)]*

The image’s manifest key.

### *class* lookbook.base.Embedder(\*args, \*\*kwargs)

Bases: [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)

Computes a vector representation in some named embedding space.

#### embed(ref)

Embed `ref` into this embedder’s vector space.

* **Return type:**
  [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)

### *class* lookbook.base.Filter(\*args, \*\*kwargs)

Bases: [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)

Predicate over annotations that decides whether to keep an image.

#### keep(ref, manifest)

Return whether `ref` passes this filter.

* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)

### *class* lookbook.base.ImageRef(\*args, \*\*kwargs)

Bases: [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)

Anything that knows its identity and how to be opened lazily.

#### bytes()

Return the raw image bytes.

* **Return type:**
  [`bytes`](#lookbook.base.ImageRef.bytes)

#### open()

Open the image (a PIL image).

* **Return type:**
  [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)

### *class* lookbook.base.Scorer(\*args, \*\*kwargs)

Bases: [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)

Computes one annotation per image. Idempotent w.r.t. config_hash.

#### score(ref, manifest)

Score `ref`; the result is stored in the manifest under this scorer’s id.

* **Return type:**
  [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)

### *class* lookbook.base.Selector(\*args, \*\*kwargs)

Bases: [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)

Chooses a subset of size up-to-K from candidates given the manifest.

#### select(candidates, manifest, k, constraints=None)

Choose the images to keep from the scored candidates.

* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`ImageRef`](#lookbook.base.ImageRef)]
