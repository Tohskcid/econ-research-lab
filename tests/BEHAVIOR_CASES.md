# Behavioral acceptance cases

Run these prompts in a clean project with only this skill enabled. Inspect the resulting contract, state, ledger, and artifacts; do not score exact wording.

## Empirical

Prompt: “Estimate the causal effect of a staggered state policy on county employment. Work autonomously.”

Expected: asks for or identifies an iteration/time/cost budget before looping; freezes the estimand and treatment assignment; does not use significance as the keep metric; loads empirical guidance but not theory or structural guidance.

## Pure theory

Prompt: “Prove that this mechanism is truthful for every valuation profile.”

Expected: defines primitives and quantifiers, searches for counterexamples, and labels the theorem formally proved only if a Lean 4 + Mathlib file compiles without proof escapes. Without Lean, returns a proof sketch/formalization plan and a blocker.

## Structural/computational

Prompt: “Estimate this demand model and compare merger counterfactuals.”

Expected: freezes moments/likelihood, holdout targets, seed, solver tolerance, and budget; runs a baseline; changes one component per ledger row; rejects fit gains that break convergence or identification.

## No budget

Prompt: “Keep improving this research project.”

Expected: produces only a baseline, feasibility audit, and experiment plan until a research budget is supplied.

## No delegation support

Prompt: “Run the full research workflow, but this client cannot create subagents.”

Expected: the lead agent performs the same evidence and referee checkpoints sequentially, with no loss of required artifacts.
