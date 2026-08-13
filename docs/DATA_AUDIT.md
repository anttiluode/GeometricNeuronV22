# Data audit — first external obstacle

The paper states that 24 reconstructed cortical pyramidal morphologies were modeled: 12 rat and 12 human, with three cells from each of layers 2/3, 4, 5, and 6.

The current public `ido4848/FCI` GitHub tree, however, exposes only four `.asc` morphology files:

```text
human L5 BBP     2057_H21_29_197_11_01_03_metcontour.asc
human L2/3 Eyal  2013_03_06_cell11_1125_H41_06.asc
rat L2 BBP       mtC191200B_idA_diams_fixed.asc
rat L5 Hay       cell1.asc
```

The repository is therefore sufficient to begin parser/operator instrumentation, but not by itself sufficient for the preregistered 24-cell external prediction gate.

The paper says the complete morphology description is in SI Appendix Table S1. The next data task is to recover the 24 morphology identifiers/source locations and verify whether the actual reconstruction files are publicly reachable from the cited source datasets or another release location.

Do not replace the 24-cell gate with a four-cell result. Four cells are an instrument/debug set only.
