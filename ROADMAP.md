# cybernetic mutualism: research program and publication roadmap

## purpose

This document turns the provisional manifesto into a research program. Its aim
is not to defend thirteen theses in sequence, but to make them more precise,
expose them to contrary evidence, and discover where they must be revised.

The work should proceed in three interleaved forms:

1. **theoretical development** — definitions, mechanisms, formal models, and
   encounters with neighbouring traditions;
2. **historical and empirical inquiry** — comparative cases, datasets, source
   criticism, and deliberately selected counterexamples;
3. **constructive experimentation** — simulations, diagrams, small software
   models, and institutional thought experiments.

Posts are public research outputs, not merely announcements of conclusions.
When useful, they should show failed models, unresolved questions, and changes
of mind.

## standards for the program

Every major claim should eventually have:

- an explicit unit and scale of analysis;
- operational definitions for its central terms;
- a proposed causal mechanism rather than an analogy;
- at least one supportive case and one difficult or negative case;
- an account of plausible rival explanations;
- a formal representation where formalisation adds information;
- evidence that could weaken or falsify it;
- a record of how the claim changed during investigation.

Every case, experiment, and model note should end with **Conclusions and Next
Steps**. That section should state the result the artifact warrants now, its
consequence for the wider theory or claim registry, and the next action most
likely to discriminate between remaining explanations. Caveats must bound a
conclusion, not substitute for one.

The program should resist four recurrent failures:

- **topological reductionism:** treating communication as the sole cause rather
  than a prior constraint within a coupled system;
- **ornamental mathematics:** translating prose into symbols without gaining a
  new prediction, distinction, or test;
- **retrospective inevitability:** reading every outcome as confirmation of a
  theory flexible enough to explain anything;
- **normative leakage:** silently turning descriptions of recurrence, fitness,
  or stability into moral endorsements.

## common analytical language

The initial social circuit remains:

> communication topology → productive organisation → material and cultural
> artefacts → worldview and philosophy → political organisation → communication
> topology

Let its domains be `T`, `P`, `A`, `W`, and `S`. A useful formal starting point is
not a one-way chain but a coupled state:

```text
x(t) = [T(t), P(t), A(t), W(t), S(t)]
dx/dt = F(x, G, R, E, D, ξ)
```

Here `G` is the multilayer communication graph, `R` resource and energy
constraints, `E` ecological conditions, `D` demographic conditions, and `ξ`
unmodelled shocks and noise. A communication substrate `σ` defines a feasible
topology space `Ω(σ)`; institutions trace paths within that space.

This notation is provisional. Its value will depend on whether it helps
distinguish competing histories and generate conditional predictions.

## thirteen thesis modules

### 1. mutualism as a theory of progress

**Central question:** Can mutualism be reconstructed as a theory of historical
development rather than only a family of economic proposals?

Develop the meanings of seriality, collective force, progress, regression, and
phase transition in Proudhon. Separate what the sources establish from the
project's reconstruction. Compare linear, cyclical, dialectical, evolutionary,
and path-dependent accounts of change.

Test the thesis against episodes that combine progress at one scale with loss at
another: industrialisation, colonial infrastructure, welfare-state formation,
post-socialist transition, and digitalisation.

**Outputs:** a close-reading essay; a genealogy of the term *progress*; and a
diagram showing scale-dependent gains and losses.

### 2. antinomies as dynamical relations

**Central question:** When is an opposition an indissoluble relation rather than
a contradiction awaiting logical or historical resolution?

Translate antinomy into the language of coupled dynamics: mutual dependence,
positive and negative feedback, delay, saturation, and metastability. Compare
Proudhon with Hegel without reducing either to a slogan. Distinguish logical
contradictions, political conflicts, trade-offs, and co-constitutive processes.

Candidate cases include liberty/authority in federations, competition/
cooperation in open-source projects, autonomy/coordination in disaster
response, and central command/local initiative in revolutionary organisations.

**Experiment:** construct minimal two-variable models and identify which
behaviours—equilibrium, oscillation, lock-in, bifurcation, collapse—correspond to
different meanings of "balance."

### 3. communication as material constraint

**Central question:** In what defensible sense is communication topology
material and causally prior?

