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
- conclusions do not introduce new evidence or exceed the identified population, model class, or proof status.

Read [data_acquisition.md](data_acquisition.md) before writing or revising any data section. Put `[claim:CLAIM_ID]` beside material Markdown claims and `[data:DATA_ID]` where a dataset or proxy is introduced or materially interpreted. Use the project's citation manager; verify citation metadata and page, theorem, table, or appendix locators against primary sources.

## Whole-manuscript argument audit

Before delivery, read the paper as one argument rather than isolated prose. Produce a compact claim map and test:

1. Does every conclusion answer the stated question and follow from named premises, evidence, or proved results?
2. Is causal, welfare, equilibrium, identification, novelty, or generality language stronger than the design or theorem permits?
3. Are maintained assumptions presented as assumptions rather than findings, and are the conclusion-carrying ones defended?
4. Do abstract, introduction, results, tables/figures, and conclusion report consistent samples, signs, magnitudes, uncertainty, definitions, and proof status?
5. Are plausible competing explanations, counterexamples, null results, failed paths, and limitations represented fairly?
6. Can a reader reconstruct the data and analysis from the cited sources, transformations, code, environment, and manifest links?
7. Is any proxy result confined to `proxy_only` claims and described as synthetic or proxy everywhere it appears?

Classify each central claim as supported, provisional, contradicted, or unsupported. Revise wording to the strongest defensible statement; do not repair a logical gap with rhetoric. Run the deterministic manifest and manuscript audits, adding `--require-data-markers` for empirical or structural papers, then conduct the shared referee checkpoint. Deliver the manuscript together with unresolved gaps, material changes, and claims that still require author judgment.
