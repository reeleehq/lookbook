# lookbook.scorers.person

Person-LoRA scorers — Phase 3.

Two backends ship for face detection:

- `MockFaceDetect`: synthesizes a centered face box, deterministic, no deps.
  Used by tests and by users who already have face boxes from another tool.
- `InsightFaceDetect`: real RetinaFace + landmarks + (optionally) gender/age,
  lazy-imported. Use for production.

Both write to the same `face_box` metric_id. They are distinguished by
`config_hash` so the cache invalidates if the user swaps backends.

Downstream scorers (`FaceArea`, `HeadPose`, `FaceQualityProxy`) read
`face_box` from the manifest via the `requires` mechanism. They never touch
the detector directly — the orchestrator runs the detector first.

The value shape of `face_box` (when a face is detected):

> {
> : “x1”: int, “y1”: int, “x2”: int, “y2”: int,
>   “confidence”: float,         # detector score
>   “n_faces”: int,              # total faces detected before keeping the largest
>   “landmarks”: list | None,    # 5 (x, y) pairs if available, else None

> }

When no face is detected, the value is `None`.

### Classes

| [`FaceArea`](#lookbook.scorers.person.FaceArea)([metric_id, cost_tier, requires, ...])   | Face area as a fraction of total image area, plus a size bin.                           |
|----------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| [`FaceQualityProxy`](#lookbook.scorers.person.FaceQualityProxy)([metric_id, cost_tier, ...])     | Combine detector confidence, face area, and (optionally) blur into a single 0..1 score. |
| [`InsightFaceDetect`](#lookbook.scorers.person.InsightFaceDetect)([metric_id, cost_tier, ...])    | RetinaFace face detection via insightface.                                              |
| [`MockFaceDetect`](#lookbook.scorers.person.MockFaceDetect)([metric_id, cost_tier, ...])       | Deterministic face detector — synthesizes one centered box per image.                   |
| [`MockHeadPose`](#lookbook.scorers.person.MockHeadPose)([metric_id, cost_tier, ...])         | Synthetic head pose — deterministic from image_id.                                      |
| [`SixDRepNetHeadPose`](#lookbook.scorers.person.SixDRepNetHeadPose)([metric_id, cost_tier, ...])   | Head-pose estimation via 6DRepNet (lazy-imported).                                      |

### *class* lookbook.scorers.person.FaceArea(metric_id='face_area', cost_tier=1, requires=('face_box', 'resolution'), backend='derived')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Face area as a fraction of total image area, plus a size bin.

Reads `face_box` and `resolution`. Both must be present upstream — the
orchestrator’s topo-sort handles this via the `requires` field.

### *class* lookbook.scorers.person.FaceQualityProxy(metric_id='face_quality', cost_tier=1, requires=('face_box', 'face_area'), backend='derived', blur_normalization=500.0)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Combine detector confidence, face area, and (optionally) blur into a
single 0..1 score.

This is a stand-in for true face image quality assessment (FIQA — see
SDD-FIQA, CR-FIQA, CLIB-FIQA in the design report). Real FIQA needs a
purpose-trained model; the proxy here is a reasonable default for
Phase 3 that uses only signals already in the manifest.

### *class* lookbook.scorers.person.InsightFaceDetect(metric_id='face_box', cost_tier=1, requires=(), backend='insightface:retinaface', model_name='buffalo_l', det_size=640)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

RetinaFace face detection via insightface.

Returns the largest face if multiple are present. `n_faces` records the
pre-filter count so a downstream filter can drop multi-face images.

### *class* lookbook.scorers.person.MockFaceDetect(metric_id='face_box', cost_tier=1, requires=(), backend='lookbook:mock_face', simulate_no_face=False)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Deterministic face detector — synthesizes one centered box per image.

Useful for tests and for end-to-end demos without a real detector. The
box covers the central 60% of the image (or 0% if `simulate_no_face`
is set, in which case the face_box value is None).

### *class* lookbook.scorers.person.MockHeadPose(metric_id='head_pose', cost_tier=1, requires=('face_box',), backend='lookbook:mock_pose')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Synthetic head pose — deterministic from image_id.

Yaw distributed roughly uniformly in [-90, 90]; pitch/roll narrower.
Useful for testing the QuotaSelector without a real head-pose model.

### *class* lookbook.scorers.person.SixDRepNetHeadPose(metric_id='head_pose', cost_tier=2, requires=('face_box',), backend='sixdrepnet', config_version='v1')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Head-pose estimation via 6DRepNet (lazy-imported).

See [https://github.com/thohemp/6DRepNet](https://github.com/thohemp/6DRepNet) for the reference implementation.