Define substrate, channel, signal, latency, fidelity, bandwidth, durability,
addressability, cost, and return capacity. Distinguish physical infrastructure,
protocol, ownership, routing authority, and actual use. Identify conditions
under which productive organisation changes before communication topology and
therefore challenges priority.

Comparative cases: scribal administration, print and confessional conflict,
telegraphy and integrated markets, rail and military mobilisation, broadcasting
and mass politics, containerisation, mobile money, and internet platforms.

**Outputs:** an operational vocabulary; a causal diagram; and an essay titled
"the base has a topology."

### 4. society as a recursive circuit

**Central question:** Does the five-domain circuit explain more than a generic
claim that everything affects everything?

Specify coupling strengths, delays, thresholds, and asymmetries between `T`,
`P`, `A`, `W`, and `S`. Establish criteria for assigning an observed phenomenon
to a domain and allow multilayer membership where necessary. Compare the circuit
with Marxian base/superstructure, cultural materialism, Luhmannian systems, and
actor-network approaches.

**Case reconstruction:** select one transition—such as print and the
Reformation—and narrate it five times, beginning from each domain. Compare which
account explains timing, geographic variation, and failed diffusion best.

**Simulation:** build a coupled five-variable model, then test whether observed
regimes require all five domains or whether a simpler model performs as well.

### 5. substrates define spaces; phases trace paths

**Central question:** Can a communication substrate define a measurable feasible
topology space without becoming a rigid stage theory?

Clarify overlap between oral, scribal, print, broadcast, digital, platform, and
persistent-live substrates. Develop indicators for the boundary of `Ω(σ)`:
maximum practical degree, distance cost, broadcast asymmetry, persistence,
searchability, verification, and coordination latency.

Use paired comparisons where the same nominal substrate yields different
institutions, and where similar institutions persist across different
substrates. Candidate comparisons include early modern print regions, radio in
democratic and authoritarian systems, and internet adoption under different
state capacities.

**Experiment:** impose changing graph constraints on identical agent rules and
measure which organisational forms become feasible, dominant, or extinct.

### 6. centralisation and decentralisation as coupled production

**Central question:** Under what conditions does decentralisation generate new
hubs, and when does centralisation enable autonomous edges?

Replace institutional labels with network measures: in-degree concentration,
betweenness, eigenvector centrality, modularity, assortativity, ownership,
protocol control, routing discretion, and exit cost. Distinguish centralisation
of infrastructure, decision, wealth, attention, and epistemic authority.

Cases should include the early web and platform capture, open protocols versus
proprietary platforms, electrical grids and microgeneration, cryptocurrency
mining and exchanges, federated social media, supply-chain standards, and party
federalism.

**Simulation:** allow preferential attachment, economies of scale, congestion,
exit, interoperability, and antitrust interventions. Map the parameter regions
in which decentralisation persists or recentralises.

### 7. productive conflict without moralised suffering

**Central question:** Which institutional conditions convert rivalry into
adaptation rather than monopoly, arms race, or collapse?

Connect excitation and inhibition to contestability, reciprocal guarantee,
transparency, resource ceilings, exit, federation, and punishment of capture.
Separate the explanatory claim that conflict can produce information from any
claim that pain or domination is desirable.

Compare scientific priority competition, open-source forks, regulated markets,
electoral opposition, adversarial legal systems, military arms races, and
ecological competitive exclusion.

**Experiment:** model populations with innovation benefits from rivalry and
nonlinear damage from escalation. Test which combinations of negative feedback
preserve diversity and output.

### 8. Marx as necessary and insufficient

**Central question:** What changes when communication topology joins or
displaces production relations at the deepest explanatory layer?

Identify propositions inherited from Marx rather than invoking "Marxism" as a
single object. Compare causal precedence in production-first and
communication-first explanations. Study how class power controls channels and
how new channels reorganise class formation.

Core cases: Soviet planning and information bottlenecks; Project Cybersyn;
Chinese reform, local experimentation, and political centralisation; logistics
and containerisation; financial data networks; platform labour; and the
attention economy.

**Comparative design:** for each case, construct rival timelines of changes in
communication, ownership, production, and state organisation. Look for temporal
precedence, necessary conditions, and cases where the proposed ordering fails.

