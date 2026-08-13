# Draft data request — missing morphology mappings for the published 24-cell FCI panel

**Do not send automatically.** This is a ready-to-send draft for a human to review.

Subject: Morphology files / exact source mappings for the 24-cell FCI panel (PNAS 2026)

Hello Dr. Aizenbud,

I am trying to reproduce a small morphology-only analysis on the 24 neuron models in Supplementary Table S1 of:

> Aizenbud et al. (2026), *Dendritic morphology and synaptic nonlinearities enhance functional complexity in human cortical neurons*, PNAS, e2533168123.

The paper's Data, Materials, and Software Availability statement says that the morphologies and neuron-model data were deposited in the cited `ido4848/FCI` GitHub repository. The current repository exposes four morphology files (rat L2 TPC, rat Hay L5 `cell1`, human `2057`, and human `1125`). I have been able to recover several additional Table-S1 cells from their cited public source archives, but I do not want to guess among multiple plausible source exemplars.

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

For `230_1` and `230_2`, public BBP-derived model collections contain more than one L4 family with the same suffix, so the suffix alone is not enough to select the intended morphology safely. For `790872626`, the current Allen RMA service does not resolve the published number as either a Specimen or NeuronReconstruction ID.

The goal is only to preserve exact provenance before running a preregistered/frozen morphology comparison; I am deliberately avoiding arbitrary replacement cells.

Thank you,
Antti Luode
