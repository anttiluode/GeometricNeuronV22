#!/usr/bin/env python3
from __future__ import annotations

import csv, json, math
from pathlib import Path
import numpy as np

ORDERS = (1,5,6,7,11,13,14,15,16,17,18,20,21,22,23,24)
ALPHA = 1.0
SEED = 20260813
NBOOT = 200_000


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return {int(r["order"]): r for r in csv.DictReader(f)}


def loocv(X, y):
    pred = np.empty(len(y))
    for i in range(len(y)):
        keep = np.arange(len(y)) != i
        mu = X[keep].mean(0)
        sd = X[keep].std(0)
        sd[sd == 0] = 1.0
        Z = (X[keep] - mu) / sd
        ym = y[keep].mean()
        beta = np.linalg.solve(Z.T @ Z + ALPHA*np.eye(X.shape[1]), Z.T @ (y[keep]-ym))
        pred[i] = ym + ((X[i]-mu)/sd) @ beta
    return pred


def ranks(x):
    idx = np.argsort(x, kind="mergesort")
    r = np.empty(len(x), float)
    r[idx] = np.arange(len(x), dtype=float)
    return r


def metrics(y, p):
    return {
        "r2": float(1 - np.sum((y-p)**2) / np.sum((y-y.mean())**2)),
        "mae": float(np.mean(np.abs(y-p))),
        "spearman": float(np.corrcoef(ranks(y), ranks(p))[0,1]),
    }


def exact_signflip(d):
    obs = abs(float(d.mean()))
    count = 0
    for mask in range(1 << len(d)):
        s = np.array([-1.0 if (mask >> j) & 1 else 1.0 for j in range(len(d))])
        count += abs(float(np.mean(d*s))) >= obs - 1e-15
    return count / float(1 << len(d))


def main():
    panel = load_csv("data/frozen_panel_v01.csv")
    target = {k: float(v["fci"]) for k,v in load_csv("data/fci_targets_fig2.csv").items()}
    rows = [panel[o] for o in ORDERS]
    if any(r["status"] == "unresolved" for r in rows):
        raise SystemExit("frozen secondary panel contains unresolved row")

    y = np.array([target[o] for o in ORDERS])
    B = np.array([[math.log(float(r["total_dendritic_area"])), math.log(float(r["longest_root_to_tip_path"]))] for r in rows])
    G = np.array([[float(r["g1_spectral_entropy"]), float(r["g2_root_participation_entropy"]), float(r["g3_log_spacing_irregularity"])] for r in rows])

    pb = loocv(B, y)
    pg = loocv(np.c_[B,G], y)
    mb, mg = metrics(y,pb), metrics(y,pg)
    d = np.abs(y-pb) - np.abs(y-pg)

    rng = np.random.default_rng(SEED)
    idx = rng.integers(0, len(d), size=(NBOOT, len(d)))
    ci = np.quantile(d[idx].mean(1), [0.025,0.975])
    rel = (mb["mae"] - mg["mae"]) / mb["mae"]
    p = exact_signflip(d)
    passed = mg["r2"] > mb["r2"] and rel >= .10 and d.mean() > 0 and ci[0] > 0 and p < .05

    out = {
        "verdict": "SECONDARY_OPERATOR_SIGNAL" if passed else "SECONDARY_NO_OPERATOR_ADVANTAGE",
        "strict_gate": "BLOCKED_INCOMPLETE_PROVENANCE",
        "orders": list(ORDERS),
        "b2": mb,
        "b2_plus_g": mg,
        "relative_mae_improvement": float(rel),
        "mean_paired_improvement": float(d.mean()),
        "bootstrap_95_ci": [float(ci[0]),float(ci[1])],
        "exact_two_sided_signflip_p": float(p),
        "predictions": [
            {"order":o,"fci":float(y[i]),"pred_b2":float(pb[i]),"pred_b2g":float(pg[i]),"paired_improvement":float(d[i])}
            for i,o in enumerate(ORDERS)
        ],
    }
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/secondary_resolved16_result.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))


if __name__ == "__main__":
    main()
