+++
title = "antinomies are dynamical systems"
slug = "antinomies-are-dynamical-systems"
status = "draft"
excerpt = "what a two-variable model clarifies about equilibrium, oscillation, lock-in, collapse, and the limits of formalizing social opposition"
+++

# antinomies are dynamical systems

an antinomy is not two nouns placed on opposite sides of a page. it is a
relation that persists through time.

liberty and authority, autonomy and coordination, competition and cooperation
become antinomic only when each tendency helps produce, enable, or delimit the
other. if one side can disappear while the relation continues unchanged, the
pair may still describe a conflict or trade-off, but it does not yet describe
an antinomy. the claim concerns reciprocal production, not verbal symmetry.

this is why antinomies should be treated as dynamical systems. the phrase does
not mean that every social contradiction is secretly an equation, or that a
small simulation can decide a political question. it means that any serious
account must specify states, relations, changes, delays, constraints, and the
conditions under which a pattern persists or breaks. without these, “balance”
can hide several incompatible outcomes.

the first model in this project makes that distinction concrete. it shows that
the same two capacities and the same response rule can settle into a reproduced
equilibrium, alternate in a period-two oscillation, lock into an asymmetric
state, or remain together below a declared viability threshold. it also shows
where a stable balance can lose stability without either capacity disappearing.

these are conclusions, but they are conclusions about a formal domain. the
model does not establish that history obeys its equations. its value is more
modest and more useful: it turns one loose philosophical metaphor into several
different claims that later evidence can support, revise, or reject.

## what is inherited, and what is reconstructed

