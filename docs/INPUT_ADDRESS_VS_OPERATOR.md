# Input address space versus morphology operator

The Aizenbud models use the same passive specific membrane parameters across morphologies, but their main simulation places **one excitatory AMPA+NMDA synapse and one inhibitory GABAA synapse per 1 micrometer of dendritic length**. The random simulation data use that same density over the dendritic surface.

Therefore a larger tree changes at least two things at once:

```text
A. electrical geometry / compartmentalization
B. number and spatial arrangement of input sites
```

V22 calls these **operator capacity** and **address capacity**.

This is not only a conceptual distinction. The released FCI trainer makes the input-domain dependence explicit:

```python
in_chans = train_data[0]['sps_in'].shape[0]
model = Tcn(in_chans=in_chans, depth=args.depth, width=args.width, ...)
```

The excitatory and inhibitory weighted-spike matrices are stacked before entering the network, and the first causal convolution maps the morphology-dependent `in_chans` to a fixed hidden width. The FCI default is `width=128`.

So the cross-morphology approximation problem is not strictly a comparison of functions on one fixed-dimensional input domain. Bigger/longer trees also present the fixed-width surrogate with more independently addressable input channels.

That is not automatically a flaw in FCI. A larger biological dendrite really can expose more synaptic input locations, and the paper is explicitly interested in the neuron's complete input/output transformation. But it changes the interpretation:

> FCI can contain both **complexity of the dendritic operator** and **complexity contributed by a larger input address space / compression problem**.

The paper normalizes input firing-rate regimes so that modeled neurons fire at about 1 spike/s, and reports robustness to structured spatiotemporal inputs and biologically realistic nonuniform placement. Those are important controls. They do not, from the main paper alone, establish what happens when the **total number of input channels is held fixed across morphologies**.

## Post-gate audit

Do not alter the frozen V22 v0.1 prediction gate. After that gate is run, separate the two mechanisms with three arms.

### A. Native-density FCI

Reproduce the paper-like condition:

```text
~1 excitatory + 1 inhibitory site per micrometer
morphology-dependent input dimension
fixed TCN width
```

This contains both operator and address capacity.

### B. Fixed-address FCI

Give every morphology the same total number `K` of excitatory and `K` inhibitory sites. Sample them by a preregistered stratification over path distance / branch class rather than letting larger trees receive more channels.

Keep:

- identical TCN architecture and width;
- matched input statistics;
- matched target output firing-rate regime;
- the actual morphology and cable dynamics.

If morphology-dependent FCI differences survive here, there is evidence for an operator effect beyond merely exposing more input coordinates.

### C. Address-only null

Construct a deliberately simple transfer system whose intrinsic operator is held fixed while only the number of independent input channels varies across the range induced by the morphologies. Train the same fixed-width TCN.

If FCI rises strongly with `in_chans` even for this trivial system, then part of the native morphology/FCI relationship is a property of the approximation bottleneck and input-domain dimensionality.

## Outcomes

```text
A differs, B survives, C weak
    -> operator capacity is strongly supported

A differs, B collapses, C strong
    -> address/input-dimension capacity explains much of the effect

A differs, B survives, C strong
    -> both mechanisms contribute

A weak after fair controls
    -> morphology story narrows substantially
```

The point is not to "debunk" the paper. The useful result would be a cleaner decomposition of what a large dendritic tree buys computationally.

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

This also brings time into Geometric Neuron without needing a vague "wide present" claim. Morphology can convert input location into different latency, rise/decay, attenuation, and relaxation-mode mixtures. The concrete question becomes:

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
