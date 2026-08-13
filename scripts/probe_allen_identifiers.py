#!/usr/bin/env python3
from __future__ import annotations

import json
from urllib.parse import urlencode
from urllib.request import urlopen

# Keep the Table-S1 IDs literal. A zero match is an unresolved provenance result,
# not permission to substitute a nearby specimen.
IDENTIFIERS = [548494556, 528614014, 539661667, 569818704, 790872626, 558211203]
API = "http://api.brain-map.org"


def query(stage: str):
    url = API + "/api/v2/data/query.json?" + urlencode({"q": stage})
    return json.load(urlopen(url, timeout=60)).get("msg", [])


for identifier in IDENTIFIERS:
    specimens = query(
        f"model::Specimen,rma::criteria,[id$eq{identifier}],"
        "rma::include,neuron_reconstructions(well_known_files)"
    )
    reconstructions = query(
        f"model::NeuronReconstruction,rma::criteria,[id$eq{identifier}],"
        "rma::include,specimen,well_known_files"
    )
    print(json.dumps({
        "identifier": identifier,
        "specimen_matches": len(specimens),
        "reconstruction_matches": len(reconstructions),
        "specimen_id_from_reconstruction": (
            (reconstructions[0].get("specimen") or {}).get("id")
            if reconstructions else None
        ),
    }))
