# Dream-RSI: Recursive Self-Improvement through Evolving Worlds

This reference defines the **Dream-RSI protocol** for economics research: converting accumulated discovery history into an exact replay simulator, enabling offline dreaming over candidate exploration and specification policies at zero execution cost, and continuously expanding the simulator pool across iterations and projects.

Based on *Dream-RSI: Recursive Self-Improvement through Evolving Worlds* (Google DeepMind, UMD, UVA, 2026; https://www.dream-rsi.com/).

---

## 1. The Core Principle

In long-horizon economics research (e.g., exploring high-dimensional Spatial DML specifications, tuning structural contraction mappings, or searching Lean 4 formal theory proof tactics), the central bottleneck is that **meta-level exploration feedback is delayed and expensive**. Running a single high-dimensional econometric specification or full structural counterfactual rollout takes minutes to hours.

**The Dream-RSI Insight**:
1. **History is already an exact simulator**: An empirical discovery run is not just dead text or a one-line result in `results.json`. It is a structured DAG (Discovery Tree) of every specification attempt, carrying its realized dataset slice, first-stage $F$-statistic, Neyman orthogonal score, Conley HAC standard errors, runtime, and convergence diagnostic.
2. **Zero-Execution Dreaming**: An alternative exploration policy (e.g., how to prune fragile covariates, what spatial lag order to test, when to stop serial search) does not need to re-execute Stata, R, or Python scripts. It replays the recorded discovery tree in memory at **zero execution cost**.
3. **Evolving World Pool**: Every completed research iteration records another discovery tree—adding one more "world" to the simulator pool. Policies dreamt across a growing pool of worlds beat policies tuned to a single run, and bring back discoveries no earlier policy could reach.

---

## 2. Discovery Tree Schema (`research/discovery_tree.jsonl`)

Every econometric exploration step is appended to `research/discovery_tree.jsonl` as a self-contained node:

```json
{
  "node_id": "spec-node-042",
  "parent_id": "spec-node-031",
  "timestamp": "2026-09-18T23:30:00Z",
  "action": "expand_spatial_lag",
  "specification": {
    "estimator": "Spatial_DML",
    "spatial_matrix": "W_345kV_topological",
    "lag_order": 2,
    "controls_subset": ["fiber_density", "water_stress", "zoning_stringency", "cdd"],
    "learner": "RandomForest_min_samples_leaf_5"
  },
  "metrics": {
    "direct_effect": -0.00323,
    "direct_se": 0.00095,
    "indirect_effect": 0.04234,
    "indirect_se": 0.00812,
    "first_stage_f": 3096.5,
    "rho": 0.7941,
    "wall_clock_seconds": 184.2,
    "gate_status": "pass"
  },
  "referee_vulnerabilities": [
    "greg_mechanical_correlation",
    "macro_transformer_supply_shock"
  ]
}
```

---

## 3. The Offline Replay Simulator

Given a recorded discovery tree $\\mathcal{T} = (\\mathcal{V}, \\mathcal{E})$, an exploration policy $\\pi_\\theta(a \\mid s)$ maps current search state $s$ (observed point estimates, stability metrics, computational budget remaining) to the next search decision $a \\in \\mathcal{A}$ (branch, prune, switch instrument, stop).

Because all node outcomes in $\\mathcal{V}$ are pre-computed:
$$\\text{Score}(\\pi_\\theta) = \\sum_{v \\in \\text{Traverse}(\\pi_\\theta, \\mathcal{T})} R(v) - \\lambda \\cdot \\text{Cost}(v)$$
Evaluating $\\text{Score}(\\pi_\\theta)$ requires **zero code executions**. A meta-agent can dream through $10^4$ candidate exploration and pruning policies in milliseconds, identifying:
- **Optimal Specification Curve Pruning**: Which model specifications maximize Neyman orthogonality without inflating standard errors?
- **Robustness Boundary Detection**: Under which covariate subsets does the treatment effect sign flip?
- **Computational Budget Allocation**: When should the agent stop serial exploration and commit to the primary manuscript specification?

---

## 4. Evolving Worlds & Cross-Project Transfer

When opening a new project in the economics research lab:

| Layer | Behavior on New Project | Role in Recursive Self-Improvement |
|---|---|---|
| **Discovery Tree (Local World)** | Re-grows from root node | Captures the new empirical setting, network topology, and institutional data primitives. |
| **Meta-Policy (Exploration Engine)** | **Transferred & Inherited** | Uses pre-trained exploration instincts (pruning heuristics, search order) to discover viable models 5–10x faster. |
| **Adversarial Pool (Referee Attacks)** | **Globally Persistent** | Retains historical referee attacks (GREG non-spatial audits, physical bypass checks, survivorship biases) so new projects pass Day 1 defenses. |

---

## 5. Verification Gate Integration

The Dream-RSI replay simulator is verified via:
1. `python3 scripts/dream_replay_simulator.py --tree research/discovery_tree.jsonl --audit`: confirms discovery tree integrity, topological DAG validity, and determinism.
2. `python3 scripts/dream_replay_simulator.py --spec-curve --dream`: evaluates offline specification curves over historical discovery nodes at zero execution compute.