**close reading:** pair Proudhon's 1846 *System of Economic Contradictions; or,
The Philosophy of Misery* with Marx's 1847 *The Poverty of Philosophy*.
reconstruct Marx's economic and dialectical objections, test them against
Proudhon's text and later work, and distinguish a real materialist correction
from polemical narrowing or retrospective Marxist canon formation.

### 9. direction without destination

**Central question:** Is increasing extent, persistence, speed,
differentiation, and complexity a real historical tendency or a selection-biased
description of survivors?

Disaggregate complexity into measurable properties. Distinguish greater
connectivity from greater variety, hierarchy, computation, and adaptive
capacity. Incorporate energetic cost, maintenance burden, ecological limits,
war, and catabolic simplification.

Cases: imperial collapse, loss and recovery of literacy, infrastructural decay,
long-distance trade contractions, state simplification, and rapid digital
expansion. Negative cases are essential.

**Evidence project:** assemble long-run proxies with uncertainty ranges and
pre-register what pattern would count as direction, stagnation, reversal, or no
general tendency.

### 10. determinism without predictive omniscience

**Central question:** What explanatory work does determinism do once uncertainty,
noise, reflexivity, and bounded models are admitted?

Separate metaphysical determinism from methodological causal explanation.
Develop the implications of path dependence, chaos, endogenous model use, and
second-order observation. Compare cybernetic accounts with compatibilism,
structural causation, critical realism, and Luhmann's observer-dependent
descriptions.

**Thought experiments:** self-defeating forecasts, public models that change the
system modelled, and interventions whose effects depend on belief in the model.

**Output:** an essay explaining why political action remains causal without
requiring an uncaused chooser.

### 11. control without a controller

**Central question:** How can societies steer when every steering apparatus is
inside the system, observes partially, and can itself be captured?

Operationalise sensing, model variety, memory, latency, actuation, audit,
Goodhart effects, and channel manipulation. Compare planning, markets,
democracy, bureaucracy, science, and media as incomplete control systems rather
than mutually exclusive answers.

Cases: Cybersyn; Soviet material balances; central-bank signalling; pandemic
response; disaster management; Wikipedia governance; content moderation; and
participatory budgeting.

**Simulation:** compare a central controller, price-mediated coordination,
polycentric governance, and hybrid recursive control under changing complexity,
delay, strategic reporting, and shocks.

### 12. making the theory risk failure

**Central question:** Which observations would genuinely make cybernetic
mutualism less credible?

Build a claim registry with confidence levels, predictions, rival hypotheses,
evidence for and against, and revision history. Separate failures of a dataset,
an operational measure, a local model, and the general program.

Initial adversarial tests:

- production or state changes consistently predict topology better than the
  reverse ordering;
- substrate changes fail to constrain observed network forms;
- centralisation cycles vanish when measured at explicit scales;
- coupled models do not outperform simpler independent-shock models;
- apparent increases in complexity are sampling artefacts;
- predicted capture does not occur where scale incentives are strongest.

**Output:** a public falsification ledger updated alongside later posts.

### 13. development through correction

**Central question:** What institutions allow an intellectual project to use
criticism as feedback without dissolving into incoherence or becoming a closed
doctrine?

Define versioned theses, issue-based criticism, source correction, model
replication, and explicit decision records. Distinguish pluralism from the
absence of a research object. Invite adversarial readings from mutualist,
Marxist, liberal, conservative, systems-theoretical, and empirical perspectives.

**Experiment:** publish selected claims with structured questions and track
which kinds of criticism produce clarification, revision, abandonment, or new
research branches.

**Output:** a living "changes to the theory" document rather than a retrospective
claim that every revision was already implicit.

## comparative case portfolio

Cases should be chosen for variation, not fame. The portfolio should contain:

- **substrate transitions:** writing, print, telegraph, broadcast, digital
  networks, and platform capture;
- **control systems:** Soviet planning, Cybersyn, Chinese experimentation,
  central banking, disaster response, and platform moderation;
- **polycentric systems:** federations, commons governance, open source,
  Wikipedia, scientific communities, and mutual-aid networks;
- **capture and recentralisation:** railways, telecommunications, cloud
  computing, app stores, cryptocurrency exchanges, and logistics platforms;
- **breakdown and simplification:** imperial fragmentation, infrastructural
  collapse, communications blackouts, sanctions, and ecological constraint;
