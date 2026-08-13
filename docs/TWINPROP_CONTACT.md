# TwinProp contact

Aizenbud, Beniaguev, Pnueli, Segev and London (2026), **What can a neuron compute?** (`10.64898/2026.06.08.730984`), is an important external boundary for V22.

The paper uses a detailed rat L5 pyramidal-cell model plus **TwinProp**, a digital-twin/backpropagation method that optimizes synaptic strengths and dendritic locations. The optimized model performs naturalistic classification and nonlinear Boolean tasks, including reported 10-bit parity accuracy of 91.24% under the stated timing condition.

The causal ablations matter more than the headline. On 4-bit parity the paper reports approximately:

```text
intact L5PC       99.4%
passive dendrites 78.1%
soma-only         76.9%
no NMDA           73.8%
LIF               68.8%
```

Their conclusion is explicitly **not morphology alone**. Morphology, NMDA-mediated synaptic nonlinearities and voltage-dependent dendritic conductances work together. Increasing task dimensionality also recruits richer distributed dendritic voltage dynamics and more NMDA current.

This occupies much of the old Geometric Neuron claim-space. V22 should not present “dendritic geometry can support multilayer-like computation” as a new destination.

The useful boundary is what the TwinProp paper deliberately leaves aside: it asks what a neuron *can* compute after an external optimizer finds synaptic strengths and locations, not how a biological or artificial system could learn such configurations under constrained local rules.

That sharpens the post-v0.1 question:

> Can a constrained slow process discover and maintain a useful control structure in a rich dendritic-like fast substrate without an unrestricted optimizer specifying the whole computation?

This is where PivotPoint and FunctionalArbors may reconnect. A dendritic location should count as a distinct option only when a standardized input there creates a materially different future response at the receiver. The relevant object is therefore a dictionary of location-to-receiver trajectories, not branch count alone.

Do not change the frozen FCI gate because of this paper. If pursued later, compare any structural/control-surface learner against strong ordinary gradient adaptation and a TwinProp-like oracle. If those baselines are cheaper or better, the structural story loses.
