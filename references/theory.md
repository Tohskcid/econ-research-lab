# Pure theory mode

Use for microeconomic theory, games, information, contracts, matching, mechanism design, or other theorem-led research.

## Contract additions

Freeze primitives, domains, timing, information, strategy spaces, equilibrium or solution concept, welfare criterion, target theorem, and allowed assumptions. Separate definitions, maintained assumptions, conjectures, and established results.

## Workflow

1. Solve the smallest benchmark and reproduce known limiting cases.
2. State the conjecture with complete quantifiers and hypotheses.
3. Search analytically and computationally for boundary cases or counterexamples.
4. Write a paper proof sketch that identifies the critical lemmas.
5. Formalize the definitions and theorem in Lean 4 + Mathlib.
6. Run `python3 scripts/check_lean_proof.py path/to/Theorem.lean` and preserve the checked source and command output.
7. Derive comparative statics, welfare implications, and testable predictions only within the proved domain.
8. Run the shared referee checkpoint against assumptions, equilibrium selection, and necessity of conditions.

## Proof status

Use exactly these labels:

- `conjecture`: no complete proof;
- `proof sketch`: informal argument with unresolved obligations;
- `formally proved`: the saved Lean file compiles with no `sorry`, `admit`, or equivalent escape;
- `disproved`: a valid counterexample violates the claim under its stated assumptions.

Lean 4 + Mathlib is the sole formal proof authority for this skill. The checker rejects local `sorry`, `admit`, `sorryAx`, and `axiom` escapes before invoking `lake env lean` (or `lean` when no Lake project exists). Computer algebra or numerical search may simplify expressions and find counterexamples, but cannot upgrade proof status. If Lean is absent, do not install it without authorization and do not label a theorem formally proved.

## Iteration

Change one definition, assumption, lemma, or proof strategy at a time. Keep a change only if the target theorem remains economically meaningful and the checked result becomes stronger, simpler, or more general. Do not weaken assumptions silently merely to make Lean succeed; record any scope change as a new hypothesis.