- **negative cases:** transitions in which the expected topology change did not
  produce the predicted institution, or the institution changed without a
  preceding communication shift.

For every celebrated case, seek a matched comparison with a different outcome.
The China case, for example, should be compared across periods and provinces and
against another developmental state rather than treated as a self-explanatory
exception.

## evidence program

### source layers

1. **primary historical material:** correspondence, administrative records,
   laws, technical standards, budgets, maps, newspapers, and contemporary
   accounts;
2. **curated quantitative data:** trade, transport, postal, telegraph, media,
   demographic, firm, state-capacity, and internet datasets;
3. **network reconstructions:** nodes, edges, direction, weights, ownership,
   latency, and missing-data assumptions;
4. **secondary interpretations:** used comparatively, with disagreements made
   visible;
5. **project-generated data:** simulation outputs, coded timelines, claim
   registries, and replication packages.

### evidence ledger

Each important item should record provenance, date range, geographic coverage,
unit of analysis, transformation steps, uncertainty, access conditions, and the
claim for which it is evidence. Quotes and historical assertions should link to
page-level sources whenever possible.

### methodological toolkit

- comparative historical analysis and process tracing;
- temporal precedence and event-sequence analysis;
- social and multilayer network analysis;
- interrupted time series and event studies where identification permits;
- qualitative comparative analysis for medium-sized case sets;
- agent-based and dynamical-systems modelling;
- sensitivity, robustness, and ablation analysis;
- prediction and revision ledgers to constrain hindsight.

## simulation program

### model 1: hub formation and capture

Agents create edges for utility, trust, and reach. Scale economies and
preferential attachment favour hubs; congestion, exit, interoperability, and
countervailing rules oppose capture. The main outputs are concentration,
modularity, resilience, innovation rate, and user welfare under shocks.

### model 2: the five-domain circuit

Represent `T`, `P`, `A`, `W`, and `S` as delayed coupled variables. Explore
whether different coupling matrices produce stable regimes, oscillations,
lock-in, phase change, or collapse. Compare against reduced models to determine
whether the five-domain architecture earns its complexity.

### model 3: requisite variety and planning

An environment generates disturbances of changing variety. Central,
distributed, market-like, and polycentric controllers receive incomplete and
strategically distorted signals. Compare response quality, cost, latency,
adaptation, and capture.

### model 4: productive conflict

Rival agents gain information and innovation from contest but incur nonlinear
escalation costs. Test exit, transparency, resource ceilings, reciprocal
guarantees, federation, and sanctions as inhibitory mechanisms.

### model 5: substrate transition

Keep agent preferences fixed while changing feasible degree, distance cost,
latency, persistence, and broadcast asymmetry. Observe which institutions can
form and whether substrate change alone reproduces historical patterns.

Every simulation should ship with assumptions, source code, reproducible seeds,
parameter sweeps, negative results, and a plain-language account of what the
model cannot establish.

## tangents worth cultivating

Tangents earn a place when they alter a variable, mechanism, or test. Promising
directions include:

- cybernetics beyond metaphor: Wiener, Ashby, Beer, second-order cybernetics,
  and the politics of cybernetic institutions;
- media ecology and communication history: Innis, McLuhan, Ong, postal systems,
  standards, and logistics;
- Luhmann, autopoiesis, and the reproduction of communication;
- symbiosis, mutual excitation, ecological succession, and evolutionary major
  transitions—used carefully rather than as direct social analogies;
- neuroscience and excitation/inhibition as a source of formal motifs, not
  political legitimation;
- commons, polycentricity, federation, and institutional diversity;
- cliodynamics, secular cycles, state capacity, and elite competition;
- information theory, algorithmic complexity, and the energetic cost of
  communication;
- artificial intelligence as a communication substrate, model-producing actor,
  and potential new concentration mechanism;
- archives, forgetting, deletion, and the political economy of social memory;
- rumours, propaganda, secrecy, encryption, and adversarial communication;
- disability, language, translation, and unequal access to channels;
- urban form and transportation as communication topology;
- catastrophe, war, climate stress, and deliberate simplification.

## publication architecture

The thirteen thesis essays should be interleaved with cases and models. A
provisional sequence is:

