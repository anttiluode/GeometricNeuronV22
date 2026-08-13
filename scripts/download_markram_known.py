#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.request import urlopen

SOURCES = {
    "229_1": "https://raw.githubusercontent.com/ModelDBRepository/260971/2bbd294c4c7e96ae8fcc45fbd2c6229ad4011b3c/L23PC/L23_PC_cADpyr229_1/morphology/dend-C170897A-P3_axon-C260897C-P4_-_Clone_4.asc",
    "229_5": "https://raw.githubusercontent.com/ModelDBRepository/260971/2bbd294c4c7e96ae8fcc45fbd2c6229ad4011b3c/L23PC/L23_PC_cADpyr229_5/morphology/dend-C260897C-P3_axon-C220797A-P3_-_Clone_0.asc",
    "TTPC_1 232_1": "https://raw.githubusercontent.com/BlueBrain/SimulationTutorials/master/YRE2016/NMC/L5_TTPC2_cADpyr232_1/morphology/dend-C060114A7_axon-C060116A3_-_Clone_2.asc",
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work-dir", type=Path, required=True)
    ap.add_argument("--receipt", type=Path, required=True)
    args = ap.parse_args()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for identifier, url in SOURCES.items():
        path = args.work_dir / (identifier.replace(" ", "_") + ".asc")
        path.write_bytes(urlopen(url, timeout=120).read())
        rows.append({"identifier": identifier, "url": url, "path": str(path)})
        print(identifier, path)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(rows, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
