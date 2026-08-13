#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from geometric_neuron_v22 import full_feature_row, load_neurom_cable_tree


VALID_SUFFIXES = {".asc", ".swc", ".h5"}


def collect_paths(inputs: list[Path]) -> list[Path]:
    out: list[Path] = []
    for item in inputs:
        if item.is_dir():
            out.extend(
                p for p in item.rglob("*")
                if p.is_file() and p.suffix.lower() in VALID_SUFFIXES
            )
        elif item.is_file() and item.suffix.lower() in VALID_SUFFIXES:
            out.append(item)
        else:
            raise FileNotFoundError(f"unsupported or missing morphology path: {item}")
    return sorted(set(p.resolve() for p in out))


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Extract frozen V22 morphology/operator features without FCI labels."
    )
    ap.add_argument("inputs", nargs="+", type=Path)
    ap.add_argument("--k", type=int, default=16)
    ap.add_argument("--csv", type=Path)
    ap.add_argument("--json", type=Path)
    args = ap.parse_args()

    paths = collect_paths(args.inputs)
    if not paths:
        raise SystemExit("no morphology files found")

    rows = []
    for path in paths:
        tree = load_neurom_cable_tree(path)
        row = {
            "path": str(path),
            "file": path.name,
            **full_feature_row(tree, k=args.k),
        }
        rows.append(row)
        print(
            f"{path.name}: nodes={row['n_nodes']} "
            f"length={row['total_dendritic_length']:.3f} "
            f"area={row['total_dendritic_area']:.3f} "
            f"G=({row['g1_spectral_entropy']:.4f}, "
            f"{row['g2_root_participation_entropy']:.4f}, "
            f"{row['g3_log_spacing_irregularity']:.4f})"
        )

    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(rows, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
