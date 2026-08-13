# Aizenbud et al. 2026 — external contact

Paper: *Dendritic morphology and synaptic nonlinearities enhance functional complexity in human cortical neurons* (PNAS, 2026).

The paper is a useful external test because it reports strong relationships between dendritic morphology and a Functional Complexity Index (FCI), while simple branch count is much weaker than physical cable allocation.

Reported morphology results include roughly:

```text
number of bifurcation branches      R^2 ~ 0.29
total bifurcating-branch length     R^2 ~ 0.45
longest bifurcation branch          R^2 ~ 0.44
total dendritic area                R^2 ~ 0.74
area + longest bifurcation branch   R^2 ~ 0.81
best four morphology features       R^2 ~ 0.88
```

The important contact is therefore not merely "neurons are tree-shaped." It is that the physical allocation of membrane and cable through a branching structure is strongly associated with input/output complexity.

That creates a hostile benchmark for Geometric Neuron: ordinary morphology already explains a lot. V22 only earns something new if a small frozen operator/modal description improves held-out prediction beyond a strong area/path baseline.

The authors released code, reconstructed morphologies, and neuron models in `ido4848/FCI` on GitHub. V22 should use those released files directly.

## Source-code surprise: approximately fixed interface, different physical metric

A later source-code audit found a particularly relevant design choice.

The paper describes one excitatory and one inhibitory input source per micrometer of dendritic length. In the released simulator, those fine-grained sources are pooled into one excitatory and one inhibitory super-synapse per NEURON segment. The model-specific segment chunk sizes are then tuned so that very different morphologies have approximately the same number of dendritic segments.

Using V22's measured cable lengths and the released average segment lengths gives approximately:

```text
human 1125 L2/3    20633.00 / 19.839  ~= 1040 segments
rat L2              4778.55 /  4.595  ~= 1040 segments
rat Hay L5          12574.40 / 12.079  ~= 1041 segments
```

The released human 1125 constructor uses a 40 micrometer chunk size, while the rat L2 constructor uses 9.195 micrometers. This strongly suggests that the input discretization was intentionally normalized near a common segment count.

This kills a tempting but wrong easy explanation: the human neuron is not simply harder for the TCN because it has vastly more segment-level input channels.

It also sharpens the Geometric Neuron contact. At approximately fixed interface dimension, the physical metric underneath the interface changes dramatically:

```text
same-ish number of sampled compartments
but
very different cable length per compartment
very different membrane allocation
very different paths / branching geometry
```

So the Aizenbud setup is unexpectedly close to a **metric-geometry test at approximately fixed discretization size**. More nodes is not the explanation; what changes is how physical cable is allocated through and between those nodes.

This is consistent with the paper's morphology-only control: assigning rat-type synapses to both species reduces but does not eliminate the human/rat FCI difference. It is also consistent with the weak predictive value of raw bifurcation count compared with area/path allocation.

Do not overstate this. The biophysical models still differ in morphology-dependent electrical load, nominal fine-grained input-source multiplicity, and other modeled details. But it is a much cleaner external collision with V22 than the phrase "complex trees compute more" suggests.

Only after the frozen morphology gate is resolved should V22 consider the paper's second result, the additional contribution of synaptic nonlinearities or the post-gate PivotPoint/transfer-response branch described in `INPUT_ADDRESS_VS_OPERATOR.md`.
