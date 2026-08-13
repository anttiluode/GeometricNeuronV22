#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from geometric_neuron_v22 import full_feature_row, load_neurom_cable_tree

ALLEN_SPECIMENS = (
    548494556,
    528614014,
    539661667,
    569818704,
    790872626,
    558211203,
)


def apply_diameter_floor(source: Path, target: Path, minimum_diameter: float = 0.3) -> int:
    """Write an SWC with radius >= minimum_diameter / 2 and return edit count."""
    minimum_radius = minimum_diameter / 2.0
    edits = 0
    output = []
    for line in source.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            output.append(line)
            continue
        fields = line.split()
        if len(fields) >= 7 and float(fields[5]) < minimum_radius:
            fields[5] = f"{minimum_radius:.8g}"
            line = " ".join(fields)
            edits += 1
        output.append(line)
    target.write_text("\n".join(output) + "\n", encoding="utf-8")
    return edits


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work-dir", type=Path, required=True)
    ap.add_argument("--receipt", type=Path, required=True)
    args = ap.parse_args()

    from allensdk.api.queries.cell_types_api import CellTypesApi

    args.work_dir.mkdir(parents=True, exist_ok=True)
    api = CellTypesApi()
    receipt = []

    for specimen_id in ALLEN_SPECIMENS:
        raw = args.work_dir / f"{specimen_id}.swc"
        floored = args.work_dir / f"{specimen_id}_dmin03.swc"
        api.save_reconstruction(specimen_id, str(raw))
        edits = apply_diameter_floor(raw, floored)
        tree = load_neurom_cable_tree(floored)
        row = {
            "specimen_id": specimen_id,
            "source": "Allen Cell Types specimen reconstruction",
            "diameter_floor_um": 0.3,
            "radius_values_raised": edits,
            "raw_sha256": sha256(raw),
            "floored_sha256": sha256(floored),
            **full_feature_row(tree),
        }
        receipt.append(row)
        print(
            specimen_id,
            f"edits={edits}",
            f"nodes={row['n_nodes']}",
            f"area={row['total_dendritic_area']:.3f}",
        )

    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
