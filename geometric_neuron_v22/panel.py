from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping

# Frozen Supplementary Table 1 identity/order; no FCI values live here.
MANIFEST = [
    (1,"Rat","L2/3","L2 TPC","Reimann 2024"),(2,"Rat","L6","L6 IPC","Reimann 2024"),
    (3,"Rat","L4","L4 TPC","Reimann 2024"),(4,"Rat","L6","L6 TPC","Reimann 2024"),
    (5,"Rat","L2/3","229_5","Markram 2015"),(6,"Rat","L2/3","229_1","Markram 2015"),
    (7,"Rat","L5","cell1","Hay 2011"),(8,"Rat","L4","230_1","Markram 2015"),
    (9,"Rat","L6","L6 UPC","Reimann 2024"),(10,"Rat","L4","230_2","Markram 2015"),
    (11,"Rat","L5","TTPC_1 232_1","Markram 2015"),(12,"Rat","L5","L5 TPC","Reimann 2024"),
    (13,"Human","L6","548494556","Allen 2015"),(14,"Human","L6","528614014","Allen 2015"),
    (15,"Human","L5","1833","Mohan 2015"),(16,"Human","L4","539661667","Allen 2015"),
    (17,"Human","L5","2057","Mohan 2015"),(18,"Human","L4","569818704","Allen 2015"),
    (19,"Human","L5","790872626","Allen 2015"),(20,"Human","L4","1496","Mohan 2015"),
    (21,"Human","L6","558211203","Allen 2015"),(22,"Human","L2/3","1204","Mohan 2015"),
    (23,"Human","L2/3","1148","Mohan 2015"),(24,"Human","L2/3","1125","Mohan 2015"),
]

STATUSES = {"author_exact", "source_compatible", "unresolved"}
FORBIDDEN = ("fci", "auc", "target", "label", "complexity_score")


def validate_receipt(rows: Iterable[Mapping[str, object]], *, gate_ready: bool = False):
    """Validate the 24-row morphology receipt before target labels are opened."""
    rows = [dict(r) for r in rows]
    if len(rows) != 24:
        raise ValueError(f"expected 24 rows, got {len(rows)}")
    by_order = {}
    used_paths = set()
    for row in rows:
        bad = next((k for k in row if any(t in str(k).lower() for t in FORBIDDEN)), None)
        if bad:
            raise ValueError(f"target-like field forbidden: {bad}")
        order = int(row["order"])
        if order in by_order:
            raise ValueError(f"duplicate order {order}")
        by_order[order] = row
    if set(by_order) != set(range(1, 25)):
        raise ValueError("receipt orders must be exactly 1..24")

    out = []
    for order, species, layer, identifier, source in MANIFEST:
        row = by_order[order]
        expected = {"species": species, "layer": layer, "identifier": identifier, "source": source}
        for key, value in expected.items():
            if str(row.get(key, "")) != value:
                raise ValueError(f"order {order}: {key} must be {value!r}")
        status = str(row.get("status", ""))
        if status not in STATUSES:
            raise ValueError(f"order {order}: invalid status {status!r}")
        path = str(row.get("path", "")).strip()
        if status == "unresolved":
            if path:
                raise ValueError(f"order {order}: unresolved row cannot have path")
            if gate_ready:
                raise ValueError(f"order {order}: unresolved morphology blocks gate")
        else:
            if not path:
                raise ValueError(f"order {order}: resolved row requires path")
            path_key = str(Path(path))
            if path_key in used_paths:
                raise ValueError(f"duplicate morphology path: {path_key}")
            used_paths.add(path_key)
        if status == "source_compatible" and "diameter_floor_applied" not in row:
            raise ValueError(f"order {order}: record diameter_floor_applied")
        out.append({**expected, "order": order, "status": status, "path": path,
                    "diameter_floor_applied": bool(row.get("diameter_floor_applied", False)),
                    "provenance_note": str(row.get("provenance_note", ""))})
    return out


def receipt_summary(rows: Iterable[Mapping[str, object]]):
    rows = validate_receipt(rows)
    counts = {s: sum(r["status"] == s for r in rows) for s in sorted(STATUSES)}
    counts["gate_compatible"] = counts["author_exact"] + counts["source_compatible"]
    return counts
