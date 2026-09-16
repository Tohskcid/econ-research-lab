# Economics manuscript workflow

Read this reference when drafting, revising, translating, or auditing an economics paper, thesis chapter, working paper, referee response, or research article.

## Contract and outline

Confirm the audience, format, language, length, target contribution, deliverable, and permitted files. Inspect the existing manuscript, bibliography, tables, figures, model, code, and project conventions before creating a new structure. Preserve the user's chosen LaTeX, Quarto, Markdown, or word-processing workflow.

Build an evidence-backed outline from the research contract. State one primary question and contribution, then map each section to the claims, evidence or findings, assumptions, tables/figures, and unresolved gaps it needs. Do not manufacture results, references, mechanisms, robustness checks, or novelty. A missing input becomes a marked gap or a scoped research task.

## Drafting

Use the structure appropriate to the paper rather than forcing fixed headings. Ensure that:

- the title and abstract report the actual question, method, main result, scope, and uncertainty;
- the introduction connects motivation, question, contribution, closest literature, result, and roadmap without overstating novelty;
- the literature review is organized by claims and differences, not one paragraph per paper;
- theory separates primitives, assumptions, definitions, propositions, intuition, proof status, and welfare or comparative-static scope;
- empirical sections distinguish estimand, assignment mechanism, data construction, estimator, inference, diagnostics, robustness, and external validity;
- structural work reports identification, moments, computation, fit, sensitivity, and counterfactual assumptions;
- conclusions do not introduce new evidence or exceed the identified population, model class, or proof status;
- LaTeX deliverables pass the compile, log, page-render, and independent visual-review gates in [latex_validation.md](latex_validation.md). Prefer redesigning or splitting wide tables, calibrated columns, `tabularx`, `longtable`, or landscape floats; use `\resizebox` only when readability survives review.

Read [data_acquisition.md](data_acquisition.md) before writing or revising any data section. Put `[claim:CLAIM_ID]` beside material Markdown claims and `[data:DATA_ID]` where a dataset or proxy is introduced or materially interpreted. Use the project's citation manager; verify citation metadata and page, theorem, table, or appendix locators against primary sources.

## Whole-manuscript argument audit

Before delivery, read the paper as one argument rather than isolated prose. Put only the 5–15 conclusion-carrying claims in the manifest argument graph using `premise_ids`, `role`, `central`, `status`, `scope`, and `uncertainty`; do not copy the manuscript into the graph. Produce a compact claim map and test:

1. Does every conclusion answer the stated question and follow from named premises, evidence, or proved results?
2. Is causal, welfare, equilibrium, identification, novelty, or generality language stronger than the design or theorem permits?
3. Are maintained assumptions presented as assumptions rather than findings, and are the conclusion-carrying ones defended?
4. Do abstract, introduction, results, tables/figures, and conclusion report consistent samples, signs, magnitudes, uncertainty, definitions, and proof status?
5. Are plausible competing explanations, counterexamples, null results, failed paths, and limitations represented fairly?
6. Can a reader reconstruct the data and analysis from the cited sources, transformations, code, environment, and manifest links?
7. Is any proxy result confined to `proxy_only` claims and described as synthetic or proxy everywhere it appears?

Classify each central claim as supported, provisional, contradicted, or unsupported. Revise wording to the strongest defensible statement; do not repair a logical gap with rhetoric. Run the deterministic manifest audit with `--require-argument-graph` and the manuscript audit with `--require-central-claims`, adding `--require-data-markers` for empirical or structural papers.

Only after those gates pass, dispatch a fresh-context `logic-referee` agent with the frozen question, manuscript, manifest, deterministic reports, necessary tables/figures, and file hashes—but none of the author's reasoning, confidence, or prior handoffs. It reviews each central claim's weakest link, scope or number mismatch, competing explanation, and required revision without editing the manuscript. The PI adjudicates every finding, revises or downgrades claims, and reruns both gates after material changes. Structural graph validity and referee review reduce logical errors; neither constitutes a formal proof that natural-language entailment is correct.

The referee returns one compact JSON object, not a rewritten paper or chain-of-thought. Include `reviewed_sha256` for `manuscript` and `manifest`; `overall_verdict` (`pass`, `revise`, or `reject`); string-list `global_gaps`; string `uncertainty`; and exactly one `claim_reviews` item per central claim. Each item contains `claim_id`, `verdict` (`coherent`, `revise`, `unsupported`, or `uncertain`), and short strings for `weakest_link`, `scope_or_number_mismatch`, `competing_explanation`, and `required_revision`.

Validate freshness and coverage before accepting the handoff:

```bash
python3 scripts/check_logic_review.py \
  --manuscript manuscript.md \
  --manifest research/manifest.jsonl \
  --review research/logic-review.json --json
```

A passing report requires current hashes, every central claim exactly once, no global gap, no required revision, and a `coherent` verdict for each claim. After any manuscript or manifest change, the old review is stale. Keep detailed notes outside the active context; pass only claim-level decisions, artifact paths, and unresolved uncertainty to the PI.
