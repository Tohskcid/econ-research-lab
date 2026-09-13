# Econ Research Lab

`econ-research-lab` is an Agent Skill for running auditable economics research with one accountable lead agent and optional specialist delegation. It supports empirical research, Lean-verified pure theory, and structural or computational work.

The design adapts two useful ideas:

- [autoresearch](https://github.com/karpathy/autoresearch): freeze the evaluation harness, establish a baseline, test one attributable change, and keep an experiment ledger.
- [ponytail](https://github.com/dietrichgebert/ponytail): reuse what exists and add only the smallest solution that survives validation.

Unlike a model-training benchmark, economics rarely has one sufficient score. The research contract therefore fixes mode-specific validity gates before iteration; statistical significance is never the optimization target.

## Workflow

1. Define the research contract and autonomy budget.
2. Route to empirical, theory, or structural/computational guidance.
3. Establish a reproducible baseline.
4. Iterate through hypothesis → minimal test → validation → ledger.
5. Deliver the best result, rejected paths, uncertainty, and reproducibility instructions.

The lead agent may delegate independent searches or audits when the host supports subagents. It otherwise performs the same checkpoints sequentially.

## Installation

Place this directory at a skill-discovery path supported by the client, for example:

```text
.agents/skills/econ-research-lab/
```

The core follows the [Agent Skills specification](https://agentskills.io/specification) and contains no client-specific orchestration requirements.

## Optional command-line tools

Install the profiler dependencies inside a virtual environment:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
```

Profile a panel and generate descriptive binned means:

```bash
.venv/bin/python scripts/econ_data_profiler.py \
  --data data.csv --id unit_id --time year \
  --x treatment --y outcome --latex --out-dir output
```

The chart is descriptive unless variables have already been residualized outside the tool.

Query the optional 2019 Taiwan NSTC journal metadata:

```bash
python3 scripts/journal_matcher.py --check "AER"
```

The ranking does not determine whether evidence is relevant or credible. Its source is 林明仁、林常青、張俊仁、曹添旺、楊浩彥（2021），〈經濟學門學術期刊評比更新：2019 年〉，《經濟論文叢刊》，49(3), 395–442.

Verify a Lean theorem before labeling it formally proved:

```bash
python3 scripts/check_lean_proof.py path/to/Theorem.lean
```

## Validation

```bash
uvx --from skills-ref agentskills validate "$(pwd)"
python3 -m unittest discover -s tests -v
```

## Structure

```text
SKILL.md                    short router and research loop
references/empirical.md    empirical validity gates
references/theory.md       Lean-backed theory workflow
references/structural.md   structural/computational workflow
references/research_protocol.md  evidence and review protocol
scripts/                    optional deterministic utilities
tests/                      CLI and invariant checks
```

MIT licensed.
