# Handoff

## Current state

GeometricNeuronV22 is a fresh convergence repository. The old repos remain the detailed experimental record; V22 is for external tests, compact instruments, and preserved receipts.

The first external target is Aizenbud et al. 2026 and the authors' released `ido4848/FCI` morphologies/models.

## Frozen first question

Does a small operator/modal description of real dendritic trees improve held-out prediction of the paper's Functional Complexity Index beyond a strong ordinary morphology baseline?

The confirmatory protocol is already frozen in `docs/FCI_EXTERNAL_GATE.md` before opening the 24 cell-level FCI labels.

Primary ordinary baseline:

```text
log(total dendritic area)
log(longest root-to-tip cable path)
```

Frozen operator panel:

```text
G1 low-spectrum entropy
G2 root modal-participation entropy
G3 low-mode spacing irregularity
```

Primary validation: leave-one-cell-out ridge regression, with a required >=10% MAE improvement plus paired uncertainty/sign-flip criteria.

## Immediate coding target

Build the morphology instrument first, without FCI labels:

1. inventory the released morphology files;
2. parse the morphology format robustly;
3. identify dendritic trees and soma/root;
4. collapse tracing samples between structural events;
5. compute ordinary morphology descriptors;
6. construct the cable-weighted operator;
7. compute G1-G3;
8. add parser/operator unit tests on tiny synthetic trees.

Only after those outputs are stable should the target table be loaded.

## Guardrails inherited from earlier repos

- `KYY`: geometry must beat strong simple baselines; solving a task is not evidence for a uniquely geometric mechanism.
- `FunctionalArbors`: propagation/transport is not the same as credit assignment.
- `GeometricNeuronPlusField`: the upstream morphology/operator picture survived better than the generic active event boundary; do not import failed event-boundary claims into V22.
- `PresentMoment`: receiver-relative accessibility is potentially relevant later, but it is not needed to make the first external morphology test harder or cleaner.

## Stop rule

If the frozen operator panel does not beat the ordinary baseline, write `NO_EXTERNAL_OPERATOR_ADVANTAGE`, preserve it, and do not add more spectral features as a rescue.
