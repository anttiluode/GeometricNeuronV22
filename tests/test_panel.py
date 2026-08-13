import csv
import unittest
from pathlib import Path

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


class PanelReceiptTests(unittest.TestCase):
    def test_complete_exact_receipt_is_gate_ready(self):
        rows = validate_receipt(receipt(), gate_ready=True)
        self.assertEqual(len(rows), 24)
        self.assertEqual(receipt_summary(rows)["gate_compatible"], 24)

    def test_target_columns_are_rejected_before_unsealing(self):
        rows = receipt()
        rows[0]["FCI"] = 0.42
        with self.assertRaisesRegex(ValueError, "target-like"):
            validate_receipt(rows)

    def test_unresolved_row_blocks_gate_but_not_recovery_audit(self):
        rows = receipt()
        rows[0]["status"] = "unresolved"
        rows[0]["path"] = ""
        validate_receipt(rows, gate_ready=False)
        with self.assertRaisesRegex(ValueError, "blocks gate"):
            validate_receipt(rows, gate_ready=True)

    def test_manifest_identity_mismatch_is_rejected(self):
        rows = receipt()
        rows[3]["identifier"] = "something-close"
        with self.assertRaisesRegex(ValueError, "identifier"):
            validate_receipt(rows)

    def test_frozen_csv_panel_is_exactly_16_plus_8(self):
        path = Path(__file__).parents[1] / "data" / "frozen_panel_v01.csv"
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 24)
        resolved = [row for row in rows if row["status"] != "unresolved"]
        unresolved = [row for row in rows if row["status"] == "unresolved"]
        self.assertEqual(len(resolved), 16)
        self.assertEqual(len(unresolved), 8)

        for expected, row in zip(MANIFEST, rows):
            order, species, layer, identifier, source = expected
            self.assertEqual(int(row["order"]), order)
            self.assertEqual(row["species"], species)
            self.assertEqual(row["layer"], layer)
            self.assertEqual(row["identifier"], identifier)
            self.assertEqual(row["source"], source)
            if row["status"] == "unresolved":
                self.assertEqual(row["total_dendritic_area"], "")
                self.assertEqual(row["g1_spectral_entropy"], "")
            else:
                self.assertNotEqual(row["content_hash"], "")
                self.assertNotEqual(row["total_dendritic_area"], "")
                self.assertNotEqual(row["longest_root_to_tip_path"], "")
                self.assertNotEqual(row["g1_spectral_entropy"], "")
                self.assertNotEqual(row["g2_root_participation_entropy"], "")
                self.assertNotEqual(row["g3_log_spacing_irregularity"], "")


if __name__ == "__main__":
    unittest.main()
