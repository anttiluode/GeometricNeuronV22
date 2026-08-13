#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

from geometric_neuron_v22 import full_feature_row, load_neurom_cable_tree

TARGETS = {
    "1833": "1833_Mohan_etal_2015",
    "1496": "1496_Mohan_etal_2015",
    "1204": "1204_Mohan_etal_2015",
    "1148": "1148_Mohan_etal_2015",
    "1125": "1125_Mohan_etal_2015",
}

CNG_URL = (
    "https://neuromorpho.org/dableFiles/dekock/"
    "CNG%20version/{name}.CNG.swc"
)


def floor_swc_diameter(source: Path, target: Path, minimum_diameter: float = 0.3) -> int:
    minimum_radius = minimum_diameter / 2.0
    edits = 0
    lines = []
    for line in source.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            lines.append(line)
            continue
        fields = line.split()
        if len(fields) >= 7 and float(fields[5]) < minimum_radius:
            fields[5] = f"{minimum_radius:.8g}"
            line = " ".join(fields)
            edits += 1
        lines.append(line)
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return edits


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work-dir", type=Path, required=True)
    ap.add_argument("--receipt", type=Path, required=True)
    args = ap.parse_args()
    args.work_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for identifier, name in TARGETS.items():
        source_url = CNG_URL.format(name=quote(name, safe="_-."))
        raw = args.work_dir / f"{name}.CNG.swc"
        floored = args.work_dir / f"{name}_dmin03.CNG.swc"
        raw.write_bytes(urlopen(source_url, timeout=60).read())
        edits = floor_swc_diameter(raw, floored)
        tree = load_neurom_cable_tree(floored)
        row = {
            "table_identifier": identifier,
            "neuron_name": name,
            "archive": "DeKock",
            "representation": "NeuroMorpho standardized CNG SWC",
            "source_url": source_url,
            "diameter_floor_um": 0.3,
            "radius_values_raised": edits,
            "raw_sha256": digest(raw),
            "floored_sha256": digest(floored),
            **full_feature_row(tree),
        }
        rows.append(row)
        print(
            identifier,
            f"edits={edits}",
            f"nodes={row['n_nodes']}",
            f"length={row['total_dendritic_length']:.3f}",
            f"area={row['total_dendritic_area']:.3f}",
            "G=("
            f"{row['g1_spectral_entropy']:.4f},"
            f"{row['g2_root_participation_entropy']:.4f},"
            f"{row['g3_log_spacing_irregularity']:.4f})",
            flush=True,
        )

    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(rows, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
