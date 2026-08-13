from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .morphology import CableTree


@dataclass(frozen=True)
class OperatorFeatures:
    k_modes: int
    g1_spectral_entropy: float
    g2_root_participation_entropy: float
    g3_log_spacing_irregularity: float

    def as_dict(self) -> dict[str, float | int]:
        return {
            "k_modes": self.k_modes,
            "g1_spectral_entropy": self.g1_spectral_entropy,
            "g2_root_participation_entropy": self.g2_root_participation_entropy,
            "g3_log_spacing_irregularity": self.g3_log_spacing_irregularity,
        }


def mass_normalized_laplacian(tree: CableTree) -> tuple[np.ndarray, np.ndarray]:
    """Return L_M and node masses for the preregistered cable operator."""

    n = tree.n_nodes
    w = np.zeros((n, n), dtype=float)
    mass = np.zeros(n, dtype=float)

    for edge in tree.edges:
        conductance = 1.0 / edge.length
        w[edge.parent, edge.child] += conductance
        w[edge.child, edge.parent] += conductance
        half_area = 0.5 * edge.area
        mass[edge.parent] += half_area
        mass[edge.child] += half_area

    if np.any(~np.isfinite(mass)) or np.any(mass <= 0):
        raise ValueError("all structural nodes need finite positive cable mass")

    laplacian = np.diag(w.sum(axis=1)) - w
    inv_sqrt_mass = 1.0 / np.sqrt(mass)
    normalized = (
        inv_sqrt_mass[:, None] * laplacian * inv_sqrt_mass[None, :]
    )
    normalized = 0.5 * (normalized + normalized.T)
    return normalized, mass


def nonzero_eigenpairs(tree: CableTree) -> tuple[np.ndarray, np.ndarray]:
    matrix, _ = mass_normalized_laplacian(tree)
    values, vectors = np.linalg.eigh(matrix)
    scale = max(1.0, float(np.max(np.abs(values))))
    keep = values > 1e-10 * scale
    return values[keep], vectors[:, keep]


def _normalized_entropy(weights: np.ndarray) -> float:
    weights = np.asarray(weights, dtype=float)
    if len(weights) < 2:
        raise ValueError("entropy feature requires at least two modes")
    total = float(weights.sum())
    if not np.isfinite(total) or total <= 0:
        raise ValueError("entropy weights must have positive finite sum")
    p = weights / total
    p = p[p > 0]
    return float(-(p * np.log(p)).sum() / np.log(len(weights)))


def operator_features(tree: CableTree, k: int = 16) -> OperatorFeatures:
    """Compute the three frozen confirmatory V22 operator features."""

    if k < 2:
        raise ValueError("k must be at least 2")

    values, vectors = nonzero_eigenpairs(tree)
    count = min(k, len(values))
    if count < 2:
        raise ValueError("tree has fewer than two nonzero modes")

    values = values[:count]
    vectors = vectors[:, :count]

    g1 = _normalized_entropy(values)

    root_loading = np.square(vectors[tree.root, :])
    g2 = _normalized_entropy(root_loading)

    spacing = np.diff(np.log(values))
    mean_spacing = float(np.mean(spacing))
    g3 = float(np.std(spacing) / (abs(mean_spacing) + np.finfo(float).eps))

    return OperatorFeatures(
        k_modes=count,
        g1_spectral_entropy=g1,
        g2_root_participation_entropy=g2,
        g3_log_spacing_irregularity=g3,
    )


def full_feature_row(tree: CableTree, k: int = 16) -> dict[str, float | int]:
    row = dict(tree.basic_features())
    row.update(operator_features(tree, k=k).as_dict())
    return row
