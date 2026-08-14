# Handoff

## Current state

GeometricNeuronV22 is the clean external-test branch of the Geometric Neuron line.

The frozen first question remains:

> Does a small operator/modal description of real dendritic trees improve held-out prediction of Aizenbud et al.'s Functional Complexity Index beyond a strong ordinary morphology baseline?

The analysis design was frozen before FCI outcome exposure. **Blinding is no longer intact**: during morphology provenance work the published Fig. 2 was opened and it prints the cell-level FCI values beside the morphology silhouettes. Do not call later analyses blinded. Features/baselines/inclusion rules may not be redesigned to improve the observed result.

## Frozen primary comparison

```text
B2
  log(total dendritic area)
  log(longest root-to-tip cable path)

B2 + G
  G1 low-spectrum entropy
  G2 root modal-participation entropy
  G3 low-mode spacing irregularity
```

Fixed ridge `alpha=1`, standardization inside each LOOCV training fold. Primary pass requires improved CV R2, >=10% MAE improvement, positive paired improvement with bootstrap CI > 0, and exact two-sided sign-flip p < .05.

## New result: secondary resolved-16 gate PASSED

Because the strict 24-cell panel is blocked by unresolved morphology provenance, a separate provenance-only 16-cell secondary panel was frozen before computation:

```text
orders 1, 5, 6, 7, 11,
       13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24
```

GitHub Actions run `31772365592` reran the frozen analysis from the committed feature/target files and completed successfully.

```text
B2
  CV R2       0.11191
  MAE         0.064400
  Spearman    0.38529

B2 + G
  CV R2       0.75479
  MAE         0.033082
  Spearman    0.85882

relative MAE improvement       48.63 %
mean paired improvement        +0.0313175
bootstrap 95 % CI              [+0.014656, +0.048506]
exact two-sided sign-flip p     0.003173828125
```

Frozen secondary verdict:

```text
SECONDARY_OPERATOR_SIGNAL
```

Permanent receipt: `artifacts/secondary_resolved16_result.json`.
Full interpretation: `docs/SECONDARY_RESOLVED16_RESULT.md`.

### Do not celebrate yet: species confounding is strong

The resolved subset is 5 rat / 11 human, and FCI strongly separates the species. A post-result boring adversary gives:

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

So a one-bit species indicator alone beats frozen B2+G in CV R2. Within species, G is actively bad in the tiny rat subset (n=5) and only modestly helpful in the human subset (n=11).

Therefore the correct interpretation is:

```text
secondary gate:  PASSED
primary gate:    BLOCKED_INCOMPLETE_PROVENANCE
warning:         SPECIES_CONFOUND_PLAUSIBLE
```

The secondary pass is interesting because the frozen operator features did dramatically improve over the predeclared morphology baseline. It is not evidence that the operator adds morphology information beyond species.

## Canonical feature table

Use only:

```text
data/frozen_panel_v01.csv
```

It contains all 24 identities in paper order, hashes and B2+G features for the 16 recovered rows, with empty feature cells for unresolved rows.

An earlier hand-transcribed JSON contained incorrect longest-path values for three Markram rows. The mismatch was caught by rereading the successful GitHub Actions recovery artifact before the secondary regression. Do not use the old JSON as a feature source.

## Data-availability finding

The final 2026 PNAS article states that morphology/neuron-model data were deposited in `ido4848/FCI`, but the cited repository currently exposes only four morphology files: rat L2 TPC, rat Hay `cell1`, human 2057, human 1125. The older preprint explicitly said only those four examples were public and the rest were available on request.

Therefore the current cited deposit is incomplete for exact 24-cell reproduction.

A ready-to-review author request is in `docs/AUTHOR_DATA_REQUEST_DRAFT.md`.

## Recovery state

### Author-exact anchors

```text
Rat   L2/3  L2 TPC
Rat   L5    cell1
Human L5    2057
Human L2/3  1125
```

### Mohan human source-compatible

```text
1833
1496
1204
1148
1125
```

`1125` provides an author-copy/source-copy calibration showing B2+G stability.

### Allen human

Recovered/processed:

```text
548494556
528614014
539661667
569818704
558211203
```

`790872626` currently resolves as neither Specimen nor NeuronReconstruction in Allen RMA. Do not guess a nearby ID.

### Markram rat

Recovered through public cortical model packages:

```text
229_1
  ModelDB L23_PC_cADpyr229_1
  dend-C170897A-P3_axon-C260897C-P4_-_Clone_4.asc

229_5
  ModelDB L23_PC_cADpyr229_5
  dend-C260897C-P3_axon-C220797A-P3_-_Clone_0.asc

TTPC_1 232_1
  Blue Brain L5_TTPC2_cADpyr232_1
  dend-C060114A7_axon-C060116A3_-_Clone_2.asc
```

Actions run `31727584626` downloaded them, applied the paper's 0.3 µm diameter floor, extracted B2+G and hashed the files.

`230_1` and `230_2` remain unresolved because the suffix is shared by multiple L4 PC/SP/SS model families.

### Reimann rat

Still unresolved as unique author-used exemplars:

```text
L6 IPC
L4 TPC
L6 TPC
L6 UPC
L5 TPC
```

Public Blue Brain/Open Brain templates expose plausible canonical defaults, but that is not enough to upgrade them without an authoritative source/author mapping. L6 TPC is additionally taxonomy-ambiguous.

## Strict 24-cell gate status

**BLOCKED_INCOMPLETE_PROVENANCE**

```text
Markram 230_1, 230_2                         2
Reimann L6 IPC, L4 TPC, L6 TPC, L6 UPC,
        L5 TPC                               5
Allen   790872626                            1
------------------------------------------------
Total                                        8
```

## Immediate next work

1. continue seeking authoritative mappings for the eight missing rows, but do not substitute convenient exemplars;
2. review/send the author data request if public provenance stays blocked;
3. if all eight are recovered, freeze the complete 24-row table and run the original v0.1 gate once;
4. when that result exists, explicitly test whether any operator signal survives species/source controls rather than interpreting the secondary pass at face value.

## Post-gate ideas that must not leak backward

- physical passive-cable operator using the paper's common Cm/Ra/Rm;
- location-to-soma response dictionary / effective control degrees of freedom;
- operator capacity versus input-address/convergence capacity;
- PivotPoint-style slow structural control against strong ordinary/TwinProp baselines.

## Guardrails

- KYY: geometry must beat strong simple baselines.
- FunctionalArbors: propagation is not credit assignment.
- PivotPoint: nominal options are not useful control degrees of freedom unless they create materially different reachable consequences.
- No extra graph features may be added to rescue v0.1 after outcome exposure.