1. **after dark mutualism:** why the name changed and what remains;
2. **antinomies are dynamical systems:** manifesto points 1–2;
3. **Marx against the *Philosophy of Misery*:** a paired close reading;
4. **the base has a topology:** point 3;
5. **case study — print, Reformation, and state formation**;
6. **the five-domain circuit:** point 4;
7. **substrates and feasible topology spaces:** point 5;
8. **model note — a minimal substrate-transition simulation**;
9. **how decentralisation manufactures hubs:** point 6;
10. **case study — the open web and platform capture**;
11. **productive conflict and its inhibitors:** point 7;
12. **Marx after the communication turn:** point 8;
13. **case study — Cybersyn and Soviet information bottlenecks**;
14. **case study — China as a coupled centralisation problem**;
15. **direction without destiny:** point 9;
16. **case study — collapse, simplification, and lost complexity**;
17. **determinism, reflexivity, and political action:** point 10;
18. **control without a controller:** point 11;
19. **model note — central, distributed, and polycentric control**;
20. **how cybernetic mutualism could be wrong:** point 12;
21. **a protocol for correction:** point 13;
22. **research report — what survived the first cycle**.

This order is a scaffold, not an obligation. A live case, newly available
archive, failed model, or productive digression may interrupt it.

## standard anatomy of a research post

Where appropriate, posts should include:

1. the claim in one paragraph;
2. definitions and scale;
3. the proposed mechanism;
4. the strongest available evidence;
5. a difficult case or rival explanation;
6. a model, diagram, dataset, or close reading;
7. what would change the conclusion;
8. consequences for the wider theory;
9. open questions and the next research action.

Shorter notes, source annotations, failed experiments, and polemical
interventions need not imitate this format.

## repository development

As material accumulates, add:

```text
research/
  glossary.md
  claims.md
  bibliography.md
  cases/
  evidence/
  models/
  decisions/
posts/
```

- `glossary.md` should distinguish technical, inherited, and project-specific
  meanings.
- `claims.md` should be the falsification and revision ledger.
- `bibliography.md` should separate read, partially read, and candidate works.
- `cases/` should hold comparable case templates rather than free-form notes.
- `evidence/` should contain provenance records and links, not copyrighted
  source dumps.
- `models/` should contain reproducible code and results.
- `decisions/` should record major conceptual changes and their reasons.

## First Research Cycle — Complete

**Status:** Complete as of 2026-09-01. The completion decision is recorded in
the [first-cycle synthesis and decision
record](research/decisions/first-cycle-synthesis.md).

The immediate cycle should produce five concrete artifacts:

1. [x] a project glossary for antinomy, topology, substrate, centralisation,
   decentralisation, control, complexity, and progress;
2. [x] a claim registry extracting the manifesto's empirical and conceptual
   claims;
3. [x] the essay "after dark mutualism," clarifying continuity and rupture;
4. [x] a paired case design for print/Reformation and a difficult comparison;
5. [x] a [minimal two-variable antinomy simulation](models/antinomy/README.md)
   with a visual parameter map, reproducible sweep, tests, and stated failure
   conditions.

