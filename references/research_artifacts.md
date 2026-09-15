# Research artifacts and deterministic gates

Read this reference when a project lacks an artifact convention, when auditing a manuscript, or when evolving this skill. Prefer the project's existing equivalent when it preserves the same links.

## Provenance graph

Use `research/manifest.jsonl` when stronger traceability than the compact experiment ledger is needed. Write one JSON object per line with a unique `id` and one of these types:

- `hypothesis`: `statement`, `falsifier`;
- `experiment`: `hypothesis_id`, `validation`;
- `run`: `experiment_id`, `harness_version`, `status`, `artifact`; add commit, input hash, seed, and environment when material;
- `evidence`: `source`, `locator`, `verified_at`; add DOI/version, access status, scope, and `relation` (`supports`, `contradicts`, or `qualifies`) when available;
- `finding`: `statement`, `run_ids`, `status`;
- `claim`: `statement` plus at least one `evidence_ids` or `finding_ids` link.

IDs are immutable. Never rewrite a failed run or redirect an old ID to a new object. A changed harness creates a new baseline. Validate links with:

```bash
python3 scripts/validate_research_manifest.py research/manifest.jsonl
```

## Literature evidence bank

Represent the literature map with `evidence` and `claim` records rather than summaries alone. Preserve the query, database, cutoff date, version, page/theorem/table locator, inclusion reason, and whether full text was checked. Record contradictions directly; do not collapse them into a consensus paragraph.

For prospective idea evaluation, freeze a historical literature cutoff before generating hypotheses and use later publications only for evaluation. Do not use a future-paper match as proof that a hypothesis was correct or novel.

## Manuscript traceability

Put `[claim:CLAIM_ID]` beside material claims in Markdown. Run:

```bash
python3 scripts/audit_claims.py manuscript.md research/manifest.jsonl
python3 scripts/audit_claims.py manuscript.md research/manifest.jsonl --strict-numbers
```

The strict option flags prose paragraphs containing numbers but no marker. It is a conservative screening aid: inspect false positives, tables, equations, citations, and generated formats manually. A valid marker proves only that a link exists; the referee checkpoint must still judge whether the evidence supports the wording.

## Skill evals

`evals/cases.jsonl` contains public development cases. An independent evaluator or deterministic artifact check produces JSONL records of the form:

```json
{"case_id":"empirical-panel","gates":["contract","estimand-frozen"],"token_count":1200}
```

Aggregate them with:

```bash
python3 scripts/run_skill_evals.py --results path/to/results.jsonl
```

The runner aggregates observed gates; it does not decide that a gate is true. Keep release holdouts outside the public skill, freeze graders before candidate runs, and retain per-mode hard gates instead of optimizing one score.
