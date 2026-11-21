# lookbook.io.ingest

### lookbook.io.ingest(source)

Materialize a source into a list of ImageRefs.

```pycon
>>> import tempfile, os
>>> with tempfile.TemporaryDirectory() as d:
...     for name in ['a.jpg', 'b.png', 'note.txt']:
...         open(os.path.join(d, name), 'wb').close()
...     refs = ingest(d)
>>> sorted(os.path.basename(r.path) for r in refs)
['a.jpg', 'b.png']
```

* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`ImageRef`](lookbook.base.html.md#lookbook.base.ImageRef)]
