# Reimann/BBP canonical morphology recipe audit

This note records a strong **target-independent provenance clue** for four of the five unresolved Reimann rows. It does not silently upgrade them to `author_exact`.

## Why this matters

The Aizenbud Table-S1 Reimann rows are named only by m-type:

```text
L2 TPC   (already author-released)
L6 IPC
L4 TPC
L6 TPC
L6 UPC
L5 TPC
```

The author-released `L2 TPC` morphology is:

```text
mtC191200B_idA
```

Two independent public Blue Brain configuration repositories define the canonical SSCx e-model recipe for `cADpyr_L2TPC` using **that exact same morphology**. In those same recipe tables, four other target m-types have deterministic canonical representatives:

```text
cADpyr_L2TPC  -> mtC191200B_idA.asc     # released Aizenbud anchor
cADpyr_L4TPC  -> C310897A-P4.asc
cADpyr_L6IPC  -> mtC110301B_idB.asc
cADpyr_L6UPC  -> Fluo12_right.asc
cADpyr_L5TPC  -> C060114A5.asc
```

Sources checked independently:

- `BlueBrain/e-model-packager`, `sscx2020/extra_data/config/recipes/recipes.json`
- `BlueBrain/SSCxEModelExamples`, `validation/lib/config/recipes/recipes.json`

Both expose the same morphology choices.

The public SSCx morphology inventory also confirms that these names belong to the expected m-type pools; for example `C310897A-P4` occurs under `L4_TPC`, `Fluo12_right` under `L6_UPC`, and `mtC110301B_idB` under `L6_IPC`.

## What is earned

The released L2 TPC anchor provides a useful calibration:

> Aizenbud's released Reimann example uses the same morphology chosen by the canonical Blue Brain `cADpyr_<mtype>` recipe.

That makes the four mappings above substantially stronger than arbitrary exemplar selection.

## What is *not* earned

It still does not prove that Aizenbud used those four canonical representatives in the unpublished/missing model folders. Therefore, under the current strict provenance policy, they remain `unresolved` until one of these occurs:

1. the missing Aizenbud model folders/manifest become available;
2. the authors confirm the mapping;
3. another Aizenbud-side artifact identifies the morphology filenames.

If a later secondary/source-compatible analysis explicitly chooses canonical BBP e-model representatives, this note is the pre-existing provenance rationale. It must not be described as recovery of the exact author files.

## L6 TPC remains especially unresolved

The canonical recipe tables inspected here do not provide a simple `cADpyr_L6TPC` entry analogous to the four mappings above. The public morphology taxonomy separates at least `L6_TPC:A` and `L6_TPC:C`, and the Aizenbud Table-S1 label does not specify the subtype.

So `L6 TPC` remains the hardest Reimann row and must not be guessed from morphology appearance or target value.
