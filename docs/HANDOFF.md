# Handoff

## Current state

GeometricNeuronV22 is the clean external-test branch of the Geometric Neuron line.

The frozen first question is unchanged:

> Does a small operator/modal description of real dendritic trees improve held-out prediction of Aizenbud et al.'s Functional Complexity Index beyond a strong ordinary morphology baseline?

The analysis design was frozen before FCI outcome exposure. **Blinding is no longer intact**, however: during morphology provenance work the published Fig. 2 was opened and it prints the cell-level FCI values beside the morphology silhouettes. Do not call the future run blinded. It remains a frozen/preregistered analysis, and no feature/baseline/inclusion decision may be changed to improve the result.

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

Validation is leave-one-cell-out fixed ridge regression. The operator arm must improve CV R2, improve MAE by at least 10%, and pass paired CI/sign-flip criteria. Otherwise the result is `NO_EXTERNAL_OPERATOR_ADVANTAGE`.

## What is built

- soma/fork/tip structural cable graph;
- contraction of tracing-only one-child boundaries;
- ordinary length/area/path/topology measurements;
- frozen mass-normalized cable graph operator;
- G1/G2/G3 extraction;
- synthetic tests and CI;
- external author-file smoke;
- independent NeuroM cross-check of ordinary measurements;
- exact 24-row target-free identity manifest and receipt validator;
- target-like-field and substitution rejection in CI;
- public-source recovery workflows for Mohan, Allen, and the mapped Markram cells.

## Data-availability finding

The final 2026 PNAS article states that the morphology/neuron-model data were deposited in `ido4848/FCI`. The current cited repository exposes only four morphology files: rat L2 TPC, rat Hay `cell1`, human 2057, human 1125. It has no releases/tags supplying the rest.

The older preprint explicitly described those same four examples as public and said the other morphologies/models were available on request. Therefore the **current cited public deposit is incomplete for an exact 24-cell reproduction**.

This is now the main wall. Do not silently fill it with arbitrary source-pool exemplars.

## Recovery state

### Author-exact anchors

```text
Rat   L2/3  L2 TPC
Rat   L5    cell1
Human L5    2057
Human L2/3  1125
```

### Mohan human source-compatible

Recovered through the DeKock NeuroMorpho archive:

```text
1833
1496
1204
1148
1125
```

The author-copy/source-copy 1125 calibration shows B2+G stability. Prefer author 1125 where available; use the source copy only with provenance retained.

### Allen human

Current RMA resolves and the recovery workflow processed:

```text
548494556
528614014
539661667
569818704
558211203
```

`790872626` resolves as neither Specimen nor NeuronReconstruction in the same service. Do not guess a nearby ID. Some recovered SWCs have disconnected-neurite warnings; record rather than silently repair them.

### Markram rat

Three source identities have now been recovered through public Markram/BBP-derived model packages:

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

Actions run `31727584626` successfully downloaded them, applied the paper's 0.3 µm diameter floor using MorphIO, extracted B2+G, and hashed the floored files. See `PROVENANCE_BLOCKERS.md` for the numerical receipt.

`230_1` and `230_2` remain unresolved. The suffix is not unique across public L4 PC/SP/SS model families, so a convenient `L4_PC` match is not sufficient provenance.

### Reimann rat

Still unresolved as unique author-used exemplars:

```text
L6 IPC
L4 TPC
L6 TPC
L6 UPC
L5 TPC
```

Public Blue Brain/Open Brain templates expose plausible canonical defaults, and the released Aizenbud L2 TPC anchor is itself consistent with that canonical-default pattern. This is useful evidence but not enough to upgrade the five rows to `source_compatible` without a source/author mapping. L6 TPC is additionally taxonomy-ambiguous.

## Strict 24-cell gate status

**BLOCKED_INCOMPLETE_PROVENANCE**

Eight rows remain unresolved:

```text
Markram 230_1, 230_2                         2
Reimann L6 IPC, L4 TPC, L6 TPC, L6 UPC,
        L5 TPC                               5
Allen   790872626                            1
------------------------------------------------
Total                                        8
```

Do not run the strict 24-cell target fit until this reaches zero.

## Immediate next work

1. seek an authoritative author/source manifest for the eight missing rows;
2. if recovered, freeze one immutable 24-row B2+G table with hashes/compatibility flags and run the frozen analysis once;
3. if exact provenance is not obtainable, freeze a **separate** reduced/source-compatible secondary panel before fitting outcomes; never relabel that as the original 24-cell gate;
4. preserve the result/null and stop/rescope according to the preregistration.

An author data request is now scientifically cleaner than choosing arbitrary Reimann exemplars, because the final paper itself says those data were deposited.

## Post-gate ideas that must not leak backward

- physical passive-cable operator using the paper's common Cm/Ra/Rm;
- location-to-soma response dictionary / effective control degrees of freedom;
- operator capacity versus afferent address/convergence capacity;
- PivotPoint-style slow structural control against strong ordinary gradient/TwinProp baselines.

Do not alter v0.1 with these after outcome exposure.

## Guardrails

- KYY: geometry must beat strong simple baselines.
- FunctionalArbors: propagation is not credit assignment.
- PivotPoint: nominal options are not useful control degrees of freedom unless they create materially different reachable consequences.
- GeometricNeuronPlusField: do not import failed generic-HH/AIS positive claims.
- No extra graph features may be added to rescue the v0.1 FCI gate.
