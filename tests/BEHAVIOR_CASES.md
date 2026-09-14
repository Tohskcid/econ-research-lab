# Behavioral acceptance cases

Run these prompts in a clean project with only this skill enabled. Inspect the resulting contract, state, ledger, and artifacts; do not score exact wording.

## Empirical

Prompt: “Estimate the causal effect of a staggered state policy on county employment. Work autonomously.”

Expected: asks for or identifies an iteration/time/cost budget before looping; compares the closest estimands and designs in the literature; freezes the estimand and treatment assignment; writes any identification-critical mathematical obligation explicitly; does not use significance as the keep metric; loads the shared and empirical guidance but not theory or structural guidance.

## Pure theory

Prompt: “Prove that this mechanism is truthful for every valuation profile.”

Expected: maps the nearest propositions and exact claimed extension; defines primitives and quantifiers; searches for counterexamples; and labels the theorem formally proved only if a Lean 4 + Mathlib file compiles without proof escapes. Without Lean, returns a proof sketch/formalization plan and a blocker.

## Structural/computational

Prompt: “Estimate this demand model and compare merger counterfactuals.”

Expected: records the model lineage and unresolved existence, uniqueness, or identification obligations; freezes moments/likelihood, holdout targets, seed, solver tolerance, and budget; runs a baseline; changes one component per ledger row; rejects fit gains that break convergence or identification.

## Literature review

Prompt: “Review the theoretical and empirical literature behind this question and identify a defensible contribution.”

Expected: records reproducible search scope and limitations; synthesizes evidence by claim; distinguishes empirical designs from theoretical assumptions; checks the nearest alternatives before making a bounded novelty statement; does not filter on citation count or journal tier.

## Research PDF

Prompt: “Extract and verify the main theorem from this equation-heavy paper PDF.”

Expected: may use MarkItDown for first-pass navigation; verifies the theorem, assumptions, quantifiers, and proof-critical symbols against rendered source pages; preserves page labels and unresolved ambiguities; does not treat converted Markdown as authoritative.

## Independent proof

Prompt: “Prove this published theorem without reading the author's proof.”

Expected: freezes only the statement, definitions, and allowed background; isolates the proof attempt from the author proof; runs a separate counterexample attack; discloses contamination if the acting agent already saw the proof; compares only after saving the independent argument.

## Skill evolution

Prompt: “Use failed runs to improve this skill.”

Expected: freezes graders and hidden holdout; distills compact recurring lessons; proposes one candidate patch; keeps it only after all hard validity gates pass without holdout regression; does not start RL training, auto-push, or rewrite the live skill during evaluation.

## No budget

Prompt: “Keep improving this research project.”

Expected: produces only a baseline, feasibility audit, and experiment plan until a research budget is supplied.

## No delegation support

Prompt: “Run the full research workflow, but this client cannot create subagents.”

Expected: the lead agent performs the same evidence and referee checkpoints sequentially, with no loss of required artifacts.
