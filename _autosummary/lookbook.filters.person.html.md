# lookbook.filters.person

Person-LoRA filters — Phase 3.

These read `face_box`, `face_area`, and (optionally) `head_pose` from the
manifest. Like all filters in lookbook, they keep an image when the
relevant evidence is missing — the design principle is that filters never
drop on absent annotations.

### Classes

| [`HasFace`](#lookbook.filters.person.HasFace)([name])                      | Drop images with no detected face.                                     |
|---------------------------------------------------------------------------------------|------------------------------------------------------------------------|
| [`MinFaceArea`](#lookbook.filters.person.MinFaceArea)([min_fraction, name])    | Drop images whose face occupies less than `min_fraction` of the frame. |
| [`MinFaceConfidence`](#lookbook.filters.person.MinFaceConfidence)([threshold, name]) | Drop images whose face-detection confidence is below `threshold`.      |
| [`SingleFaceOnly`](#lookbook.filters.person.SingleFaceOnly)([name])               | Drop images with more than one detected face.                          |

### *class* lookbook.filters.person.HasFace(name='has_face')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Drop images with no detected face.

#### keep(ref, manifest)

Return whether `ref` passes this filter.

* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)

### *class* lookbook.filters.person.MinFaceArea(min_fraction=0.05, name='min_face_area')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Drop images whose face occupies less than `min_fraction` of the frame.

#### keep(ref, manifest)

Return whether `ref` passes this filter.

* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)

### *class* lookbook.filters.person.MinFaceConfidence(threshold=0.5, name='min_face_confidence')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Drop images whose face-detection confidence is below `threshold`.

#### keep(ref, manifest)

Return whether `ref` passes this filter.

* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)

### *class* lookbook.filters.person.SingleFaceOnly(name='single_face_only')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Drop images with more than one detected face.

Reads `face_box.n_faces`. Useful for character LoRAs where you want
isolated subject images.

#### keep(ref, manifest)

Return whether `ref` passes this filter.

* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)
