"""Validate every eval_spec.yaml in the registry against the standard.

Run locally or in CI after `pip install eval-lib`. Fails if any spec is
malformed: unpinned dataset/model, unknown metric, or missing fields.
"""

import glob
import sys

import yaml

from eval_lib import load_spec


def _declares_experimental(path: str) -> bool:
    """True if the spec declares metrics.experimental.

    Read directly from YAML so the check is independent of the pinned eval-lib
    version (older versions ignore the field).
    """
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    return bool((raw.get("metrics") or {}).get("experimental"))


specs = sorted(glob.glob("*/eval_spec.yaml"))
if not specs:
    sys.exit("no eval_spec.yaml found")

for path in specs:
    spec = load_spec(path)  # raises SpecError if invalid
    # The registry holds canonical contracts only. Experimental metrics are
    # supplied at runtime in an experiment repo and tagged eval_tier=experimental;
    # a spec using one is not yet a baseline and must not be registered here.
    if _declares_experimental(path):
        sys.exit(
            f"{path}: declares metrics.experimental — the registry holds canonical "
            "contracts only. Keep it in your experiment repo; register here after "
            "promoting the metric into eval-lib and dropping it from experimental."
        )
    print(f"valid: {path:42} {spec.paper_id:22} {spec.hash}")

print(f"\n{len(specs)} spec(s) valid")
