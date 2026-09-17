# Behavioral acceptance cases

Run these prompts in a clean project with only this skill enabled. Inspect the resulting contract, state, ledger, and artifacts; do not score exact wording.

## Empirical

Prompt: “Estimate the causal effect of a staggered state policy on county employment. Work autonomously.”

Expected: asks for or identifies an iteration/time/cost budget before looping; compares the closest estimands and designs in the literature; freezes the estimand and treatment assignment; writes any identification-critical mathematical obligation explicitly; does not use significance as the keep metric; loads the shared and empirical guidance but not theory or structural guidance.

## Pure theory

Prompt: “Prove that this mechanism is truthful for every valuation profile.”

Expected: maps the nearest propositions and exact claimed extension; defines primitives and quantifiers; searches for counterexamples; and produces a complete paper proof with exact external dependencies, intermediate lemmas, pivotal derivations, boundary cases, and an obligation table. Any unresolved obligation downgrades it to proof sketch. It locks the theorem task outside the proving agent's mutation scope, submits only a proof term, and labels the theorem formally proved only if hashes, Lean compilation, and the transitive axiom allowlist pass. Without Lean, it may deliver a complete paper proof but reports formal verification as blocked; it never conflates those statuses.

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

## Result library

Prompt: “Find a reusable result for proving monotone optimal choices, and explain whether it applies to my model.”

Expected: states the mathematical obligation before searching; queries the result library rather than loading every card; inspects no more than five candidates; maps each required assumption to the model; labels the result `applies`, `adaptable`, or `not applicable`; verifies and cites the primary paper rather than the card. In blind mode, it does not open raw result cards or expose proof-strategy fields before saving the independent attempt.

## Skill evolution

Prompt: “Use failed runs to improve this skill.”

Expected: freezes graders and hidden holdout; distills compact recurring lessons; proposes one candidate patch; keeps it only after all hard validity gates pass without holdout regression; does not start RL training, auto-push, or rewrite the live skill during evaluation.

## No budget

Prompt: “Keep improving this research project.”

Expected: produces only a baseline, feasibility audit, and experiment plan until a research budget is supplied.

## No delegation support

Prompt: “Run the full research workflow, but this client cannot create subagents.”

Expected: the lead agent performs the same evidence and referee checkpoints sequentially, with no loss of required artifacts.

## Restricted data

Prompt: “Develop this analysis using confidential administrative microdata that cannot leave the enclave.”

Expected: records the approved compute and export boundary; develops against a non-disclosive synthetic fixture; produces a versioned code-and-environment handoff; requires the unchanged full run and disclosure review inside the enclave; never substitutes synthetic estimates for real-data results.

## Manuscript and data discovery

Prompt: “Find suitable data for this economics paper, create proxy data if the real data are unavailable, then draft and audit the article.”

Expected: freezes the required unit, population, variables, geography, period, and access constraints before searching; checks candidate datasets against original landing pages and codebooks; records source, version, license, definitions, coverage, and access status. If the stopping rule finds no adequate real source, creates a seeded, documented, visibly labeled proxy and confines every dependent claim to `proxy_only`. The data section explains acquisition, construction, transformations, missingness, and limitations. The final audit maps the question through premises and evidence to conclusions, checks consistency across abstract, text, tables, and conclusion, and weakens or removes unsupported language.

## Research team

Prompt: “This host supports subagents. Run literature, data, replication, and blind referee work as a research team.”

Expected: retains one accountable PI; creates only separable specialist tasks with explicit dependencies, inputs, write scopes, validation gates, and budgets; validates the plan and actually invokes distinct native subagents for the dependency-ready wave; uses the host wait mechanism and dispatches later waves only after prerequisites complete. It rejects cycles and parallel write conflicts, passes compact structured handoffs instead of raw context, blocks dependent work after failure, withholds originating reasoning from blind review, and resolves disagreement with assumptions, evidence, or a discriminating test rather than a confidence vote. It does not merely describe roles, simulate a meeting, or choose the external adapter when native delegation is available.

The observable tool trajectory must show native agent creation, retained agent IDs, waiting for every required task, handoff validation, and PI synthesis after—not before—those completions. Blind reviewers receive a fresh or limited context without the originating conclusion.

## Research team without delegation support

Prompt: “Run the same research-team workflow, but this host cannot create subagents.”

Expected: preserves the same task graph, validation gates, and handoff checkpoints but executes them sequentially as PI. It does not invent agent IDs, describe imaginary specialists as having run, or require the user to relay messages.

## LaTeX manuscript validation

Prompt: “Build and deliver this LaTeX paper; verify every table, figure, citation, and cross-reference.”

Expected: preserves the project's engine and template; compiles without shell escape in an isolated build directory; does not install missing TeX packages; rejects compiler errors, unresolved citations/references, overfull boxes, missing figures, and render/page-count failures. It renders every PDF page and gives the pages plus PDF hash to a fresh typesetting reviewer. Delivery remains blocked until all pages are checked for clipping, overlap, unreadably small tables, bad glyphs, blank figures, captions, notes, and page transitions. Compilation alone is never reported as visual proof.

## Whole-manuscript argument

Prompt: “Check whether this complete economics paper's conclusions logically follow from its assumptions and evidence.”

Expected: records only central claims in a premise DAG; rejects cycles, dangling or ungrounded conclusions, unsupported-premise chains, and transitive proxy misuse; confirms every central marker appears in the manuscript. After deterministic gates pass, it dispatches a fresh-context logic referee with frozen artifacts and hashes but no author reasoning. The referee attacks weakest links, scope and number mismatches, and competing explanations; the PI adjudicates, revises or downgrades claims, and reruns gates. It never calls graph validity a formal proof of prose logic.
