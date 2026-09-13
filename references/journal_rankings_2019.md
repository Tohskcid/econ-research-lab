# 2019 Taiwan NSTC economics journal metadata

Load this reference only when the user explicitly requests Taiwan journal evaluation or the 2019 ranking. It is metadata, not an evidence-quality rule or a literature inclusion filter.

## Provenance

林明仁、林常青、張俊仁、曹添旺、楊浩彥（2021），〈經濟學門學術期刊評比更新：2019 年〉，《經濟論文叢刊》，49(3), 395–442。

The year 2019 identifies the ranking update; 2021 is the article's publication year. Mention the source when explaining where the metadata came from, but never instruct a user to cite this skill.

## Usage

```bash
python3 scripts/journal_matcher.py --check "Journal of Finance"
python3 scripts/journal_matcher.py --list-tier "Excellent"
python3 scripts/journal_matcher.py --list-tier "A+" --json
```

The local snapshot covers the source's Excellent, A+, and A lists plus the bundled TSSCI aliases. Verify the source again before using the result in a formal institutional evaluation. A missing or fuzzy match does not imply a lower rank.
