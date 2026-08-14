# Geometric Neuron, evolved

> **Working picture, not a claim that this is how a biological neuron "really" computes.**
>
> This note is the conceptual descendant of the original Perception Laboratory accident, rewritten after contact with Aizenbud et al. 2026, the V22 matched-synapse null, and ordinary dendritic neuroscience.

## 1. The accident we actually started from

The original loop was almost embarrassingly simple:

```text
constant signal
      |
      v
homeostatic coupler
      |
      | scalar output controls checker size
      v
checkerboard image
      |
      v
Image -> Vector
      |
      v
Vector Splitter
      |
      | first few scalar taps
      +---------------------------> homeostatic coupler
```

The saved Perception Laboratory graph confirms the literal topology: the coupler drove `Checkerboard.square_size`; the checkerboard image went through a 256-dimensional `ImageToVector`; and splitter outputs `out_0` through `out_3` were fed back into the coupler. The constant signal supplied a stable setpoint modulation.

The checkerboard node itself was not intelligent. It generated a regular two-dimensional pattern from one scalar square-size control. `ImageToVector` then downsampled the image to a small spatial grid and flattened it, and the splitter exposed individual coordinates again. The homeostatic coupler supplied the slow/nonlinear feedback machinery that kept the loop from simply exploding or collapsing.

Yet the closed loop produced unexpectedly structured, ECG-like dynamics.

The original Geometric Neuron speculation grew from a naive question:

> What if a neuron contains something more spatial than the usual weighted-sum picture suggests?

That literal picture was too unconstrained. There is no evidence that a soma contains a checkerboard, that neurons secretly perform image vectorization, or that the particular Perception Laboratory controller maps onto a biological homeostat.

But the accident contained a better abstraction that took much longer to see:

> **A distributed spatial state can be written, selectively read, compressed through a small output bottleneck, and fed back into what happens next.**

That is the part worth carrying forward.

---

## 2. The checkerboard should not survive. The writable spatial state should.

The most important correction is to stop treating the checkerboard as the biological object.

A dendritic arbor already supplies a real spatially extended dynamical state. At any moment different cable locations can have different membrane voltages, recent synaptic histories, local conductance states, branch-specific input coincidences, and different distances and transfer paths to the soma.

So the evolved analogy is not:

```text
checkerboard == dendrite
```

It is:

```text
checkerboard intuition
        ->
there exists an extended state with many addressable locations
```

And unlike the original checkerboard, the biological version is **writable**.

Synaptic events write locally into that state. Neighboring cable changes the consequence of the write. Voltage-dependent conductances make the effect depend on what is already happening there. The state then continues to evolve rather than being regenerated from one scalar control.

This makes the dendrite closer to the hypothetical Perception Laboratory system we later wished we had built: a field-like object with many local write sites, multiple coupled regions, and state that persists long enough for one local event to alter the meaning of another.

"Field" here is deliberately modest language. It does not require a new physical field. The spatially distributed membrane/conductance state of an ordinary compartmental neuron is enough.

---

## 3. Soma as Image->Vector: useful analogy, wrong literal mechanism

The original `ImageToVector` node took a large two-dimensional object and reduced it to a much smaller representation.

A biological soma does not flatten a dendritic image into a vector. But the **computational bottleneck** is strikingly similar.

The dendritic tree may contain a very high-dimensional internal state:

```text
u_1(t), u_2(t), ... u_N(t)
```

where each `u_i` stands for the local electrical/biophysical state of a dendritic region. Downstream cells do not receive that complete map. What becomes externally consequential is a far smaller receiver trajectory: somatic voltage, spike initiation dynamics, and ultimately an axonal spike train.

So the evolved analogy is:

```text
large distributed internal state
             |
             v
      soma / axon readout
             |
             v
small externally visible trajectory
```

This is why the readout matters as much as the internal richness.

A dendritic tree can contain many internal modes that are practically invisible at the soma. Those states should not automatically be counted as useful computation. Conversely, two local inputs that produce reliably distinct somatic futures are functionally distinguishable even if the whole tree has a low-dimensional global description.

The useful question therefore shifts from:

> How complicated is the dendrite internally?

into:

> **Which differences inside the dendrite survive the projection to a receiver?**

That is the biological descendant of `ImageToVector`.

---

## 4. The Vector Splitter becomes selective access, not literal coordinates

The original accident did something severe: it created a 256-value representation and then fed only a few scalar coordinates back into the controller.

That meant most of the representation could exist without influencing the next loop state. A tiny subset of readout locations was load-bearing.

The evolved biological idea is not that dendrites contain numbered vector coordinates. It is that **access is selective**.

