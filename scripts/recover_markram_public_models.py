#!/usr/bin/env python3
"""Recover public source morphologies for Markram Table-S1 cells."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

from geometric_neuron_v22 import full_feature_row, load_neurom_cable_tree

TARGETS = (
    ("229_1", "ModelDBRepository/260971", "2bbd294c4c7e96ae8fcc45fbd2c6229ad4011b3c", "L23_PC_cADpyr229_1", "L23PC/L23_PC_cADpyr229_1/morphology/dend-C170897A-P3_axon-C260897C-P4_-_Clone_4.asc"),
    ("229_5", "ModelDBRepository/260971", "2bbd294c4c7e96ae8fcc45fbd2c6229ad4011b3c", "L23_PC_cADpyr229_5", "L23PC/L23_PC_cADpyr229_5/morphology/dend-C260897C-P3_axon-C220797A-P3_-_Clone_0.asc"),
    ("TTPC_1 232_1", "BlueBrain/SimulationTutorials", "master", "L5_TTPC2_cADpyr232_1", "YRE2016/NMC/L5_TTPC2_cADpyr232_1/morphology/dend-C060114A7_axon-C060116A3_-_Clone_2.asc"),
)


def floor_diameter(source: Path, target: Path, minimum: float = 0.3) -> int:
    radius = minimum / 2.0
    edits, out = 0, []
    for line in source.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s and not s.startswith("#"):
            fields = line.split()
            if len(fields) >= 7 and float(fields[5]) < radius:
                fields[5] = f"{radius:.8g}"
                line = " ".join(fields)
                edits += 1
        out.append(line)
    target.write_text("\n".join(out) + "\n", encoding="utf-8")
    return edits


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work-dir", type=Path, required=True)
    ap.add_argument("--receipt", type=Path, required=True)
    args = ap.parse_args()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for identifier, repo, ref, package, source_path in TARGETS:
        url = f"https://raw.githubusercontent.com/{repo}/{ref}/{source_path}"
        safe = identifier.replace(" ", "_")
        raw = args.work_dir / f"{safe}.asc"
        fixed = args.work_dir / f"{safe}_dmin03.asc"
        raw.write_bytes(urlopen(url, timeout=120).read())
        edits = floor_diameter(raw, fixed)
        row = {
            "table_identifier": identifier,
            "status": "source_compatible",
            "source_repository": repo,
            "source_ref": ref,
            "model_package": package,
            "source_path": source_path,
            "source_url": url,
            "diameter_floor_um": 0.3,
            "radius_values_raised": edits,
            "raw_sha256": sha256(raw),
            "floored_sha256": sha256(fixed),
            **full_feature_row(load_neurom_cable_tree(fixed)),
        }
        rows.append(row)
        print(identifier, package, f"edits={edits}", f"nodes={row['n_nodes']}", flush=True)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(rows, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
