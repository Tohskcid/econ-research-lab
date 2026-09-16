# Research-team orchestration protocol

Read this reference when the host can run multiple agents or when a research project has separable specialist tasks. The lead investigator remains the single PI and final decision-maker. Roles are temporary capabilities, not fixed simulated personas.

## When to delegate

Delegate only when a task has a bounded objective, explicit inputs, an independently checkable output, and little need for continuous shared context. Good candidates include literature search, data-source audit, replication, proof or counterexample attack, robustness analysis, and blind referee review. Keep coupled model decisions, final interpretation, and scope changes with the PI.

Execution priority is:

1. host-native subagents when available and authorized;
2. the external adapter runner when native delegation is unavailable;
3. sequential PI execution when neither is available.

Do not report a multi-agent run unless distinct agent contexts actually executed tasks. A list of personas, an imagined meeting, or one model writing several role-labeled paragraphs is not multi-agent collaboration.

Create a JSON task plan with one accountable PI and a directed acyclic graph:

```json
{
  "contract_id": "project-001",
  "pi": "lead-investigator",
  "tasks": [
    {
      "id": "literature",
      "role": "literature-auditor",
      "objective": "Map the nearest claims and contradictions",
      "depends_on": [],
      "inputs": ["research/state.md"],
      "write_scope": ["research/literature"],
      "validation": ["primary locators present", "search limits reported"],
      "budget": {"max_seconds": 600}
    }
  ]
}
```

Use `write_scope` for paths an agent may change, not paths it may merely read. Independent tasks must not have overlapping write scopes. Put potentially conflicting work in separate paths and let a later PI task compare it; never let agents race to edit the manuscript or state file. The runner checks declared scopes and returned artifact paths; the host adapter must enforce the actual filesystem sandbox or worktree boundary.

Validate or execute with:

```bash
python3 scripts/run_research_team.py validate research/team-plan.json
python3 scripts/run_research_team.py run research/team-plan.json \
  --adapter path/to/agent-adapter --work-dir research/team-run --max-workers 4
```

## Native subagent execution

When the host provides spawn, message, interrupt, and wait controls, the PI performs the DAG directly:

1. Validate the plan, retain coupled work locally, and identify the dependency-ready wave.
2. Spawn at most the authorized concurrency limit and retain the returned agent identifier beside the task ID. Give each specialist its task object, exact allowed inputs and write scope, relevant mode reference, validation gates, budget, and handoff schema. Do not send unrelated conversation history, other agents' conclusions, or the entire library.
3. Use separate worktrees or non-overlapping artifact paths when the host supports them. Never assign simultaneous edits to the same manuscript, state, data, or code file.
4. Wait for completions through the host's native wait mechanism rather than polling or narrating unchanged status. Record each returned handoff. Do not deliver the research result while any required agent is still running. An invalid or incomplete handoff gets at most one bounded correction request; otherwise mark the task failed.
5. Dispatch the next ready wave only after dependencies complete. A failed or blocked dependency blocks its descendants until the PI revises and revalidates the plan.
6. For blind replication, proof attack, or referee review, create a fresh or limited context rather than inheriting the full PI conversation. Pass only the frozen question, permitted definitions or inputs, raw artifacts, and validation harness—not the originating reasoning, conclusion, or confidence—until the independent handoff is saved.
7. After all reachable tasks stop, the PI compares evidence, resolves disagreements with a discriminating test when possible, updates the research manifest, and writes the final synthesis. Specialists never approve their own result or change the contract.

The PI should use native controls itself; do not ask the user to open, monitor, or relay messages between agents. If the host cannot create distinct contexts, state that limitation and use the fallback rather than claiming a team run.

## External adapter fallback

Set `--max-workers 1` for sequential fallback. The adapter receives one JSON request on stdin and returns exactly one JSON handoff on stdout. Provider credentials, model settings, agent creation, and trajectory capture stay in the adapter:

```json
{
  "task_id": "literature",
  "status": "complete",
  "summary": "Decision-relevant conclusion only",
  "evidence_ids": ["E1"],
  "artifacts": ["research/literature/map.md"],
  "uncertainty": "Coverage is limited before 1990",
  "blockers": [],
  "recommended_next": "PI should compare E1 with the proposed contribution"
}
```

The runner executes dependency-ready tasks concurrently, applies each task timeout, blocks downstream tasks after a failed or blocked dependency, and writes individual handoffs, `events.jsonl`, and `report.json`. Import accepted findings and evidence into the existing research manifest; do not duplicate full logs there.

## Context economy

Give each specialist only the contract slice, selected mode reference, IDs, and artifact paths needed for its task. Retrieve a compact index before opening a paper, dataset description, proof trace, render, or log; open the minimum selected artifact and keep bulky content on disk. Handoffs state the decision, evidence IDs or file hashes, uncertainty, blockers, and next action. Do not relay chain-of-thought, copied literature, raw data, full regression output, complete compiler logs, page-by-page prose, or other agents' unchanged handoffs. Deduplicate shared inputs by path and hash, and stop dispatching when another context would not add an independently testable result.

## Independence and decisions

For replication, proof attack, or referee work, withhold the originating agent's reasoning and conclusion until the independent handoff is saved. Give the reviewer the frozen question, permitted inputs, validation harness, and raw artifacts needed to reproduce the claim.

When handoffs disagree, the PI records the disputed claim, differing assumptions or inputs, and a discriminating test. Do not resolve disagreement by vote or agent confidence. Preserve rejected paths and classify the decision under the research contract's evidence standard.

## V1 boundary

The external runner's task graph is static during a run: it does not choose a model, create provider accounts, change the research contract, add tasks to the validated DAG, merge conflicting files, or let specialists approve their own output. This does not prevent the Skill from creating native subagents for tasks already in the plan. Declared write-scope validation is not an operating-system sandbox. The PI may create a new versioned plan after reviewing the report. Paid tools, restricted data, external communication, and expanded mutation scope still require separate authority.
