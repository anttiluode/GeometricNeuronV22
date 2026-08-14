#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

ORDERS = (1, 5, 6, 7, 11, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24)
ALPHA = 1.0
SEED = 20260814
NBOOT = 200_000


def load_csv(path: str):
    with open(path, newline="", encoding="utf-8") as f:
        return {int(r["order"]): r for r in csv.DictReader(f)}


def loocv(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    pred = np.empty(len(y))
    for i in range(len(y)):
        keep = np.arange(len(y)) != i
        mu = X[keep].mean(0)
        sd = X[keep].std(0)
        sd[sd == 0] = 1.0
        Z = (X[keep] - mu) / sd
        ym = y[keep].mean()
        beta = np.linalg.solve(
            Z.T @ Z + ALPHA * np.eye(X.shape[1]),
            Z.T @ (y[keep] - ym),
        )
        pred[i] = ym + ((X[i] - mu) / sd) @ beta
    return pred


def ranks(x: np.ndarray) -> np.ndarray:
    idx = np.argsort(x, kind="mergesort")
    r = np.empty(len(x), float)
    r[idx] = np.arange(len(x), dtype=float)
    return r


def metrics(y: np.ndarray, p: np.ndarray) -> dict:
    denom = np.sum((y - y.mean()) ** 2)
    return {
        "r2": float(1 - np.sum((y - p) ** 2) / denom) if denom > 0 else float("nan"),
        "mae": float(np.mean(np.abs(y - p))),
        "spearman": float(np.corrcoef(ranks(y), ranks(p))[0, 1]) if len(y) > 2 else float("nan"),
    }


def exact_signflip(d: np.ndarray) -> float:
    obs = abs(float(d.mean()))
    count = 0
    for mask in range(1 << len(d)):
        s = np.array([-1.0 if (mask >> j) & 1 else 1.0 for j in range(len(d))])
        count += abs(float(np.mean(d * s))) >= obs - 1e-15
    return count / float(1 << len(d))


def model_result(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, dict]:
    p = loocv(X, y)
    return p, metrics(y, p)


def main() -> None:
    panel = load_csv("data/frozen_panel_v01.csv")
    targets = load_csv("data/fci_targets_common_rat_synapse_figs5.csv")
    rows = [panel[o] for o in ORDERS]
    if any(r["status"] == "unresolved" for r in rows):
        raise SystemExit("frozen common-synapse panel contains unresolved morphology row")

    y = np.array([float(targets[o]["fci_common_rat_synapse"]) for o in ORDERS])
    B = np.array([
        [
            math.log(float(r["total_dendritic_area"])),
            math.log(float(r["longest_root_to_tip_path"])),
        ]
        for r in rows
    ])
    G = np.array([
        [
            float(r["g1_spectral_entropy"]),
            float(r["g2_root_participation_entropy"]),
            float(r["g3_log_spacing_irregularity"]),
        ]
        for r in rows
    ])
    species = np.array([[1.0 if targets[o]["species"] == "Human" else 0.0] for o in ORDERS])

    pb, mb = model_result(B, y)
    pg, mg = model_result(np.c_[B, G], y)
    d = np.abs(y - pb) - np.abs(y - pg)

    rng = np.random.default_rng(SEED)
    idx = rng.integers(0, len(d), size=(NBOOT, len(d)))
    ci = np.quantile(d[idx].mean(1), [0.025, 0.975])
    rel = (mb["mae"] - mg["mae"]) / mb["mae"]
    p = exact_signflip(d)

    passed = (
        mg["r2"] > mb["r2"]
        and rel >= 0.10
        and d.mean() > 0
        and ci[0] > 0
        and p < 0.05
    )

    # Fixed post-result adversaries. These do not enter the gate verdict.
    ps, ms = model_result(species, y)
    pbs, mbs = model_result(np.c_[B, species], y)
    pgs, mgs = model_result(np.c_[B, G, species], y)

    subgroup = {}
    for name, value in (("rat", 0.0), ("human", 1.0)):
        sel = species[:, 0] == value
        y_sub = y[sel]
        b_sub = B[sel]
        g_sub = G[sel]
        pb_sub, mb_sub = model_result(b_sub, y_sub)
        pg_sub, mg_sub = model_result(np.c_[b_sub, g_sub], y_sub)
        subgroup[name] = {
            "n": int(sel.sum()),
            "orders": [int(o) for o, keep in zip(ORDERS, sel) if keep],
            "b2": mb_sub,
            "b2_plus_g": mg_sub,
            "relative_mae_improvement": float((mb_sub["mae"] - mg_sub["mae"]) / mb_sub["mae"]),
        }

    out = {
        "verdict": "COMMON_SYNAPSE_OPERATOR_SIGNAL" if passed else "COMMON_SYNAPSE_NO_OPERATOR_ADVANTAGE",
        "strict_24_gate": "BLOCKED_INCOMPLETE_PROVENANCE",
        "target": "SI Fig S5; all morphologies with rat-type synapses",
        "orders": list(ORDERS),
        "b2": mb,
        "b2_plus_g": mg,
        "relative_mae_improvement": float(rel),
        "mean_paired_improvement": float(d.mean()),
        "bootstrap_95_ci": [float(ci[0]), float(ci[1])],
        "exact_two_sided_signflip_p": float(p),
        "predictions": [
            {
                "order": int(o),
                "identifier": targets[o]["identifier"],
                "species": targets[o]["species"],
                "fci_common_rat_synapse": float(y[i]),
                "pred_b2": float(pb[i]),
                "pred_b2g": float(pg[i]),
                "paired_improvement": float(d[i]),
            }
            for i, o in enumerate(ORDERS)
        ],
        "fixed_post_result_diagnostics": {
            "species_only": ms,
            "b2_plus_species": mbs,
            "b2_plus_g_plus_species": mgs,
            "within_species": subgroup,
        },
    }

    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/common_synapse_resolved16_result.json").write_text(
        json.dumps(out, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
