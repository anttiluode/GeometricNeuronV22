# Figure S5 receipt: per-cell FCI under common rat-type synapses

Status: **target recovered from the published Supplementary Figure S5**.

This is a post-v0.1 follow-up receipt. It does not modify the frozen original-Fig2 gate, which remains blocked by incomplete morphology provenance.

## Why this target matters

The resolved-16 original-Fig2 gate produced a large B2+G improvement, but a one-bit species indicator predicted the original FCI target extremely well. That is a serious confound because the original 24-cell condition combines:

```text
morphology
+
species-specific synaptic parameters / NMDA nonlinearity
```

Aizenbud et al. supplied the right intervention in SI Fig. S5: all 24 morphologies are simulated with **identical rat-type synapses**. The SI caption states that human neurons still have higher FCI in this condition (two-sided t-test `p = 0.022`).

This target therefore removes the most obvious path by which a morphology feature could predict species-specific synaptic physics without measuring it.

## How the supplement was recovered

The brittle historical article `bin/` URLs failed in August 2026. The final supplementary PDF was recovered reproducibly from the official PMC Open Access AWS dataset using the new per-version layout:

```text
PMC13367794.1/pnas.2533168123.sapp.pdf
```

The repository contains:

- `scripts/fetch_aizenbud_supplement.py`
- `.github/workflows/fetch-aizenbud-supplement.yml`

GitHub Actions run `31777248643` completed successfully and uploaded the PDF/text/receipt artifact.

## The useful surprise

Figure S5 does not merely show unlabeled boxes. It prints each cell's FCI value to four decimals immediately above the corresponding boxplot and repeats the morphology silhouette below it.

The S5 x-axis is sorted by the common-synapse FCI rather than by the Table-S1 identity order. Therefore target recovery has two pieces:

1. read the printed four-decimal FCI value at each S5 position;
2. map the repeated morphology silhouette back to the same silhouette in Fig. 2, constrained by species and cortical layer.

For rat cells the mapping is additionally exact by construction: the original rat models already used rat-type synapses, and the twelve orange S5 values exactly reproduce the twelve original Fig. 2 rat FCI values.

For human cells the repeated silhouette is used to recover identity within each three-cell cortical-layer group.

## Human silhouette mapping receipt

```text
Table-S1 order  identifier   layer   S5 position   common-rat-synapse FCI
13              548494556    L6      6             0.2076
14              528614014    L6      3             0.2024
15              1833         L5      16            0.2476
16              539661667    L4      13            0.2389
17              2057         L5      21            0.3024
18              569818704    L4      8             0.2199
19              790872626    L5      9             0.2201
20              1496         L4      20            0.2728
21              558211203    L6      17            0.2502
22              1204         L2/3    24            0.3401
23              1148         L2/3    22            0.3128
24              1125         L2/3    23            0.3223
```

The strongest visual anchors are especially distinctive:

- Human L6 order 14 is the very tall sparse morphology -> S5 position 3.
- Human L5 order 17 (`2057`) is the giant tall/broad morphology -> S5 position 21.
- Human L4 order 20 (`1496`) has the distinctive three long near-parallel apical stems -> S5 position 20.
- Human L2/3 order 22 (`1204`) has the paired long apical stems -> S5 position 24.

The remaining matches are then confirmed within their fixed three-cell species/layer groups by the repeated branching silhouette. This is a figure-identity mapping, not a choice based on V22 features or regression performance.

Canonical recovered targets are stored in:

```text
data/fci_targets_common_rat_synapse_figs5.csv
```

## Important statistical status

The common-synapse outcomes are now **exposed**. This cannot be called a blinded new experiment.

However, the model family was already fixed before seeing this target:

```text
B2
  log(area)
  log(longest root-to-tip path)

B2 + G
  same frozen G1/G2/G3

fixed ridge alpha=1
training-fold standardization
LOOCV
```

No G4, no feature search, no changed regularization, and no target-driven inclusion decisions are allowed.

The clean question is now narrower:

> Does the already-frozen operator description retain held-out predictive value over area + path when species-specific synaptic parameters have been experimentally removed by the original authors?

## Guardrail

A positive common-synapse result would strengthen the morphology/operator interpretation, but it would still not prove that G1/G2/G3 are causal mechanisms. A null would strongly support the simpler reading that the spectacular resolved-16 original-Fig2 result was largely a species-correlated target effect.
