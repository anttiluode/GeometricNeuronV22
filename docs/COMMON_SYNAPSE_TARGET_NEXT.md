# Cleaner next external target: common-synapse FCI

This note is a **post-result follow-up**, not a modification of the frozen v0.1 gate.

## Why the resolved-16 pass is suspicious

The original Fig. 2 FCI target mixes at least two species-linked causes:

```text
morphology
+
species-specific synaptic parameters / NMDA nonlinearity
```

Our V22 features are morphology-only. On the resolved-16 subset, a one-bit species indicator predicts the Fig. 2 FCI extremely well. Therefore a morphology feature that happens to separate rat from human can indirectly predict **species-specific synaptic physics that it never measured**.

That is a legitimate predictive correlation but a bad target for the narrower mechanistic question:

> Does morphology/operator structure itself explain functional complexity beyond ordinary morphology?

## The paper already contains the right intervention

Aizenbud et al. repeat the FCI comparison after assigning **rat-type synapses to both rat and human morphologies**. The paper reports that the human morphology group still has significantly higher FCI on average (`p = 0.022`).

Conceptually that condition is much cleaner for V22:

```text
same synapse regime
       |
       +--> rat morphology
       |
       +--> human morphology
```

Now species identity cannot win merely by standing in for different synaptic parameter sets.

## Proposed future gate

Only if the per-cell common-rat-synapse FCI values can be recovered externally, freeze a new analysis before fitting them:

```text
TARGET
  each cell's FCI under the common rat-synapse condition

BASELINE
  same B2 as v0.1

OPERATOR
  same frozen G1/G2/G3 initially

PRIMARY QUESTION
  does B2+G improve held-out prediction over B2
  when the synapse species difference has been experimentally removed?
```

Do not digitize a plot and then redesign the model around the resulting values. Prefer released numeric data or an author-provided table.

## Why this is now more important than inventing G4

The resolved-16 gate passed dramatically, but the species-only diagnostic nearly explains the excitement away. The scientifically useful response is not to search for stronger graph features. It is to find a target where the obvious confound has been removed by the original experimenters.

That would convert V22 from:

> morphology predicts a target strongly correlated with species

into the cleaner question:

> morphology predicts functional complexity **under matched synaptic physics**.

That is much closer to the claim GeometricNeuronV22 actually wants to earn.
