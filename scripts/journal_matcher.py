#!/usr/bin/env python3
"""Query the optional 2019 Taiwan NSTC economics journal metadata."""

import argparse
import difflib
import json
import re
import unicodedata


TIERS = {
    "Excellent": [
        ("american economic review", "AER"),
        ("econometrica", "ECMA"),
        ("journal of finance", "JF"),
        ("journal of political economy", "JPE"),
        ("quarterly journal of economics", "QJE"),
        ("review of economic studies", "REStud"),
    ],
    "A+": [
        ("american economic journal: applied economics", "AEJ: Applied"),
        ("american economic journal: economic policy", "AEJ: Policy"),
        ("american economic journal: macroeconomics", "AEJ: Macro"),
        ("american economic journal: microeconomics", "AEJ: Micro"),
        ("economic journal", "EJ"),
        ("economic theory", "ET"),
        ("european economic review", "EER"),
        ("experimental economics", "Exp Econ"),
        ("games and economic behavior", "GEB"),
        ("international economic review", "IER"),
        ("journal of accounting and economics", "JAE"),
        ("journal of business and economic statistics", "JBES"),
        ("journal of development economics", "JDE"),
        ("journal of econometrics", "JoE"),
        ("journal of economic growth", "JEG"),
        ("journal of economic history", "JEH"),
        ("journal of economic literature", "JEL"),
        ("journal of economic perspectives", "JEP"),
        ("journal of economic theory", "JET"),
        ("journal of financial and quantitative analysis", "JFQA"),
        ("journal of financial economics", "JFE"),
        ("journal of human resources", "JHR"),
        ("journal of international economics", "JIE"),
        ("journal of labor economics", "JoLE"),
        ("journal of law and economics", "JLE"),
        ("journal of monetary economics", "JME"),
        ("journal of public economics", "JPubE"),
        ("journal of the european economic association", "JEEA"),
        ("journal of urban economics", "JUE"),
        ("quantitative economics", "QE"),
        ("rand journal of economics", "RAND"),
        ("review of economic dynamics", "RED"),
        ("review of economics and statistics", "REStat"),
        ("review of finance", "RF"),
        ("review of financial studies", "RFS"),
        ("theoretical economics", "TE"),
    ],
    "A": [
        ("american journal of agricultural economics", "AJAE"),
        ("brookings papers on economic activity", "BPEA"),
        ("canadian journal of economics", "CJE"),
        ("econometric theory", "EcT"),
        ("economic development and cultural change", "EDCC"),
        ("economic inquiry", "EI"),
        ("economic policy", "EP"),
        ("economica", "Economica"),
        ("health economics", "HE"),
        ("international journal of industrial organization", "IJIO"),
        ("journal of applied econometrics", "JApE"),
        ("journal of banking and finance", "JBF"),
        ("journal of comparative economics", "JCE"),
        ("journal of economic behavior and organization", "JEBO"),
        ("journal of economic dynamics and control", "JEDC"),
        ("journal of economics and management strategy", "JEMS"),
        ("journal of environmental economics and management", "JEEM"),
        ("journal of health economics", "JHE"),
        ("journal of industrial economics", "JIEc"),
        ("journal of international money and finance", "JIMF"),
        ("journal of law economics and organization", "JLEO"),
        ("journal of mathematical economics", "JMathE"),
        ("journal of money credit and banking", "JMCB"),
        ("journal of population economics", "JPopE"),
        ("journal of risk and uncertainty", "JRU"),
        ("macroeconomic dynamics", "MD"),
        ("oxford economic papers", "OEP"),
        ("scandinavian journal of economics", "SJE"),
        ("social choice and welfare", "SCW"),
    ],
    "TSSCI Core": [
        ("經濟論文叢刊", "TER"),
        ("經濟論文", "AEP"),
        ("經濟研究", "ER"),
        ("人文及社會科學集刊", "JSSP"),
        ("經濟預測與政策", "EFP"),
    ],
}

