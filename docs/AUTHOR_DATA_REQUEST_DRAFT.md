# Draft data request — missing morphology mappings for the published 24-cell FCI panel

**Do not send automatically.** This is a ready-to-send draft for a human to review.

Subject: Morphology files / exact source mappings for the 24-cell FCI panel (PNAS 2026)

Hello Dr. Aizenbud,

I am trying to reproduce a small morphology-only analysis on the 24 neuron models in Supplementary Table S1 of:

> Aizenbud et al. (2026), *Dendritic morphology and synaptic nonlinearities enhance functional complexity in human cortical neurons*, PNAS, e2533168123.

The paper's Data, Materials, and Software Availability statement says that the morphologies and neuron-model data were deposited in the cited `ido4848/FCI` GitHub repository. The current repository exposes four morphology files (rat L2 TPC, rat Hay L5 `cell1`, human `2057`, and human `1125`). I also checked the reachable public repository history before the January 2026 restructure; the pre-restructure tree appears to contain the same four morphology files rather than the full Table-S1 panel. I have recovered several additional Table-S1 cells independently from their cited public source archives, but I do not want to guess among multiple plausible source exemplars.

Could you provide either the exact morphology files used for the remaining rows, or a mapping from the Table-S1 identifiers/m-types to their source morphology filenames/IDs?

The currently unresolved rows are:

```text
Rat / Markram 2015
  230_1
  230_2

Rat / Reimann 2024
  L6 IPC
  L4 TPC
  L6 TPC
  L6 UPC
  L5 TPC

Human / Allen 2015
  790872626
```

For four Reimann rows I found a strong candidate mapping in the public Blue Brain SSCx e-model recipes:

```text
L4 TPC -> C310897A-P4.asc
L6 IPC -> mtC110301B_idB.asc
L6 UPC -> Fluo12_right.asc
L5 TPC -> C060114A5.asc
```

Those same recipes map `L2 TPC -> mtC191200B_idA.asc`, which exactly matches the L2 TPC morphology released in your repository. I am therefore especially interested in whether the four candidate mappings above are in fact the files used in the FCI simulations. `L6 TPC` remains subtype-ambiguous in the public sources.

For `230_1` and `230_2`, public BBP-derived model collections contain more than one L4 family with the same suffix, so the suffix alone is not enough to select the intended morphology safely. For `790872626`, the current Allen RMA service does not resolve the published number as either a Specimen or NeuronReconstruction ID.

The goal is only to preserve exact provenance before running a frozen morphology comparison; I am deliberately avoiding arbitrary replacement cells.

If it is readily available, I would also be grateful for the **per-cell numeric FCI values underlying the condition where rat-type synapses were assigned to both rat and human morphologies** (the morphology-focused comparison reported in the paper). That would provide a cleaner morphology-only target than digitizing a figure.

Thank you,
Antti Luode
