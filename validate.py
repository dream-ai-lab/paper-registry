"""Validate every eval_spec.yaml in the registry against the standard.

Run locally or in CI after `pip install eval-lib`. Fails if any spec is
malformed: unpinned dataset/model, unknown metric, or missing fields.
"""

import glob
import sys

from eval_lib import load_spec

specs = sorted(glob.glob("*/eval_spec.yaml"))
if not specs:
    sys.exit("no eval_spec.yaml found")

for path in specs:
    spec = load_spec(path)  # raises SpecError if invalid
    print(f"valid: {path:42} {spec.paper_id:22} {spec.hash}")

print(f"\n{len(specs)} spec(s) valid")
