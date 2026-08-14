# GeometricNeuronV22

An external-test repository for the Geometric Neuron line.

## Current verdict

The first abstract operator test has now met a genuinely useful external null.

On a provenance-resolved 16-cell subset of Aizenbud et al. 2026, the frozen graph/modal features `G1/G2/G3` initially looked spectacular on the original rat-vs-human FCI target:

```text
B2 area+path      CV R2 ~0.112
B2 + G            CV R2 ~0.755
```

But a one-bit species indicator alone scored ~0.796, exposing a major confound: the original target also contains species-specific synaptic/NMDA parameters.

The paper's SI Fig. S5 supplies the clean intervention. It repeats all 24 morphologies with **identical rat-type synapses**. We recovered the per-cell S5 values from the published figure, froze the same resolved-16 test, and reran it in GitHub Actions:

```text
common-rat-synapse FCI

B2 area+path      CV R2 0.628   MAE 0.02406
B2 + G            CV R2 0.608   MAE 0.02493

relative MAE improvement  -3.62 %
sign-flip p                0.794
```

Frozen verdict:

```text
COMMON_SYNAPSE_NO_OPERATOR_ADVANTAGE
```

So **V22 v0.1 does not earn the claim that its abstract graph-modal features explain morphology-dependent FCI beyond ordinary dendritic size/path geometry**. The old positive is preserved, but so is the experiment that largely explains it away.

See:

- `docs/COMMON_SYNAPSE_FIGS5_RECEIPT.md`
- `docs/COMMON_SYNAPSE_RESOLVED16_GATE.md`
- `docs/COMMON_SYNAPSE_RESOLVED16_RESULT.md`
- `docs/HANDOFF.md`

## Provenance work remains open

The exact original 24-cell morphology panel is still incomplete in the cited public deposit. Eight mappings remain unresolved, so the strict original-Fig2 24-cell gate stays:

```text
BLOCKED_INCOMPLETE_PROVENANCE
```

Convenient replacement cells are not allowed. `docs/FCI_REPOSITORY_HISTORY_AUDIT.md`, `docs/REIMANN_CANONICAL_RECIPE_AUDIT.md`, and `docs/AUTHOR_DATA_REQUEST_DRAFT.md` record the current recovery state.

## If the line continues

Do **not** add more graph statistics to rescue the exposed FCI target. A physical passive-cable operator would be a genuinely different hypothesis and should face a fresh external target/dataset rather than being tuned against Fig. S5.
