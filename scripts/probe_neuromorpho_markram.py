#!/usr/bin/env python3
from __future__ import annotations

import json
from urllib.parse import urlencode
from urllib.request import urlopen

TARGETS = ["229_5", "229_1", "230_1", "230_2", "232_1"]
ENDPOINT = "https://neuromorpho.org/api/neuron/select/"

for target in TARGETS:
    url = ENDPOINT + "?" + urlencode({"q": f"neuron_name:*{target}*"})
    payload = json.load(urlopen(url, timeout=60))
    records = payload.get("_embedded", {}).get("neuronResources", [])
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
    print(json.dumps({"target": target, "matches": compact}))
