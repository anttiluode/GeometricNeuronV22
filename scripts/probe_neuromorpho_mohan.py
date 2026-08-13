#!/usr/bin/env python3
from __future__ import annotations

import json
from urllib.parse import urlencode
from urllib.request import urlopen

ENDPOINT = "https://neuromorpho.org/api/neuron/select/"


def query(pattern: str) -> list[dict]:
    url = ENDPOINT + "?" + urlencode({"q": f"neuron_name:{pattern}"})
    payload = json.load(urlopen(url, timeout=60))
    return payload.get("_embedded", {}).get("neuronResources", [])


for target in ["1833", "2057", "1496", "1204", "1148", "1125"]:
    records = query(f"{target}*")
    compact = [
        {
            "neuron_id": row.get("neuron_id"),
            "neuron_name": row.get("neuron_name"),
            "archive": row.get("archive"),
            "species": row.get("species"),
            "brain_region": row.get("brain_region"),
            "original_format": row.get("original_format"),
        }
        for row in records
        if "mohan" in str(row.get("neuron_name", "")).lower()
        or str(row.get("archive", "")).lower() == "dekock"
    ]
    print(json.dumps({"family": "Mohan", "target": target, "matches": compact}))


for target in ["229_5", "229_1", "230_1", "230_2", "232_1"]:
    records = query(f"*{target}*")
    compact = [
        {
            "neuron_id": row.get("neuron_id"),
            "neuron_name": row.get("neuron_name"),
            "archive": row.get("archive"),
            "species": row.get("species"),
            "brain_region": row.get("brain_region"),
            "cell_type": row.get("cell_type"),
            "original_format": row.get("original_format"),
        }
        for row in records[:50]
    ]
    print(json.dumps({"family": "Markram", "target": target, "matches": compact}))
