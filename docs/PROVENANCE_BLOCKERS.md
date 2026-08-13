# Morphology provenance blockers — v0.1 gate

This note exists to keep the external FCI gate from quietly substituting convenient morphologies after the analysis was frozen.

The rule is simple:

> **No fitting or feature redesign against FCI/AUC targets until every row admitted to a gate has an explicit morphology provenance decision.**

## Important availability finding

The final 2026 PNAS paper states that **morphologies and neuron-model data have been deposited in the authors' GitHub repository** (`ido4848/FCI`). The cited repository currently exposes only four morphology files:

- Rat L2/3 `L2 TPC`
- Rat L5 `cell1`
- Human L5 `2057`
- Human L2/3 `1125`

The older 2024 preprint was explicit that only those four examples were public and that the other neuron morphologies/models were available on request. The final publication therefore promises a fuller public deposit than is presently visible in the cited repository.

The current cited deposit has no GitHub releases or tags that provide a second obvious archive of the missing cells. Therefore **the current public deposit is incomplete for reproducing the 24-cell panel exactly**.

Do not repair this by choosing convenient exemplars after the fact. Exhaust authoritative mappings first; if the author-used files remain unavailable, an author data request or a separately frozen reduced/source-compatible analysis is cleaner than pretending the primary 24-cell panel was recovered.

## Important blinding correction

The B2+G features, baseline, panel order and decision rule were frozen before inspecting the 24 FCI outcomes. During the subsequent provenance hunt, however, Fig. 2 of the published paper was opened to inspect morphology silhouettes; that figure prints the FCI values beside the morphologies.

Therefore the future v0.1 analysis is **frozen/preregistered but no longer outcome-blind**. Do not describe it as a blinded test. The guardrail is now mechanical: no feature, baseline, inclusion, or provenance decision may be tuned to improve the target result.

## Current 24-row status

### Author-exact files already in the released FCI repository

- Rat L2/3 `L2 TPC` — released BBP/Reimann morphology used by the authors.
- Rat L5 `cell1` — released Hay morphology used by the authors.
- Human L5 `2057` — released author-used ASC.
- Human L2/3 `1125` — released author-used ASC.

These are the calibration anchor files for the extractor.

### Mohan human source-compatible recovery

The DeKock NeuroMorpho archive contains standardized CNG versions for:

- `1833`
- `1496`
- `1204`
- `1148`
- `1125`

The `1125` source copy was compared against the author-used ASC before target mapping. The frozen B2+G quantities were extremely stable despite small tracing/topology representation differences; see `MOHAN_CNG_CALIBRATION.md`. Therefore the source-compatible CNG representation is admissible for missing Mohan rows with provenance retained. The exact author `1125` remains preferable where available.

### Allen human rows

Current Allen RMA resolves five of the six Table-S1 identifiers as specimen IDs:

- `548494556`
- `528614014`
- `539661667`
- `569818704`
- `558211203`

A GitHub Actions recovery run downloaded and processed all five before deliberately hitting the unresolved identifier. The paper states that all morphologies were edited so no diameter was below 0.3 µm; the recovery script applies that same floor before feature extraction.

`790872626` currently resolves as neither a `Specimen` nor a `NeuronReconstruction` in the same Allen RMA service. **Do not guess a nearby Allen cell.** It remains unresolved.

Some recovered Allen SWCs emit disconnected-neurite warnings in NeuroM/MorphIO. That is a compatibility/provenance issue to record, not a reason to silently repair the source geometry.

### Markram rat rows — three source mappings recovered

The original broad NeuroMorpho filename search was misleading: an exact-name `229_1` hit there is a hippocampal dentate-granule cell from the wrong archive. That match remains rejected.

A better source route recovered three Markram-2015 model identities through public cortical model packages:

- `229_1` -> ModelDB `L23_PC_cADpyr229_1` -> `dend-C170897A-P3_axon-C260897C-P4_-_Clone_4.asc`
- `229_5` -> ModelDB `L23_PC_cADpyr229_5` -> `dend-C260897C-P3_axon-C220797A-P3_-_Clone_0.asc`
- `TTPC_1 232_1` -> Blue Brain `L5_TTPC2_cADpyr232_1` -> `dend-C060114A7_axon-C060116A3_-_Clone_2.asc`

These are **source-compatible**, not `author_exact`, until an Aizenbud-side manifest confirms the exact copies used in the FCI run.

GitHub Actions run `31727584626` downloaded all three, applied the paper's 0.3 µm diameter floor with MorphIO, extracted the frozen V22 features, hashed the resulting files, and completed successfully. The structural/operator receipts were:

