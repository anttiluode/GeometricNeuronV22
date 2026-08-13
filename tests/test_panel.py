import pytest

from geometric_neuron_v22.panel import MANIFEST, receipt_summary, validate_receipt


def receipt(status="author_exact"):
    rows = []
    for order, species, layer, identifier, source in MANIFEST:
        row = {
            "order": order,
            "species": species,
            "layer": layer,
            "identifier": identifier,
            "source": source,
            "status": status,
            "path": f"morph/{order:02d}.swc" if status != "unresolved" else "",
        }
        if status == "source_compatible":
            row["diameter_floor_applied"] = True
        rows.append(row)
    return rows


def test_complete_exact_receipt_is_gate_ready():
    rows = validate_receipt(receipt(), gate_ready=True)
    assert len(rows) == 24
    assert receipt_summary(rows)["gate_compatible"] == 24


def test_target_columns_are_rejected_before_unsealing():
    rows = receipt()
    rows[0]["FCI"] = 0.42
    with pytest.raises(ValueError, match="target-like"):
        validate_receipt(rows)


def test_unresolved_row_blocks_gate_but_not_recovery_audit():
    rows = receipt()
    rows[0]["status"] = "unresolved"
    rows[0]["path"] = ""
    validate_receipt(rows, gate_ready=False)
    with pytest.raises(ValueError, match="blocks gate"):
        validate_receipt(rows, gate_ready=True)


def test_manifest_identity_mismatch_is_rejected():
    rows = receipt()
    rows[3]["identifier"] = "something-close"
    with pytest.raises(ValueError, match="identifier"):
        validate_receipt(rows)
