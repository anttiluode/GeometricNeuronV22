#!/usr/bin/env python3
from __future__ import annotations

import json
from urllib.parse import urlencode
from urllib.request import urlopen

TARGETS = ["1833", "2057", "1496", "1204", "1148", "1125"]
ENDPOINT = "https://neuromorpho.org/api/neuron/select/"

for target in TARGETS:
    url = ENDPOINT + "?" + urlencode({"q": f"neuron_name:{target}*"})
    payload = json.load(urlopen(url, timeout=60))
    records = payload.get("_embedded", {}).get("neuronResources", [])
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
    print(json.dumps({"target": target, "matches": compact}))
