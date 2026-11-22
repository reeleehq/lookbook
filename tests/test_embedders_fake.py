"""Real embedders driven through fake ``torch`` / ``transformers`` / ``insightface`` modules.

No weights, no download, no GPU: the fakes stand in for the heavy libraries so the
embedders' own logic (lazy model load, device pick, normalisation, face choice) is tested.
"""

from __future__ import annotations

import contextlib
import sys
import types

import numpy as np
import pytest
from PIL import Image

from lookbook import PathImageRef


class _T:
    """A minimal tensor: wraps an ndarray, supports the calls the embedders make."""

    def __init__(self, a):
        self.a = np.asarray(a, dtype=np.float32)

    def to(self, device):
        return self

    def squeeze(self, axis):
        return _T(self.a.squeeze(axis))

    def cpu(self):
        return self

    def numpy(self):
        return self.a


def _fake_torch(cuda=False, mps=False):
    t = types.ModuleType("torch")
    t.cuda = types.SimpleNamespace(is_available=lambda: cuda)
    t.backends = types.SimpleNamespace(
        mps=types.SimpleNamespace(is_available=lambda: mps)
    )
    t.no_grad = contextlib.nullcontext
    return t


@pytest.fixture
def img_ref(tmp_path):
    p = tmp_path / "a.png"
    Image.new("RGB", (8, 8), (200, 10, 10)).save(p)
    return PathImageRef(str(p))


def _install(monkeypatch, **mods):
    for name, mod in mods.items():
        monkeypatch.setitem(sys.modules, name, mod)


class _Loadable:
    """Stands in for a transformers model/processor class."""

    loads: list = []

    @classmethod
    def from_pretrained(cls, name):
        cls.loads.append(name)
        return cls()

    def to(self, device):
        return self

    def eval(self):
        pass


def test_autodevice_prefers_cuda_then_mps_then_cpu():
    from lookbook.embedders.clip import _autodevice

    assert _autodevice(_fake_torch(cuda=True)) == "cuda"
    assert _autodevice(_fake_torch(mps=True)) == "mps"
    assert _autodevice(_fake_torch()) == "cpu"
    no_mps = _fake_torch()
    no_mps.backends = types.SimpleNamespace()
    assert _autodevice(no_mps) == "cpu"


def test_clip_embed_is_unit_norm_and_loads_model_once(monkeypatch, img_ref):
    from lookbook.embedders.clip import CLIPEmbedder

    class Model(_Loadable):
        loads: list = []

        def get_image_features(self, **inputs):
            return _T([[3.0, 4.0]])

    class Proc(_Loadable):
        loads: list = []

        def __call__(self, images, return_tensors):
            return {"pixel_values": _T([[0.0]])}

    tf = types.ModuleType("transformers")
    tf.CLIPModel, tf.CLIPProcessor = Model, Proc
    _install(monkeypatch, torch=_fake_torch(), transformers=tf)
    emb = CLIPEmbedder()
    v = emb.embed(img_ref)
    assert np.allclose(v, [0.6, 0.8]) and v.dtype == np.float32
    emb.embed(img_ref)
    assert Model.loads == ["openai/clip-vit-base-patch32"]
    assert emb.config_hash == "clip:openai/clip-vit-base-patch32"


def test_clip_zero_vector_is_returned_unnormalised(monkeypatch, img_ref):
    from lookbook.embedders.clip import CLIPEmbedder

    class Model(_Loadable):
        loads: list = []

        def get_image_features(self, **inputs):
            return _T([[0.0, 0.0]])

    class Proc(_Loadable):
        loads: list = []

        def __call__(self, images, return_tensors):
            return {"x": _T([[0.0]])}

    tf = types.ModuleType("transformers")
    tf.CLIPModel, tf.CLIPProcessor = Model, Proc
    _install(monkeypatch, torch=_fake_torch(), transformers=tf)
    assert not CLIPEmbedder().embed(img_ref).any()


def test_dinov2_embed_uses_pooler_output(monkeypatch, img_ref):
    from lookbook.embedders.dinov2 import DINOv2Embedder

    class Model(_Loadable):
        loads: list = []

        def __call__(self, **inputs):
            return types.SimpleNamespace(pooler_output=_T([[0.0, 5.0, 12.0]]))

    class Proc(_Loadable):
        loads: list = []

        def __call__(self, images, return_tensors):
            return {"pixel_values": _T([[0.0]])}

    tf = types.ModuleType("transformers")
    tf.AutoModel, tf.AutoImageProcessor = Model, Proc
    _install(monkeypatch, torch=_fake_torch(), transformers=tf)
    emb = DINOv2Embedder()
    assert np.allclose(emb.embed(img_ref), np.array([0, 5, 12]) / 13)
    assert emb.config_hash == "dinov2:facebook/dinov2-base"


@pytest.mark.parametrize(
    "module, cls, missing",
    [
        ("lookbook.embedders.clip", "CLIPEmbedder", "torch"),
        ("lookbook.embedders.dinov2", "DINOv2Embedder", "torch"),
        ("lookbook.embedders.arcface", "InsightFaceArcFace", "insightface.app"),
    ],
)
def test_missing_dependency_gives_install_hint(monkeypatch, img_ref, module, cls, missing):
    import importlib

    _install(monkeypatch, **{missing: None})  # None in sys.modules: import fails
    emb = getattr(importlib.import_module(module), cls)()
    with pytest.raises(ImportError, match="requires"):
        emb.embed(img_ref)


def test_arcface_picks_the_largest_face_and_normalises(monkeypatch, img_ref):
    from lookbook.embedders.arcface import InsightFaceArcFace

    def face(bbox, emb):
        return types.SimpleNamespace(bbox=bbox, embedding=emb)

    class FaceAnalysis:
        faces: list = []

        def __init__(self, name):
            self.name = name

        def prepare(self, ctx_id, det_size):
            self.det_size = det_size

        def get(self, arr):
            return self.faces

    app_mod = types.ModuleType("insightface.app")
    app_mod.FaceAnalysis = FaceAnalysis
    pkg = types.ModuleType("insightface")
    pkg.app = app_mod
    _install(monkeypatch, insightface=pkg, **{"insightface.app": app_mod})

    emb = InsightFaceArcFace()
    assert emb.config_hash == "arcface:buffalo_l:640"
    FaceAnalysis.faces = []
    z = emb.embed(img_ref)
    assert z.shape == (512,) and not z.any()
    FaceAnalysis.faces = [
        face([0, 0, 2, 2], [1.0, 0.0]),
        face([0, 0, 10, 10], [0.0, 2.0]),
        face([5, 5, 3, 3], [9.0, 9.0]),  # negative extent: zero area
    ]
    assert np.allclose(emb.embed(img_ref), [0.0, 1.0])
