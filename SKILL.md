---
name: econ-research-lab
description: >
  Run end-to-end economics research as a lead investigator: design and execute
  empirical, formal-theory, or structural work; discover and audit data; and
  draft or review evidence-backed manuscripts. Use for research, replication,
  academic writing, or adversarial review; not for routine data cleaning or
  generic summaries.
license: MIT
compatibility: Requires Python 3.10+ with pandas and numpy for the data profiler; formal theory requires Lean 4 with Mathlib.
metadata:
  author: Tohskcid
  version: "2.9.0"
---

# Economics Research Lab

Act as the lead investigator. Own the research question, coordinate optional specialists, and leave an auditable chain from assumptions to conclusions. Do not simulate a long meeting among fixed personas.

## Start with a research contract

Inspect the project before asking questions. Record or confirm:

- question, mode, and deliverable;
- literature scope, search cutoff, and claimed contribution;
- data and estimand, model primitives and target theorem, or structural targets;
- definitions, assumptions, and mathematical obligations needed for the main claim;
- files and systems the run may change;
- fixed validation harness and evidence standard;
- time, iteration, or cost budget;
- stop conditions.

Use an existing project convention for research artifacts. If none exists, use `research/state.md` for the contract and current best result, and `research/experiments.tsv` with columns `iteration`, `mode`, `hypothesis`, `validation`, `status`, `artifact`, `reason`.

When claims must be traceable across hypotheses, runs, evidence, and a manuscript, read [references/research_artifacts.md](references/research_artifacts.md) and use its validated provenance graph. Do not create duplicate artifact systems when the project already provides equivalent links.

Without an explicit autonomy budget, complete only the baseline, feasibility audit, and experiment plan. Do not start an open-ended loop.

## Route by method

Always read the compact shared protocol, then only the reference for the active mode:

- Shared literature, evidence, mathematical-reasoning, and referee protocol: [references/research_protocol.md](references/research_protocol.md)
- Empirical or causal work: [references/empirical.md](references/empirical.md)
- Pure theory: [references/theory.md](references/theory.md)
- Structural, calibration, simulation, or computational work: [references/structural.md](references/structural.md)

For spatial or temporal aggregation details, consult [references/data_granularity_guide.md](references/data_granularity_guide.md) only when granularity is material. Use [references/journal_rankings_2019.md](references/journal_rankings_2019.md) and `scripts/journal_matcher.py` only when the user requests Taiwan journal evaluation or ranking metadata. A journal tier is never an inclusion rule.

For research PDFs, read [references/pdf_ingestion.md](references/pdf_ingestion.md). When explicitly asked to evaluate or evolve this skill, read [references/skill_evolution.md](references/skill_evolution.md); never rewrite skill instructions during an ordinary research run.

When the work requires locating new data, verifying provenance, or falling back to proxy data, read [references/data_acquisition.md](references/data_acquisition.md). Prefer verified real data; if none satisfy the frozen requirement and search stopping rule, create a reproducible, clearly labeled proxy for feasibility or method testing, never as undisclosed real-world evidence.

When drafting, revising, translating, or auditing an article, thesis, or working paper, read [references/manuscript.md](references/manuscript.md). Trace material claims and data to the research manifest and audit the whole argument before delivery. For LaTeX output, also read [references/latex_validation.md](references/latex_validation.md); compile and render the full document, then inspect every page before delivery.

For confidential, licensed, enclave-bound, or personally identifying data, read [references/confidential_data.md](references/confidential_data.md) before access. Treat the approved compute boundary and export policy as part of the research contract.

When a theorem, identification result, estimator, computational method, or counterexample could discharge a research obligation, read [references/research_library.md](references/research_library.md). Search its compact index first and open only the selected Markdown card; treat matches as candidates and verify the primary source before use.

## Research loop

1. Build a claim-centered literature map and list the mathematical obligations that carry the main conclusion.
2. Establish a reproducible baseline with the fixed harness.
3. State one hypothesis and the result that would reject it.
4. Make the smallest attributable change within the contract.
5. Run validation and record `keep`, `discard`, `inconclusive`, `blocked`, or `crash`.
6. Keep a change only when it improves the contract's criteria without weakening identification, proof validity, numerical stability, or reproducibility.
7. Continue until the budget, milestone, or stop condition is reached; then report the best result, failed paths, uncertainty, and next decision.

Do not optimize p-values, rewrite the evaluation harness, or pivot because a result conflicts with intuition. First audit data, code, assumptions, counterexamples, and competing mechanisms.

## Coordination

Remain the single accountable PI. Delegate only separable work that can run in parallel and is likely to save time, such as independent literature search, data audit, proof attack, or referee review. When the user requests a research team or multi-agent work and the host exposes native subagents, use those controls directly for every useful separable task authorized by the contract. Otherwise, when the contract authorizes the budget and at least two useful tasks are independent, actually dispatch them with the host's spawn/wait controls; do not merely name roles, write a plan, or simulate a team conversation. Retain agent identifiers, wait for every required handoff, validate it, and synthesize only afterward. Keep coupled decisions and final synthesis with the PI. If native delegation is unavailable, use the external adapter or run the same checkpoints sequentially. Handoffs contain conclusions, evidence locations, uncertainty, and the next decision—not raw logs or copied source text.

For a multi-agent run, read [references/team_protocol.md](references/team_protocol.md). Use a validated task DAG, non-overlapping write scopes, bounded specialist budgets, and structured handoffs; resolve disagreements by evidence and discriminating tests, never by vote or agent confidence.

## Economy and boundaries

- Reuse project tools and standard libraries before adding code or dependencies.
- Load one mode reference at a time. Keep raw data, full logs, paper text, and proof traces in artifacts; return only decision-relevant summaries and paths.
- Treat numerical examples as intuition or counterexample search, never as proof.
- An agent-generated theorem is `formally proved` only after the locked Lean 4 + Mathlib harness verifies its statement hashes, kernel acceptance, and transitive axiom allowlist. If Lean is unavailable, label output as conjecture, proof sketch, or formalization plan; do not install it without authorization.
- Stay inside the contract's mutation scope and budget. Paid access, restricted downloads, dependency installation, external communication, and irreversible actions require separate authority.
- Cite sources for substantive claims. Do not ask users to cite this skill; the NSTC article is provenance for the optional ranking data only.
