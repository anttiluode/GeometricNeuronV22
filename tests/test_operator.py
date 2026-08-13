import unittest

import numpy as np

from geometric_neuron_v22 import CableEdge, make_tree, mass_normalized_laplacian, operator_features


def example_tree(scale=1.0):
    # Area scales quadratically under a geometric scale transform.
    a = scale * scale
    return make_tree([
        CableEdge(0, 1, 2.0 * scale, 4.0 * a),
        CableEdge(1, 2, 1.0 * scale, 2.0 * a),
        CableEdge(1, 3, 3.0 * scale, 3.0 * a),
        CableEdge(3, 4, 1.5 * scale, 1.5 * a),
        CableEdge(3, 5, 2.5 * scale, 2.5 * a),
    ])


class CableTreeTests(unittest.TestCase):
    def test_basic_morphology_metrics(self):
        tree = example_tree()
        self.assertEqual(tree.number_of_bifurcations, 2)
        self.assertEqual(tree.number_of_forking_points, 2)
        self.assertEqual(tree.number_of_leaves, 3)
        self.assertAlmostEqual(tree.total_length, 10.0)
        self.assertAlmostEqual(tree.total_area, 13.0)
        self.assertAlmostEqual(tree.longest_root_to_tip_path, 7.5)

    def test_operator_is_symmetric_and_has_one_zero_mode(self):
        tree = example_tree()
        matrix, mass = mass_normalized_laplacian(tree)
        self.assertTrue(np.all(mass > 0))
        self.assertTrue(np.allclose(matrix, matrix.T))
        values = np.linalg.eigvalsh(matrix)
        self.assertLess(abs(values[0]), 1e-10)
        self.assertTrue(np.all(values[1:] > 0))

    def test_frozen_features_ignore_uniform_geometric_scale(self):
        base = operator_features(example_tree(1.0), k=5)
        large = operator_features(example_tree(7.0), k=5)
        self.assertAlmostEqual(base.g1_spectral_entropy, large.g1_spectral_entropy, places=10)
        self.assertAlmostEqual(base.g2_root_participation_entropy, large.g2_root_participation_entropy, places=10)
        self.assertAlmostEqual(base.g3_log_spacing_irregularity, large.g3_log_spacing_irregularity, places=10)

    def test_same_total_length_can_have_different_operator_shape(self):
        a = make_tree([
            CableEdge(0, 1, 2.0, 2.0),
            CableEdge(1, 2, 2.0, 2.0),
            CableEdge(1, 3, 2.0, 2.0),
            CableEdge(3, 4, 2.0, 2.0),
        ])
        b = make_tree([
            CableEdge(0, 1, 1.0, 2.0),
            CableEdge(1, 2, 1.0, 2.0),
            CableEdge(1, 3, 1.0, 2.0),
            CableEdge(3, 4, 5.0, 2.0),
        ])
        self.assertAlmostEqual(a.total_length, b.total_length)
        fa = operator_features(a, k=4)
        fb = operator_features(b, k=4)
        self.assertGreater(
            abs(fa.g3_log_spacing_irregularity - fb.g3_log_spacing_irregularity),
            1e-3,
        )


if __name__ == "__main__":
    unittest.main()
