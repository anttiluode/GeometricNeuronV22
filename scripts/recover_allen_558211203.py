#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from geometric_neuron_v22 import full_feature_row, load_neurom_cable_tree
from recover_allen_table_s1 import apply_diameter_floor, fetch_reconstruction, sha256

SPECIMEN_ID = 558211203

raw = Path("data/allen") / f"{SPECIMEN_ID}.swc"
floored = Path("data/allen") / f"{SPECIMEN_ID}_dmin03.swc"
link = fetch_reconstruction(SPECIMEN_ID, raw)
edits = apply_diameter_floor(raw, floored)
tree = load_neurom_cable_tree(floored)
row = {
    "specimen_id": SPECIMEN_ID,
    "source": "Allen Cell Types specimen reconstruction",
    "download_link": link,
    "diameter_floor_um": 0.3,
    "radius_values_raised": edits,
    "raw_sha256": sha256(raw),
    "floored_sha256": sha256(floored),
    **full_feature_row(tree),
}
Path("artifacts").mkdir(exist_ok=True)
Path("artifacts/allen_558211203.json").write_text(json.dumps(row, indent=2), encoding="utf-8")
print(json.dumps(row, indent=2))
