# Economics result-card library

This directory is a small, versioned solution index—not a PDF archive and not an authority. It helps an agent move from a research obligation to candidate theorems, identification results, estimators, algorithms, and known failure conditions.

Files:

- `catalog.jsonl`: paper metadata and source links;
- `index.jsonl`: compact searchable fields and paths only;
- `papers/*.md`: one reusable result card per file, loaded only after selection;
- `relations.jsonl`: typed links among result cards.

Search by the problem to solve:

```bash
python3 scripts/search_library.py "monotone optimal choice single crossing" --mode theory
python3 scripts/search_library.py "staggered adoption heterogeneous effects" --mode empirical
python3 scripts/search_library.py "dynamic discrete choice computation" --mode structural
python3 scripts/search_library.py --show rust-nested-fixed-point
```

Search returns three compact candidates by default. Open only the selected card with `--show`; use `--limit 5` only when needed. For a blind reconstruction, combine `--show CARD_ID --blind`. It removes proof and author-solution sections from output. The research protocol also requires the agent not to open the underlying Markdown directly until its independent attempt is saved.

Validate the database after every edit:

```bash
python3 scripts/validate_library.py
```

The cards record canonical solution routes and core assumptions, not exhaustive theorem statements. `verification` describes how closely the card was checked against the source; it does not certify that the result applies to a new model. Before use, inspect the primary source, reconstruct the assumption mapping, and record any mismatch. Do not commit copyrighted PDFs or restricted material.
