# Research-question survey gate

Read this reference at the start of a new research question, before choosing an empirical design, structural model, or theorem strategy. Skip only when the user explicitly requests replication of a named work or supplies a current, auditable survey; record that basis.

## Normalize and search

Translate the initial question into the population or model class, outcome or target theorem, treatment/exposure or mechanism, candidate estimand, setting, and time horizon. Preserve the user's original wording alongside the normalized form.

Freeze a search cutoff and scope. Search several formulations rather than the exact title phrase:

- question and outcome/exposure synonyms;
- proposed mechanism and competing mechanisms;
- candidate estimands, designs, or proof concepts;
- population, institution, geography, period, and data source;
- backward references from close works and forward citations to them.

Use discovery indexes to find candidates, then verify bibliographic metadata and substantive comparisons against primary papers or credible working papers. An abstract-only or inaccessible work remains explicitly limited. Absence from one database is not evidence of novelty.

## Nearest-work matrix

For each close work record a canonical HTTPS locator to the DOI, publisher, working-paper archive, or official repository; a free-form citation is not verification. Bind the checked metadata or saved landing-page record through `source_evidence_artifact` and `source_evidence_sha256`. Also record its question, estimand or theorem, design or proof method, mechanism, data/model class, scope, main result, and exact difference from the proposal. Mark at least one nearest alternative and classify the relationship as `duplicate`, `replication`, `extension`, `external-validity`, `adjacent`, or `contradiction`.

Compare differences that can support a contribution: a distinct question, new credible variation, new data measurement, relaxed or sharper assumptions, new mechanism, materially broader scope, external-validity test, or informative replication. A different country, sample, estimator, or recent period is not automatically a contribution; explain why it changes what can be learned.

## Decision gate

Write `research/topic-survey.json` and validate it:

```bash
python3 scripts/check_topic_survey.py research/topic-survey.json --root . --json
```

Choose one decision:

- `proceed`: sufficiently distinct under the recorded search, with a bounded contribution statement;
- `reframe`: closest work absorbs the original claim but a defensible different estimand, mechanism, data advantage, or scope remains;
- `replicate`: the value is verification, transportability, or correction rather than novelty;
- `stop`: the proposed contribution is duplicated or not decision-relevant;
- `blocked`: coverage, access, or institutional information is insufficient.

Use contribution class `distinct-under-search`, never “proven novel.” Preserve search limitations. A duplicate cannot proceed unchanged, and zero verified close works yields `blocked`/`unresolved`, not a novelty claim. Freeze an accepted survey decision in the research contract before entering the method router or main research loop.
