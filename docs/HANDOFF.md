# Handoff

## Current state

GeometricNeuronV22 is the external-test branch of the Geometric Neuron line.

The most important new result is now a **clean negative** for the frozen abstract operator features.

The original resolved-16 Fig. 2 target produced a spectacular B2+G gain, but that target was strongly species-confounded. We therefore recovered the per-cell FCI values from SI Fig. S5, where **all rat and human morphologies are equipped with identical rat-type synapses**, and reran the same frozen B2 versus B2+G comparison.

That cleaner gate says:

```text
COMMON_SYNAPSE_NO_OPERATOR_ADVANTAGE
```

Do not restart from the earlier positive and forget this null.

## Frozen v0.1 predictors

```text
B2
  log(total dendritic area)
  log(longest root-to-tip cable path)

B2 + G
  G1 low-spectrum entropy
  G2 root modal-participation entropy
  G3 low-mode spacing irregularity
```

Fixed ridge `alpha=1`, standardization inside each LOOCV training fold.

No G4/G5 may be added to rescue v0.1 on any already-exposed FCI target.

## Original resolved-16 Fig. 2 result

Frozen provenance-resolved subset:

```text
orders 1, 5, 6, 7, 11,
       13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24
```

GitHub Actions run `31772365592`:

```text
original Fig. 2 FCI

B2
  CV R2       0.11191
  MAE         0.064400

B2 + G
  CV R2       0.75479
  MAE         0.033082

relative MAE improvement       48.63 %
bootstrap 95 % CI              [+0.014656, +0.048506]
exact sign-flip p               0.00317
```

Frozen secondary verdict was `SECONDARY_OPERATOR_SIGNAL`.

But the immediate species adversary was devastating:

```text
species only       R2 0.7957
B2 + species       R2 0.8391
B2 + G + species   R2 0.8237
```

So the spectacular result could be a morphology/species fingerprint predicting a target that also contains species-specific synaptic/NMDA physics.

See `SECONDARY_RESOLVED16_RESULT.md`.

## Cleaner external target recovered from SI Fig. S5

Aizenbud et al. already performed the intervention needed to attack that confound: all 24 morphologies were simulated with the same **rat-type synaptic parameters**.

The final supplement was recovered reproducibly from the official 2026 PMC AWS Open Access dataset. GitHub Actions run `31777248643` succeeded using:

```text
PMC13367794.1/pnas.2533168123.sapp.pdf
```

Fig. S5 prints each four-decimal per-cell FCI value above its boxplot and repeats the morphology silhouette below it. The x-axis is sorted by common-synapse FCI, so identity was recovered by matching the repeated silhouette back to Fig. 2 within fixed species/layer groups.

Canonical target table:

```text
data/fci_targets_common_rat_synapse_figs5.csv
```

Target recovery receipt:

```text
docs/COMMON_SYNAPSE_FIGS5_RECEIPT.md
```

This target is outcome-exposed, not blind. The model and gate were nevertheless frozen before fitting it; see `COMMON_SYNAPSE_RESOLVED16_GATE.md`.

## Common-synapse resolved-16 result: v0.1 FAILS

GitHub Actions run `31778100080` completed successfully.

```text
common-rat-synapse FCI

B2
  CV R2       0.627747
  MAE         0.024057
  Spearman    0.720588

B2 + G
  CV R2       0.608452
  MAE         0.024927
  Spearman    0.720588

relative MAE improvement       -3.62 %
mean paired improvement        -0.0008706
bootstrap 95 % CI              [-0.007255, +0.005164]
exact two-sided sign-flip p     0.79355
```

Frozen verdict:

```text
COMMON_SYNAPSE_NO_OPERATOR_ADVANTAGE
```

The intervention also kills the old trivial species predictor:

```text
species only
  CV R2   0.0061
  MAE     0.03721
```

and G remains unhelpful after species is supplied:

```text
B2 + species       R2 0.6680, MAE 0.02192
B2 + G + species   R2 0.5518, MAE 0.02650
```

Within-species exploratory LOOCV points the same way:

```text
Rat n=5
  B2     R2 +0.227, MAE 0.01510
  B2+G   R2 -0.552, MAE 0.02442

Human n=11
  B2     R2 +0.571, MAE 0.02596
  B2+G   R2 +0.351, MAE 0.02978
```

See `COMMON_SYNAPSE_RESOLVED16_RESULT.md`.

## Current scientific interpretation

The cleanest reading is now:

