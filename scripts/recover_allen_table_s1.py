#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

from geometric_neuron_v22 import full_feature_row, load_neurom_cable_tree

# 790872626 is currently unresolved in both Specimen and NeuronReconstruction
# queries. Keep it literal, but put it last so all resolvable Table-S1 Allen
# cells are audited before the script stops on the provenance failure.
ALLEN_SPECIMENS = (
    548494556,
    528614014,
    539661667,
    569818704,
    558211203,
    790872626,
)
API = "http://api.brain-map.org"


def apply_diameter_floor(source: Path, target: Path, minimum_diameter: float = 0.3) -> int:
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


def fetch_reconstruction(specimen_id: int, target: Path) -> str:
    criteria = f"[id$eq{specimen_id}],neuron_reconstructions(well_known_files)"
    include = (
        "neuron_reconstructions(well_known_files("
        "well_known_file_type[name$eq'3DNeuronReconstruction']))"
    )
    rma = f"model::Specimen,rma::criteria,{criteria},rma::include,{include}"
    query_url = API + "/api/v2/data/query.json?" + urlencode({"q": rma})
    payload = json.load(urlopen(query_url, timeout=60))
    results = payload.get("msg", [])
    if not results:
        raise RuntimeError(f"Allen API returned no specimen {specimen_id}")
    reconstructions = results[0].get("neuron_reconstructions", [])
    if not reconstructions:
        raise RuntimeError(f"specimen {specimen_id} has no reconstruction")
    files = reconstructions[0].get("well_known_files", [])
    if not files:
        raise RuntimeError(f"specimen {specimen_id} has no reconstruction file")
    download_link = files[0]["download_link"]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(urlopen(API + download_link, timeout=60).read())
    return download_link


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work-dir", type=Path, required=True)
    ap.add_argument("--receipt", type=Path, required=True)
    args = ap.parse_args()

    args.work_dir.mkdir(parents=True, exist_ok=True)
    receipt = []

    for specimen_id in ALLEN_SPECIMENS:
        raw = args.work_dir / f"{specimen_id}.swc"
        floored = args.work_dir / f"{specimen_id}_dmin03.swc"
        download_link = fetch_reconstruction(specimen_id, raw)
        edits = apply_diameter_floor(raw, floored)
        tree = load_neurom_cable_tree(floored)
        row = {
            "specimen_id": specimen_id,
            "source": "Allen Cell Types specimen reconstruction",
            "download_link": download_link,
            "diameter_floor_um": 0.3,
            "radius_values_raised": edits,
            "raw_sha256": sha256(raw),
            "floored_sha256": sha256(floored),
            **full_feature_row(tree),
        }
        receipt.append(row)
        print(specimen_id, f"edits={edits}", f"nodes={row['n_nodes']}")

    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
