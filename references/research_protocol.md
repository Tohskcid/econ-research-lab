# Shared research protocol

Use this reference when synthesizing literature, recording experiments, delegating work, or running the final adversarial review.

## Literature checkpoint

Set the review scope from the question, mechanism, estimand or theorem, method, population/model class, and search cutoff. Search primary papers and credible working papers using concept synonyms, backward references, and forward citations. Record queries, sources searched, dates, access status, and inclusion reasons.

Synthesize by claim rather than paper order. For each close work, capture its question, result, assumptions, design or proof method, scope, and relation to the proposed contribution. For empirical work compare estimands, assignment mechanisms, data, and external validity; for theory compare primitives, solution concepts, theorem statements, and which assumptions strengthen or relax prior results. Surface disagreements and negative results. Do not claim novelty until the nearest alternatives and their differences have been checked.

Scale depth to the deliverable: a feasibility audit may use a compact map; a literature review or novelty claim requires reproducible coverage and explicit search limitations.

For a sustained review, contradiction search, or novelty audit, use the claim/evidence records in [research_artifacts.md](research_artifacts.md). Reuse an existing local index when available. Metadata retrieval, full-text search, and contextual reranking may assist discovery, but every delivered claim still needs a verified primary-source locator. When evaluating hypothesis generation, prefer a historical literature cutoff and later-paper validation over same-run self-grading.

## Mathematical reasoning checkpoint

Create only the obligations needed to support the claim. Depending on the mode these may include well-defined domains, existence, uniqueness, identification, rank or support conditions, continuity/convexity, invariance, estimator properties, equilibrium mappings, comparative statics, or bounds.

For each obligation state the proposition, assumptions, argument or checker, status, and unresolved gap. Separate maintained assumptions from derived implications. Test boundary cases and seek counterexamples before strengthening a claim. Symbolic algebra, simulation, and numerical examples may check derivations or find failures but do not replace a proof. Use the proof-status rules in `theory.md` whenever presenting a result as a theorem.

When a full proof is requested, apply the complete paper-proof gate in `theory.md`. Store the full derivation once as an artifact; downstream agents receive only obligation statuses, exact dependency locators, checker status, uncertainty, and the artifact path unless they are assigned to audit the proof itself.

## Evidence

For each material claim record: source, exact supported claim, research design or proof status, population/model scope, limitation, and verification date. Prefer primary sources. Distinguish published evidence, working papers, official data, documentation, and conjecture. Citation count and journal tier are metadata, not credibility or inclusion rules.

When a manuscript or evidence package is in scope, link claims to evidence, findings to runs, and runs to the frozen harness. Validate these references before the referee checkpoint; a link proves provenance, not substantive support.

Never claim novelty from a narrow search. Preserve queries, databases, dates, and inclusion reasons. Mark unread or inaccessible full text explicitly.

## Compact artifacts

Keep details in project files and pass only:

- decision or finding;
- evidence/artifact location;
- uncertainty or failed check;
- next decision.

Do not impose an arbitrary token cap that removes identification assumptions, proof obligations, or failure information.

## Iteration ledger

Each row in `experiments.tsv` describes one attributable change. Status meanings:

- `keep`: improves the fixed criteria and passes every validity gate;
- `discard`: valid run but no net improvement;
- `inconclusive`: evidence cannot distinguish the hypothesis;
- `blocked`: missing authority, input, or required capability;
- `crash`: execution failed before valid evaluation.

Never edit prior rows to improve the story. Link results rather than pasting logs.

## Referee checkpoint

Before delivery, attack the strongest claim:

1. Is the estimand, theorem, or target object well-defined?
2. Which assumption carries the conclusion, and is it defended?
3. What observationally equivalent mechanism or counterexample remains?
4. Does the validation harness test the claim rather than a convenient proxy?
5. Can another researcher reproduce the result from recorded inputs?

Classify conclusions as supported, provisional, inconclusive, or contradicted. A surprising result triggers an audit, not automatic rejection or a forced pivot.
