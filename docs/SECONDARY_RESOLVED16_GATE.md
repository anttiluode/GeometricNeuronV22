# Secondary provenance-resolved gate — frozen before computation

Status: **secondary analysis; not the strict 24-cell v0.1 gate.**

The strict 24-cell panel is blocked because eight published rows do not currently have a unique author/source morphology mapping. This secondary gate is frozen only to learn whether the existing external signal is already obviously dead or worth preserving while the provenance request remains open.

## Inclusion rule

Use **exactly the 16 rows marked `author_exact` or `source_compatible` by the provenance freeze.**

Frozen orders:

```text
1, 5, 6, 7, 11,
13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24
```

No row may be added, removed, substituted, or reclassified in response to its FCI value. The inclusion rule is based only on morphology provenance. It is visibly imbalanced (5 rat, 11 human) and therefore cannot replace the full 12+12 primary panel.

The **canonical target-free feature table** is `data/frozen_panel_v01.csv`, committed as `e72b84220e0f0e0741f59ce395dae4990aebb85d` with SHA256:

```text
1f8d05ca14e6c09351ab8dd2c186da36399708c9b3e1a6893f88f84d7c20a677
```

An earlier hand-transcribed JSON at commit `f7211fe...` contained incorrect longest-path values for the three recovered Markram rows. The mismatch was caught by rereading the successful GitHub Actions artifact **before the secondary regression was run**. Inclusion status did not change. The CSV above uses the artifact values and is the only feature table admitted to this secondary computation.

## Features and estimator

Use the unchanged v0.1 gate:

```text
B2
  log(total dendritic area)
  log(longest root-to-tip cable path)

B2 + G
  G1 low-spectrum entropy
  G2 root modal-participation entropy
  G3 low-mode spacing irregularity
```

Fixed ridge regression `alpha = 1.0`, standardization inside each training fold, leave-one-cell-out cross-validation.

No species indicator is added. No hyperparameter is tuned. No new morphology feature is admitted.

## Metrics and verdict rule

Report:

- CV R2;
- MAE;
- Spearman correlation;
- per-cell absolute-error improvement (`|e_B2| - |e_B2+G|`);
- mean paired improvement;
- percentile bootstrap 95% CI of mean paired improvement using 200,000 resamples and seed `20260813`;
- exact two-sided sign-flip p value over all `2^16` sign assignments.

For continuity, apply the same pass rule as the strict gate:

1. CV R2 improves;
2. MAE improves by at least 10%;
3. mean paired absolute-error improvement > 0;
4. bootstrap 95% CI is entirely above 0;
5. exact two-sided sign-flip p < 0.05.

Call the secondary result only:

```text
SECONDARY_OPERATOR_SIGNAL
```

or

```text
SECONDARY_NO_OPERATOR_ADVANTAGE
```

Even a pass does **not** pass the strict 24-cell gate.

## Blinding status

The original feature/baseline/decision-rule design was frozen before the cell-level outcomes were inspected. Outcome blinding was subsequently lost during provenance work because published Fig. 2 displays the FCI values beside each morphology. This secondary analysis is therefore **frozen but not blinded**.

The purpose of this document is to prevent post-outcome flexibility, not to recreate blindness that no longer exists.
