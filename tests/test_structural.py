import unittest

from geometric_neuron_v22 import CableEdge, make_tree
from geometric_neuron_v22.structural import collapse_unifurcations


class StructuralCollapseTests(unittest.TestCase):
    def test_one_child_boundaries_are_removed_without_changing_cable_totals(self):
        raw = make_tree([
            CableEdge(0, 1, 1.0, 2.0),
            CableEdge(1, 2, 2.0, 3.0),
            CableEdge(2, 3, 3.0, 4.0),
            CableEdge(2, 4, 4.0, 5.0),
        ])
        out = collapse_unifurcations(raw)
        self.assertEqual(out.n_nodes, 4)
        self.assertAlmostEqual(out.total_length, raw.total_length)
        self.assertAlmostEqual(out.total_area, raw.total_area)
        self.assertAlmostEqual(out.longest_root_to_tip_path, raw.longest_root_to_tip_path)
        self.assertFalse(any(
            node != out.root and len(kids) == 1
            for node, kids in enumerate(out.children())
        ))


if __name__ == "__main__":
    unittest.main()
