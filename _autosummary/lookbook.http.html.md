# lookbook.http

HTTP surface for lookbook, built with `qh` over FastAPI.

Each HTTP route is a thin function that takes JSON-able args and returns
a JSON-able dict. The route functions are the *only* thing this module
adds — all real work is delegated to the existing facade.

Build the app with `mk_lookbook_app()` and run it with `serve()` (or use
the `lookbook serve` CLI command).

### Functions

| [`compare_to_reference`](#lookbook.http.compare_to_reference)(\*, reference_paths, ...)   | Identity/likeness of a candidate vs a locked reference (or pool).   |
|---------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| [`curate_source`](#lookbook.http.curate_source)(source_path, \*[, k, recipe])      | Run a recipe on a directory of images.                              |
| [`get_annotations`](#lookbook.http.get_annotations)(image_id)                        | All annotations for one image (drawn from the manifest).            |
| [`get_image`](#lookbook.http.get_image)(image_id)                              | Return the raw bytes of an image by id.                             |
| [`get_run`](#lookbook.http.get_run)(run_id)                                  | One run record by id.                                               |
| [`ingest_source`](#lookbook.http.ingest_source)(source_path)                       | Ingest a directory or file.                                         |
| [`list_plugins`](#lookbook.http.list_plugins)()                                   | All registered scorers / embedders / filters / selectors.           |
| [`list_recipes`](#lookbook.http.list_recipes)()                                   | All available recipes / profiles, with their specs.                 |
| [`list_runs`](#lookbook.http.list_runs)()                                      | All run ids stored on the server.                                   |
| [`mk_lookbook_app`](#lookbook.http.mk_lookbook_app)(\*[, app])                       | Build a FastAPI app exposing the lookbook HTTP surface.             |
| [`reset_stores`](#lookbook.http.reset_stores)([stores])                           | Replace the server-wide stores.                                     |
| [`score_image`](#lookbook.http.score_image)(\*[, source_path, image_id])         | Score a single image by metric id.                                  |
| [`serve`](#lookbook.http.serve)(\*[, host, port])                          | Run the lookbook HTTP server (uvicorn under the hood).              |

### lookbook.http.compare_to_reference(, reference_paths, candidate_path, embedder='arcface', threshold=0.85, aggregation='max', normalization='rescale')

Identity/likeness of a candidate vs a locked reference (or pool).

The reference-supervisor verb: returns a normalized similarity in
`[0, 1]` (1 = same identity) plus an advisory `passed` flag. Pass one
or more `reference_paths` (server-local image paths) and a single
`candidate_path`. `embedder` selects the space — `"arcface"` for
faces (default), `"clip"` / `"dinov2"` for scenes/architecture.

The pass/fail is **advisory** — the caller decides whether to act on it.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### lookbook.http.curate_source(source_path, , k=20, recipe='funnel')

Run a recipe on a directory of images. Returns the run record.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### lookbook.http.get_annotations(image_id)

All annotations for one image (drawn from the manifest).

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### lookbook.http.get_image(image_id)

Return the raw bytes of an image by id.

The server reads from `stores.images[image_id]["path"]`. If the entry
is missing, returns a 404-style error dict (FastAPI surfaces this as a
JSON response; a future iteration may switch to a streaming binary
response via FastAPI’s `Response`).

### lookbook.http.get_run(run_id)

One run record by id.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### lookbook.http.ingest_source(source_path)

Ingest a directory or file. Records id->path in `stores.images`.

Returns the list of resolved image ids.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### lookbook.http.list_plugins()

All registered scorers / embedders / filters / selectors.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### lookbook.http.list_recipes()

All available recipes / profiles, with their specs.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### lookbook.http.list_runs()

All run ids stored on the server.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### lookbook.http.mk_lookbook_app(, app=None, \*\*kwargs)

Build a FastAPI app exposing the lookbook HTTP surface.

Each function becomes a POST endpoint with a JSON body matching its
keyword arguments. Use the auto-generated `/docs` (Swagger) or
`/redoc` for interactive exploration. Disabling qh’s convention-based
routing keeps the path scheme uniform — every route is `POST /<verb>`
and takes a JSON body — which is the pattern most agent clients
(and our future MCP layer) expect.

### lookbook.http.reset_stores(stores=None)

Replace the server-wide stores. Used by tests; rare otherwise.

### lookbook.http.score_image(, source_path='', image_id='', metric_id)

Score a single image by metric id.

Pass either `source_path` (file path on the server) or `image_id`
(must already have a path recorded via ingest).

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### lookbook.http.serve(, host='127.0.0.1', port=8000, \*\*kwargs)

Run the lookbook HTTP server (uvicorn under the hood).
