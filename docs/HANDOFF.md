# Handoff

## Current state

GeometricNeuronV22 is the clean external-test branch of the Geometric Neuron line.

The frozen first question is unchanged:

> Does a small operator/modal description of real dendritic trees improve held-out prediction of Aizenbud et al.'s Functional Complexity Index beyond a strong ordinary morphology baseline?

The 24 cell-level FCI mapping remains sealed.

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

## What is now built

- soma/fork/tip structural cable graph;
- contraction of tracing-only one-child boundaries;
- ordinary length/area/path/topology measurements;
- frozen mass-normalized cable graph operator;
- G1/G2/G3 extraction;
- synthetic tests and CI;
- external four-morphology smoke against the authors' current GitHub files;
- independent NeuroM cross-check of ordinary measurements.

The external smoke passed. The structural contraction was important: e.g. the human 2057 tracing graph dropped from 222 section nodes to 134 structural nodes without changing cable measurements.

## Data recovery state

The current `ido4848/FCI` repository contains only four morphology files, not all 24. The complete 24 identity/order manifest was recovered from the supplement and is stored in `FCI_MORPHOLOGY_MANIFEST.md` without FCI values.

### Mohan human cells

Five missing Mohan identities are independently available through the NeuroMorpho DeKock archive as standardized CNG SWCs: 1833, 1496, 1204, 1148, and 1125. The exact author-used 2057 file is already public.

Cell 1125 gives a calibration pair between the author copy and NeuroMorpho CNG. Primary B2+G quantities are extremely stable despite small topology-representation differences; see `MOHAN_CNG_CALIBRATION.md`. CNG recovery is therefore acceptable for the primary Mohan B2+G panel with provenance retained.

### Allen human cells

Current Allen RMA resolves five of the six Table-S1 identifiers as specimen IDs:

```text
548494556
528614014
539661667
569818704
558211203
```

`790872626` currently resolves as neither a Specimen ID nor a NeuronReconstruction ID. Do not guess a replacement. Four resolvable Allen files have already been downloaded in Actions; 558211203 remains straightforward to recover separately. Some Allen source SWCs contain disconnected neurite fragments, so provenance/compatibility needs explicit handling.

### Rat cells

The authors' public repo already provides rat L2 TPC and Hay `cell1`. The remaining Reimann/Markram morphologies still need exact-source recovery. A NeuroMorpho identifier probe for the Markram names is the next low-cost step.

## New mechanism distinctions to retain

1. **operator capacity**: geometry changes electrical propagation and compartmentalization;
2. **address capacity**: in the paper, synapse count scales with dendritic length, so larger trees also expose more input sites.

A later fixed-input-budget experiment can separate them, but not before the frozen FCI gate.

A physically derived passive cable operator using the paper's common Cm/Ra/Rm is also documented as a post-gate v0.2. Do not swap it into v0.1 after seeing target results.

## Immediate next work

1. finish morphology provenance/recovery;
2. freeze one 24-row label-free feature table with compatibility flags;
3. only then map the FCI targets;
4. run the frozen gate once;
5. preserve the result and stop/rescope according to the preregistration.

## Guardrails

- KYY: geometry must beat strong simple baselines.
- FunctionalArbors: propagation is not credit assignment.
- GeometricNeuronPlusField: do not import the failed generic-HH/AIS positive claims.
- No extra graph features may be added to rescue the v0.1 FCI gate.