The cycle's completion condition was not the checked artifact list alone. It
required the artifacts to reveal at least one necessary manifesto revision.
That condition was met: the synthesis found that section 2's assertion that
every order generates new asymmetries and counterforces exceeded CM-05's
available warrant. The [dated manifesto
revision](MANIFESTO.md#2-antinomies-do-not-end) now states a bounded,
falsifiable tendency. No claim confidence was raised by closing the cycle.

## Second Research Cycle — Active

**Status:** Proposed on 2026-09-01 and activated on 2026-09-03 after review and
acceptance of the first-cycle decision record and bounded manifesto revision.
Activation is a workflow decision, not an empirical result. The public essay is
complete. The robustness package is complete as a reviewable artifact, with
CM-04 narrowed at C1; preregistration and evidence deliverables remain pending.

### Purpose

Test whether the first cycle's formal antinomy distinctions survive less
restrictive assumptions and can be connected to observable institutional
relations, while beginning the evidence needed to adjudicate communication-
first explanations. The cycle must preserve uncoupled, common-shock,
state-first, and production-first rivals instead of treating coupling or
topological priority as given.

### Ordered Deliverables and Dependencies

1. [x] **Decision gate — first-cycle synthesis and bounded manifesto revision.**
   Review the [first-cycle decision
   record](research/decisions/first-cycle-synthesis.md) and its dated revision
   to [manifesto section 2](MANIFESTO.md#2-antinomies-do-not-end). Acceptance
   closes the first cycle and fixes the bounded CM-05 language used by every
   later item. Tests [CM-04](research/claims.md#cm-04--cybernetic-dynamics-can-formalise-antinomies)
   and [CM-05](research/claims.md#cm-05--social-orders-can-regenerate-antagonism) only
   at the level of warranted scope; it supplies no empirical support.
2. [x] **Public essay — [“Antinomies Are Dynamical
   Systems”](posts/antinomies-are-dynamical-systems.md).** Explain the
   conceptual distinction among persistent relation, equilibrium, oscillation,
   lock-in, and collapse; report the toy model's negative and limiting findings;
   and distinguish the project's reconstruction from claims about Proudhon.
   This follows item 1 but can proceed independently of items 3 and 5. It
   addresses [CM-01](research/claims.md#cm-01--antinomies-as-mutually-dependent-relations),
   [CM-04](research/claims.md#cm-04--cybernetic-dynamics-can-formalise-antinomies),
   and [CM-05](research/claims.md#cm-05--social-orders-can-regenerate-antagonism).
3. [x] **[Two-variable model robustness
   package](models/antinomy_robustness/README.md).** Replace symmetric coupling with
   separate directional effects, compare synchronous and asynchronous updates,
   and reproduce the sweep with at least one alternative bounded response
   function. Predefine which regime distinctions must survive, report boundary
   movement and failures, and retain an uncoupled ablation. This follows item 1
   and can run independently of the essay and print case. It directly tests
   [CM-04](research/claims.md#cm-04--cybernetic-dynamics-can-formalise-antinomies).
   The [item 3 decision](research/decisions/antinomy-structural-robustness.md)
   narrows CM-04 at C1: equilibrium, lock-in, and operational collapse survive
   all 18 tested variants; period-two oscillation survives only four.
4. [ ] **One preregistered empirical antinomy.** Name an institution and observation
   window; define observable autonomy and coordination proxies; specify directed
   cross-effects; and compare the coupled account with uncoupled and
   common-shock rivals. Design work may begin after item 1 in parallel with the
   essay, but preregistration must be frozen before evidence collection and its
   final model-comparison rules must incorporate item 3's robustness decision.
   It tests [CM-01](research/claims.md#cm-01--antinomies-as-mutually-dependent-relations)
   and [CM-04](research/claims.md#cm-04--cybernetic-dynamics-can-formalise-antinomies).
5. [ ] **First print/Reformation evidence pass.** Freeze the jurisdiction list,
   outcome codebook, phase boundaries, and missing-data rules; build the dated
   ordinance and censorship ledger; and complete Saxony and Venice process
   traces. Decide whether the catalogs warrant a reproducible network dataset
   or only bounded descriptive comparisons. This follows item 1 and can proceed
   independently of items 2 through 4. It tests
   [CM-07](research/claims.md#cm-07--communication-topology-constrains-social-organisation),
   [CM-08](research/claims.md#cm-08--communication-topology-can-be-causally-prior),
   and [CM-09](research/claims.md#cm-09--durable-phenomena-enter-a-five-domain-circuit).

### Completion and Decision Criteria

The second cycle is complete only when all five deliverables have reviewable
artifacts and a second-cycle decision record makes the following decisions:

- retain, narrow, or reject CM-04 according to whether its regime distinctions
  survive asymmetric coupling, asynchronous updates, and an alternative
  response function under prespecified criteria;
- retain CM-05 at C1 or revise it again, without treating the recurrence of one
  modeled regime as evidence for a universal historical tendency;
- accept the empirical antinomy preregistration only if autonomy,
  coordination, reciprocal effects, uncoupled dynamics, and common shocks have
  observable and discriminating specifications fixed before evidence;
- classify the print/Reformation evidence path as a reproducible network study
  or a bounded process-tracing comparison, and record what the first evidence
  pass warrants for CM-07 through CM-09; and
- state which findings change the wider programme, which claims remain at C1,
  and the next action most likely to discriminate among surviving rivals.

Publication of the essay or execution of a model sweep alone does not complete
the cycle. Confidence may rise only when linked evidence meets the registry's
declared standard; registration of this proposal raises none.
