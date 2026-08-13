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

Only after the morphology gate is resolved should V22 consider the paper's second result, the additional contribution of synaptic nonlinearities.
