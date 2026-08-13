# Input address space versus morphology operator

The Aizenbud models use the same passive specific membrane parameters across morphologies, but place one excitatory and one inhibitory synapse per micrometer of dendritic length.

Therefore a larger tree changes two things at once:

```text
A. electrical geometry / compartmentalization
B. number and spatial arrangement of input sites
```

V22 should keep these separate conceptually. Call them **operator capacity** and **address capacity**.

The paper reports robustness to other input protocols, so this is not a claim that its morphology result is an artifact. It is a cleaner decomposition for our mechanism work.

After the frozen 24-cell prediction gate, a useful controlled experiment is to compare native input density with a fixed total input-site budget per morphology. If differences survive with equal input count, morphology-dependent electrical dynamics have an effect beyond simply providing more input addresses.

This later experiment is a mechanism probe, not a rescue of the preregistered FCI gate.
