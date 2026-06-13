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
