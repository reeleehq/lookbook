# lookbook.profiles

Subject profiles — declarative recipes loaded from YAML.

A profile is just a recipe with a name and a YAML file. The schema mirrors
the in-code `RECIPES` dict in `lookbook/__main__.py`:

> name: person
> description: short description shown in `lookbook list-recipes`
> scorers: [scorer_id, …]
> embedders: [embedder_id, …]   # optional
> filters: [filter_id, …]       # may include [name, kwargs] entries
> selector: selector_id           # may be [name, kwargs]
> diagnose_clusters: 12           # optional
> constraints: { … }            # default constraints (e.g. quotas)

Profiles ship in `lookbook/profiles/*.yaml`. Users can override or add
profiles by dropping YAML files into `<config_root>/profiles/` (resolved
via `config2py`).

### Functions

| [`list_profiles`](#lookbook.profiles.list_profiles)()   | All profile names available, shipped + user-defined.    |
|--------------------------------------------------------------------|---------------------------------------------------------|
| [`load`](#lookbook.profiles.load)(name)        | Load a profile by name, returning a recipe-shaped dict. |

### lookbook.profiles.list_profiles()

All profile names available, shipped + user-defined.

User profiles override shipped ones with the same name.

* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

### lookbook.profiles.load(name)

Load a profile by name, returning a recipe-shaped dict.

Raises `KeyError` if the profile is unknown.

```pycon
>>> spec = load("person")
>>> "scorers" in spec
True
```

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)
