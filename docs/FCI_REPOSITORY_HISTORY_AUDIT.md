# FCI repository-history audit

Status: **reproducibility/provenance audit only**. This does not alter the frozen V22 features, baseline, target, inclusion rule, or primary verdict.

## Question

The final Aizenbud et al. 2026 PNAS paper says that morphology/neuron-model data were deposited in the cited `ido4848/FCI` GitHub repository. The current repository exposes only four morphology files. A possible benign explanation was that the other models had once been public and were removed during the January 2026 repository restructure.

I checked the reachable public default-branch history to test that explanation.

## Relevant upstream commits

```text
74434e34b4be3ec7f0adce70cfbf26a4f442f0e4
  2024-12-04
  "added rat and human l2/3 and l5 models"

05ace4823439220780670578cc2ef3d7b285e50e
  2026-01-11
  last pre-restructure commit inspected recursively

5bb4db205d2536acefe304cc413eac4a765528b6
  2026-01-21
  "restructred repository to make more usable"

55826436751c03a32dfd39e91a48894869e1db57
  2026-01-21
  current head when audited
```

## What the pre-restructure tree contains

The complete recursive tree at `05ace482...` contains exactly the same four model morphology blobs relevant here:

```text
Human L5
  neuron_models/human/bbp/Human_L5_PC_BBP_passive_dends_simple_soma/
    morphologies/2057_H21_29_197_11_01_03_metcontour.asc

Human L2/3
  neuron_models/human/eyal/Human_L23_PC_0603_11_937_Eyal_passive_dends_simple_soma/
    morphologies/2013_03_06_cell11_1125_H41_06.asc

Rat L2 TPC
  neuron_models/rat/bbp/Rat_L2_TPC_BBP_Mandge_diams_fixed_passive_dends_simple_soma/
    morphologies/mtC191200B_idA_diams_fixed.asc

Rat Hay L5
  neuron_models/rat/hay/Rat_L5b_PC_2_Hay_passive_dends_simple_soma/
    morphologies/cell1.asc
```

The earlier model-add commit `74434e34...` already contains these same four morphology files. I found no additional Table-S1 morphology/model directories in the reachable public history before the January 2026 restructure.

## Conclusion

The missing Table-S1 morphologies were **not merely deleted by the January 2026 repository restructure**, at least not from the reachable public default-branch history inspected here. The public repository appears to have contained the same four example morphologies from its initial model deposit through the pre-restructure state and into the current repository.

Therefore the strongest reproducibility statement currently earned is:

> The public `ido4848/FCI` history available through GitHub is insufficient for exact reconstruction of the published 24-cell morphology panel. The missing cells do not appear in the accessible pre-restructure default-branch history either.

This is not a criticism of the biological result. It is a provenance/data-availability finding relevant to reproducing the exact cell-level morphology analysis.

## What this changes for V22

Nothing about the frozen primary test changes.

```text
primary gate: BLOCKED_INCOMPLETE_PROVENANCE
```

It does make an author request cleaner than further repository archaeology. We can still recover source-compatible cells independently, but no missing row is to be called `author_exact` unless an authoritative Aizenbud-side mapping/file is obtained.

## Guardrail

Do not use this audit as permission to substitute canonical BBP exemplars into the primary 24-cell panel. The four canonical Reimann recipe mappings are valuable sensitivity-analysis candidates, not proof of which files Aizenbud used.