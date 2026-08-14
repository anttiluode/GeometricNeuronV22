# Secondary provenance-resolved 16-cell result

Status: **SECONDARY_OPERATOR_SIGNAL** under the frozen secondary rule.

This is **not** the strict 24-cell v0.1 result. The strict panel remains blocked by eight unresolved morphology mappings.

## Frozen setup

The secondary gate was frozen in `SECONDARY_RESOLVED16_GATE.md` before computation. It uses exactly orders:

```text
1, 5, 6, 7, 11,
13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24
```

Features are unchanged from v0.1:

```text
B2
  log(total dendritic area)
  log(longest root-to-tip cable path)

B2 + G
  G1 low-spectrum entropy
  G2 root modal-participation entropy
  G3 low-mode spacing irregularity
```

Fixed ridge `alpha=1`, standardization within each LOOCV training fold.

## Frozen result

```text
n = 16

B2
  CV R2       0.11191
  MAE         0.064400
  Spearman    0.38529

B2 + G
  CV R2       0.75479
  MAE         0.033082
  Spearman    0.85882

relative MAE improvement       48.63 %
mean paired error improvement  +0.0313175
bootstrap 95 % CI              [+0.014656, +0.048506]
exact two-sided sign-flip p     0.003173828125  (208 / 65536)
```

All five frozen criteria pass, so the secondary verdict is:

```text
SECONDARY_OPERATOR_SIGNAL
```

This is a real numerical surprise relative to the deliberately strong two-feature morphology baseline. It must **not** be promoted to the primary claim, because the recovered subset is provenance-selected and badly species-imbalanced: 5 rat and 11 human cells.

## Per-cell receipt

| order | cell | FCI | B2 pred | B2+G pred | paired improvement |
|---:|---|---:|---:|---:|---:|
| 1 | L2 TPC | 0.1877 | 0.267465 | 0.226924 | +0.040541 |
| 5 | 229_5 | 0.2156 | 0.290590 | 0.165287 | +0.024676 |
| 6 | 229_1 | 0.2260 | 0.264464 | 0.289472 | -0.025008 |
| 7 | cell1 | 0.2342 | 0.358900 | 0.288263 | +0.070637 |
| 11 | TTPC_1 232_1 | 0.2509 | 0.377079 | 0.271792 | +0.105287 |
| 13 | 548494556 | 0.3146 | 0.322153 | 0.338301 | -0.016148 |
| 14 | 528614014 | 0.3274 | 0.344699 | 0.334570 | +0.010128 |
| 15 | 1833 | 0.3618 | 0.353491 | 0.349944 | -0.003547 |
| 16 | 539661667 | 0.3626 | 0.314143 | 0.340936 | +0.026793 |
| 17 | 2057 | 0.3672 | 0.418401 | 0.399869 | +0.018532 |
| 18 | 569818704 | 0.3757 | 0.297111 | 0.413963 | +0.040326 |
| 20 | 1496 | 0.3957 | 0.333033 | 0.322613 | -0.010420 |
| 21 | 558211203 | 0.4004 | 0.269780 | 0.343564 | +0.073784 |
| 22 | 1204 | 0.4165 | 0.369099 | 0.414587 | +0.045488 |
| 23 | 1148 | 0.4190 | 0.352422 | 0.393776 | +0.041353 |
| 24 | 1125 | 0.4294 | 0.361776 | 0.420435 | +0.058658 |

## Immediate adversarial diagnostic: species confounding

Because the resolved subset is 5 rat / 11 human and the published FCI values strongly separate the species, the first post-result diagnostic was fixed to a boring question:

> Is the apparent operator advantage mostly a species classifier in disguise?

This diagnostic is **post hoc** and cannot alter the frozen secondary verdict.

LOOCV results:

```text
species only
  R2   0.79573
  MAE  0.029035

B2 + species
  R2   0.83910
  MAE  0.027104

B2 + G + species
  R2   0.82366
  MAE  0.026425
```

So a one-bit species indicator alone beats the frozen B2+G model in CV R2. After species is supplied explicitly, adding G slightly reduces MAE (~2.5 %) but **reduces R2**. That is a serious warning that much of the spectacular secondary gain may be species separation rather than within-species morphology/operator information.

The within-species exploratory split points the same way:

```text
Rat only, n=5
  B2     R2 +0.227, MAE 0.01510
  B2+G   R2 -0.552, MAE 0.02442
  relative MAE change: -61.7 %

Human only, n=11
  B2     R2 +0.098, MAE 0.03094
  B2+G   R2 +0.247, MAE 0.02758
  relative MAE improvement: +10.8 %
```

Those subgroup numbers are tiny-sample diagnostics, not confirmatory tests. They are useful mainly because they prevent the secondary pass from becoming mythology.

## Interpretation

The resolved-16 gate did something genuinely nontrivial: the frozen operator features dramatically improved prediction over area + path on this subset.

But the first boring adversary is already strong enough that the result cannot support a claim like “operator geometry predicts FCI beyond species.” The strict balanced 24-cell panel is now more important, not less.

Therefore:

```text
secondary gate:  PASSED
primary gate:    BLOCKED_INCOMPLETE_PROVENANCE
strong warning: SPECIES_CONFOUND_PLAUSIBLE
```

The next scientifically clean move remains recovery of the eight exact morphology mappings (or author confirmation that the published deposit is incomplete), followed by the frozen 24-cell analysis with no feature redesign.