Different synapses, branches, active zones, branch points, inhibitory locations, and receiver paths expose different pieces of the distributed state to future dynamics. Merely having an internal degree of freedom is not enough. It matters only if some downstream process can be changed by it.

This gives a stronger definition of a dendritic computational degree of freedom:

> Two local states or input locations count as different only when they can create materially distinguishable future receiver trajectories under a fixed comparison rule.

That is stricter than counting branches, synapses, graph modes, or compartments.

---

## 5. What the Aizenbud paper changes

Aizenbud et al. 2026 provides an unusually useful collision because it asks a neighboring question with independently reconstructed neurons and detailed biophysical simulations.

Their result says, in broad terms:

```text
larger / more extended / differently allocated dendritic morphology
+
local synaptic nonlinearity, especially NMDA-like behavior
=
harder-to-approximate neuronal input/output mapping
```

The paper argues that larger dendritic surface, greater extent, and richer branching can support more compartmentalized processing: semi-independent dendritic subregions whose interactions make the whole input/output transformation richer.

That is much closer to the evolved Geometric Neuron than the old claim that complicated shape is itself the computation.

The paper also forced an important separation. In the original rat-versus-human comparison, morphology and species-specific synaptic properties both contributed. In SI Fig. S5 the authors gave every morphology the same rat-type synapses. Human morphology still had a group-level advantage, but the species gap shrank substantially.

V22 then supplied its own correction: the frozen abstract graph-modal features `G1/G2/G3` looked spectacular on the original mixed-physics target, but lost their advantage when tested against the common-synapse condition. Ordinary area + longest path was already strong.

So the evolved model should **not** say:

```text
complex global graph spectrum = neuronal computation
```

The v0.1 experiment did not earn that.

Instead the paper and the null point toward a more local and physical picture:

```text
where an input is written
        x
how geometry transfers it
        x
what nonlinear state exists there
        x
what the receiver can distinguish
```

The multiplication signs matter. Remove any one factor and the computational repertoire can collapse.

---

## 6. Geometry is an address-and-transfer medium, not a hidden code

The evolved Geometric Neuron therefore treats morphology as doing two related jobs.

First, geometry provides **addresses**. A long branched arbor exposes many physically distinct places where inputs can arrive.

Second, geometry provides a **transfer system**. The same small perturbation delivered to two sites can arrive at the soma with different attenuation, latency, rise/decay profile, interaction partners, and mixture of relaxation modes.

Those two effects should not be conflated. More synaptic locations are not automatically more useful degrees of freedom, and a complicated passive transfer function is not automatically functional complexity.

For a fixed morphology and a fixed operating state, imagine applying the same small test input at each of `K` locations:

```text
site i -> dendritic dynamics -> receiver trajectory h_i(t)
```

Build the response dictionary

```text
H = [ vec(h_1)  vec(h_2) ... vec(h_K) ]
```

The relevant quantity is not simply `K`. It is the diversity of the columns of `H` after ordinary attenuation/size effects are controlled.

If a hundred sites all create the same normalized receiver trajectory, they are a hundred physical addresses but close to one effective readout class.

If nearby sites create reliably different downstream futures, geometry has converted location into consequential state.

This is the current core of Geometric Neuron.

---

## 7. Local nonlinearity makes the field genuinely writable

A passive dendritic tree is already stateful because membrane capacitance gives it temporal evolution, but in the linear regime one perturbation mostly superposes with another.

Local nonlinear conductances change the game.

A minimal compartment picture is ordinary cable neuroscience:

```text
C_i du_i/dt
    = sum_j G_ij (u_j - u_i)
      - gL_i (u_i - E_L)
      + I_syn,i(u_i, x_i, m_i)
```

`G_ij` is determined by cable geometry and axial resistance. `C_i` and leak scale with membrane area. The interesting term is `I_syn,i`: with voltage-dependent synapses or active conductances, the effect of an input depends on the current local state.

Then the same write is no longer guaranteed to mean the same thing twice:

```text
input at site i + quiet branch
    !=
input at site i + already depolarized branch
```

This is where "writable field" becomes more than a metaphor. One event changes the state in which the next event is interpreted.

The evolved Geometric Neuron therefore puts **state-dependent local interaction** above global graph complexity.

---

## 8. The Homeostatic Coupler survives only as a slow-control hint

The original Homeostatic Coupler was the accidental governor that made the loop interesting. It had a setpoint, bounded nonlinearity, slow integral state, a dead zone, and an `edge_of_chaos` mode that amplified deviations when recent variance was too low and damped them when variance was too high.

That is software, not a biological model.

