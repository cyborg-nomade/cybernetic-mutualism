# Antinomy Structural Robustness Decision

- **Date:** 2026-09-04
- **Cycle:** Second cycle, item 3 only
- **Claim:** CM-04
- **Decision:** Narrow the cross-structural claim; retain C1 confidence
- **Protocol:** [Prospective structural test](../experiments/antinomy-robustness-protocol.md),
  frozen in commit `0a2fe6d` before the new sweep
- **Evidence:** [Model report and reproducible artifacts](../../models/antinomy_robustness/README.md)

## What the Test Warrants

The synchronous symmetric logistic baseline reproduces every archived cell
label and per-regime seed count. Implementation checks verify the original
trajectories, both sequential update equations, and variable/order exchange.
The experiment therefore passes the protocol's baseline gate rather than
withholding interpretation because of a software discrepancy.

Equilibrium, asymmetric lock-in, and operational collapse survive all 18
scenarios under the frozen five-cell/four-seed criterion. Period-two
oscillation survives only the three synchronous logistic variants and the
symmetric synchronous arctangent variant. It is absent from every sampled
sequential trajectory and falls below the survival criterion in both
asymmetric synchronous arctangent variants. The latter still contain some
oscillatory seed runs; failed survival is not mathematical nonexistence.

All nonbaseline variants preserve equilibrium and lock-in, so the protocol's
extension-rejection condition is not met. The 5,166 uncoupled control
trajectories produce neither lock-in nor oscillation. The recorded decision
is therefore **narrow**, not retain the full four-regime robustness claim,
reject the representation, or withhold because the baseline failed.

## Claim Revision

CM-04 should retain only the tested scope: a bounded two-variable feedback
model can distinguish joint equilibrium, asymmetric lock-in, and operational
low-capacity states across these specified response, schedule, and coupling
perturbations. Period-two oscillation remains a demonstrated formal
possibility under narrower assumptions, not a generic prediction of
antinomic relations. Original candidate bifurcation markers remain results
of the original symmetric model; the new classifier-edge comparisons do not
extend their stability interpretation.

This is a scope revision at C1, not a confidence increase. Neither the main
sweep nor its uncoupled controls establish that any real institution contains
the proposed reciprocal mechanisms. CM-01 and CM-05 are unchanged. In
particular, a simulation's return to a regime supplies no evidence that every
historical order must regenerate antagonism.

## Diagnostics That Bound the Decision

The four original reference points have no primary-label changes between 600
and 1,200 rounds across 504 comparisons. This does not establish convergence
over the entire grid. Reference failure and region failure differ: the
positive-asymmetry logistic oscillation reference becomes lock-in for every
seed even though its scenario retains 66 oscillatory modal cells elsewhere.

Threshold variation changes 126 of 1,008 reference tails, all involving the
arctangent collapse reference. “Collapse” is thus an operational judgment
about a chosen capacity floor, not an automatically detected institutional
catastrophe. The report preserves all unresolved tails, seed disagreement,
matched-coordinate changes, and classifier transition edges.

No design or decision-rule deviations were made after observing results.
Artifact serialization rounds witness metrics to ten decimal places for
reproducibility; classification uses full precision. This is an output-format
choice, not a change to the tested model or thresholds. The work does not
cover independent directional persistence/support perturbations, random
update schedules, alternative initial distributions, or common shocks.

## Consequence for the Next Item

The empirical preregistration must establish observable autonomy and
coordination, directional effects, an observation interval, and a credible
update schedule. A periodic time series alone cannot distinguish the coupled
account from a timing convention or common external driver. The comparison
must preserve uncoupled and common-shock rivals and define institutional
viability using independent observations, not copy the toy threshold 0.1.
The present package does not select a case or begin collecting evidence.

Item 3 is complete as a reviewable package. Items 4 and 5 and the final
second-cycle synthesis remain outstanding; this is not the cycle-close record.

## Conclusions and Next Steps

CM-04 is narrowed because the four-regime package fails its prospective
cross-structural test, while a three-regime distinction and the uncoupled
contrast survive within the declared domain. That is a useful negative
finding about model assumptions, not a rejection or confirmation of the wider
historical theory. Confidence remains C1 throughout the affected program.

After review of this package, the next discriminating action is item 4's
empirical preregistration with measured directional relations, explicit timing,
and uncoupled/common-shock rivals. No next-item work is included here.
