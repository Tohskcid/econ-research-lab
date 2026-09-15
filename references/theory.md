# Pure theory mode

Use for microeconomic theory, games, information, contracts, matching, mechanism design, or other theorem-led research.

## Contract additions

Freeze primitives, domains, timing, information, strategy spaces, equilibrium or solution concept, welfare criterion, target theorem, and allowed assumptions. Separate definitions, maintained assumptions, conjectures, and established results.

## Workflow

1. Map the theorem's lineage: nearest propositions, definitions, proof strategies, counterexamples, and the exact assumption or conclusion changed.
2. Reproduce the closest known benchmark and limiting cases before claiming an extension.
3. State the conjecture with complete quantifiers and hypotheses.
4. Search Mathlib documentation and the local environment for existing definitions, lemmas, and naming conventions before recreating them. If already configured, LeanSearch/Loogle or LeanDojo-v2 may assist premise search; do not install or contact a service without authority.
5. Search analytically and computationally for boundary cases or counterexamples.
6. Write a paper proof sketch and a dependency manifest: theorem statement hash, assumptions, imports, critical lemmas, Mathlib/Lean version, and unresolved obligations.
7. Formalize the definitions and theorem in Lean 4 + Mathlib.
8. Run `python3 scripts/check_lean_proof.py path/to/Theorem.lean` and preserve the checked source and command output.
9. Derive comparative statics, welfare implications, and testable predictions only within the proved domain.
10. Run the shared referee checkpoint against assumptions, equilibrium selection, and necessity of conditions.

## Proof status

Use exactly these labels:

- `conjecture`: no complete proof;
- `proof sketch`: informal argument with unresolved obligations;
- `formally proved`: the saved Lean file compiles with no `sorry`, `admit`, or equivalent escape;
- `disproved`: a valid counterexample violates the claim under its stated assumptions.

Lean 4 + Mathlib is the sole formal proof authority for this skill. The checker rejects local `sorry`, `admit`, `sorryAx`, and `axiom` escapes before invoking `lake env lean` (or `lean` when no Lake project exists). Computer algebra or numerical search may simplify expressions and find counterexamples, but cannot upgrade proof status. If Lean is absent, do not install it without authorization and do not label a theorem formally proved.

## Independent reconstruction

When asked to prove a published claim without consulting its proof, freeze the statement, definitions, and allowed background results before proof search. Keep the author proof inaccessible to the proof attempt; use a fresh context or independent agent when available. Run a separate counterexample attack. Compare with the author proof only after saving the independent argument. If the acting agent has already seen the proof, disclose contamination and do not call its reconstruction blind.

## Iteration

Change one definition, assumption, lemma, or proof strategy at a time. Keep a change only if the target theorem remains economically meaningful and the checked result becomes stronger, simpler, or more general. Do not weaken assumptions silently merely to make Lean succeed; record any scope change as a new hypothesis.
