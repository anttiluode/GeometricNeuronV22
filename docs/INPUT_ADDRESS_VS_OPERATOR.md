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

## PivotPoint seam

This distinction also creates a precise bridge to PivotPoint. A dendritic location is not interesting merely because it is another coordinate. It is interesting if an intervention there can produce a **materially distinct future state** at a receiver such as the soma or another compartment.

That motivates a stronger quantity than raw synapse count: **effective dendritic control degrees of freedom**. See `PIVOTPOINT_BRIDGE.md`.
