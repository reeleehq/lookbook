# lookbook.refs

Concrete `ImageRef` implementations.

Refs are the unit of identity in lookbook. The orchestrator passes refs
around; scorers open them lazily; the manifest is keyed by `image_id`.

Three impls are provided here. None of them require Pillow at import time;
`open()` defers the import.

All three expose `local_path(cache_dir=None) -> str` — a path on the
local filesystem that the bytes are reachable through. Path refs return
their existing path; bytes/url refs materialize once into a content-
addressed cache and reuse the result. This is the ergonomic surface for
downstream tools that want a file (e.g. ffmpeg, lookbook → fal upload).

### Functions

| [`to_local_path`](#lookbook.refs.to_local_path)(ref, \*[, cache_dir])   | Return a filesystem path where the bytes of `ref` can be read.   |
|----------------------------------------------------------------------------------------|------------------------------------------------------------------|

### Classes

| [`BytesImageRef`](#lookbook.refs.BytesImageRef)(payload[, image_id, metadata])     | An image stored as raw bytes in memory.   |
|---------------------------------------------------------------------------------------------------|-------------------------------------------|
| [`PathImageRef`](#lookbook.refs.PathImageRef)(path[, image_id, metadata])         | An image referenced by filesystem path.   |
| [`UrlImageRef`](#lookbook.refs.UrlImageRef)(url[, image_id, metadata, \_cached]) | An image referenced by URL.               |

### *class* lookbook.refs.BytesImageRef(payload, image_id='', metadata=dict())

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

An image stored as raw bytes in memory.

#### bytes()

Return the raw image bytes.

* **Return type:**
  [`bytes`](#lookbook.refs.BytesImageRef.bytes)

#### local_path(, cache_dir=None)

Materialize the bytes into a file (cached by image_id).

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

#### open()

Open the image (a PIL image).

### *class* lookbook.refs.PathImageRef(path, image_id='', metadata=dict())

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

An image referenced by filesystem path.

#### bytes()

Return the raw image bytes.

* **Return type:**
  [`bytes`](#lookbook.refs.PathImageRef.bytes)

#### local_path(, cache_dir=None)

Return the existing on-disk path. `cache_dir` is ignored.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

#### open()

Open the image (a PIL image).

### *class* lookbook.refs.UrlImageRef(url, image_id='', metadata=dict(), \_cached=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

An image referenced by URL.

The bytes are fetched on first access and cached on the instance.

#### bytes()

Return the raw image bytes.

* **Return type:**
  [`bytes`](#lookbook.refs.UrlImageRef.bytes)

#### local_path(, cache_dir=None)

Download (once) and return the local path.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

#### open()

Open the image (a PIL image).

### lookbook.refs.to_local_path(ref, , cache_dir=None)

Return a filesystem path where the bytes of `ref` can be read.

Works on any object that exposes `.local_path(cache_dir)` — i.e.
every concrete `ImageRef` shipped with lookbook. Provided as a
free function so downstream code doesn’t need to know which subtype
it has.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
