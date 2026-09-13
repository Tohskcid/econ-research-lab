# Structural and computational mode

Use for structural estimation, calibration, simulation, numerical equilibrium, counterfactuals, or computational macro/IO/finance/trade.

## Contract additions

Freeze the economic environment, parameterization, identified and calibrated parameters, moments or likelihood, holdout targets, solver and tolerances, random seeds, counterfactual, hardware/time budget, and primary fit and welfare metrics.

## Baseline and validity gates

1. Reproduce a transparent benchmark and limiting cases.
2. Verify units, constraints, equilibrium conditions, and accounting identities.
3. Report convergence, sensitivity to starting values, numerical error, runtime, and seed stability.
4. Separate in-sample targeted moments from holdout validation.
5. Diagnose identification or observational equivalence before interpreting parameters.
6. For counterfactuals, state which policy-invariant primitives and equilibrium responses carry the result.

Fit improvement cannot compensate for non-convergence, failed identities, weaker identification, or an altered validation sample.

## Iteration

Run one attributable change per row: a moment, parameter restriction, numerical method, or model mechanism. Evaluate it with the frozen harness and record fit, holdout performance, convergence, runtime, and complexity. Keep equal-performing simplifications; discard cosmetic complexity and changes that only retune the evaluation target.

The harness may be revised only when a defect is documented. Record the revision as a new baseline so results across harness versions are not compared as if identical.
