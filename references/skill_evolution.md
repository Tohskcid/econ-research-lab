# Skill evolution protocol

Use only when the user explicitly asks to evaluate or evolve `econ-research-lab`. This adapts SkillRL's experience distillation and failure-driven evolution without requiring SFT or reinforcement learning.

## Fixed evaluation

Freeze a versioned baseline, representative development cases, hidden holdout cases, graders, token accounting, and stop budget. Use hard validity gates before soft scores:

- empirical: estimand, identification, inference, and no p-value optimization;
- theory: explicit assumptions, counterexample search, proof status, and Lean acceptance when formal proof is claimed;
- structural: convergence, identification, holdout fit, and reproducibility;
- literature/PDF: claim-source support and visual verification of proof-critical transcriptions.

Do not optimize a single aggregate score across failed validity gates.

Use the schema and commands in [research_artifacts.md](research_artifacts.md). Public development cases live in `evals/cases.jsonl`; keep release holdouts outside the public repository. The eval runner aggregates gates observed by an independent evaluator or deterministic artifact checks and must not treat an agent's unsupported self-report as evidence.

For host integration and public DGP checks, read [eval_adapter.md](eval_adapter.md). Keep model invocation in a thin external adapter rather than adding a provider SDK to this skill.

## Candidate loop

1. Run the baseline and retain compact success and failure records, not raw trajectories.
2. Distill recurring decision errors, missing scope conditions, and useful successful strategies.
3. Map general rules to `SKILL.md`, mode-specific rules to one reference, and recurring failures to a validity gate or behavioral case.
4. Propose one minimal attributable patch. Do not change the grader or holdout to favor it.
5. Rerun development and holdout cases. Keep only if the target failure improves, no hard gate regresses, and token cost remains justified; otherwise discard or mark inconclusive.
6. Record the diff, scores, reason, and version in the ledger. Require review before promotion or push.

Do not modify the live skill during a research run. Do not start model training, paid evaluation, dependency installation, or open-ended evolution without an explicit budget and authority. Consider full SkillRL only after enough reliably graded trajectories and suitable compute exist.
