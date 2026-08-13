# Morphology/operator instrument smoke — result

## Status

**PASS as an instrument check. Not an FCI result.**

The V22 morphology pipeline was run against all four morphology files currently present in the authors' public `ido4848/FCI` repository. No FCI labels were used.

## External files processed

```text
Human L5    2057_H21_29_197_11_01_03_metcontour.asc
Human L2/3  2013_03_06_cell11_1125_H41_06.asc
Rat L2      mtC191200B_idA_diams_fixed.asc
Rat L5      cell1.asc
```

## Sampling/reconstruction hygiene

The first implementation treated each NeuroM section as an operator edge. Real ASC morphology can preserve one-child section boundaries, so a tracing/file-format boundary could become an operator node despite not being a soma, fork, or tip.

V22 now contracts every non-root one-child node before constructing the operator. Length and membrane area are summed along the contracted cable, preserving total cable and root-to-tip path distances.

Observed node counts after contraction:

```text
2057 human L5       134   (initial section graph: 222)
1125 human L2/3     209   (initial section graph: 241)
rat L2               71   (initial section graph: 76)
rat Hay L5           194   (initial section graph: 194)
```

This matters: without contraction, operator features could partly measure reconstruction bookkeeping rather than biological branching geometry.

## Cross-check against NeuroM 3.2.8

For every public external morphology, V22 ordinary measurements were compared directly against independent NeuroM feature functions.

```text
2057 human L5
  length        V22 27041.335705   NeuroM 27041.333984
  area          V22 68588.785870   NeuroM 68588.789062
  bifurcations  V22 59             NeuroM 59
  leaves        V22 72             NeuroM 72
  max path      V22 2121.815858    NeuroM 2121.815674

1125 human L2/3
  length        V22 20633.003506   NeuroM 20633.003906
  area          V22 86647.731610   NeuroM 86647.734375
  bifurcations  V22 94             NeuroM 94
  leaves        V22 110            NeuroM 110
  max path      V22 1230.587479    NeuroM 1230.587524

rat L2
  length        V22 4778.547419    NeuroM 4778.547363
  area          V22 11056.122399   NeuroM 11056.123047
  bifurcations  V22 32             NeuroM 32
  leaves        V22 38             NeuroM 38
  max path      V22 399.534199     NeuroM 399.534210

rat Hay L5
  length        V22 12574.397935   NeuroM 12574.397461
  area          V22 29872.286071   NeuroM 29872.287109
  bifurcations  V22 92             NeuroM 92
  leaves        V22 101            NeuroM 101
  max path      V22 1300.533502    NeuroM 1300.533569
```

The small floating-point differences are consistent with NeuroM returning some derived quantities at lower precision; a relative tolerance of `1e-6` passes all four cells. Discrete topology counts match exactly.

## Frozen operator features on the four debug cells

These values are descriptive only; four cells are not a prediction cohort.

```text
2057 human L5       G1 0.9421   G2 0.5521   G3 1.4357
1125 human L2/3     G1 0.9488   G2 0.5959   G3 1.3004
rat L2              G1 0.9380   G2 0.4231   G3 1.3958
rat Hay L5          G1 0.9040   G2 0.5184   G3 1.2173
```

Do not interpret the apparent species ordering in four selected cells. The 24-cell external gate remains sealed.

## Decision

The morphology/operator instrument is sufficiently consistent with NeuroM to proceed to **data recovery**.

Next task: recover the remaining Table-S1 morphologies with explicit provenance and compatibility status. Do not open or map the 24 FCI targets until the morphology side is complete and frozen.