```text
229_1
  nodes 90
  total dendritic length 6090.413 µm
  total dendritic area   12398.280 µm²
  G1 0.960147   G2 0.667071   G3 1.797844
  floored SHA256 9df31c3f893cbc2c14b1b1e3aeaef680355f7445028802259e4e1085a3c1d239

229_5
  nodes 108
  total dendritic length 7030.022 µm
  total dendritic area   16610.200 µm²
  G1 0.953504   G2 0.564251   G3 2.040392
  floored SHA256 f0df3254ca4642bab1184389888904288ce75e55d04bbbab8facbb4f218274d1

TTPC_1 232_1
  nodes 212
  total dendritic length 18153.471 µm
  total dendritic area   48326.326 µm²
  G1 0.913134   G2 0.427538   G3 1.345259
  floored SHA256 8e80e32fdf3fc35c898811d0fea807b20570e6c91e5644a182e8190ed517c24f
```

The remaining Markram rows are:

- `230_1`
- `230_2`

They are **not safely resolved by the bare suffix**. Public BBP-derived inventories contain multiple L4 model families carrying `cADpyr230_1` / `cADpyr230_2` suffixes (including PC, SP and SS families) with different morphologies. A public `L4_PC_cADpyr230_1` morphology exists, but choosing it merely because the Table-S1 row says `230_1` would be an inference, not provenance. Keep both rows unresolved until a source/author mapping identifies the intended family.

### Reimann rat rows

Still unresolved as unique author-used exemplars:

- `L6 IPC`
- `L4 TPC`
- `L6 TPC`
- `L6 UPC`
- `L5 TPC`

Aizenbud et al. cite Reimann et al., *Modeling and simulation of neocortical micro- and mesocircuitry. Part I: Anatomy* for these rows. That model is publicly deposited, but Supplementary Table S1 identifies these cells only by m-type labels rather than unique morphology filenames/IDs.

There is useful target-independent evidence for canonical e-model defaults in public Blue Brain/Open Brain tooling. For example, the same L2 TPC family used by the released Aizenbud anchor defaults to `mtC191200B_idA`, while public templates expose defaults such as `mtC110301B_idB` for L6 IPC, `C310897A-P4` for L4 TPC, `Fluo12_right` for L6 UPC, and `C060114A5` for L5 TPC. These are **candidate source defaults, not proof of Aizenbud's selected exemplars**. L6 TPC is additionally taxonomy-ambiguous.

Primary source pools already identified:

- Reimann anatomy dataset: `10.5281/zenodo.8155899`.
- Full BBP Somatosensory Cortex SONATA dataset: `10.7910/DVN/HISHXN`.

Do not choose an arbitrary m-type/default representative and call it the Table-S1 cell.

## Machine guardrail

`geometric_neuron_v22/panel.py` freezes the 24 Table-S1 identities/order without target values. A morphology receipt must classify each row as:

- `author_exact`
- `source_compatible`
- `unresolved`

The validator rejects target-like fields (`FCI`, `AUC`, `target`, `label`, etc.), identity substitutions, duplicate resolved paths, and gate-ready receipts containing unresolved rows. Source-compatible rows must explicitly record whether the 0.3 µm diameter floor was applied.

CI tests this contract.

## Strict primary gate status

The exact/source-compatible 24-cell panel is **not gate-ready**.

Hard unresolved rows at this point:

```text
Markram: 230_1, 230_2                         2
Reimann: L6 IPC, L4 TPC, L6 TPC, L6 UPC,
         L5 TPC                               5
Allen:   790872626                            1
------------------------------------------------
Total unresolved                              8
```

This is now a data/provenance blocker, not an operator-code blocker.

## What closes the blockers

Preferred order:

1. obtain the missing author-used files or an authoritative manifest from the cited FCI deposit/authors;
2. resolve Allen `790872626` through an authoritative mapping or exact archived source;
3. freeze one immutable 24-row B2+G table with hashes and compatibility flags;
4. run the already-frozen target analysis once, without changing features/baselines after outcome exposure.

If exact provenance proves unavailable, do **not** improvise. A reduced-panel/source-compatible secondary analysis must be specified and frozen separately, and it must be reported as such rather than quietly replacing the primary 24-cell gate.

## Why this boring step matters

At n=24, one or two morphology substitutions can materially change a leave-one-cell-out comparison. Provenance is therefore part of the statistical instrument, not clerical cleanup.
