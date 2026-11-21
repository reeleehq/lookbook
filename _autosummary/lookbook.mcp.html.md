# lookbook.mcp

MCP surface for lookbook, built with `fastmcp`.

Each verb from `lookbook.http` is exposed as an MCP tool that an LLM
agent can call. The tool functions are intentionally the same callables
used by the HTTP layer — JSON-able args, JSON-able returns. This means
swapping between an HTTP frontend and an MCP frontend is “wire it once,
expose it twice.”

Run the server over stdio with `lookbook mcp` (the default transport
that Claude Desktop and the Anthropic SDK expect).

### Functions

| [`mcp_compare_to_reference`](#lookbook.mcp.mcp_compare_to_reference)(reference_paths, ...)   | Check whether a generated image still matches a locked reference.    |
|---------------------------------------------------------------------------------------------------|----------------------------------------------------------------------|
| [`mcp_curate_source`](#lookbook.mcp.mcp_curate_source)(source_path[, k, recipe])      | Run a full curation pipeline on a directory and return the K best.   |
| [`mcp_get_annotations`](#lookbook.mcp.mcp_get_annotations)(image_id)                    | All annotations stored for one image.                                |
| [`mcp_get_image`](#lookbook.mcp.mcp_get_image)(image_id)                          | Look up an image's path and metadata by id.                          |
| [`mcp_get_run`](#lookbook.mcp.mcp_get_run)(run_id)                              | Fetch a stored run record by id.                                     |
| [`mcp_ingest_source`](#lookbook.mcp.mcp_ingest_source)(source_path)                   | Scan a directory or file for images and register them on the server. |
| [`mcp_list_plugins`](#lookbook.mcp.mcp_list_plugins)()                               | List every registered scorer / embedder / filter / selector.         |
| [`mcp_list_recipes`](#lookbook.mcp.mcp_list_recipes)()                               | List every available curation recipe / profile.                      |
| [`mcp_list_runs`](#lookbook.mcp.mcp_list_runs)()                                  | All curation runs stored on this server.                             |
| [`mcp_score_image`](#lookbook.mcp.mcp_score_image)(metric_id[, source_path, ...])   | Score one image against one metric and cache the result.             |
| [`mk_lookbook_mcp`](#lookbook.mcp.mk_lookbook_mcp)(\*[, name])                      | Build a FastMCP server exposing the lookbook curation verbs.         |
| [`serve`](#lookbook.mcp.serve)(\*[, transport])                           | Run the lookbook MCP server.                                         |

### lookbook.mcp.mcp_compare_to_reference(reference_paths, candidate_path, embedder='arcface', threshold=0.85, aggregation='max', normalization='rescale')

Check whether a generated image still matches a locked reference.

The reference-supervisor verb. Embeds the candidate and the reference(s)
in the chosen space and returns a normalized identity similarity in
`[0, 1]` (1 = same identity) plus an advisory `passed` flag against the
threshold. The pass/fail is advisory — you decide whether to act on it.

* **Parameters:**
  * **reference_paths** ([`list`](https://docs.python.org/3/builtins/stdtypes.html#list)) – one or more server-local paths of the locked
    reference image(s). A pool is folded by `aggregation`.
  * **candidate_path** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – server-local path of the candidate generation.
  * **embedder** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – `"arcface"` for face identity (default), `"clip"` or
    `"dinov2"` for scenes / architecture / props.
  * **threshold** ([`float`](https://docs.python.org/3/builtins/functions.html#float)) – advisory pass/fail cutoff on the [0, 1] scale.
  * **aggregation** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – how to fold a reference pool — `"max"` (matches any
    locked view; default), `"mean"`, or `"min"`.
  * **normalization** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – cosine→[0,1] map — `"rescale"` (default) or `"clamp"`.
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)
* **Returns:**
  ```
  `
  ```

  {identity_cosine, score, passed, threshold, per_reference,
  : aggregation, n_references}\`.

### lookbook.mcp.mcp_curate_source(source_path, k=20, recipe='funnel')

Run a full curation pipeline on a directory and return the K best.

The high-level entry point. Picks K reference images from the
directory using the named recipe (cheap funnel, embeddings + facility
location, person profile, etc.). Returns a run record containing the
chosen image_ids, drop attributions per filter, optional cluster
coverage, scorer ids that ran, and run timing.

* **Parameters:**
  * **source_path** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – absolute path to the directory of candidate images.
  * **k** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – target subset size (the number of images to keep).
  * **recipe** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – a recipe / profile name. Use `list_recipes` to see options.
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

Common recipes:

> - `random`        : placeholder, deterministic, no real scoring.
> - `funnel`        : Phase 1 cheap filter — fast, no GPU.
> - `funnel_relaxed`: same but lower thresholds for typical phone shots.
> - `diverse`       : DINOv2 embeddings + facility-location.
> - `diverse_clip`  : same with CLIP semantic embeddings.
> - `person`
>   : ArcFace identity + pose-bin quotas).
> - `person_mock`   : person without model downloads (testing).

### lookbook.mcp.mcp_get_annotations(image_id)

All annotations stored for one image.

Includes the metric_id, value, config_hash, cost_tier, backend, and
timestamp for each annotation. Use this to understand *why* an image
was kept or rejected — the manifest holds the full provenance.

* **Parameters:**
  **image_id** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – as returned from `ingest_source` or `curate_source`.
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### lookbook.mcp.mcp_get_image(image_id)

Look up an image’s path and metadata by id.

Returns `{image_id, path, n_bytes}` when found. Phase 5 returns
metadata only — agents that want the raw bytes should read the file
directly when running on the same host as the server.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### lookbook.mcp.mcp_get_run(run_id)

Fetch a stored run record by id.

The run record contains: kept and candidate image_ids, scorer_ids,
selector_id, started_at / finished_at timestamps, and a `report`
block with drop attributions and (when applicable) cluster coverage.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### lookbook.mcp.mcp_ingest_source(source_path)

Scan a directory or file for images and register them on the server.

Records `image_id -> path` in the server’s image store so later calls
(`score_image`, `get_image`, `curate_source`) can refer to images by
id. Returns the list of image_ids and the count.

* **Parameters:**
  **source_path** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – absolute path on the server’s filesystem.
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### lookbook.mcp.mcp_list_plugins()

List every registered scorer / embedder / filter / selector.

Use this to discover available metric_ids for `score_image` and to
understand what capabilities each recipe is wiring together.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### lookbook.mcp.mcp_list_recipes()

List every available curation recipe / profile.

Returns a dict where each value is a recipe spec describing the
scorers, embedders, filters, selector, and default constraints. Use
this first to see what `curate_source` will accept for the `recipe`
argument.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### lookbook.mcp.mcp_list_runs()

All curation runs stored on this server.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### lookbook.mcp.mcp_score_image(metric_id, source_path='', image_id='')

Score one image against one metric and cache the result.

Pass either `source_path` (a path on the server) or `image_id` (must
already be registered via `ingest_source`). Returns the metric value;
re-running with the same metric_id and config is free.

* **Parameters:**
  * **metric_id** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – a registered scorer name (see `list_plugins`).
  * **source_path** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – optional, the path to the image.
  * **image_id** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – optional, an id from a previous `ingest_source`.
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### lookbook.mcp.mk_lookbook_mcp(, name='lookbook')

Build a FastMCP server exposing the lookbook curation verbs.

Each verb becomes an MCP tool. The agent’s typical sequence is:

> list_recipes() -> pick a recipe
> curate_source(path, k, recipe) -> get back a run record
> get_annotations(image_id) -> understand why each kept image won
> get_run(run_id) -> review the full report

The server uses the same Stores singleton as `lookbook.http`, so an
HTTP server and an MCP server backed by the same data folder share
the manifest and the runs index.

### lookbook.mcp.serve(, transport='stdio', \*\*kwargs)

Run the lookbook MCP server.

The default transport is stdio — the protocol Claude Desktop and the
Anthropic SDK expect when launching an MCP server as a subprocess.
Pass `transport="http"` (and a port via kwargs) for HTTP-streamable
transport.

* **Return type:**
  [`None`](https://docs.python.org/3/builtins/constants.html#None)
