# project glossary

This glossary fixes provisional meanings for terms that the manifesto currently
uses across philosophy, history, network analysis, and cybernetics. Its purpose
is analytical discipline, not terminological closure. Every empirical use of a
term should still name its unit of analysis, scale, layer, and observation
window.

Three labels identify the status of a definition:

- **inherited** — drawn from a named intellectual tradition and not necessarily
  used consistently across that tradition;
- **technical** — tied to an established formal or empirical literature;
- **project-specific** — a reconstruction adopted by cybernetic mutualism and
  open to revision.

When an entry combines labels, the project-specific definition must not be
silently attributed to the inherited source.

## quick reference

| Term | Status | Working definition |
| --- | --- | --- |
| [Antinomy](#antinomy) | Inherited; project-specific | Opposed tendencies that remain mutually dependent within a shared relation. |
| [Topology](#topology) | Technical; project-specific | The structure of possible or observed relations in a specified communication network. |
| [Substrate](#substrate) | Project-specific | The material and technical capacities that make a range of communication relations feasible. |
| [Centralisation](#centralisation) | Technical; project-specific | The degree or increase of concentration in a specified network position, resource, or decision capacity. |
| [Decentralisation](#decentralisation) | Technical; project-specific | A decrease of concentration in a specified network position, resource, or decision capacity. |
| [Control](#control) | Technical; project-specific | Regulation that keeps selected variables within a target or viable range despite disturbance. |
| [Complexity](#complexity) | Technical; project-specific | A declared vector of structural or dynamical properties, never an unqualified rank. |
| [Progress](#progress) | Inherited; project-specific | Directional change in an explicitly named capacity or evaluative criterion at a stated scale. |

## antinomy

**Status:** inherited from Proudhon; reconstructed by the project.

An **antinomy** is a relation between opposed tendencies that are mutually
dependent: each is produced, enabled, or made intelligible by the relation that
also produces the other. Removing one pole would therefore transform or destroy
the relation, not merely settle a disagreement within it. Liberty and authority
in a federation, for example, qualify only if the account shows how common
coordination both depends on local autonomy and limits it.

The term does not mean any logical contradiction, political conflict, binary,
or trade-off. Nor does it imply that the two poles are morally equivalent, that
they have equal strength, or that their interaction reaches equilibrium. An
antinomic system may stabilise, oscillate, lock in, bifurcate, or collapse.

To use the term analytically, specify:

1. the two tendencies and the shared relation in which they arise;
2. the mechanism of mutual dependence or production;
3. the feedback signs, delays, constraints, and asymmetries;
4. the scale and period over which the relation persists;
5. evidence that eliminating either tendency changes the relation itself.

Proudhon's formulations vary across works and periods. The 1846 *System of
Economic Contradictions* describes terms that are necessary to one another yet
opposed; the 1853 *Philosophy of Progress* places antinomy within a broader idea
of serial order. The manifesto's emphasis on dynamical persistence without a
final synthesis is a project reconstruction. It should not be presented as a
settled summary of every Proudhonian use.

## topology

**Status:** technical in graph and network analysis; extended by the project.

The **topology of communication** is the relational structure of a specified
communication network. At minimum, represent it as a graph
`G = (V, E)`, with declared meanings for nodes `V` and edges `E`. Most project
uses will also require edge direction, weight, sign, layer, and time:
`G(t) = (V, E, w, d, l)`.

Topology answers questions such as who can address whom, through which
intermediaries, with what asymmetry, and along how many alternative paths. It
does not by itself describe message meaning or prove an effect on behaviour.
Physical distance, ownership, protocol authority, and actual traffic are not
synonyms for topology; they should appear as separate layers, attributes, or
explanatory variables when relevant.

Each empirical use must declare:

- the nodes, edge rule, direction, weight, and layer;
- whether an edge means technical possibility, legal permission, observed use,
  or successful receipt;
- the observation window and treatment of missing or inactive ties;
- the measures selected for the claim, such as degree distribution, path
  length, clustering, modularity, assortativity, or betweenness;
- the process expected to run on the network.

The project therefore uses *topology* more narrowly than "the whole
communication system." Network structure may constrain a process without being
its sole or deepest cause.

## substrate

**Status:** project-specific.

A **communication substrate** is the relatively durable material and technical
ensemble that enables signals to be produced, transmitted, copied, stored,
retrieved, and answered. A substrate is described by a capacity-and-cost profile
rather than a medium label alone. Relevant dimensions include reach, latency,
bandwidth, fidelity, durability, searchability, addressability, copying cost,
verification, and return-channel capacity.

For a substrate `σ`, `Ω(σ)` denotes the set of network topologies
that are materially and technically feasible under stated resource conditions.
Feasible does not mean likely, legal, profitable, or politically permitted.
Institutions select and maintain paths within this possibility space, while
ecology, energy, demography, ownership, and conflict can narrow it further.

Analysis should separate five layers that are often collapsed:

1. physical infrastructure and devices;
2. encoding, reproduction, and transport techniques;
3. protocols and standards;
4. ownership, access rules, and routing authority;
5. observed use and traffic.

This distinction exposes a necessary correction to the manifesto's provisional
sequence: **platform capture is not itself a substrate on the same level as
oral, scribal, print, broadcast, or digital communication**. It is an
institutional and ownership regime operating on digital substrates. Likewise,
"persistent, global, live interconnection" is currently a hypothesised capacity
profile, not an established historical substrate. Later work should revise the
sequence accordingly.

## centralisation

**Status:** technical in network analysis; extended by the project.

**Centralisation** is the degree to which a specified relation, resource, or
capacity is concentrated among a smaller share of nodes or positions, or a
change that increases that concentration. It is a network- or system-level
property. **Centrality**, by contrast, describes the position of a node within a
network. Freeman centralisation measures compare the observed dispersion of
node centralities with the maximum dispersion possible for a graph of the same
size.

There is no meaningful claim that a society or institution is simply
"centralised." At minimum, name the dimension:

- infrastructure ownership;
- graph position, using a declared centrality measure;
- routing or gatekeeping discretion;
- decision and enforcement authority;
- wealth or productive capacity;
- attention or epistemic authority;
- protocol and standard-setting power.

These dimensions can move in different directions. A network may distribute
physical nodes while centralising identity, discovery, or protocol control. A
central infrastructure may also increase the practical autonomy of peripheral
nodes. Measures are comparable only when node definitions, layers, scale, and
observation windows are held stable or their changes are modelled explicitly.

Centralisation is descriptive, not a synonym for domination, efficiency,
coordination, hierarchy, or moral failure. Those are possible mechanisms or
consequences to be tested.

## decentralisation

**Status:** technical in network analysis; extended by the project.

**Decentralisation** is a decrease in the concentration of a specified
relation, resource, or capacity across nodes or positions. It must be defined
against the same dimension and baseline used to define centralisation. A change
in degree centralisation, for example, says nothing by itself about ownership
concentration or decision rights.

Decentralisation is not equivalent to equal distribution, localism,
federation, democracy, resilience, openness, or the absence of hubs. It can
increase coordination cost, obscure accountability, or allow an unmeasured
layer to centralise. Conversely, formal hierarchy can coexist with distributed
experimentation or redundant routing.

A defensible claim should report the before-and-after distribution, the level
at which nodes are aggregated, the network layer, and the actors' exit and
interoperability conditions. Centralisation and decentralisation can occur
simultaneously at different scales or in different layers; they are paired
directions of measurement, not mutually exclusive institutional types.

## control

**Status:** technical in cybernetics and control theory; extended by the
project.

**Control** is a process by which actions keep selected variables near a target
or within a viable range despite disturbances. A control account must identify
the controlled variables, target or viability bounds, disturbances, sensing,
decision or transformation rule, actuation, feedback or feedforward channels,
delay, and cost.

A controller need not be a person, command centre, or unitary institution.
Regulation may be distributed across prices, norms, protocols, offices,
automatic devices, and reciprocal observation. "Control without a controller"
therefore means control without a single external or sovereign controller, not
the absence of regulation.

The term is analytically distinct from domination. A process can regulate
temperature, inventory, infection, or traffic without ranking persons; a
dominating institution can also fail to control the variables it claims to
govern. Political analysis must separately ask who selects the target, who can
alter the regulator, whose reports count, who bears errors and costs, and who
can exit or appeal.

Ashby's law of requisite variety supplies a necessary constraint: successful
regulation requires enough response variety to counter the disturbances that
matter. It does not establish that maximal variety, central command, or any
particular institution is sufficient for good control.

## complexity

**Status:** technical family of concepts; reconstructed by the project.

**Complexity** is not a single substance or universal ranking. In this project
it is a declared vector of properties selected because they bear on a causal
claim. Candidate dimensions include:

- number and diversity of components or states;
- differentiation of roles, functions, or communication codes;
- density and heterogeneity of relations;
- modularity, hierarchy, and cross-scale organisation;
- dynamical variety, nonlinearity, and path dependence;
- information needed to describe, predict, reproduce, or control the system;
- energetic and organisational cost of maintenance.

Connection count, size, Shannon entropy, algorithmic description length, and
hierarchical depth measure different things. None may stand in for complexity
without argument. More entropy can mean greater uncertainty rather than richer
organisation; more edges can mean repetition rather than differentiation; more
components can coexist with simpler dynamics.

Every use must name the object, dimension, measure, scale, and comparison class.
Claims about increasing historical complexity should be disaggregated into
testable trends with uncertainty ranges and negative cases. Complexity has no
automatic relation to intelligence, adaptability, resilience, justice, or
progress, and it can impose fragility, energy demand, and control burdens.

## progress

**Status:** inherited from Proudhon; reconstructed by the project.

**Progress** is directional change in an explicitly named capacity or
evaluative criterion at a stated scale and over a stated interval. A claim of
progress is incomplete until it answers: progress in what, for whom or for
which system, over what period, at what scale, and at what cost elsewhere?

The term has three uses that must remain separate:

1. **descriptive direction:** a measured variable changes persistently in a
   stated direction;
2. **functional improvement:** performance rises relative to a declared task or
   viability condition;
3. **normative improvement:** a change is judged better according to explicit
   values and affected standpoints.

The manifesto's historical hypothesis concerns serial and path-dependent
transformation, not universal moral ascent. Proudhon's *Philosophy of Progress*
opposes movement and seriality to absolutism, but the project's language of
feedback, phase transition, and scale-dependent gain is a later reconstruction.
It should not be attributed to him without qualification.

Progress should normally be represented as a vector. A transition can increase
extent and speed of communication while reducing autonomy, ecological
viability, or local knowledge. Gains at one layer or scale do not cancel losses
at another. The rival outcomes are direction, stagnation, reversal, or no
general tendency; survival of the cases easiest to observe is not evidence of a
universal law.

## source notes

These sources establish lineages and measurement problems; they do not by
themselves validate the project's reconstructions.

- W. Ross Ashby, [*An Introduction to Cybernetics*](https://ashby.info/Ashby-Introduction-to-Cybernetics.pdf)
  (1956), especially parts two and three on variety and regulation.
- Linton C. Freeman,
  ["Centrality in Social Networks: Conceptual Clarification"](https://doi.org/10.1016/0378-8733(78)90021-7),
  *Social Networks* 1 (1978/79): 215–239.
- M. E. J. Newman,
  ["The Structure and Function of Complex Networks"](https://doi.org/10.1137/S003614450342480),
  *SIAM Review* 45, no. 2 (2003): 167–256.
- Pierre-Joseph Proudhon,
  [*What Is Property?*](https://www.gutenberg.org/ebooks/360) (1840), for
  collective force and association.
- Pierre-Joseph Proudhon,
  [*System of Economic Contradictions; or, The Philosophy of Misery*](https://www.gutenberg.org/ebooks/444)
  (1846), especially chapter 2 on antinomy.
- Pierre-Joseph Proudhon,
  [*The Philosophy of Progress*](https://theanarchistlibrary.org/library/pierre-joseph-proudhon-the-philosophy-of-progress)
  (1853), working English translation by Shawn P. Wilbur.
- Claude E. Shannon,
  ["A Mathematical Theory of Communication"](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x),
  *Bell System Technical Journal* 27, no. 3 (1948): 379–423; and 27,
  no. 4: 623–656.
- Herbert A. Simon, ["The Architecture of Complexity"](https://www.jstor.org/stable/985254),
  *Proceedings of the American Philosophical Society* 106, no. 6 (1962):
  467–482.

## revision protocol

When later work changes an entry, record the claim or evidence that prompted the
change and link the relevant decision or claim-registry item. A revision should
state whether it corrects an inherited attribution, changes a project
definition, replaces a measure, or narrows the domain in which the term applies.
