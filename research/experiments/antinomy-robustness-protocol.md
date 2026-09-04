# Antinomy Structural Robustness Protocol

- **Registered:** 2026-09-04, before executing the new structural sweep
- **Claim:** CM-04; no empirical evidence for CM-01 or CM-05 is generated
- **Baseline:** First-cycle model at Git commit `bf00fc5`
- **Scope:** Second-cycle item 3 only; no institutional evidence collection

## Question and Design

Do the baseline regime distinctions survive changes to reciprocal coupling,
update schedule, and bounded response shape? This is a structural sensitivity
experiment, not parameter estimation or a claim that these perturbations exhaust
plausible social models. The baseline already exists; this protocol is prospective
only for the new structural comparisons.

Use the original support grid (-6 to 4 by 0.25), inhibition grid (0 to 14 by
0.25), seven seeds (7, 19, 41, 73, 101, 151, 211), 600 response rounds, and final
100-state classifier. Persistence and reciprocal enablement remain 2; shocks
remain zero. Preserve the original generated files unchanged.

Cross all three factors (18 scenarios):

| Factor | Prespecified levels |
| --- | --- |
| Directional asymmetry, d | 0, -0.1, +0.1 |
| Bounded response | Original logistic sigmoid; 0.5 + atan(pi z / 4) / pi |
| Update schedule | Synchronous; autonomy then coordination; coordination then autonomy |

For autonomy, enablement and inhibition are multiplied by (1+d); for
coordination they are multiplied by (1-d). Directional parameters are separate
in code; this intervention scales both signed components together and therefore
still identifies only the net cross-effect. It does not independently identify
enablement and inhibition. Support and persistence are not perturbed in this
package. The alternative response has the same midpoint (0.5) and derivative
(0.25) at zero as the logistic, but different tails.

Each sequential round updates both capacities exactly once. The second update
uses the newly updated first capacity and its own old capacity. Classify at
round boundaries, not half-steps: otherwise alternating which coordinate is
updated could itself manufacture an apparent period-two signal. Both fixed
orders are included; randomized schedules and unequal response rates are out
of scope. These are alternative discrete maps, not time-step refinements of a
continuous-time system.

## Decision Rules

Retain the baseline classifier and its tie-break order. A regime survives in a
scenario if at least five cells have that modal label with at least four of
seven seeds agreeing. This is a declared finite-grid screening threshold, not
a probability, significance level, or mathematical proof of attractor existence.
Report counts for equilibrium, lock-in, period-two oscillation, operational
collapse, and unresolved behavior without reassigning inconvenient outcomes.

- **Retain cross-structural robustness** only if all four named regimes survive
  in every scenario and the uncoupled controls have neither lock-in nor
  oscillation.
- **Narrow CM-04** if the baseline is reproduced but one or more structural
  variants lose a regime, or controls reproduce a purported coupling-specific
  regime. State which assumptions the missing distinction depends on.
- **Withhold a decision** if baseline reproduction or implementation checks fail.
  Diagnose software errors before interpreting structural results.
- **Reject the present robustness extension** if no non-baseline scenario
  retains both equilibrium and lock-in. This does not erase the original
  baseline demonstration or reject the wider research program.

The last rule takes precedence over narrowing; baseline failure takes precedence
over every scientific decision. No confidence increase follows from any outcome.

## Diagnostics and Controls

For every cell retain all seven seed labels, modal label, agreement count, and
whether seeds disagree. Compare each scenario with the identical-grid baseline:
matched modal agreement, per-regime intersection-over-union, and changed
horizontal/vertical transition-edge locations. Export edge coordinates so
boundary changes can be inspected. These are classifier boundaries, not a
bifurcation continuation or stability proof for the modified systems.

Repeat the four original representative points at 600 and 1,200 rounds for
every scenario and seed, recording both labels and numerical metrics. Report
reference failures separately from grid-region survival: a region can move
without disappearing. These horizon checks do not establish global convergence.
Also reclassify these witnesses with collapse thresholds 0.075/0.1/0.125 and
lock-in gaps 0.20/0.25/0.30; do not tune the primary classifier afterwards.

At every support level and for every scenario/seed, cancel both directional
cross-effects by setting each inhibition equal to its enablement. Inhibition
grid coordinates then become redundant, so run each unique support once.
Retain these controls in a separate file. A common-shock rival belongs to the
later empirical comparison and is not claimed to have been tested here.

## Software Verification and Reproduction

| Layer | Required checks |
| --- | --- |
| Model | Exact synchronous-logistic baseline trajectory equivalence; hand-calculated sequential rounds; exchange of variables and update orders; bounds and invalid-input rejection |
| Response | Midpoint, midpoint slope, monotonicity, boundedness, and a shape distinct from the logistic |
| Classification | Reuse baseline metric definitions and thresholds; preserve unresolved cases and stable tie-breaking |
| Experiment | Full factorial coverage; deterministic seeds; complete controls; synthetic tests for survival and decision branches; transition-edge coordinates |
| Artifacts | Repeat small generation byte for byte; reproduce full committed outputs independently; verify baseline cell labels against the original CSV |

Run the repository quality gate, including strict typing, readability lint,
tests, and at least 80% total branch-aware coverage. Scientific failure is a
valid output, not a failing software test. Freeze this protocol in its own
commit before running the new sweep; record deviations explicitly if required.

## Conclusions and Next Steps

This protocol warrants no new claim about antinomies. It defines what will
count as survival, failure, or an uninterpretable software result before the
structural comparison. CM-04 remains C1, provisionally retained only within
its first-cycle toy domain. Implement and verify the experiment next, execute
the frozen design, and write a decision that bounds the empirical
preregistration without beginning that next cycle item.
