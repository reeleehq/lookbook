"""Registry, run-report and CLI-function tests (no model weights, no network)."""

from __future__ import annotations

import json

import pytest

from lookbook import __main__ as cli
from lookbook import registry
from lookbook.report import Report


# --- registry --------------------------------------------------------------


def test_register_get_names_and_contains():
    r = registry._Registry[int]("widget")
    assert r.register("b", 2) == 2
    r.register("a", 1)
    assert r.names() == ["a", "b"]
    assert "a" in r and "z" not in r
    assert sorted(r) == ["a", "b"]
    assert r.get("a") == 1


def test_register_refuses_duplicates_unless_overwrite():
    r = registry._Registry[int]("widget")
    r.register("a", 1)
    with pytest.raises(KeyError, match="already registered"):
        r.register("a", 2)
    r.register("a", 3, overwrite=True)
    assert r.get("a") == 3


def test_get_unknown_lists_known_names():
    r = registry._Registry[int]("widget")
    r.register("a", 1)
    with pytest.raises(KeyError, match=r"No widget registered.*\['a'\]"):
        r.get("nope")


@pytest.mark.parametrize(
    "decorator, reg",
    [
        (registry.register_scorer, registry.scorers),
        (registry.register_filter, registry.filters),
        (registry.register_embedder, registry.embedders),
        (registry.register_selector, registry.selectors),
    ],
)
def test_decorators_register_and_return_the_object(decorator, reg):
    name = "_test_plugin_xyz"
    try:

        @decorator(name)
        def plugin():
            return 1

        assert reg.get(name) is plugin and plugin() == 1
        with pytest.raises(KeyError):
            decorator(name)(lambda: 2)
    finally:
        reg._items.pop(name, None)


# --- report ----------------------------------------------------------------


def test_report_to_dict_copies_containers():
    rep = Report(
        n_candidates=5,
        n_survivors=3,
        n_kept=2,
        dropped_by_filter={"blur": 2},
        scorer_ids=["s"],
        selector_id="topk",
        notes={"a": 1},
    )
    d = rep.to_dict()
    assert d["dropped_by_filter"] == {"blur": 2} and d["selector_id"] == "topk"
    d["dropped_by_filter"]["blur"] = 99
    assert rep.dropped_by_filter == {"blur": 2}


def test_report_human_lists_drops_sorted_by_count_and_notes():
    rep = Report(
        n_candidates=10,
        n_survivors=6,
        n_kept=3,
        dropped_by_filter={"small": 1, "blur": 3},
        notes={"why": "because"},
    )
    text = rep.human()
    assert "candidates: 10" in text and "kept:       3" in text
    assert text.index("blur: 3") < text.index("small: 1")
    assert "why: because" in text


def test_report_human_minimal():
    assert Report().human().splitlines() == [
        "candidates: 0",
        "survivors:  0",
        "kept:       0",
    ]


# --- CLI helpers -----------------------------------------------------------


def test_normalizers():
    assert cli._normalize_filter_specs(["a", ["b", {"x": 1}], ["c"]]) == [
        "a",
        ("b", {"x": 1}),
        ["c"],
    ]
    assert cli._normalize_selector_spec(["s", {"k": 1}]) == ("s", {"k": 1})
    assert cli._normalize_selector_spec("topk") == "topk"


def test_resolve_recipe_known_and_unknown():
    assert cli._resolve_recipe("random") is cli.RECIPES["random"]
    with pytest.raises(SystemExit, match="Unknown recipe/profile"):
        cli._resolve_recipe("definitely-not-a-recipe")


def test_list_plugins_and_recipes_print(capsys):
    cli.list_plugins()
    out = capsys.readouterr().out
    for kind in ("scorers:", "selectors:", "filters:", "embedders:"):
        assert kind in out
    cli.list_recipes()
    out = capsys.readouterr().out
    assert "random  [in-code]" in out and "selector:" in out


def test_list_recipes_reports_a_profile_that_fails_to_load(monkeypatch, capsys):
    monkeypatch.setattr(cli._profiles, "list_profiles", lambda: ["broken"])

    def boom(name):
        raise ValueError("bad yaml")

    monkeypatch.setattr(cli._profiles, "load", boom)
    cli.list_recipes()
    assert "broken  [profile]  (failed to load: bad yaml)" in capsys.readouterr().out


def test_curate_in_memory_prints_json_record(tmp_path, capsys):
    from PIL import Image

    for i in range(4):
        Image.new("RGB", (64 + i, 64), (10 * i, 20, 30)).save(tmp_path / f"{i}.png")
    cli.curate(str(tmp_path), k=2, recipe="diverse_mock", in_memory=True)
    record = json.loads(capsys.readouterr().out)
    assert isinstance(record, dict) and record


def test_serve_and_mcp_delegate(monkeypatch, capsys):
    import lookbook.http as http
    import lookbook.mcp as mcp_mod

    calls = []
    monkeypatch.setattr(http, "serve", lambda **kw: calls.append(("http", kw)))
    monkeypatch.setattr(mcp_mod, "serve", lambda **kw: calls.append(("mcp", kw)))
    cli.serve(host="0.0.0.0", port=9)
    cli.mcp(transport="sse")
    assert calls == [
        ("http", {"host": "0.0.0.0", "port": 9}),
        ("mcp", {"transport": "sse"}),
    ]
    assert "0.0.0.0:9" in capsys.readouterr().out


def test_main_runs_a_command(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["lookbook", "list-plugins"])
    assert cli.main() in (0, None)
    assert "scorers:" in capsys.readouterr().out
