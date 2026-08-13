#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from morphio.mut import Morphology


def floor_file(source: Path, target: Path, minimum: float) -> int:
    morph = Morphology(source)
    edits = 0
    for section in morph.iter():
        values = np.asarray(section.diameters, dtype=float).copy()
        mask = values < minimum
        edits += int(mask.sum())
        if np.any(mask):
            values[mask] = minimum
            section.diameters = values
    soma = np.asarray(morph.soma.diameters, dtype=float).copy()
    if soma.size:
        mask = soma < minimum
        edits += int(mask.sum())
        if np.any(mask):
            soma[mask] = minimum
            morph.soma.diameters = soma
    morph.write(target)
    return edits


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path)
    ap.add_argument("target", type=Path)
    ap.add_argument("--minimum", type=float, default=0.3)
    args = ap.parse_args()
    edits = floor_file(args.source, args.target, args.minimum)
    print(f"diameter_values_raised={edits}")


if __name__ == "__main__":
    main()
