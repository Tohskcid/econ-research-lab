# External agent evaluation adapter

Read this reference only when evaluating or evolving the skill. The core remains model- and platform-neutral: an external host invokes the agent, while this repository supplies frozen cases and deterministic graders.

For each run, preserve skill commit, case ID, model and reasoning configuration, tool permissions, environment, token count, wall time, exit status, final answer, and artifact paths. Use a clean workspace and do not expose grader expectations or release holdouts to the acting agent.

Public DGP development cases can be generated with:

```bash
python3 scripts/run_dgp_evals.py generate --out-dir path/to/fixtures
```

Give the agent only the generated manifest, named CSV, prompt, and this submission contract:

```json
{"case_id":"...","decision":"...","findings":["..."],"estimate":0.0}
```

Collect one JSON object per case and grade it with:

```bash
python3 scripts/run_dgp_evals.py grade --results path/to/submissions.jsonl
```

An executable adapter can run the complete public loop. It receives one request as JSON on stdin and must print exactly one submission JSON object on stdout:

```bash
python3 scripts/run_dgp_evals.py run \
  --adapter path/to/agent-adapter \
  --work-dir path/to/run \
  --output path/to/report.json
```

The adapter owns provider authentication, model invocation and trajectory capture. Keep secrets and provider SDKs outside this skill.

These public cases detect basic design failures and output-contract regressions; they are not a research-quality benchmark and can be gamed if their expected answers are exposed. Keep release cases and DGP truth outside the repository. Use `run_skill_evals.py` separately for independently observed behavioral gates. Never let the candidate skill grade its own prose.
