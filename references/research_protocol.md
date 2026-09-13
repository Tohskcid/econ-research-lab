# Shared research protocol

Use this reference when synthesizing literature, recording experiments, delegating work, or running the final adversarial review.

## Evidence

For each material claim record: source, exact supported claim, research design or proof status, population/model scope, limitation, and verification date. Prefer primary sources. Distinguish published evidence, working papers, official data, documentation, and conjecture. Citation count and journal tier are metadata, not credibility or inclusion rules.

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
