# External FCI geometry gate v0.1

Status: **frozen before opening the 24 cell-level FCI labels.**

This gate was first written in `GeometricNeuronPlusField/FCI_EXTERNAL_GEOMETRY_PREREG_V01.md` and is carried into V22 unchanged in substance.

## Question

Does a frozen graph/operator description add held-out information about neuronal functional complexity beyond ordinary dendritic size/path morphometrics?

## Graph construction

For each dendritic reconstruction:

1. identify the soma/root;
2. keep dendritic cable geometry for the primary graph;
3. collapse consecutive reconstruction samples between structural events;
4. structural nodes are soma/root, bifurcations, and terminal tips;
5. each collapsed edge stores cable length and approximate membrane area;
6. exclude axon from the primary morphology graph when present.

The collapse is essential: operator features should not depend mainly on how densely a tracing program sampled points along the same cable.

Primary cable operator:

```text
w_ij = 1 / ell_ij
L = D - W
L_M = M^(-1/2) L M^(-1/2)
```

Node mass receives half of each incident edge's membrane area.

## Ordinary morphology baseline

Primary baseline:

```text
B2 = [log_total_dendritic_area,
      log_longest_root_to_tip_path]
```

Also report total dendritic length and number of bifurcations, but do not tune the primary baseline against the target.

## Frozen operator features

Use the first `K = 16` nonzero eigenpairs, or all available nonzero modes if fewer exist.

Exactly three confirmatory features:

```text
G1  normalized entropy of the first-K nonzero eigenvalues
G2  normalized entropy of root modal participation
G3  coefficient-like irregularity of adjacent log-eigenvalue spacing
```

No extra graph feature may be added to rescue this confirmatory gate after labels are opened.

## Prediction

Because the dataset is tiny, use fixed ridge regression (`alpha = 1.0`) with standardization inside each training fold.

Compare:

```text
B2
B2 + G1 + G2 + G3
```

Primary validation is leave-one-cell-out cross-validation.

Report CV R^2, MAE, Spearman correlation, and paired absolute-error improvement for every held-out cell.

## Gate

Call only:

```text
OPERATOR_ADDS_EXTERNAL_COMPLEXITY_SIGNAL
```

if all are true:

1. CV R^2 improves over B2;
2. MAE improves by at least 10%;
3. mean paired absolute-error improvement is positive;
4. bootstrap 95% CI of the mean paired improvement is entirely above zero;
5. two-sided sign-flip p < 0.05.

Otherwise:

```text
NO_EXTERNAL_OPERATOR_ADVANTAGE
```

A single feature correlation, a human-vs-rat separation, or a high in-sample R^2 does not pass.

## Interpretation

Pass: the small frozen operator description carries external predictive information beyond the ordinary baseline in this dataset.

Fail: the external morphology result is already captured at a simpler level than the current Geometric Neuron operator description.