Still, it contributed one useful architectural intuition: fast local dynamics may live inside a slower control context.

A biological analogue could be homeostatic excitability, neuromodulation, slow conductance changes, receptor state, plasticity, metabolic constraint, or some other slow process that changes the effective gain of fast dendritic events.

The evolved model does not require one particular controller. It only leaves room for

```text
fast writable dendritic state
+
slow state that changes what local events can do
```

because that makes the set of effective receiver futures state-dependent.

This is a hypothesis to test, not a mapping from the Perception Laboratory node to one named biological mechanism.

---

## 9. The evolved Geometric Neuron in one picture

```text
                   slow context m(t)
                         |
                         v
input x_i(t) ---> [ local writable state u_i ]
                         |
                  geometry / cable
                  coupling between
                    local regions
                         |
            local nonlinear interactions
                         |
                         v
                 distributed state U(t)
                         |
                         v
                   SOMA / AXON
                 lossy projection R
                         |
                         v
                 receiver future y(t)
```

The architecture is not defined by a special checkerboard, eigenbasis, fractal pattern, or soma shape.

It is defined by five relationships:

1. **addressed write** — inputs perturb particular locations rather than an undifferentiated scalar sum;
2. **geometric transfer** — physical placement changes how perturbations spread and combine;
3. **local state dependence** — nonlinear events depend on what is already happening locally;
4. **receiver bottleneck** — only some internal distinctions survive into downstream behavior;
5. **slow context** — optional slower variables can alter which local interactions are effective.

That is the evolved Geometric Neuron working picture.

---

## 10. What is standard neuroscience and what is our speculative layer

Most ingredients above are not novel: dendritic cable theory, compartmentalized voltage, NMDA nonlinearities, branch-specific integration, active conductances, somatic integration, and homeostatic/neuromodulatory control are established neuroscience topics.

The Geometric Neuron contribution is therefore **not** "neurons have dendrites" or "dendrites are nonlinear."

The speculative synthesis inherited from the accident is narrower:

> Treat the neuron as a **stateful addressed medium** and judge its internal degrees of freedom by the distinct downstream futures that local writes can actually produce.

That framing connects the Perception Laboratory accident to real dendritic neuroscience without asking biology to resemble our software boxes.

It also tells us what would falsify the idea.

If, after strong controls for area, path length, branch allocation, input count, and ordinary cable properties, different local writes collapse to essentially the same small family of receiver trajectories, there is little earned Geometric Neuron content left.

If local nonlinear state does not expand or reorganize those receiver-distinguishable futures beyond passive transfer, then the nonlinear part of the picture also dies.

The burden is on the geometry/state story to beat simpler explanations.

---

## 11. What V22 v0.1 killed, and why that improves the concept

V22 v0.1 tested global structural summaries:

```text
G1 spectral entropy
G2 root modal-participation entropy
G3 low-mode spacing irregularity
```

They were good species fingerprints but did not improve held-out prediction of the matched-synapse FCI target over ordinary area + path.

That null removes a tempting but weak branch of the idea:

> complicated whole-tree spectrum = extra computation.

The evolved version does not rescue those features. It moves the claim to a different measurable object:

```text
local write
   -> state-dependent propagation/interactions
   -> distinguishable receiver future
```

The next external tests therefore should not search for a prettier graph statistic on the exposed FCI target. They should ask whether real neurons exhibit receiver-distinguishable location/state effects beyond strong ordinary morphology and cable baselines.

That is a new test. It is allowed to fail.

---

## 12. From accidental toy to a more realistic artificial neuron

If this picture is ever turned back into an artificial neuron, the descendant should not recreate the checkerboard.

A closer artificial analogue would contain a small tree or spatial mesh of local stateful units. Inputs would be assigned to addresses. Edges would transmit state with controlled delay/attenuation. Some local units would have bounded state-dependent nonlinearities. A small receiver would observe the resulting dynamics. Optional slow modulators would alter gains or thresholds.

The learning objective would not reward decorative geometric complexity. It would reward useful downstream distinctions on held-out tasks while comparing against strong ordinary baselines.

In other words, the artificial version should inherit the **relationships** from the accident, not the accidental parts list.

---

# Short form

The original intuition was:

> maybe a neuron contains something image-like.

The evolved version is:

> **A neuron can be viewed as a spatially addressed, stateful dynamical medium. Inputs write locally; morphology determines transfer and interaction; nonlinear local state changes what a write means; and the soma/axon acts as a severe readout bottleneck. The useful computational degrees of freedom are the internal differences that survive as materially distinct downstream futures.**

The checkerboard was noise.

The loop was the clue.
