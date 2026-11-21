# lookbook.interactive

Interactive curate loop — keep the human in the loop.

The non-interactive [`lookbook.curate()`](lookbook.html.md#lookbook.curate) runs the pipeline once
and returns its top-k. That works for fully-automated workflows but
loses the human’s taste signal: a ranking that ranks “boring but
high-quality” images above “stylistically perfect but slightly
blurry” ones.

[`curate_interactive()`](#lookbook.interactive.curate_interactive) invites the caller into the loop. Each
round:

1. The pipeline picks the top `present` unseen candidates.
2. The caller’s `on_decision(refs, info)` returns an
   [`InteractiveDecision`](#lookbook.interactive.InteractiveDecision) saying which to keep, which to
   > reject, and whether to stop.
3. Kept refs lock into the final selection. Rejected refs leave the
   candidate pool and won’t be shown again. Everything else is
   eligible to come back next round (handy when the caller wants to
   defer a decision).
4. The loop terminates when the caller says `stop`, when the
   confirmed-kept set reaches `k`, when the candidate pool is
   exhausted, or when `max_rounds` is reached.

Two `on_decision` shapes are supported:

- A function: `on_decision(refs, info) -> InteractiveDecision`.
- A list of pre-recorded [`InteractiveDecision`](#lookbook.interactive.InteractiveDecision) items, applied
  one per round. Useful for tests and headless replays.

### Functions

| [`curate_interactive`](#lookbook.interactive.curate_interactive)(source, \*, on_decision[, ...])   | Run the pipeline in rounds, taking keep/reject decisions per round.   |
|-------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|

### Classes

| [`InteractiveDecision`](#lookbook.interactive.InteractiveDecision)(\*[, keep, reject, stop])   | One round's verdict from the caller.   |
|--------------------------------------------------------------------------------------------------|----------------------------------------|

### *class* lookbook.interactive.InteractiveDecision(, keep=(), reject=(), stop=False)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

One round’s verdict from the caller.

#### keep

```
``
```

image_id\`\`s the caller wants to lock into the final
selection. They’re added immediately, removed from the
candidate pool, and not shown again.

* **Type:**
  [`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`...`](https://docs.python.org/3/builtins/constants.html#Ellipsis)]

#### reject

```
``
```

image_id\`\`s the caller never wants to see again in
this run.

* **Type:**
  [`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`...`](https://docs.python.org/3/builtins/constants.html#Ellipsis)]

#### stop

When True, the loop terminates after applying this
round’s keep/reject and returns whatever is in the
confirmed-kept set so far (clipped to `k`).

* **Type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)

### lookbook.interactive.curate_interactive(source, , on_decision, k=20, present=8, max_rounds=20, scorer_ids=('random_score',), embedder_ids=(), filter_ids=(), selector_id='top_k', stores=None, constraints=None)

Run the pipeline in rounds, taking keep/reject decisions per round.

Args mirror [`lookbook.curate()`](lookbook.html.md#lookbook.curate) plus:

* **Parameters:**
  * **on_decision** ([`Union`](https://docs.python.org/3/library/typing.html#typing.Union)[[`Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)[[[`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`ImageRef`](lookbook.base.html.md#lookbook.base.ImageRef)], [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]], [`InteractiveDecision`](#lookbook.interactive.InteractiveDecision)], [`Sequence`](https://docs.python.org/3/library/typing.html#typing.Sequence)[[`InteractiveDecision`](#lookbook.interactive.InteractiveDecision)]]) – A callable or a pre-recorded sequence of
    [`InteractiveDecision`](#lookbook.interactive.InteractiveDecision). The callable receives the
    round’s top candidates and an info dict
    `{round, n_kept_so_far, n_pool_remaining}`.
  * **present** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – How many candidates to surface per round.
  * **max_rounds** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Hard cap on iterations; a defensive guard against
    broken decision callables that never stop.
* **Return type:**
  [`RunResult`](lookbook.pipeline.html.md#lookbook.pipeline.RunResult)
* **Returns:**
  A `RunResult` whose `kept` list is the confirmed
  set (in the order they were kept). `candidates` carries the
  same as the final round’s pre-selection candidate pool.
