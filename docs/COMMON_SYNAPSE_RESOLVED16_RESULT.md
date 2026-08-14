# Common-rat-synapse resolved-16 result

Status: **COMMON_SYNAPSE_NO_OPERATOR_ADVANTAGE**.

This is the cleaner external follow-up to the spectacular but species-confounded original-Fig2 resolved-16 result.

The gate was frozen in `COMMON_SYNAPSE_RESOLVED16_GATE.md` before fitting this target. The Figure-S5 values had already been visually recovered, so the test is not outcome-blind; however, the morphology panel, B2 baseline, G1/G2/G3 features, ridge alpha, LOOCV procedure, and five-part success rule were all fixed before this fit.

GitHub Actions run:

```text
31778100080
```

completed successfully.

## Result

```text
n = 16

target:
  SI Fig. S5 FCI
  all morphologies equipped with identical rat-type synapses

B2
  CV R2       0.627747
  MAE         0.024057
  Spearman    0.720588

B2 + G
  CV R2       0.608452
  MAE         0.024927
  Spearman    0.720588

relative MAE improvement       -3.62 %
mean paired error improvement  -0.0008706
bootstrap 95 % CI              [-0.007255, +0.005164]
exact two-sided sign-flip p      0.79355
```

The operator arm fails essentially every criterion. It slightly **worsens** both CV R2 and MAE.

Frozen verdict:

```text
COMMON_SYNAPSE_NO_OPERATOR_ADVANTAGE
```

## This resolves the main confound unusually cleanly

The previous original-Fig2 resolved-16 test looked dramatic:

```text
original Fig2 target

B2      CV R2  ~0.112
B2+G    CV R2  ~0.755
MAE improvement ~48.6 %
```

But a one-bit species indicator alone gave CV R2 ~0.796 on that target. The original target combines morphology with species-specific synaptic/NMDA parameters.

After the original authors perform the intervention we wanted -- **rat-type synapses on every morphology** -- the picture reverses:

```text
common-synapse target

B2      CV R2  0.628
B2+G    CV R2  0.608
```

And, critically, the one-bit species diagnostic now collapses:

```text
species only
  CV R2   0.0061
  MAE     0.03721
```

So the matched-synapse target did what it was supposed to do: it removed the trivial ability of species identity to stand in for species-specific synaptic physics.

Under that cleaner target, ordinary area + path is strong and the frozen abstract operator features add no held-out advantage.

## Fixed post-result adversaries

```text
species only
  R2   0.0061
  MAE  0.03721

B2 + species
  R2   0.6680
  MAE  0.02192

B2 + G + species
  R2   0.5518
  MAE  0.02650
```

Adding G after B2+species makes the held-out model worse.

Within-species exploratory diagnostics point the same way:

```text
Rat only, n=5
  B2     R2 +0.227, MAE 0.01510
  B2+G   R2 -0.552, MAE 0.02442

Human only, n=11
  B2     R2 +0.571, MAE 0.02596
  B2+G   R2 +0.351, MAE 0.02978
```

The subgroup sizes are small, so these are diagnostics rather than separate confirmatory claims. Their role is simply to make a hidden rescue story harder.

## Interpretation

The cleanest current reading is:

> The frozen V22 graph-modal features G1/G2/G3 were excellent predictors of a target that strongly separated rat and human cells, but they do **not** improve held-out prediction once the original experimenters remove species-specific synaptic parameters.

That makes the spectacular original resolved-16 signal look primarily like a **species-correlated target effect / morphology species fingerprint**, not evidence that these particular abstract operator descriptors capture the morphology-dependent computation measured by FCI.

This is a genuine negative result for **V22 v0.1**, not a failure of the Aizenbud morphology result. In fact, the ordinary B2 baseline becoming strong under the common-synapse intervention is broadly consistent with the paper's own conclusion that dendritic size/extent are important drivers of FCI.

## What is now dead

Do not claim from the resolved-16 work that:

- G1/G2/G3 predict FCI beyond species;
- abstract graph-modal structure explains the common-synapse morphology effect;
- the original 48.6% MAE improvement is mechanistic evidence for Geometric Neuron.

Do not add G4/G5 on this exposed target to rescue the result.

## What remains alive

The narrower external facts remain useful:

1. morphology itself matters in Aizenbud's simulations;
2. area/path already capture a substantial part of the cleaner common-synapse target;
3. the V22 provenance/recovery machinery is now reusable;
4. a future **physical cable operator** is still a conceptually different hypothesis, but it must be treated as a new test rather than a reinterpretation of this null.

The strict 24-cell original-Fig2 gate remains `BLOCKED_INCOMPLETE_PROVENANCE`, but its scientific priority is now lower: the cleaner common-synapse target has already answered the key species-confound question for the resolved panel.
