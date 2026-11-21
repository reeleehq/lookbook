# lookbook.scorers.technical

Technical scorers — Phase 0/1.

Phase 0 ships `RandomScore` (placeholder for end-to-end orchestration).

Phase 1 adds the cheap-funnel scorers — these run on CPU with Pillow + numpy
as the base path, falling back to richer backends (cv2, imagehash) when
they’re available. None of them require torch or any GPU dep.

metric_id     | tier | requires    | needs                |
<br/>

```
|---------------|
```

——

```
|-------------|
```

———————-|
| resolution    | T0   | —           | Pillow               |
| file_hash     | T0   | —           | stdlib               |
| phash         | T1   | —           | imagehash (optional) |
| blur          | T1   | —           | numpy (cv2 optional) |
| exposure      | T1   | —           | numpy + Pillow       |

### Functions

| [`phash_distance`](#lookbook.scorers.technical.phash_distance)(a, b)   | Hamming distance between two hex-encoded perceptual hashes.   |
|-------------------------------------------------------------------------|---------------------------------------------------------------|

### Classes

| [`Blur`](#lookbook.scorers.technical.Blur)([metric_id, cost_tier, requires, ...])       | Variance of Laplacian — higher means sharper.                  |
|----------------------------------------------------------------------------------------------------|----------------------------------------------------------------|
| [`Exposure`](#lookbook.scorers.technical.Exposure)([metric_id, cost_tier, requires, ...])   | Exposure characterization from the grayscale histogram.        |
| [`FileHash`](#lookbook.scorers.technical.FileHash)([metric_id, cost_tier, requires, ...])   | SHA1 of the raw image bytes — exact-duplicate detection.       |
| [`PerceptualHash`](#lookbook.scorers.technical.PerceptualHash)([metric_id, cost_tier, ...])       | Perceptual hash for near-duplicate detection.                  |
| [`RandomScore`](#lookbook.scorers.technical.RandomScore)([metric_id, cost_tier, ...])          | Deterministic pseudo-random score in [0, 1) keyed by image_id. |
| [`Resolution`](#lookbook.scorers.technical.Resolution)([metric_id, cost_tier, requires, ...]) | Image dimensions and long-side.                                |
| [`TechnicalQuality`](#lookbook.scorers.technical.TechnicalQuality)([metric_id, cost_tier, ...])     | Composite 0..1 technical-quality score.                        |

### *class* lookbook.scorers.technical.Blur(metric_id='blur', cost_tier=1, requires=(), backend='cv2-or-numpy', max_side=512)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Variance of Laplacian — higher means sharper. T1.

Uses cv2 when available (the canonical implementation); otherwise falls
back to a small numpy 3x3 kernel convolution. Numbers are comparable to
the cv2 path within a few percent on natural images.

### *class* lookbook.scorers.technical.Exposure(metric_id='exposure', cost_tier=1, requires=(), backend='numpy', max_side=512)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Exposure characterization from the grayscale histogram. T1.

Returns mean, std, and key percentiles. Together they let a downstream
filter say “drop images that are mostly black or mostly white.”

### *class* lookbook.scorers.technical.FileHash(metric_id='file_hash', cost_tier=0, requires=(), backend='stdlib:sha1')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

SHA1 of the raw image bytes — exact-duplicate detection. T0.

### *class* lookbook.scorers.technical.PerceptualHash(metric_id='phash', cost_tier=1, requires=(), backend='imagehash', algorithm='phash')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Perceptual hash for near-duplicate detection. T1.

Uses `imagehash` (MIT) when available; result is the hex string of the
hash. The default algorithm is `phash` (DCT-based). Hamming distance
between hex strings (over hash bits) is the standard near-dup metric;
`lookbook.scorers.technical.phash_distance` provides it.

### *class* lookbook.scorers.technical.RandomScore(metric_id='random_score', cost_tier=0, requires=(), seed=0, backend='lookbook:random')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Deterministic pseudo-random score in [0, 1) keyed by image_id.

### *class* lookbook.scorers.technical.Resolution(metric_id='resolution', cost_tier=0, requires=(), backend='Pillow')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Image dimensions and long-side. T0 — header read, no decode.

### *class* lookbook.scorers.technical.TechnicalQuality(metric_id='technical_quality', cost_tier=1, requires=('blur', 'exposure', 'resolution'), backend='derived', blur_normalization=500.0, target_long_side=1024, clipping_penalty=2.0)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Composite 0..1 technical-quality score. T1, derived.

Reads `blur`, `exposure`, and `resolution` from the manifest (the
orchestrator’s topo-sort runs them first via `requires`) and folds
them into one rankable number. This is the non-face counterpart of
`face_quality`: it gives `top_k` a single metric for curating image
pools where no face is involved — environment plates, prop refs,
style boards.

The blend is sharpness-dominant (a soft or blown reference is the
worst failure mode), with exposure clipping and resolution as
secondary terms. `blur` missing yields a neutral 0.5 sharpness so a
pool scored without the blur scorer still ranks by exposure + size.

### lookbook.scorers.technical.phash_distance(a, b)

Hamming distance between two hex-encoded perceptual hashes.

* **Return type:**
  [`int`](https://docs.python.org/3/builtins/functions.html#int)
