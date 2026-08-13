# Data audit — first external obstacle

The paper states that 24 reconstructed cortical pyramidal morphologies were modeled: 12 rat and 12 human, with three cells from each of layers 2/3, 4, 5, and 6.

The current public `ido4848/FCI` GitHub tree exposes only four `.asc` morphology files:

```text
human L5 BBP     2057_H21_29_197_11_01_03_metcontour.asc
human L2/3 Eyal  2013_03_06_cell11_1125_H41_06.asc
rat L2 BBP       mtC191200B_idA_diams_fixed.asc
rat L5 Hay       cell1.asc
```

This is consistent with the earlier preprint's data-availability statement: it explicitly made those four morphologies/models public and said the remaining morphologies, models, FCI values, and correlation values were available upon request. The final paper says the morphology/model data were deposited on GitHub, but the current repository contents have not expanded to the full 24-cell set.

The full 24 morphology identities are nevertheless recoverable from Supplementary Table 1 and are now frozen in `FCI_MORPHOLOGY_MANIFEST.md` without FCI labels.

The next task is therefore data recovery, not cohort reduction: locate exact author-used files where possible, otherwise locate the cited source reconstructions and record whether the paper's stated diameter-floor edit can be reproduced exactly.

Do not replace the 24-cell gate with a four-cell result. Four cells are an instrument/debug set only.
