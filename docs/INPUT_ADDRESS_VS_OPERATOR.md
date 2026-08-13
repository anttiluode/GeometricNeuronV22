# Input address space versus morphology operator

The Aizenbud paper states that the main simulations place **one excitatory AMPA+NMDA synapse and one inhibitory GABAA synapse per 1 micrometer of dendritic length**. The random simulation data use that same nominal density over the dendritic surface.

Therefore a larger tree can change at least two biological/computational things at once:

```text
A. electrical geometry / compartmentalization
B. number and spatial arrangement of nominal input sites
```

V22 calls these **operator capacity** and **address capacity**.

## Important source-code correction

An initial V22 audit briefly suspected a third issue: perhaps larger morphologies were simply giving the fixed-width TCN more input channels. Reading the released FCI simulator corrected that suspicion.

The one-per-micrometer inputs are **not** all exposed as separate TCN channels. The simulator first creates one excitatory and one inhibitory synaptic object per NEURON segment. The number of nominal 1-micrometer input sources associated with each segment is approximately the segment length, and their spike trains are pooled into a segment-level weighted `super-synapse` channel.

The trainer then stacks the excitatory and inhibitory segment-level matrices and sets

```python
in_chans = train_data[0]['sps_in'].shape[0]
model = Tcn(in_chans=in_chans, depth=args.depth, width=args.width, ...)
```

with the FCI default hidden width equal to 128.

Crucially, the released model files strongly indicate that the spatial discretization was deliberately adjusted to approximately **1040 dendritic segments per morphology**, rather than letting channel count scale freely with dendritic length. For the three public models for which V22 currently has both morphology length and released segment metadata:

```text
human 1125 L2/3
  V22 cable length       20633.00 um
  released avg seg len      19.839 um
  implied segments        ~1040.0

rat L2
  V22 cable length        4778.55 um
  released avg seg len       4.595 um
  implied segments        ~1039.9

rat Hay L5
  V22 cable length       12574.40 um
  released avg seg len      12.079 um
  implied segments        ~1041.0
```

The corresponding model constructors use very different segment chunk sizes (for example 40 um for the public human L2/3 model and 9.195 um for the public rat L2 model), which is exactly what one would expect if the goal is to keep the segment/channel count approximately fixed despite very different cable lengths.

So the strong version of the suspected surrogate-input-dimension confound is **not supported by the released code**. This is a useful kill, and V22 should preserve it.

Do not claim that human FCI is higher merely because a human morphology presents more TCN input channels. The public implementation appears designed to prevent that simple explanation.

## What still remains worth separating

The biological/address distinction survives in a subtler form.

A longer dendritic tree still represents more nominal one-per-micrometer input sources. In the released implementation, more of those sources are pooled into each of roughly the same number of segment-level channels. Thus larger morphology can still change:

```text
operator geometry
+ nominal input address count
+ how many nominal input sources are mixed within each spatial segment
```

That is not automatically a flaw in FCI. A larger biological dendrite really can expose more synaptic input locations, and the paper is explicitly interested in the complete neuron I/O transformation. The paper also normalizes input regimes to produce about 1 spike/s output and reports robustness to structured spatiotemporal inputs and biologically realistic nonuniform placement.

The remaining question is therefore mechanistic, not accusatory:

> How much of morphology-dependent complexity comes from the electrical operator itself, versus the extra spatial input-address capacity that a larger dendritic surface physically provides?

## Post-gate mechanism audit

Do not alter the frozen V22 v0.1 prediction gate. After that gate is run, separate the mechanisms with three arms.

### A. Native-density condition

Reproduce the paper-like condition:

```text
nominal input density scales with dendritic length
approximately matched segment-level TCN channel count
real morphology and cable dynamics
```

This contains both operator and address capacity.

### B. Fixed-address condition

Give every morphology the same total number `K` of excitatory and `K` inhibitory nominal input sources. Sample them by a preregistered stratification over path distance / branch class while keeping the segment-level observation scheme matched.

Keep:

- identical TCN architecture and effective input dimensionality;
- matched input statistics;
- matched target output firing-rate regime;
- the actual morphology and cable dynamics.

If morphology-dependent complexity survives here, it supports an operator effect beyond simply exposing more nominal input addresses.

### C. Pooling/address-only control

Hold the underlying transfer system deliberately simple while varying how many nominal input sources are pooled into a fixed number of observed segment-level channels. This asks whether source multiplicity/pooling alone makes the fixed TCN approximation harder or easier.

The direction is not assumed in advance. Pooling could increase stochastic/combinatorial richness, but it could also average inputs and simplify them. Let the control say which.

## Outcomes

```text
A differs, B survives, C weak
    -> operator capacity is strongly supported

A differs, B collapses, C strong
    -> input-address / pooling capacity explains much of the effect

A differs, B survives, C strong
    -> both mechanisms contribute

A weak after fair controls
    -> morphology story narrows substantially
```

The point is not to debunk the paper. The useful result would be a cleaner decomposition of what a large dendritic tree buys computationally.

## PivotPoint seam: effective dendritic control degrees of freedom

This distinction creates a more precise bridge to PivotPoint.

PivotPoint's useful control degree of freedom is not another named action; it is a materially distinct reachable future. Apply the same logic inside a dendritic tree.

For a fixed morphology and operating state, apply the same small test input at location `i` and observe the future receiver trajectory, initially at the soma:

```text
site i -> cable dynamics -> somatic response h_i(t)
```

Two physical sites should not count as two useful degrees of freedom if they produce effectively the same receiver trajectory. A stronger quantity than raw synapse count is therefore the **effective diversity of location-to-receiver transfer kernels**.

With the same number `K` of sampled sites for every morphology, build a transfer dictionary:

```text
H = [vec(h_1) vec(h_2) ... vec(h_K)]
```

Possible descriptive quantities include effective rank, singular-value entropy, or response clusters above a fixed tolerance. Report both raw responses and column-normalized responses so simple attenuation is separated from temporal-shape diversity.

This brings time into Geometric Neuron without needing a vague "wide present" claim. Morphology can convert input location into different latency, rise/decay, attenuation, and relaxation-mode mixtures. The concrete question becomes:

> **How many materially different future receiver trajectories can this morphology produce when only the input location changes?**

That is very close to PivotPoint's operational control-DOF definition, now applied inside one cell.

The passive case is only the baseline. Local NMDA-like nonlinearities can make the effect of one input depend on simultaneous activity and current voltage state, so the effective repertoire of reachable futures can itself become state-dependent. This does not imply that dendrites choose or that neurons are conscious; it is a statement about conditional local influence.

A later, separately preregistered ladder would be:

1. **D0 — passive fixed-K transfer diversity:** same material constants, same `K`, same observation horizon, real morphologies.
2. **D1 — matched morphology controls:** preserve simple size/path quantities while altering branch allocation; if size/path explains the effect, stop.
3. **D2 — nonlinear expansion:** only after D0/D1, test whether multi-site nonlinear responses occupy receiver trajectories outside the passive linear span.

The possible synthesis is therefore narrower than the old slogan "shape computes":

```text
morphology creates local input addresses
+ cable dynamics map addresses to temporal receiver trajectories
+ nonlinear local state changes which combinations are effective
= state-dependent reachable receiver futures
```

If real morphologies do not show this beyond ordinary area/path effects, the bridge dies. If they do, V22 has a direct route toward an artificial-neuron design later: a small tree of local stateful subunits evaluated by the distinct downstream effects they can create, rather than by decorative geometric complexity.
