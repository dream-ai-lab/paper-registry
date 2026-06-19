# paper-registry

The central catalog of **eval contracts** — one `eval_spec.yaml` per paper,
plus the `baseline_registry.yaml` of accepted reproduce runs. This is the
single source of truth for "how is paper X evaluated".

```
paper-registry/
├── baseline_registry.yaml        # accepted reproduce run id + score per paper
├── <paper-id>/
│   ├── eval_spec.yaml            # pinned dataset + model + metrics (the contract)
│   └── paper_meta.yaml           # title, authors, url
└── validate.py                   # checks every spec against the standard
```

## Who edits this

A **survey member** opens a PR adding/changing an `eval_spec.yaml`. CI validates
it against the pinned [`eval-lib`](https://github.com/dream-ai-lab/eval-lib)
(pinned dataset+model revisions, known metrics, required fields) before merge.
No code is run here — just the contract.

## When must a spec be registered here?

Two different "musts" — don't confuse them:

- **Mandatory (technical):** every run needs a *valid* `eval_spec.yaml` —
  `eval-lib`'s `run_paper` logs its `eval_spec_hash` and attaches the file as an
  artifact. **Where the spec lives is your choice** (`run_paper` reads any local
  path). Comparability comes from the **hash**, not the location: two runs with
  the same `eval_spec_hash` are comparable even if the specs lived in different
  repos.
- **Mandatory (policy):** for any *shared/official* paper, the canonical spec
  lives **here**, so there is exactly one reviewed contract per `paper_id`.

| Register here (PR a spec) | Skip — keep the spec in your own repo |
|---|---|
| Paper is reproduced by more than one person | Quick personal / throwaway experiment |
| A result will become a **baseline** others compare to | Still iterating; register once it stabilises |
| You want it discoverable + reviewed | Private exploration |
| Every metric is **standard** (lives in `eval-lib`) | Uses an **experimental** metric (`metrics.experimental`) |

Rule of thumb: **register before a result becomes a baseline.** Never let two
divergent specs exist for the same `paper_id`.

A spec that declares `metrics.experimental` is by definition not yet canonical —
its metric lives in the experiment, not `eval-lib`, and its runs are tagged
`eval_tier=experimental`. `validate.py` **rejects** such specs here. Promote the
metric into `eval-lib` first (bump its version, drop the name from
`experimental`), then register the now-standard spec.

## Avoiding spec drift

If an experiment repo **copies** a spec from here, keep it byte-identical — the
`eval_spec_hash` will reveal any divergence when runs are compared. For strict
single-source, reference this registry instead (git submodule, as
`eval-pipeline` does, or fetch by commit) rather than copying.

## Use a spec in an experiment

Experiment repos (created from
[`experiment-template`](https://github.com/dream-ai-lab/experiment-template))
copy the relevant `eval_spec.yaml` and pin it. The `eval_spec_hash` logged with
every run ties a result back to the exact contract here.

## Validate locally

```bash
pip install "git+https://github.com/dream-ai-lab/eval-lib@v0.1.0"
python validate.py
```
