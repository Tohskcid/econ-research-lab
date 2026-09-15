# Data discovery, verification, and proxy protocol

Read this reference when a research question needs new data or when a manuscript describes data provenance.

## Define the requirement before searching

Translate the estimand or model into a data requirement: unit, population, geography, period, frequency, outcome, treatment or exposure, covariates, linkage keys, required sample size, and acceptable access or license. Separate indispensable fields from useful fields. Record the search date and stopping rule.

## Discover and verify real data

Search automatically within the research contract. Prefer official statistical agencies, administrative owners, first-party repositories, documented APIs, and established archives; use aggregators only to discover the original source. Search dataset registries, replication packages, paper supplements, code repositories, and cited data documentation with synonyms for the variables and population.

Before acquisition, verify each candidate against the original landing page and codebook:

- producer, canonical locator, version or release, access date, license, access restrictions, and update/revision policy;
- unit of observation, variable definitions, coverage, sampling frame, missingness conventions, geography/time compatibility, and stable identifiers;
- whether a paper or repository transformed the source and whether those transformations are reproducible;
- file integrity with a checksum when downloaded, without placing restricted or copyrighted data in Git.

Do not infer a license, population, frequency, or variable definition from a filename or aggregator description. Mark inaccessible or unverified candidates explicitly. Record an accepted source as a `dataset` object in the research manifest and link every consuming run with `data_ids`.

## Fallback when no adequate data are available

After the stopping rule is reached, create proxy data automatically when it can advance feasibility, code, estimator, power, or failure-mode testing. Use the closest defensible rung:

1. lawful public aggregates or a related population, clearly labeled as a proxy;
2. synthetic observations calibrated to documented ranges or published moments;
3. an explicit hypothetical DGP when no empirical calibration is available.

Write a project-local generator with a fixed seed, data dictionary, units, support, dependence structure, missingness, and sample size. Preserve the generator, parameters, seed, and output path. Add tests for schema, support, deterministic reproduction, and the feature the proxy is meant to exercise. Record it as a `proxy` object in the manifest.

Never silently replace unavailable real data. Prefix or annotate proxy artifacts clearly and state what empirical features they do not reproduce. Proxy results may support engineering or method claims only. A manuscript claim linked to proxy data must be scoped `proxy_only`; it cannot establish prevalence, magnitude, causal effects, external validity, or policy conclusions about the real population. If no defensible proxy can exercise the required mechanism, deliver the schema and acquisition gap and mark substantive estimation blocked.

## Data-section handoff

The manuscript must explain the producer and access route, version/date, unit and sample construction, period/geography, variables and transformations, linkage, exclusions, missingness, weights, revisions, license or disclosure restrictions, and reproducibility artifacts. For proxy data, also disclose why real data were unavailable, calibration sources, DGP, seed, intended use, and the prohibition on real-world interpretation.