in the 1846 [*System of Economic Contradictions; or, The Philosophy of
Misery*](https://www.gutenberg.org/cache/epub/444/pg444-images.html),
Pierre-Joseph Proudhon distinguishes antinomy from logical contradiction. an
antinomy contains “two terms, necessary to each other, but always opposed.” his
examples concern economic categories whose useful and destructive effects
cannot be separated by simply choosing one side.

that formulation supplies the inheritance: mutual necessity, opposition, and a
relation whose movement cannot be understood by isolating either term. it does
not supply a modern dynamical model. Proudhon also describes higher ideas,
reconciliations, and serial economic periods in ways that do not map neatly
onto the vocabulary used here.

the later [*Philosophy of
Progress*](https://theanarchistlibrary.org/library/pierre-joseph-proudhon-the-philosophy-of-progress)
strengthens the anti-absolutist side of the inheritance. progress there means
movement, transformation, and susceptibility to revision rather than a fixed
final order. Proudhon opposes taking property, communism, centralization,
federalism, or another principle in an exclusive and absolute sense. but
feedback, state space, attractors, bifurcation, and parameter sweeps belong to a
later formal language.

the distinction matters because a retrospective vocabulary can clarify an old
problem while also rewriting it. calling Proudhon a cyberneticist before
cybernetics would replace interpretation with annexation. the narrower claim is
that a cybernetic reconstruction can test what follows when opposed capacities
are represented as mutually affecting variables.

Marx's [*The Poverty of
Philosophy*](https://www.marxists.org/archive/marx/works/1847/poverty-philosophy/)
remains a warning inside this reconstruction. Marx charges Proudhon with
turning historically produced relations into abstract categories and then
mistaking their conceptual sequence for historical movement. a simulation can
repeat the same error in newer notation. equations do not become historical
because their variable names are political. a formal antinomy earns its use
only when it creates distinctions, identifies failure conditions, and can
eventually be compared with observations and rival explanations.

## from opposed terms to a response rule

the [minimal two-variable
model](https://github.com/cyborg-nomade/cybernetic-mutualism/blob/main/models/antinomy/README.md)
represents one stipulated relation between local autonomy capacity, `A`, and
collective coordination capacity, `C`. both range from zero to one. autonomy
means the ability of local units to initiate, vary, or refuse action;
coordination means the ability of the same relation to align action, pool
information, or maintain common commitments.

these are not measurements of liberty and authority across a whole society.
they are dimensionless capacities in a toy system. one update is a response
interval, not a day, year, or historical epoch.

the model updates each capacity from four influences: shared support,
self-persistence, enablement by the other capacity, and inhibition by the other
capacity. a sigmoid response keeps the values bounded. the published sweep
holds persistence and enablement constant while varying shared support and
opposition.

the symmetry is deliberately severe. both capacities receive the same support,
persist at the same rate, affect one another with the same strength, and update
at the same moment. this makes the first question legible: can a minimal
coupled system distinguish several outcomes before asymmetry, institutions,
actors, or history are added?

the answer is yes. across 2,337 parameter cells and seven small initial
perturbations per cell, the modal map contains 621 equilibria, 206
oscillations, 544 lock-ins, 951 low-viability states classified operationally
as collapse, and 15 unresolved cells. the counts are not estimates of how often
these outcomes occur in the world. they describe the geometry of this chosen
parameter grid.

## balance is not one outcome

equilibrium is the easiest word to misunderstand. in the model it means that
successive changes become negligible while both capacities remain above the
viability threshold and neither dominates the other by more than the declared
gap. nothing in that definition says the equilibrium is just, efficient, or
desirable. it is a fixed point reproduced by the update rule.

oscillation means that the system repeats after two updates but not after one.
each capacity responds to the previous state, and sufficiently strong
cross-inhibition makes correction overshoot. the result is not indecision
around an underlying harmonious center. the alternation is itself the durable
pattern.

lock-in is a fixed but asymmetric outcome. one capacity remains high while the
other remains low. because the equations are symmetric, the model contains
mirror lock-ins: a small initial difference can select which capacity becomes
dominant even when the parameters do not privilege either one. identical rules
therefore need not produce an equal result.

collapse is the most dangerous label. here it means only that both long-run
values fall below 0.1. this is a declared joint viability condition, not an
institution vanishing, a society disintegrating, or a mathematical
singularity. changing the threshold can change the label. the representative
example survives checks at nearby thresholds, but the concept remains
operational and contestable.

bifurcation is not a fifth destination. it names a change in the system's
qualitative behavior as parameters change. the map marks 115 cells adjacent to
a change in the local stability of the symmetric fixed point. those cells are
candidates for a more exact continuation analysis. they show where balance can
cease to hold, not what every trajectory must become.

the 73 cells in which initial perturbations select different classifications
are equally important. one parameter setting can contain more than one
attractor, or can converge too slowly for the present horizon to settle the
question. a regime map that erased those disagreements would look cleaner and
say less.

## what the sweep warrants

the first conclusion is that *balance* should be retired as a sufficient
description. equilibrium, oscillation, and asymmetric lock-in are not poetic
variants. they have different trajectories, stability properties, and
political implications. collapse is different again because it depends on an
explicit viability judgment. bifurcation belongs to parameter change rather
than to the list of long-run states.

the second conclusion is that coupling performs formal work. in a sampled
ablation, reciprocal enablement and opposition cancel so that each variable
responds only to shared support and its own prior state. that uncoupled version
produces equilibrium or low viability at the tested support levels, but not
lock-in or coupled oscillation. cross-effects are therefore necessary for those
outcomes in this sampled model.

this result does not prove that a real federation, firm, commune, or state
contains the proposed cross-effects. it identifies what an empirical claim
would have to show. autonomy and coordination must affect one another in
directed, observable ways; a shared shock that moves both cannot simply be
renamed coupling.

the third conclusion is negative: adaptation was not needed. the manifesto
listed adaptation among the languages through which antinomies might be
formalized, but persistence, saturation, response lag, and feedback sign are
already enough to generate the four operational regimes. this narrows the
formal claim. adaptation may matter in later models, but it cannot be credited
for distinctions produced without it.

the fourth conclusion is another limit. reciprocal enablement and opposition
enter the present equations only through their difference. the sweep cannot
identify them separately. a high-enablement, high-opposition relation can be
formally identical to a weaker version of both if the net effect is the same.
the model therefore demonstrates consequences of net coupling, not an
empirical decomposition of cooperation and conflict.

these conclusions provisionally retain the project's claim that cybernetic
dynamics can formalize antinomies. they do not raise its confidence beyond
conjecture. the model distinguishes outcomes that the prose did not, but its
symmetry, synchronous timing, chosen response function, and absence of measured
cases remain open failure points.

## an antinomy is an empirical burden

the model makes the word *antinomy* harder to use, which is an improvement.

it is not enough to name two values that sound opposed. a candidate antinomy
must specify the institution or relation in which the capacities arise, the
observation window, the directed effects, the delays, and the conditions under
which either side enables or constrains the other. it must distinguish mutual
production from a temporary trade-off, one-way dependence, and two independent
responses to a common cause.

consider autonomy and coordination in a federation. shared standards might
increase local capacity by making information and resources portable.
successful local experiments might increase the federation's coordinating
capacity by supplying variety and knowledge. the same standards might also
restrict local refusal, while local vetoes might inhibit common action. whether
these effects exist, in which direction, and with what delay cannot be settled
by the elegance of the example.

nor does persistence confer legitimacy. an exploitative lock-in may be stable.
an oscillation may distribute costs asymmetrically. an equilibrium may keep the
modeled variables inside their ranges by exporting damage to people and
conditions outside the system boundary. the choice of variables and viability
thresholds is already political. dynamics can clarify consequences; they do
not choose the values by which those consequences should be judged.

## what changes next

the model has earned a harder test, not a larger mythology.

the next robustness pass will break its symmetry. autonomy and coordination
will receive separate persistence, enablement, inhibition, and timing. the
synchronous update will be compared with asynchronous responses, and the
sigmoid with another bounded response function. the regime distinctions must
survive prespecified perturbations rather than being rescued after inspection.
if they disappear under modest changes, the formal claim will be narrowed
again.

the next empirical step will then choose one institution and preregister
observable proxies for autonomy, coordination, reciprocal effects, uncoupled
dynamics, and common shocks. that comparison is decisive. the toy model begins
by imposing an antinomic relation; evidence must determine whether any real
candidate deserves the name.

to say that antinomies are dynamical systems is therefore not to announce a law
of history. it is to replace a suggestive opposition with a research program:
name the states, specify the relation, follow the changes, test the rivals, and
record the conditions under which the pattern does not survive.
