# Physical cable operator — post-gate direction

The frozen v0.1 external gate uses a deliberately simple structural operator. Do not change that gate after freezing it.

A more physically motivated v0.2 operator is available directly from the Aizenbud model assumptions.

For each cable segment, passive cable theory gives the schematic dependencies:

```text
axial coupling   proportional to radius^2 / (Ra * length)
membrane leak    proportional to membrane area / Rm
capacitance      proportional to Cm * membrane area
```

The linear passive system can therefore be written as

```text
C dV/dt = -(G_axial + G_leak) V + I
```

with morphology determining the matrices. The generalized eigenmodes of this system are physical passive voltage-relaxation modes of the reconstructed cell, not a claim that the neuron explicitly computes graph eigenvectors.

This matters because the paper fixes the same specific passive parameters across its morphologies (`Cm=1 uF/cm^2`, `Ra=150 ohm cm`, `Rm=20,000 ohm cm^2`). Morphology and diameters therefore determine the passive operator under common material constants.

The paper also rescales somatic/axonal active conductances using an electrical-load ratio `rho` based on dendritic input conductance. That suggests a strong simple physics baseline for later work: compare any modal descriptor against a small set including dendritic area, path length, and electrical load.

## Rule

Do not use this operator to rescue a failed v0.1 FCI gate. If investigated, preregister it as a separate physically motivated v0.2 test.
