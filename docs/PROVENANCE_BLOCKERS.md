# Morphology provenance blockers — v0.1 gate

This note exists to keep the external FCI gate from quietly substituting convenient morphologies after the target values are opened.

The rule is simple:

> **No FCI/AUC target mapping until every row admitted to the primary panel has an explicit morphology provenance decision made without looking at its target.**

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

### Markram rat rows

Still unresolved as exact source morphologies:

- `229_5`
- `229_1`
- `230_1`
- `230_2`
- `TTPC_1 232_1`

A NeuroMorpho name probe produced only wrong-provenance matches. In particular, an exact-name `229_1` entry exists there but is a rat hippocampal dentate-granule reconstruction from a different archive, not the Markram 2015 cortical cell. Substring matches for the other names likewise point to unrelated species, brain regions or cell classes.

**Reject those matches. Filename resemblance is not provenance.**

### Reimann rat rows

Still unresolved as unique exemplars:

- `L6 IPC`
- `L4 TPC`
- `L6 TPC`
- `L6 UPC`
- `L5 TPC`

Aizenbud et al. cite Reimann et al., *Modeling and simulation of neocortical micro- and mesocircuitry. Part I: Anatomy* for these rows. That model is publicly deposited (including reconstructed morphologies), but Supplementary Table S1 identifies these cells only by m-type labels rather than a unique morphology filename/ID.

Primary data sources identified without opening FCI targets:

- Reimann anatomy dataset: `10.5281/zenodo.8155899`.
- Full BBP Somatosensory Cortex SONATA dataset: `10.7910/DVN/HISHXN`, which exposes morphology archives separately from the rest of the circuit.

The existence of many morphologies of the correct m-type does **not** identify which exemplar Aizenbud et al. used. Do not choose an arbitrary representative and call it the Table-S1 cell.

## Machine guardrail

`geometric_neuron_v22/panel.py` now freezes the 24 Table-S1 identities/order without any target values. A morphology receipt must classify each row as:

- `author_exact`
- `source_compatible`
- `unresolved`

The validator rejects target-like fields (`FCI`, `AUC`, `target`, `label`, etc.), identity substitutions, duplicate resolved paths, and gate-ready receipts containing unresolved rows. Source-compatible rows must explicitly record whether the 0.3 µm diameter floor was applied.

CI tests this contract.

## What closes the blockers

Preferred order:

1. recover the exact missing Markram/Reimann files or a unique mapping from an author/source manifest;
2. resolve Allen `790872626` through an authoritative mapping or exact archived source;
3. build one immutable 24-row label-free B2+G table with hashes and compatibility flags;
4. only then map the 24 FCI targets and run the frozen gate once.

If exact provenance proves unavailable, do **not** improvise after seeing targets. Any reduced-panel or source-compatible substitution policy must be written and frozen first, with the lost rows stated explicitly.

## Why this boring step matters

At n=24, one or two morphology substitutions can materially change a leave-one-cell-out comparison. Provenance is therefore part of the statistical instrument, not clerical cleanup.