> G1/G2/G3 were excellent predictors of the original rat-vs-human mixed-physics target, but they do not add held-out predictive value over ordinary area + path once the original experimenters match synaptic physics across species.

Therefore **V22 v0.1 does not earn the claim that these abstract graph-modal features capture the morphology-dependent computation measured by FCI**.

This does **not** undermine the Aizenbud morphology result. In fact, B2 alone becomes strong on the cleaner target (`R2 ~0.63`), which is compatible with the paper's emphasis on dendritic size/extent.

Do not reinterpret the old 48.6% MAE gain as mechanistic evidence.

## Strict 24-cell original-Fig2 gate

Still:

```text
BLOCKED_INCOMPLETE_PROVENANCE
```

Eight morphology identities/files remain unresolved:

```text
Markram 230_1, 230_2                         2
Reimann L6 IPC, L4 TPC, L6 TPC, L6 UPC,
        L5 TPC                               5
Allen   790872626                            1
------------------------------------------------
Total                                        8
```

The clean common-synapse result lowers the scientific priority of spending a long time forcing the original mixed-physics 24-cell gate to completion, but the provenance work remains useful for exact reproducibility.

## Provenance findings

### Public FCI repository is genuinely incomplete for the 24-cell panel

The reachable pre-restructure history of `ido4848/FCI` was audited. The December 2024 / January 2026 trees contain the same four example morphologies as the present repository:

```text
Rat L2 TPC
Rat Hay cell1
Human 2057
Human 1125
```

The missing Table-S1 morphologies were not simply removed in the January 2026 restructure, at least not from reachable public default-branch history.

See `FCI_REPOSITORY_HISTORY_AUDIT.md`.

### Strong target-independent Reimann canonical clue

Two independent public Blue Brain SSCx recipe tables agree on:

```text
L2 TPC  -> mtC191200B_idA.asc   # exactly matches Aizenbud's released anchor
L4 TPC  -> C310897A-P4.asc
L6 IPC  -> mtC110301B_idB.asc
L6 UPC  -> Fluo12_right.asc
L5 TPC  -> C060114A5.asc
```

These are strong source-compatible candidates, **not author-exact proof**. `L6 TPC` remains subtype-ambiguous.

See `REIMANN_CANONICAL_RECIPE_AUDIT.md`.

### Markram ambiguity remains real

Recovered source-compatible:

```text
229_1
229_5
TTPC_1 232_1
```

`230_1`/`230_2` remain ambiguous because public model collections reuse those suffixes across different L4 families. Do not guess.

### Allen

Recovered:

```text
548494556
528614014
539661667
569818704
558211203
```

`790872626` does not resolve as a current Allen Specimen or NeuronReconstruction ID.

## Canonical morphology feature table

Use only:

```text
data/frozen_panel_v01.csv
```

An older hand-transcribed JSON has incorrect longest-path values for three Markram rows and is not a canonical feature source.

## Author request

`docs/AUTHOR_DATA_REQUEST_DRAFT.md` is ready for human review. It asks for:

- the exact eight missing morphology mappings/files;
- confirmation/rejection of the four canonical Reimann mappings;
- the L6 TPC subtype;
- clarification of `230_1`, `230_2`, and Allen `790872626`;
- optionally, the numeric per-cell common-rat-synapse FCI table (now independently recoverable from Fig S5, but an author table would still be a useful cross-check).

Do not send automatically.

## Where to go next

### Do not rescue v0.1

No extra graph statistics on the now-exposed common-synapse target.

### Legitimate new hypothesis, if reopened

The post-gate idea that still has a principled basis is a **physical passive-cable operator** using dendritic radii/lengths and common `Cm/Ra/Rm`, rather than the abstract mass-normalized graph operator.

That is a different model class and must be treated as a new hypothesis, not `G4`.

Because the common-synapse outcomes are now exposed, the preferred validation is an independent external target/dataset or an analysis plan derived wholly from cable theory before any fitting. Do not tune the cable operator against Fig S5.

Other later ideas remain quarantined:

- location-to-soma response dictionary / effective control degrees of freedom;
- operator capacity versus input-address/convergence capacity;
- PivotPoint-style slow structural control against strong ordinary/TwinProp baselines.

## Guardrails

- KYY: geometry must beat strong simple baselines.
- FunctionalArbors: propagation is not credit assignment.
- PivotPoint: nominal options are not useful control degrees of freedom unless they create materially different reachable consequences.
- V22: the matched-synapse experiment killed the abstract G1/G2/G3 mechanistic interpretation. Preserve that kill.
