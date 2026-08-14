# Frozen gate: common-rat-synapse FCI on the provenance-resolved 16-cell panel

Status: **FROZEN BEFORE FITTING THIS TARGET**.

Important limitation: the Figure-S5 outcomes have already been visually recovered, so this is **not outcome-blind**. The purpose of freezing this note before running the regression is to prevent target-driven redesign of the already-existing V22 model after seeing the common-synapse values.

## Why this gate exists

The original resolved-16 Fig. 2 gate passed strongly, but a one-bit species indicator was an excellent predictor of the original FCI target. The original target mixes morphology with species-specific synaptic/NMDA parameters.

SI Fig. S5 supplies the cleaner intervention: all 24 morphologies receive identical rat-type synapses.

The question is therefore:

> Does the **already-frozen** G1/G2/G3 operator description still improve held-out prediction over area + path when species-specific synaptic parameters have been experimentally removed?

## Immutable target receipt

```text
data/fci_targets_common_rat_synapse_figs5.csv
Git blob SHA-1: cbbe6cd2c72f67a1d8b66efececcc9c3e6dd4d30
```

Target recovery/mapping is documented separately in `COMMON_SYNAPSE_FIGS5_RECEIPT.md`.

## Immutable morphology panel

Use exactly the same provenance-resolved rows as the previous secondary gate:

```text
1, 5, 6, 7, 11,
13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24
```

No row may be added or removed based on the common-synapse result.

## Immutable predictors

```text
B2
  log(total dendritic area)
  log(longest root-to-tip cable path)

B2 + G
  G1 low-spectrum entropy
  G2 root modal-participation entropy
  G3 low-mode spacing irregularity
```

No G4. No alternate Laplacian/operator. No tuning based on this target.

## Immutable fitting

```text
ridge alpha = 1.0
standardize features inside each LOOCV training fold
intercept via training-fold target mean
leave-one-cell-out predictions
```

## Immutable success rule

Exactly the same five-part rule used for the resolved-16 original-Fig2 gate:

1. `CV R2(B2+G) > CV R2(B2)`;
2. relative MAE improvement is at least 10%;
3. mean paired absolute-error improvement is positive;
4. bootstrap 95% CI for paired improvement has lower bound above 0;
5. exact two-sided sign-flip `p < 0.05`.

If all five pass:

```text
COMMON_SYNAPSE_OPERATOR_SIGNAL
```

otherwise:

```text
COMMON_SYNAPSE_NO_OPERATOR_ADVANTAGE
```

The strict exact-24 primary morphology gate remains separately blocked by the eight unresolved morphology mappings.

## Adversarial interpretation rule

A pass would be materially more interesting than the original resolved-16 pass because the target no longer contains species-specific synaptic parameters. It still would **not** show that G1/G2/G3 are causal mechanisms.

A fail would strongly favor the mundane interpretation that the spectacular original resolved-16 gain depended on species-correlated aspects of the mixed morphology+synapse target.

If the gate passes, the first post-result diagnostic is fixed in advance to be boring:

```text
species only
B2 + species
B2 + G + species
rat-only exploratory LOOCV
human-only exploratory LOOCV
```

Those diagnostics cannot rescue or overturn the frozen gate verdict.