JOURNAL_DB = {
    name: {"tier": tier, "short": short}
    for tier, journals in TIERS.items()
    for name, short in journals
}

ALIASES = {
    "aer": "american economic review", "ecma": "econometrica", "jf": "journal of finance",
    "jpe": "journal of political economy", "qje": "quarterly journal of economics",
    "restud": "review of economic studies", "jbes": "journal of business and economic statistics",
    "joe": "journal of econometrics", "jfe": "journal of financial economics",
    "rfs": "review of financial studies", "ter": "經濟論文叢刊",
    "taiwan economic review": "經濟論文叢刊", "academia economic papers": "經濟論文",
    "journal of social sciences and philosophy": "人文及社會科學集刊",
}


def normalize_name(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold().strip().replace("&", " and ")
    value = re.sub(r"[\u2010-\u2015\-:,.]", " ", value)
    return " ".join(value.split())


NORMALIZED_DB = {normalize_name(name): name for name in JOURNAL_DB}
NORMALIZED_ALIASES = {normalize_name(alias): target for alias, target in ALIASES.items()}


def lookup_candidates(query: str, limit: int = 3, cutoff: float = 0.55):
    q = normalize_name(query)
    if not q:
        return []
    if q in NORMALIZED_ALIASES:
        name = NORMALIZED_ALIASES[q]
        return [(name, JOURNAL_DB[name], 1.0)]
    if q in NORMALIZED_DB:
        name = NORMALIZED_DB[q]
        return [(name, JOURNAL_DB[name], 1.0)]

    partial = []
    for normalized, name in NORMALIZED_DB.items():
        if q == normalize_name(JOURNAL_DB[name]["short"]):
            return [(name, JOURNAL_DB[name], 1.0)]
        if q in normalized:
            partial.append((name, JOURNAL_DB[name], difflib.SequenceMatcher(None, q, normalized).ratio()))
    if partial:
        return sorted(partial, key=lambda item: item[2], reverse=True)[:limit]

    matches = difflib.get_close_matches(q, NORMALIZED_DB, n=limit, cutoff=cutoff)
    return [
        (NORMALIZED_DB[match], JOURNAL_DB[NORMALIZED_DB[match]], difflib.SequenceMatcher(None, q, match).ratio())
        for match in matches
    ]


def lookup_journal(query: str):
    candidates = lookup_candidates(query, limit=1)
    return candidates[0] if candidates else (None, None, 0.0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", "-c", help="Journal name or acronym")
    parser.add_argument("--list-tier", "-l", choices=[*TIERS, "Top 5", "All"])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.list_tier:
        tier = "Excellent" if args.list_tier == "Top 5" else args.list_tier
        results = {name: data for name, data in JOURNAL_DB.items() if tier == "All" or data["tier"] == tier}
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f"\n=== {tier} ({len(results)} journals) ===")
            for name, data in results.items():
                print(f"- {data['short']}: {name.title()}")
        return

    if args.check:
        candidates = lookup_candidates(args.check)
        name, info, score = candidates[0] if candidates else (None, None, 0.0)
        if args.json:
            print(json.dumps({
                "query": args.check, "matched": name, "score": round(score, 3), "info": info,
                "candidates": [
                    {"name": candidate, "score": round(candidate_score, 3), "info": candidate_info}
                    for candidate, candidate_info, candidate_score in candidates
                ],
            }, ensure_ascii=False, indent=2))
        elif info:
            print(f"\nQuery: {args.check}\nMatch: {name.title()} ({info['short']})\nTier: {info['tier']}\nConfidence: {score:.1%}")
            if score < 0.8 and len(candidates) > 1:
                print("Other candidates: " + ", ".join(candidate for candidate, _, _ in candidates[1:]))
        else:
            print(f"\nNot found in this optional 2019 ranking dataset: {args.check}")
            print("No match indicates database coverage or name-matching limits, not a journal tier.")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
