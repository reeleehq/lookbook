# lookbook.scorers

Scorers: per-image annotation producers.

Each submodule registers its scorers into `lookbook.registry.scorers` on
import. Heavy ML deps must be lazy-imported inside scorer methods, never at
module top.

### Modules

| [`identity`](lookbook.scorers.identity.html.md#module-lookbook.scorers.identity)   | Cross-image identity / likeness scorer — compare a candidate to a reference.   |
|----------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| [`person`](lookbook.scorers.person.html.md#module-lookbook.scorers.person)       | Person-LoRA scorers — Phase 3.                                                 |
| [`technical`](lookbook.scorers.technical.html.md#module-lookbook.scorers.technical) | Technical scorers — Phase 0/1.                                                 |
